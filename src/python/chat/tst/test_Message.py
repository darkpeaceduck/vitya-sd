import unittest
import chat.Message as Message
from chat.Message import MessageQueueProcessor
from queue import Empty

class Test(unittest.TestCase):


    def test_Message_decode(self):
        inp = b'vasyly'
        outp = 'vasyly'
        self.assertEqual(str(Message.Message(byte_data=inp)), outp)

    def test_Message_encode(self):
        inp = 'vasyly'
        outp = b'vasyly'
        self.assertEqual(Message.Message(str_data=inp).get_bytes(), outp)
        
    def test_MessageQueueProcessor(self):
        str_items = ["one", "two", "three"]
        msg_items = list(map(lambda x: Message.Message(x), str_items))
        proc = MessageQueueProcessor()
        
        for item in msg_items:
            proc.push_msg(item)
        
        for item in msg_items:
            self.assertEqual(str(item), str(proc.get_msg()))
            
        self.assertRaises(Empty, proc.get_msg)
                
        
if __name__ == "__main__":
    unittest.main()