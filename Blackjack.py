# Blackjack.py
# A command line blackjack game

import random
import time


class Deck:
    suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self):
        self.deck = []

    def fill_deck(self):
        """Load deck with 6 decks of cards"""
        for i in range(0, 6):
            for suit in Deck.suits:
                for value in Deck.values:
                    self.deck.append(Card(suit, value))

    def clear_deck(self):
        self.deck = []

    def shuffle(self):
        return random.shuffle(self.deck)


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"


class Player:
    def __init__(self, chips):
        self.hand = []
        self.chips = chips
        self.handscore = 0
        self.isbusted = False
        self.ace_count = 0

    def place_bet(self):
        bet = input(f"\nYou have {self.chips} chips. \nHow much would you like to bet?: ")
        try:
            if int(bet) > self.chips:
                print("You don't have enough to bet that much!")
                self.place_bet()
            else:
                self.chips -= int(bet)
                return int(bet)
        except ValueError:
            print("That is not a valid bet entry.")
            self.place_bet()

    def show_hand(self):
        print("\nPlayers Hand:")
        for n, card in enumerate(self.hand):
            print(str(self.hand[n]))
        print()


class Dealer:
    def __init__(self):
        self.hand = []
        self.handscore = 0
        self.isbusted = False
        self.ace_count = 0

    def show_hand(self, showall=False):
        """Prints out the dealers hand, pass showall=True to show all cards else only shows 1st card"""
        print("\nDealer's Hand:")
        if showall:
            for n, card in enumerate(self.hand):
                print(str(self.hand[n]))
        else:
            print(str(self.hand[0]))
            print("???")


class Game:
    def __init__(self, players, deck):
        self.players = players
        self.deck = deck
        self.playerbet = 0
        self.players_turn = True

    def deal(self):
        print(f"{len(self.deck.deck)} cards in Deck")
        if len(self.deck.deck) < 104:  # When stack gets to total of 2 card decks remaining, reshuffle 6 decks
            print("Reshuffling decks...")
            self.deck.clear_deck()
            self.deck.fill_deck()
            self.deck.shuffle()
            time.sleep(4)
        for i in range(2):
            for player in self.players:
                card = self.deck.deck.pop()
                if "Ace" in card.value:  # Ace counter used for calculating value of Ace as 1 or 11
                    player.ace_count += 1
                player.hand.append(card)
                self.add_points(player, card)

    def add_points(self, player, card):
        if card.value in ["Jack", "Queen", "King"]:
            player.handscore += 10
        if card.value in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            player.handscore += int(card.value)
        if card.value == "Ace":
            player.handscore += 11

    def hit(self, player):
        card = self.deck.deck.pop()
        player.hand.append(card)
        if "Ace" in card.value:
            player.ace_count += 1
        if isinstance(player, Dealer):
            player.show_hand(True)
        else:
            player.show_hand()
        self.add_points(player, card)
        self.checkbust(player)

    def playerchoice(self, player):
        answer = input("Hit or Stick? H/S: ")
        if answer.lower() == "h":
            self.hit(player)
        if answer.lower() == "s":
            print(f"Player Sticks with hand of {str(player.handscore)}\n")
            self.players_turn = False

    def checkbust(self, player):
        """Checks for bust if handscore over 21, presence of ace reduces by 10, ace count allows for multiple aces"""
        if player.ace_count > 0 and player.handscore > 21:
            player.handscore -= 10
            player.ace_count -= 1
        if player.handscore > 21:
            if isinstance(player, Player):
                print("Player Busts!")
                self.players_turn = False
                player.isbusted = True
                self.playerlose()
            if isinstance(player, Dealer):
                print("\nDealer Busts!")
                player.isbusted = True

    def playerwin(self, player):
        print(f"You win! \n{str(2 * self.playerbet)} chips added to your total.")
        player.chips += 2 * self.playerbet
        self.playerbet = 0

    def playerlose(self):
        print(f"You lose!")

    def draw(self, player):
        print(f"Its a draw, you get your bet of {self.playerbet} back.")
        player.chips += self.playerbet

    def comparescores(self, player, dealer):
        if player.handscore > dealer.handscore:
            self.playerwin(player)
        if player.handscore == dealer.handscore:
            self.draw(player)
        if player.handscore < dealer.handscore:
            self.playerlose()

    def resetplayers(self):
        for player in self.players:
            player.hand = []
            player.handscore = 0
            player.isbusted = False
            player.ace_count = 0
        self.playerbet = 0

    def playagain(self, player):
        again = None
        while again != "y" or again != "n":
            again = input("\nWould you like to play again? Y/N: ")
            if again.lower() == "y":
                return True
            if again.lower() == "n":
                print(f"\nOk, thanks for playing. You walk away with {player.chips} chips.")
                input("Press any key to exit: ")
                return False
            else:
                print("That was not a valid input")


def main():
    print("\n---------- Welcome to Blackjack ----------\n")
    newdeck = Deck()
    newdeck.fill_deck()
    newdeck.shuffle()
    player = Player(100)
    dealer = Dealer()
    players = [player, dealer]
    game = Game(players, newdeck)

    running = True
    while running:
        if player.chips == 0:
            print("You are flat broke! It's time to leave the table.")
            input("Press any key to walk away in shame.")
            break
        game.playerbet = player.place_bet()
        game.deal()
        dealer.show_hand()
        player.show_hand()
        while game.players_turn:
            game.playerchoice(player)
        if not player.isbusted:
            dealer.show_hand(True)
            while not game.players_turn:
                if dealer.handscore < 17:
                    time.sleep(1)
                    print("\nDealer Hits")
                    game.hit(dealer)
                    time.sleep(1)
                if dealer.handscore >= 17 and not dealer.isbusted:
                    print(f"\nDealer Sticks with hand of {str(dealer.handscore)}\n")
                    break
                if dealer.isbusted:
                    game.playerwin(player)
                    break
            if not dealer.isbusted:
                game.comparescores(player, dealer)
        again = game.playagain(player)
        if not again:
            running = False
        game.players_turn = True
        game.resetplayers()


if __name__ == "__main__":
    main()
