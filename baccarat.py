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

    @property
    def value(self):
        """Returns the value of the card according to 
        baccarat rules.
        """
        if self._rank in range(2, 10):
            return self._rank
        elif self._rank == 'ace':
            return 1
        else:
            return 0

    @property
    def rank(self):
        return self._rank

    @property
    def suit(self):
        return self._suit

    def __add__(self, other):
        return (self.value + other) % 10

    __radd__ = __add__

    def __repr__(self):
        """Return the representation string as if the object was
        called when creating a new instance.
        """
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
    def __init__(self, num_decks):
        if not isinstance(num_decks, int):
            raise TypeError('Number of decks must be an integer.')
        elif num_decks < 1:
            raise ValueError('Number of decks must be positive.')
        self._num_decks = num_decks
        self.add_decks()

    @property
    def num_decks(self):
        return self._num_decks

    @property
    def cards(self):
        return self._cards

    def add_decks(self):
        """Refils the shoe with num_decks decks."""
        self._cards = []
        for i in range(self._num_decks):
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
