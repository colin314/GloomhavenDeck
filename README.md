For base deck, the template is modifier (int),rolling (bit),Effect (int from effect enum).

For deck modifications, the template is add_card (int),modifier (int),rolling (bit),Effect (int from effect enum).

So, to take a perk that replaces two -1 cards with two +1 cards, you'd put the following lines in a file called DeckModifications.csv

```
0,-1,0,0
0,-1,0,0
1,1,0,0
1,1,0,0
```