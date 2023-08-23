'''
load img map
draw physic TILES
'''
import pygame as pg
#
NEIGHBOR_OFFSETS = [(-1, -1), (-1, 0), (-1, 1),
                    (1, -1), (1, 0), (1, 1),
                    (0, -1), (0, 0), (0, 1)]

PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size = 19):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(15):
            self.tilemap[str(3+i)+';10'] = {'type': 'grass','variant': 1, 'pos': (3+i, 10)}
            self.tilemap['10;'+ str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5+i)}
            self.tilemap[str(30+i)+';30'] = {'type': 'grass','variant': 1, 'pos': (30+i, 30)}
            self.tilemap['35;'+ str(20 + i) ] = {'type': 'stone', 'variant': 1, 'pos': (35, 20+i)}

    def get_barries(self):
        '''
        return pos: stone, grasss
        '''
        barries = []
        for tile in self.tilemap.values():
            if tile['type'] in PHYSICS_TILES:
                barries.append(tile['pos'])
        return barries

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0]), int(pos[1]))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])

        return tiles

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type']  in PHYSICS_TILES:
                rects.append(pg.Rect(tile['pos'][0], tile['pos'][1],
                                    1, 1)) # tao cac rect bao quanh thuc the de xac dinh physical
        return rects

    def render(self, surf):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0]*self.tile_size,
                                                                        tile['pos'][1]*self.tile_size))

