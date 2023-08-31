'''
tim duong di cua monster den player
dieu kien:
+ko ra khoi map
+ko dung vat can

'''

from collections import  deque
import time
from math import sqrt
from random import randint



class BFS:
	def __init__(self, barriesrs):
		self.barriesrs = barriesrs #danh sach vi tri vat can

	def is_valid_move(self, x, y):
		if x < 0 or y < 0:
			return False
		if (x, y) in self.barriesrs:
			return False
		return True

	def trace(self, start, target):
		start_time = time.time()
		X = [-1, 1, 0, 0]
		Y = [0, 0, -1, 1]
		queue = deque([(start, [])])
		visited = set()
		while queue:
			current, path = queue.popleft()
			x, y = current
			if current == target:

				end_time = time.time()
				# Tính thời gian chạy
				elapsed_time = end_time - start_time
				# print("Thời gian chạy:", elapsed_time, "giây")
				# self.screen.blit(create_text('Time run bfs: ' + str(elapsed_time), (255, 0, 0), 20), (790, 220))

				if not path :
					return (0, 0)
				return path[0]

			if current in visited:
				continue

			visited.add(current)


			for i in range(4):
				new_x = x+X[i]
				new_y = y+Y[i]
				if self.is_valid_move(new_x, new_y):
					queue.append(((new_x, new_y), path + [(X[i], Y[i])]))

		return None  # No path found

class DFS:
	def __init__(self, barriesrs):
		self.barriesrs = barriesrs #danh sach vi tri vat can

	def is_valid_move(self, x, y):
		if x < 0 or y < 0:
			return False
		if (x, y) in self.barriesrs:
			return False
		return True

	def trace(self, start, target):
		X = [-1, 1, 0, 0]
		Y = [0, 0, -1, 1]
		queue = deque([(start, [])])
		visited = set()
		while queue:
			current, path = queue.pop()
			x, y = current
			if current == target:
				if not path :
					return (0, 0)
				return path[0]

			if current in visited:
				continue

			visited.add(current)


			for i in range(4):
				new_x = x+X[i]
				new_y = y+Y[i]
				if self.is_valid_move(new_x, new_y):
					queue.append(((new_x, new_y), path + [(X[i], Y[i])]))

		return None  # No path found

def distance(p1, p2): # Tính khoảng cách 2 điểm
	return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
	
class H:
	def __init__(self, barriers):
		self.barriers = set(barriers) # Chuyển danh sách vật cản thành tập hợp
		self.max_depth = 1000

	def is_valid_move(self, x, y):
		if x < 0 or y < 0:
			return False
		if (x, y) in self.barriers:
			return False
		return True

	def trace(self, start, target):
		X = [-1, 1, 0, 0]
		Y = [0, 0, -1, 1]
		mi = 100000000
		id = 0
		for i in range(4):
			x_new = start[0] + X[i]
			y_new = start[1] + Y[i]
			if self.is_valid_move(x_new, y_new):
				dis = distance((x_new, y_new), target)
				if dis == 1:
					return False
				if dis <= mi:
					mi = dis
					id = i
		return (X[id],Y[id])