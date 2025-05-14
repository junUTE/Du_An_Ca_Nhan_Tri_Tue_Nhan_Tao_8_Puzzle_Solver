from collections import defaultdict
from utils import is_solvable
import random


MOVES = [(0,1), (1,0), (0,-1), (-1,0)] 
MOVE_NAMES = ['RIGHT', 'DOWN', 'LEFT', 'UP']

def manhattan(state, goal):
    return sum(abs((val - 1) % 3 - (i % 3)) + abs((val - 1) // 3 - (i // 3))
               for i, val in enumerate(state) if val != 0)

def encode(state):
    return tuple(state)

def decode(state):
    return list(state)

def get_possible_actions(state):
    idx = state.index(0)
    row, col = divmod(idx, 3)
    actions = []
    for i, (dr, dc) in enumerate(MOVES):
        new_r, new_c = row + dr, col + dc
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            actions.append(MOVE_NAMES[i])
    return actions

def apply_action(state, action):
    idx = state.index(0)
    row, col = divmod(idx, 3)
    move_idx = MOVE_NAMES.index(action)
    dr, dc = MOVES[move_idx]
    new_r, new_c = row + dr, col + dc
    if not (0 <= new_r < 3 and 0 <= new_c < 3):
        return state  # không hợp lệ, giữ nguyên
    new_idx = new_r * 3 + new_c
    new_state = state[:]
    new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
    return new_state

def Q_Learning(start_state, goal_state, episodes=5000, alpha=0.1, gamma=0.9, epsilon=0.1):
    Q = defaultdict(float)
    goal = tuple(goal_state)

    for _ in range(episodes):
        state = start_state[:]
        for _ in range(50):  # tối đa 50 bước mỗi episode
            s_enc = encode(state)
            actions = get_possible_actions(state)
            if not actions:
                break
            if random.random() < epsilon:
                action = random.choice(actions)
            else:
                q_vals = [(Q[(s_enc, a)], a) for a in actions]
                action = max(q_vals)[1]

            next_state = apply_action(state, action)
            reward = 100 if tuple(next_state) == goal else -1
            next_enc = encode(next_state)
            max_next_q = max([Q[(next_enc, a)] for a in get_possible_actions(next_state)] + [0])
            Q[(s_enc, action)] += alpha * (reward + gamma * max_next_q - Q[(s_enc, action)])

            state = next_state
            if tuple(state) == goal:
                break

    # Truy xuất đường đi tốt nhất
    path = [start_state]
    state = start_state[:]
    expansions = 0
    for _ in range(100):
        s_enc = encode(state)
        actions = get_possible_actions(state)
        if not actions:
            break
        q_vals = [(Q[(s_enc, a)], a) for a in actions]
        action = max(q_vals)[1]
        state = apply_action(state, action)
        path.append(state)
        expansions += 1
        if tuple(state) == goal:
            break

    if tuple(state) == goal:
        return path, expansions
    else:
        return [], expansions
    
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

        next_gen = population[:10]  # Giữ lại 10 cá thể tốt nhất
        while len(next_gen) < POPULATION_SIZE:
            parent1, parent2 = random.choices(population[:50], k=2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            next_gen.append(child)

        population = next_gen

    return path, expansions