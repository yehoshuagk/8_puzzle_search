import copy
import sys
from datetime import datetime

sys.setrecursionlimit(10**6)


class Node:
    def __init__(self, state, action = "Start", parent=None, g=0, h=0, d=0):
        self.state = state
        self.action = action
        self.parent = parent
        self.g = g
        self.h = h
        self.d = d
        self.f = g + h

    def __repr__(self):
        return f"< state = {self.state}, action = {self.action}, g(n) = {self.g}, h(n) = {self.h}, d(n) = {self.d}, f(n) = {self.g + self.h}, Parent = Pointer to {self.parent is not None} >"
    

class Problem:
    def __init__ (self, start, goal, successor, heuristic=None):
        self.start = start
        self.goal = goal
        self.successor = successor
        self.heuristic = heuristic


def read_text(filename):
    with open(filename, 'r') as file:
        list = []
        for line in file:
            if line[0].isdigit():
                newline = line.strip()
                temp = []
                split = line.split()
                for i in split:
                    temp.append(int(i))
                list.append(temp)

    return list

def heuristic_fn(state, goal):
    total = 0

    rows = 3
    cols = 3

    for i in range(rows):
        for j in range(cols):
            tile = state[i][j]
            if tile != 0:
                for r in range(rows):
                    for c in range(cols):
                        if goal[r][c] == tile:
                            distance = abs(i - r) + abs(j - c)
                            total += distance * tile
    
    return total 

def successor_fn(state, current_node):
    rows = 3
    cols = 3
    successors = []

    for i in range(rows):
        for j in range(cols):
            if state[i][j] == 0:
                #up
                if i > 0:
                    #do the up swap, create a node, add it to a list of successors 
                    new_state = copy.deepcopy(state)
                    tile = new_state[i-1][j]
                    new_state[i][j] = new_state[i-1][j]
                    new_state[i-1][j] = 0
                    new_node = Node(state=new_state, action=(f"Move {tile} Down"), parent = current_node, g = current_node.g + tile, h = heuristic_fn(new_state, goal_txt), d = current_node.d + 1)
                    successors.append(new_node)

                #down
                if i < rows - 1:
                    new_state = copy.deepcopy(state)
                    tile = new_state[i+1][j]
                    new_state[i][j] = new_state[i+1][j]
                    new_state[i+1][j] = 0
                    new_node = Node(state=new_state, action=(f"Move {tile} Up"), parent = current_node, g = current_node.g + tile, h = heuristic_fn(new_state, goal_txt), d = current_node.d + 1)
                    successors.append(new_node)
                
                #left
                if j > 0:
                    new_state = copy.deepcopy(state)
                    tile = new_state[i][j-1]
                    new_state[i][j] = new_state[i][j-1]
                    new_state[i][j-1] = 0
                    new_node = Node(state=new_state, action = (f"Move {tile} Right"), parent = current_node, g = current_node.g + tile, h = heuristic_fn(new_state, goal_txt), d = current_node.d + 1)
                    successors.append(new_node)

                #right
                if j < cols - 1:
                    new_state = copy.deepcopy(state)
                    tile = new_state[i][j+1]
                    new_state[i][j] = new_state[i][j+1]
                    new_state[i][j+1] = 0
                    new_node = Node(state=new_state, action = (f"Move {tile} Left"), parent = current_node, g = current_node.g + tile, h = heuristic_fn(new_state, goal_txt), d = current_node.d + 1)
                    successors.append(new_node)
        
    return successors 

def get_cost(n):
    return n.g

def get_heur(n):
    return n.h

def get_depth(n):
    return n.d

def get_f(n):
    return n.g + n.h

start_txt = read_text(sys.argv[1])
goal_txt = read_text(sys.argv[2])
method = "a*"


dump = False

"""read the last argument for method and dump
.lower() makes it case insensitive"""
for arg in sys.argv[3:]:
    if arg.lower() in ("-d", "--dump", "true"):
        dump = True
    elif arg.lower() in ("bfs", "dfs", "ucs", "greedy", "a*"):
        method = arg.lower()

print(f"Command-Line Arguments : {sys.argv[1:]}")


prob_h = heuristic_fn(start_txt, goal_txt)
problem1 = Problem(start_txt, goal_txt, successor_fn, heuristic = prob_h)


def graph_search(problem, strategy = "a*"):
    nodes_popped, nodes_expanded, nodes_generated, max_fringe = 0, 0, 0, 0

    #closed <--- an empty set
    closed = set()

    #fringe <-- insert(make-node(INITIAL-STATE[problem]), fringe)
    start_node = Node(state=problem.start, h = heuristic_fn(problem.start, problem.goal))
    
    nodes_generated += 1
    max_fringe += 1


    fringe = []
    fringe.append(start_node)

    dump_file = None
    if dump:
        timestamp = datetime.now().strftime("%m_%d_%Y-%H_%M_%S")
        #safe method is for a*, * character cannot be in filename
        safe_method = method.replace("*", "star")
        dump_file = open(f"trace-{safe_method}-{timestamp}.txt", "w")

        dump_file.write("After Initialization\n")
        dump_file.write(f"\tClosed: {list(closed)}\n")
        dump_file.write(f"\tFringe: {fringe}\n")

        dump_file.write(f"\tNodes Popped: {nodes_popped}\n")
        dump_file.write(f"\tNodes Expanded: {nodes_expanded}\n")
        dump_file.write(f"\tNodes Generated: {nodes_generated}\n")
        dump_file.write(f"\tMax Fringe Size: {max_fringe}\n")

        dump_file.write(f"\tRunning {strategy}\n")
        dump_file.write(f"\tGenerating successors to {start_node}\n")


    #loop do 
    while fringe:
    # if fringe is empty then return failure
        if not fringe:
            return None
        
        #node <--- remove-front(fringe)
        
        if (strategy == "bfs"):
            fringe.sort(key=get_depth)
            node = fringe.pop(0)

        if (strategy == "dfs"):
            fringe.sort(key=get_depth, reverse = True)
            node = fringe.pop(0)
           

        elif (strategy == "ucs"):
            fringe.sort(key=get_cost)
            node = fringe.pop(0)
            

        elif (strategy == "greedy"):
            fringe.sort(key=get_heur)
            node = fringe.pop(0)
          

        elif (strategy == "a*"):
            fringe.sort(key=get_f)
            node = fringe.pop(0)
        
        nodes_popped += 1


        #if GOAL-TEST(problem, STATE[node]) then return node
        if node.state == problem.goal:
            solution_depth = node.d
            solution_cost = node.g
            path = []
            while node.parent is not None:
                path.append(node.action)
                node = node.parent
            path.reverse()

            if dump and dump_file:
                dump_file.close()

            print(f"Nodes Popped: {nodes_popped}")
            print(f"Nodes Expanded: {nodes_expanded}")
            print(f"Nodes Generated: {nodes_generated}")
            print(f"Max Fringe Size: {max_fringe}")

            print(f"Solution Found at depth {solution_depth} with cost of {solution_cost}.")
            print("Steps:")
            for action in path:
                print(f"\t{action}")
            return
        
        if str(node.state) not in closed:
            closed.add(str(node.state))
            nodes_num = successor_fn(node.state, node)
            fringe.extend(nodes_num)
        
            nodes_expanded += 1
            nodes_generated += len(nodes_num)

            size = len(fringe)
            max_fringe = max(max_fringe, len(fringe))

            if dump and dump_file:
                dump_file.write(f"\tRunning: {strategy}\n")
                dump_file.write(f"\tGenerating successors to {node}\n")

                dump_file.write(f"\tNodes Popped: {nodes_popped}\n")
                dump_file.write(f"\tNodes Expanded: {nodes_expanded}\n")
                dump_file.write(f"\tNodes Generated: {nodes_generated}\n")
                dump_file.write(f"\tMax Fringe Size: {max_fringe}\n") 

                dump_file.write(f"\tClosed: {list(closed)}\n")
                dump_file.write(f"\tFringe: {fringe}\n")

    if dump_file:
        dump_file.close()

    return None

graph_search(problem1, method)

        
    



