import random

def backtracking_search(start_state, goal_state):
    def is_complete(assignment):
        return len(assignment) == 9

    def select_unassigned_variable(assignment):
        for var in range(9):
            if var not in assignment:
                return var
        return None

    def is_consistent(var, value, assignment):
        return value not in assignment.values()

    def order_domain_values(var, assignment):
        return list(range(9))

    def recursive_backtracking(assignment, path):
        nonlocal steps
        if is_complete(assignment):
            assigned_list = [assignment[i] for i in range(9)]
            if assigned_list == goal_state:
                return path + [assigned_list]
            return None
        
        var = select_unassigned_variable(assignment)
        for value in order_domain_values(var, assignment):
            if is_consistent(var, value, assignment):
                assignment[var] = value
                steps += 1
                result = recursive_backtracking(assignment, path + [[assignment[i] if i in assignment else 0 for i in range(9)]])
                if result is not None:
                    return result
                del assignment[var]
        return None

    steps = 0
    assignment = {}
    result = recursive_backtracking(assignment, [])
    return (result, steps) if result else (None, steps)

def ac3(variables, domains, constraints):
    from collections import deque
    queue = deque([(xi, xj) for xi in variables for xj in constraints[xi]])

    while queue:
        xi, xj = queue.popleft()
        if revise(domains, xi, xj):
            if not domains[xi]:
                return False  # Không còn giá trị hợp lệ nào
            for xk in constraints[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def revise(domains, xi, xj):
    revised = False
    to_remove = []
    for x in domains[xi]:
        # Nếu không tồn tại giá trị y khác x trong xj → x không hợp lệ
        if all(x == y for y in domains[xj]):
            to_remove.append(x)
            revised = True
    for x in to_remove:
        domains[xi].remove(x)
    return revised

def ac3_filter(state):
    """AC-3 style AllDiff check for state"""
    return len(set(state)) == 9 and set(state) == set(range(9))


def backtracking_with_ac3(start_state, goal_state):
    def is_complete(assignment):
        return len(assignment) == 9

    def select_unassigned_variable(assignment, domains):
        for var in range(9):
            if var not in assignment:
                return var
        return None

    def order_domain_values(var, domains):
        return domains[var]

    def ac3(domains, constraints):
        from collections import deque
        queue = deque([(xi, xj) for xi in constraints for xj in constraints[xi]])
        while queue:
            xi, xj = queue.popleft()
            if revise(domains, xi, xj):
                if not domains[xi]:
                    return False
                for xk in constraints[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(domains, xi, xj):
        revised = False
        for x in domains[xi][:]:
            # loại x nếu không tồn tại giá trị nào trong xj ≠ x
            if all(x == y for y in domains[xj]):
                domains[xi].remove(x)
                revised = True
        return revised

    def recursive_backtracking(assignment, domains):
        nonlocal steps
        if is_complete(assignment):
            assigned_list = [assignment[i] for i in range(9)]
            if assigned_list == goal_state:
                return [assigned_list]
            return None

        var = select_unassigned_variable(assignment, domains)
        for value in order_domain_values(var, domains):
            # Sao chép sâu các miền để có thể hoàn tác khi cần
            local_assignment = assignment.copy()
            local_domains = {v: domains[v][:] for v in domains}
            local_assignment[var] = value
            local_domains[var] = [value]
            steps += 1

            if ac3(local_domains, constraints):
                result = recursive_backtracking(local_assignment, local_domains)
                if result:
                    state_now = [local_assignment.get(i, 0) for i in range(9)]
                    return [state_now] + result
        return None

    # === Khởi tạo ===
    steps = 0
    assignment = {}
    variables = list(range(9))
    domains = {v: list(range(9)) for v in variables}
    constraints = {v: [u for u in variables if u != v] for v in variables}

    result = recursive_backtracking(assignment, domains)
    return (result, steps) if result else (None, steps)

def create_constraints():
    """Tạo ràng buộc AllDiff: mỗi ô phải có giá trị khác nhau"""
    return {f"X{i}": [f"X{j}" for j in range(9) if j != i] for i in range(9)}

def is_consistent(var, value, assignment, constraints):
    """Kiểm tra xem có xung đột với các biến đã gán không"""
    for neighbor in constraints[var]:
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True

def backtrack(assignment, variables, domains, constraints, path, expansions, max_depth, depth, goal_state):
    if len(assignment) == len(variables):
        # Kiểm tra nếu không khớp goal_state → loại bỏ
        assigned_list = [assignment[f"X{i}"] for i in range(9)]
        if assigned_list != goal_state:
            return None

        grid = [[None for _ in range(3)] for _ in range(3)]
        for var, val in assignment.items():
            idx = int(var[1:])
            row, col = divmod(idx, 3)
            grid[row][col] = val
        path.append(grid)
        return assignment

    var = next((v for v in variables if v not in assignment), None)
    for value in domains[var]:
        if is_consistent(var, value, assignment, constraints):
            assignment[var] = value
            expansions[0] += 1
            max_depth[0] = max(max_depth[0], depth)
            result = backtrack(assignment, variables, domains, constraints, path, expansions, max_depth, depth + 1, goal_state)
            if result:
                return result
            del assignment[var]
    return None

def trial_and_error(start_state, goal_state):
    variables = [f"X{i}" for i in range(9)]
    domains = {var: list(range(9)) for var in variables}
    for var in domains:
        random.shuffle(domains[var])

    constraints = create_constraints()
    assignment = {}
    path = []
    expansions = [0]
    max_depth = [0]

    result = backtrack(assignment, variables, domains, constraints, path, expansions, max_depth, 0, goal_state)

    if result:
        flat_path = []
        for grid in path:
            flat = [0 if cell is None else cell for row in grid for cell in row]
            flat_path.append(flat)
        return flat_path, expansions[0], max_depth[0]
    else:
        return [], expansions[0], max_depth[0]