
# This class represents a player and keeps their color and age

# Color is  one of "red", "white", "brown", "black"

class Player:

    # Returns a Player object given their age and color
    # PosInt, Color -> Player
    # Raises ValueError if age is less than 0
    def __init__(self, age, color):
        if age > 0:
            self.age = age
        else:
            raise ValueError("Age must be a positive int")
        self.color = color

    # Returns the Color of this Player
    # Void -> Color
    def get_color(self):
        return self.color

    # Returns the age of this Player
    # Void -> Int
    def get_age(self):
        return self.age

    # Returns the age and color of this player as a tuple
    # Void -> (PosInt, Color)
    def get_data(self):
        return (self.age, self.color)

    # Here we overwrite == so that it compares the colors only of the Players
    # Object -> Boolean
    # Raises TypeError if other is not a Player
    def __eq__(self, other):
        if type(other) == type(self).__name__:
            return self.color == other.get_color()
        elif other == self.color:
            return True
        else:
            raise TypeError("other must be of type Player")

    def __hash__(self):
        return hash(self.color)
