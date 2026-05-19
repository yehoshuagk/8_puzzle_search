Expense 8 Puzzle Search
Python version 3.13.2

Structure:
I defined nodes and problems as classes that are then called in the graph search function.

There is a simple read_text function to place the start and goal text files into arrays.

Heuristic_fn finds the location of a tile's value in the start array compared to the location of the same value in the goal's array, then uses the manhattan distance 
to get an admissable heuristic.

Successor_fn is a nested loop used to locate the blank, which then determines the allotted movements in the array based on its index.
A copy of the state is made, a tile is made for blank's new location, a swap is made between the blank's tile and the tile of the other state's value, and a new node who's state carries the new
location of blank is appended to a list of valid successors. 

4 get_x functions to help my fringe in graph search to easily sort nodes based on whatever strategy

graph_search simply follows the class psuedocode through the classes and functions explained earlier.
A closed set and start node is created, along with a fringe that immediately appends the start node. The fringe continues to pop
nodes in strategy-determined order until the there is a node who's state is aligned with the array of the goal's.
Information about the nodes and fringe are all generated throughout the process.

Compile:
My code follows the standard structure asked in the rubric.
"python expense_8_puzzle.py start.txt goal.txt method dump-flag" to start the code.
Method and dump are optional, a* is the default for method if not specified and false is the the default if dump is not specified. 
Also handles when method is not specified and dump is.

Extra Notes:
Utilized python's sort() function for the different fringe pop strategies, using the key based on what parameter each strategy
prioritizes. For DFS, simply reversed the sort so the largest depth was at the front of the fringe to be popped. 

Have recursion limit issues with DFS's dump file. UCS and DFS files take up a lot of space, so I figured it is not a big deal as long as the dump file
still works as intended.
