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
                    arcs.append(f"({places[i]}, {transitions[j]})")
                else:
                    arcs.append(f"({transitions[j]}, {places[i]})")
    
    # Generating 5-tuple in LaTeX format
    initial_marking = [f"1" if any(place in arc for arc in arcs) else "0" for place in places]
    petri_tex = r"""\begin{align*}
    N & = (P, T, F, W, M_0) \\
    P & = \{""" + ', '.join(places) + r"""\} \\
    T & = \{""" + ', '.join(transitions) + r"""\} \\
    F & = \{""" + ', '.join(arcs) + r"""\} \\
    W & = \{1\} \\
    M_0 & = \{""" + ', '.join(initial_marking) + r"""\}
\end{align*}"""
    
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