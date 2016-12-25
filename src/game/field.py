class Field:
    def __init__(self, rows=0, cols=0):
        self._rows = rows
        self._cols = cols
        self._field = [[' '] * cols for i in range(rows)]
        
    def load_file(self, filename):
        with open(filename, 'r') as f:
            self._rows, self._cols = [int(x) for x in next(f).split()]
            self._field = []
            for line in f:
                chars = list(str.rstrip(line))
                self._field.append(chars)
                print(chars)
                
    def set_at(self, x, y, c):
        self._field[x][y] = c
    def get_at(self, x, y):
        return self._field[x][y]
    def get_demensions(self):
        return (self._rows, self._cols)