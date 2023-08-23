'''
Xử lý các kịch bản game
+ tính điểm
+ check loss
+ tăng độ khó
'''

import  pygame as pg
from random import randint, sample

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Action:
    def __init__(self, game,  size, number_cell):
        self.game = game
        self.point = 0
        self.size = size
        self.NUMBER_CELL = number_cell


    def rect(self, pos):
        return pg.Rect(pos[0], pos[1], 1, 1)

    def check_collision(self, pos_player, pos_boss):
        self.collisions = False
        entity_rect_player = self.rect(tuple(pos_player))
        entity_rect_boss  = self.rect(tuple(pos_boss))
        if entity_rect_player.colliderect(entity_rect_boss):  # phat hien va cham
           self.collisions = True

        return self.collisions

    def gen_loc(self):
        return [randint(0, self.NUMBER_CELL - 2), randint(0, self.NUMBER_CELL - 2)]

    def gen_apple(self):
        self.apple = self.gen_loc()

    def check_point(self, pos_player, surf):
        if self.check_collision(pos_player, self.apple) == True:
            self.point +=1
            self.gen_apple()

    def render(self, surf, type):
        font_big = pg.font.SysFont('sans', 50)
        font_small = pg.font.SysFont('sans', 20)
        if type == 2:
            game_over_text = font_big.render("Game over, score: " + str(self.point), True, WHITE)  # Chữ, mượt, màu
            press_space_text = font_big.render("Press Space to Reset", True, WHITE)  # Chữ, mượt, màu
            surf.blit(game_over_text, (90, 250))
            surf.blit(press_space_text, (90, 300))

        elif type == 3:
            pg.draw.rect(surf, GREEN, (self.apple[0] * self.size,
                                       self.apple[1] * self.size, self.size,
                                       self.size))  # Tọa độ đỉnh, chiều ngang dọc
        else:
            score_text = font_small.render("Score: " + str(self.point), True, WHITE)
            surf.blit(score_text, (5, 5))

