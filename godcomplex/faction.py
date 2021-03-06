
import random
import string
from colors import color, COLORS

# hacky: directly represent ansi colors
colors = list(COLORS)
random.shuffle(colors)

class Faction:
    def __init__(self, people, name=None):
        self.people = people
        self.color = colors.pop(0)
        self.settlements = set()

        # TODO: better random name generation, obviously
        self.name = 'The First Tribe of {}'.format(string.capwords(people.name))

    def add_settlement(self, settlement):
        self.settlements.add(settlement)

    def __repr__(self):
        return '<Faction {} settlements={}>'.format(
            color(self.name, self.color),
            self.settlements)

    def __str__(self, use_color=False):
        if use_color:
            return color(self.name, self.color)
        return self.name
