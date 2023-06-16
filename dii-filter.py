import numpy as np
import scipy as sp
import skimage
import sys
from matplotlib import pyplot as plt

imgpath = sys.argv[1]
r = int(sys.argv[2])

image = skimage.io.imread(imgpath, as_gray=True)


def volume_integral_invariant(img, radius, x, y):
    volume = 0
    for i in range(-radius, radius+1):
        for j in range(-r, r+1):
            h = img[x+i, y+j] - img[x, y] + np.sqrt(radius**2 - x**2 - y**2)
            sphere = 2 * np.sqrt(radius**2 - i**2 - j**2)

            volume += np.max(
                np.min(h, sphere),
                0
            )

    # normalizing
    volume = (3 * volume) / (2 * np.pi * radius**3) - 1
    return volume


def vii_image(img, radius):
    img = np.zeros((img.shape[0], img.shape[1]))
    for x in range(radius, len(img[0])-radius):
        for y in range(radius, len(img)-radius):
            img[x, y] = volume_integral_invariant(img, radius, x, y)
    return img


return_image = vii_image(image, r)
plt.imshow(return_image)
plt.show()
