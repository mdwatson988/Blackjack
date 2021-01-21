class Player:
    def __init__(self, name, chipstack):
        self.hand = []
        self.hand_value = 0
        self.busted = False
        self.got_blackjack = False
        self.name: str = name
        self.chipstack: int = chipstack

    def get_hand_value(self):
        # Hand value must be recalculated after each card dealt in case previous ace value must be changed from 11 to 1
        self.hand_value = 0
        ace_counter = 0
        for i in self.hand:
            # Integers counted
            if type(i) == int:
                self.hand_value += i
            # J, Q, K counted as 10
            elif type(i) == str:
                if i != "A":
                    self.hand_value += 10
                # count aces so they can be scored and added last
                else:
                    ace_counter += 1
        if ace_counter > 0:
            # Logic to determine if aces should count as 11 or 1
            if self.hand_value + 10 + ace_counter <= 21:
                self.hand_value += (10 + ace_counter)
            else:
                self.hand_value += ace_counter
        # Check for bust or blackjack
        if self.hand_value > 21:
            print(self.name + " busted.\n")
            self.busted = True
        if self.hand_value == 21:
            print(self.name + " got Blackjack!\n")
            self.got_blackjack = True

    def deal_cards(self, card_deck):
        for i in range(2):
            self.hand.append(card_deck.pop())
        print("\n" + self.name + " was dealt " + str(self.hand) + ".")
        self.get_hand_value()
        # Inform user of hand values of anything under 21
        self.print_hand_value()

    def hit(self, card_deck):
        new_card = card_deck.pop()
        self.hand.append(new_card)
        print(self.name + " hit and drew " + str(new_card) + ".\n")
        self.print_hand()
        self.get_hand_value()
        # Inform user of hand values of anything under 21
        if not self.busted and not self.got_blackjack:
            self.print_hand_value()

    def stay(self):
        self.get_hand_value()
        print(self.name + " stayed at " + str(self.hand_value) + ".\n")

    def print_hand(self):
        print(self.name + "'s current hand is " + str(self.hand) + ".")

    def print_hand_value(self):
        print(self.name + "'s current hand value is " + str(self.hand_value) + ".\n")

    def wager(self, amount):
        self.chipstack -= amount
        print("\n" + self.name + " wagered $" + str(amount) + ".\n")
        return amount

    def won_hand(self, amount):
        self.chipstack += amount

    def print_chipsatck(self):
        print(self.name + "'s current chip stack value is $" + str(self.chipstack) + ".\n")

class Dealer(Player):
    # Dealer only dealt one card
    def deal_cards(self, card_deck):
        self.hand.append(card_deck.pop())
        print(self.name + " was dealt " + str(self.hand) + ".")
        self.get_hand_value()

    def wager(self, amount):
        self.chipstack -= amount
        return amount

    def print_chipsatck(self):
        print("\n" + self.name + "'s current chip stack value is $" + str(self.chipstack) + ".")
