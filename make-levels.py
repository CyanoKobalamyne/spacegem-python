import pickle

levels = []

levels.append([{"x": 700, "y": 300, "signals": [[0,0],[0,1],[0,2]]}])

pickle.dump(levels, open("levels", "wb"))
