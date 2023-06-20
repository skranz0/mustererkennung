import numpy as np
import skimage
import sys
from matplotlib import pyplot as plt
from tqdm import tqdm

imgpath = sys.argv[1]
r = int(sys.argv[2])
checkerboard = np.array([[i + j for j in range(5)] for i in range(5)]) % 2


def main():
    print(f"Reading file {imgpath}")
    image = skimage.io.imread(imgpath, as_gray=True)
    # image = checkerboard

    volume_image = vii_image(image, r)
    skimage.io.imsave("volume.tiff", volume_image)
    skimage.io.imshow(volume_image)
    #print(volume_image)
    plt.imshow(volume_image)
    plt.show()


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
    empty = np.ones((input_img.shape[0], input_img.shape[1]))
    print("Calculating volume")
    for y in tqdm(range(0, empty.shape[0])):
        for x in range(0, empty.shape[1]):
            empty[y, x] = volume_integral_invariant(input_img, radius, x, y)
    return empty


if __name__ == "__main__":
    main()
