import unittest
from cli.preprocessor import substitute
from cli.env import Env

class Test(unittest.TestCase):


    def test_subst_double_quote_and_outside(self):
        key = "myvar"
        value = "punch"
        env = Env()
        env.add_vars({key : value})
        s = 'lalal {0}{1} "dfdf {0}{1} dd"lala'
        self.assertEqual(substitute(s.format("$", key),  env), s.format("", value))
        
    def test_subst_single_quote_and_outside(self):
        key = "myvar"
        value = "punch"
        env = Env()
        env.add_vars({key : value})
        s = "lalal {0}{1} 'dfdf {2}{3} dd'lala"
        self.assertEqual(substitute(s.format("$", key, "$", key),  env), s.format("", value, "$", key))


if __name__ == "__main__":
    unittest.main()