from card import Card, card_back
from abc import ABC, abstractmethod
from itertools import zip_longest

DARK_GREY = "\033[90m"
RED = "\033[31m"
BOLD = '\033[1m'
STRIKETHROUGH = '\033[9m'
RESET = '\033[0m'

def join_multiline_strings(*strings, spacer): # Takes a set of multiline strings and combines them into one set of rows for printing
    if not strings:
        return ["", "", "", "", ""]

    rows = []

    for row in zip_longest(*strings, fillvalue=""):
        rows.append(spacer.join(row))

    return rows

class Player(ABC): 
    def __init__(self, name):
        self.name = name
        self.hand: list[Card] = []
        self.busted = False

    def __str__(self) -> str:
        return self.name

    def give_card(self, card: Card):
        self.hand.append(card)

    def get_score(self): # Get total score by summing the point value of all cards in hand
        if self.busted: return 0 # Win protection

        points = sum(card.points for card in self.hand)

        # Handle aces
        if points > 21:
            for card in self.hand:
                if card.value == "Ace":
                    card.points = 1
                    points = sum(card.points for card in self.hand)

        return points

    def get_player_render(self, busted=False):
        title = f"{self.name.upper()}: {self.get_score()}"

        card_strings = join_multiline_strings(
            *(card.drawing for card in self.hand),
            spacer=" "
        )

        cards_width = 0
        hand_length = len(self.hand)
        if hand_length > 0:
            cards_width = (len(card_back[0]) * hand_length) + (hand_length - 1)

        longest_width = max(cards_width, len(title))

        title += " " * (longest_width - (len(title)))

        if cards_width < longest_width:
            card_strings = [
                line + " " * (longest_width - len(line))
                for line in card_strings
            ]

        render = [title]
        render.extend(card_strings)

        return render
        
    @abstractmethod
    def take_turn(self) -> bool:
        pass


class ComputerPlayer(Player):
    def __init__(self, name):
            super().__init__(name)

    def take_turn(self):
        if self.get_score() < 18:
            return True
        else: 
            return False
        

class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def take_turn(self):
        while True:
            decision = input("What would you like to do? HIT or STAND: ").upper()

            if "H" in decision:
                return True
            elif "S" in decision:
                return False
            else: 
                print("Sorry, try again")
        