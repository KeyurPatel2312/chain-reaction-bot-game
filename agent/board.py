import copy

class Board():
	def __init__(self, m = 9, n = 6, player = 1):
		self.m = m
		self.n = n
		self.board = [[0 for i in range(self.n)] for i in range(self.m)]
		self.player = player

	def __getitem__(self, pos):
		return self.board[pos[0]][pos[1]]

	def __setitem__(self, pos, value):
		self.board[pos[0]][pos[1]] = value

	def __str__(self):
		state = ""
		for i in range(self.m):
			for j in range(self.n):
				state += str(self.board[i][j])
				state += " "
			state += "\n"
		return state

	def critical_mass(self, pos):
		if pos == (0, 0) or pos == (self.m-1, self.n-1) or pos == (self.m-1, 0) or pos == (0, self.n-1):
			return 2
		elif pos[0] == 0 or pos[0] == self.m-1 or pos[1] == 0 or pos[1] == self.n-1:
			return 3
		else:
			return 4

	def neighbors(self, pos):
		neighbors_list = []
		for i in [(pos[0],pos[1]+1), (pos[0],pos[1]-1), (pos[0]+1,pos[1]), (pos[0]-1,pos[1])]:
			if 0 <= i[0] < self.m and 0 <= i[1] < self.n:
				neighbors_list.append(i)
		return neighbors_list

	def input(self, state, player):
		for pos in [(x,y) for x in range(self.m) for y in range(self.n)]:
			self.board[pos[0]][pos[1]] = state[pos[0]][pos[1]]
		self.player = player

	def valid_move(self):
		if self.cal_heuristics() in [200,-200]:
			return []
		valid = []
		for pos in [(x,y) for x in range(self.m) for y in range(self.n)]:
			if self.board[pos[0]][pos[1]]/self.player >= 0:
				valid.append(pos)
		return valid

	def invalid_move(self):
		invalid = []
		for pos in [(x,y) for x in range(self.m) for y in range(self.n)]:
			if self.board[pos[0]][pos[1]]/self.player < 0:
				invalid.append(pos)
		return invalid

	def move(self, pos):
		self.board[pos[0]][pos[1]] += self.player
		unstable = []
		unstable.append(pos)
		while len(unstable) > 0:
			pos = unstable.pop(0)
			if self.cal_heuristics() in [200,-200]:
				break
			if abs(self.board[pos[0]][pos[1]]) >= self.critical_mass(pos):
				self.board[pos[0]][pos[1]] -= self.player * self.critical_mass(pos)
				for i in self.neighbors(pos):
					self.board[i[0]][i[1]] = self.player * (abs(self.board[i[0]][i[1]]) + 1)
					unstable.append(i)
		self.player *= -1      

	def cal_heuristics(self,player = 1):

		heuristic_value = 0

		positive_orbs, negative_orbs = 0, 0

		for pos in [(x,y) for x in range(self.m) for y in range(self.n)]:
			if self.board[pos[0]][pos[1]] > 0:
				positive_orbs += self.board[pos[0]][pos[1]]
			else:
				negative_orbs += self.board[pos[0]][pos[1]]

		heuristic_value = positive_orbs + negative_orbs

		if negative_orbs == 0 and positive_orbs > 1:
			heuristic_value = 200

		elif positive_orbs == 0 and negative_orbs < -1:
			heuristic_value = -200

		return heuristic_value * player

	def list(self):
		state = []
		for i in range(self.m):
			for j in range(self.n):
				state.append(self.board[i][j])
		return state

	def reset(self):
		self.board = [[0 for i in range(self.n)] for i in range(self.m)]
		self.player = 1