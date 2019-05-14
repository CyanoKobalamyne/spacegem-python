"""Level definitions for World 1."""


class Level_1:
    # Player definition: (x, y)
    player = (1, 4)
    # Platform definition: (x, y, width)
    platforms = [
        (0, 5, 3),
        (5, 5.5, 3),
        (10, 5, 3),
        (10, 3, 3),
        (15, 4.5, 3),
        (15, 2, 3),
        (20, 2.5, 3),
        (21, 4.5, 3),
    ]
    # Gem definition: (x, y, note, winner)
    gems = [
        (22, 3.5, 0, True),
    ]


class Level_2:
    player = (1, 4)
    platforms = [
        (0, 5, 3),
        (5, 5.5, 3),
        (5, 3, 3),
        (10, 5, 3),
        (15, 4.5, 3),
        (15, 2, 3),
        (20, 3, 3),
    ]
    gems = [
        (6, 2, 6, False),
        (21, 2, 4, True),
    ]
