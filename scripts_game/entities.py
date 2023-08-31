'''
xử lý các đối tượng vật lý
blit img
update position
handel collision
'''
import pygame as pg
from random import randint




class PhysicsEntity:
    
    def __init__(self, game, e_type, pos, size):
        self.game = game # Kế thừa class game
        self.type = e_type # Loại đối tượng
        self.pos = list(pos) # đảm bảo mỗi thực thể có một pos riêng
        self.size = size # Kích thước ô
        self.velocity = [0, 0] # thể hiện tốc độ thay đổi vị trí của thưc thể
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False} #check va cham
        self.zoom_monster = 10
    
        # self.monter_main_beauty = "../AI-BFS-game/data/images/monster/beauty.png"
        # self.monter_main_beauty = pg.image.load(self.monter_main_beauty)
        # self.monter_beauty = pg.transform.scale(self.monter_main_beauty, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.monter_main_bird = "../AI-BFS-game/data/images/monster/bird.png"
        self.monter_main_bird = pg.image.load(self.monter_main_bird)
        self.monter_bird = pg.transform.scale(self.monter_main_bird, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.monter_main_dat = "../AI-BFS-game/data/images/monster/dat.png"
        self.monter_main_dat = pg.image.load(self.monter_main_dat)
        self.monter_dat = pg.transform.scale(self.monter_main_dat, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.monter_main_girl1 = "../AI-BFS-game/data/images/monster/girl1.png"
        self.monter_main_girl1 = pg.image.load(self.monter_main_girl1)
        self.monter_girl1 = pg.transform.scale(self.monter_main_girl1, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.monter_main_girl2 = "../AI-BFS-game/data/images/monster/girl2.png"
        self.monter_main_girl2 = pg.image.load(self.monter_main_girl2)
        self.monter_girl2 = pg.transform.scale(self.monter_main_girl2, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.monter_main_luan = "../AI-BFS-game/data/images/monster/luan.png"
        self.monter_main_luan = pg.image.load(self.monter_main_luan)
        self.monter_luan = pg.transform.scale(self.monter_main_luan, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.monter_main_ma = "../AI-BFS-game/data/images/monster/ma.png"
        self.monter_main_ma = pg.image.load(self.monter_main_ma)
        self.monter_ma = pg.transform.scale(self.monter_main_ma, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.monter_main_ma2 = "../AI-BFS-game/data/images/monster/ma2.png"
        self.monter_main_ma2 = pg.image.load(self.monter_main_ma2)
        self.monter_ma2 = pg.transform.scale(self.monter_main_ma2, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.monter_main_nhan = "../AI-BFS-game/data/images/monster/nhan.png"
        self.monter_main_nhan = pg.image.load(self.monter_main_nhan)
        self.monter_nhan = pg.transform.scale(self.monter_main_nhan, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.monter_main_phu1 = "../AI-BFS-game/data/images/monster/phu1.png"
        self.monter_main_phu1 = pg.image.load(self.monter_main_phu1)
        self.monter_phu1 = pg.transform.scale(self.monter_main_phu1, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.monter_main_phu2 = "../AI-BFS-game/data/images/monster/phu2.png"
        self.monter_main_phu2 = pg.image.load(self.monter_main_phu2)
        self.monter_phu2 = pg.transform.scale(self.monter_main_phu2, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.monter_main_shark1 = "../AI-BFS-game/data/images/monster/shark1.png"
        self.monter_main_shark1 = pg.image.load(self.monter_main_shark1)
        self.monter_shark1 = pg.transform.scale(self.monter_main_shark1, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.monter_main_shark2 = "../AI-BFS-game/data/images/monster/shark2.png"
        self.monter_main_shark2 = pg.image.load(self.monter_main_shark2)
        self.monter_shark2 = pg.transform.scale(self.monter_main_shark2, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.monter_main_shark3 = "../AI-BFS-game/data/images/monster/shark3.png"
        self.monter_main_shark3 = pg.image.load(self.monter_main_shark3)
        self.monter_shark3 = pg.transform.scale(self.monter_main_shark3, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.monter_main_tai = "../AI-BFS-game/data/images/monster/tai.png"
        self.monter_main_tai = pg.image.load(self.monter_main_tai)
        self.monter_tai = pg.transform.scale(self.monter_main_tai, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.monter_main_tuanio = "../AI-BFS-game/data/images/monster/tuanio.png"
        self.monter_main_tuanio = pg.image.load(self.monter_main_tuanio)
        self.monter_tuanio = pg.transform.scale(self.monter_main_tuanio, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.monter_main_witch = "../AI-BFS-game/data/images/monster/witch.png"
        self.monter_main_witch = pg.image.load(self.monter_main_witch)
        self.monter_witch = pg.transform.scale(self.monter_main_witch, (size[0]+self.zoom_monster, size[1]+self.zoom_monster))

        self.list_monster = [self.monter_main_bird, self.monter_main_dat, self.monter_main_girl1, self.monter_main_girl2, self.monter_main_luan, self.monter_main_ma, self.monter_main_ma2, self.monter_main_nhan, self.monter_main_phu1, self.monter_main_phu2, self.monter_main_shark1, self.monter_main_shark2, self.monter_main_shark3, self.monter_main_tai, self.monter_main_tuanio, self.monter_main_witch]
        self.index_monster = randint(0, len(self.list_monster)-1)
        self.final_monster = self.list_monster[self.index_monster]
        self.final_monster_temp = self.list_monster[self.index_monster]


    def update_click_change_monster(self):
        temp = self.index_monster
        while temp == self.index_monster:
            self.index_monster = randint(0, len(self.list_monster)-1)

        self.final_monster = self.list_monster[self.index_monster]
        self.final_monster_temp = self.list_monster[self.index_monster]
        return self.index_monster
        

    # Update và trả về zoom monster
    def update_monster_size(self, update):
        if update == -1:
            self.zoom_monster = max(0, self.zoom_monster-10)
        elif update == 1:
            self.zoom_monster = min(10000, self.zoom_monster+10)
        return self.zoom_monster
    
    # Thay đổi kích thước trong thời gian chơi
    def update_monster_size_real_time(self):
        self.final_monster_temp = pg.transform.scale(self.final_monster, (self.size[0]+self.zoom_monster, self.size[1]+self.zoom_monster))



    def rect(self):
        return pg.Rect(self.pos[0], self.pos[1], 1, 1)

    def update(self, tilemap,  movement=(0, 0)): # Bản đồ vật cản, bước đi tiếp theo
        """
        Cập nhật vị trí các đối tượng

        """
        #self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        tmp_movement = (movement[0]+self.velocity[0], movement[1]+self.velocity[1]) # Cộng thêm vận tốc

        self.pos[0] += tmp_movement[0] # Thay đổi tọa độ x

        entity_rect = self.rect() # Dùng tạo hình chữ nhật check va chạm
        
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect): # phat hien va cham
                if tmp_movement[0] > 0:
                    self.collisions['right'] = True
                    entity_rect.right = rect.left
                if tmp_movement[0] < 0:
                    self.collisions['left'] = True
                    entity_rect.left = rect.right
                self.pos[0] = entity_rect.x # Lấy tọa x


        self.pos[1] += tmp_movement[1]
        entity_rect = self.rect()

        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):  # phat hien va cham
                if tmp_movement[1] > 0:
                    self.collisions['down'] = True
                    entity_rect.bottom = rect.top
                if tmp_movement[1] < 0:
                    self.collisions['up'] = True
                    entity_rect.top = rect.bottom
                self.pos[1] = entity_rect.y

        # self.velocity[1] = min(5, self.velocity[1] + 0.1)  # van toc roi

        # Không sài
        if self.collisions['up'] or self.collisions['down']:
            self.velocity[1] = 0

    def render(self, surf):
        # assert isinstance(self.game, object)
        # surf: bề mặt
        """
        In nhân vật

        """
        if self.type == 'player' :
            surf.blit(self.game.assets['player'], (self.pos[0] * self.size[0],
    									self.pos[1] *  self.size[0],))
        else:
            # pg.draw.rect(surf, (255, 0, 0), (self.pos[0] * self.size,
    		# 							self.pos[1] *  self.size,
            #                              self.size,  self.size))  # Tọa độ đỉnh, chiều ngang dọc
            self.final_monster_temp = pg.transform.scale(self.final_monster, (self.size[0]+self.zoom_monster, self.size[1]+self.zoom_monster))
            surf.blit(self.final_monster_temp, (self.pos[0] * self.size[0] - self.zoom_monster,
    									self.pos[1] *  self.size[0]- self.zoom_monster,))
