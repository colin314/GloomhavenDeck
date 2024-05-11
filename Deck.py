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

    def loadDeckModifications(self, modificationFile):
        f = open(modificationFile)
        lines = f.read().splitlines()

        for modStr in lines:
            mods = modStr.split(",", 3)
            if len(mods) != 4:
                raise Exception(
                    "Unexpected input in modification strings. Must have at least 4 elements"
                )
            removeCard = mods[0] == "0"
            modifier = int(mods[1])
            rolling = mods[2] == "1"
            effects = [Effect(int(x)) for x in mods[3].split(",")]
            if removeCard:
                for card in self.Cards:
                    if card.equals(modifier, rolling, effects):
                        self.Cards.remove(card)
                        break
            else:
                newCard = Card(modifier, rolling, *effects)
                self.Cards.append(newCard)

    def _addCard(self, cardStr):
        self.Cards.append(self._loadCard(cardStr))

    # Card string is modifier,rolling,Effect_list_(comma separated)
    def _loadCard(self, cardStr):
        x = cardStr.split(",", 2)
        modifier = int(x[0])
        rolling = x[1] == "1"
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

        effectList = []
        # Draw card
        while True:
            drawnCard = self.Cards.pop()
            attackValue = attackValue + drawnCard.modifier
            effectList.extend(drawnCard.Effects)
            # If the card shouldn't be removed, then add it to drawn pile
            if not Effect.REMOVE in drawnCard.Effects:
                self.Drawn.append(drawnCard)
            if not drawnCard.rolling:
                break

        attackValue = max(attackValue, 0)
        print(f"\t{attackValue}")

        # Print out effects
        for effect in effectList:
            print(f"\t{effect}")
            if effect == Effect.SHUFFLE:
                self.resetNeeded = True

        # Reset reminder
        if self.resetNeeded:
            print("\tDon't forget you need to reset your deck")

        return attackValue
