import datetime
import argparse
from rules import Game

def hand_values(hand):
    """Creates a list of strings with the values of a hand."""
    values = []
    for i in range(3):
        try:
            values.append(str(hand[i]))
        except IndexError:
            values.append('x')
    return values

def main():

    # Counters
    shoe_count = 0
    game_count = 0
    total_wins = {'banco': 0, 'punto': 0, 'tie': 0}

    # Argument parser
    parser = argparse.ArgumentParser(description='Simulates baccarat games to a text file.')
    parser.add_argument('-s', action='store', dest='shoes', default=10000,
                        type=int, help='number of shoes to be simulated, default 10000')
    parser.add_argument('-d', action='store', dest='decks', default=8,
                        type=int, help='number of decks per shoe, default 8')
    args = parser.parse_args()

    # Create game object
    sim = Game()
    sim.create_shoe(args.decks)

    # Set file name
    now = datetime.datetime.now()
    file_name = f'{args.decks}_{args.shoes}_{now.strftime("%d%m%y%H%M%S")}.txt'

    # Open file
    with open(file_name, 'w') as sim_file:

        # Run through num_shoes
        for i in range(args.shoes):
            shoe_wins = {'banco': 0, 'punto': 0, 'tie': 0}
            shoe_count += 1
            sim_file.write(f'\nShoe number {i + 1}\n\n')

            # While the shoe has more than 5 cards
            while sim.num_cards >= 6:
                result = []
                game_count += 1

                # Baccarat game
                sim.deal_hands()
                if not sim.is_natural():
                    sim.draw_thirds()
                game_result = sim.game_result()
                shoe_wins[game_result] += 1
                total_wins[game_result] += 1

                # Append to results list
                result.append(game_result.title()[0])
                result.append(str(sim.banco_value))
                result.append(str(sim.punto_value))
                result.extend(hand_values(sim.banco_values))
                result.extend(hand_values(sim.punto_values))
                sim_file.write(','.join(result) + '\n')

                # Progress
                progress = round((shoe_count / args.shoes) * 100, 1)
                print(f'Progress: {progress}%', end='\r')

            # Shoe results
            sim_file.write('\nShoe results:\n')
            for win in shoe_wins:
                sim_file.write(f'{win.title()}:\t{shoe_wins[win]}\n')
            sim.create_shoe(args.decks)

        # Total results
        sim_file.write('\nTotal results:\n')
        for win in total_wins:
            sim_file.write(f'{win.title()}:\t{total_wins[win]}\t\
({round((total_wins[win]/game_count) * 100, 4)}%)\n')

if __name__ == '__main__':
    main()
