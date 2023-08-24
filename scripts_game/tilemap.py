'''
load img map
draw physic TILES
'''
import pygame as pg
import json
from random import randint

# List chứa hướng đi
NEIGHBOR_OFFSETS = [(-1, -1), (-1, 0), (-1, 1),
                    (1, -1), (1, 0), (1, 1),
                    (0, -1), (0, 0), (0, 1)]

# Loại vật cản
PHYSICS_TILES = {'grass', 'stone'}



# with open('C:/Users/Admin/Documents/Project/Phu_ga/AI-BFS-game/data/maps/0.json', 'r') as f:
#     map_data = json.load(f)

class Tilemap:
    def __init__(self, game, tile_size = 19, NUMBER_CELL = 10):
        self.game = game
        self.tile_size = tile_size # = Grid size
        self.tilemap = {} # Load tọa độ vật cản, loại vật cản, loại của loại vật cản
        self.offgrid_tiles = [] # Lưu trữ ô xung quanh
        self.number_cell = NUMBER_CELL

        # Vẽ vật cản
        for i in range(15):
            # self.tilemap[str(3+i)+';10'] = {'type': 'grass','variant': 1, 'pos': (3+i, 10)} # [tọa độ x, y chuỗi] = {loại, kiểu của loại, tọa độ x, y dạng số}
            self.tilemap[str(3+i)+';10'] = {'type': 'stone','variant': 1, 'pos': (3+i, 10)} # [tọa độ x, y chuỗi] = {loại, kiểu của loại, tọa độ x, y dạng số}
            self.tilemap['10;'+ str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5+i)} 

            # self.tilemap[str(30+i)+';30'] = {'type': 'grass','variant': 1, 'pos': (30+i, 30)}
            self.tilemap[str(30+i)+';30'] = {'type': 'stone','variant': 1, 'pos': (30+i, 30)}
            self.tilemap['35;'+ str(20 + i) ] = {'type': 'stone', 'variant': 1, 'pos': (35, 20+i)}
        
        for i in range(5):
            x = randint(5, 40)
            y = randint(5, 40)
            for j in range(randint(2, 4)):
                self.tilemap[str(x)+';'+ str(y+j)] = {'type': 'stone', 'variant': 1, 'pos': (x, y+j)}
        for i in range(5):
            x = randint(5, 40)
            y = randint(5, 40)
            for j in range(randint(2, 4)):
                self.tilemap[str(x+j)+';'+ str(y)] = {'type': 'stone', 'variant': 1, 'pos': (x+j, y)}


        # Vẽ tường khu vực chơi
        for i in range(1, self.number_cell-1):
            x = i
            y = 0
            self.tilemap[str(x)+';'+str(y)] = {'type': 'stone','variant': 1, 'pos': (x, y)} # [tọa độ x, y chuỗi] = {loại, kiểu của loại, tọa độ x, y dạng số}
            x = self.number_cell-1
            y = i
            self.tilemap[str(x)+';'+str(y)] = {'type': 'stone','variant': 1, 'pos': (x, y)}
            x = 0
            y = i
            self.tilemap[str(x)+';'+str(y)] = {'type': 'stone','variant': 1, 'pos': (x, y)}
            x = i
            y = self.number_cell-1
            self.tilemap[str(x)+';'+str(y)] = {'type': 'stone','variant': 1, 'pos': (x, y)}
        
        self.tilemap[str(0)+';'+str(0)] = {'type': 'stone','variant': 1, 'pos': (0, 0)}
        self.tilemap[str(self.number_cell-1)+';'+str(self.number_cell-1)] = {'type': 'stone','variant': 1, 'pos': (self.number_cell-1, self.number_cell-1)}
        self.tilemap[str(0)+';'+str(self.number_cell-1)] = {'type': 'stone','variant': 1, 'pos': (0, self.number_cell-1)}
        self.tilemap[str(self.number_cell-1)+';'+str(0)] = {'type': 'stone','variant': 1, 'pos': (self.number_cell-1, 0)}

        #     self.tilemap[str(30+i)+';30'] = {'type': 'stone','variant': 1, 'pos': (30+i, 30)}
        #     self.tilemap['35;'+ str(20 + i) ] = {'type': 'stone', 'variant': 1, 'pos': (35, 20+i)}
            

    def get_barries(self):
        '''
        Lấy tọa độ vật cản -> để một lát nữa để search

        return pos: stone, grasss
        '''

        barries = [] # Tọa độ vật cản
        for tile in self.tilemap.values():
            if tile['type'] in PHYSICS_TILES:
                barries.append(tile['pos'])
        return barries

    def tiles_around(self, pos):
        """
        Lấy tọa độ những ô xung quanh để check xem có phải vật cản

        """
        tiles = [] # Tọa độ vật cản
        tile_loc = (int(pos[0]), int(pos[1])) # Vô nghĩa
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])

        return tiles # Chứa tọa độ vật cản xung quanh

    def physics_rects_around(self, pos):
        """
        Vẽ hình CN xung quanh để check va chạm
        """
        rects = [] # Chứa hình vẽ của HCN
        for tile in self.tiles_around(pos):
            if tile['type']  in PHYSICS_TILES:
                rects.append(pg.Rect(tile['pos'][0], tile['pos'][1],
                                    1, 1)) # tao cac rect bao quanh thuc the de xac dinh physical
        return rects

    def render(self, surf):
        # Chưa xài
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])

        # Vẽ vật cản
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0]*self.tile_size,
                                                                        tile['pos'][1]*self.tile_size)) # (đường dẫn của ảnh, x*grid_size, y*...)
