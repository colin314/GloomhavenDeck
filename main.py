from Deck import Deck
import cmd, sys

deck = Deck("BaseDeck.csv", "DeckModifications.csv")


class DeckProgram(cmd.Cmd):
    intro = "Welcome to the automated Gloomhaven attack deck program."
    prompt = "Input: "
    file = None

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.deck = Deck("BaseDeck.csv", "DeckModifications.csv")

    def do_attack(self, arg):
        "Draw a card from the deck: attack 5"
        self.deck.draw(*parse(arg))

    def do_reset(self, arg):
        "Shuffle the discard back into the attack deck: reset"
        self.deck.reset()

    def do_curse(self, arg):
        "Add a n curses to your deck: curse"
        if not arg:
            arg = 1
        self.deck.addCurse(int(arg))

    def do_bye(self, arg):
        "Stop recording, close the turtle window, and exit:  BYE"
        print("Thank you for using the virtual attack deck")
        self.close()
        return True

    # ----- record and playback -----
    def do_record(self, arg):
        "Save future commands to filename:  RECORD rose.cmd"
        self.file = open(arg, "w")

    def do_playback(self, arg):
        "Playback commands from a file:  PLAYBACK rose.cmd"
        self.close()
        with open(arg) as f:
            self.cmdqueue.extend(f.read().splitlines())

    def precmd(self, line):
        line = line.lower()
        if self.file and "playback" not in line:
            print(line, file=self.file)
        return line

    def close(self):
        if self.file:
            self.file.close()
            self.file = None


def parse(arg):
    "Convert a series of zero or more numbers to an argument tuple"
    return tuple(map(int, arg.split()))


if __name__ == "__main__":
    DeckProgram().cmdloop()
