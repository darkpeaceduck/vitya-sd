import os

class Env:
    def __init__(self):
        self.dict = os.environ
    def add_vars(self, **kwargs):
        self.update(kwargs)
    def get_vars(self):
        return self.dict