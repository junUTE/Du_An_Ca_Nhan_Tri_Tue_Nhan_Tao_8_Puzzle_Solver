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
    path = [start]  # Bao gồm 'start' trong đường dẫn
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

        #"Sắp xếp các điểm lân cận theo heuristic (khoảng cách Manhattan)
        neighbors.sort(key=lambda state: heuristic(state, goal))
        expansions += len(neighbors)

        # Chọn điểm lân cận tốt nhất
        best_neighbor = neighbors[0]
        if heuristic(best_neighbor, goal) >= heuristic(current, goal):
            # Nếu không có cải thiện, dừng lại
            return None, expansions

        current = best_neighbor
        path.append(current)

    return path, expansions

def steepest_ascent_hill_climbing(start, goal):
    """Steepest-Ascent Hill Climbing algorithm."""
    current = start
    path = [start]  # Bao gồm 'start' trong đường dẫn
    expansions = 0

    while current != goal:
        idx = current.index(0)
        row, col = divmod(idx, 3)
        neighbors = []

        # Tạo tất cả các điểm lân cận có thể có
        for move in MOVES:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                new_state = current[:]
                new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                neighbors.append(new_state)

        # Sắp xếp các điểm lân cận theo heuristic (khoảng cách Manhattan)
        neighbors.sort(key=lambda state: heuristic(state, goal))
        expansions += len(neighbors)

        # Chọn điểm lân cận tốt nhất
        best_neighbor = neighbors[0]
        if heuristic(best_neighbor, goal) >= heuristic(current, goal):
            # Nếu không có cải thiện, dừng lại
            return None, expansions

        current = best_neighbor
        path.append(current)

    return path, expansions

def Stochastic_hill_Climbing(start, goal):
    current = start
    path = [start]  # Bao gồm 'start' trong đường dẫn
    expansions = 0

    while current != goal:
        idx = current.index(0)
        row, col = divmod(idx, 3)
        neighbors = []
        # Tạo tất cả các điểm lân cận có thể có
        for move in MOVES:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                new_state = current[:]
                new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                neighbors.append(new_state)

        # Sắp xếp các điểm lân cận theo heuristic (khoảng cách Manhattan)
        better_neighbors = [neighbor for neighbor in neighbors if heuristic(neighbor, goal) < heuristic(current, goal)]
        expansions += len(neighbors)

        if not better_neighbors:
            # Nếu không có điểm lân cận tốt hơn, dừng lại
            return None, expansions

        # Chọn ngẫu nhiên một trong các điểm lân cận tốt hơn
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
            return path, expansions  # Trả về đường dẫn nếu không có hàng xóm

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

        # Cập nhật nhiệt độ
        h = heuristic(current, goal)
        if h < best_score:
            best = current
            best_score = h

        temperature *= cooling_rate

    if current == goal:
        return path, expansions
    else:
        return path, expansions  # Trả về đường dẫn nếu không tìm thấy giải pháp

def Beam_Search(start, goal, beam_width=3):
    """Beam Search algorithm for solving the 8-puzzle problem."""
    queue = [(heuristic(start, goal), start, [start])]  # Bắt đầu với hàng đợi chứa trạng thái khởi đầu
    visited = set([tuple(start)])  # Tập các trạng thái đã thăm

    expansions = 0  # Biến đếm số lần mở rộng nút
    while queue:
        # Sắp xếp hàng đợi theo giá trị heuristic
        queue.sort(key=lambda x: x[0])
        # Chỉ giữ lại beam_width trạng thái tốt nhất
        queue = queue[:beam_width]

        next_queue = []  # Hàng đợi cho các trạng thái tiếp theo
        for _, state, path in queue:
            expansions += 1
            if state == goal:
                return path, expansions  # Trả về đường dẫn nếu tìm thấy giải pháp
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
            # Thêm các hàng xóm vào hàng đợi tiếp theo
            for neighbor in neighbors:
                next_queue.append((heuristic(neighbor, goal), neighbor, path + [neighbor]))

        # Cập nhật hàng đợi
        queue = next_queue

    return None, expansions  # Trả về None nếu không tìm thấy giải pháp

