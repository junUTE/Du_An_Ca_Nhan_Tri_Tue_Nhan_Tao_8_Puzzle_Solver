from utils import is_solvable
import random

MOVES = [(0,1), (1,0), (0,-1), (-1,0)]

def manhattan(state, goal):
    return sum(abs((val - 1) % 3 - (i % 3)) + abs((val - 1) // 3 - (i // 3))
               for i, val in enumerate(state) if val != 0)

def heuristic(state, goal):
    """Calculate the Manhattan distance heuristic."""
    return sum(abs((val - 1) % 3 - (i % 3)) + abs((val - 1) // 3 - (i // 3))
               for i, val in enumerate(state) if val != 0)

def simple_hill_climbing(start, goal):
    current = start
    path = [start]  # Include start in the path
    expansions = 0

    while current != goal:
        idx = current.index(0)
        row, col = divmod(idx, 3)
        neighbors = []

        for move in MOVES:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                new_state = current[:]
                new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                neighbors.append(new_state)

        # Sort neighbors by heuristic (Manhattan distance)
        neighbors.sort(key=lambda state: heuristic(state, goal))
        expansions += len(neighbors)

        # Choose the best neighbor
        best_neighbor = neighbors[0]
        if heuristic(best_neighbor, goal) >= heuristic(current, goal):
            # No improvement, terminate
            return None, expansions

        current = best_neighbor
        path.append(current)

    return path, expansions

def steepest_ascent_hill_climbing(start, goal):
    """Steepest-Ascent Hill Climbing algorithm."""
    current = start
    path = [start]  # Include start in the path
    expansions = 0

    while current != goal:
        idx = current.index(0)
        row, col = divmod(idx, 3)
        neighbors = []

        # Generate all possible neighbors
        for move in MOVES:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                new_state = current[:]
                new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                neighbors.append(new_state)

        # Sort neighbors by heuristic (Manhattan distance)
        neighbors.sort(key=lambda state: heuristic(state, goal))
        expansions += len(neighbors)

        # Choose the best neighbor
        best_neighbor = neighbors[0]
        if heuristic(best_neighbor, goal) >= heuristic(current, goal):
            # No improvement, terminate
            return None, expansions

        current = best_neighbor
        path.append(current)

    return path, expansions

def Stochastic_hill_Climbing(start, goal):
    current = start
    path = [start]  # Include start in the path
    expansions = 0

    while current != goal:
        idx = current.index(0)
        row, col = divmod(idx, 3)
        neighbors = []
        # Generate all possible neighbors
        for move in MOVES:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                new_state = current[:]
                new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                neighbors.append(new_state)

        # Filter neighbors with better heuristic values
        better_neighbors = [neighbor for neighbor in neighbors if heuristic(neighbor, goal) < heuristic(current, goal)]
        expansions += len(neighbors)

        if not better_neighbors:
            # No better neighbors, terminate
            return None, expansions

        # Randomly select one of the better neighbors
        current = random.choice(better_neighbors)
        path.append(current)

    return path, expansions

def Simulated_Annealing(start, goal):
    current = start
    path = [start]
    expansions = 0
    temperature = 5.0
    cooling_rate = 0.99
    best = current
    best_score = heuristic(current, goal)

    while current != goal and temperature > 0.01:
        idx = current.index(0)
        row, col = divmod(idx, 3)
        neighbors = []

        for move in MOVES:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                new_state = current[:]
                new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                neighbors.append(new_state)

        expansions += len(neighbors)

        if not neighbors:
            return path, expansions  # Return the path even if the goal is not reached

        probabilities = []
        for neighbor in neighbors:
            delta_e = heuristic(current, goal) - heuristic(neighbor, goal)
            if delta_e > 0:
                probabilities.append(1.0)
            else:
                probabilities.append(pow(2.71828, delta_e / temperature))

        total_prob = sum(probabilities)
        probabilities = [p / total_prob for p in probabilities]

        current = random.choices(neighbors, probabilities)[0]
        path.append(current)

        # Update the best state
        h = heuristic(current, goal)
        if h < best_score:
            best = current
            best_score = h

        temperature *= cooling_rate

    if current == goal:
        return path, expansions
    else:
        return path, expansions  # Return the path even if the goal is not reached

def Beam_Search(start, goal, beam_width=3):
    """Beam Search algorithm for solving the 8-puzzle problem."""
    queue = [(heuristic(start, goal), start, [start])]  # Include start in the path
    visited = set([tuple(start)])  # Track visited states

    expansions = 0  # Count the number of expansions
    while queue:
        # Sort the queue based on the heuristic value
        queue.sort(key=lambda x: x[0])
        # Keep only the top beam_width elements
        queue = queue[:beam_width]

        next_queue = []  # Prepare the next level of the queue
        for _, state, path in queue:
            expansions += 1
            if state == goal:
                return path, expansions  # Return the full path and expansions
            idx = state.index(0)
            row, col = divmod(idx, 3)
            neighbors = []
            for move in MOVES:
                new_row, new_col = row + move[0], col + move[1]
                if 0 <= new_row < 3 and 0 <= new_col < 3:
                    new_idx = new_row * 3 + new_col
                    new_state = state[:]
                    new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                    if tuple(new_state) not in visited:
                        neighbors.append(new_state)
                        visited.add(tuple(new_state))
            # Add neighbors to the next queue with their heuristic value
            for neighbor in neighbors:
                next_queue.append((heuristic(neighbor, goal), neighbor, path + [neighbor]))

        # Update the queue for the next iteration
        queue = next_queue

    return None, expansions  # Return None if no solution is found

POPULATION_SIZE = 100
MUTATION_RATE = 0.1
MAX_GENERATIONS = 200

def generate_individual():
    while True:
        individual = list(range(9))
        random.shuffle(individual)
        if is_solvable(individual):
            return individual

def fitness(individual, goal):
    return -manhattan(individual, goal)  # càng gần đích, giá trị càng cao

def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end] = parent1[start:end]

    p2_filtered = [x for x in parent2 if x not in child]
    idx = 0
    for i in range(size):
        if child[i] is None:
            child[i] = p2_filtered[idx]
            idx += 1
    return child

def mutate(individual):
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(9), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

def Genetic_Algorithm(start_state, goal_state):
    population = [generate_individual() for _ in range(POPULATION_SIZE)]
    path = []
    expansions = 0

    for generation in range(MAX_GENERATIONS):
        population.sort(key=lambda x: fitness(x, goal_state), reverse=True)
        best = population[0]

        path.append(best)
        expansions += len(population)

        if best == goal_state:
            return path, expansions

        next_gen = population[:10]  # elitism
        while len(next_gen) < POPULATION_SIZE:
            parent1, parent2 = random.choices(population[:50], k=2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            next_gen.append(child)

        population = next_gen

    return path, expansions