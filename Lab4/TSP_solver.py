import math
import random
import time
import os

def distance(city1, city2):
    return math.sqrt((city1[0]-city2[0])**2+(city1[1]-city2[1])**2)

def td(tour):
    return sum(distance(tour[i], tour[(i+1) % len(tour)]) for i in range(len(tour)))

def simulated_annealing(cities,temperature=10000,cooling_rate=0.999,st=1e-8,maxiter=1000000):
    ct=cities[:]
    bt=ct[:]
    n = len(cities)

    iteration = 1
    while temperature > st and iteration < maxiter:
        [i, j] = sorted(random.sample(range(n), 2))
        new_tour = ct[:]
        new_tour[i:j+1] = reversed(new_tour[i:j+1])
        current_distance = td(ct)
        new_distance = td(new_tour)
        if new_distance < current_distance:
            ct = new_tour
            if new_distance < td(bt):
                bt = new_tour
        elif random.random() < math.exp((current_distance - new_distance) / temperature):
            ct = new_tour
        temperature *= cooling_rate
        iteration += 1
    return bt, td(bt)

def read_tsp_file(file_path):
    cities = []
    with open(file_path, 'r') as file:
        reading_coords = False
        for line in file:
            if "NODE_COORD_SECTION" in line:
                reading_coords = True
                continue
            if reading_coords:
                if line.strip() == "EOF":
                    break
                parts = line.strip().split()
                if len(parts) == 3 and parts[0].isdigit():
                    cities.append((float(parts[1]), float(parts[2])))
    if not cities:
        print(f"No cities found in {file_path}.")
    return cities

def solve_tsp(name, cities):
    start_time = time.time()
    _,best_distance = simulated_annealing(cities)
    end_time = time.time()

    print(f"Problem: {name}")
    print(f"Number of cities: {len(cities)}")
    print(f"Best distance found: {best_distance:.2f}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print("--------------------")

    return best_distance, end_time - start_time

tsp_files = [
    "/content/bcl380.tsp",
    "/content/pbk411.tsp",
    "/content/pbl395.tsp",
    "/content/pbm436.tsp",
    "/content/pbn423.tsp",
]

results = {}

for tsp_file in tsp_files:
    if os.path.exists(tsp_file):
        cities = read_tsp_file(tsp_file)
        if cities:
            name = os.path.splitext(tsp_file)[0]
            results[name] = solve_tsp(name, cities)
    else:
        print(f"File not found: {tsp_file}")

print("\nSummary of results:")
for name, (distance, time) in results.items():
    print(f"{name}: Distance = {distance:.2f}, Time = {time:.2f}s")