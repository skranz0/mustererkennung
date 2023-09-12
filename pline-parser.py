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
    center_vector = list(map(lambda a, b: a - b, center.coordinates, last_in.coordinates))
    out_vector = list(map(lambda a, b: a - b, first_out.coordinates, last_in.coordinates))

    return 180 - np.arccos(np.dot(center_vector, out_vector) / (np.linalg.norm(center_vector) * np.linalg.norm(out_vector)))


def filter_response(i: Vertex, c: Vertex, beta: float, r: float) -> list[float]:
    d = math.dist(c, i)
    p = 2 * d * math.cos(beta)
    q = d + 0.5 * (-p + sqrt(p ** 2 - 4 * (d ** 2 - r ** 2)))
    return q


def run_length(qp: float, qm: float, r: float) -> float:
    q = 0.5 * (qp / r + qm /r)
    return q


def calc_alpha(q: float, beta: float, r: float) -> float: # bekommt das q von filter response, nicht run length
    alpha = np.arccos(q * math.cos(beta) / r)


def visualize_pline():
    pass

def main():
    plines = read_pline(sys.argv[1])
    radius = sys.argv[2]
    """
    TODO für alle Punkte q und alpha bestimmen
    TODO q und alpha für alle Punkte visualisieren
    TODO mby plines visualisieren
    """
    
    


if __name__ == "__main__":
    main()