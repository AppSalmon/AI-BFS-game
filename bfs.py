import pygame
from time import sleep
from random import randint, sample
from collections import deque



pygame.init()
screen = pygame.display.set_mode((1000, 750))
pygame.display.set_caption('X')


GRID_SIZE = 15
PLAY_SIZE = 750
NUMBER_CELL = PLAY_SIZE//GRID_SIZE+1

running = True
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)



font_small = pygame.font.SysFont('sans', 20)
font_big = pygame.font.SysFont('sans', 50)

# Load ảnh
image_phu_ran = "zyro-image.png"
image_ran = pygame.image.load(image_phu_ran)
image_ran = pygame.transform.scale(image_ran, (GRID_SIZE+20, GRID_SIZE+20))

clock = pygame.time.Clock()

barriers = []
# barriers = [[2, 2], [3, 3], [4, 4]] # Chướng ngại vật

start_x = 2
end_x = 50
num_barriers = 10  # Số lượng chướng ngại vật

x_values = sample(range(start_x, end_x + 1), num_barriers)

for x in x_values:
	y = x  # Giả sử tọa độ y tương ứng với x trên đường thẳng cong
	barriers.append([x, y])

snake = [0, 9] # Tọa độ con quái vật x, y
snake_old = [0, 9]
monster = [randint(0, NUMBER_CELL), randint(0, NUMBER_CELL)]
shortest_path = []


direction = "right" # Hướng di chuyển của con rắn
directions_monster = [(0, 1), (0, -1), (1, 0), (-1, 0)]
apple = [randint(0, NUMBER_CELL-2), randint(0, NUMBER_CELL-2)] # Đồ ăn
score = 0
pausing = False # Chương trình có chạy không

def is_valid_move(x, y, barriers):
	if x < 0 or y < 0:
		return False
	for barrier in barriers:
		if x == barrier[0] and y == barrier[1]:
			return False
	return True

def bfs(start, target, barriers):
	queue = deque([(start, [])])
	visited = set()

	while queue:
		current, path = queue.popleft()
		x, y = current

		if current == target:
			return path

		if current in visited:
			continue

		visited.add(current)

		# Generate possible next moves: up, down, left, right
		# moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
		moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
		 (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)]


		for move in moves:
			new_x, new_y = move
			if is_valid_move(new_x, new_y, barriers):
				queue.append((move, path + [move]))

	return None  # No path found

cnt = 0
while running:
	cnt += 1		
	clock.tick(60) # Tốc độ khung hình mỗi giây
	screen.fill(BLACK) # Background xanh lá

	# Vẽ lưới
	# for i in range(NUMBER_CELL):
	# 	pygame.draw.line(screen, WHITE, (0, i*GRID_SIZE), (PLAY_SIZE, i*GRID_SIZE)) # Màu, tọa độ đầu, tọa độ cuối 
	# 	pygame.draw.line(screen, WHITE, (i*GRID_SIZE, 0), (i*GRID_SIZE, PLAY_SIZE)) # Màu, tọa độ đầu, tọa độ cuối 

	# Vẽ rắn
	screen.blit(image_ran, (snake[0]*GRID_SIZE-10, snake[1]*GRID_SIZE-10))
	# pygame.draw.rect(screen, GREEN, (snake[0]*GRID_SIZE, snake[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE)) # Tọa độ đỉnh, chiều ngang dọc
	
	# Vẽ táo
	pygame.draw.rect(screen, GREEN, (apple[0]*GRID_SIZE, apple[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE)) # Tọa độ đỉnh, chiều ngang dọc

	# Vẽ chướng ngại
	for barrier in barriers:
		pygame.draw.rect(screen, WHITE, (barrier[0]*GRID_SIZE, barrier[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE)) # Tọa độ đỉnh, chiều ngang dọc

	# Ăn táo và tính điểm
	if snake[0] == apple[0] and snake[1] == apple[1]:
		score += 1
		# Random thức ăn mới và không nằm trên con rắn
		while True:
			apple = [randint(0, NUMBER_CELL-2), randint(0, NUMBER_CELL-2)] # Đồ ăn
			error = False
			if snake[0] == apple[0] and snake[1] == apple[1]:
				error = True
			if error == False:
				break

	# Kiểm tra xem có tông tường không
	if snake[0] < 0 or snake[0] > NUMBER_CELL or snake[1] < 0 or snake[1] > NUMBER_CELL:
		pausing = True
	

	# In điểm
	score_text = font_small.render("Score: " + str(score), True, WHITE)
	screen.blit(score_text, (5, 5))

	# Di chuyển của BFS
	directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]



	# Tìm đường đi từ con rắn đến quả táo

	shortest_path = bfs(tuple(monster), tuple(snake_old), barriers)
	if len(shortest_path) > 0:
		monster = shortest_path[0]
	# print("Shortest path:", shortest_path)

	# Vẽ monster
	pygame.draw.rect(screen, RED, (monster[0]*GRID_SIZE, monster[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE)) # Tọa độ đỉnh, chiều ngang dọc

	# Di chuyển của rắn
	if pausing == False: # Nếu rắn vẫn còn sống
		if direction == "right":
			snake[0]+=1
		if direction == "left":
			snake[0]-=1
		if direction == "up":
			snake[1]-=1
		if direction == "down":
			snake[1]+=1

	if cnt % 10 == 0:
		x_old = snake[0]
		y_old = snake[1]
		snake_old = [x_old, y_old]

	if pausing == True:
		game_over_text = font_big.render("Game over, score: " + str(score), True, WHITE) # Chữ, mượt, màu
		press_space_text = font_big.render("Press Space to Reset", True, WHITE) # Chữ, mượt, màu
		screen.blit(game_over_text, (90, 250))
		screen.blit(press_space_text, (90, 300))
		
	sleep(0.1)
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # Tắt chương trình
			running = False
			pygame.quit()
		if event.type == pygame.KEYDOWN: # Khi bấm nút trên bàn phím
			if event.key == pygame.K_UP: # Khi bấm nút lên
				direction = "up"
			if event.key == pygame.K_DOWN: # Khi bấm nút xuống
				direction = "down"
			if event.key == pygame.K_LEFT: # Khi bấm nút trái
				direction = "left"
			if event.key == pygame.K_RIGHT: # Khi bấm nút phải
				direction = "right"
			# if event.key == pygame.K_SPACE:
			# 	snake = [0, 9] # Tọa độ con rắn x, y từ đuôi đến đầu
			# 	direction = "right" # Hướng di chuyển của con rắn
			# 	apple = [randint(0, NUMBER_CELL), randint(0, NUMBER_CELL)] # Đồ ăn
			# 	score = 0
			# 	pausing = False # Chương trình có chạy không

	pygame.display.flip()

pygame.quit()