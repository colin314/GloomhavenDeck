from Deck import Deck

f = open("BaseDeck.csv")
lines = f.read().splitlines()

for line in lines:
    x = line.split(",", 2)


deck = Deck("BaseDeck.csv")
print([x.id for x in deck.Cards])
