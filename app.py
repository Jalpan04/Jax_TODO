import tkinter as tk
from tkinter import font
from datetime import datetime, timedelta


class Task(tk.Frame):
    def __init__(self, parent, text, due_datetime, on_delete, on_toggle, on_drag_start, on_drag_motion, on_drag_drop):
        super().__init__(parent, bg="#2c2c2c", bd=2, relief=tk.RAISED)
        self.parent = parent
        self.text = text
        self.due_datetime = due_datetime
        self.on_delete = on_delete
        self.on_toggle = on_toggle
        self.on_drag_start = on_drag_start
        self.on_drag_motion = on_drag_motion
        self.on_drag_drop = on_drag_drop
        self.completed = False

        # Font Settings (Fallback if Geo isn't available)
        try:
            self.task_font = font.Font(family="Geo", size=12, weight="bold")
        except:
            self.task_font = font.Font(size=12, weight="bold")

        # Checkbox Button
        self.check_var = tk.BooleanVar()
        self.check_button = tk.Checkbutton(
            self, variable=self.check_var, command=self.toggle_done, bg="#2c2c2c",
            activebackground="#2c2c2c"
        )
        self.check_button.pack(side=tk.LEFT, padx=5)

        # Task Label (Expands to fill space)
        self.label = tk.Label(self, text=self.get_display_text(), font=self.task_font, fg="white", bg="#2c2c2c", anchor="w")
        self.label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Delete Button
        self.delete_button = tk.Button(self, text="❌", command=self.delete_task, bg="#2c2c2c", fg="#ff9100",
                                       relief=tk.FLAT, width=3)
        self.delete_button.pack(side=tk.RIGHT, padx=5)

        # Drag & Drop Support (Now on Entire Task)
        self.bind_events(self)
        self.bind_events(self.label)
        self.bind_events(self.check_button)
        self.bind_events(self.delete_button)

    def get_display_text(self):
        """Returns formatted task text with date and time"""
        formatted_date = self.due_datetime.strftime("%d/%m/%y %H:%M")
        return f"{self.text}  (Due: {formatted_date})"

    def bind_events(self, widget):
        """Bind drag events to all child widgets so entire module is draggable"""
        widget.bind("<ButtonPress-1>", self.start_drag)
        widget.bind("<B1-Motion>", self.on_drag_motion)
        widget.bind("<ButtonRelease-1>", self.on_drag_drop)

    def toggle_done(self):
        """Mark task as completed or uncompleted"""
        self.completed = not self.completed
        new_font = self.task_font.copy()
        new_font.config(overstrike=self.completed)

        if self.completed:
            self.label.config(fg="#888888", font=new_font)  # Dull color with strikethrough
        else:
            self.label.config(fg="white", font=self.task_font)

        self.on_toggle(self)

    def delete_task(self):
        """Delete the task"""
        self.on_delete(self)

    def start_drag(self, event):
        """Starts dragging"""
        self.on_drag_start(self)


class TaskManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Scheduler")
        self.geometry("450x550")
        self.configure(bg="#1e1e1e")  # Dark Mode

        self.tasks = []
        self.dragged_task = None
        self.y_offset = 0  # Store Y offset of cursor inside the dragged task

        # Task List Frame
        self.task_frame = tk.Frame(self, bg="#1e1e1e")
        self.task_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Bottom Input Frame
        self.input_frame = tk.Frame(self, bg="#1e1e1e")
        self.input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Task Entry Box
        self.task_entry = tk.Entry(self.input_frame, font=("Geo", 12, "bold"), bd=2, relief=tk.GROOVE,
                                   bg="#2c2c2c", fg="white", insertbackground="white", width=18)
        self.task_entry.pack(side=tk.LEFT, padx=5)

        # Date Entry Box with Placeholder
        self.date_entry = tk.Entry(self.input_frame, font=("Geo", 12, "bold"), bd=2, relief=tk.GROOVE,
                                   bg="#2c2c2c", fg="#888888", insertbackground="white", width=8)
        self.date_entry.pack(side=tk.LEFT, padx=5)
        self.date_entry.insert(0, "DDMMYY")

        # Time Entry Box with Placeholder
        self.time_entry = tk.Entry(self.input_frame, font=("Geo", 12, "bold"), bd=2, relief=tk.GROOVE,
                                   bg="#2c2c2c", fg="#888888", insertbackground="white", width=6)
        self.time_entry.pack(side=tk.LEFT, padx=5)
        self.time_entry.insert(0, "HHMM")

        # Add Task Button
        self.add_btn = tk.Button(self.input_frame, text="Add", command=self.add_task, **self.btn_style())
        self.add_btn.pack(side=tk.RIGHT, padx=5)

        # Bind Placeholder Logic
        self.date_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.date_entry, "DDMMYY"))
        self.date_entry.bind("<FocusOut>", lambda e: self.restore_placeholder(self.date_entry, "DDMMYY"))

        self.time_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.time_entry, "HHMM"))
        self.time_entry.bind("<FocusOut>", lambda e: self.restore_placeholder(self.time_entry, "HHMM"))


    def btn_style(self):
        """Returns button styling"""
        return {
            "font": ("Geo", 12, "italic"), "bg": "#ff9100", "fg": "black",
            "bd": 0, "relief": tk.FLAT, "width": 8, "height": 1,
            "activebackground": "#d67c00", "activeforeground": "black",
            "cursor": "hand2"
        }

    def clear_placeholder(self, entry_widget, placeholder_text):
        """Clears placeholder text when clicking inside"""
        if entry_widget.get() == placeholder_text:
            entry_widget.delete(0, tk.END)
            entry_widget.config(fg="white")  # Change text color to normal

    def restore_placeholder(self, entry_widget, placeholder_text):
        """Restores placeholder text when losing focus if empty"""
        if not entry_widget.get():
            entry_widget.insert(0, placeholder_text)
            entry_widget.config(fg="#888888")  # Make placeholder text gray


    def add_task(self):
        """Adds a new task module"""
        task_text = self.task_entry.get().strip()
        date_text = self.date_entry.get().strip()
        time_text = self.time_entry.get().strip()

        if not task_text:  # Prevent empty task addition
            return

        due_datetime = self.get_due_datetime(date_text, time_text)

        task = Task(
            self.task_frame, task_text, due_datetime, self.remove_task, self.keep_order,
            self.start_drag, self.move_task, self.drop_task
        )
        task.pack(fill=tk.X, pady=2, padx=5)
        self.tasks.append(task)

        # Clear inputs
        self.task_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)

    def get_due_datetime(self, date_text, time_text):
        """Parses date and time, applies defaults if empty"""
        now = datetime.now()

        # Handle time input
        if time_text and time_text.isdigit() and len(time_text) == 4:
            hours, minutes = int(time_text[:2]), int(time_text[2:])
        else:
            hours, minutes = now.hour, now.minute

        # Handle date input
        if date_text and date_text.isdigit() and len(date_text) == 6:
            day, month, year = int(date_text[:2]), int(date_text[2:4]), int(date_text[4:])
            year += 2000  # Convert YY to YYYY
        else:
            day, month, year = now.day, now.month, now.year

        try:
            return datetime(year, month, day, hours, minutes)
        except ValueError:
            return now + timedelta(days=1)  # Default: Next day if invalid

    def remove_task(self, task):
        """Removes the task from the list"""
        if task in self.tasks:
            task.destroy()
            self.tasks.remove(task)

    def keep_order(self, task):
        """Ensures order remains unchanged when toggling completion"""
        pass

    def start_drag(self, task):
        """Starts dragging a task"""
        self.dragged_task = task
        task.lift()
        task.config(bg="#444444")  # Highlight the task while dragging
        self.y_offset = task.winfo_pointery() - task.winfo_rooty()
        self.x_offset = task.winfo_pointerx() - task.winfo_rootx()

    def move_task(self, event):
        """Moves the dragged task smoothly"""
        if not self.dragged_task:
            return

        # Calculate new Y position
        y_pos = event.y_root - self.task_frame.winfo_rooty() - self.y_offset

        # Ensure the dragged task stays centered
        frame_width = self.task_frame.winfo_width()
        task_width = self.dragged_task.winfo_width()
        x_pos = (frame_width - task_width) // 2  # Centering formula

        # Move the task to new position while keeping it centered
        self.dragged_task.place(x=x_pos, y=y_pos)

        # Determine new order
        for i, t in enumerate(self.tasks):
            if t == self.dragged_task:
                continue

            t_y = t.winfo_y() + t.winfo_height() // 2
            if y_pos < t_y:
                self.tasks.remove(self.dragged_task)
                self.tasks.insert(i, self.dragged_task)
                self.update_task_order()
                break

    def drop_task(self, event):
        """Drops the dragged task and maximizes it on right-click release"""
        if not self.dragged_task:
            return

        if event.num == 3:  # Right-click release (Right Mouse Button)
            # Expand the module
            self.dragged_task.config(width=self.task_frame.winfo_width(), height=100)  # Adjust height as needed

        self.dragged_task.config(bg="#2c2c2c")  # Reset color
        self.dragged_task.place_forget()  # Reset position
        self.update_task_order()
        self.dragged_task = None

    def update_task_order(self):
        """Updates the order of tasks on the UI"""
        for t in self.tasks:
            t.pack_forget()
            t.pack(fill=tk.X, pady=2, padx=5)


if __name__ == "__main__":
    app = TaskManager()
    app.mainloop()
