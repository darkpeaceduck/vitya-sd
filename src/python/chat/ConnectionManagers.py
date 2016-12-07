import threading
from abc import abstractmethod
import asyncore
import logging
import socket
from queue import Queue, Empty
import chat.Message as Message
from chat.Message import MessageQueueProcessor
import chat.grpc_serv_pb2 as grpc_serv_pb2
import concurrent.futures as futures
import grpc

class AbstractConnectionManager:
    def __init__(self):
        self.listeners = []
    
    @abstractmethod
    def send(self, msg):
        pass
    
    @abstractmethod
    def connect(self, bind_address, address):
        pass
    
    @abstractmethod
    def listen(self, bind_adress):
        pass
    
    @abstractmethod
    def close(self):
        pass
    
    def addListener(self, listener):
        self.listeners.append(listener)
        
    def noticeListeners(self, event, msg=None):
        for listener in self.listeners:
            method = getattr(listener, event)
            if msg:
                method(msg)
            else:
                method()
        
    def on_sent(self, msg):
        self.noticeListeners("on_sent", msg)

    def on_closed(self):
        self.noticeListeners("on_closed")
        
    def on_connected(self, client):
        self.noticeListeners("on_connected", client)
        
    def on_receive_msg(self, msg):
        self.noticeListeners("on_receive_msg", msg)
        
class SocketAsyncCoreServer(asyncore.dispatcher):
    
    def __init__(self, bind_address, connection_handler):
        self.logger = logging.getLogger('asyncore server')
        asyncore.dispatcher.__init__(self)
        self.connection_handler = connection_handler
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(bind_address)
        self.address = self.socket.getsockname()
        self.logger.debug('binding to %s', self.address)
        self.listen(1)

    def handle_accept(self):
        sock, addr = self.accept()
        self.logger.debug('handle_accept() -> %s', addr)
        self.connection_handler.on_connected((addr, \
                  SocketAsyncCoreClientHandler(sock, self.connection_handler)))
        self.handle_close()
    
    def handle_close(self):
        self.logger.debug('handle_close()')
        self.close()

class SocketAsyncCoreClientHandler(asyncore.dispatcher, MessageQueueProcessor):
    def __init__(self, sock, connection_handler):
        MessageQueueProcessor.__init__(self)
        self.connection_handler = connection_handler
        self.logger = logging.getLogger('clientHandler%s' % str(sock.getsockname()))
        asyncore.dispatcher.__init__(self, sock=sock)
    
    def handle_write(self):
        try:
            msg = self.get_msg()
            data = msg.get_bytes()
            self.send(data)
            self.connection_handler.on_sent(msg)
            self.logger.debug('handle_write() -> data send')
        except Empty:
            self.logger.debug('handle_write() -> msg queue empty')

    def handle_read(self):
        data = self.recv(Message.MESSAGE_MAX_LENGTH)
        self.logger.debug('handle_read() -> (%d) "%s"', len(data), data)
        msg = Message.Message(byte_data=data)
        self.connection_handler.on_receive_msg(msg)
    
    def handle_close(self):
        self.logger.debug('handle_close()')
        self.close()
        self.connection_handler.on_closed()
        
class SocketAsyncCoreClient(asyncore.dispatcher, MessageQueueProcessor):
    def __init__(self, bind_adress, connect_adress, connection_handler):
        MessageQueueProcessor.__init__(self)
        self.connection_handler = connection_handler
        self.logger = logging.getLogger('asynccore client')
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(bind_adress)
        self.address = self.socket.getsockname()
        self.connect_adress = connect_adress
        self.logger.debug('connecting to %s', connect_adress)
        self.connect(connect_adress)
    
    def handle_connect(self):
        self.logger.debug('handle_connect()')
        self.connection_handler.on_connected((self.connect_adress, self))

    def handle_close(self):
        self.logger.debug('handle_close()')
        self.close()
        self.connection_handler.on_closed()

    def handle_write(self):
        try:
            msg = self.get_msg()
            data = msg.get_bytes()
            self.send(data)
            self.connection_handler.on_sent(msg)
            self.logger.debug('handle_write() -> data send')
        except Empty:
            self.logger.debug('handle_write() -> msg queue empty')

    def handle_read(self):
        data = self.recv(Message.MESSAGE_MAX_LENGTH)
        self.logger.debug('handle_read() -> (%d) "%s"', len(data), data)
        msg = Message.Message(byte_data=data)
        self.connection_handler.on_receive_msg(msg)
        
class SocketAsyncCoreConnectionManager(AbstractConnectionManager):
    def __init__(self):
        self.active_instance = None
        AbstractConnectionManager.__init__(self)
        
    def on_connected(self, args):
        addr, obj = args
        self.active_instance = obj
        super(SocketAsyncCoreConnectionManager, self).on_connected(addr)
        
    def send(self, msg):
        if self.active_instance:
            self.active_instance.push_msg(msg)
    
    def _connect(self, bind_adress, address):
        self.active_instance = SocketAsyncCoreClient(bind_adress, address, self)
        asyncore.loop()
        
    def _listen(self, bind_adress):
        self.active_instance = SocketAsyncCoreServer(bind_adress, self)
        asyncore.loop()
        
    def _close(self):
        if self.active_instance:
            self.active_instance.close()
        
    @abstractmethod
    def connect(self, bind_adress, address):
        threading.Thread(target=self._connect, args=[bind_adress, address]).start()
    
    @abstractmethod
    def listen(self, bind_adress):
        threading.Thread(target=self._listen, args=[bind_adress]).start()
    
    @abstractmethod
    def close(self):
        threading.Thread(target=self._close).start()
        
class GrpcServicer(grpc_serv_pb2.ChatServicer):
    def __init__(self, connection_manager):
        self.logger = logging.getLogger("grpc servicer")
        grpc_serv_pb2.ChatServicer.__init__(self)
        self.connection_manager = connection_manager
    def Send(self, request, context):
        msg = Message.Message(str_data=request.message)
        self.logger.debug("New msg incomes {0}".format(str(msg)))
        self.connection_manager.on_receive_msg(msg)
        return request
        
class GrpcConnectionManager(AbstractConnectionManager):
    MAX_WORKERS = 4
    def __init__(self):
        self.active_instance = None
        self.server = None
        self.channel = None
        self.stub = None
        AbstractConnectionManager.__init__(self)
        self.logger = logging.getLogger("grpc connection manager")

    def send(self, msg):
        if self.stub:
            self.stub.Send(grpc_serv_pb2.TransmitMessage(message=str(msg)))
            self.logger.debug("sent msg {0}".format(str(msg)))
            self.on_sent(msg)
            
    def connect(self, bind_adress, address):
        addr, port = address
        self.logger.debug("connecting to {0}:{1}".format(addr, port))
        self.channel = grpc.insecure_channel("{0}:{1}".format(addr, port))
        self.stub = grpc_serv_pb2.ChatStub(self.channel)
        self.on_connected(address)
        self.logger.debug("connected to {0}:{1}".format(addr, port))
    
    def listen(self, bind_adress):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=self.MAX_WORKERS))
        grpc_serv_pb2.add_ChatServicer_to_server(GrpcServicer(self), self.server)
        addr, port = bind_adress
        self.server.add_insecure_port("{0}:{1}".format(addr, port))
        self.server.start()
        self.logger.debug("listening {0}:{1}".format(addr, port))
    
    def close(self):
        if self.server:
            self.server.stop(0)   
        self.stub = None
        self.channel = None
        self.on_closed() 
        self.logger.debug("incoming channels, stubs went down; server went down")
        
