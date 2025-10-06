import math
import random
import time

def distance(city1, city2):
    return math.sqrt((city1[0]-city2[0])**2+(city1[1]-city2[1])**2)

def td(tour):
    return sum(distance(tour[i], tour[(i+1) % len(tour)]) for i in range(len(tour)))

def simulated_annealing(cities,temperature=10000,cooling_rate=0.995,st=1e-8,maxiter=1000000):
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

cities = [
    ("Jaipur",(26.9124, 75.7873)),
    ("Udaipur", (24.5854, 73.6684)),
    ("Jodhpur", (26.2389, 73.122)),
    ("Ajmer", (26.4499, 74.6399)),
    ("Bikaner", (28.0229, 73.3120)),
    ("Pushkar", (26.4851, 74.6100)),
    ("Chittorgarh", (24.8796, 74.6293)),
    ("Jaisalmer", (26.9157, 70.9160)),
    ("Mount Abu", (24.5921, 72.7014)),
    ("Sikar", (27.6106, 75.1393)),
    ("Neemrana", (27.9852, 76.4577)),
    ("Kota", (25.1638, 75.8644)),
    ("Tonk", (26.0899, 75.7889)),
    ("Barmer", (25.7410, 71.4280)),
    ("Bundi", (25.4472, 75.6306)),
    ("Bikaner", (26.1865, 75.0499)),
    ("Sawai Madhopur",(26.0252, 76.3397)),
    ("Fatehpur Sikri", (27.0977, 77.6616)),
    ("Bhilwara", (26.5290, 74.6100)),
    ("Mandawa", (27.1500, 75.2520)),
    ("Jhalawar", (23.5867, 76.1632))
]

city_coordinates = [city[1] for city in cities]

start_time = time.time()
best_tour, best_distance = simulated_annealing(city_coordinates)
end_time = time.time()

print(f"Number of cities: {len(city_coordinates)}")
print(f"Best distance found: {best_distance:.2f}")
print(f"Time taken: {end_time - start_time:.2f} seconds")