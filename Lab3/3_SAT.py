import string
import random
import copy
import numpy as np

def make_formula(num_clauses, num_vars):
    if 3 > num_vars:
        print(f"Error: A 3-SAT clause requires at least 3 variables (n={num_vars} is too small).")
        return [], []
    l_vars = list(string.ascii_lowercase[:num_vars])
    u_vars = [v.upper() for v in l_vars]
    all_literals = l_vars + u_vars
    formula = []
    for _ in range(num_clauses):
        chosen_vars = random.sample(l_vars, 3)
        clause = [var if random.choice([True, False]) else var.upper() for var in chosen_vars]
        formula.append(sorted(clause))
    return formula, all_literals

def make_assignment(literals, num_vars):
    l_assign = list(np.random.choice(2, num_vars))
    u_assign = [1 - val for val in l_assign]
    return dict(zip(literals, l_assign + u_assign))

def eval_formula(formula, assignment):
    return sum(any(assignment[literal] for literal in clause) for clause in formula)

def hill_climbing(formula, assignment, prev_score, found_step, total_steps):
    best_assignment = assignment.copy()
    max_score = prev_score
    best_neighbor_assignment = assignment.copy()
    for literal in list(assignment.keys()):
        if not literal.islower():
            continue
        total_steps += 1
        temp_assignment = assignment.copy()
        temp_assignment[literal] = 1 - temp_assignment[literal]
        temp_assignment[literal.upper()] = 1 - temp_assignment[literal.upper()]
        score = eval_formula(formula, temp_assignment)
        if score > max_score:
            max_score = score
            best_neighbor_assignment = temp_assignment.copy()
            found_step = total_steps
    if max_score == prev_score:
        return best_assignment, max_score, f"{found_step}/{total_steps}"
    return hill_climbing(formula, best_neighbor_assignment, max_score, found_step, total_steps)

def beam_search(formula, assignment, beam_width, steps):
    if eval_formula(formula, assignment) == len(formula):
        return assignment, f"{steps}/{steps}"
    candidates = []
    for literal in list(assignment.keys()):
        if not literal.islower():
            continue
        steps += 1
        new_assignment = assignment.copy()
        new_assignment[literal] = 1 - new_assignment[literal]
        new_assignment[literal.upper()] = 1 - new_assignment[literal.upper()]
        score = eval_formula(formula, new_assignment)
        candidates.append((new_assignment, score, steps))
    best_in_beam = sorted(candidates, key=lambda x: x[1])[-beam_width:]
    for state, score, step_count in best_in_beam:
        if score == len(formula):
            return state, f"{step_count}/{steps}"
    best_next_state = best_in_beam[-1][0]
    return beam_search(formula, best_next_state, beam_width, steps)

def variable_neighborhood_search(formula, assignment, neighborhood_size, steps):
        if eval_formula(formula, assignment) == len(formula):
            return assignment, f"{steps}/{steps}", neighborhood_size
        candidates = []
        for literal in list(assignment.keys()):
            if not literal.islower():
                continue
            steps += 1
            new_assignment = assignment.copy()
            new_assignment[literal] = 1 - new_assignment[literal]
            new_assignment[literal.upper()] = 1 - new_assignment[literal.upper()]
            score = eval_formula(formula, new_assignment)
            candidates.append((new_assignment, score, steps))
        best_neighbors = sorted(candidates, key=lambda x: x[1])[-neighborhood_size:]
        for state, score, step_count in best_neighbors:
            if score == len(formula):
                return state, f"{step_count}/{steps}", neighborhood_size
        best_next_state = best_neighbors[-1][0]
        return variable_neighborhood_search(formula, best_next_state, neighborhood_size + 1, steps)

def run_solvers():
    try:
        num_clauses = int(input("Enter the number of clauses (m): "))
        num_vars = int(input("Enter the number of variables (n): "))
        print("-" * 30)
        formula, literals = make_formula(num_clauses, num_vars)
        if not formula:
            return
        print(f"Generated a 3-SAT problem with {num_vars} variables and {num_clauses} clauses.")
        initial_assignment = make_assignment(literals, num_vars)
        initial_score = eval_formula(formula, initial_assignment)
        print(f"Initial Random Assignment Score: {initial_score}/{len(formula)}")
        print("-" * 30)
        _, hc_score, hc_penetrance = hill_climbing(formula, initial_assignment.copy(), initial_score, 1, 1)
        print(f"Hill-Climbing:\n  - Final Score: {hc_score}\n  - Penetrance (steps to best / total steps): {hc_penetrance}")
        bs_assignment, bs_penetrance = beam_search(formula, initial_assignment.copy(), 3, 1)
        bs_score = eval_formula(formula, bs_assignment)
        print(f"\nBeam Search (w=3):\n  - Final Score: {bs_score}\n  - Penetrance: {bs_penetrance}")
        vnd_assignment, vnd_penetrance, final_n = variable_neighborhood_search(formula, initial_assignment.copy(), 1, 1)
        vnd_score = eval_formula(formula, vnd_assignment)
        print(f"\nVariable Neighborhood Search:\n  - Final Score: {vnd_score}\n  - Penetrance: {vnd_penetrance}\n  - Final Neighborhood Size: {final_n}")
    except (ValueError, IndexError):
        print("Invalid input. Please enter valid integers. Ensure n >= 3.")

if __name__ == "__main__":
    run_solvers()
