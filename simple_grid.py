import numpy as np
import enum

class DConn(enum.Flag):
	NONE = 0
	SW = enum.auto()
	NE = enum.auto()
	SE = enum.auto()
	NW = enum.auto()

def minmax(ar):
	a = np.min(ar)
	b = np.max(ar)
	return (a, b)

def process_block(x, y, im, dcon):
	# blocK:
	# a   |   b
	# - (x,y) -
	# c   |   d
	a = im[y-1,x-1]
	b = im[y+1,x-1]
	c = im[y-1,x+1]
	d = im[y+1,x+1]

	r0, r1 = minmax([a,d])
	r2, r3 = minmax([b,c])

	if r1 < r2:
		im[y, x] = (r2, r3)

		dcon[y  ,x-1] = DConn.NE
		dcon[y-1,x  ] = DConn.SW

		dcon[y+1,x-1] = DConn.NE
		dcon[y  ,x  ] = DConn.SW | DConn.NE 
		dcon[y-1,x+1] = DConn.SW

		dcon[y  ,x+1] = DConn.SW
		dcon[y+1,x  ] = DConn.NE

	elif r3 < r0:
		im[y, x] = (r0, r1)

		dcon[y  ,x-1] = DConn.SE
		dcon[y+1,x  ] = DConn.NW

		dcon[y-1,x-1] = DConn.SE
		dcon[y  ,x  ] = DConn.SE | DConn.NW
		dcon[y+1,x+1] = DConn.NW

		dcon[y-1,x  ] = DConn.SE
		dcon[y  ,x+1] = DConn.NW

	else:
		im[y, x] = minmax([a,b,c,d])


def build_simple_grid(img):
	h, w = img.shape
	im = np.zeros((2*h-1, 2*w-1), tuple)
	dcon = np.full((2*h-1, 2*w-1), DConn.NONE, dtype=DConn)
	im[0::2, 0::2] = img

	# y is odd & x is even
	# yy, xx = np.mgrid[1::2, 0::2]
	Y, X = np.arange(2*h-1), np.arange(2*w-1)

	yy, xx = np.meshgrid(Y[1::2], X[::2]) 

	for (x,y) in zip(xx.ravel(), yy.ravel()):
		mina, maxa = minmax([im[y-1, x], im[y+1,x]])
		im[y, x] = (mina, maxa)

	# yy, xx = np.mgrid[0::2, 1::2]
	yy, xx = np.meshgrid(Y[0::2], X[1::2])

	# y is even & x is odd
	for (x,y) in zip(xx.ravel(), yy.ravel()):
		mina, maxa = minmax([im[y,x-1], im[y,x+1]])
		im[y, x] = (mina, maxa)

	# yy, xx = np.mgrid[1::2, 1::2]
	yy, xx = np.meshgrid(Y[1::2], X[1::2])
	for (x, y) in zip(xx.ravel(), yy.ravel()):
		print(y,x)
		process_block(x, y, im, dcon)

	yy, xx = np.meshgrid(Y[::2], X[::2])
	for (x, y) in zip(xx.ravel(), yy.ravel()):
		im[y, x] = (im[y, x], im[y, x])

	return (dcon, im)

def tikz_simple_khalimsky_grid(im, dcon):
	h, w = im.shape
	yy, xx = np.meshgrid(np.arange(h), np.arange(w))

	tikz = "\\begin{tikzpicture}\n"

	H, W = (h * 1.6 +1.0), (w * 1.6 + 1.0)

	F = lambda y, x: f"[{im[y,x][0]}, {im[y,x][1]}]"

	tikz += tikz_edges(im, dcon)

	for (x,y) in zip(xx.ravel(), yy.ravel()):
		x_even = ((x % 2) == 0)
		y_even = ((y % 2) == 0)

		if x_even and y_even:
			x_, y_ = x // 2, y // 2
			tl = (x_ * 1.6, H - (y_ * 1.6))
			br = (tl[0] + 1.0, tl[1] - 1.0)

			tikz += f"\t\\draw[fill=white] ({tl[0]},{tl[1]}) rectangle ({br[0]}, {br[1]}); "
			tikz += f"\\node at ({(tl[0]+br[0])/2}, {(tl[1]+br[1])/2}) {{${F(y, x)}$}};\n"

		elif x_even and not y_even: # y is odd and x is even, then vertical-rectangle
			x_, y_ = x // 2, y // 2
			tl = (x_ * 1.6, H - (y_ * 1.6))
			br = (tl[0] + 1.0, tl[1] - 1.0)

			tikz += f"\t\\draw[fill=white] ({tl[0]},{tl[1]-1.05}) rectangle ({br[0]},{br[1]-0.55});\n"
			tikz += f"\\node[] at ({tl[0]+0.5}, {tl[1]-1.3}) {{\\small {F(y, x)}}};\n"

		elif not x_even and y_even:
			x_, y_ = x // 2, y // 2
			tl = (x_ * 1.6, H - (y_ * 1.6))
			br = (tl[0] + 1.0, tl[1] - 1.0)

			tikz += f"\t\\draw[fill=white] ({tl[0]+1.05},{tl[1]}) rectangle ({br[0]+0.55},{br[1]});\n"
			tikz += f"\\node[rotate=90] at ({tl[0]+1.35}, {tl[1]-0.5}) {{\\small {F(y, x)}}};\n"


		else:  # x and y are odd. => circle
			x_, y_ = x // 2, y // 2
			center =  x_ * 1.6 + 1.3, H - ((y_ * 1.6) + 1.3)

			tikz += f"\t\\draw[fill=white] ({center[0]},{center[1]}) circle (0.25); "
			tikz += f"\\node[] at ({center[0]}, {center[1]}) {{\\tiny {F(y, x)}}};\n"

	tikz += "\\end{tikzpicture}"

	return tikz

def tikz_edges(im, dcon):
	h, w = im.shape
	Y, X = np.arange(h), np.arange(w)

	tikz = "\n"

	H, W = (h * 1.6 + 1.0), (w * 1.6 + 1.0)

	xx, yy = np.meshgrid(X[1::2], Y[0::2])
	for (x,y) in zip(xx.ravel(), yy.ravel()):
		x_, y_ = ((x // 2) * 1.6)+1.05, H - ((y // 2) * 1.6)
		tikz += f"\\draw[line width=1mm] ({x_}, {y_-0.5}) -- ({x_-0.05}, {y_-0.5});"
		tikz += f"\\draw[line width=1mm] ({x_+0.50}, {y_-0.5}) -- ({x_+0.55}, {y_-0.5});\n"

		if dcon[y, x] & DConn.NW:
			tikz += f"""\\draw[red, line width=1mm] ({x_+0.2}, {y_-0.2}) -- ({x_-0.2}, {y_+0.2});"""

		if dcon[y, x] & DConn.SE:
			tikz += f"""\\draw[red, line width=1mm] ({x_+0.35}, {y_-0.85}) -- ({x_+0.7}, {y_-1.2});"""

		if dcon[y, x] & DConn.NE:
			tikz += f"""\\draw[red, line width=1mm] ({x_+0.35}, {y_-0.2}) -- ({x_+0.6}, {y_+0.1});"""

		if dcon[y, x] & DConn.SW:
			tikz += f"""\\draw[red, line width=1mm] ({x_+0.2}, {y_-0.8}) -- ({x_-0.2}, {y_-1.2});"""			


	xx, yy = np.meshgrid(X[0::2], Y[1::2])
	for (x,y) in zip(xx.ravel(), yy.ravel()):
		x_, y_ = ((x // 2) * 1.6), H - ((y // 2) * 1.6) - 1.05
		tikz += f"\\draw[line width=1mm] ({x_+0.5}, {y_}) -- ({x_+0.5}, {y_+0.05});" 
		tikz += f"\\draw[line width=1mm] ({x_+0.5}, {y_-0.50}) -- ({x_+0.5}, {y_-0.55});\n"

	xx, yy = np.meshgrid(X[1::2], Y[1::2])
	for (x, y) in zip(xx.ravel(), yy.ravel()):
		x_, y_ = ((x // 2) *1.6), H - ((y // 2)*1.6)
		cx,cy = x_ + 1.3, y_ - 1.3
		tikz += f"\\draw[line width=1mm] ({cx-0.25}, {cy}) -- ({cx-0.30}, {cy});\n"
		tikz += f"\\draw[line width=1mm] ({cx+0.25}, {cy}) -- ({cx+0.30}, {cy});\n"
		tikz += f"\\draw[line width=1mm] ({cx}, {cy-0.25}) -- ({cx}, {cy-0.30});\n"
		tikz += f"\\draw[line width=1mm] ({cx}, {cy+0.25}) -- ({cx}, {cy+0.30});\n"

		if dcon[y,x] & DConn.NW:
			tikz += f"""\\draw[red, line width=1mm] ({cx}, {cy}) -- ({x_+0.5}, {y_-0.5});\n"""

		if dcon[y,x] & DConn.SE:
			tikz += f"""\\draw[red, line width=1mm] ({cx}, {cy}) -- ({x_+1.6+0.5}, {y_-1.6-0.5});\n"""			

		if dcon[y,x] & DConn.NE:
			tikz += f"""\\draw[red, line width=1mm] ({cx}, {cy}) -- ({x_+1.6+0.5}, {y_-0.5});\n"""

		if dcon[y,x] & DConn.SW:
			tikz += f"""\\draw[red, line width=1mm] ({cx}, {cy}) -- ({x_+0.5}, {y_-1.6-0.5});\n"""


	tikz += "\n"
	return tikz


# depth algorithm
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
		if (up < 255): return down

		if (level - down) > (up - level):
			return up
		else:
			return down

	def empty(self):
		for l in np.arange(256):
			if len(self.q[l]) != 0:
				return False
		return True

def neighbours(p, dcon):
	n = [(p[0], p[1]-1), (p[0]+1, p[1]), (p[0], p[1]+1), (p[0]+1,p[1])]
	if dcon[p[0], p[1]] & DConn.NE:
		n.append((p[0]-1, p[1]+1))

	if dcon[p[0], p[1]] & DConn.NW:
		n.append((p[0]-1, p[1]-1))

	if dcon[p[0], p[1]] & DConn.SE:
		n.append((p[0]+1, p[1]+1))

	if dcon[p[0], p[1]] & DConn.SW:
		n.append((p[0]+1, p[1]-1))

	return n

def computeSimpleOrderMap(img, grid, dcon, p_inf=(0,0), should_save_depth_changes=False):
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
				save_tikz(grid, Ord, dcon, f"my-tex/{d:02d}.tex")
			d += 1
		Ord[p[0], p[1]] = d
		R.append(p)
		for n in neighbours(p, dcon):
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

	if should_save_depth_changes:
		save_tikz(grid, Ord, dcon, f"my-tex/{d:02d}.tex")
	return (R, Ord)

def save_tikz(grid, depth, dcon, tikz_filepath):
	h, w = grid.shape
	yy, xx = np.mgrid[0:h, 0:w]

	tikz = "\\begin{tikzpicture}\n"

	tikz += tikz_edges(grid, dcon)

	H, W = (h * 1.6 + 1.0), (w * 1.6 + 1.0)

	F = lambda y, x: f"[${grid[y,x][0]}, {grid[y,x][1]}$]"

	for (x, y) in zip(xx.ravel(), yy.ravel()):
		x_even = ((x % 2) == 0)
		y_even = ((y % 2) == 0)

		if x_even and y_even:
			x_, y_ = x // 2, y // 2
			tl = (x_ * 1.6, H - (y_ * 1.6))
			br = (tl[0] + 1.0, tl[1] - 1.0)

			tikz += f"\t\\draw[line width=0.5mm,fill=white] ({tl[0]}, {tl[1]}) rectangle ({br[0]},{br[1]}); "
			if depth[y,x] > -1:
				tikz += f"\\fill[black!30] ({tl[0]+0.2},{tl[1]-0.2}) rectangle ({br[0]-0.2},{br[1]+0.2});\n"
				tikz += f"\\node[black] at ({(tl[0]+br[0])/2}, {(tl[1]+br[1])/2}) {{${int(depth[y,x])}$}};\n"
			else:
				tikz += f"\\node[] at ({(tl[0]+br[0])/2}, {(tl[1]+br[1])/2}) {{\\small {F(y, x)}}};\n"

		elif x_even and not y_even: # y is odd and x is even, then vertical-rectangle
			x_, y_ = x // 2, y // 2
			tl = (x_ * 1.6, H - (y_ * 1.6))
			br = (tl[0] + 1.0, tl[1] - 1.0)

			tikz += f"\t\\draw[fill=white] ({tl[0]}, {tl[1]-1.05}) rectangle ({br[0]}, {br[1]-0.55});\n"
			if depth[y, x] > -1:
				tikz += f"\t\\fill[black!30] ({tl[0]+0.1}, {tl[1]-1.05-0.1}) rectangle ({br[0]-0.1},{br[1]-0.55+0.1});\n"
				tikz += f"\\node[] at ({tl[0]+0.5}, {tl[1]-1.3}) {{\\small {int(depth[y, x])}}};\n"
			else:
				tikz += f"\\node[] at ({tl[0]+0.5}, {tl[1]-1.3}) {{\\small {F(y, x)}}};\n"

		elif not x_even and y_even:
			x_, y_ = x // 2, y // 2
			tl = (x_ * 1.6, H - (y_ * 1.6))
			br = (tl[0] + 1.0, tl[1] - 1.0)

			tikz += f"\t\\draw[fill=white] ({tl[0]+1.05}, {tl[1]}) rectangle ({br[0]+0.55}, {br[1]});\n"
			if depth[y, x] > -1:
				tikz += f"\t\\fill[black!30] ({tl[0]+1.05+0.15}, {tl[1]-0.15}) rectangle ({br[0]+0.55-0.1}, {br[1]+0.1});\n"
				tikz += f"\\node[] at ({tl[0]+1.35}, {tl[1]-0.5}) {{\\small {int(depth[y,x])}}};\n"
			else:
				tikz += f"\\node[rotate=90] at ({tl[0]+1.35}, {tl[1]-0.5}) {{\\small {F(y, x)}}};\n"

		else:  # x and y are odd => circle
			x_, y_ = x // 2, y // 2
			center = x_ * 1.6 + 1.3, H - ((y_ * 1.6) + 1.3)

			tikz += f"\t\\draw[fill=white] ({center[0]}, {center[1]}) circle (0.25); "
			if depth[y, x] > -1:
				tikz += f"\t\\fill[black!30] ({center[0]}, {center[1]}) circle(0.25);\n"
				tikz += f"\\node[] at ({center[0]}, {center[1]}) {{ \\tiny {int(depth[y, x])}}};\n"
			else:
				tikz += f"\\node[] at ({center[0]}, {center[1]}) {{ \\tiny {F(y, x)}}};\n"

	tikz += "\\end{tikzpicture}"

	with open(tikz_filepath, "w") as f:
		f.write(tikz)


def simple_tikz_depth(depth):
	h, w = depth.shape
	yy, xx = np.mgrid[0:h, 0:w]

	tikz = "\\begin{tikzpicture}\n"

	H, W = (h * 1.05 + 1.0), (w * 1.05 + 1.0)

	mn, mx = np.min(depth), np.max(depth)
	grey = lambda y, x: int((1 - ((depth[y,x] - mn) / mx)) * 100)

	for (x, y) in zip(xx.ravel(), yy.ravel()):
		tl = (x * 1.05, H - (y * 1.05))
		br = (x * 1.05 + 1.0), (H - (y * 1.05 - 1.0))

		if y % 2 == 0 and x % 2 == 0:
			tikz += f"\t\\draw[black, line width=0.5mm] ({tl[0]},{tl[1]}) rectangle ({br[0]}, {br[1]}); "
		else:
			tikz += f"\t\\draw[black] ({tl[0]},{tl[1]}) rectangle ({br[0]}, {br[1]}); "

		tikz += f"\t\\fill[black!{grey(y,x)}] ({tl[0]+0.15},{tl[1]+0.15}) rectangle ({br[0]-0.15}, {br[1]-0.15}); "
		
		if grey(y,x) < 50:
			tikz += f"\\node[black] at ({(tl[0]+br[0])/2}, {(tl[1]+br[1])/2}) {{${depth[y, x]}$}};\n"
		else:
			tikz += f"\\node[white] at ({(tl[0]+br[0])/2}, {(tl[1]+br[1])/2}) {{${depth[y, x]}$}};\n"
	
	tikz += "\\end{tikzpicture}" 

	return tikz