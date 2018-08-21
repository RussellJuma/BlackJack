import random
from os import system, name

players = []
deck_of_cards = []


class Card:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class DeckOfCards:
    card_count = 0

    def generate_deck(number_of_players):
        if number_of_players <= 3:
            number_of_decks = 3
        else:
            number_of_decks = number_of_players

        deck_count = 0
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

        while number_of_decks >= deck_count:
            count = 0
            card_value = 13
            while card_value >= count:
                if count == 0:
                    for suit in suits:  # Ace
                        deck_of_cards.append(Card("Ace of " + suit, 11))
                elif 10 >= count > 1:  # 2 - 10
                    for suit in suits:
                        deck_of_cards.append(Card(str(count) + " " + suit, count))
                elif count == 11:  # Jack
                    for suit in suits:
                        deck_of_cards.append(Card("Jack of " + suit, 10))
                elif count == 12:  # Queen
                    for suit in suits:
                        deck_of_cards.append(Card("Queen of " + suit, 10))
                elif count == 13:  # King
                    for suit in suits:
                        deck_of_cards.append(Card("King of " + suit, 10))
                count = count + 1
            deck_count = deck_count + 1
        DeckOfCards.shuffle()

    def shuffle():
        random.shuffle(deck_of_cards)

    def pull_card():
        DeckOfCards.card_count = DeckOfCards.card_count + 1
        if DeckOfCards.card_count < len(deck_of_cards):
            return deck_of_cards[DeckOfCards.card_count-1]
        elif DeckOfCards.card_count == len(deck_of_cards):
            DeckOfCards.shuffle()
            DeckOfCards.card_count = 0
            DeckOfCards.pull_card()


class Player:
    def __init__(self, name):
        self.name = str(name)
        self.balance = 500
        self.cards = []

    def hand(self, card_1, card_2, reset):
        if reset == "clear":
            self.cards.clear()
        self.cards.append(card_1)
        self.cards.append(card_2)
        self.hand_value = card_check(self.cards)

    def hit(self, card):
        self.cards.append(card)
        self.hand_value = card_check(self.cards)

    def bet(self, wager):
        while not wager.isdigit():
            input("Bet cannot contain letters, must be a digit, how much?")

        self.wager = int(wager)
        if (self.balance - self.wager) >= 0:
            self.balance = self.balance - self.wager
            return self.wager
        elif wager == 0:
            print(self.name + " bet $0")
            return self.wager
        else:
            Player.bet(input("Not enough funds! You have $" + str(self.balance)))


class Dealer:
    def __init__(self):
        if len(players) > 1:
            count = 0
            names = ""
            while count < (len(players)-1):
                names = names + str(players[count].name) + ", "
                count = count + 1
            names = names + "and " + str(players[len(players)-1].name)
        else:
            names = str(players[0].name)
        print("Welcome " + names + " to BlackJack!!!")
        self.cards = []

    def hand(self, card_1, card_2, reset):
        if reset == "clear":
            self.cards.clear()
        self.cards.append(card_1)
        self.cards.append(card_2)
        self.hand_value = card_check(self.cards)

    def hit(self, card):
        self.cards.append(card)
        self.hand_value = card_check(self.cards)

    def deal_cards(self):
        for player in players:
            print(player.name + "'s Balance $" + str(player.balance))
            player.bet(input(player.name + " how much do you want to bet?"))
            if player.wager > 0:
                card_1 = DeckOfCards.pull_card()
                card_2 = DeckOfCards.pull_card()
                player.hand(card_1, card_2, "clear")
        card_1 = DeckOfCards.pull_card()
        card_2 = DeckOfCards.pull_card()
        self.hand(card_1, card_2, "clear")
        for player in players:
            self.request_hit(player)
        self.play()

    def request_hit(self, player):
        clear_screen()
        print("The dealer has a " + str(dealer.cards[0].name) + " showing.")
        card_output = ""
        for card in player.cards:
            card_output = "|" + card.name + "|" + card_output
        print(player.name + " have a " + card_output + " for a total of " + str(player.hand_value))
        if player.hand_value < 22:
            while True:
                response = input("Do you want to hit? (Y/N)")
                if response == "Y":
                    player.hit(DeckOfCards.pull_card())
                    self.request_hit(player)
                    break
                elif response == "N":
                    break
                    return
        else:
            print(player.name + " Busted")

    def play(self):
        #Trying to beat the majority of the players
        average_value = []
        for player in players:
            if player.hand_value <=21:
                average_value.append(player.hand_value)
        if sum(average_value) == 0:
            average_value.append(1)
        average = (sum(average_value)/(len(average_value)))
        while self.hand_value < average:
            self.hit(DeckOfCards.pull_card())

        for player in players:
            output = "Dealer has " + str(self.hand_value) + " | " + player.name + " has " + str(player.hand_value) + " | "
            if self.hand_value == 21: #Win - Black Jack
                print("Dealer has BlackJack")
                if player.hand_value == 21:
                    player.balance = player.balance + player.wager
                    print(player.name + " loses $0")
                else:
                    print(output + player.name + " lost $" + str(player.wager))
            elif self.hand_value < player.hand_value and player.hand_value <= 21: #Win - Dealer loss
                player.balance = player.balance + player.wager * 2
                print(output + player.name + " Wins $" + str(player.wager * 2))
            elif self.hand_value > player.hand_value and self.hand_value <= 21: #Loss - Dealer Win
                print(output + player.name + " lost $" + str(player.wager))
            elif self.hand_value > 21 and player.hand_value <=21: #Win - Dealer Bust
                player.balance = player.balance + player.wager * 2
                print(output + "Dealer bust " + player.name + " Wins $" + str(player.wager * 2))
            elif player.hand_value > 21: #Loss - Player Bust
                print(output + player.name + " busted, loses $" + str(player.wager))
            elif self.hand_value == player.hand_value:  # Loss - Player Bust #Stand Off
                player.balance = player.balance + player.wager
                print(output + player.name + " Stand Off, loses $0")
        players_to_remove = []
        for player in players:
            if player.balance == 0:
                print(player.name + " have a nice day, you no longer have money to play")
                players_to_remove.append(player)
        for player in players:
            while True:
                response = input(player.name + " do you want to continue? (Y/N) ")
                if response == "Y":
                    break
                if response == "N":
                    break
            if response == "Y":
                clear_screen()
            elif response == "N":
                if player.balance >= 500:
                    print("Have a nice day " + player.name + ", you won $" + str(player.balance - 500) + " for a total of $" + str(player.balance))
                else:
                    print("Have a nice day " + player.name + ", you lost $" + str(player.balance - 500) + " for a total of $" + str(player.balance))
                players_to_remove.append(player)

        for player in players_to_remove:
            players.remove(player)

        if len(players) == 0:
            new_game()
        else:
            self.deal_cards()


def card_check(cards):
    card_total = 0
    cards = sorted(cards, key=lambda Card: Card.value)

    for card in cards:
        if card.value < 11:
            card_total = card_total + card.value
        elif card.value == 11:
            if card_total > 11:
                card_total = card_total + 1
            else:
                card_total = card_total + card.value
    return card_total

def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
def new_game():
    number_of_players = input("How many players?")
    count = 0

    if number_of_players.isdigit():
        if number_of_players != "0":
            number_of_players = int(number_of_players)
        else:
            print("Cannot be 0, try again.")
            new_game()
    else:
        print("Cannot contain letters, try again")
        new_game()

    while number_of_players > count:
        duplicate = False
        input_name = input("What is the name of player " + str(count + 1) + "?")
        while input_name == "" or input_name.isdigit():
            input_name = input("What is the name of player " + str(count + 1) + "?")
        while True:
            for player in players:
                if input_name == player.name:
                    duplicate = True
                    break
                else:
                    duplicate = False
            if duplicate == True:
                input_name = input(input_name + " is already taken, choose another name for player " + str(count + 1) + "?")
            elif duplicate == False:
                break
        players.append(Player(input_name))
        count = count + 1
    DeckOfCards.generate_deck(number_of_players)

new_game()
dealer = Dealer()
dealer.deal_cards()