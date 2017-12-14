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
        """Get card value."""
        return self._value

    @property
    def rank(self):
        """Get card rank."""
        return self._rank

    @property
    def suit(self):
        """Get card suit."""
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
    def __init__(self, num_decks):
        if not isinstance(num_decks, int):
            raise TypeError('Number of decks must be an integer.')
        elif num_decks < 1:
            raise ValueError('Number of decks must be positive.')
        self._num_decks = num_decks
        self._cards = []
        self.add_decks()

    @property
    def num_decks(self):
        """Get shoe number of decks."""
        return self._num_decks

    @property
    def cards(self):
        """Get shoe cards list."""
        return self._cards

    def add_decks(self, num_decks=None):
        """Refils the shoe with decks. Uses self.num_decks value if empty."""
        if not num_decks:
            num_decks = self._num_decks

        for i in range(num_decks):
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
    """A hand of cards to be played. Either from the banker or the player.

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

    @property
    def cards(self):
        """Get hand cards list."""
        return self._cards

    @property
    def value(self):
        """Get hand value."""
        return sum(self._cards)

    def add_cards(self, cards):
        """Add cards to the hand object.

        Args:
            cards: list, a list of card type objects.

        Raises:
            TypeError: when a object different from card is present on the list
                used as argument to the add_card() method.
        """
        for card in cards:
            if not isinstance(card, Card):
                raise TypeError('Not a valid Card type object.')
            self._cards.append(card)

    def is_natural(self):
        """Check if the hand is a natural according to the rules of
        the game.

        Returns:
            bol, True if is a natural, False otherwise.
        """
        if len(self._cards) == 2 and 8 <= self.value <= 9:
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
            if 0 <= self.value <= 5:
                return True
        return False

class Banco(Hand):
    """Banker(banco) hand of baccarat. Adds the third card check for
    the banker. Subclass of Hand.
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
                if not isinstance(player_third, Card):
                    raise TypeError('Punto third card not a Card type object.')
                if 0 <= self.value <= 2:
                    return True
                elif 3 <= self.value <= 6:
                    if player_third.value in third_card_rules[self.value]:
                        return True
            else:
                if 0 <= self.value <= 5:
                    return True
        return False

class Player:
    """A player of baccarat game. Create several instances to have multiplayer.

    Args:
        balance: int, the initial balance of the player.

    Atributes:
        pid: int, sequencial id number of the playeri.
        balance: int, the balance of player.
        hand_bet: str, the hand in which the player is betting.
        amount_bet: int, the amount of a bet.

    Raises:
        TypeError: if the balance is not an integer.
        ValueError: if the balance is not positive.
    """
    _pid = 1

    def __init__(self, balance):
        if not isinstance(balance, int):
            raise TypeError('Balance must be an integer.')
        elif balance < 1:
            raise ValueError('Balance must be positive.')
        self._pid = Player._pid
        self._balance = balance
        self._hand_bet = None
        self._amount_bet = 0
        Player._pid += 1

    @property
    def pid(self):
        """Get the player id."""
        return self._pid

    @property
    def balance(self):
        """Get the player balance."""
        return self._balance

    @property
    def hand_bet(self):
        """Get the hand on which the bet was made.

        Raises:
            ValueError: When setting if the value is neither punto,
                banco or tie.
        """
        return self._hand_bet

    @hand_bet.setter
    def hand_bet(self, hand):
        if hand not in ['punto', 'banco', 'tie']:
            raise ValueError('Invalid hand')
        self._hand_bet = hand

    @property
    def amount_bet(self):
        """Get the amount of a bet.

        Raises:
            TypeError: When setting if the amount is a integer.
            ValueError: When setting if the amount exceed the
                available balance.
        """
        return self._amount_bet

    @amount_bet.setter
    def amount_bet(self, amount):
        if not isinstance(amount, int):
            raise TypeError('Amount must be a integer.')
        if amount < 1:
            raise ValueError('Amount must be positive.')
        if amount > self._balance:
            raise ValueError('Amount exceeds available balance.')
        self._amount_bet = amount

    def is_valid_bet(self):
        """Checks if the current bet is valid.

        Returns:
            bol, True if the bet is valid, False otherwise.
        """
        if self._hand_bet not in ['punto', 'banco', 'tie'] or self._amount_bet <= 0:
            return False
        return True

    def win(self):
        """Perform the necessary actions upon a player win: adds the winnings
        to the balance according the bet and resets the bet.

        Raises:
            InvalidBet: If the player does not have a valid bet.
        """
        if self.is_valid_bet():
            if self._hand_bet == 'punto':
                self._balance += int(self._amount_bet * 1)
            elif self._hand_bet == 'banco':
                self._balance += int(self._amount_bet * 0.95)
            elif self._hand_bet == 'tie':
                self._balance += int(self._amount_bet * 8)
            self._hand_bet = None
            self._amount_bet = 0
        else:
            raise InvalidBet('Player does not have a valid bet')

    def lose(self):
        """Performs the necessary action upon a player lose: resets the bet.

        Raises:
            InvalidBet: If the player does not have a valid bet.
        """
        if self.is_valid_bet():
            self._balance -= self._amount_bet
            self._hand_bet = None
            self._amount_bet = 0
        else:
            raise InvalidBet('Player does not have a valid bet')

    def __repr__(self):
        """Return the representation string as if the object was
        called when creating a new instance with the current balance.
        """
        return f'Player({self._balance})'

    def __str__(self):
        """Return a string separated by new lines with the id, amount and bet
        of the player in case there is a valid one.
        """
        bet = f'Hand bet: {self._hand_bet}, Amount bet: {self._amount_bet}'
        no_bet = 'No bet'
        return f'Player: {self._pid}, Balance: {self._balance}, {bet if self.is_valid_bet() else no_bet}'

class Game:
    def __init__(self, num_decks=8):
        self._game_running = False
        self._players = []
        self._punto = []
        self._banco = []
        self.create_shoe(num_decks)

    @property
    def punto_value(self):
        return self._punto.value

    @property
    def punto_cards(self):
        return ', '.join([card.__str__() for card in self._punto.cards])

    @property
    def banco_value(self):
        return self._banco.value

    @property
    def banco_cards(self):
        return ', '.join([card.__str__() for card in self._banco.cards])

    @property
    def num_decks(self):
        return self._shoe.num_decks

    def create_shoe(self, num_decks):
        self._shoe = Shoe(num_decks)
        self._num_decks = num_decks

    def deal_hands(self):
        if self._game_running:
            raise GameError('Game is running')
        self._punto = Punto(self._shoe.draw_cards(2))
        self._banco = Banco(self._shoe.draw_cards(2))
        self._game_running = True

    def is_natural(self):
        if not self._game_running:
            raise GameError('Game is not running.')
        natural = self._punto.is_natural() or self._banco.is_natural()
        if natural:
            self._game_running = False
        return natural

    def draw_thirds(self):
        if not self._game_running:
            raise GameError('Game is not running.')
        if self.is_natural():
            raise GameError('Can\'t draw third cards when there is a natural.')
        third_draws = []
        if self._punto.draw_third():
            self._punto.add_cards(self._shoe.draw_cards(1))
            third_draws.append(['punto', self._punto.cards[2].__str__()])
            if self._banco.draw_third(self._punto.cards[2]):
                self._banco.add_cards(self._shoe.draw_cards(1))
                third_draws.append(['banco', self._banco.cards[2].__str__()])
        elif self._banco.draw_third():
            self._banco.add_cards(self._shoe.draw_cards(1))
            third_draws.append(['banco', self._banco.cards[2].__str__()])
        self._game_running = False
        return third_draws

    def game_result(self):
        if self._game_running:
            raise GameError('Game is running.')
        if self._punto.value > self._banco.value:
            return 'punto'
        elif self._punto.value < self._banco.value:
            return 'banco'
        else:
            return 'tie'

    def __repr__(self):
        return f'Game({self._shoe.num_decks})'

class Table(Game):
    def __init__(self, num_decks=8):
        self._bets_open = True
        Game.__init__(self, num_decks)

    @property
    def num_players(self):
        return len(self._players)

    @property
    def available_players(self):
        players = []
        for player in self._players:
            if player.balance > 0:
                players.append(self._players.index(player))
        return players

    @property
    def valid_bets(self):
        players = []
        for player_i in self.available_players:
            if self._players[player_i].is_valid_bet():
                players.append(player_i)
        return players

    def deal_hands(self):
        if not self._bets_open:
            raise GameError('There are some bets on table.')
        self._bets_open = False
        Game.deal_hands(self)

    def add_player(self, balance):
        self._players.append(Player(balance))

    def bet(self, player_i, hand_bet, amount_bet):
        if not self._bets_open:
            raise GameError('A player cannot make a bet after the hands are dealt.')
        self._players[player_i].hand_bet = hand_bet
        self._players[player_i].amount_bet = amount_bet

    def bet_result(self, player_i):
        if self._players[player_i].hand_bet == self.game_result():
            self._players[player_i].win()
            result = ('win', self._players[player_i].balance)
        else:
            self._players[player_i].lose()
            result = ('lose', self._players[player_i].balance)
        if not self.valid_bets:
            self._bets_open = True
        return result

    def __getitem__(self, player_i):
        return self._players[player_i].__str__()

    def __repr__(self):
        return f'Table({self._shoe.num_decks})'

class InvalidBet(Exception):
    pass

class GameError(Exception):
    pass


def show_status(player, banker):
    print(player)
    print(player.value)
    print(banker)
    print(banker.value)
    print()

def check_winner(player, banker):
    if player.value > banker.value:
        return 'Punto wins.'
    elif player.value < banker.value:
        return 'Banco wins.'
    else:
        return 'Tie.'

def main():
    shoe = Shoe(2)
    player = Punto(shoe.draw_cards(2))
    banker = Banco(shoe.draw_cards(2))

    show_status(player, banker)

    if player.is_natural() or banker.is_natural():
        print(f'{check_winner(player, banker)} Natural.')
    else:
        if player.draw_third():
            player.add_cards(shoe.draw_cards(1))
            if banker.draw_third(player.cards[2]):
                banker.add_cards(shoe.draw_cards(1))
        elif banker.draw_third():
            banker.add_cards(shoe.draw_cards(1))

        show_status(player, banker)
        print(check_winner(player, banker))

if __name__ == '__main__':
    main()
