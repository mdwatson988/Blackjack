from stack import Stack
from player import Player
import random


# function for user to input move choice
def choose_move():
    while True:
        user_input = input('Would you like to hit or stay? Press "H" to hit or "S" to stay.\n')
        if user_input == "H" or user_input == "h":
            return user_input.upper()
        elif user_input == "S" or user_input == "s":
            return user_input.upper()
        else:
            print("Sorry, invalid selection.")


# Create randomized deck as a Stack with cards as Nodes
def build_deck():
    # First create a list of all cards
    card_list = []
    counter = 0
    while counter < 4:
        royal_cards = ["J", "Q", "K", "A"]
        for i in range(2, 11):
            card_list.append(i)
        for i in royal_cards:
            card_list.append(i)
        counter += 1
    # Randomize list
    random.shuffle(card_list)
    # Create deck by linking cards from list into a Stack
    deck = Stack("Card Deck")
    for i in card_list:
        deck.push(i)
    return deck


# Welcome message and player name input
print("\n\n           -----------------\n\n"
      "Welcome to Python Blackjack! Good luck!\n\n"
      "           -----------------\n")

username = input("Please enter your Python Blackjack username: ")
# Create player and dealer
dealer = Player("Dealer")
user = Player(username)

# Start the game
# Outer while loop for entire play session
while True:

    # Reset player variables for subsequent games
    dealer.hand = []
    user.hand = []
    dealer.busted = False
    dealer.got_blackjack = False
    user.busted = False
    user.got_blackjack = False

    # Inner while loop for individual games
    while True:
        # Shuffle a new deck and deal first cards
        current_deck = build_deck()
        print("\nDealing cards to start the game!\n")
        dealer.deal_cards(current_deck)
        user.deal_cards(current_deck)

        # Player automatically wins if dealt blackjack and dealer not also dealt blackjack
        if user.got_blackjack and not dealer.got_blackjack:
            print("Congratulations, you won with a natural Blackjack!\n")
            break

        print("Player Turn\n-----------")
        while True:
            # If user busted or got blackjack they don't need more cards
            if user.busted or user.got_blackjack:
                break
            else:
                user_choice = choose_move()
                if user_choice == "H":
                    user.hit(current_deck)
                elif user_choice == "S":
                    user.stay()
                    break

        # Player automatically loses with bust, regardless of dealer outcome
        if user.busted:
            print("Sorry, you lost.\n")
            break

        print("Dealer Turn\n-----------")
        dealer.print_hand()
        dealer.print_hand_value()
        while True:
            # If dealer busted or got blackjack they don't need more cards
            if dealer.busted or dealer.got_blackjack:
                break
            # Dealer must hit if hand value under 17 or if hand value is 17 and hand contains an Ace
            elif dealer.hand_value < 17 or dealer.hand_value == 17 and "A" in dealer.hand:
                dealer.hit(current_deck)
            else:
                dealer.stay()
                break

        print("------------\nGame Results\n------------")
        print(user.name + ": " + str(user.hand_value))
        print(dealer.name + ": " + str(dealer.hand_value) + "\n")

        # Assess winner
        if user.hand_value == dealer.hand_value:
            print("Hands are equivalent so game results in a push.\n")
        elif user.hand_value > dealer.hand_value or dealer.busted:
            print("Congratulations, you won!\n")
        else:
            print("Sorry, you lost.\n")
        break

    # Play again or break out of play session
    replay_decision = input('\nWould you like to play again? Press "N" to quit or any other key to continue.\n')
    if replay_decision == "N" or replay_decision == "n":
        break
