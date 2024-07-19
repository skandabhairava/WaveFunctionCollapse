#!/usr/bin/env python3
import pygame, random
from pygame.surface import Surface

pygame.init()
WIDTH = 25
SIZE = (WIDTH, 11*WIDTH//16) #WIDTH HEIGHT of aspect ratio 16:11
print(SIZE)
print("\n\n")
window = pygame.display.set_mode((SIZE[0]*32, SIZE[1]*32))
pygame.display.set_caption("Wave Function Collapse")
clock = pygame.time.Clock()
running = True

class Tile:
    def __init__(self, name: str, texture: Surface, rules: dict[str, int]):
        self.name: str = name
        self.texture: Surface = texture
        self.rules: dict[str, int] = rules

TYPES_TILES: dict[str, Tile] = {
    "GRASS": Tile("GRASS", pygame.image.load("textures/grass.png"),
                  {"GRASS": 90, "SAND": 5, "WATER": 0}
                  ),
    "SAND": Tile("Sand", pygame.image.load("textures/sand.png"),
                 {"SAND": 90, "WATER": 40, "GRASS": 8}
                 ),
    "WATER": Tile("Water", pygame.image.load("textures/water.png"),
                 {"WATER": 90, "SAND": 5, "GRASS": 0}
                 )
}

TILES: list[list[None|str]] = [[None for y in range(SIZE[0])] for x in range(SIZE[1])]
QUEUE = []
DONE_MAIN = 0

def propagate2D(coords: tuple, arr: list[list]) -> tuple:
    x, y = coords[0], coords[1]
    top, left, right, bottom, top_left, top_right, bottom_left, bottom_right = None, None, None, None, None, None, None, None
    if y > 0: top = (x, y - 1)
    if y < len(arr)-1: bottom = (x, y + 1)
    if x > 0: left = (x - 1, y)
    if x < len(arr[0])-1: right = (x + 1, y)

    if y > 0 and x > 0: top_left = (x - 1, y - 1)
    if y > 0 and x < len(arr[0])-1: top_right = (x + 1, y - 1)
    if y < len(arr)-1 and x > 0: bottom_left = (x - 1, y + 1)
    if y < len(arr)-1 and x < len(arr[0])-1: bottom_right = (x + 1, y + 1)

    return (top, right, bottom, left, top_left, top_right, bottom_left, bottom_right)

QUEUE.append((random.randint(0, len(TILES[0])-1), random.randint(0, len(TILES)-1)))
#QUEUE.append((24, 2))
TILES[QUEUE[0][1]][QUEUE[0][0]] = "GRASS"
DONE_MAIN += 1
#24, 2

lock = False

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if lock:
        continue

    if DONE_MAIN >= SIZE[0] * SIZE[1]:
        #print("DONE!", DONE_MAIN)
        continue

    ############################################################################
    target_coords = propagate2D(QUEUE[0], TILES)

    current_coord = QUEUE.pop(0)
    #print(current_coord)
    #if TILES[current_coord[1]][current_coord[0]]

    #TILES[current_coord[1]][current_coord[0]] = random.choices()

    for i in target_coords:
        if (i is not None) and (TILES[i[1]][i[0]]) is None:
            choices = {}
            secondary_targets = propagate2D(i, TILES)
            for j in secondary_targets:
                if (j is not None) and (TILES[j[1]][j[0]]) is not None:
                    secondary_tile = TYPES_TILES[TILES[j[1]][j[0]]]
                    #print(secondary_tile.name)
                    for key, val in secondary_tile.rules.items():
                        if key in choices:
                            choices[key] = min(choices[key], val)
                            continue

                        choices[key] = val
            TILES[i[1]][i[0]] = random.choices(tuple(choices.keys()), tuple(choices.values()))[0]  # type: ignore
            #TILES[i[1]][i[0]] = "GRASS"
            DONE_MAIN += 1
            QUEUE.append(i)
    ############################################################################ 

    window.fill((255, 255, 255))
    for i, rows in enumerate(TILES):
        for j, col in enumerate(rows):
            match col:
                case None:
                    #draw white square
                    window.fill((255, 255, 255), (j*32, i*32, 32, 32))
                case tile_name:
                    if tile_name not in TYPES_TILES:
                        window.fill((0, 0, 0), (j*32, i*32, 32, 32))
                        continue

                    tile = TYPES_TILES[tile_name.upper()]
                    window.blit(tile.texture, (j*32, i*32))

    pygame.display.update()