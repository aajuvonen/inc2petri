import sys

def parse_matrix(matrix_str):
    matrix = eval(matrix_str)
    return matrix

def generate_petri_tex(matrix):
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

    # Determine places with arcs leading from them
    initial_marking = set()
    for arc in arcs:
        initial_marking.add(arc[0])

    # Creating LaTeX representation
    petri_tex = "\\begin{align*}\n"
    petri_tex += "    N & = (P, T, F, W, M_0) \\\\\n"
    petri_tex += "    P & = \\{" + ", ".join(places) + "\\} \\\\\n"
    petri_tex += "    T & = \\{" + ", ".join(transitions) + "\\} \\\\\n"
    petri_tex += "    F & = \\{" + ", ".join([f"({arc[0]}, {arc[1]})" for arc in arcs]) + "\\} \\\\\n"
    petri_tex += "    W & = \\{1\\} \\\\\n"
    petri_tex += "    M_0 & = (" + ", ".join(["1" if place in initial_marking else "0" for place in places]) + ") \n"
    petri_tex += "\\end{align*}"
    
    return petri_tex

def save_to_tex(petri_tex):
    with open("output_petri.tex", "w") as file:
        file.write(petri_tex)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python winc2petri_tex.py \"[[-1, 1], [1, -1], [0, 0]]\"")
        sys.exit(1)
    
    matrix_str = sys.argv[1]
    matrix = parse_matrix(matrix_str)
    petri_tex = generate_petri_tex(matrix)
    save_to_tex(petri_tex)