# Space Gem

_Space Gem_ is a game to teach the basics of music theory to elementary and middle school students. It uses "gems" as an abstraction of musical notes, to ease the cognitive burden associated with understanding modern standard musical notation.

This game was created as a final project for the MIT class 11.127/CMS.590: Design and Development of Games for Learning.

# Installation instructions

In order to run the game, you will need an up-to-date version of Python (at least 3.6). You can check your Python version by executing `python3 --version` in a terminal. If needed, you can find help with installing or updating Python [here](https://docs.python.org/3/using/index.html).

You will also need Pygame. It can be installed by running `pip3 install pygame` in a terminal.

You can launch the game with the command `python3 game.py`.

# Source code organization

- `game.py` has the main method that starts the game
- `setup.py` has general constants that can be adjusted to customize the look and feel of the game
- `utils.py` has general utility classes like `Scene`, `Vector`, `Button`, and `TextBox`
- `menus.py` has the machinery for managing scene transitions
- world 1: code is in `platformer.py`, level specifications are in `world1.py`
- world 2: code is in `spaceships.py` and `interval.py`, level specifications are in `levels` in pickled (binary) format and which can be changed by running `make-levels.py`
- `narratives.py` contains the intro text displayed at the beginning of the game, each world, and each level
