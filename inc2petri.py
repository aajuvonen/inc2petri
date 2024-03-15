import numpy as np
from sympy import latex

def incidence_matrix_to_petri_net(incidence_matrix):
    """Converts an incidence matrix to a Petri net."""
    pre, post = np.where(incidence_matrix > 0), np.where(incidence_matrix < 0)
    places = set(pre[0]) | set(post[0])
    transitions = set(pre[1]) | set(post[1])

    petri_net = {
        'places': places,
        'transitions': transitions,
        'input_arcs': [(pre[0][i], pre[1][i]) for i in range(len(pre[0]))],
        'output_arcs': [(post[0][i], post[1][i]) for i in range(len(post[0]))]
    }

    return petri_net

def petri_net_to_latex(petri_net):
    """Generates LaTeX code for typesetting the Petri net."""
    places = list(petri_net['places'])
    transitions = list(petri_net['transitions'])
    input_arcs = petri_net['input_arcs']
    output_arcs = petri_net['output_arcs']

    latex_code = "\\begin{tikzpicture}[node distance=2cm,>=stealth,thick,place/.style={circle,draw,minimum size=8mm,inner sep=0pt}]"

    # Places (Nodes)
    for i, place in enumerate(places):
        if i == 0:
            latex_code += f"\n\\node [place,tokens=1] (v{place+1}) {{$v_{place+1}$}};"
        else:
            latex_code += f"\n\\node [place,right=of v{places[i-1]+1}] (v{place+1}) {{$v_{place+1}$}};"
    
    # Transitions
    for transition in transitions:
        latex_code += f"\n\\node [transition,below=1cm of v{transition+1}] (T{transition}) {{$T_{{{transition+1}{transition+2}}}$}};"
    
    # Arcs
    for arc in input_arcs:
        weight = incidence_matrix[arc[0], arc[1]]
        latex_code += f"\n\\draw [->] (v{arc[0]+1}) -- (T{arc[1]}) node[midway,left] {{{weight}}};"
    
    for arc in output_arcs:
        weight = incidence_matrix[arc[0], arc[1]]
        latex_code += f"\n\\draw [->] (T{arc[1]}) -- (v{arc[0]+1}) node[midway,left] {{{weight}}};"
    
    latex_code += "\n\\end{tikzpicture}"
    return latex_code

if __name__ == "__main__":
    import sys

    # Check if a matrix is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python script.py '[[...], [...], ...]'")
        sys.exit(1)

    # Parse the incidence matrix from the command line argument
    try:
        incidence_matrix = np.array(eval(sys.argv[1]))
    except Exception as e:
        print("Error parsing incidence matrix:", e)
        sys.exit(1)

    # Convert incidence matrix to Petri net
    petri_net = incidence_matrix_to_petri_net(incidence_matrix)

    # Generate LaTeX code for the Petri net
    latex_code = petri_net_to_latex(petri_net)

    print(latex_code)