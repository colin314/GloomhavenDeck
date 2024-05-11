from Card import Card
from MyEnums import Effect
import random as rand


class Deck:
    def __init__(self, deckFile):
        self.Cards = []
        self.Drawn = []
        self.loadDeck(deckFile)
        self.shuffle()

    def loadDeck(self, deckFile):
        f = open(deckFile)
        lines = f.read().splitlines()

        for cardStr in lines:
            self._addCard(cardStr)

    def _addCard(self, cardStr):
        self.Cards.append(self._loadCard(cardStr))

    # Card string is modifier,rolling,Effect_list_(comma separated)
    def _loadCard(self, cardStr):
        x = cardStr.split(",", 2)
        modifier = int(x[0])
        rolling = bool(x[1])
        effects = [int(i) for i in x[2].split(",")]
        return Card(modifier, rolling, *effects)

    def _shuffle(self):
        rand.shuffle(self.Cards)

    def reset(self):
        self.Cards.extend(self.Drawn)
        self.Drawn = []
        self._shuffle()

    def draw(self, attackValue):
        # Add handling for empty deck
        drawnCard = self.Cards.pop()
        self.Drawn.append(drawnCard)
        attackValue = max(attackValue + drawnCard.modifier, 0)
        print(f"\t{attackValue}")
        for effect in drawnCard.Effects:
            print(f"\t{effect}")
        return attackValue
