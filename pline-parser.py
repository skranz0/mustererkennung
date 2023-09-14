import sys
import math
import numpy as np


class Vertex:
    def __init__(self, id: int, coordinates: list[float], orientation: list[float]) -> None:
        self.id = id # TODO make this a dictionary
        self.coordinates = coordinates
        self.orientation = orientation
    def __str__(self) -> str:
        return f"ID: {self.id}\nCoord: {self.coordinates}\nOrient: {self.orientation}"

class Pline:
    def __init__(self, label: int, vertex_count: int, vertices: list[Vertex]) -> None:
        self.label = label
        self.vertex_count = vertex_count
        self.vertices = vertices
    def __str__(self) -> str:
        return f"Polyline {self.label} with {self.vertex_count} vertices"


def read_pline(path: str) -> list[Pline]:
    """Read a polyline from a `.pline` file.

    Args:
        path (str): Path to the file.

    Returns:
        list[Pline]: List of polylines in the file.
    """
    print(f"Parsing file {path}")
    with open(path) as f:
        lines = f.readlines()

    pline_strings = []
    for line in lines:
        if not line.startswith('#'):
            pline_strings.append(line[:-1])

    plines = []
    for pline in pline_strings:
        pline_string = str.split(pline, " ")
        pline_string.reverse()

        pline_label = int(pline_string.pop())
        pline_nvert = int(pline_string.pop())
        pline_verts = []
        while len(pline_string) % 7 == 0 and len(pline_string) > 0: 
            new_id = int(pline_string.pop())
            
            new_coord = [float(x) for x in pline_string[-3:]]
            new_coord.reverse()
            del pline_string[-3:]
            
            new_orient = [float(x) for x in pline_string[-3:]]
            new_orient.reverse()
            del pline_string[-3:]
            
            new_vertex = Vertex(new_id, new_coord, new_orient)
            pline_verts.append(new_vertex)
        #else:
        #    print(f"Liste hat Länge {len(pline_string)}")
        
        new_pline = Pline(pline_label, pline_nvert, pline_verts)
        plines.append(new_pline)
        print(f"{new_pline} eingelesen")
    return plines


def last_in_circle(pline: Pline, start_index: int, radius: int, direction = "right") -> int:
    """From a circle around a vertex of a polyline, find last following vertex that is still inside the circle.

    Args:
        pline (Pline): A polyline.
        start_index (int): The index of the vertex in the center of the circle.
        radius (int): The radius of the circle.
        direction (str, optional): Choose if a vertex right or left from the original vertex is looked for. Defaults to "right".

    Returns:
        int: The index of the last vertex following the original vertex that is still inside the circle.
    """
    # TODO choose vertex by id instead of just position in array mby?
    last_vertex_index = [start_index]
    while True:
        if direction == "right":
            next_vertex_index = (last_vertex_index + 1) % len(pline.vertices)
            if next_vertex_index == start_index:
                return None
        else:
            next_vertex_index = (last_vertex_index - 1) % len(pline.vertices)
        distance = math.dist(pline.vertices[start_index].coordinates,
                             pline.vertices[next_vertex_index].coordinates)
        if distance > radius:
            break
        last_vertex_index = next_vertex_index
    return last_vertex_index

def calc_beta(center: Vertex, last_in: Vertex, first_out: Vertex) -> float:
    """Calculate the angle beta

    Args:
        center (Vertex): Middle point of the circle.
        last_in (Vertex): Last vertex still inside the circle.
        first_out (Vertex): First vertex outside of the circle.

    Returns:
        float: beta in DEG.
    """
    center_vector = list(map(lambda a, b: a - b, center.coordinates, last_in.coordinates))
    out_vector = list(map(lambda a, b: a - b, first_out.coordinates, last_in.coordinates))

    return 180 - np.arccos(np.dot(center_vector, out_vector) / (np.linalg.norm(center_vector) * np.linalg.norm(out_vector)))


def filter_response(i: Vertex, c: Vertex, beta: float, r: float) -> list[float]:
    d = math.dist(c, i)
    p = 2 * d * math.cos(beta)
    q = d + 0.5 * (-p + math.sqrt(p ** 2 - 4 * (d ** 2 - r ** 2)))
    return q


def run_length(qp: float, qm: float, r: float) -> float:
    q = 0.5 * (qp / r + qm /r)
    return q


def calc_alpha(q: float, beta: float, r: float) -> float: # bekommt das q von filter response, nicht run length
    alpha = np.arccos(q * math.cos(beta) / r)


def visualize_pline():
    # TODO let that do something
    pass

def main():
    plines = read_pline(sys.argv[1])
    radius = sys.argv[2]
    """
    TODO für alle Punkte q und alpha bestimmen
    TODO q und alpha für alle Punkte visualisieren
    TODO mby plines visualisieren
    """

    sharp_corners_qs = []
    sharp_corners_alphas = []
    for pline in plines:
        qs = []
        alphas = []
        for vertex in pline.vertices:
            last_right = last_in_circle(pline, pline.index(vertex), radius)
            beta_right = calc_beta(vertex, pline.vertices[last_right], pline.vertices[last_right+1])
            response_right = filter_response(vertex, pline.vertices[last_right], beta_right, radius)

            last_left = last_in_circle(pline, pline.index(vertex), radius, direction="left")
            beta_left = calc_beta(vertex, pline.vertices[last_left], pline.vertices[last_left-1])
            response_left = filter_response(vertex, pline.vertices[last_left], beta_left, radius)

            q = run_length(response_right, response_left, radius)

            alpha = calc_alpha(response_right, beta_right, radius)

            qs.append(q)
            alphas.append(alpha)
        sharp_corners_qs.append(qs)
        sharp_corners_alphas.append(alphas)



if __name__ == "__main__":
    main()