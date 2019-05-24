N-queen-puzzles with Python3

How this program works

Given an initial configuration, and a search strategy as an input, the program follows a series of states(path) from the initial configuration to the goal state.

EXAMPLE INPUT Initial State : 1,2,3,8,0,2,7,6,5 Goal State: 1,2,3,8,2,7,6,0,5 Strategy: Breath-first

The following strategies was be implemented:

Bounded Depth-first search (depth is provided at input) Iterative Deepening search Breath-first search Best-first (A*) search with each of the following heuristic functions H:

Number of tiles out of place minimum number of moves to reach the goal state (Manhattan distance) heuristic H defined below 2*C where C is the Chebyshev distance (see below)

H is a combination of two measures:

    totdist: the "total distance" of the eight tiles in Pos (Pos is a board position) from their "home squares". We use the Manhattan distance (see below for the definition of the Manhattan distance) to calculate the distance of each tile from its home square. For example, in the starting position of the puzzle (a) in the figure below, totdist = 4.

    seq: the "sequence score" that measures the degree to which the tiles are already ordered in the current position with respect to the order required in the goal configuration. seq is computed as the sum of scores for each tile according to the following rules: a tile in the centre scores 1; a tile on a non-central square scores 0 if the tile is, in the clockwise direction, followed by its proper successor.

    such a tile scores 2 if it is not followed by its proper successor.

For example, for the starting position (a) of the puzzle in the figure below, seq = 6.

The heuristic estimate, H, is computed as:

H = totdist + 3*seq

The "Manhattan distance" between 2 squares S1 and S2 is the distance between S1 and S2 in the horizontal direction (dx) plus the distance between S1 and S2 in the vertical direction (dy). To minimize the length of solutions. Therefore, I define the cost of all the arcs in the state space to equal 1.

The Chebyshev distance, C, is defined as follows (using dx and dy defined above): C = max(dx,dy)
