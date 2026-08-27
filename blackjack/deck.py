from card import Card, card_suit_table
import random

suit_cards = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace" ]

class Deck:
    def __init__(self):
        self.create()
        self.shuffle()

    # Creates a new, unshuffled deck of 52 cards
    def create(self):
        cards = []

        for suit in card_suit_table:
            for value in suit_cards:
                cards.append(Card(value, suit))

        self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)

    def get_card_count(self):
        return len(self.cards)

    def draw_card(self):
        return self.cards.pop()
        