from Card import Card
from MyEnums import Effect
import random as rand
from tabulate import tabulate
from datetime import datetime


class Deck:
    def __init__(self, deckFile, modificationFile, resetTimeout = 60):
        self._Cards = []
        self._Drawn = []
        self._loadDeck(deckFile)
        self._loadDeckModifications(modificationFile)
        self._shuffle()
        self._resetNeeded = False
        self._resetTime = datetime.now()
        self._resetTimeout = resetTimeout

#region Private functions
    def _loadDeck(self, deckFile):
        f = open(deckFile)
        lines = f.read().splitlines()

        for cardStr in lines:
            self._addCard(cardStr)

    def _loadDeckModifications(self, modificationFile):
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
                for card in self._Cards:
                    if card.equals(modifier, rolling, effects):
                        self._Cards.remove(card)
                        break
            else:
                newCard = Card(modifier, rolling, *effects)
                self._Cards.append(newCard)

    def _addCard(self, cardStr):
        self._Cards.append(self._loadCard(cardStr))

    # Card string is modifier,rolling,Effect_list_(comma separated)
    def _loadCard(self, cardStr):
        x = cardStr.split(",", 2)
        modifier = int(x[0])
        rolling = x[1] == "1"
        effects = [Effect(int(i)) for i in x[2].split(",")]
        return Card(modifier, rolling, *effects)

    def _shuffle(self):
        rand.shuffle(self._Cards)

    def _getEffectString(self, effectList):
        if any(x == Effect.SHUFFLE for x in effectList):
            self._setResetFlag()
        return str.join(", ", [x.name for x in effectList if not x == Effect.NONE])

    def _drawCard(self, drawnCards):
        if len(self._Cards) == 0:
            self.reset()
        # Check for the condition where all cards are in the draw pile
        if len(self._Cards) == 0:
            print(
                "You're completely out of cards to draw (everything has already been drawn). This shouldn't happen, but I'm going to just shuffle all drawn cards back in. You might lose some attack effects. Just saying."
            )
            self._Drawn.extend(drawnCards)
            self.reset()
        # Draw the card
        drawnCard = self._Cards.pop()
        # Add non-remove cards (i.e., non Curse/Bless) to the drawn pile
        if not Effect.REMOVE in drawnCard.Effects:
            drawnCards.append(drawnCard)
        return drawnCard

    def _checkForReset(self):
        if self._resetNeeded and (datetime.now() - self._resetTime).total_seconds() > self._resetTimeout:
            cont = input("Your deck needs a reset. Enter 0 to ignore and continue, 1 to reset and continue: ")
            cont = int(cont)
            if cont == 1:
                self.reset()
            else:
                self._resetTime = datetime.now()

    def _setResetFlag(self):
        self._resetNeeded = True
        self._resetTime = datetime.now()
#endregion

#region Public functions
    def reset(self, hard=False):
        if not hard and not self._resetNeeded:
            print("No reset is needed. If you would like to reset anyways, do a hard reset.")
            return
        self._Cards.extend(self._Drawn)
        self._Drawn = []
        self._shuffle()
        self._resetNeeded = False

    def addCurse(self, n=1):
        for i in range(n):
            curseCard = Card(0, False, Effect.MISS, Effect.REMOVE)
            self._Cards.append(curseCard)
            self._shuffle()

    def addBless(self, n=1):
        for i in range(n):
            curseCard = Card(0, False, Effect.CRITICAL, Effect.REMOVE)
            self._Cards.append(curseCard)
            self._shuffle()

    def draw(self, attackValue, attackCount=1):
        self._checkForReset()
        if len(self._Cards) == 0:
            self.reset()
        drawnCards = []

        origAttack = attackValue
        attacks = [["Attack Value", "Effect List"]]
        for i in range(attackCount):
            effectList = []
            attackValue = origAttack
            # Draw card
            while True:
                drawnCard = self._drawCard(drawnCards)
                attackValue = attackValue + drawnCard.modifier
                effectList.extend(drawnCard.Effects)

                if not drawnCard.rolling:
                    break

            attackValue = max(attackValue, 0)
            effectStr = self._getEffectString(effectList)
            attacks.append([attackValue, effectStr])
        print(
            tabulate(
                attacks,
                headers="firstrow",
                tablefmt="fancy_grid",
                showindex="always",
            )
        )

        # Place all drawn cards into the discard
        self._Drawn.extend(drawnCards)

        # Reset reminder
        if self._resetNeeded:
            print("\tDon't forget you need to reset your deck")

        return attackValue

    def drawSpecial(self, attackValue, attackCount=1, advantage=False):
        self._checkForReset()
        for i in range(attackCount):
            drawnCards = []
            currCard = self._drawCard(drawnCards)
            rollingCards = []
            while currCard.rolling:
                rollingCards.append(currCard)
                currCard = self._drawCard(drawnCards)
            firstCard = currCard
            secondCard = self._drawCard(drawnCards)

            self._Drawn.extend(drawnCards)

            # Check for shuffle cards
            if any(any(x == Effect.SHUFFLE for x in card.Effects) for card in drawnCards):
                self._setResetFlag()

            # If disadvantage, discard all rolling modifiers
            if not advantage:
                rollingCards = []

            rollingModifier = sum([x.modifier for x in rollingCards])
            rollingEffects = set(
                [
                    effect
                    for card in rollingCards
                    for effect in card.Effects
                    if effect != Effect.NONE
                ]
            )

            # First Card
            rollingModifierStr = self._getEffectString(rollingEffects)
            firstRow = [
                attackValue + rollingModifier + firstCard.modifier,
                self._getEffectString(firstCard.Effects),
                rollingModifierStr,
            ]
            secondRow = [
                attackValue + rollingModifier + secondCard.modifier,
                self._getEffectString(secondCard.Effects),
                rollingModifierStr,
            ]

            print(
                tabulate(
                    [
                        ["Attack value", "Modifiers", "Rolling Modifiers"],
                        firstRow,
                        secondRow,
                    ],
                    headers="firstrow",
                    tablefmt="fancy_grid",
                    showindex="always",
                )
            )

        if self._resetNeeded:
            print("\tDon't forget you need to reset your deck")

        print("")
#endregion