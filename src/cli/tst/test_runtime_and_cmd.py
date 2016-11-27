
import unittest
from cli.runtime import *
from io import StringIO
import tempfile
import os
from cli.env import Env
import copy


#TODO : написать текст, почему два модуля вместе (по идее runtime должен дергать абкстракцию и мы её затем в тесте
#подменяем, но мне впадлу такое
class Test(unittest.TestCase):
    def make_output_str(self, env, input_obj):
        output = StringIO()
        input_obj.exec(env, None, output)
        output.seek(0)
        return output.read()
        
    def test_cmd_echo(self):
        req_output = "it string"
        cmd = Cmd("echo", EnvSet(), [req_output])
        self.assertEqual(self.make_output_str(None, cmd), req_output + "\n")
        
    def test_cmd_echo_and_wc(self):
        req_s = "it string"
        req_output = "1 2 {0}".format(len(req_s) + 1)
        cmd = Pipe(Cmd("echo", EnvSet(), [req_s]), Cmd("wc", EnvSet(), []))
        self.assertEqual(self.make_output_str(None, cmd), req_output + "\n")

    def test_cmd_cat(self):
        with tempfile.NamedTemporaryFile() as file:
            contents = "AAAAA BBBBBB \n CCC dDDD \n"
            file.write(str.encode(contents))
            file.flush()
            cmd = Cmd("cat", EnvSet(), [file.name])
            self.assertEqual(self.make_output_str(None, cmd), contents)
            
    def test_cmd_pwd(self):
        path = os.getcwd()
        cmd = Cmd("pwd", EnvSet(), [])
        self.assertEqual(self.make_output_str(None, cmd), path + "\n")
        
    def test_envset(self):
        key = "a"
        value = "b"
        env = Env()
        env_req = copy.copy(env)
        env_req.add_vars({key:value})
        envset = EnvSet()
        envset.add_assign(EnvAssigment(key, value))
        
        self.make_output_str(env, envset)
        self.assertEqual(env, env_req)
        
    def test_grep(self):
        with tempfile.NamedTemporaryFile() as file:
            contents = "AAAAA BBBBBB \n CCC dDDD \n"
            req = "AAAAA BBBBBB "
            pattern = "BB"
            file.write(str.encode(contents))
            file.flush()
            cmd = Cmd("grep", EnvSet(), [pattern, file.name])
            self.assertEqual(self.make_output_str(None, cmd), req + "\n")
        
if __name__ == "__main__":
    unittest.main()