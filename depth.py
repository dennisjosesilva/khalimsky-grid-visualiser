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


def computeOrderMap(img, grid, p_inf = (0,0), should_save_depth_changes=False):
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
			if should_save_depth_changes:
				save_tikz(grid, Ord, f"my-tex/0{d}.tex")
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

	save_tikz(grid, Ord, f"my-tex/0{d+4}.tex")
	return (R, Ord) 


def save_tikz(grid, depth, tikz_filepath):
	h, w = grid.shape 
	yy, xx = np.mgrid[0:h, 0:w]

	tikz = "\\begin{tikzpicture}\n"

	H, W = (h * 1.6 + 1.0), (w * 1.6 + 1.0)

	F = lambda  y, x: f"[${grid[y,x][0]}, {grid[y,x][1]}$]"

	for (x, y) in zip(xx.ravel(), yy.ravel()):
		x_even = ((x % 2) == 0)
		y_even = ((y % 2) == 0) 

		if x_even and y_even:
			x_, y_ = x // 2, y // 2
			tl = (x_ * 1.6, H - (y_ * 1.6))
			br = (tl[0] + 1.0, tl[1] - 1.0)

			if x_ % 2 == 0 and y_ % 2 == 0:
				tikz += f"\t\\draw[black,line width=0.5mm] ({tl[0]},{tl[1]}) rectangle ({br[0]}, {br[1]}); "
				if depth[y, x] > -1:
					tikz += f"\\fill[black!30] ({tl[0]+0.2},{tl[1]-0.2}) rectangle ({br[0]-0.2}, {br[1]+0.2});\n"
					tikz += f"\\node[black] at ({(tl[0]+br[0])/2}, {(tl[1]+br[1])/2}) {{${int(depth[y,x])}$}};\n"
				else:
					tikz += f"\\node[black] at ({(tl[0]+br[0])/2}, {(tl[1]+br[1])/2}) {{${F(y, x)}$}};\n"
					
			else:
				tikz += f"\t\\draw ({tl[0]},{tl[1]}) rectangle ({br[0]}, {br[1]});"
				if depth[y, x] > -1:
					tikz += f"\\fill[black!30] ({tl[0]+0.2},{tl[1]-0.2}) rectangle ({br[0]-0.2}, {br[1]+0.2});\n"
					tikz += f"\\node[black] at ({(tl[0]+br[0])/2}, {(tl[1]+br[1])/2}) {{${int(depth[y,x])}$}};\n"
				else:	
					tikz += f"\\node at ({(tl[0]+br[0])/2}, {(tl[1]+br[1])/2}) {{${F(y, x)}$}};\n"

		elif x_even and not y_even: # y is odd and x is even, then vertical-rectangle
			x_, y_ = x // 2, y // 2
			tl = (x_ * 1.6, H - (y_ * 1.6))
			br = (tl[0] + 1.0, tl[1] - 1.0)

			tikz += f"\t\\draw ({tl[0]},{tl[1]-1.05}) rectangle ({br[0]},{br[1]-0.55});\n"
			if depth[y, x] > -1:
				tikz += f"\t\\fill[black!30] ({tl[0]+0.1},{tl[1]-1.05-0.1}) rectangle ({br[0]-0.1},{br[1]-0.55+0.1});\n"
				tikz += f"\\node[] at ({tl[0]+0.5}, {tl[1]-1.3}) {{\\small {int(depth[y, x])}}};\n"
			else:	
				tikz += f"\\node[] at ({tl[0]+0.5}, {tl[1]-1.3}) {{\\small {F(y, x)}}};\n"

		elif not x_even and y_even:
			x_, y_ = x // 2, y // 2
			tl = (x_ * 1.6, H - (y_ * 1.6))
			br = (tl[0] + 1.0, tl[1] - 1.0)

			tikz += f"\t\\draw ({tl[0]+1.05},{tl[1]}) rectangle ({br[0]+0.55},{br[1]});\n"
			if depth[y, x] > -1:
				tikz += f"\t\\fill[black!30] ({tl[0]+1.05+0.15},{tl[1]-0.15}) rectangle ({br[0]+0.55-0.1},{br[1]+0.1});\n"
				tikz += f"\\node[] at ({tl[0]+1.35}, {tl[1]-0.5}) {{\\small {int(depth[y, x])}}};\n"
			else:
				tikz += f"\\node[rotate=90] at ({tl[0]+1.35}, {tl[1]-0.5}) {{\\small {F(y, x)}}};\n"

		else:  # x and y are odd. => circle
			x_, y_ = x // 2, y // 2
			center =  x_ * 1.6 + 1.3, H - ((y_ * 1.6) + 1.3)

			tikz += f"\t\\draw ({center[0]},{center[1]}) circle (0.25); "
			if depth[y, x] > -1:
				tikz += f"\t\\fill[black!30] ({center[0]},{center[1]}) circle (0.15); "
				tikz += f"\\node[] at ({center[0]}, {center[1]}) {{\\tiny {int(depth[y, x])}}};\n"
			else:
				tikz += f"\\node[] at ({center[0]}, {center[1]}) {{\\tiny {F(y, x)}}};\n"

	tikz += "\\end{tikzpicture}"
	
	with open(tikz_filepath, "w") as f:
		f.write(tikz)