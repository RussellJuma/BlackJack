import random

players = []
deck_of_cards = []

class Card:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class DeckOfCards:

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

    card_count = 0

    def pull_card(self, card_count):
        card_count = card_count + 1
        if card_count < len(deck_of_cards):
            return deck_of_cards[card_count-1]
        elif card_count == len(deck_of_cards):
            DeckOfCards.shuffle()
            DeckOfCards.pull_card(0)

class Player:
    def __init__(self, name):
        self.name = str(name)
        self.balance = 500

    def hand(self, card_1, card_2, reset):
        if reset == "clear":
            self.cards.clear()
        self.cards.append(card_1)
        self.cards.append(card_2)
        card_check(sum(self.cards))

    def hit(self, card):
        card_check(sum(self.cards.append(card)))

    def bet(self, wager):
        while not wager.isdigit():
            input("Cannot contain letters, must be a digit, try again")

        if self.balance - wager >= 0:
            self.balance = self.balance - wager
            self.wager = wager
            return self.wager
        elif wager == 0:
            print(self.name + " bet $0")
            return self.wager
        else:
            Player.bet(input("Not enough funds! You have $" + self.balance))


class Dealer:
    def hand(self, card_1, card_2, reset):
        if reset == "clear":
            self.cards.clear()
        self.cards.append(card_1)
        self.cards.append(card_2)
        card_check(sum(self.cards))

    def hit(self, card):
        card_check(sum(self.cards.append(card)))

    def deal_cards():
        for player in players:
            player.bet(input(player.name + " how much do you want to bet? You have $" + player.balance))
            if player.wager > 0:
                card_1 = DeckOfCards.pull_card()
                card_2 = DeckOfCards.pull_card()
                Player.hand(card_1, card_2, "clear")
        card_1 = DeckOfCards.pull_card()
        card_2 = DeckOfCards.pull_card()
        Dealer.hand(card_1, card_2, "clear")

def card_check(card_value):
    if card_value > 21:
        return "Bust"
    elif card_value == 21:
        return "Black Jack"
    else:
        return card_value

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
        input_name = input("What is the name of player " + str(count + 1) + "?")
        while input_name == "":
            input_name = input("What is the name of player " + str(count + 1) + "? It cannot be nothing!")
        while input_name in players:
            input_name = input(input_name + " is already taken, choose another name for player " + str(count + 1) + "?")
        players.append(Player(input_name))
        count = count + 1
    DeckOfCards.generate_deck(number_of_players)


new_game()
Dealer.deal_cards()