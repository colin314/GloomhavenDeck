from MyEnums import Effect
import uuid
from Resources import bcolors

class Card:
    def __init__(self, modifier, rolling=False, *args):
        self.id = uuid.uuid4()
        self.modifier = modifier
        self.rolling = rolling
        self.Effects = []
        for x in args:
            self.Effects.append(x)

    def equals(self, modifier, rolling, effects):
        return (
            self.modifier == modifier
            and self.rolling == rolling
            and set(self.Effects) == set(effects)
        )

    def print(self):
        print(f"Modifier: {self.modifier}")
        print(f'Rolling? {"Yes" if self.rolling else "No"}')
        print(f'Effect: {str.join(",",[str(effect) for effect in self.Effects])}')

    def key(self):
        return str.join("^",[str(self.modifier),str(self.rolling),*sorted([x.name for x in self.Effects])])
    
    def modifierStr(self):
        if Effect.CRITICAL in self.Effects:
            color = bcolors.MAGENTA
        elif Effect.MISS in self.Effects:
            color = bcolors.YELLOW
        elif self.modifier > 0:
            color = bcolors.GREEN
        elif self.modifier < 0:
            color = bcolors.RED
        else:
            color = bcolors.WHITE
        return color + str(self.modifier) + bcolors.ENDC
