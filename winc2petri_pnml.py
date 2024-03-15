import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout

def parse_matrix(matrix_str):
    matrix = eval(matrix_str)
    return matrix

def generate_petri_pnml(matrix):
    G = nx.DiGraph()
    num_places = len(matrix)
    num_transitions = len(matrix[0])
    places = [f"v_{i+1}" for i in range(num_places)]
    transitions = [f"T_{j+1}" for j in range(num_transitions)]

    for i in range(num_places):
        for j in range(num_transitions):
            if matrix[i][j] != 0:
                if matrix[i][j] > 0:
                    G.add_edge(transitions[j], places[i])
                else:
                    G.add_edge(places[i], transitions[j])

    pos = graphviz_layout(G, prog="dot")  # Use Graphviz for Sugiyama layout

    # Rotate and double the distances between objects
    for node, coord in pos.items():
        x, y = coord
        pos[node] = (-2 * y, 2 * x)  # Swap x and y, negate new x, and double the distances

    # Creating PNML structure
    pnml = ET.Element("pnml")
    net = ET.SubElement(pnml, "net", {"id": "information_warfare", "type": "http://www.pnml.org/version-2009/grammar/ptnet"})

    # Adding places
    for place_id in places:
        x, y = pos[place_id]
        place = ET.SubElement(net, "place", {"id": place_id})
        graphics = ET.SubElement(place, "graphics")
        position = ET.SubElement(graphics, "position", {"x": str(x), "y": str(y)})
        if any(place_id == arc[0] for arc in G.edges()):
            initial_marking = ET.SubElement(place, "initialMarking")
            text = ET.SubElement(initial_marking, "text")
            text.text = "1"

    # Adding transitions
    for transition_id in transitions:
        x, y = pos[transition_id]
        transition = ET.SubElement(net, "transition", {"id": transition_id})
        graphics = ET.SubElement(transition, "graphics")
        position = ET.SubElement(graphics, "position", {"x": str(x), "y": str(y)})

    # Adding arcs
    for arc in G.edges():
        source, target = arc
        ET.SubElement(net, "arc", {"id": f"arc_{source}_to_{target}", "source": source, "target": target})

    # Generating PNML file
    tree = ET.ElementTree(pnml)
    xml_str = minidom.parseString(ET.tostring(pnml)).toprettyxml(indent="    ")
    with open("output_petri.pnml", "w") as f:
        f.write(xml_str)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python winc2petri_pnml.py \"[[-1, 1], [1, -1], [0, 0]]\"")
        sys.exit(1)
    
    matrix_str = sys.argv[1]
    matrix = parse_matrix(matrix_str)
    generate_petri_pnml(matrix)