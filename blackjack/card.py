card_back = [
    "╔═════╗",
   f"║?????║",
   f"║?????║",
   f"║?????║",
    "╚═════╝"
]

# Convert a card string suit to suit symbol
card_suit_table = {
    "hearts": "♥",
    "diamonds": "♦",
    "clubs": "♣",
    "spades": "♠"
}

# Convert a card string value to points
card_point_table = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 11 # remember to handle special case
}

# Create a visible card
def make_card(value, suit):
    value_length = len(value)

    # Convert whole string to fist letter instead
    if value_length > 2:
        value = value[0]

    return [
        "╔═════╗",
       f"║{value:<5}║",
       f"║  {card_suit_table[suit]}  ║",
       f"║   {value:>2}║",
        "╚═════╝"
    ]

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.drawing = make_card(value, suit)
        self.face_up = True
        self.points = self.get_points()

    def __str__(self):
        return f"{self.value} of {self.suit}"

    def get_points(self):
        if self.face_up:
            return card_point_table[self.value]
        else: return 0

    def flip(self):
        self.face_up = not self.face_up

        if self.face_up:
            self.drawing = make_card(self.value, self.suit)
        else:
            self.drawing = card_back
