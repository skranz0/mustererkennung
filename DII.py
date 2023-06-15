import numpy as np
import scipy as sp
import skimage
import sys
import matplotlib.pyplot as plt

imgpath = sys.argv[1]
r = sys.argv[2]

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
    #Normalisierung
    V = (3*V)/(2*np.pi*r**3) - 1    
    return V       

def vii_image(image, r):
    img = np.zeros((image.shape[0], image.shape[1]))
    for x in range(r,len(image[0])-r):
        for y in range(r,len(image)-r):
            img[x][y] = volume_integral_invariant(image, r, x, y)
    return img

return_image = vii_image(image,r)
plt.imshow(return_image)
plt.show()
