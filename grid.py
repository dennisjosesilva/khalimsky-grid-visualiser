import numpy as np

def interpolate(img, op):
	w, h = img.shape
	it = np.zeros((2*h-1, 2*w-1), np.uint8)
	
	it[::2, ::2] = img
	yy, xx = np.mgrid[0:2*h-1, 0:2*w-1]

	for (x,y) in zip(xx.ravel(), yy.ravel()):
		if y % 2 != 0:
			if x % 2 != 0:
				it[y, x] = np.max([it[y-1,x-1], it[y+1,x-1], it[y-1,x+1], it[y+1,x+1]])
			else:
				it[y, x] = np.max([it[y-1, x], it[y+1, x]])
		elif x % 2 != 0:
			it[y, x] = np.max([it[y, x-1], it[y, x+1]])
		else:
			it[y, x] = it[y, x]

	return it



def immerse(img):
	w, h = img.shape
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
	pass


def tikz_khalimsky_grid(img):
	h, w = img.shape 
	yy, xx = np.mgrid[0:h, 0:w]

	tikz = "\\begin{tikzpicture}\n"

	H, W = (h * 1.6 + 1.0), (w * 1.6 + 1.0)

	for (x, y) in zip(xx.ravel(), yy.ravel()):
		x_even = ((x % 2) == 0)
		y_even = ((y % 2) == 0) 

		if x_even and y_even:
			x_, y_ = x / 2, y / 2
			tl = (x_ * 1.6, H - (y_ * 1.6))
			br = (tl[0] + 1.0, tl[1] - 1.0)

			tikz += f"\t\\draw ({tl[0]},{tl[1]}) rectangle ({br[0]}, {br[1]}); "
			tikz += f"\\node at ({(tl[0]+br[0])/2}, {(tl[1]+br[1])/2}) {{${img[y, x]}$}};\n"

		elif x_even and not y_even:
			pass

		elif not x_even and y_even:
			pass

		else:  # x and y are odd.
			



	tikz += "\\end{tikzpicture}"
	
	return tikz