from collections import deque

def get_successors(state):
    successors = []
    s = list(state)

    try:
        empty_idx = s.index('_')
    except ValueError:
        return []

    # East slide
    if empty_idx > 0 and s[empty_idx - 1] == 'E':
        new_s = s[:]
        new_s[empty_idx], new_s[empty_idx - 1] = new_s[empty_idx - 1], new_s[empty_idx]
        successors.append(tuple(new_s))

    # West slide
    if empty_idx < len(s) - 1 and s[empty_idx + 1] == 'W':
        new_s = s[:]
        new_s[empty_idx], new_s[empty_idx + 1] = new_s[empty_idx + 1], new_s[empty_idx]
        successors.append(tuple(new_s))

    # East jump
    if empty_idx > 1 and s[empty_idx - 2] == 'E':
        new_s = s[:]
        new_s[empty_idx], new_s[empty_idx - 2] = new_s[empty_idx - 2], new_s[empty_idx]
        successors.append(tuple(new_s))

    # West jump
    if empty_idx < len(s) - 2 and s[empty_idx + 2] == 'W':
        new_s = s[:]
        new_s[empty_idx], new_s[empty_idx + 2] = new_s[empty_idx + 2], new_s[empty_idx]
        successors.append(tuple(new_s))

    return successors


def solve_with_bfs(start_state, goal_state):
    queue = deque([[start_state]])
    visited = {start_state}

    while queue:
        path = queue.popleft()
        current_state = path[-1]

        if current_state == goal_state:
            return path

        for successor in get_successors(current_state):
            if successor not in visited:
                visited.add(successor)
                queue.append(path + [successor])

    return None


# --- Main ---
initial_state = ('E', 'E', 'E', '_', 'W', 'W', 'W')
goal_state = ('W', 'W', 'W', '_', 'E', 'E', 'E')

solution_path = solve_with_bfs(initial_state, goal_state)

if solution_path:
    print("Optimal solution found! The sequence of steps is:\n")
    for i, state in enumerate(solution_path):
        print(f"Step {i:2d}: {' '.join(state)}")
    print(f"\nThis solution is optimal and requires {len(solution_path) - 1} steps.")
else:

    print("No solution was found.")
