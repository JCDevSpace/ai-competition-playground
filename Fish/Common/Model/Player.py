
# TODO: write purpose statement

class Player:

    def __init__(self, age, color):
        self.age = age
        self.color = color

    def get_color(self):
        return self.color

    def get_age(self):
        return self.age

    def get_data(self):
        return (self.age, self.color)

    def __eq__(self, other):
        if type(other) == type(self):
            return self.color == other.get_color()
        else:
            raise TypeError("other must be of type Player")
