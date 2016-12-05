import unittest
from chat.ConnectionManagers import AbstractConnectionManager
from chat.Message import Message
from chat.Bus import StateBus


class Test(unittest.TestCase):
    TEST_ADDR = ('localhost', 10000)
    TEST_MSG = Message(str_data="message")
    class TestConectionManager(AbstractConnectionManager):
        def __init__(self):
            AbstractConnectionManager.__init__(self)

        def send(self, msg):
            self.on_sent(msg)
        
        def connect(self, bind_address, address):
            self.on_connected(address)
        
        def listen(self, bind_adress):
            self.on_connected(Test.TEST_ADDR)
        
        def close(self):
            self.on_closed()
            
        def receive_msg(self):
            self.on_receive_msg(Test.TEST_MSG)
            
    def test_StateBus_on_listen(self):
        manager = Test.TestConectionManager()
        bus = StateBus(manager)
        self.assertIsNone(bus.get_state("connected"))
        self.assertIsNone(bus.get_state("closed"))
        manager.listen(self.TEST_ADDR)
        self.assertEqual(bus.get_state("connected"), self.TEST_ADDR)
        manager.receive_msg()
        self.assertEqual(str(bus.get_msg()), str(self.TEST_MSG))
        manager.close()
        self.assertTrue(bus.get_state("closed"))
        
    def test_StateBus_on_connect(self):
        manager = Test.TestConectionManager()
        bus = StateBus(manager)
        self.assertIsNone(bus.get_state("connected"))
        self.assertIsNone(bus.get_state("closed"))
        manager.connect(self.TEST_ADDR, self.TEST_ADDR)
        self.assertEqual(bus.get_state("connected"), self.TEST_ADDR)
        manager.receive_msg()
        self.assertEqual(str(bus.get_msg()), str(self.TEST_MSG))
        manager.close()
        self.assertTrue(bus.get_state("closed"))
        


if __name__ == "__main__":
    unittest.main()