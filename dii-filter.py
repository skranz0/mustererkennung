import numpy as np
import scipy as sp
import skimage
import sys

imgpath = sys.argv[1]
r = sys.argv[2]

#image = cv2.imread("/Users/skranz/PycharmProjects/mustererkennung/Bilder_itit15_DII_Implementierung/testimage_grid.png", cv2.LOAD_IMAGE_GRAYSCALE)
image = skimage.io.imread(imgpath, as_gray=True)


def volume_integral_invariant(img, r, x, y):
    V = 0
    for i in range(-r,r+1):
        for j in range(-r,r+1):
            h = img[x+i, y+j] - img[x, y] + np.sqrt(r**2 - x**2 - y**2)
            sphere = 2 * np.sqrt(r**2 - i**2 - j**2)

            V += np.max(
                np.min(h, sphere),
                0
            )
