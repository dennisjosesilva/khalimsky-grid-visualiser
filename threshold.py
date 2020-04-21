import numpy as np

def grey_upper_level_set(img, level):
	return img >= level

def grey_lower_level_set(img, level):
	return img <= level 

def intvl_upper_level_set(grid, level):
	upper = np.vectorize(lambda v: v[1] >= level)
	return upper(grid)

def intvl_lower_level_set(grid, level):
	lower = np.vectorize(lambda v: v[0] <= level)
	return lower(grid)

def tikz_level_set_khalimsky_grid(levelset):
	h, w = levelset.shape 
	yy, xx = np.mgrid[0:h, 0:w]

	tikz = "\\begin{tikzpicture}\n"

	H, W = (h * 1.6 + 1.0), (w * 1.6 + 1.0)

	for (x, y) in zip(xx.ravel(), yy.ravel()):
		x_even = ((x % 2) == 0)
		y_even = ((y % 2) == 0) 

		if x_even and y_even:
			x_, y_ = x // 2, y // 2
			tl = (x_ * 1.6, H - (y_ * 1.6))
			br = (tl[0] + 1.0, tl[1] - 1.0)

			if x_ % 2 == 0 and y_ % 2 == 0:
				tikz += f"\t\\draw[black,line width=0.5mm] ({tl[0]},{tl[1]}) rectangle ({br[0]}, {br[1]}); "
			else:
				tikz += f"\t\\draw ({tl[0]},{tl[1]}) rectangle ({br[0]}, {br[1]}); "
			
			if levelset[y, x]:
				tikz += f"\t\\fill[black] ({tl[0]+0.2},{tl[1]-0.2}) rectangle ({br[0]-0.2}, {br[1]+0.2});"

		elif x_even and not y_even: # y is odd and x is even, then vertical-rectangle
			x_, y_ = x // 2, y // 2
			tl = (x_ * 1.6, H - (y_ * 1.6))
			br = (tl[0] + 1.0, tl[1] - 1.0)

			tikz += f"\t\\draw ({tl[0]},{tl[1]-1.05}) rectangle ({br[0]},{br[1]-0.55});\n"
			if levelset[y, x]:
				tikz += f"\t\\fill[black] ({tl[0]+0.1},{tl[1]-1.05-0.1}) rectangle ({br[0]-0.1},{br[1]-0.55+0.1});\n"
						

		elif not x_even and y_even:
			x_, y_ = x // 2, y // 2
			tl = (x_ * 1.6, H - (y_ * 1.6))
			br = (tl[0] + 1.0, tl[1] - 1.0)

			tikz += f"\t\\draw ({tl[0]+1.05},{tl[1]}) rectangle ({br[0]+0.55},{br[1]});\n"
			if levelset[y, x]:
				tikz += f"\t\\fill[black] ({tl[0]+1.05+0.15},{tl[1]-0.15}) rectangle ({br[0]+0.55-0.1},{br[1]+0.1});\n"
						

		else:  # x and y are odd. => circle
			x_, y_ = x // 2, y // 2
			center =  x_ * 1.6 + 1.3, H - ((y_ * 1.6) + 1.3)

			tikz += f"\t\\draw ({center[0]},{center[1]}) circle (0.25); "
			if levelset[y, x]:
				tikz += f"\t\\fill[black] ({center[0]},{center[1]}) circle (0.15); "

	tikz += "\\end{tikzpicture}"
	
	return tikz


def tikz_level_set(levelset):
	h, w = levelset.shape
	yy, xx = np.mgrid[0:h, 0:w]

	tikz = "\\begin{tikzpicture}\n"

	H, W = (h * 1.05 + 1.0), (w * 1.05 + 1.0)

	
	for (x, y) in zip(xx.ravel(), yy.ravel()):
		tl = (x * 1.05, H - (y * 1.05))
		br = (x * 1.05 + 1.0), (H - (y * 1.05 - 1.0))		
		
		tikz += f"\t\\draw[black] ({tl[0]},{tl[1]}) rectangle ({br[0]}, {br[1]}); "
		if levelset[y, x]:
			tikz += f"\t\\fill[black] ({tl[0]+0.15},{tl[1]+0.15}) rectangle ({br[0]-0.15}, {br[1]-0.15});\n"
		
	tikz += "\\end{tikzpicture}"

	return tikz