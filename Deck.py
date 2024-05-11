from Card import Card
from MyEnums import Effect
import random as rand


class Deck:
    def __init__(self, deckFile):
        self.Cards = []
        self.Drawn = []
        self.loadDeck(deckFile)
        self._shuffle()
        self.resetNeeded = False

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
        effects = [Effect(int(i)) for i in x[2].split(",")]
        return Card(modifier, rolling, *effects)

    def _shuffle(self):
        rand.shuffle(self.Cards)

    def reset(self):
        self.Cards.extend(self.Drawn)
        self.Drawn = []
        self._shuffle()
        self.resetNeeded = False

    def addCurse(self, n=1):
        for i in range(n):
            curseCard = Card(0, False, Effect.MISS, Effect.REMOVE)
            self.Cards.append(curseCard)
            self._shuffle()

    def addBless(self, n=1):
        for i in range(n):
            curseCard = Card(0, False, Effect.CRITICAL, Effect.REMOVE)
            self.Cards.append(curseCard)
            self._shuffle()

    def draw(self, attackValue):
        if len(self.Cards) == 0:
            self.reset()

        # Draw card
        drawnCard = self.Cards.pop()

        # If the card shouldn't be removed, then add it to drawn pile
        if not Effect.REMOVE in drawnCard.Effects:
            self.Drawn.append(drawnCard)

        attackValue = max(attackValue + drawnCard.modifier, 0)
        print(f"\t{attackValue}")

        # Print out effects
        for effect in drawnCard.Effects:
            print(f"\t{effect}")
            if effect == Effect.SHUFFLE:
                self.resetNeeded = True

        # Reset reminder
        if self.resetNeeded:
            print("\tDon't forget you need to reset your deck")

        return attackValue
