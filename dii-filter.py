import numpy as np
import skimage
import sys
from matplotlib import pyplot as plt
from tqdm import tqdm

imgpath = sys.argv[1]
r = int(sys.argv[2])
checkerboard = np.array([[i + j for j in range(5)] for i in range(5)]) % 2


print(f"Reading file {imgpath}")
image = skimage.io.imread(imgpath, as_gray=True)
#image = checkerboard


def volume_integral_invariant(img, radius, x, y):
    volume = 0
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):

            # don't exceed the image
            if x + i < np.shape(img)[1] and y + j < np.shape(img)[0]:
                a = y + j
                b = x + i
            elif x + i < np.shape(img)[1] and y + j >= np.shape(img)[0]:
                # y spiegeln
                a = y - j
                b = x + i
            elif x + i >= np.shape(img)[1] and y + j < np.shape(img)[0]:
                # x spiegeln
                a = y + j
                b = x - i
            elif x + i >= np.shape(img)[1] and y + j >= np.shape(img)[0]:
                # beides spiegeln
                a = y - j
                b = x - i

            def calc_h():
                if radius ** 2 - x ** 2 - y ** 2 >= 0:
                    return img[abs(a), abs(b)] - img[y, x] + np.sqrt(radius ** 2 - x ** 2 - y ** 2)
                else:
                    return img[abs(a), abs(b)] - img[y, x]

            def calc_sphere():
                if radius ** 2 - i ** 2 - j ** 2 >= 0:
                    return 2 * np.sqrt(radius ** 2 - i ** 2 - j ** 2)
                else:
                    return 0

            h = calc_h()
            sphere = calc_sphere()

            tmp = min(h, sphere)
            volume += max(tmp, 0)
    # normalizing
    if volume != 0:
        volume = (3 * volume) / (2 * np.pi * radius ** 3) - 1
    return volume


def vii_image(input_img, radius):
    empty = np.zeros((input_img.shape[0], input_img.shape[1]))
    print("Calculating volume")
    for y in tqdm(range(0, len(empty))):
        for x in range(0, len(empty[0])):
            empty[y, x] = volume_integral_invariant(input_img, radius, x, y)
    return empty


def is_zero_crossing(volume, x, y):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (volume.shape[0] > y + i >= 0 and
                    0 <= x + j < volume.shape[1]):
                if volume[y + i, x + j] * volume[y, x] < 0:
                    return 1
    return 0


def zero_crossing(volume):
    empty = np.zeros((volume.shape[0], volume.shape[1]))
    print("Check for zero crossings")
    for y in tqdm(range(0, len(empty))):
        for x in range(0, len(empty[0])):
            empty[y, x] = is_zero_crossing(volume, x, y)
    return empty


volume_image = vii_image(image, r)
print(volume_image)
plt.imshow(volume_image)
plt.show()

zero_crossings = zero_crossing(volume_image)
print(zero_crossings)
plt.imshow(zero_crossings)
plt.show()
