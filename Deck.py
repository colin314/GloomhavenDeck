from Card import Card
from MyEnums import Effect


class Deck:
    def __init__(self, deckFile):
        self.Cards = []
        self.loadDeck(deckFile)

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