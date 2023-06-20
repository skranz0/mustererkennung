import sys

import numpy as np
import skimage
from matplotlib import pyplot as plt
from tqdm import tqdm

image = skimage.io.imread(sys.argv[1], as_gray=True)
volume_image = skimage.io.imread(sys.argv[2], as_gray=True)
r = int(sys.argv[3])
epsilon = 0.1  # TODO argv


def main():
    zero_crossings = zero_crossing(volume_image)

    t = t_mask(image, r)

    edge_img = edge_image(zero_crossings, t)
    skimage.io.imsave("out/edge_img.tiff", edge_img)


def is_zero_crossing(volume, x, y):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (volume.shape[0] > y + i >= 0 and
                    0 <= x + j < volume.shape[1]):
                if (volume[y + i, x + j] * volume[y, x] < 0 or
                        (volume[y + i, x + j] == 0 and volume[y, x] < 0)):
                    return 1
    return 0


def zero_crossing(volume):
    empty = np.zeros((volume.shape[0], volume.shape[1]))
    print("Check for zero crossings")
    for y in tqdm(range(0, empty.shape[0])):
        for x in range(0, empty.shape[1]):
            empty[y, x] = is_zero_crossing(volume, x, y)
    return empty


def patch(input_img, scharr_img, radius, x, y):
    p = 0
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            if 0 <= y + i < input_img.shape[0] and 0 <= x + j < input_img.shape[1]:
                if (input_img[y + i, x + j] - input_img[y, x]) ** 2 + i ** 2 + j ** 2 <= radius ** 2:
                    p += scharr_img[y + i, x + j]
    return p


def t_mask(input_image, radius):
    scharr_img = skimage.filters.scharr(input_image)
    empty = np.zeros(input_image.shape)
    print(f"empty = {empty.shape}")
    t = np.zeros(input_image.shape)
    print("Create patch")
    for y in tqdm(range(0, empty.shape[0])):
        for x in range(0, empty.shape[1]):
            empty[y, x] = patch(input_image, scharr_img, radius, x, y)
    print("Calculate t-mask")
    for y in tqdm(range(0, empty.shape[0])):
        for x in range(0, empty.shape[1]):
            tmp = min_patch(empty, radius, x, y) * (2 + epsilon)
            if empty[y, x] > tmp:
                t[y, x] = 1
    return t


def min_patch(patch, radius, x, y):
    if x - r < 0:
        a = 0
        b = x + r
    elif x + r >= len(patch):
        a = x - r
        b = len(patch)
    else:
        a = x - r
        b = x + r

    if y - r < 0:
        c = 0
        d = y + r
    elif y + r >= len(patch):
        c = y - r
        d = len(patch)
    else:
        c = y - r
        d = y + r
    print(f"x = {x}, y = {y}")
    print(patch[c:d, a:b].shape)
    return min(map(min, patch[c:d+1, a:b+1]))


def is_edge(zero_crossings, t, x, y):
    return zero_crossings[y, x] * t[y, x]


def edge_image(zero_crossings, t):
    empty = np.zeros(zero_crossings.shape)
    print("Calculate edge image")
    print(zero_crossings.shape)
    print(t.shape)
    for x in tqdm(range(0, zero_crossings.shape[1])):
        for y in range(0, zero_crossings.shape[0]):
            print(f"x = {x}, y = {y}")
            empty[y, x] = is_edge(zero_crossings, t, x, y)
    return empty


if __name__ == "__main__":
    main()
