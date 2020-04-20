from grid import interpolate, immerse, tikz_khalimsky_grid
import numpy as np

f = np.array(
	[[0,0,0,0,0,0,0],
	 [0,4,4,4,7,7,7],
	 [0,7,7,4,7,4,7],
	 [0,7,4,4,7,4,7],
	 [0,4,4,4,7,4,7],
	 [0,7,7,4,7,7,7],
	 [0,0,0,0,0,0,0]], np.uint8)


it = interpolate(f, None)
im = immerse(it)

# print(im.shape)
tikz = tikz_khalimsky_grid(im)

with open("grid.tex", "w") as f:
	f.write(tikz)
