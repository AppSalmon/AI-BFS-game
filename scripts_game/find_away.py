import copy


class Queue:
    def __init__(self):
        self.list = []

    def push(self, item):
        self.list.insert(0, item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0

def check(x, y):
    return x>=0 and x<=200 and y>=0 and y <=200

def BFS(pos_st, pos_ed):

  tree = Queue()
  tree.push(((pos_st[0], pos_st[1]), []))

  # store the visited state
  visited = []

  while not tree.isEmpty():
    (state, path) = tree.pop()
    if state == pos_ed:
        break
    for i in range(-1, 2):
        for j in range(-1, 2):
            cur_state = (state[0] +i, state[1]+j)

            if check(cur_state[0], cur_state[1]) and cur_state not in visited :
                print(cur_state)
                visited.append(cur_state)
                tree.push((cur_state, path+[cur_state]))

  return path




# class Find_away:
#     def __init__(self, pos1, pos2):
#         self.pos_st = list(pos1)
#         self.pos_ed = list(pos2)
#         self.visited = {}
#         self.queue = []
#
#     def check(self, x, y):
#         print(x,y)
#         return x>=0 and x<=800 and y>=0 and y<=480
#
#     def trace(self):
#
#
#
#         # print(res)
#         self.visited[str(self.pos_st[0]) +';'+str(self.pos_st[1])] =
#         self.queue.append([self.pos_st])
#         while self.queue:
#
#             path = self.queue.pop(0)
#
#             node  = path[-1]
#
#             # print(node[0])
#             if node == self.pos_ed:
#                 return path
#
#             for i in range (-1, 2):
#                 for j in range(-1, 2):
#                     tmp = copy.deepcopy(node)
#                     tmp[0] += i
#                     tmp[1] += j
#                     # print(tmp)
#                     if tmp not in self.visited and self.check(tmp[0], tmp[1]):
#                         new_path = list(path)
#                         new_path.append(tmp)
#                         self.queue.append(new_path)
#                         self.visited[str(tmp[0])+';'+str(tmp[1])]
#
#             # break
#
