import pygame
from time import sleep
from random import randint, sample
from math import sqrt


import sys
import pygame as pg #sdl to python
from scripts_game.entities import  PhysicsEntity
from scripts_game.utils import load_image, load_images
from scripts_game.tilemap import Tilemap
from scripts_game.search import BFS, DFS
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

# Load ảnh
background_green1 = "../AI-BFS-game/data/images/background/green1.png"
background_green1 = pygame.image.load(background_green1)
background_green1 = pygame.transform.scale(background_green1, (GRID_SIZE, GRID_SIZE))


background_water = "../AI-BFS-game/data/images/background/water.png"
background_water = pygame.image.load(background_water)
background_water = pygame.transform.scale(background_water, (GRID_SIZE, GRID_SIZE))

background_sand = "../AI-BFS-game/data/images/background/sand.png"
background_sand = pygame.image.load(background_sand)
background_sand = pygame.transform.scale(background_sand, (GRID_SIZE, GRID_SIZE))




def create_text(x, color, size): # Tạo chữ
	font = pygame.font.SysFont('sans', size)
	return font.render(x, True, color)


def distance(p1, p2): # Tính khoảng cách 2 điểm
	return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)




class Game:
	"""
	
	Toàn bộ về game

	"""
	def __init__(self):
		pygame.init()  #constructor
		pygame.display.set_caption('TTPN-Game')

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
 
		# List background
		self.list_background = [background_green1, background_sand, background_water]
		self.final_background = background_green1
		self.cnt_click_background = 0
		self.index_monster = ""
		self.end_game = False


		# Tạo đối tượng người chơi
		self.player = PhysicsEntity(self, 'player', (2, 9),(GRID_SIZE, GRID_SIZE))
		self.monster = PhysicsEntity(self, 'monster', (randint(0, NUMBER_CELL), randint(0, NUMBER_CELL)), (GRID_SIZE, GRID_SIZE))
		self.monster_size_add = 1
		self.direction = "."
		self.result1 = ""
		self.result2 = ""
		# self.monster = PhysicsEntity(self, monter_1, (randint(0, NUMBER_CELL), randint(0, NUMBER_CELL)), GRID_SIZE)


		self.tilemap = Tilemap(self, tile_size=GRID_SIZE, NUMBER_CELL = NUMBER_CELL)
		self.bfs_monster = BFS(self.tilemap.get_barries())


		self.move_x = [False, False]; # Bước đi tiếp theo của nhân vật (L, R)
		self.move_y = [False, False]; # 

		self.action = Action(self, GRID_SIZE, NUMBER_CELL, self.tilemap.get_barries())
		self.action.gen_apple()

		self.pos = [100, 100] # Để cho dui
		self.pausing = False # Check thắng thua

	def run(self):
		while True:
			# cnt += 1
			self.screen.fill(BLACK)  # fill toan bo backround ve mau nen

			# Vẽ lưới check code
			# for i in range(NUMBER_CELL):
			# 	pygame.draw.line(self.screen, WHITE, (0, i * GRID_SIZE),
			# 					 (PLAY_SIZE, i * GRID_SIZE))  # Màu, tọa độ đầu, tọa độ cuối
			# 	pygame.draw.line(self.screen, WHITE, (i * GRID_SIZE, 0),
			# 					 (i * GRID_SIZE, PLAY_SIZE))  # Màu, tọa độ đầu, tọa độ cuối

			# Vẽ khu vực chơi
			pygame.draw.line(self.screen, RED, (0, 0 * GRID_SIZE),
								(PLAY_SIZE, 0 * GRID_SIZE))  # Màu, tọa độ đầu, tọa độ cuối
			pygame.draw.line(self.screen, RED, (NUMBER_CELL * GRID_SIZE, 0),
								(NUMBER_CELL * GRID_SIZE, PLAY_SIZE))  # Màu, tọa độ đầu, tọa độ cuối
			
			# ========= Interface ============
			# Vẽ ô kc và warning
			pygame.draw.rect(self.screen, GREEN, (770, 150, 220, 100), 2)
			kc = round(distance(self.player.pos, self.monster.pos) * GRID_SIZE, 2)
			if kc > 200:
				self.screen.blit(create_text('K/c: ' + str(kc) + 'px', GREEN, 40), (777, 175))
			else:
				self.screen.blit(create_text('K/c: ' + str(kc) + 'px', RED, 40), (777, 175))
				self.screen.blit(create_text('Warning!', RED, 20), (790, 220))

			# Vẽ ô Monster size
			self.monster_size_add = self.monster.update_monster_size(0)
			self.screen.blit(create_text("Monster size", GREEN, 30), (770, 270))
			pygame.draw.rect(self.screen, GREEN, (770, 320, 50, 50), 2)
			pygame.draw.rect(self.screen, GREEN, (770+50, 320, 100, 50), 2)
			pygame.draw.rect(self.screen, GREEN, (770+150, 320, 50, 50), 2)
			self.screen.blit(create_text("<", GREEN, 40), (785, 320))
			self.screen.blit(create_text(">", GREEN, 40), (770+150+15, 320))
			self.screen.blit(create_text(str(self.monster_size_add), GREEN, 30), (850, 325))

			# Vẽ ô thay đổi monster
			self.screen.blit(create_text("Change monster", GREEN, 30), (770, 380))
			pygame.draw.rect(self.screen, GREEN, (770, 420, 100, 50), 2)
			pygame.draw.rect(self.screen, GREEN, (770+100, 420, 50, 50), 2)
			self.screen.blit(create_text(">", GREEN, 40), (770+115, 420))
			self.screen.blit(create_text(str(self.index_monster), GREEN, 40), (785, 425))

			# Vẽ ô thay đổi background
			self.screen.blit(create_text("Change background", GREEN, 30), (770, 480))
			pygame.draw.rect(self.screen, GREEN, (770, 520, 100, 50), 2)
			pygame.draw.rect(self.screen, GREEN, (770+100, 520, 50, 50), 2)
			self.screen.blit(create_text(">", GREEN, 40), (770+115, 520))
			

			# Viết tên của background
			if self.cnt_click_background % 3 == 0:
				self.screen.blit(create_text("Tree", GREEN, 40), (780, 520))
			elif self.cnt_click_background % 3 == 1:
				self.screen.blit(create_text("Sand", GREEN, 40), (780, 520))
			elif self.cnt_click_background % 3 == 2:
				self.screen.blit(create_text("Water", GREEN, 40), (780, 520))

			# Vẽ hướng đi
			pygame.draw.rect(self.screen, GREEN, (770, 600, 200, 130), 2)
			self.screen.blit(create_text(str(self.direction), RED, 100), (850, 600))
			
			# Lấy tọa độ chuột
			mouse_x, mouse_y = pygame.mouse.get_pos()
			# self.screen.blit(create_text(f'({mouse_x}, {mouse_y})', WHITE, 15), (mouse_x+15, mouse_y))

			# Vẽ các thành phần của bản đồ
			barrier = self.tilemap.get_barries()
			for i in range(0, NUMBER_CELL):
				for j in range(0, NUMBER_CELL):
					x, y = i, j
					check_invalid_background = False
					for bar in barrier:
						if x == bar[0] and y == bar[1]:
							check_invalid_background = True
							break
					if check_invalid_background == False:
						self.screen.blit(self.final_background, (x*GRID_SIZE, y*GRID_SIZE))

			# # Vẽ chướng ngại
			self.tilemap.render(self.screen)

			# # Vẽ player
			self.player.update(self.tilemap, (self.move_x[1] - self.move_x[0], self.move_y[1] - self.move_y[0]))
			# print(self.player.pos)
			self.player.render(self.screen)

			# vẽ táo
			self.action.render(self.screen, 3, self.player.pos)
			self.action.render(self.screen, 1, self.player.pos)

			# vẽ boss
			next_step = self.bfs_monster.trace(tuple(self.monster.pos), tuple(self.player.pos))

			self.monster.update(self.tilemap, (next_step[0] , next_step[1]))
			self.monster.render(self.screen)

			# Kiểm tra xem player va chạm monster nhưng player có còn mạng không
			check_die, check_end_game = self.action.check_collision(self.player.pos, self.monster.pos)
			if check_die == True and check_end_game == True:
				self.pausing = True
			elif check_die == True:
				self.action.lost_life()
				self.monster.pos = [randint(0, NUMBER_CELL), randint(0, NUMBER_CELL)]

			# Code cũ khi chưa có heart
			# self.pausing = self.action.check_collision(self.player.pos, self.monster.pos)
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
							self.end_game = False
					if event.key == pg.K_RIGHT:
						self.move_x[1] = True
						self.move_x[0] = False
						self.move_y[0] = False
						self.move_y[1] = False
						self.direction = ">"
					if event.key == pg.K_LEFT:
						self.move_x[1] = False
						self.move_x[0] = True
						self.move_y[0] = False
						self.move_y[1] = False
						self.direction = "<"
					if event.key == pg.K_UP:
						self.move_x[1] = False
						self.move_x[0] = False
						self.move_y[1] = False
						self.move_y[0] = True
						self.direction = "^"
					if event.key == pg.K_DOWN:
						self.move_x[1] = False
						self.move_x[0] = False
						self.move_y[0] = False
						self.move_y[1] = True
						self.direction = "v"
				# Lúc bấm chuột
				if event.type == pygame.MOUSEBUTTONDOWN:
					
					# Giảm monster size
					if 770 < mouse_x < 815 and 320 < mouse_y < 365:
						self.monster_size_add = self.monster.update_monster_size(-1)
						self.monster.update_monster_size_real_time()
					
					# Tăng monster size
					if 920 < mouse_x < 960 and 320 < mouse_y < 365:
						self.monster_size_add = self.monster.update_monster_size(1)
						self.monster.update_monster_size_real_time()
					
					# Thay đổi monster
					if 870 < mouse_x < 915 and 420  < mouse_y < 460:
						self.index_monster = self.monster.update_click_change_monster()

					# Thay đổi background
					if 870 < mouse_x < 915 and 520  < mouse_y < 560:
						self.cnt_click_background += 1
						self.final_background =  self.list_background[self.cnt_click_background % 3]
					


			# self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
			if self.pausing == True:
				self.screen.fill(BLACK)
				self.action.render(self.screen, 2, self.player.pos)
				
				if self.end_game == False:
					""" Bảng xếp hạng """
					numbers = []
					with open('ranking.txt', 'r') as file:
						for line in file:
							print(line)
							number = int(line.strip())
							numbers.append(number)
					print(numbers)
					numbers.append(self.action.point)
					numbers.sort(reverse=True)  # Sắp xếp từ lớn đến bé
					numbers_sort = numbers[:5]
					if self.action.point in numbers_sort:
						self.result1 = "Chuc mung ban da dat thu hang: " + str(numbers.index(self.action.point)+1)

					with open('ranking.txt', 'w') as file:
						for number in numbers_sort:
							file.write(str(number) + '\n')
					self.result2 = "BXH: " + str(numbers_sort)
				self.end_game = True

				self.screen.blit(create_text(self.result1, RED, 40), (250, 600))
				self.screen.blit(create_text(self.result2, RED, 40), (350, 650))


			pygame.display.update()
			self.clock.tick(60)

game = Game()
game.run()
