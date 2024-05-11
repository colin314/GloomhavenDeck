from MyEnums import Effect
import uuid


class Card:
    def __init__(self, modifier, rolling=False, *args):
        self.id = uuid.uuid4()
        self.modifier = modifier
        self.rolling = rolling
        self.Effects = []
        for x in args:
            self.Effects.append(x)
