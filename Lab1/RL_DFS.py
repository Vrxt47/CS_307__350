def get_successors(state):
    successors = []
    s = list(state)
    try:
        empty_idx = s.index('_')
    except ValueError:
        return []

    if empty_idx > 0 and s[empty_idx - 1] == 'E':
        new_s = s[:]
        new_s[empty_idx], new_s[empty_idx - 1] = new_s[empty_idx - 1], new_s[empty_idx]
        successors.append(tuple(new_s))

    if empty_idx < 6 and s[empty_idx + 1] == 'W':
        new_s = s[:]
        new_s[empty_idx], new_s[empty_idx + 1] = new_s[empty_idx + 1], new_s[empty_idx]
        successors.append(tuple(new_s))

    if empty_idx > 1 and s[empty_idx - 2] == 'E':
        new_s = s[:]
        new_s[empty_idx], new_s[empty_idx - 2] = new_s[empty_idx - 2], new_s[empty_idx]
        successors.append(tuple(new_s))

    if empty_idx < 5 and s[empty_idx + 2] == 'W':
        new_s = s[:]
        new_s[empty_idx], new_s[empty_idx + 2] = new_s[empty_idx + 2], new_s[empty_idx]
        successors.append(tuple(new_s))

    return successors

def solve_with_dfs(start_state, goal_state):
    stack = [[start_state]]
    visited = {start_state}

    while stack:
        path = stack.pop()
        current_state = path[-1]

        if current_state == goal_state:
            return path

        for successor in get_successors(current_state):
            if successor not in visited:
                visited.add(successor)
                new_path = path + [successor]
                stack.append(new_path)

    return None

initial_state = ('E', 'E', 'E', '_', 'W', 'W', 'W')
goal_state = ('W', 'W', 'W', '_', 'E', 'E', 'E')

solution_path = solve_with_dfs(initial_state, goal_state)

if solution_path:
    print("Solution found with DFS! The sequence of steps is:\n")
    for i, state in enumerate(solution_path):
        print(f"Step {i:2d}: {' '.join(state)}")
    print(f"\nDFS found a solution with {len(solution_path) - 1} steps.")
    print("Note: This path is not guaranteed to be the shortest one.")
else:
    print("No solution was found.")