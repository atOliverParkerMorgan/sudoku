class Node:
    def __init__(self, x, y, value, board_size):
        self.x = x
        self.y = y
        self.value = int(value) if value and str(value).isdigit() else 0
        self.user_cannot_change = False
        self.note_nums = []
        self.valid_values = [i for i in range(1, board_size + 1) if i != self.value or self.value == 0]

    def __str__(self):
        return f"|{self.value}|"