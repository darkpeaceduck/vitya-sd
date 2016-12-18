import os

#env implementation"
class Env:
    def __init__(self):
        self.dict = os.environ
    def __eq__(self, other):
        return self.dict == other.dict
    def add_vars(self, dct):
        self.dict.update(dct)
    def get_vars(self):
        return self.dict