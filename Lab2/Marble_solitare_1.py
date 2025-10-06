import heapq
import time

#It's impossible to solve with this on collab
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost < other.path_cost

initial_state = (
    (-1, -1, 1, 1, 1, -1, -1),
    (-1, -1, 1, 1, 1, -1, -1),
    ( 1,  1, 1, 1, 1,  1,  1),
    ( 1,  1, 1, 0, 1,  1,  1),
    ( 1,  1, 1, 1, 1,  1,  1),
    (-1, -1, 1, 1, 1, -1, -1),
    (-1, -1, 1, 1, 1, -1, -1),
)

total_nodes_expanded = 0

def is_goal_state(state):
    marble_count = sum(row.count(1) for row in state)
    return marble_count == 1 and state[3][3] == 1

def get_successors(node):
    successors = []
    state = node.state
    for r in range(7):
        for c in range(7):
            if state[r][c] == 1:
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    jumped_r, jumped_c = r + dr, c + dc
                    to_r, to_c = r + 2 * dr, c + 2 * dc

                    if 0 <= to_r < 7 and 0 <= to_c < 7 and \
                       state[to_r][to_c] != -1 and \
                       state[jumped_r][jumped_c] == 1 and \
                       state[to_r][to_c] == 0:

                        new_state_list = [list(row) for row in state]
                        new_state_list[r][c] = 0
                        new_state_list[jumped_r][jumped_c] = 0
                        new_state_list[to_r][to_c] = 1
                        new_state = tuple(map(tuple, new_state_list))

                        child_node = Node(new_state, node, action=((r, c), (to_r, to_c)), path_cost=node.path_cost + 1)
                        successors.append(child_node)
    return successors

def uniform_cost_search():
    global total_nodes_expanded
    total_nodes_expanded = 0

    start_node = Node(state=initial_state, path_cost=0)
    frontier = [(start_node.path_cost, start_node)]
    explored = set()

    while frontier:
        priority, current_node = heapq.heappop(frontier)
        total_nodes_expanded += 1

        if is_goal_state(current_node.state):
            return current_node

        if current_node.state in explored:
            continue

        explored.add(current_node.state)

        for child in get_successors(current_node):
            if child.state not in explored:
                heapq.heappush(frontier, (child.path_cost, child))

    return None

def extract_path(node):
    actions = []
    current = node
    while current.parent is not None:
        actions.append(current.action)
        current = current.parent
    return actions[::-1]

def print_board(state):
    char_map = {1: 'o', 0: '.', -1: ' '}
    for row in state:
        print(" ".join(char_map[cell] for cell in row))

if __name__ == '__main__':
    print("--- Initial Board ---")
    print_board(initial_state)
    print("\nStarting Uniform Cost Search...")

    start_time = time.time()
    result_node = uniform_cost_search()
    end_time = time.time()

    if result_node:
        print("\n--- Solution Found! ---")
        print(f"Time Taken: {end_time - start_time:.2f} seconds")
        print(f"Nodes Expanded: {total_nodes_expanded}")
        print(f"Path Length: {result_node.path_cost} moves")
        print("\n--- Final Board ---")
        print_board(result_node.state)

        print("\n--- Moves ---")
        moves = extract_path(result_node)
        for i, move in enumerate(moves):
            print(f"Move {i+1}: Jump from {move[0]} to {move[1]}")
    else:
        print("\n--- No solution found. ---")
