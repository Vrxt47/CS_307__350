import heapq
import time

class Node:
    def __init__(self, state, parent=None, action=None, g=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g

    def __lt__(self, other):
        return self.g < other.g

initial_state = [
    [2, 2, 1, 1, 1, 2, 2],
    [2, 2, 1, 1, 1, 2, 2],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [2, 2, 1, 1, 1, 2, 2],
    [2, 2, 1, 1, 1, 2, 2]
]

goal_state = [
    [2, 2, 0, 0, 0, 2, 2],
    [2, 2, 0, 0, 0, 2, 2],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [2, 2, 0, 0, 0, 2, 2],
    [2, 2, 0, 0, 0, 2, 2]
]

total_nodes_expanded = 0

def heuristic(state):
    return sum(row.count(1) for row in state)

def get_successors(node):
    successors = []
    state = node.state
    move_deltas = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    jump_deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for r in range(7):
        for c in range(7):
            if state[r][c] == 1:
                for i in range(4):
                    to_r, to_c = r + move_deltas[i][0], c + move_deltas[i][1]
                    jumped_r, jumped_c = r + jump_deltas[i][0], c + jump_deltas[i][1]

                    if 0 <= to_r < 7 and 0 <= to_c < 7 and \
                       state[jumped_r][jumped_c] == 1 and state[to_r][to_c] == 0:

                        new_state = [row[:] for row in state]
                        new_state[r][c] = 0
                        new_state[jumped_r][jumped_c] = 0
                        new_state[to_r][to_c] = 1

                        child_node = Node(new_state, node, action=((r, c), (to_r, to_c)), g=node.g + 1)
                        successors.append(child_node)
    return successors

def best_first_search():
    global total_nodes_expanded
    total_nodes_expanded = 0

    frontier = []
    explored = set()

    start_node = Node(initial_state, g=0)
    h_value = heuristic(start_node.state)
    heapq.heappush(frontier, (h_value, start_node))

    while frontier:
        _, current_node = heapq.heappop(frontier)
        total_nodes_expanded += 1

        if current_node.state == goal_state:
            return current_node

        state_str = str(current_node.state)
        if state_str in explored:
            continue

        explored.add(state_str)

        for child in get_successors(current_node):
            if str(child.state) not in explored:
                child_h = heuristic(child.state)
                heapq.heappush(frontier, (child_h, child))

    return None

def extract_path(node):
    actions = []
    current = node
    while current.parent is not None:
        actions.append(current.action)
        current = current.parent
    return actions[::-1]

def print_board(state):
    char_map = {1: 'o', 0: '.', 2: ' '}
    for row in state:
        print(" ".join(char_map[cell] for cell in row))

if __name__ == '__main__':
    print("--- Initial Board ---")
    print_board(initial_state)
    print("\nStarting Best-First Search...")

    start_time = time.time()
    result_node = best_first_search()
    end_time = time.time()

    if result_node:
        print("\n--- Solution Found! ---")
        print(f"Time Taken: {end_time - start_time:.2f} seconds")
        print(f"Nodes Expanded: {total_nodes_expanded}")
        print(f"Path Length: {result_node.g} moves")
        print("\n--- Final Board ---")
        print_board(result_node.state)

        print("\n--- Moves ---")
        moves = extract_path(result_node)
        for i, move in enumerate(moves):
            print(f"Move {i+1}: Jump from {move[0]} to {move[1]}")
    else:
        print("\n--- No solution found. ---")