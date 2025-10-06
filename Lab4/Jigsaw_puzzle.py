import random
import math
import numpy as np
import scipy.io
import sys

BLOCKS_PER_SIDE = 15
BLOCK_SIZE = 225 // BLOCKS_PER_SIDE

def cost_function(puzzle):
    cost = 0
    for i in range(225):
        for j in range(225):
            if j + 1 != 225 and (j + 1) % BLOCK_SIZE == 0:
                cost += abs(int(puzzle[225*i + j]) - int(puzzle[225*i + j + 1]))
            if i + 1 != 225 and (i + 1) % BLOCK_SIZE == 0:
                cost += abs(int(puzzle[225*i + j]) - int(puzzle[225*(i+1) + j]))
    return cost

def swap_pieces(puzzle):
    i, j = random.sample(range(BLOCKS_PER_SIDE**2), 2)
    r1, r2 = i // BLOCKS_PER_SIDE, j // BLOCKS_PER_SIDE
    c1, c2 = i % BLOCKS_PER_SIDE, j % BLOCKS_PER_SIDE
    rn1, rn2 = BLOCK_SIZE * r1, BLOCK_SIZE * r2
    cn1, cn2 = BLOCK_SIZE * c1, BLOCK_SIZE * c2
    piece1 = []
    piece2 = []
    for x in range(BLOCK_SIZE):
        for y in range(BLOCK_SIZE):
            piece1.append(puzzle[225*(rn1 + x) + (cn1 + y)])
            piece2.append(puzzle[225*(rn2 + x) + (cn2 + y)])
    for x in range(BLOCK_SIZE):
        for y in range(BLOCK_SIZE):
            puzzle[225*(rn1 + x) + (cn1 + y)] = piece2[x*BLOCK_SIZE + y]
            puzzle[225*(rn2 + x) + (cn2 + y)] = piece1[x*BLOCK_SIZE + y]
    return puzzle

def simulated_annealing(puzzle, T_initial, alpha, stopping_temp):
    T = T_initial
    current_state = puzzle
    current_cost = cost_function(current_state)

    minState = current_state.copy()
    minCost = current_cost

    while T > stopping_temp:
        new_state = swap_pieces(current_state.copy())
        new_cost = cost_function(new_state)

        if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / T):
            current_state = new_state
            current_cost = new_cost

        if current_cost < minCost:
            minCost = current_cost
            minState = current_state.copy()

        T *= alpha

    return minState, minCost

print("Loading .mat file...")
data = scipy.io.loadmat('/content/output.mat')

mat_variable_name = None
for key in data:
    if not key.startswith('__'):
        mat_variable_name = key
        break

if mat_variable_name is None:
    print("Error: Could not find a valid matrix variable in the .mat file.")
    print(f"   Available keys: {data.keys()}")
    sys.exit()

print(f"Found data under variable name: '{mat_variable_name}'")
puzzle_matrix = data[mat_variable_name]
puzzle = puzzle_matrix.flatten().tolist()

print("Solving puzzle with simulated annealing... (This may take a moment)")
T_initial = 1000
alpha = 0.99
stopping_temp = 0.1
solved_puzzle, min_cost = simulated_annealing(puzzle, T_initial, alpha, stopping_temp)

scipy.io.savemat('answer.mat', {mat_variable_name: np.array(solved_puzzle).reshape(225, 225)})

print("\n--- Process Complete! ---")
print(f"Minimum cost found: {min_cost}")
print("Solved puzzle saved to 'answer.mat'")