import random

def generate_k_sat(k, n, m):
    if k > n:
        print(f"Error: k ({k}) cannot be greater than n ({n}).")
        return []

    formula = []
    all_variables = list(range(1, n + 1))

    for _ in range(m):
        clause_variables = random.sample(all_variables, k)

        new_clause = []
        for var in clause_variables:
            if random.choice([True, False]):
                new_clause.append(var)
            else:
                new_clause.append(-var)

        formula.append(new_clause)

    return formula

if __name__ == "__main__":
    K_val = 3
    N_vars = 10
    M_clauses = 20

    problem_instance = generate_k_sat(K_val, N_vars, M_clauses)

    if problem_instance:
        print(f"Generated a {K_val}-SAT problem with {N_vars} variables and {M_clauses} clauses:")
        for i, clause in enumerate(problem_instance):
            print(f"Clause {i+1}: {clause}")
