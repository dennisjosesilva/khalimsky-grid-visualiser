import numpy as np

def interpolate(img, op):
	w, h = img.shape
	it = np.zeros((2*h-1, 2*w-1), np.uint8)

	xx, yy = np.mgrid[0:2*h-1, 0:2*w-1]

	it[0::2, 0::2] = img
	for (x,y) in zip(xx.ravel(), yy.ravel()):
		if y % 2 == 1:
			if x % 2 == 1:
				it[x, y] = np.max([it[x-1,y-1], it[x+1,y-1], it[x-1,y+1], it[x+1,y+1]])
			else:
				it[x, y] = np.max([it[x, y-1], it[x, y+1]])
		elif x % 2 == 1:
			it[x, y] = np.max([it[x-1, y], it[x+1, y]])
		else:
			it[x, y] = it[x, y]

	return it



def immerse(img):
	w, h = img.shape
	im = np.zeros((2*h-1, 2*w-1), tuple)
	im[0::2, 0::2] = img

	xx, yy = np.mgrid[0:2*h-1, 0:2*w-1]

	for (x, y) in zip(xx.ravel(), yy.ravel()):
		if y % 2 == 1:
			if x % 2 == 1:
				maxa = np.max([im[x-1,y-1], im[x+1,y-1], im[x-1,y+1], im[x+1,y+1]])
				mina = np.min([im[x-1,y-1], im[x+1,y-1], im[x-1,y+1], im[x+1,y+1]])
				im[x, y] = (mina, maxa)
			else:
				maxa = np.max([im[x, y-1], im[x, y+1]])
				mina = np.min([im[x, y-1], im[x, y+1]])
				im[x, y] = (mina, maxa)
		elif x % 2 == 1:
			maxa = np.max([im[x-1, y], im[x+1, y]])
			mina = np.min([im[x-1, y], im[x+1, y]])
			im[x, y] = (mina, maxa)
		else:
			im[x, y] = im[x, y]


	xx, yy = np.mgrid[:2*h-1:2, :2*w-1:2]
	for (x, y) in zip(xx.ravel(), yy.ravel()):
		im[x, y] = (im[x, y], im[x, y])

	return im


def tikz_interpolation(img):
	h, w = img.shape
	pass