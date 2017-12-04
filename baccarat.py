import random

SUITS = ['hearts', 'spades', 'clubs', 'diamonds']
RANKS = ['ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'jack', 'queen', 'king']

class Card:
    """Playing card to be used to fill a baccarat shoe and
    to be drawn to a playing hand.

    Args:
        rank: int or string, the rank of the card.
        suit: string, the suit of the card.

    Attributes:
        value: int, baccarat value of the card.
        rank: int or string, the rank of the card.
        suit: string, the suit of the card.

    Raises:
        ValueError: On invalid card rank or suit.
    """
    def __init__(self, rank, suit):
        if rank not in RANKS:
            raise ValueError('Invalid card rank.')
        if suit not in SUITS:
            raise ValueError('Invalid card suit.')
        self._rank = rank
        self._suit = suit
        self._value = self._rank if self._rank in range(2, 10) \
                    else 1 if self._rank == 'ace' \
                    else 0

    @property
    def value(self):
        return self._value

    @property
    def rank(self):
        return self._rank

    @property
    def suit(self):
        return self._suit

    def __add__(self, other):
        return (self._value + other) % 10

    __radd__ = __add__

    def __repr__(self):
        """Return the representation string as if the object was
        called when creating a new instance.
        """
        if isinstance(self._rank, str):
            return f'Card(\'{self._rank}\', \'{self._suit}\')'
        elif isinstance(self._rank, int):
            return f'Card({self._rank}, \'{self._suit}\')'
            

    def __str__(self):
        """Return a string with the rank and suit of the card."""
        return f'{self._rank} of {self._suit}'

class Shoe:
    """Shoe with num_decks shuffled decks. All cards used in the game
    will be drawn from this set.

    Args:
        num_decks: int, number of decks on the shoe.

    Attributes:
        num_decks: int, number of decks on the shoe.
        cards: list, all the instances of the object PlayinCard
            on the Shoe object.

    Raises:
        TypeError: If the num_decks is not an integer.
        ValueError: If the num_decks is not positive.
    """
    def __init__(self, decks):
        if not isinstance(decks, int):
            raise TypeError('Number of decks must be an integer.')
        elif decks < 1:
            raise ValueError('Number of decks must be positive.')
        self._decks = decks
        self._cards = []
        self.add_decks()

    @property
    def decks(self):
        return self._decks

    @property
    def cards(self):
        return self._cards

    def add_decks(self, decks=None):
        """Refils the shoe with decks. Uses self.decks value if empty."""
        if not decks:
            decks = self._decks

        for i in range(decks):
            for suit in SUITS:
                for rank in RANKS:
                   self._cards.append(Card(rank, suit)) 
        random.shuffle(self._cards)

    def draw_cards(self, num_cards):
        """Draws cards from shoe. Refills the shoe when
        it is empty.

        Args:
            num_cards: int, number of cards to be drawn.

        Returns:
            cards_drawn: list, cards drawn from shoe.
        """
        cards_drawn = []
        for i in range(num_cards):
            if len(self._cards) == 0:
                self.add_decks()
                print('Refilling shoe...')
            cards_drawn.append(self._cards.pop())
        return cards_drawn

    def __repr__(self):
        """Return the representation string as if the object was
        called when creating a new instance.
        """
        return f'Shoe({self._num_decks})'

    def __str__(self):
        """Returns a string with the number of decks and the
        number of cards left.
        """
        return f'{self._num_decks} decks shoe. {len(self._cards)} cards left.'

class Hand:
    """A hand of cards to be played. Either from the bank or the player.

    Args:
        cards: list, a list of card objects to be added to the hand
            using the add_cards() method.

    Atributes:
        cards: list, a list of card type objects.
        value: int, the sum of the individual card values according to
            baccarat rules.
    """
    def __init__(self, cards):
        self._cards = []
        self.add_cards(cards)
        self._value = sum(self._cards)

    @property
    def cards(self):
        return self._cards

    @property
    def value(self):
        return self._value

    def add_cards(self, cards):
        """Add cards to the hand object.

        Args:
            cards: list, a list of card type objects.

        Raises:
            TypeError: when a object different from card is present on the list
                used as argument to the add_card() method.
        """
        try:
            for card in cards:
                assert isinstance(card, Card)
                self._cards.append(card)
            self._value = sum(self._cards)
        except AssertionError:
            raise TypeError('Not a valid Card type object.')

    def is_natural(self):
        """Check if the hand is a natural according to the rules of
        the game.

        Returns:
            bol, True if is a natural, False otherwise.
        """
        if len(self._cards) == 2 and 8 <= self._value <= 9:
            return True
        return False

    def __repr__(self):
        """Return the representation string as if the object was
        called when creating a new instance.
        """
        return f'Hand({self._cards})'

    def __str__(self):
        """Return a string with all the cards on the hand."""
        return ', '.join([card.__str__() for card in self._cards])

class Punto(Hand):
    """Player(punto) hand of baccarat. Adds the third card check for
    the player. Subclass of Hand.
    """
    def __init__(self, cards):
        Hand.__init__(self, cards)

    def draw_third(self):
        """Verifies the need of a third card draw.

        Returns:
            bol, True if there is need to a third card draw,
                False otherwise.
        """
        if len(self._cards) == 2:
            if 0 <= self._value <= 5:
                return True
        return False

class Banco(Hand):
    """Bank(banco) hand of baccarat. Adds the third card check for
    the bank. Subclass of Hand.
    """
    def __init__(self, cards):
        Hand.__init__(self, cards)

    def draw_third(self, player_third=None):
        """Verifies the need of a third card draw.

        Args:
            player_third: Card object, third card of the player.

        Returns:
            bol, True if there is need to a third card draw,
                False otherwise.
        """
        third_card_rules = {3: [0, 1, 2, 3, 4, 5, 6, 7, 9],
                            4: [2, 3, 4, 5, 6, 7],
                            5: [4, 5, 6, 7],
                            6: [6, 7]}

        if len(self._cards) == 2:
            if player_third:
                try:
                    assert isinstance(player_third, Card)
                    if 0 <= self._value <= 2:
                        return True
                    elif player_third.value in third_card_rules[self._value]:
                        return True
                except AssertionError:
                    raise TypeError('Punto third card not a Card type object.')
                except KeyError:
                    return False
                return False
            else:
                if 0 <= self._value <= 5:
                    return True
        return False

class Player:
    _id = 1

    def __init__(self, balance):
        self._id = Player._id
        self._balance = balance
        self._hand_bet = None
        self._amount_bet = 0
        Player._id += 1

    @property
    def balance(self):
        return self._balance

    @property
    def hand_bet(self):
        return self._hand_bet

    @hand_bet.setter
    def hand_bet(self, hand):
        if hand not in ('punto', 'banco'):
            raise ValueError('Invalid hand')
        self._hand_bet = hand

    @property
    def amount_bet(self):
        return self._amount_bet

    @amount_bet.setter
    def amount_bet(self, amount):
        if not isinstance(amount, int) or amount < 1:
            raise TypeError('Amount must be an positive integer.')
        if amount > self._balance:
            raise ValueError('Amount exceeds available balance.')
        self._balance -= amount
        self._amount_bet = amount

    def result(self, result):
        results = {'win': self.win, 'lose': self.lose}
        if self._hand_bet not in ('punto', 'banco') or self._amount_bet == 0:
            raise TypeError('Player does not have a valid bet')
        if result not in ('win', 'lose'):
            raise TypeError('Invalid result')
        results[result]()

    def win(self):
        if self._hand_bet == 'punto':
            self._balance = self._balance + (self._amount_bet * 2)
        elif self._hand_bet == 'banco':
            self._balance = self._balance + (self._amount_bet * 1.95)
        self.lose()

    def lose(self):
        self._hand_bet = None
        self._amount_bet = 0


def show_status(player, bank):
    print(player)
    print(player.value)
    print(bank)
    print(bank.value)
    print()

def check_winner(player, bank):
    if player.value > bank.value:
        return 'Punto wins.'
    elif player.value < bank.value:
        return 'Banco wins.'
    else:
        return 'Tie.'

def main():
    shoe = Shoe(2)
    player = Punto(shoe.draw_cards(2))
    bank = Banco(shoe.draw_cards(2))

    show_status(player, bank)

    if player.is_natural() or bank.is_natural():
        print(f'{check_winner(player, bank)} Natural.')
    else:
        if player.draw_third():
            player.add_cards(shoe.draw_cards(1))
            if bank.draw_third(player.cards[2]):
                bank.add_cards(shoe.draw_cards(1))
        elif bank.draw_third():
            bank.add_cards(shoe.draw_cards(1))

        show_status(player, bank)
        print(check_winner(player, bank))

if __name__ == '__main__':
    main()
