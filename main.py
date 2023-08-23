import pygame
from time import sleep
from random import randint, sample


import sys
import pygame as pg #sdl to python
from scripts_game.entities import  PhysicsEntity
from scripts_game.utils import load_image, load_images
from scripts_game.tilemap import Tilemap
from scripts_game.search import BFS
from scripts_game.action import  Action
# from scripts_game.find_away import *




GRID_SIZE = 15 
PLAY_SIZE = 750
NUMBER_CELL = PLAY_SIZE//GRID_SIZE

running = True
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


# font_small = pg.SysFont('sans', 20)




# font_small = pygame.font.SysFont('sans', 20)
# font_big = pygame.font.SysFont('sans', 50)



class Game:
	"""
	
	Toàn bộ về game

	"""
	def __init__(self):
		pygame.init()  #constructor
		pygame.display.set_caption('X')

		self.screen = pygame.display.set_mode((1000, 750))  # set display game (weight, height)
		self.clock = pygame.time.Clock()


		# Khai báo tài nguyên game
		self.assets = {
			'decor': load_images('tiles/decor'),
			'grass': load_images('tiles/grass'),
			'large_decor': load_images('tiles/large_decor'),
			'stone': load_images('tiles/stone'),
			'player': load_image('entities/player.png'),
			'monster': "1"
		}

		# Tạo đối tượng người chơi
		self.player = PhysicsEntity(self, 'player', (0, 9),(GRID_SIZE, GRID_SIZE))
		self.monster = PhysicsEntity(self, 'monster', (randint(0, NUMBER_CELL), randint(0, NUMBER_CELL)), GRID_SIZE)

		self.tilemap = Tilemap(self, tile_size=GRID_SIZE)
		self.bfs_monster = BFS(self.tilemap.get_barries())


		self.move_x = [False, False]; # Bước đi tiếp theo của nhân vật (L, R)
		self.move_y = [False, False]; # 

		self.action = Action(self, GRID_SIZE, NUMBER_CELL)
		self.action.gen_apple()

		self.pos = [100, 100] # Để cho dui
		self.pausing = False # Check thắng thua

	def run(self):
		while True:
			# cnt += 1
			self.screen.fill(BLACK)  # fill toan bo backround ve mau nen

			# Vẽ lưới
			# for i in range(NUMBER_CELL):
			# 	pygame.draw.line(self.screen, WHITE, (0, i * GRID_SIZE),
			# 					 (PLAY_SIZE, i * GRID_SIZE))  # Màu, tọa độ đầu, tọa độ cuối
			# 	pygame.draw.line(self.screen, WHITE, (i * GRID_SIZE, 0),
			# 					 (i * GRID_SIZE, PLAY_SIZE))  # Màu, tọa độ đầu, tọa độ cuối

			# Vẽ các thành phần của bản đồ từ dữ liệu JSON
			# for obj in map_data['objects']:
			# 	pos = obj['position']
			# 	color = obj.get('color', (255, 255, 255))
			# 	size = obj.get('size', (20, 20))
			# 	pygame.draw.rect(screen, color, pygame.Rect(pos[0], pos[1], size[0], size[1]))

			# # Vẽ chướng ngại
			self.tilemap.render(self.screen)

			# # Vẽ player
			self.player.update(self.tilemap, (self.move_x[1] - self.move_x[0], self.move_y[1] - self.move_y[0]))
			# print(self.player.pos)
			self.player.render(self.screen)

			# vẽ táo
			self.action.render(self.screen, 3)
			self.action.render(self.screen, 1)
			#vẽ boss
			next_step = self.bfs_monster.trace(tuple(self.monster.pos), tuple(self.player.pos))

			self.monster.update(self.tilemap, (next_step[0] , next_step[1]))
			self.monster.render(self.screen)

			self.pausing = self.action.check_collision(self.player.pos, self.monster.pos)
			self.action.check_point(self.player.pos, self.screen)

			# self.act

			sleep(0.1)

			for event in pg.event.get():  # bat su kien, neu khong bat su kien window se nghi chuong trinh ko phan hoi.
				if event.type == pg.QUIT:  # bat su kien exit
					pg.quit()
					sys.exit()
				elif event.type == pg.KEYDOWN:
					if self.pausing == True:
						if event.key == pg.K_SPACE:
							self.__init__()
							self.run()
					if event.key == pg.K_RIGHT:
						self.move_x[1] = True
						self.move_x[0] = False
						self.move_y[0] = False
						self.move_y[1] = False
					if event.key == pg.K_LEFT:
						self.move_x[1] = False
						self.move_x[0] = True
						self.move_y[0] = False
						self.move_y[1] = False
					if event.key == pg.K_UP:
						self.move_x[1] = False
						self.move_x[0] = False
						self.move_y[1] = False
						self.move_y[0] = True
					if event.key == pg.K_DOWN:
						self.move_x[1] = False
						self.move_x[0] = False
						self.move_y[0] = False
						self.move_y[1] = True

			# self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
			if self.pausing == True:
				self.screen.fill(BLACK)
				self.action.render(self.screen, 2)

			pygame.display.update()
			self.clock.tick(60)

game = Game()
game.run()
