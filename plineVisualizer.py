import sys
from matplotlib import pyplot as plt
import pandas as pd
from plineParser import Pline, Vertex, read_pline


def transform_pline(pline: Pline):
    xs = []
    ys = []
    zs = []
    for vertex in pline.vertices:
        xs.append(vertex.coordinates[0])
        ys.append(vertex.coordinates[1])
        zs.append(vertex.coordinates[2])
    coordinates = [xs, ys, zs]
    return coordinates

    

def visualize_pline(pline: Pline):
    """fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.scatter(xs, ys, zs)
    plt.show()"""

def main():
    path = sys.argv[1]
    plines = read_pline(path)
    for pline in plines:
        points = transform_pline(pline)
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ax.plot(points[0], points[1], points[2])
    plt.show()



if __name__ == "__main__":
    main()
