class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value: int = value
        self.userCannotChange = False
        self.noteNums = []

    def __str__(self):
        return f"|{self.value}|"
