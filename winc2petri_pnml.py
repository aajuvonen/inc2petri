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
                    G.add_edge(transitions[j], places[i], weight=str(matrix[i][j]))
                else:
                    G.add_edge(places[i], transitions[j], weight=str(-matrix[i][j]))

    pos = graphviz_layout(G, prog="dot")  # Use Graphviz for Sugiyama layout

    # Rotate and double the distances between objects
    for node, coord in pos.items():
        x, y = coord
        pos[node] = (-2 * y, 2 * x)  # Swap x and y, negate new x, and double the distances

    # Creating PNML structure
    pnml = ET.Element("pnml")
    net = ET.SubElement(pnml, "net", {"id": "output_petri", "type": "http://www.pnml.org/version-2009/grammar/pnml"})

    # Adding places
    for place_id in places:
        if place_id not in G:
            for transition_id in transitions:
                G.add_edge(transition_id, place_id)

    # Adding transitions
    for transition_id in transitions:
        if transition_id not in G:
            for place_id in places:
                G.add_edge(transition_id, place_id)

    # Removing dummy arcs
    G.remove_nodes_from(nx.isolates(G))

    # Adding places
    for place_id in places:
        x, y = pos.get(place_id, (0, 0))  # Default position if not found
        place = ET.SubElement(net, "place", {"id": place_id})
        graphics = ET.SubElement(place, "graphics")
        position = ET.SubElement(graphics, "position", {"x": str(x), "y": str(y)})
        name = ET.SubElement(place, "name")
        text = ET.SubElement(name, "text")

    # Adding transitions
    for transition_id in transitions:
        x, y = pos.get(transition_id, (0, 0))  # Default position if not found
        transition = ET.SubElement(net, "transition", {"id": transition_id})
        graphics = ET.SubElement(transition, "graphics")
        position = ET.SubElement(graphics, "position", {"x": str(x), "y": str(y)})
        name = ET.SubElement(transition, "name")
        text = ET.SubElement(name, "text")

    # Adding arcs
    for arc in G.edges(data=True):
        source, target, data = arc
        weight = data.get("weight")
        if weight:
            arc_elem = ET.SubElement(net, "arc", {"id": f"arc_{source}_to_{target}", "source": source, "target": target})
            inscription = ET.SubElement(arc_elem, "inscription")
            text = ET.SubElement(inscription, "text")
            text.text = weight

    # Calculate initial tokens for places based on outbound arc weights
    initial_tokens = [sum(abs(matrix[i][j]) for j in range(num_transitions) if matrix[i][j] < 0) for i in range(num_places)]

    # Setting initial markings for places
    for place_id, initial_token in zip(places, initial_tokens):
        if initial_token > 0:
            place_elem = net.find("./place[@id='{}']".format(place_id))
            initial_marking = ET.SubElement(place_elem, "initialMarking")
            text = ET.SubElement(initial_marking, "text")
            text.text = str(initial_token)

    # Generating PNML file
    tree = ET.ElementTree(pnml)
    xml_str = minidom.parseString(ET.tostring(pnml)).toprettyxml(indent="    ", encoding="UTF-8")
    with open("output_petri.pnml", "wb") as f:
        f.write(xml_str)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python winc2petri_pnml.py \"[[-1, 1], [1, -1], [0, 0]]\"")
        sys.exit(1)
    
    matrix_str = sys.argv[1]
    matrix = parse_matrix(matrix_str)
    generate_petri_pnml(matrix)