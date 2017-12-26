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
game_count = 0
total_wins = {'banco': 0, 'punto': 0, 'tie': 0}

sim = Game()
sim.create_shoe(num_decks)

for i in range(10000):
    print(f'\nShoe number {i + 1}\n')
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
        print(','.join(result))
    print()
    print('Shoe results:')
    for win in shoe_wins:
        print(f'{win.title()}:\t{shoe_wins[win]}')
    sim.create_shoe(num_decks)
print()
print('Total results:')
for win in total_wins:
    print(f'{win.title()}:\t{total_wins[win]}', end = '\t')
    print(f'({round((total_wins[win]/game_count) * 100, 4)}%)')
