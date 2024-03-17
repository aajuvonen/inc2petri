# inc2petri – Scripts for creation of Petri nets from incidence matrices 

This repository has a set of helper scripts developed with the assistance of OpenAI's language model.

`mat2py.m` converts Octave matrices into Python's string matrix format.

`wadj2winc.m` converts weighted adjacency matrices into weighted incidence matrices.

`winc2petri_tex.py` takes as input weighted incidence matrices of digraphs, and outputs in LaTex a 5-tuple Petri net $ N = (P, T, F, W, M_0)$ such that the initial marking of places is the sum of outbound arc's weights for each node.

`winc2petri_pnml.py` takes as input weighted incidence matrices of digraphs, and outputs a Petri net in PNML file format compatible with for example [Fachpraktikum Programmiersysteme WiSe23/24](https://www.fernuni-hagen.de/ilovepetrinets/fapra/wise23/blau/index.html).

## Usage

```python winc2petri_tex.py "[[-1, 1], [1, -1], [0, 0]]"```

```python winc2petri_pnml.py "[[-1, 1], [1, -1], [0, 0]]"```

## License

MIT license. Read more in LICENSE.md