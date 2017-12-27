import datetime
from rules import Game

def hand_values(hand):
    values = []
    for i in range(3):
        try:
            values.append(str(hand[i]))
        except IndexError:
            values.append('x')
    return values

num_decks = 8
num_shoes = 1000
shoe_count = 0
game_count = 0
total_wins = {'banco': 0, 'punto': 0, 'tie': 0}

sim = Game()
sim.create_shoe(num_decks)

now = datetime.datetime.now()
file_name = f'{num_decks}_{num_shoes}_{now.strftime("%d%m%y%H%M%S")}.txt'

prog_full = '**********'
prog_empty = '----------'

with open(file_name, 'w') as sim_file:

    print(' Generating:')
    for i in range(num_shoes):
        shoe_count += 1
        sim_file.write(f'\nShoe number {i + 1}\n\n')
        shoe_wins = {'banco': 0, 'punto': 0, 'tie': 0}

        while sim.num_cards >= 6:
            result = []
            game_count += 1
            sim.deal_hands()
            if not sim.is_natural():
                sim.draw_thirds()
            game_result = sim.game_result()
            shoe_wins[game_result] += 1
            total_wins[game_result] += 1
            result.append(game_result.title()[0])
            result.append(str(sim.banco_value))
            result.append(str(sim.punto_value))
            result.extend(hand_values(sim.banco_values))
            result.extend(hand_values(sim.punto_values))
            sim_file.write(','.join(result) + '\n')
            progress = int((shoe_count / num_shoes) * 10)
            print(f' [{prog_full[:progress] + prog_empty[progress:]}]', end='\r')

        sim_file.write('\nShoe results:\n')
        for win in shoe_wins:
            sim_file.write(f'{win.title()}:\t{shoe_wins[win]}\n')
        sim.create_shoe(num_decks)

    sim_file.write('\nTotal results:\n')
    for win in total_wins:
        sim_file.write(f'{win.title()}:\t{total_wins[win]}\t\
({round((total_wins[win]/game_count) * 100, 4)}%)\n')
print(f' Complete. Written to {file_name}')
