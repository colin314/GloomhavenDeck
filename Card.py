from MyEnums import Effect


class Card:
    def __init__(self, modifier, rolling=False, *args):
        self.modifier = modifier
        self.rolling = rolling
        self.Effects = []
        for x in args:
            self.Effects.append(Effect(x))
