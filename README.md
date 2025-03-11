# Jax_TODO

A simple Task Scheduler built with **Tkinter** that allows users to add, remove, and reorder tasks using drag-and-drop functionality. Each task can have a due date and time, and completed tasks are displayed with a strikethrough effect.

---

## Features

- Add tasks with a description and due date/time
- Mark tasks as completed (strikethrough effect)
- Remove tasks easily
- Drag and drop to reorder tasks
- Dark mode UI

---

## Requirements

Ensure you have Python installed (>= 3.6). The application uses the following Python libraries:

- `tkinter` (built-in)
- `datetime`

No additional external dependencies are required.

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/task-scheduler.git
   cd task-scheduler
   ```

2. **Run the script:**
   ```sh
   python task_scheduler.py
   ```

---

## Usage

1. Enter the task name in the input field.
2. Optionally, specify the due date (format: `DDMMYY`) and time (format: `HHMM`).
3. Click the "Add" button to add the task.
4. Click the checkbox to mark a task as completed (strikethrough effect applied).
5. Click the ❌ button to delete a task.
6. Drag and drop tasks to reorder them.

---

## Notes

- If an invalid date or time is entered, the task will default to the next day.
- If no time is provided, the current time is used by default.

---

## License

MIT License

---

## Author

Your Name

Feel free to contribute to the project!


If an invalid date or time is entered, the task will default to the next day.

If no time is provided, the current time is used by default.
