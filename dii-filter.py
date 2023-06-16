import numpy as np
import scipy as sp
import skimage
import sys
from matplotlib import pyplot as plt
from tqdm import tqdm

imgpath = sys.argv[1]
r = int(sys.argv[2])

print(f"Reading file {imgpath}")
image = skimage.io.imread(imgpath, as_gray=True)
print(image)

def volume_integral_invariant(img, radius, x, y):
    volume = 0
    for i in range(-radius, radius+1):
        for j in range(-r, r+1):
            # don't go to negative pixel positions
            if x+i >= 0 and y+j >= 0:
                # don't exceed the image
                if x+i < np.shape(img)[0] and y+j < np.shape(img)[1]:
                    # make sure there is no sqrt < 0
                    d = radius**2 - x**2 - y**2
                    if d >= 0:
                        h = img[x+i, y+j] - img[x, y] + np.sqrt(d)
                        sphere = 2 * np.sqrt(d)
                    else:
                        h = 0
                        sphere = 0

                    volume += np.max(
                        np.min(h, sphere),
                        0
                    )

    # normalizing
    volume = (3 * volume) / (2 * np.pi * radius**3) - 1
    return volume


def vii_image(input_img, radius):
    img = np.zeros((input_img.shape[0], input_img.shape[1]))
    for x in tqdm(range(radius, len(img[0])-radius), unit="pixelrows"):
        for y in range(radius, len(img)-radius):
            img[x, y] = volume_integral_invariant(input_img, radius, x, y)
    return img


return_image = vii_image(image, r)
plt.imshow(return_image)
plt.show()
