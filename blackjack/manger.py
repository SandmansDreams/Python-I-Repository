""" NOTES
Game Loop:
    1. Create and shuffle a 52-card deck
    2. Deal each player 2 cards face up
    3. Deal the dealer:
        - 1 card face up
        - 1 card face down
    4. Starting with the players:
        - Check for Blackjack (has of exactly 21 including one ace and a value 10 card)
        - If they do not have Blackjack, they may:
            - Hit
            - Stand
    5. If a player busts (have over 21), their turn ends immediately
    6. Once player is done, dealer reveals hidden card
    7. Dealer must:
        - Hit while their hand totals less than 16.
        - Stand when their hand totals 16 or higher.
    8. Compare each remaining player's hand against the dealer:
        - Player busts -> Player loses.
        - Dealer busts -> Players win.
        - Player has higher total -> Player wins.
        - Dealer has higher total -> Player loses.
        - Equal totals -> Push (tie).
    9. Start the next round.
"""

import time
import os
from deck import Deck
from players import ComputerPlayer, HumanPlayer, Player, join_multiline_strings

GREEN = '\033[32m'
RESET = '\033[0m'

def print_style(string, styles):
    print(f"{"".join(styles)}{string}{RESET}")
    time.sleep(0.5)

# Manages the game
class Dealer(Player):
    def __init__(self, player: HumanPlayer, opponent_count):
        super().__init__("Dealer")

        players: list[Player] = [self]
        players.append(player)
        players.extend(self.create_opponents(opponent_count))
        self.players = players

        self.deck = Deck()

    # Creates a number of opponent players
    def create_opponents(self, count) -> list[ComputerPlayer]:
        if count > 4: count = 4
        opps = []

        for i in range(count):
            opps.append(ComputerPlayer(f"Comp{i + 1}"))

        return opps

    # Actually run the game
    def run_game(self) -> bool:
        print_style("Starting game...", GREEN)
        self.deck = Deck() # Create a fresh shuffled deck

        print_style("Deck shuffled, dealing...", GREEN)

        self.deal_initial_cards()

        print_style("Finished dealing, checking for blackjack...", GREEN)

        for player in self.players[1:]:
            has_blackjack = self.check_for_blackjack(player)
            if has_blackjack: return self.restart()

        print_style("No one has blackjack, taking turns...", GREEN)

        have_winner = self.do_turns()
        if have_winner: return self.restart()

        winners = self.get_winners_from_points()
        print_style(f"{" and ".join(winners)} have won through points! Congrats!", GREEN)

        # Prompt to start again
        return self.restart()

    def restart(self):
        query = input("Wanna go again? Y/N: ").upper()

        if query in ["Y"]:
            for player in self.players:
                player.hand = []

            return True

        else: return False


    def deal_initial_cards(self): # Deal each player 2 cards face up and the dealer one card face down and one face up
        cards_dealt = 0

        while cards_dealt < 2:
            # For each player, deal a face up card
            for player in reversed(self.players):
                if player.name == "Dealer": # If its the dealer
                    # If its the first time, deal a face down card to the dealer
                    if cards_dealt == 0:
                        self.deal_card(self, True)
                        print_style("Dealt face down card to dealer", GREEN)
                        time.sleep(.5)
                        continue

                self.deal_card(player)
                print_style(f"Dealt face up card to {player.name}", GREEN)
                time.sleep(.5)
            cards_dealt += 1

    def deal_card(self, target, flipped = False):
        card = self.deck.draw_card()
        if flipped: card.flip()
        target.give_card(card)
        self.render_board()

    def render_board(self):
        os.system("cls||clear")
        spacer = "     "
        second_row_players = self.players[1:]

        second_row = join_multiline_strings(
            *(player.get_player_render() for player in second_row_players),
            spacer = spacer
        )

        # Print the dealer centered
        first_row = self.players[0].get_player_render()

        board_width = max(
            len(line)
            for line in second_row
        )

        for line in first_row:
            print(line.center(board_width))

        print()

        for line in second_row:
            print(line)

    def check_for_blackjack(self, player: Player) -> bool:
        if len(player.hand) > 2: return False

        if player.get_score() == 21:
            if any(card.value == "Ace" for card in player.hand):
                print_style(f"{player.name} has blackjack! We have a winner!", GREEN)
                return True

        return False

    def do_turns(self) -> bool:
        # Let each player in order (clockwise) play based on their hand, if a player busts, they are out so remove them from the play order
        for player in reversed(self.players):
            if player.busted: continue # Skip busted players

            print_style(f"{player.name}'s Turn", GREEN)
            time.sleep(0.5)

            if player.name == "Dealer":
                # If all players busted, dealer wins
                if all(player.busted for player in self.players[1:]):
                    print_style(f"Everyone busted, the dealer wins!", GREEN)
                    return True
                
                self.hand[0].flip()
                self.render_board()
                print_style("Dealer flipped card", GREEN)

            # Players make decisions and then consequences happen
            hit = player.take_turn()
            time.sleep(0.5)

            if hit:
                print_style(f"{player.name} chose hit, dealing card...", GREEN)
                self.deal_card(player)
                new_score = player.get_score()

                if new_score > 21:
                    player.busted = True
                    if player.name == "Dealer":
                        print_style(f"{player.name} busted, everyone else wins!", GREEN)
                        return True

                    print_style(f"{player.name} busted, they are out of the game", GREEN)

                continue

            print_style(f"{player.name} chose to stand", GREEN)
            time.sleep(0.5)

        return False

    def take_turn(self):
        if self.get_score() < 16:
            return True
        else: 
            return False

    def get_winners_from_points(self):
        winners = []
        max_score = max(player.get_score() for player in self.players)

        for player in self.players:
            if player.get_score() == max_score:
                winners.append(player.__str__())

        return winners
