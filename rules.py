from cards import Card, Shoe
from hands import Punto, Banco
from players import Player

class Game:
    """Application of the rules of baccarat - punto banco variation. This class
    manages only the card handling and its results.

    Args:
        num_decks: int, number of decks of the initial shoe. Optional, default
            value 8.

    Attributes:
        punto_value: int, value of punto hand.
        punto_cards: str, cards of punto hand.
        banco_value: int, value of banco hand.
        banco_cards: str, cards of banco hand.
        num_decks: int, current number of decks in the shoe.
    """
    def __init__(self, num_decks=8):
        self._game_running = False
        self._players = []
        self._punto = None
        self._banco = None
        self.create_shoe(num_decks)

    @property
    def punto_value(self):
        """Returns value of punto hand.

        Raises:
            ValueError: If _punto is None.
        """
        if not self._punto:
            raise ValueError('No hands were dealt.')
        return self._punto.value

    @property
    def punto_values(self):
        """Returns the individual card values of punto hand.

        Raises:
            ValueError: If _punto is None.
        """
        if not self._punto:
            raise ValueError('No hands were dealt.')
        values = []
        for card in self._punto.cards:
            values.append(card.value)
        return values

    @property
    def punto_cards(self):
        """Returns cards of punto hand.

        Raises:
            ValueError: If _punto is None.
        """
        if not self._punto:
            raise ValueError('No hands were dealt.')
        return ', '.join([card.__str__() for card in self._punto.cards])

    @property
    def banco_value(self):
        """Returns value of banco hand.

        Raises:
            ValueError: If _banco is None.
        """
        if not self._banco:
            raise ValueError('No hands were dealt.')
        return self._banco.value

    @property
    def banco_values(self):
        """Returns the individual card values of banco hand.

        Raises:
            ValueError: If _punto is None.
        """
        if not self._banco:
            raise ValueError('No hands were dealt.')
        values = []
        for card in self._banco.cards:
            values.append(card.value)
        return values

    @property
    def banco_cards(self):
        """Returns cards of banco hand.

        Raises:
            ValueError: If _banco is None.
        """
        if not self._banco:
            raise ValueError('No hands were dealt.')
        return ', '.join([card.__str__() for card in self._banco.cards])

    @property
    def num_decks(self):
        """Returns initial number of decks of _shoe."""
        return self._shoe.num_decks

    @property
    def num_cards(self):
        """Returns current number of cards in shoe."""
        return self._shoe.num_cards

    def create_shoe(self, num_decks):
        """Creates an instance of Shoe with num_decks."""
        self._shoe = Shoe(num_decks)
        self._num_decks = num_decks

    def deal_hands(self):
        """Deals both hands. Creates a Punto and Banco instance and pops two
        cards from the Shoe instance. Sets the game as open.

        Raises:
           GameError: If a game is currently running.
        """
        if self._game_running:
            raise GameError('Game is running')
        self._punto = Punto(self._shoe.draw_cards(2))
        self._banco = Banco(self._shoe.draw_cards(2))
        self._game_running = True

    def is_natural(self):
        """Checks if there is an hand with a natural. If there is closes the
        game.

        Returns:
            bol, True if there is a natural, False otherwise.

        Raises:
            GameError: If there is no game running.
        """
        if not self._game_running:
            raise GameError('Game is not running.')
        natural = self._punto.is_natural() or self._banco.is_natural()
        if natural:
            self._game_running = False
        return natural

    def draw_thirds(self):
        """Applies the third card drawing rules to draw a possible third card
        for both hands. Closes the game.

        Returns: list with tuples, each tuple contains the hand and card that
            was drawn to which the third card rules were applied.

        Raises:
            GameError: If a game is not running or there is an hand with a natural.
        """
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
        """Checks was is the result of the game.

        Returns:
            str, with the winning hand or 'tie' in case is a tie.

        Raises:
            GameError: If the game is still running.
        """
        if self._game_running:
            raise GameError('Game is running.')
        if self._punto.value > self._banco.value:
            return 'punto'
        elif self._punto.value < self._banco.value:
            return 'banco'
        else:
            return 'tie'

    def __repr__(self):
        """Return the representation string as if the object was
        called when creating a new instance with the current number of decks.
        """
        return f'Game({self._shoe.num_decks})'

class Table(Game):
    """Table of a game of baccarat. Introduces the players and betting system.
    Sets the bets as open. Subclass of Game.

    Attributes:
        num_players: int, total number of players.
        available_players: list, with the indexes of the players that are still
            in game with a positive balance.
        valid_bets: list, with the indexes of the players that currently have a
            valid bet on the table.
    """
    def __init__(self, num_decks=8):
        self._bets_open = True
        Game.__init__(self, num_decks)

    @property
    def num_players(self):
        """Retuns the total number of players."""
        return len(self._players)

    @property
    def available_players(self):
        """Returns the list of indexes of the players with positive balance."""
        players = []
        for player in self._players:
            if player.balance > 0:
                players.append(self._players.index(player))
        return players

    @property
    def valid_bets(self):
        """Returns the list of players with valid bets on table."""
        players = []
        for player_i in self.available_players:
            if self._players[player_i].is_valid_bet():
                players.append(player_i)
        return players

    def deal_hands(self):
        """Deals both hands. Calls deal_hands from the superclass Game. Sets the
        bets as closed.
        """
        if not self._bets_open:
            raise GameError('There are some bets on table.')
        self._bets_open = False
        Game.deal_hands(self)

    def add_player(self, balance):
        """Add a new player to the table.

        Args:
            balance: int, the initial balance of the player.
        """
        self._players.append(Player(balance))

    def bet(self, player_i, hand_bet, amount_bet):
        """Place a bet.

        Args:
            player_i: int, index of the player that will make the bet.
            hand_bet: str, the hand to be bet. Can also be a tie.
            amount_bet: int, the amount to bet.

        Raises:
            GameError: If the bets are closed.
        """
        if not self._bets_open:
            raise GameError('A player cannot make a bet after the hands are dealt.')
        self._players[player_i].hand_bet = hand_bet
        self._players[player_i].amount_bet = amount_bet

    def bet_result(self, player_i):
        """Apply the result, win or loss, of a bet according to the result of a game.

        Args:
            player_i: int, the index of the player to apply the bet result.
        """
        if self._players[player_i].hand_bet == self.game_result():
            self._players[player_i].win()
            result = ('win', self._players[player_i].balance)
        else:
            self._players[player_i].lose()
            result = ('lose', self._players[player_i].balance)
        return result

    def open_bets(self):
        if not self.valid_bets:
            self._bets_open = True
        return self._bets_open

    def __getitem__(self, player_i):
        """Get the status of a player.

        Args:
            player_i: int, the index of the player to get the status.

        Returns:
            str, the status of the player.
        """
        return self._players[player_i].__str__()

class GameError(Exception):
    pass
