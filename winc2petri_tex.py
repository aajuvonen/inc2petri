import sys

def parse_matrix(matrix_str):
    matrix = eval(matrix_str)
    return matrix

def generate_petri_tex(matrix):
    num_places = len(matrix)
    num_transitions = len(matrix[0])
    places = [f"v_{i+1}" for i in range(num_places)]
    transitions = [f"e_{j+1}" for j in range(num_transitions)]
    arcs = []
    weights = []
    for i in range(num_places):
        for j in range(num_transitions):
            weight = matrix[i][j]
            if weight != 0:
                if weight > 0:
                    arcs.append((transitions[j], places[i]))
                else:
                    arcs.append((places[i], transitions[j]))
                weights.append(abs(weight))

    # Determine initial marking based on the sum of weights of outbound arcs
    initial_marking = {}
    for arc in arcs:
        place = arc[0]
        weight = weights[arcs.index(arc)]
        if place in initial_marking:
            initial_marking[place] += weight
        else:
            initial_marking[place] = weight

    # Creating LaTeX representation
    petri_tex = "\\begin{align*}\n"
    petri_tex += "    N & = (P, T, F, W, M_0) \\\\\n"
    petri_tex += "    P & = (" + ", ".join(places) + ") \\\\\n"
    petri_tex += "    T & = (" + ", ".join(transitions) + ") \\\\\n"
    petri_tex += "    F & = (" + ", ".join([f"({arc[0]}, {arc[1]})" for arc in arcs]) + ") \\\\\n"
    petri_tex += "    W & = (" + ", ".join(map(str, weights)) + ") \\\\\n"
    petri_tex += "    M_0 & = (" + ", ".join([str(initial_marking.get(place, 0)) for place in places]) + ") \n"
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