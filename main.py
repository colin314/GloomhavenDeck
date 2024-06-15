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
        self.defaultAttack = 2

    def do_a(self, arg):
        "Make an attack for x n times: attack x n"
        if not arg:
            arg = str(self.defaultAttack) + " 1"
        self.deck.draw(*parse(arg))

    def do_aa(self, arg):
        "Make an attack x with advantage n times: aa x n"
        if not arg:
            arg = str(self.defaultAttack) + " 1"
        elif len(str.split(arg," ")) < 2:
            arg = arg + " 1"
        arg = parse(arg)
        self.deck.drawSpecial(arg[0], attackCount=arg[1], advantage=True)

    def do_da(self, arg):
        "Make an attack x with disadvantage n times: da x n"
        if not arg:
            arg = str(self.defaultAttack) + " 1"
        elif len(str.split(arg," ")) < 2:
            arg = arg + " 1"
        arg = parse(arg)
        self.deck.drawSpecial(arg[0], attackCount=arg[1], advantage=False)

    def do_reset(self, arg):
        "Shuffle the discard back into the attack deck. Only resets if one is needed. To override this (i.e., a hard reset), add a 1 as an option to the command: reset"
        if not arg:
            arg = False
        else:
            arg = True
        self.deck.reset(arg)

    def do_settimeout(self, arg):
        "Set the reset deck reminder timeout. Specify nothing to reset to default of 60 seconds: settimeout 60"
        if not arg:
            arg = 60
        else:
            arg = int(arg)
        self.deck.resetTimeout = arg

    def do_setdefatt(self,arg):
        "Set the default attack value. Specify nothing to reset to default of 2: setdefatt 2"
        if not arg:
            self.defaultAttack = 2
        else:
            self.defaultAttack = int(arg)

    def do_curse(self, arg):
        "Add n curses to your deck (default 1): curse n"
        if not arg:
            arg = 1
        self.deck.addCurse(int(arg))

    def do_bless(self, arg):
        "Add n blesses to your deck (default 1): bless n"
        if not arg:
            arg = 1
        self.deck.addBless(int(arg))

    def do_print(self, arg):
        "Print the contents of the deck"
        self.deck.printDeck()

    def do_undo(self, arg):
        "Undo the most recent command. Only works on commands that modify the deck."
        self.deck.undo()

    def do_q(self, arg):
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
