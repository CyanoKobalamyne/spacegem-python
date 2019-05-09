# General description of stuff

TL;DR: work on level2.py for now, but that may change soon.

Right now, the interval.py file has an independent working minigame for the interval thing, but the code is not refactored to work with a scene manager. This is OLD CODE. 

The level2.py file has interval minigame code which has been refactored to work with a scene manager and it has the scene manager as well. At some point soon, I will refactor this to move the minigame outside the main file and just import to keep things more modular.

# Aron: what you should do

For testing, you can change the `__init__ ` method of SceneManager to start with an instance of your scene class instead of TitleScene and just put your code directly in the level2.py file. You can look at the IntervalScene class for an example of how stuff is done.

# How to install and run

install python3
run `pip3 install pygame`
run `python3 interval.py`
