


class Player:

    def __init__(self, age, color):
        self.age = age
        self.color = color

    def get_color(self):
        return self.color

    def get_age(self):
        return self.age

    def __eq__(self, other):
        if type(other) == type(self):
            return self.age == other.get_age()
        else:
            raise TypeError("other must be of type Player")

    def __lt__(self, other):
        if type(other) == type(self):
            return self.age < other.get_age()
        else:
            raise TypeError("other must be of type Player")

    def __gt__(self, other):
        if type(other) == type(self):
            return self.age > other.get_age()
        else:
            raise TypeError("other must be of type Player")
