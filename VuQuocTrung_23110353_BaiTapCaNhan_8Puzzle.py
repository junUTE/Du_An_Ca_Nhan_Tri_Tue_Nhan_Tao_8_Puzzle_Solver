import tkinter as tk
from tkinter import messagebox
from collections import deque
import heapq
from time import sleep, time
import random
from tkinter import ttk  # Import ttk for combobox and LabelFrame

MOVES = [(0,1), (1,0), (0,-1), (-1,0)]
label_font = ("Arial", 14, "bold")
text_font = ("Arial", 12)

def bfs(start, goal):
    queue = deque([(start, [start])])  # Include start in the path
    visited = set([tuple(start)])
    expansions = 0  # Track the number of expansions

    while queue:
        state, path = queue.popleft()
        expansions += 1  # Increment expansions for each state dequeued
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
    stack = [(start, [start], 0)]  # Include start in the path
    visited = set([tuple(start)])
    expansions = 0  # Track the number of expansions

    while stack:
        state, path, depth = stack.pop()
        expansions += 1  # Increment expansions for each state popped
        if state == goal:
            return path, expansions
        if depth >= max_depth:
            continue
        idx = state.index(0)
        row, col = divmod(idx, 3)

        for move in reversed(MOVES):
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
    queue = [(0, start, [start])]  # Include start in the path
    visited = set([tuple(start)])
    expansions = 0  # Track the number of expansions

    while queue:
        cost, state, path = heapq.heappop(queue)
        expansions += 1  # Increment expansions for each state dequeued
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

def iddfs(start, goal, max_depth=50):
    def dls(state, goal, depth, path, visited):
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

    for depth in range(max_depth + 1):
        visited = set([tuple(start)])
        result, expansions = dls(start, goal, depth, [start], visited)  # Include start in the path
        if result:
            return result, expansions
    return None, len(visited)

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



#------------------------------------------------------
# Add a function to check if the puzzle is solvable
def is_solvable(state):
    flat = [num for num in state if num != 0]
    inversions = sum(1 for i in range(len(flat)) for j in range(i + 1, len(flat)) if flat[i] > flat[j])
    return inversions % 2 == 0

def draw_board(canvas, board, step, elapsed, expansions=0):
    canvas.delete('all')
    cell_size = 100
    for i in range(3):
        for j in range(3):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            num = board[i * 3 + j]
            if num != 0:
                canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')
                canvas.create_text(x1 + 50, y1 + 50, text=str(num), font=('Arial', 36, "bold"))
    step_label.config(text=f"Step: {step}")
    time_label.config(text=f"Time: {elapsed:.3f}s")
    expansion_label.config(text=f"Expansions: {expansions}")

def save_to_data_grid(algorithm, time_elapsed, expansions):
    """Save algorithm results to the data grid view."""
    data_grid.insert("", "end", values=(algorithm, f"{time_elapsed:.3f}", expansions))

def log_step(step, board):
    """Log each step of the algorithm execution in the text box."""
    text_box.insert(tk.END, f"Step {step}:\n")
    for i in range(3):
        text_box.insert(tk.END, f"{board[i * 3:(i + 1) * 3]}\n")
    text_box.insert(tk.END, "\n")
    text_box.see(tk.END)  # Auto-scroll to the latest entry

def solve_puzzle(start, goal, algorithm, canvas, root):
    algorithms = {
        "BFS": bfs,
        "DFS": dfs,
        "UCS": ucs,
        "Greedy": greedy,
        "IDDFS": iddfs,
        "A*": a_star,
        "IDA*": ida_star,
        "Simple Hill Climbing": simple_hill_climbing,
        "Steepest Ascent Hill Climbing": steepest_ascent_hill_climbing,
        "Stochastic Hill Climbing": Stochastic_hill_Climbing,
        "Simulated Annealing": Simulated_Annealing,
        "Beam Search": Beam_Search,
        "And Or Graph Search": And_or_graph_search,
        "Searching With No Observation": searching_with_no_observation
    }

    if not is_solvable(start):
        messagebox.showinfo("Result", "This puzzle is not solvable")
        return

    text_box.delete(1.0, tk.END)  # Clear the text box before starting
    start_time = time()
    solution, expansions = algorithms[algorithm](start, goal)
    end_time = time()
    elapsed_time = end_time - start_time

    draw_board(canvas, start, 0, 0, expansions)

    if solution:
        for i, step in enumerate(solution):
            draw_board(canvas, step, i, elapsed_time, expansions)
            log_step(i, step)  # Log each step to the text box
            root.update()
            sleep(0.5)
        save_to_data_grid(algorithm, elapsed_time, expansions)  # Save results to the data grid
    else:
        messagebox.showinfo('Solution', 'No solution found')
        save_to_data_grid(algorithm, elapsed_time, expansions)  # Save results even if no solution is found

def start_solver():
    try:
        # Disable "OK" and "Reset" buttons
        ok_button.config(state="disabled")
        reset_button.config(state="disabled")

        start_state = [int(entry.get()) if entry.get() else 0 for row in start_entries for entry in row]
        goal_state = [int(entry.get()) if entry.get() else 0 for row in goal_entries for entry in row]
        
        # Set default goal state if all values are 0
        if all(value == 0 for value in goal_state):
            goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        
        if all(value == 0 for value in start_state):  # Check if the initial state is empty
            messagebox.showerror("Error", "Please enter Initial State")
            return
        
        algorithm = algo_var.get()
        if not algorithm:
            messagebox.showerror("Error", "Please select an algorithm")
            return
        
        solve_puzzle(start_state, goal_state, algorithm, canvas, root)
    except ValueError:
        messagebox.showerror("Error", "Invalid input, please enter numbers")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    finally:
        # Re-enable "OK" and "Reset" buttons after the process is complete
        ok_button.config(state="normal")
        reset_button.config(state="normal")

def quit_program():
    """Gracefully quit the program."""
    try:
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            root.destroy()  # Destroy the root window to exit the program
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while quitting: {e}")

def reset():
    # Clear the start state input fields
    for row in start_entries:
        for entry in row:
            entry.delete(0, tk.END)
    
    # Reset the goal state input fields to default values
    for i, row in enumerate(goal_entries):
        for j, entry in enumerate(row):
            entry.delete(0, tk.END)
            entry.insert(0, [1, 2, 3, 4, 5, 6, 7, 8, 0][i * 3 + j])
    
    # Clear the canvas
    canvas.delete('all')
    
    # Clear the Execution Steps text box
    text_box.delete(1.0, tk.END)
    
    # Clear the Algorithm Results data grid
    for item in data_grid.get_children():
        data_grid.delete(item)

def confirm_input():
    try:
        start_state = [int(entry.get()) if entry.get() else 0 for row in start_entries for entry in row]
        
        # Check for duplicate numbers in the initial state
        if len(start_state) != len(set(start_state)):
            messagebox.showerror("Error", "Duplicate numbers found or empty. Please enter again.")
            return
        
        # Check if the initial state contains exactly the numbers 0-8
        if sorted(start_state) != list(range(9)):
            messagebox.showerror("Error", "Invalid Initial State. Please enter numbers 0-8 exactly once.")
            return
        
        # Clear the Algorithm Results data grid
        for item in data_grid.get_children():
            data_grid.delete(item)
        
        # Clear the Execution Steps text box
        text_box.delete(1.0, tk.END)
        
        # Draw the board with the new start state
        draw_board(canvas, start_state, 0, 0)
    except ValueError:
        messagebox.showerror("Error", "Invalid input, please enter numbers")


# GUI Setup
root = tk.Tk()
root.title("8 Puzzle Solver")

main_frame = tk.Frame(root)
main_frame.pack()

# Canvas for Visualization (Center)
# Create a style for the LabelFrame
style = ttk.Style()
style.configure("Custom.TLabelframe.Label", font=label_font, fg="#2E86C1", bg="#AED6F1", db=2, relief="groove")
canvas_frame = ttk.LabelFrame(main_frame, text="Visualization", padding=(10, 10), style="Custom.TLabelframe")

canvas_frame.pack(side="left", padx=10, pady=10)
canvas = tk.Canvas(canvas_frame, width=300, height=300)
canvas.pack()

# Step, Time, and Expansions Display
info_frame = ttk.LabelFrame(canvas_frame, text="Information", padding=(6, 1), style="Custom.TLabelframe")
info_frame.pack(pady=10)
step_label = tk.Label(info_frame, text="Step: 0", font=("Arial", 14))
step_label.pack()
time_label = tk.Label(info_frame, text="Time: 0.00s", font=("Arial", 14))
time_label.pack()
expansion_label = tk.Label(info_frame, text="Expansions: 0", font=("Arial", 14))  # New label for expansions
expansion_label.pack()

# Input and Controls (Right)
input_frame = ttk.LabelFrame(main_frame, text="Input and Controls", padding=(10, 10), style="Custom.TLabelframe")
input_frame.pack(side="right", padx=10, pady=10)

# Initial State Input
initial_state_frame = ttk.LabelFrame(input_frame, text="Initial State", padding=(10, 10), style="Custom.TLabelframe")
initial_state_frame.pack(pady=5)
start_entries = [[tk.Entry(initial_state_frame, width=2, font=("Arial", 18)) for _ in range(3)] for _ in range(3)]
for i, row in enumerate(start_entries):
    for j, entry in enumerate(row):
        entry.grid(row=i, column=j, padx=5, pady=5)

# Add a frame for the data grid view and text box
data_grid_frame = ttk.LabelFrame(main_frame, text="Algorithm Results", padding=(10, 10), style="Custom.TLabelframe")
data_grid_frame.pack(side="left", padx=10, pady=10)

# Create a Treeview widget for the data grid
data_grid = ttk.Treeview(data_grid_frame, columns=("Algorithm", "Time", "Expansions"), show="headings", height=10)
data_grid.heading("Algorithm", text="Algorithm")
data_grid.heading("Time", text="Time (s)")
data_grid.heading("Expansions", text="Expansions")
data_grid.column("Algorithm", width=200, anchor="center")
data_grid.column("Time", width=110, anchor="center")
data_grid.column("Expansions", width=150, anchor="center")
data_grid.pack()

# Add a text box below the data grid view
text_box_frame = ttk.LabelFrame(data_grid_frame, text="Execution Steps", padding=(10, 10), style="Custom.TLabelframe")
text_box_frame.pack(fill="both", expand=True, pady=10)
text_box = tk.Text(text_box_frame, height=10, wrap="word", font=("Arial", 13))
text_box.pack(fill="both", expand=True)
scrollbar = ttk.Scrollbar(text_box_frame, orient="vertical", command=text_box.yview)
scrollbar.pack(side="right", fill="y")
text_box.config(yscrollcommand=scrollbar.set)

# OK Button for Initial State
ok_button = tk.Button(initial_state_frame, text="OK", command=confirm_input, bg="lightblue", fg="black")
ok_button.grid(row=3, column=0, columnspan=3, pady=5)  # Use grid instead of pack

# Goal State Input
goal_state_frame = ttk.LabelFrame(input_frame, text="Goal State", padding=(10, 10), style="Custom.TLabelframe")
goal_state_frame.pack(pady=5)
goal_entries = [[tk.Entry(goal_state_frame, width=2, font=("Arial", 18)) for _ in range(3)] for _ in range(3)]
for i, row in enumerate(goal_entries):
    for j, entry in enumerate(row):
        entry.grid(row=i, column=j, padx=5, pady=5)

# Initialize the goal state input fields with default values
for i, row in enumerate(goal_entries):
    for j, entry in enumerate(row):
        entry.insert(0, [1, 2, 3, 4, 5, 6, 7, 8, 0][i * 3 + j])

# Algorithm Selection
algorithm_frame = ttk.LabelFrame(input_frame, text="Algorithm Selection", padding=(10, 10), style="Custom.TLabelframe")
algorithm_frame.pack(pady=5)
algo_var = tk.StringVar(value="")
algo_combobox = ttk.Combobox(algorithm_frame, textvariable=algo_var, state="readonly", width=25)
algo_combobox['values'] = sorted(["BFS",
                                   "DFS",
                                    "UCS",
                                    "Greedy",
                                    "IDDFS",
                                    "A*",
                                    "IDA*",
                                    "Simple Hill Climbing", 
                                    "Steepest Ascent Hill Climbing",
                                    "Stochastic Hill Climbing", 
                                    "Simulated Annealing", 
                                    "Beam Search", 
                                    "And Or Graph Search",
                                    "Searching With No Observation"])
algo_combobox.pack()

# Control Buttons
control_frame = ttk.LabelFrame(input_frame, text="Controls", padding=(10, 10), style="Custom.TLabelframe")
control_frame.pack(pady=5)
tk.Button(control_frame, text="Run", command=start_solver, bg="lightgreen", fg="black").pack(side="left", padx=5)
reset_button = tk.Button(control_frame, text="Reset", command=reset, bg="#FFA07A", fg="black")
reset_button.pack(side="left", padx=5)
tk.Button(control_frame, text="Quit", command=quit_program, bg="lightcoral", fg="black").pack(side="left", padx=5)

# Initialize the board with default values
default_board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
draw_board(canvas, default_board, 0, 0.0, 0)

root.mainloop()
