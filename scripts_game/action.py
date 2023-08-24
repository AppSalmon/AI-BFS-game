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
BLUE = (0, 0, 255)



class Action:
    def __init__(self, game,  size, number_cell, barries):
        self.game = game
        self.point = 0 # Điểm người chơi
        self.live = 3 # Số mạng sống
        self.size = size # Grid_size
        self.NUMBER_CELL = number_cell
        self.barrier = barries
        self.food_type = randint(1, 10) # random đồ ăn

        self.food_1 = "../AI-BFS-game/data/images/food/coin.png"
        self.food_1 = pg.image.load(self.food_1)
        self.food_1 = pg.transform.scale(self.food_1, (self.size, self.size))

        self.heart = "../AI-BFS-game/data/images/food/heart.png"
        self.heart = pg.image.load(self.heart)
        self.heart = pg.transform.scale(self.heart, (self.size, self.size))

        self.cup_image = "../AI-BFS-game/data/images/food/cup.png"
        self.cup_image = pg.image.load(self.cup_image)
        self.cup_image = pg.transform.scale(self.cup_image, (500, 350))


    def rect(self, pos):
        return pg.Rect(pos[0], pos[1], 1, 1)

    def lost_life(self):
        self.live -= 1

    def check_collision(self, pos_player, pos_boss):
        """
        Check va chạm bot <=> player
        """
        self.collisions = False
        entity_rect_player = self.rect(tuple(pos_player))
        entity_rect_boss  = self.rect(tuple(pos_boss))
        if entity_rect_player.colliderect(entity_rect_boss):  # phat hien va cham
           self.collisions = True

        return self.collisions, self.live <= 0

    def gen_loc(self):
        """
        Random tọa độ

        """
        return [randint(1, self.NUMBER_CELL - 2), randint(1, self.NUMBER_CELL - 2)]

    def gen_apple(self):
        check_invalid = True
        while check_invalid:
            check_invalid = False
            self.apple = self.gen_loc() # trả về list
            for barri in self.barrier:
                x, y = barri
                if x == self.apple[0] and y == self.apple[1]:
                    check_invalid = True

    def check_point(self, pos_player, surf):
        """
        Cộng điểm người chơi và gen táo mới

        """
        if self.check_collision(pos_player, self.apple)[0] == True:
            if self.food_type <= 3:
                self.live += 1
            else:
                self.point +=1
            self.gen_apple()
            self.food_type = randint(1, 10)

    def render(self, surf, type, pos_player):
        font_big = pg.font.SysFont('sans', 50)
        font_small = pg.font.SysFont('sans', 20)

        if self.live > 0: # Vẽ vòng tròn bảo vệ khi mạng lớn hơn 0
            pg.draw.circle(surf, BLUE, (pos_player[0]*self.size+5, pos_player[1]*self.size+5), self.size + randint(0, 5), randint(1, 2))

        if type == 2:
            game_over_text = font_big.render("Game over, score: " + str(self.point), True, WHITE)  # Chữ, mượt, màu
            press_space_text = font_big.render("Press Space to Reset", True, WHITE)  # Chữ, mượt, màu
            surf.blit(game_over_text, (300, 150))
            surf.blit(press_space_text, (300, 200))
            surf.blit(self.cup_image, (230, 250))

        elif type == 3:
            # pg.draw.rect(surf, GREEN, (self.apple[0] * self.size,
            #                            self.apple[1] * self.size, self.size,
            #                            self.size))  # Tọa độ đỉnh, chiều ngang dọc

            if self.food_type <= 3:
                surf.blit(self.heart, (self.apple[0] * self.size,
                                       self.apple[1] * self.size))
            else:
                surf.blit(self.food_1, (self.apple[0] * self.size,
                                       self.apple[1] * self.size))
        else:
            score_text = font_big.render("Score: " + str(self.point), True, GREEN)
            surf.blit(score_text, (770, 10))

            score_text = font_big.render("Live: " + str(self.live), True, GREEN)
            surf.blit(score_text, (770, 69))

