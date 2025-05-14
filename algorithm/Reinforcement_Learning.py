from collections import defaultdict
import random

MOVES = [(0,1), (1,0), (0,-1), (-1,0)]  # RIGHT, DOWN, LEFT, UP
MOVE_NAMES = ['RIGHT', 'DOWN', 'LEFT', 'UP']

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