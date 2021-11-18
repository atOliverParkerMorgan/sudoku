class Node:
    def __init__(self, x, y, value, validValues, squareIndex):
        self.x = x
        self.y = y
        self.value = value
        self.validValues = validValues
        self.squareIndex = squareIndex

    def __str__(self):
        return f"|{self.value}|"
