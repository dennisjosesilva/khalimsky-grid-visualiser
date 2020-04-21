import numpy as np

def interpolate(img, op):
	h, w = img.shape
	it = np.zeros((2*h-1, 2*w-1), np.uint8)
	
	it[::2, ::2] = img
	yy, xx = np.mgrid[0:2*h-1, 0:2*w-1]

	for (x,y) in zip(xx.ravel(), yy.ravel()):
		if y % 2 != 0:
			if x % 2 != 0:
				it[y, x] = op([it[y-1,x-1], it[y+1,x-1], it[y-1,x+1], it[y+1,x+1]])
			else:
				it[y, x] = op([it[y-1, x], it[y+1, x]])
		elif x % 2 != 0:
			it[y, x] = op([it[y, x-1], it[y, x+1]])
		else:
			it[y, x] = it[y, x]

	return it



def immerse(img):
	h, w = img.shape
	im = np.zeros((2*h-1, 2*w-1), tuple)
	im[0::2, 0::2] = img

	yy, xx = np.mgrid[0:2*h-1, 0:2*w-1]

	for (x, y) in zip(xx.ravel(), yy.ravel()):
		if y % 2 != 0:
			if x % 2 != 0:
				maxa = np.max([im[y-1,x-1], im[y+1,x-1], im[y-1,x+1], im[y+1,x+1]])
				mina = np.min([im[y-1,x-1], im[y+1,x-1], im[y-1,x+1], im[y+1,x+1]])
				im[y, x] = (mina, maxa)
			else:
				maxa = np.max([im[y-1, x], im[y+1, x]])
				mina = np.min([im[y-1, x], im[y+1, x]])
				im[y, x] = (mina, maxa)
		elif x % 2 != 0:
			maxa = np.max([im[y, x-1], im[y, x+1]])
			mina = np.min([im[y, x-1], im[y, x+1]])
			im[y, x] = (mina, maxa)
		else:
			im[y, x] = im[y, x]


	yy, xx = np.mgrid[:2*h-1:2, :2*w-1:2]
	for (x, y) in zip(xx.ravel(), yy.ravel()):
		im[y, x] = (im[y, x], im[y, x])

	return im


def tikz_interpolation(img):
	h, w = img.shape
	yy, xx = np.mgrid[0:h, 0:w]

	tikz = "\\begin{tikzpicture}\n"

	H, W = (h * 1.05 + 1.0), (w * 1.05 + 1.0)

	for (x, y) in zip(xx.ravel(), yy.ravel()):
		tl = (x * 1.05, H - (y * 1.05))
		br = (x * 1.05 + 1.0), (H - (y * 1.05 - 1.0))
		
		if x % 2 == 0 and y % 2 == 0:
			tikz += f"\t\\draw[black,line width=0.5mm] ({tl[0]},{tl[1]}) rectangle ({br[0]}, {br[1]}); "
			tikz += f"\\node[black] at ({(tl[0]+br[0])/2}, {(tl[1]+br[1])/2}) {{${img[y, x]}$}};\n"
		else:
			tikz += f"\t\\draw[] ({tl[0]},{tl[1]}) rectangle ({br[0]}, {br[1]}); "
			tikz += f"\\node[] at ({(tl[0]+br[0])/2}, {(tl[1]+br[1])/2}) {{${img[y, x]}$}};\n"
	
	tikz += "\\end{tikzpicture}"

	return tikz


def tikz_khalimsky_grid(img):
	h, w = img.shape 
	yy, xx = np.mgrid[0:h, 0:w]

	tikz = "\\begin{tikzpicture}\n"

	H, W = (h * 1.6 + 1.0), (w * 1.6 + 1.0)

	F = lambda  y, x: f"[${img[y,x][0]}, {img[y,x][1]}$]"

	for (x, y) in zip(xx.ravel(), yy.ravel()):
		x_even = ((x % 2) == 0)
		y_even = ((y % 2) == 0) 

		if x_even and y_even:
			x_, y_ = x // 2, y // 2
			tl = (x_ * 1.6, H - (y_ * 1.6))
			br = (tl[0] + 1.0, tl[1] - 1.0)

			if x_ % 2 == 0 and y_ % 2 == 0:
				tikz += f"\t\\draw[black,line width=0.5mm] ({tl[0]},{tl[1]}) rectangle ({br[0]}, {br[1]}); "
				tikz += f"\\node[black] at ({(tl[0]+br[0])/2}, {(tl[1]+br[1])/2}) {{${F(y, x)}$}};\n"
			else:
				tikz += f"\t\\draw ({tl[0]},{tl[1]}) rectangle ({br[0]}, {br[1]}); "
				tikz += f"\\node at ({(tl[0]+br[0])/2}, {(tl[1]+br[1])/2}) {{${F(y, x)}$}};\n"

		elif x_even and not y_even: # y is odd and x is even, then vertical-rectangle
			x_, y_ = x // 2, y // 2
			tl = (x_ * 1.6, H - (y_ * 1.6))
			br = (tl[0] + 1.0, tl[1] - 1.0)

			tikz += f"\t\\draw ({tl[0]},{tl[1]-1.05}) rectangle ({br[0]},{br[1]-0.55});\n"
			tikz += f"\\node[] at ({tl[0]+0.5}, {tl[1]-1.3}) {{\\small {F(y, x)}}};\n"

		elif not x_even and y_even:
			x_, y_ = x // 2, y // 2
			tl = (x_ * 1.6, H - (y_ * 1.6))
			br = (tl[0] + 1.0, tl[1] - 1.0)

			tikz += f"\t\\draw ({tl[0]+1.05},{tl[1]}) rectangle ({br[0]+0.55},{br[1]});\n"
			tikz += f"\\node[rotate=90] at ({tl[0]+1.35}, {tl[1]-0.5}) {{\\small {F(y, x)}}};\n"


		else:  # x and y are odd. => circle
			x_, y_ = x // 2, y // 2
			center =  x_ * 1.6 + 1.3, H - ((y_ * 1.6) + 1.3)

			tikz += f"\t\\draw ({center[0]},{center[1]}) circle (0.25); "
			tikz += f"\\node[] at ({center[0]}, {center[1]}) {{\\tiny {F(y, x)}}};\n"

	tikz += "\\end{tikzpicture}"
	
	return tikz


def tikz_depth(img):
	h, w = img.shape
	yy, xx = np.mgrid[0:h, 0:w]

	tikz = "\\begin{tikzpicture}\n"

	H, W = (h * 1.05 + 1.0), (w * 1.05 + 1.0)

	mn, mx = np.min(img), np.max(img)
	grey = lambda y, x: int((1- ((img[y, x] - mn) / mx)) * 100)

	for (x, y) in zip(xx.ravel(), yy.ravel()):
		tl = (x * 1.05, H - (y * 1.05))
		br = (x * 1.05 + 1.0), (H - (y * 1.05 - 1.0))		
		
		if y % 4 == 0 and x % 4 == 0:
			tikz += f"\t\\draw[black, line width=1.0mm] ({tl[0]},{tl[1]}) rectangle ({br[0]}, {br[1]}); "
		else:
			tikz += f"\t\\draw[black] ({tl[0]},{tl[1]}) rectangle ({br[0]}, {br[1]}); "

		tikz += f"\t\\fill[black!{grey(y,x)}] ({tl[0]+0.15},{tl[1]+0.15}) rectangle ({br[0]-0.15}, {br[1]-0.15}); "
		
		if grey(y,x) < 50:
			tikz += f"\\node[black] at ({(tl[0]+br[0])/2}, {(tl[1]+br[1])/2}) {{${img[y, x]}$}};\n"
		else:
			tikz += f"\\node[white] at ({(tl[0]+br[0])/2}, {(tl[1]+br[1])/2}) {{${img[y, x]}$}};\n"
	
	tikz += "\\end{tikzpicture}"

	return tikz

