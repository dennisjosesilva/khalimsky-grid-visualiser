import numpy as np

class Queue:
	def __init__(self):
		self.q = []
		for l in np.arange(256):
			self.q.append([])

	def insert(self, level, point):
		self.q[level].append(point)

	def pop(self, level):
		l = level
		if len(self.q[level]) == 0:
			l = self.next__(level)
		return (l, self.q[l].pop(0))

	def next__(self, level):
		down, up = level-1, level+1

		while up < 256 and len(self.q[up]) == 0:
			up += 1

		while down >= 0 and len(self.q[down]) == 0:
			down -= 1

		if (down < 0): return up
		if (up > 255): return down

		if  (level - down) > (up - level):
			return up
		else:
			return down

	def empty(self):
		for l in np.arange(256):
			if len(self.q[l]) != 0:
				return False
		return True

def n4(p):
	return [
		(p[0], p[1]-1), 
		(p[0]+1, p[1]),
		(p[0], p[1]+1),
		(p[0]+1, p[1])]


def computeOrderMap(img, grid, p_inf = (0,0)):
	UNPROCESSED = -2
	PROCESSED = -1

	Q = Queue()
	R = []
	Ord = np.ones(grid.shape) * UNPROCESSED
	l_old = img[p_inf[0], p_inf[1]]
	Q.insert(l_old, p_inf)
	d = 0

	F = lambda pt: grid[pt[0], pt[1]]

	while not Q.empty():
		(l, p) = Q.pop(l_old)
		if l_old != l:
			d += 1
		Ord[p[0], p[1]] = d
		R.append(p)
		for n in n4(p):
			if n[0] >= 0 and n[0] < Ord.shape[0] and n[1] >= 0 and n[1] < Ord.shape[1] and Ord[n[0], n[1]] == UNPROCESSED:
			   (a, b) = F(n)
			   if l < a: 
			   		Q.insert(a, n)
			   elif l > b:
			   		Q.insert(b, n)
			   else:
			   		Q.insert(l, n)
			   Ord[n[0], n[1]] = PROCESSED
		l_old = l

	return (R, Ord) 



