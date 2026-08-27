from manger import Dealer
from players import HumanPlayer

def main():
    human = HumanPlayer("Gabriel")
    dealer = Dealer(human, 3)

    gaming = True
    while gaming:
        gaming = dealer.run_game()

    print("Thanks for playing!")

main()