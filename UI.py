import tkinter as tk
from tkinter import messagebox
from collections import deque
from time import sleep, time
from tkinter import ttk  

from utils import is_solvable

from algorithm.Uninformed_Search import bfs, dfs, ucs, iddfs
from algorithm.Informed_Search import greedy, a_star, ida_star
from algorithm.Local_Search import simple_hill_climbing, steepest_ascent_hill_climbing, Stochastic_hill_Climbing, Simulated_Annealing, Beam_Search, Genetic_Algorithm
from algorithm.CSP import backtracking_search, backtracking_with_ac3, trial_and_error
from algorithm.Searching_in_Complex import And_or_graph_search, searching_with_no_observation, belief_bfs
from algorithm.Reinforcement_Learning import Q_Learning


label_font = ("Arial", 14, "bold")
text_font = ("Arial", 12)


def draw_board(canvas, board, step, elapsed, expansions=0):
    canvas.delete('all')
    cell_size = 100
    for i in range(3):
        for j in range(3):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            idx = i * 3 + j
            if idx >= len(board):
                continue  # Bỏ qua nếu dữ liệu thiếu
            num = board[idx]
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
    text_box.insert(tk.END, f"Step {step}:\n")
    for i in range(3):
        row_slice = board[i * 3:(i + 1) * 3]
        text_box.insert(tk.END, f"{row_slice}\n")
    text_box.insert(tk.END, "\n")
    text_box.see(tk.END)


def solve_puzzle(_, __, algorithm, canvas, root):
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
        "Searching With No Observation": searching_with_no_observation,
        "Belief BFS": belief_bfs,
        "Backtracking Search": backtracking_search,
        "Backtracking AC3": backtracking_with_ac3,
        "Genetic Algorithm": Genetic_Algorithm,
        "Trial And Error": trial_and_error,
        "Q Learning": Q_Learning,
    }

    # ✅ Danh sách các thuật toán không cần nhập trạng thái đầu
    no_input_algorithms = [
        "Backtracking Search",
        "Backtracking AC3",
        "Trial And Error",
        "Genetic Algorithm"
    ]

    try:
        text_box.delete(1.0, tk.END)
        algorithm = algo_var.get()

        # ✅ Belief BFS dùng input đặc biệt (có thể chứa None)
        if algorithm == "Belief BFS":
            start_state = [
                int(entry.get()) if entry.get().isdigit() else None
                for row in start_entries for entry in row
            ]
            goal_state = [
                int(entry.get()) if entry.get().isdigit() else 0
                for row in goal_entries for entry in row
            ]
            if all(v == 0 for v in goal_state):
                goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

        # ✅ Thuật toán không cần input → tạo mặc định
        elif algorithm in no_input_algorithms:
            start_state = [0] * 9  # không dùng
            goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

        # ✅ Các thuật toán còn lại cần input từ người dùng
        else:
            start_state = [
                int(entry.get()) if entry.get().isdigit() else 0
                for row in start_entries for entry in row
            ]
            goal_state = [
                int(entry.get()) if entry.get().isdigit() else 0
                for row in goal_entries for entry in row
            ]
            if all(v == 0 for v in goal_state):
                goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

            if not is_solvable(start_state):
                messagebox.showinfo("Result", "This puzzle is not solvable")
                return

        # ✅ Chạy thuật toán
        start_time = time()
        result = algorithms[algorithm](start_state, goal_state)
        end_time = time()
        elapsed_time = end_time - start_time

        # ✅ Một số thuật toán trả về 3 phần tử (path, expansions, depth)
        if isinstance(result, tuple) and len(result) == 3:
            solution, expansions, _ = result
        else:
            solution, expansions = result

        if solution:
            draw_board(canvas, solution[0], 0, 0, expansions)
            for i, step in enumerate(solution):
                draw_board(canvas, step, i, elapsed_time, expansions)
                log_step(i, step)
                root.update()
                sleep(0.5)
            save_to_data_grid(algorithm, elapsed_time, expansions)
        else:
            messagebox.showinfo('Solution', 'No solution found')
            save_to_data_grid(algorithm, elapsed_time, expansions)

    except ValueError:
        messagebox.showerror("Error", "Invalid input, please enter numbers")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")


def start_solver():
    try:
        # Disable "OK" and "Reset" buttons
        ok_button.config(state="disabled")
        reset_button.config(state="disabled")

        # Đọc trạng thái đầu và trạng thái đích từ ô nhập
        start_state = [int(entry.get()) if entry.get() else 0 for row in start_entries for entry in row]
        goal_state = [int(entry.get()) if entry.get() else 0 for row in goal_entries for entry in row]

        # Nếu goal_state rỗng, đặt mặc định
        if all(value == 0 for value in goal_state):
            goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

        # Đọc thuật toán được chọn
        algorithm = algo_var.get()

        # Kiểm tra nếu chọn dòng nhóm (--- ...)
        if not algorithm or algorithm.startswith("---"):
            messagebox.showerror("Error", "Please select a valid algorithm (not a group heading)")
            return

        # Gọi hàm giải thuật
        solve_puzzle(start_state, goal_state, algorithm, canvas, root)

    except ValueError:
        messagebox.showerror("Error", "Invalid input, please enter numbers")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    finally:
        # Re-enable buttons
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
        #if len(start_state) != len(set(start_state)):
           # messagebox.showerror("Error", "Duplicate numbers found or empty. Please enter again.")
            #return
        
        # Check if the initial state contains exactly the numbers 0-8
        # if sorted(start_state) != list(range(9)):
        #     messagebox.showerror("Error", "Invalid Initial State. Please enter numbers 0-8 exactly once.")
        #     return
        
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
root.title("8 Puzzle Solver - Vũ Quốc Trung_23110353")

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
algo_combobox['values'] = [
    "--- Uninformed Search ---",
    "BFS",
    "DFS",
    "UCS",
    "IDDFS",

    "--- Informed Search ---",
    "Greedy",
    "A*",
    "IDA*",

    "--- Local Search ---",
    "Simple Hill Climbing",
    "Steepest Ascent Hill Climbing",
    "Stochastic Hill Climbing",
    "Simulated Annealing",
    "Beam Search",
    "Genetic Algorithm",

    "--- Constraint Satisfaction ---",
    "Backtracking Search",
    "Backtracking AC3",
    "Trial And Error",

    "--- Complex Environment ---",
    "And Or Graph Search",
    "Searching With No Observation",
    "Belief BFS",

    "--- Reinforcement Learning ---",
    "Q Learning",
]
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