class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.userCannotChange = False

    def __str__(self):
        return f"|{self.value}|"
