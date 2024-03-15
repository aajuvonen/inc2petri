import sys
import xml.etree.ElementTree as ET

def parse_matrix(matrix_str):
    matrix = eval(matrix_str)
    return matrix

def generate_petri_pnml(matrix):
    num_places = len(matrix)
    num_transitions = len(matrix[0])
    places = [f"v_{i+1}" for i in range(num_places)]
    transitions = [f"T_{j+1}" for j in range(num_transitions)]
    arcs = []
    for i in range(num_places):
        for j in range(num_transitions):
            if matrix[i][j] != 0:
                if matrix[i][j] > 0:
                    arcs.append((transitions[j], places[i]))
                else:
                    arcs.append((places[i], transitions[j]))
    
    # Creating PNML structure
    pnml = ET.Element("pnml")
    net = ET.SubElement(pnml, "net", {"id": "information_warfare", "type": "http://www.pnml.org/version-2009/grammar/ptnet"})
    
    # Adding places
    for place_id in places:
        place = ET.SubElement(net, "place", {"id": place_id})
        if any(place_id == arc[0] for arc in arcs):
            initial_marking = ET.SubElement(place, "initialMarking")
            text = ET.SubElement(initial_marking, "text")
            text.text = "1"
    
    # Adding transitions
    for transition_id in transitions:
        ET.SubElement(net, "transition", {"id": transition_id})
    
    # Adding arcs
    for arc in arcs:
        source, target = arc
        ET.SubElement(net, "arc", {"id": f"arc_{source}_to_{target}", "source": source, "target": target})
    
    # Generating PNML file
    tree = ET.ElementTree(pnml)
    tree.write("output_petri.pnml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python winc2petri_pnml.py \"[[-1, 1], [1, -1], [0, 0]]\"")
        sys.exit(1)
    
    matrix_str = sys.argv[1]
    matrix = parse_matrix(matrix_str)
    generate_petri_pnml(matrix)