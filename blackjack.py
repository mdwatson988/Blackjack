from stack import Stack
from player import Player, Dealer
import random


# function for user to input move decision
def choose_move():
    while True:
        user_input = input('Would you like to hit or stay? Press "H" to hit or "S" to stay.\n')
        if user_input == "H" or user_input == "h":
            return user_input.upper()
        elif user_input == "S" or user_input == "s":
            return user_input.upper()
        else:
            print("Sorry, invalid selection.")


# Functions for user to input wager and beginning chipstack size
def choose_wager():
    while True:
        user_wager = input('How much would you like to wager? Choose an a multiple of $5 between $50 and $200: $')
        try:
            user_wager_int = int(user_wager)
            if 50 <= user_wager_int <= 200 and user_wager_int % 5 == 0:
                return user_wager_int
            else:
                print("Sorry, invalid selection.")
        # Try again if user inputs non numeric string
        except ValueError:
            print("Sorry, invalid selection.")


def choose_starting_chipstack():
    while True:
        user_chipstack = input('How much money are you bringing to the table? Choose an a multiple of $100 between '
                               '$500 and $2000: $')
        try:
            user_chipstack_int = int(user_chipstack)
            if 500 <= user_chipstack_int <= 2000 and user_chipstack_int % 100 == 0:
                return user_chipstack_int
            else:
                print("Sorry, invalid selection.")
        # Try again if user inputs non numeric string
        except ValueError:
            print("Sorry, invalid selection.")


# Function for rounding to multiple of 5 used when wagers multiplied by fractions
def round_to_five(amount):
    return int(5 * round(amount / 5))


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
print("\n\n           =================\n"
      "Welcome to Python Blackjack! Good luck!\n"
      "           =================\n\n")

username = input("Please enter your Python Blackjack username: ")
chipstack = choose_starting_chipstack()

# Create player and dealer
dealer = Dealer("Dealer", 10000)
user = Player(username, chipstack)

# Start the game
# Outer while loop for entire play session
while True:

    # Reset game variables for subsequent games
    dealer.hand = []
    user.hand = []
    total_pot = 0
    dealer.busted = False
    dealer.got_blackjack = False
    user.busted = False
    user.got_blackjack = False
    # Give dealer more money if all has been lost
    if dealer.chipstack <= 0:
        dealer.chipstack += 10000

    # Inner while loop for individual games
    while True:
        # Inform user of chip stacks and do initial wager
        dealer.print_chipsatck()
        user.print_chipsatck()
        while True:
            wager_amount = choose_wager()
            if wager_amount <= user.chipstack:
                total_pot += user.wager(wager_amount)
                total_pot += dealer.wager(wager_amount)
                break
            else:
                print("You can't afford to wager that much.")


        # Shuffle a new deck and deal first cards
        current_deck = build_deck()
        print("\nDealing cards to start the game!\n")
        dealer.deal_cards(current_deck)
        user.deal_cards(current_deck)

        # Player automatically wins if dealt blackjack
        if user.got_blackjack:
            print("Congratulations, you won with a natural Blackjack and get bonus chips!")
            # Player wins 3/2s the wager with natural Blackjack
            user.won_hand(total_pot)
            bonus_chips = round_to_five(1 / 2 * wager_amount)
            user.chipstack += bonus_chips
            dealer.chipstack -= bonus_chips
            dealer.print_chipsatck()
            user.print_chipsatck()
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
            print("Sorry, you lost.")
            dealer.won_hand(total_pot)
            dealer.print_chipsatck()
            user.print_chipsatck()
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

        print("\n============\nGame Results\n============\n")
        print(user.name + ": " + str(user.hand_value))
        print(dealer.name + ": " + str(dealer.hand_value) + "\n")

        # Assess winner
        if user.hand_value == dealer.hand_value:
            print("Hands are equivalent so game results in a push. Wagers are returned.")
            user.chipstack += wager_amount
            dealer.chipstack += wager_amount
        elif user.hand_value > dealer.hand_value or dealer.busted:
            print("Congratulations, you won!")
            user.won_hand(total_pot)
        else:
            print("Sorry, you lost.")
            dealer.won_hand(total_pot)

        dealer.print_chipsatck()
        user.print_chipsatck()
        break

    # Play again or break out of play session
    replay_decision = input('\nWould you like to play again? Press "N" to quit or any other key to continue.\n')
    if replay_decision == "N" or replay_decision == "n":
        break
