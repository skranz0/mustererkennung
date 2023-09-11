import sys


class Vertex:
    def __init__(self, id: int, coordinates: list[float], orientation: list[float]) -> None:
        self.id = id
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

#filepath = sys.argv[1]
filepath = "polylines_test/polyline_test_subdiv_10k_verts.pline"

with open(filepath) as f:
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
    #print(f"{new_pline} eingelesen")

print(len(plines))
