"""World and level definitions."""
from setup import GameSettings as GS
from setup import PlatformerSettings as PS


class World_1:
    class Level_1:
        # Player definition: (x, y)
        player = (3 * PS.BLOB_SIZE,
                  GS.SCREEN_HEIGHT / PS.PPU - 2 * PS.BLOB_SIZE)
        # Platform definition: (x, y, width, height)
        platforms = [
            (0, GS.SCREEN_HEIGHT / PS.PPU - PS.PLATFORM_HEIGHT,
             GS.SCREEN_WIDTH / PS.PPU / 2, PS.PLATFORM_HEIGHT),
            (GS.SCREEN_WIDTH / PS.PPU / 2 + PS.BLOB_SIZE * 1.5,
             GS.SCREEN_HEIGHT / PS.PPU - PS.PLATFORM_HEIGHT,
             GS.SCREEN_WIDTH / PS.PPU / 2, PS.PLATFORM_HEIGHT),
        ]
        # Gem definition: (x, y, note, winner)
        gems = [
            (0, GS.SCREEN_HEIGHT / PS.PPU - 2 * PS.BLOB_SIZE, 2, False),
            (GS.SCREEN_WIDTH / PS.PPU - 2 * PS.BLOB_SIZE,
             GS.SCREEN_HEIGHT / PS.PPU - 2 * PS.BLOB_SIZE,
             0, True),
        ]
