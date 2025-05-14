import random
from collections import deque
from itertools import permutations
from utils import is_solvable

MOVES = [(0,1), (1,0), (0,-1), (-1,0)]

def get_neighbors(state):
    """
    Lấy danh sách các trạng thái lân cận từ trạng thái hiện tại.
    """
    neighbors = []
    idx = state.index(0)
    row, col = divmod(idx, 3)
    for move in MOVES:
        new_row, new_col = row + move[0], col + move[1]
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_idx = new_row * 3 + new_col
            new_state = state[:]
            new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
            neighbors.append(new_state)
    return neighbors

def And_or_graph_search(start, goal, max_depth=50):
    """
    Hàm tìm kiếm AND-OR để giải bài toán 8-puzzle.
    """
    expansions = 0

    def goal_test(state):
        """
        Kiểm tra xem trạng thái hiện tại có phải là trạng thái mục tiêu không.
        """
        return state == goal

    def results(state, action):
        """
        Trả về trạng thái mới sau khi thực hiện hành động.
        """
        new_state = state[:]
        idx = new_state.index(0)
        row, col = divmod(idx, 3)
        new_row, new_col = row + action[0], col + action[1]
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_idx = new_row * 3 + new_col
            new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
        return new_state

    def or_search(state, path, depth):
        """
        Hàm OR-SEARCH: trả về kế hoạch điều kiện hoặc thất bại.
        """
        nonlocal expansions
        if goal_test(state):
            return [state]
        if state in path or depth > max_depth:
            return None
        expansions += 1
        for neighbor in get_neighbors(state):
            if neighbor not in path:
                plan = and_search([neighbor], path + [state], depth + 1)
                if plan:
                    return [state] + plan
        return None

    def and_search(states, path, depth):
        """
        Hàm AND-SEARCH: trả về kế hoạch điều kiện hoặc thất bại.
        """
        full_plan = []
        for s in states:
            plan = or_search(s, path, depth)
            if plan is None:
                return None
            full_plan.extend(plan[1:] if full_plan else plan)
        return full_plan

    plan = or_search(start, [], 0)
    return (plan, expansions) if plan else (None, expansions)

def searching_with_no_observation(start, goal, max_steps=1000):
    current = start
    path = [start]
    visited = set()
    visited.add(tuple(start))
    expansions = 0

    for step in range(max_steps):
        if current == goal:
            return path, expansions

        idx = current.index(0)
        row, col = divmod(idx, 3)
        neighbors = []

        for move in MOVES:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                new_state = current[:]
                new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                if tuple(new_state) not in visited:
                    neighbors.append(new_state)
                    visited.add(tuple(new_state))

        expansions += len(neighbors)

        if not neighbors:
            return None, expansions

        current = random.choice(neighbors)
        path.append(current)

    return None, expansions

def generate_belief_states(partial_state, max_states=1000):
    # Đảm bảo độ dài đủ 9
    if len(partial_state) != 9:
        raise ValueError("Initial state must have exactly 9 positions (some may be None)")

    full = partial_state[:]
    known_vals = {val for val in full if val is not None}
    missing_vals = list(set(range(9)) - known_vals)

    belief_states = set()
    for perm in permutations(missing_vals):
        temp = full[:]
        idx = 0
        for i in range(9):
            if temp[i] is None:
                temp[i] = perm[idx]
                idx += 1
        if is_solvable(temp):
            belief_states.add(tuple(temp))
            if len(belief_states) >= max_states:
                break

    return [list(state) for state in belief_states]


def belief_bfs(partial_start, goal):
    #Chạy BFS trên tập hợp các trạng thái ban đầu có thể có từ một input thiếu thông tin
    start_beliefs = generate_belief_states(partial_start)
    queue = deque()
    visited = set()
    expansions = 0

    for state in start_beliefs:
        queue.append((state, [state]))
        visited.add(tuple(state))

    while queue:
        state, path = queue.popleft()
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
                    visited.add(tuple(new_state))
                    queue.append((new_state, path + [new_state]))

    return None, expansions