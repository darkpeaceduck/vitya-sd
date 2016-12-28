from abc import abstractmethod
from chat.Message import MessageQueueProcessor, Message
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from queue import Empty

'''
If you want to split interracting functional with connection managers into
bus, just override render_loop method and use composition.
Otherwise, inhirite AbstractBus  too.
'''
class AbstractView:
    @abstractmethod
    def render_loop(self):
        pass
    
class TkinterUIView(AbstractView):
    UPDATE_UI_TIMEOUT = 1000
    DEFAULT_BIND_ADDR = "localhost"
    DEFAULT_BIND_PORT = "9082"
    DEFAULT_USERNAME = "USER"
    def __init__(self, bus):
        AbstractView.__init__(self)
        self.bus = bus
        self.state = {
            "connected" : None,
            "closed" : None,
        }
    
    def get_user_invite(self, user):
        return "<" + user + ">"
        
    def on_name_entry_button(self):
        self.msg_entry.delete(0, tk.END)
        self.msg_entry.insert(0, self.get_user_invite(self.name_entry.get()))
        
    def on_msg_entry_button(self):
        msg_str = self.msg_entry.get()
        self.bus.send(Message(str_data=msg_str))
        self.msg_entry.delete(0, tk.END)
        self.msg_entry.insert(0, self.get_user_invite(self.name_entry.get()))
        
    def on_listen_button(self):
        self.bus.listen(self.get_bind_addr())
        self.connection_info_hide()
        self.close_button.pack()
        
    def on_connect_button(self):
        bind_addr = self.get_bind_addr()
        connect_addr = self.get_connect_addr()
        self.bus.connect(bind_addr, connect_addr)
        self.connection_info_hide()
        self.close_button.pack()
        
    def on_close_button(self):
        self.bus.close()
        
    def on_exit(self):
        self.bus.close()
        self.root.destroy()
        
    def shedule_update_ui(self):
        self.root.after(self.UPDATE_UI_TIMEOUT, self.update_ui)
        
    def update_ui(self):
        self.chat_entry.config(state=tk.NORMAL)
        if self.bus.get_state("connected"):
            self.chat_entry.insert(tk.INSERT, "connected {0}\n".format(self.bus.get_state("connected")))
            self.bus.clear_state("connected")
        if self.bus.get_state("closed"):
            self.chat_entry.insert(tk.INSERT, "closed\n")
            self.bus.clear_state("closed")
        try:
            while True:
                msg = self.bus.get_msg()
                self.chat_entry.insert(tk.INSERT, str(msg) + "\n")
        except Empty:
            pass
        finally:
            self.chat_entry.config(state=tk.DISABLED)
            self.shedule_update_ui()
    
    def get_bind_addr(self):
        addr = self.bind_addr_entry.get()
        port = int(self.bind_port_entry.get())
        return (addr, port)
    
    def get_connect_addr(self):
        addr = self.connect_addr_entry.get()
        port = int(self.connect_port_entry.get())
        return (addr, port)
    
    def create_bind_entry(self):
        self.bind_addr_entry = tk.Entry()
        self.bind_addr_entry.insert(0, self.DEFAULT_BIND_ADDR)
        self.bind_addr_entry.pack()
        self.bind_port_entry = tk.Entry()
        self.bind_port_entry.insert(0, self.DEFAULT_BIND_PORT)
        self.bind_port_entry.pack()
        
    def create_connect_entry(self):
        self.connect_addr_entry = tk.Entry()
        self.connect_addr_entry.insert(0, self.DEFAULT_BIND_ADDR)
        self.connect_addr_entry.pack()
        self.connect_port_entry = tk.Entry()
        self.connect_port_entry.insert(0, self.DEFAULT_BIND_PORT)
        self.connect_port_entry.pack()
        
    def create_control_buttons(self):
        
        self.listen_button = tk.Button(master = self.root, text = "listen", \
                                    command = self.on_listen_button)
        self.listen_button.pack()
        self.connect_button = tk.Button(master = self.root, text = "connect", \
                                    command = self.on_connect_button)
        self.connect_button.pack()
        self.close_button = tk.Button(master = self.root, text = "close", \
                                    command = self.on_close_button)
        
    def connection_info_hide(self):
        self.listen_button.pack_forget()
        self.connect_button.pack_forget()
        self.bind_addr_entry.pack_forget()
        self.bind_port_entry.pack_forget()
        self.connect_addr_entry.pack_forget()
        self.connect_port_entry.pack_forget()
        
    def create_name_entry(self):
        self.name_entry = tk.Entry()
        self.name_entry.insert(tk.END, self.DEFAULT_USERNAME)
        self.name_entry.pack()
        self.name_entry_button = tk.Button(master = self.root, text = "change name", \
                                    command = self.on_name_entry_button)
        self.name_entry_button.pack()
        
    def create_msg_entry(self):
        self.msg_entry = tk.Entry()
        self.msg_entry.insert(tk.END, self.get_user_invite(self.DEFAULT_USERNAME))
        self.msg_entry.pack()
        self.msg_entry_button = tk.Button(master = self.root, text = "send msg", \
                                    command = self.on_msg_entry_button)
        self.msg_entry_button.pack()
        
    def create_chat_entry(self):
        self.chat_entry = ScrolledText(self.root)
        self.chat_entry.config(state=tk.DISABLED)
        self.chat_entry.pack()
        
    def render_loop(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.create_bind_entry()
        self.create_connect_entry()
        self.create_control_buttons()
        self.create_name_entry()
        self.create_msg_entry()
        self.create_chat_entry()
        self.shedule_update_ui()
        tk.mainloop()