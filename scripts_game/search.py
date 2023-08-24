'''
tim duong di cua monster den player
dieu kien:
+ko ra khoi map
+ko dung vat can

'''

from collections import  deque


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
		X = [-1, 1, 0, 0]
		Y = [0, 0, -1, 1]
		queue = deque([(start, [])])
		visited = set()
		while queue:
			current, path = queue.popleft()
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