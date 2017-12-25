import time
from rules import Table

class Cli:
    """Command line interface of the game. Only interacts with Table object in
    order to receive input from the game logic.
    """
    def __init__(self):
        self._game = Table()
        self._quit = False
        self._options = {
            '1': self.status,
            '2': self.add_player,
            '3': self.place_bets,
            '4': self.deal_hands,
            '5': self.create_shoe,
            '0': self.quit
            }

    def run(self):
        """Main menu of the game."""
        print('Welcome to Baccarat Punto Banco')
        while not self._quit:
            print('''
Options:
1: Status
2: Add player
3: Place bets
4: Deal cards
5: Change shoe
0: Quit''')
            print()
            selection = input('Your selection: ')
            print()
            if selection and selection in self._options:
                self._options.get(self._options[selection]())
            else:
                print('Selection not recognized.')

    def status(self):
        """Prints the players status and other in game information."""
        print(f'Shoe with {self._game.num_decks} deck(s).')
        if self._game.available_players:
            print(f'{len(self._game.available_players)} player(s) in game:')
            for player in self._game.available_players:
                print(self._game[player])
        else:
            print('No players present on the table.')
        input('Press <enter> to continue...')

    def add_player(self):
        """Adds a new player to the game."""
        balance_input = input('Initial balance for the new player or <c> to cancel: ')
        if balance_input.lower() in ['c', 'cancel']:
            return
        try:
            # Try to convert to int but don't capture error
            try:
                balance_input = int(balance_input)
            except:
                pass
            self._game.add_player(balance_input)
            print()
            print(f'Player added with {balance_input} balance.')
            input('Press <enter> to continue...')
        except (ValueError, TypeError) as error:
            print()
            print(error)
            self.add_player()

    def place_bets(self):
        """Loops through out all the available player to place the individual
        bets.
        """
        if self._game.available_players:
            for player_i in self._game.available_players:
                self.bet(player_i)
            print('All bets placed.')
        else:
            print('No players to place bets.')
        input('Press <enter> to continue...')

    def bet(self, player_i):
        """Places an individual bet for player_i."""
        hands = {
            'p': 'punto',
            'punto': 'punto',
            'b': 'banco',
            'banco': 'banco',
            't': 'tie',
            'tie': 'tie'
            }
        action = 'Replacing' if player_i in self._game.valid_bets else 'New'
        print(f'{action} bet for Player {player_i + 1}. Press <s> to skip.')
        hand_input = input('The hand to bet. <p> punto, <b> banco, <t> tie: ')
        if hand_input.lower() in ['s', 'skip']:
            print()
            return
        amount_input = input('The amount to bet: ')
        if amount_input.lower() in ['s', 'skip']:
            print()
            return
        try:
            # Try to convert to int but don't capture error
            try:
                amount_input = int(amount_input)
            except:
                pass
            self._game.bet(player_i, hands.get(hand_input.lower()), amount_input)
            print()
        except (ValueError, TypeError, GameError) as error:
            print()
            print(error)
            self.bet(player_i)

    def deal_hands(self):
        """Deals both punto and banco hands and proceeds with the game itself.
        Check if there is a natural, draws possible thrird cards and apply the
        bet results.
        """

        def result_str():
            """Returns a string with the game result to be printed as output."""
            if self._game.game_result() != 'tie':
                return self._game.game_result().title() + ' win'
            else:
                return self._game.game_result().title()

        def print_hands():
            print(f'Punto hand: {self._game.punto_cards}.')
            punto_values = ', '.join([str(value) for value in self._game.punto_values])
            print(f'Cards values: {punto_values}.')
            print(f'Total hand value: value: {self._game.punto_value}.')
            time.sleep(0.5)
            print(f'Banco hand: {self._game.banco_cards}.')
            banco_values = ', '.join([str(value) for value in self._game.banco_values])
            print(f'Cards values: {banco_values}.')
            print(f'Total hand value: value: {self._game.banco_value}.')


        print('Dealing hands...')
        time.sleep(1)
        self._game.deal_hands()
        print_hands()
        print()
        if self._game.is_natural():
            time.sleep(0.5)
            print(f'{result_str()}. Natural.')
        else:
            print('Drawing third cards...')
            time.sleep(1)
            third_draws = self._game.draw_thirds()
            for third_draw in third_draws:
                print(f'{third_draw[0].title()} draw third card, {third_draw[1]}.')
                time.sleep(0.5)
            print()
            print_hands()
            time.sleep(0.5)
            print(f'{result_str()}.')
        print()
        input('Press <enter> to continue...')
        print()
        print('Checking bets...')
        time.sleep(1)
        if self._game.valid_bets:
            for player_i in self._game.valid_bets:
                bet_result = self._game.bet_result(player_i)
                print(f'Player {player_i + 1} {bet_result[0]}. Balance: {bet_result[1]}.')
                time.sleep(0.5)
        else:
            print('No bets no table.')
        if self._game.open_bets():
            print('Bets are open.')
        print()
        input('Press <enter> to continue...')

    def create_shoe(self):
        """Creates a new shoe. Replaces the previous one."""
        shoe_input = input('The number of decks for the new shoe or <c> to cancel: ')
        if shoe_input.lower() in ['c', 'cancel']:
            return
        try:
            # Try to convert to int but don't capture error
            try:
                shoe_input = int(shoe_input)
            except:
                pass
            self._game.create_shoe(shoe_input)
            print()
            print(f'A new shoe with {int(shoe_input)} deck(s) will be used on the game.')
            input('Press <enter> to continue...')
        except (ValueError, TypeError) as error:
            print()
            print(error)
            self.create_shoe()

    def quit(self):
        """Quits the game uppon confirmation from the user."""
        quit_input = input('Do you really wish to quit? <y/n>: ')
        if quit_input.lower() in ['y', 'yes']:
            self._quit = True
        elif quit_input.lower() in ['n', 'no']:
            return
        else:
            print('Invalid input.')
            self.quit()

if __name__ == '__main__':
    Cli().run()
