'''
xử lý các đối tượng vật lý
blit img
update position
handel collision
'''
import pygame as pg


class PhysicsEntity:
    
    def __init__(self, game, e_type, pos, size):
        self.game = game # Kế thừa class game
        self.type = e_type # Loại đối tượng
        self.pos = list(pos) # đảm bảo mỗi thực thể có một pos riêng
        self.size = size # Kích thước ô
        self.velocity = [0, 0] # thể hiện tốc độ thay đổi vị trí của thưc thể
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False} #check va cham

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
            pg.draw.rect(surf, (255, 0, 0), (self.pos[0] * self.size,
    									self.pos[1] *  self.size,
                                         self.size,  self.size))  # Tọa độ đỉnh, chiều ngang dọc

print("Phú code bug rồi")