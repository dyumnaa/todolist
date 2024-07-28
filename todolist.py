import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import PIL for image handling
import os  # Import os for file path checking

# Initialize the main window
root = tk.Tk()
root.title("To-Do List")
root.geometry("350x600+400+100")  # Adjusted size to make it more compact
root.resizable(False, False)

# Check if the background image file exists
background_image_path = "Images/background.png"  # Path to your background image

# Load and set the background image
if os.path.exists(background_image_path):
    try:
        # Load the background image
        background_image = Image.open(background_image_path)
        # Resize the image to fit the window
        background_image = background_image.resize((350, 600), Image.LANCZOS)  # Use Image.LANCZOS for high-quality resizing
        # Create a PhotoImage from the PIL Image
        background_photo = ImageTk.PhotoImage(background_image)

        # Create a label with the background image
        background_label = tk.Label(root, image=background_photo)
        # Place the label to fill the entire window
        background_label.place(relwidth=1, relheight=1)  # relwidth and relheight fill the window
    except Exception as e:
        print(f"Failed to load the image: {e}")
else:
    print("Background image file not found.")

# Define colors
bg_color = "#F3DFE5"           # Light Pink for main background
frame_bg_color = "#F3DFE5"     # Very Light Pink for frames
accent_color = "#D78AAD"       # Pink for completed tasks
text_color = "#414A7C"         # Dark Blue for text
button_color = "#C34E5D"       # Dark Pink for buttons
button_hover_color = "#A73C4A" # Darker Pink for button hover
button_text_color = "#FFFFFF"  # White for button text
tick_color = "#847A74"         # Grey for tick mark
header_color = "#414A7C"       # Dark Blue for header text
completed_task_color = "#D78AAD"  # Light pink for completed task background

# Task list to hold tasks and their completion status
task_list = []

# Function to add a task
def add_task():
    task = task_entry.get()
    task_entry.delete(0, tk.END)

    if task:
        task_list.append({"task": task, "completed": False})
        update_task_file()
        display_tasks()
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

# Function to delete a task
def delete_task():
    selected_task_index = listbox.curselection()
    
    if selected_task_index:
        listbox.delete(selected_task_index)
        del task_list[selected_task_index[0]]
        update_task_file()
        display_tasks()
    else:
        messagebox.showwarning("Warning", "You must select a task to delete.")

# Function to display the list of tasks
def display_tasks():
    listbox.delete(0, tk.END)
    for index, task_data in enumerate(task_list):
        task = task_data['task']
        completed = task_data['completed']
        display_text = f"{'✔' if completed else '◻'} {task}"  # Tick box for completed tasks, empty box for incomplete
        listbox.insert(tk.END, display_text)
        listbox.itemconfig(tk.END, {
            'bg': completed_task_color if completed else bg_color,
            'fg': text_color
        })
    update_task_count()

# Function to update task counts
def update_task_count():
    completed_tasks = sum(1 for task in task_list if task["completed"])
    remaining_tasks = len(task_list) - completed_tasks
    completed_label.config(text=f"Completed: {completed_tasks}")
    remaining_label.config(text=f"Remaining: {remaining_tasks}")

# Function to mark a task as complete or incomplete
def toggle_task_complete():
    selected_task_index = listbox.curselection()
    
    if selected_task_index:
        task = task_list[selected_task_index[0]]
        task["completed"] = not task["completed"]
        update_task_file()
        display_tasks()
    else:
        messagebox.showwarning("Warning", "You must select a task to mark complete.")

# Function to open task file and load tasks into the application
def open_task_file():
    try:
        with open("tasklist.txt", "r") as taskfile:
            tasks = taskfile.readlines()
        
        for task in tasks:
            if task.strip():
                task_info = task.strip().split('|')
                if len(task_info) == 2:
                    task_list.append({"task": task_info[0], "completed": task_info[1] == "True"})
                else:
                    print(f"Skipping invalid task format: {task}")
        
        display_tasks()
    except FileNotFoundError:
        with open('tasklist.txt', 'w') as file:
            file.close()

# Function to update the task file whenever a change is made
def update_task_file():
    with open("tasklist.txt", "w") as taskfile:
        for task_data in task_list:
            taskfile.write(f"{task_data['task']}|{task_data['completed']}\n")

# Function to create rounded corners for buttons
def create_rounded_button(parent, text, command, x, y):
    button = tk.Button(parent, text=text, command=command, relief='flat', bd=0, bg=button_color, fg=button_text_color, font=("Verdana", 10, "bold"), width=18)
    button.place(x=x, y=y)
    button.bind("<Enter>", lambda e: button.config(bg=button_hover_color))
    button.bind("<Leave>", lambda e: button.config(bg=button_color))
    return button

# Setting up the UI components

# Create background frame
background_frame = tk.Frame(root, bg=frame_bg_color)
background_frame.place(relwidth=1, relheight=1)

# Icon
image_icon = tk.PhotoImage(file="Images/task.png")
root.iconphoto(False, image_icon)

# Dock image
dock_image = tk.PhotoImage(file="Images/dock.png")
dock_label = tk.Label(background_frame, image=dock_image, bg=frame_bg_color)
dock_label.place(x=10, y=10)

# Note image
note_image = tk.PhotoImage(file="Images/task.png")
note_label = tk.Label(background_frame, image=note_image, bg=frame_bg_color)
note_label.place(x=290, y=10)

# Heading
heading = tk.Label(background_frame, text="ALL TASKS", font=("Helvetica", 18, "bold"), fg=header_color, bg=frame_bg_color)
heading.place(x=110, y=10)

# Main entry frame with background color
frame = tk.Frame(background_frame, bg="#F3DFE5", height=50)
frame.place(x=0, y=50, relwidth=1, height=50)

task_entry = tk.Entry(frame, width=20, font=("Arial", 14), bd=1, bg="#FFFFFF", fg=text_color)
task_entry.pack(side=tk.LEFT, padx=10, pady=5)

add_button = tk.Button(frame, text="ADD", font=("Arial", 14, "bold"), width=8, bg=button_color, fg=button_text_color, bd=0, command=add_task)
add_button.pack(side=tk.RIGHT, padx=10, pady=5)

# Task count and buttons frame
task_count_frame = tk.Frame(background_frame, bg=frame_bg_color)
task_count_frame.place(x=0, y=100, relwidth=1, height=50)  # Positioned above the task list

completed_label = tk.Label(task_count_frame, text="Completed: 0", font=("Arial", 10), bg=frame_bg_color, fg=text_color)
completed_label.pack(side=tk.LEFT, padx=10, pady=5)

remaining_label = tk.Label(task_count_frame, text="Remaining: 0", font=("Arial", 10), bg=frame_bg_color, fg=text_color)
remaining_label.pack(side=tk.RIGHT, padx=10, pady=5)

# Listbox and scrollbar
frame1 = tk.Frame(background_frame, bd=3, bg=frame_bg_color)
frame1.place(x=0, y=150, relwidth=1, relheight=0.4)  # Adjusted y-coordinate and height

listbox = tk.Listbox(frame1, font=("Courier New", 12), bg=bg_color, fg=text_color, cursor="hand2", selectbackground=button_color, selectmode=tk.SINGLE)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=2, pady=2, expand=True)
scrollbar = tk.Scrollbar(frame1)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Create a bottom frame for the buttons
button_frame = tk.Frame(background_frame, bg=frame_bg_color)
button_frame.place(x=0, y=450, relwidth=1, height=50)  # Positioned at the bottom of the task list

# Delete button
delete_icon = tk.PhotoImage(file="Images/delete.png")
delete_button = tk.Button(button_frame, image=delete_icon, bd=0, command=delete_task, bg=frame_bg_color)
delete_button.pack(side=tk.LEFT, padx=50, pady=10)  # Adjusted x-coordinate

# Mark complete button
create_rounded_button(button_frame, "MARK COMPLETE", toggle_task_complete, 150, 10)  # Adjusted x and y-coordinates

# Open the task file to load tasks
open_task_file()

# Run the application
root.mainloop()
