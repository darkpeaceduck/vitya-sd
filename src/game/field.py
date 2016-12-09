class Field:
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._field = [[' '] * cols for i in range(rows)]
    def set_at(self, x, y, c):
        self._field[x][y] = c
    def get_at(self, x, y):
        return self._field[x][y]
    def get_demensions(self):
        return (self._rows, self._cols)