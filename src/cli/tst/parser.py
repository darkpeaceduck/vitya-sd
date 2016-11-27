import unittest
from cli.lang import *
from cli.parser import *

class Test(unittest.TestCase):
    def make_envset(self, list):
        req_envet = EnvSet()
        for key, value in list:
            req_envet.add_assign(EnvAssigment(key, value))
        return req_envet
    
    def test_cmd(self):
        s = "a=b b='c d' c=\"d e\" cmd arg1 \"arg2\" 'arg3'"
        req_envet = self.make_envset([("a", "b"), ("b","c d"), ("c" ,"d e")])
        args = ["arg1", "arg2", "arg3"]
        req = Cmd("cmd", req_envet, args)
        self.assertEqual(parse(s), req)
        
    def test_simple_pipe(self):
        s = "  cmd1   |  cmd2  | cmd3 "
        req = Pipe(Pipe(Cmd("cmd1", EnvSet(), []), 
                   Cmd("cmd2", EnvSet(), [])),
                   Cmd("cmd3", EnvSet(), []))
        self.assertEqual(parse(s), req)
        
    def test_global_envset(self):
        arg = "aa"
        value = 'bbb  ccc  ddd'
        s = ["    {0}='{1}'",
             "   {0}=\"{1}\""]
        req = EnvSet()
        req.add_assign(EnvAssigment(arg, value))
        for line in s : 
            self.assertEqual(parse(line.format(arg, value)), req)      
        
    def test_full_functional(self):
        pass
        s = "aa=bb  b='123 45' c=\"  aaa  bbb  cc\" comm1 arg1 'arg2 carg2' \"arg3 carg3\" | e=c comm2 arg4 arg5 | comm3"
        env_cmd1  = self.make_envset([("aa", "bb"), ("b","123 45"), ("c" ,"  aaa  bbb  cc")])
        env_cmd2 = self.make_envset([("e", "c")])
        args_cmd1 = ["arg1", "arg2 carg2", "arg3 carg3"]
        args_cmd2 = ["arg4", "arg5"]
        cmd1 = Cmd("comm1", env_cmd1, args_cmd1)
        cmd2 = Cmd("comm2", env_cmd2, args_cmd2)
        cmd3 = Cmd("comm3", EnvSet(), [])
        req = Pipe(Pipe(cmd1, cmd2), cmd3)
        self.assertEqual(parse(s), req)


if __name__ == "__main__":
    unittest.main()