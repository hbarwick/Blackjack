# Blackjack.py
# A command line blackjack game

import random
import time
import itertools


class Deck:
    suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)

    def fill_deck(self):
        """Load deck with 6 decks of cards"""
        for i in range(0, 6):
            for suit, value in itertools.product(self.suits, self.values):
                self.cards.append(Card(suit, value))

    def clear_deck(self):
        self.cards = []

    def shuffle(self):
        random.shuffle(self.cards)


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"

    @property
    def cardscore(self):
        if self.value in ["Jack", "Queen", "King"]:
            return 10
        if self.value in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            return int(self.value)
        if self.value == "Ace":
            return 1


class Player:
    def __init__(self):
        self.hand = []

    def show_hand(self):
        print("\nPlayers Hand:")
        for n, card in enumerate(self.hand):
            print(str(self.hand[n]))
        print()

    def reset(self):
        self.hand = []

    @property
    def ace_count(self):
        return len([c for c in self.hand if c.value == "Ace"])

    @property
    def handscore(self):
        return sum([c.cardscore for c in self.hand])

    @property
    def handscore_ace_adjusted(self):
        for ace in range(self.ace_count):
            if self.handscore < 12:
                self.handscore += 10
        return self.handscore

    @property
    def isbusted(self):
        if self.handscore_ace_adjusted > 21:
            return True


class Human(Player):
    def __init__(self, chips):
        super().__init__()
        self.chips = chips

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


class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.hand = []

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
    def __init__(self):
        self.players = []
        self.deck = []
        self.playerbet = 0
        self.players_turn = True

    def deal(self):
        print(f"{len(self.deck)} cards in Deck")
        if len(self.deck) < 104:  # When stack gets to total of 2 card decks remaining, reshuffle 6 decks
            print("Reshuffling decks...")
            self.deck.clear_deck()
            self.deck.fill_deck()
            self.deck.shuffle()
            time.sleep(4)
        for i in range(2):
            for player in self.players:
                card = self.deck.cards.pop()
                player.hand.append(card)

    def hit(self, player):
        card = self.deck.cards.pop()
        player.hand.append(card)
        if isinstance(player, Dealer):
            player.show_hand(True)
        else:
            player.show_hand()
        self.checkbust(player)
        print(f"player handscore is {player.handscore_ace_adjusted}")

    def playerchoice(self, player):
        answer = input("Hit or Stick? H/S: ")
        if answer.lower() == "h":
            self.hit(player)
        if answer.lower() == "s":
            print(f"Player Sticks with hand of {str(player.handscore_ace_adjusted)}\n")
            self.players_turn = False

    def checkbust(self, player):
        if player.isbusted:
            if isinstance(player, Human):
                print("Player Busts!")
                self.players_turn = False
                self.playerlose()
            if isinstance(player, Dealer):
                print("\nDealer Busts!")

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
        if player.handscore_ace_adjusted > dealer.handscore_ace_adjusted:
            self.playerwin(player)
        if player.handscore_ace_adjusted == dealer.handscore_ace_adjusted:
            self.draw(player)
        if player.handscore_ace_adjusted < dealer.handscore_ace_adjusted:
            self.playerlose()

    def resetplayers(self):
        for player in self.players:
            player.reset()
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

    def play(self):
        print("\n---------- Welcome to Blackjack ----------\n")
        self.deck = Deck()
        player = Human(100)
        dealer = Dealer()
        self.players = [player, dealer]
        self.deck.fill_deck()
        self.deck.shuffle()
        running = True
        while running:
            if self.players[0].chips == 0:
                print("You are flat broke! It's time to leave the table.")
                input("Press any key to walk away in shame.")
                break
            self.playerbet = player.place_bet()
            self.deal()
            dealer.show_hand()
            player.show_hand()
            while self.players_turn:
                self.playerchoice(player)
            if not player.isbusted:
                dealer.show_hand(True)
                while not self.players_turn:
                    if dealer.handscore_ace_adjusted < 17:
                        time.sleep(1)
                        print("\nDealer Hits")
                        self.hit(dealer)
                        time.sleep(1)
                    if dealer.handscore_ace_adjusted >= 17 and not dealer.isbusted:
                        print(f"\nDealer Sticks with hand of {str(dealer.handscore_ace_adjusted)}\n")
                        break
                    if dealer.isbusted:
                        self.playerwin(player)
                        break
                if not dealer.isbusted:
                    self.comparescores(player, dealer)
            again = self.playagain(player)
            if not again:
                running = False
            self.players_turn = True
            self.resetplayers()


def main():
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
