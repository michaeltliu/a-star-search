## a-star-search
Visualize the A* search algorithm performed on randomly generated terrain

Requires pygame. Install using `pip install pygame`

Then: `python3 game.py`

Heuristic static weighting, grid size, and animation speed are adjustable at the top of the code

Apparently Euclidean distance being a consistent heuristic doesn't allow me to forgo a minimum path length map for visited nodes. Maybe it did but I didn't check closely enough. Oh well, safe > sorry

Sometimes the random terrain makes it impossible to reach the target. If the map is especially large, it might be best to interrupt out early and try again. (Given grid dimensions n by n and obstacle density p, what's the probability of a viable path? Percolation but easier?)