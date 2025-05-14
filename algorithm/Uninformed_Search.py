from collections import deque
import heapq

# Các hướng di chuyển: phải, xuống, trái, lên
MOVES = [(0,1), (1,0), (0,-1), (-1,0)]

def bfs(start, goal):
    queue = deque([(start, [start])])  # Hàng đợi chứa trạng thái và đường đi
    visited = set([tuple(start)])      # Tập các trạng thái đã thăm
    expansions = 0                     # Biến đếm số lần mở rộng nút

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
                    queue.append((new_state, path + [new_state]))
                    visited.add(tuple(new_state))
    return None, expansions

def dfs(start, goal, max_depth=50):
    stack = [(start, [start], 0)]  # Ngăn xếp chứa trạng thái, đường đi, độ sâu hiện tại
    visited = set([tuple(start)])
    expansions = 0

    while stack:
        state, path, depth = stack.pop()
        expansions += 1
        if state == goal:
            return path, expansions
        if depth >= max_depth:
            continue
        idx = state.index(0)
        row, col = divmod(idx, 3)

        for move in reversed(MOVES):  # Duyệt ngược để thứ tự giống với BFS
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                new_state = state[:]
                new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                if tuple(new_state) not in visited:
                    stack.append((new_state, path + [new_state], depth + 1))
                    visited.add(tuple(new_state))
    return None, expansions

def ucs(start, goal):
    queue = [(0, start, [start])]  # Hàng đợi ưu tiên chứa (chi phí, trạng thái, đường đi)
    visited = set([tuple(start)])
    expansions = 0

    while queue:
        cost, state, path = heapq.heappop(queue)
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
                    heapq.heappush(queue, (cost + 1, new_state, path + [new_state]))
                    visited.add(tuple(new_state))
    return None, expansions

def iddfs(start, goal, max_depth=50):
    def dls(state, goal, depth, path, visited):
        # Nếu đạt độ sâu 0, kiểm tra đích
        if depth == 0:
            return (path, len(visited)) if state == goal else (None, len(visited))
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
                    result, expansions = dls(new_state, goal, depth - 1, path + [new_state], visited)
                    if result:
                        return result, expansions
        return None, len(visited)

    # Tăng dần độ sâu tối đa từ 0 đến max_depth
    for depth in range(max_depth + 1):
        visited = set([tuple(start)])
        result, expansions = dls(start, goal, depth, [start], visited)
        if result:
            return result, expansions
    return None, len(visited)