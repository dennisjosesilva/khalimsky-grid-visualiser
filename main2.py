from simple_grid import build_simple_grid
import numpy as np

img = np.array([
	[0,4,1],
	[8,2,8]], np.uint8)

(dcon, grid) = build_simple_grid(img)

print(dcon)