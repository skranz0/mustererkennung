import skimage
from matplotlib import pyplot as plt
import numpy as np

# Lade das Bild
pltimage = skimage.io.imread("~/Schreibtisch/lenna_2048.png", as_gray=True)

# Konvertiere das Bild in ein NumPy-Array
pltimage = np.array(pltimage)

# Berechne die Höhe des Plots
height = pltimage.mean()

# Erstelle ein 3D-Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Berechne die X- und Y-Koordinaten der Punkte
x = np.arange(pltimage.shape[0])
y = np.arange(pltimage.shape[1])

# Erstelle ein Raster aus den X- und Y-Koordinaten
X, Y = np.meshgrid(x, y)

# Erstelle ein Array mit den Höhen der Punkte
Z = pltimage / height

# Zeichne das 3D-Raster
ax.plot_surface(X, Y, Z, cmap="gray")

# Zeige den Plot an
plt.show()