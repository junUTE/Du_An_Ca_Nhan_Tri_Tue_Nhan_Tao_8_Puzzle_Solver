from collections import deque
import heapq

MOVES = [(0,1), (1,0), (0,-1), (-1,0)]

def heuristic(state, goal):
    """Calculate the Manhattan distance heuristic."""
    return sum(abs((val - 1) % 3 - (i % 3)) + abs((val - 1) // 3 - (i // 3))
               for i, val in enumerate(state) if val != 0)

def greedy(start, goal):
    queue = [(heuristic(start, goal), start, [start])]  # Include start in the path
    visited = set([tuple(start)])
    expansions = 0

    while queue:
        _, state, path = heapq.heappop(queue)
        expansions += 1
        if state == goal:
            return path, expansions
        idx = state.index(0)
        row, col = divmod(idx, 3)

        for move in MOVES:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                new_state = state[:]
                new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                if tuple(new_state) not in visited:
                    heapq.heappush(queue, (heuristic(new_state, goal), new_state, path + [new_state]))
                    visited.add(tuple(new_state))
    return None, expansions

def a_star(start, goal):
    queue = [(heuristic(start, goal), 0, start, [start])]  # Include start in the path
    visited = set([tuple(start)])
    expansions = 0

    while queue:
        f, g, state, path = heapq.heappop(queue)
        expansions += 1
        if state == goal:
            return path, expansions
        idx = state.index(0)
        row, col = divmod(idx, 3)

        for move in MOVES:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                new_state = state[:]
                new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                if tuple(new_state) not in visited:
                    g_new = g + 1
                    f_new = g_new + heuristic(new_state, goal)
                    heapq.heappush(queue, (f_new, g_new, new_state, path + [new_state]))
                    visited.add(tuple(new_state))
    return None, expansions

def ida_star(start, goal):
    def search(path, g, bound):
        state = path[-1]
        f = g + heuristic(state, goal)
        if f > bound:
            return None, f
        if state == goal:
            return path, g
        idx = state.index(0)
        row, col = divmod(idx, 3)
        min_bound = float('inf')
        for move in MOVES:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                new_state = state[:]
                new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    result, new_bound = search(path + [new_state], g + 1, bound)
                    if result:
                        return result, g + 1
                    min_bound = min(min_bound, new_bound)
        return None, min_bound

    bound = heuristic(start, goal)
    path = [start]  # Include start in the path
    visited = set([tuple(start)])
    while True:
        result, bound = search(path, 0, bound)
        if result:
            return result, len(visited)
        if bound == float('inf'):
            return None, len(visited)