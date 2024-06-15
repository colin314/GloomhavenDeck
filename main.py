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

    def do_a(self, arg):
        "Make an attack for x n times: attack x n"
        if not arg:
            arg = "2 1"
        self.deck.draw(*parse(arg))

    def do_aa(self, arg):
        "Make an attack with advantage: aa 2"
        if not arg:
            arg = 2
        self.deck.drawSpecial(int(arg), True)

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
