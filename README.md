# Baccarat
Baccarat game Punto Banco variant in python. Small first personal project.  
The game supports multiple players and tries to emulate a casino baccarat table.  
The simulation supports cli arguments and outputs a number simulated baccarat shoes to a text file.

### How to run
#### Baccarat game cli
Just run baccarat-cli.py on python.
```
python3 baccarat-cly.py
```
#### Baccarat simulation
Run baccarat-sim.py on python. The number of shoes to be simulated and the number of decks per shoe can be set with the optional ```-s``` and ```-d``` arguments respectively. The default number of shoes is 10000 with 8 decks each.
```
python3 baccarat-sim.py [-h] [-s SHOES] [-d DECKS]
```

### Prerequisites
* Python 3.6
