class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value: int = value
        self.user_cannot_change = False
        self.note_nums = []

    def __str__(self):
        return f"|{self.value}|"
