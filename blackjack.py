from stack import Stack
from player import Player, Dealer, SplitHand
import random


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


def choose_num_players():
    while True:
        user_input = input("How many players are at the table? Enter a number between 1 and 5: ")
        try:
            user_input_int = int(user_input)
            if user_input_int in range(1, 6):
                return user_input_int
            else:
                print("Sorry, invalid selection.")
        # Try again if user inputs non numeric string
        except ValueError:
            print("Sorry, invalid selection.")


# function for user to input move decision
def choose_move():
    while True:
        user_input = input('Would you like to hit, stay, or double down? Press "H" to hit, "S" to stay, or "D" to '
                           'double down.\n')
        if user_input in ["H", "h", "S", "s", "D", "d"]:
            return user_input.upper()
        else:
            print("Sorry, invalid selection.")


# Functions for user to input wager and beginning chipstack size
def choose_wager(user_choosing_wager):
    while True:
        user_wager = input(user_choosing_wager.name + ', how much would you like to wager? Choose an a multiple of $5 '
                                                      'between $50 and $200: $')
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


def choose_to_split():
    while True:
        user_input = input('\nYou were dealt two of the same card. Would you like to place another wager to split the '
                           'cards into two hands? Press "Y" to split or "N" to keep one hand.\n')
        if user_input in ["Y", "y", "N", "n"]:
            return user_input.upper()
        else:
            print("Sorry, invalid selection.")


def add_wagers_to_pot(hand_doing_betting, dealer_matching_bet, amount_wagered):
    total_bet = 0
    total_bet += hand_doing_betting.wager(amount_wagered)
    total_bet += dealer_matching_bet.wager(amount_wagered)
    if hand_doing_betting.double_down:
        total_bet += hand_doing_betting.wager(amount_wagered)
        total_bet += dealer_matching_bet.wager(amount_wagered)
    return total_bet


def dealt_blackjack(hand_that_won, dealer_paying_out, amount_in_pot):
    print(hand_that_won.name + " won with a natural Blackjack and gets bonus chips! Congratulations!\n")
    # Player wins 3/2s the wager with natural Blackjack
    hand_that_won.won_hand(amount_in_pot)
    # Pot holds 2x wager amount, so extra 1/2 wager == 1/4 pot
    bonus_chips = round_to_five(0.25 * amount_in_pot)
    hand_that_won.won_hand(bonus_chips)
    dealer_paying_out.chipstack -= bonus_chips


# Function for rounding to multiple of 5 used when wagers multiplied by fractions
def round_to_five(amount):
    return int(5 * round(amount / 5))


# START THE GAME #


# Welcome message and player name input
print("\n\n           =================\n"
      "Welcome to Python Blackjack! Good luck!\n"
      "           =================\n\n")

num_players = choose_num_players()
print('')

# Create dealer and players
dealer = Dealer("Dealer", 5000)
player_list = []
player_counter = 0
for player in range(num_players):
    username = input("Player " + str(player_counter + 1) + ", please enter your Python Blackjack username: ")
    chipstack = choose_starting_chipstack()
    print('')
    user = Player(username, chipstack)
    player_list.append(user)
    player_counter += 1

# Outer while loop for entire play session
while True:

    # Reset game variables for subsequent games
    # Hands at table may increase for individual games due to split hand and must be reset
    hands_at_table_list = [player for player in player_list]
    # Wager dictionary to track wagers for payouts
    wager_dict = {}
    dealer.hand = []
    dealer.busted = False
    dealer.got_blackjack = False
    for individual_hand in hands_at_table_list:
        individual_hand.hand = []
        individual_hand.busted = False
        individual_hand.got_blackjack = False
        individual_hand.double_down = False

    # Give more money if all has been lost
    if dealer.chipstack <= 1000:
        print("You're breaking the bank! Giving the dealer another $10000.\n")
        dealer.chipstack += 10000
    for player in hands_at_table_list:
        if player.chipstack <= 50:
            print("You're broke! Time for a visit to the ATM?\n")
            more_money = choose_starting_chipstack()
            player.chipstack += more_money

    # Inner while loop for individual games
    while True:
        # Inform users of chip stacks
        print("------------------\nCurrent Chipstacks\n------------------")
        dealer.print_chipsatck()
        for player in hands_at_table_list:
            player.print_chipsatck()
        print('')

        #  Confirm initial wagers
        for player in hands_at_table_list:
            while True:
                wager_amount = choose_wager(player)
                if wager_amount <= player.chipstack:
                    print("\n" + player.name + " wagered $" + str(wager_amount) + ".\n")
                    wager_dict[player.name] = wager_amount
                    break
                else:
                    print("You can't afford to wager that much.")

        # Shuffle a new deck and deal first cards
        current_deck = build_deck()
        print("\nDealing cards to start the game!\n")
        dealer.deal_cards(current_deck)
        for user in hands_at_table_list:
            user.deal_cards(current_deck)

        # Each hand takes a turn
        for individual_hand in hands_at_table_list:
            print("\n" + individual_hand.name + "'s Turn\n--------------")

            # Check for card split opportunity and create SplitHand object if user desires
            if individual_hand.hand[0] == individual_hand.hand[1]:
                if individual_hand.chipstack > wager_dict[individual_hand.name]:
                    individual_hand.print_hand()
                    split_choice = choose_to_split()
                    if split_choice == "Y":
                        # Create new Split Hand object for new hand
                        split_hand = SplitHand(individual_hand, individual_hand.name + "'s split hand")
                        # Add new hand to hands at table list and add appropriate wager to dictionary
                        hands_at_table_list.append(split_hand)
                        wager_dict[split_hand.name] = wager_dict[individual_hand.name]
                        # Deal second card to original user hand
                        individual_hand.second_card(current_deck)
                        individual_hand.get_hand_value()
                        split_hand.second_card(current_deck)
                        split_hand.get_hand_value()

            individual_hand.print_hand()
            individual_hand.print_hand_value()

            while True:
                # If user busted or got blackjack they don't need more cards
                if individual_hand.hand_value > 21:
                    break
                elif individual_hand.hand_value == 21:
                    print(individual_hand.name + " is stopping at 21!\n")
                    break
                else:
                    user_choice = choose_move()
                    if user_choice == "H":
                        individual_hand.hit(current_deck)
                    elif user_choice == "S":
                        individual_hand.stay()
                        break
                    # If user chooses to double down, double user wager and deal one more card
                    elif user_choice == "D":
                        print(individual_hand.name + " doubled their wager and only gets one more card.\n")
                        individual_hand.hit(current_deck)
                        individual_hand.double_down = True
                        break

        # If all hands busted or all hands got natural blackjack game ends immediately
        hands_busted_list = []
        for individual_hand in hands_at_table_list:
            hands_busted_list.append(individual_hand.busted)

        natural_blackjack_list = []
        for individual_hand in hands_at_table_list:
            natural_blackjack_list.append(individual_hand.got_blackjack)

        if all(hands_busted_list) or all(natural_blackjack_list):

            print("\n============\nGame Results\n============")

            for individual_hand in hands_at_table_list:

                # Function removes wagers from chipstacks of player and dealer and creates the pot for each hand
                pot = add_wagers_to_pot(individual_hand, dealer, wager_dict[individual_hand.name])

                print("\n\n" + individual_hand.name + "'s Results\n----------------")

                if individual_hand.busted:
                    print(individual_hand.name + " busted.\n")
                    dealer.won_hand(pot)
                    individual_hand.print_chipsatck()

                if individual_hand.got_blackjack:
                    dealt_blackjack(individual_hand, dealer, pot)

                dealer.print_chipsatck()

            # Dealer turn skipped, break out of current game
            break

        print("Dealer Turn\n-----------")
        dealer.print_hand()
        dealer.print_hand_value()
        while True:
            # If dealer busted or got blackjack they don't need more cards
            if dealer.hand_value > 20:
                break
            # Dealer must hit if hand value under 17 or if hand value is 17 and hand contains an Ace
            elif dealer.hand_value < 17 or dealer.hand_value == 17 and "A" in dealer.hand:
                dealer.hit(current_deck)
            else:
                dealer.stay()
                break

        print("\n============\nGame Results\n============")

        # Loop to do results for each hand. Pot counter corresponds to index of appropriate bet pool
        for individual_hand in hands_at_table_list:

            # Function removes wagers from chipstacks of player and dealer and creates the pot for the hand
            pot = add_wagers_to_pot(individual_hand, dealer, wager_dict[individual_hand.name])

            print("\n\n" + individual_hand.name + "'s Results\n----------------")
            print(individual_hand.name + ": " + str(individual_hand.hand_value))
            print(dealer.name + ": " + str(dealer.hand_value) + "\n")

            # Assess winners and pay out
            # Player automatically wins and gets bonus chips if dealt blackjack
            if individual_hand.got_blackjack:
                dealt_blackjack(individual_hand, dealer, pot)

            # Player automatically loses with bust, regardless of dealer outcome
            elif individual_hand.busted:
                print(individual_hand.name + " busted.\n")
                dealer.won_hand(pot)

            elif individual_hand.hand_value == dealer.hand_value:
                print("Hands are equivalent so game results in a push. Wagers are returned.\n")
                individual_hand.won_hand(int(0.5 * pot))
                dealer.won_hand(int(0.5 * pot))

            elif individual_hand.hand_value > dealer.hand_value or dealer.busted:
                print(individual_hand.name + " won! Congratulations!\n")
                individual_hand.won_hand(pot)

            else:
                print(individual_hand.name + " lost.\n")
                dealer.won_hand(pot)

            dealer.print_chipsatck()
            individual_hand.print_chipsatck()

        # Break out of loop for individual game
        break

    # Play again or break out of play session
    replay_decision = input('\nWould you like to play again? Press "N" to quit or any other key to continue.\n')
    if replay_decision == "N" or replay_decision == "n":
        break
