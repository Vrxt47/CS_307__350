import time
import heapq

class Node:
    def __init__(self, state, parent=None, action=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

goal_state = [
    [2,2,0,0,0,2,2],
    [2,2,0,0,0,2,2],
    [0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0],
    [2,2,0,0,0,2,2],
    [2,2,0,0,0,2,2]
]

initial_state = [
    [2, 2, 1, 1, 1, 2, 2],
    [2, 2, 1, 1, 1, 2, 2],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [2, 2, 1, 1, 1, 2, 2],
    [2, 2, 1, 1, 1, 2, 2]
]


def h1(state):
    return sum(row.count(1) for row in state)

def h2(state):
    td = 0
    for x in range(7):
        for y in range(7):
            if state[x][y] == 1:
                td+= abs(x-3) + abs(y-3)
    return td

def succesor(node, heuristic):
    successors = []
    dm = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    mm = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for x in range(7):
        for y in range(7):
            if node.state[x][y] == 1:
                for d in range(4):
                    nx,ny = x + dm[d][0], y + dm[d][1]
                    midx,midy = x + mm[d][0], y + mm[d][1]

                    if 0 <= nx < 7 and 0 <= ny < 7 and node.state[midx][midy] == 1 and node.state[nx][ny] == 0:
                        ns = [row[:] for row in node.state]
                        ns[x][y] = 0
                        ns[midx][midy] = 0
                        ns[nx][ny] = 1
                        child_node = Node(ns, node, action=[(x, y),(nx,ny)],g=node.g + 1, h=heuristic(ns))
                        successors.append(child_node)
    return successors

def a_star_search(initial_state,heuristic):
    initial_node = Node(initial_state)
    frontier = []
    explored = set()

    initial_node.h=heuristic(initial_node.state)
    heapq.heappush(frontier,initial_node)

    while frontier:
        current_node = heapq.heappop(frontier)

        if (current_node.state==goal_state):
            print("Search completed")
            return current_node

        explored.add(str(current_node.state))

        for child in succesor(current_node, heuristic):
            if str(child.state) not in explored:
                child.h = heuristic(child.state)
                heapq.heappush(frontier, child)

    return None

def eact(node):
    actions=[]
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    return actions[::-1]



print("A* search started with heuristic one")
start_time=time.time()
result_node=a_star_search(initial_state, h1)
end_time=time.time()


if result_node:
    print("Total cost:", result_node.f)
    print("time:",end_time - start_time)
    print("Moves:")
    moves = eact(result_node)
    for move in moves:
        print(move)
else:
    print("No solution found.")

print("\nA* search started with heuristic two")
start_time = time.time()
result_node = a_star_search(initial_state,h2)
end_time = time.time()


if result_node:
    print("Total cost:",result_node.f)
    print("time:",end_time-start_time)
    print("Moves:")
    moves = eact(result_node)
    for move in moves:
        print(move)
else:
    print("No solution found.")