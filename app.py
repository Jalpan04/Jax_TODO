import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFrame, QVBoxLayout, QHBoxLayout,
                             QCheckBox, QLabel, QPushButton, QLineEdit, QWidget,
                             QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem)
from PyQt6.QtCore import Qt, QPoint, QMimeData, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont, QDrag, QFontDatabase, QColor, QIcon, QPalette, QLinearGradient, QPainter
from datetime import datetime, timedelta

from style import TaskStyles

class Task(QFrame):
    def __init__(self, parent, text, due_datetime, on_delete, on_toggle):
        super().__init__(parent)
        self.parent = parent
        self.text = text
        self.due_datetime = due_datetime
        self.on_delete = on_delete
        self.on_toggle = on_toggle
        self.completed = False
        self.drag_start_position = None
        self.styles = TaskStyles()

        # Add shadow effect for depth
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

        # Setup task appearance
        self.setStyleSheet(self.styles.task_normal_style())
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedHeight(60)  # Consistent height for all tasks

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)

        # Checkbox
        self.check_box = QCheckBox()
        self.check_box.toggled.connect(self.toggle_done)
        self.check_box.setStyleSheet(self.styles.checkbox_style())
        self.check_box.setCheckable(True)
        self.check_box.setText("")  # No text beside the checkbox
        layout.addWidget(self.check_box)

        # Task info container
        task_info_container = QWidget()
        task_info_container.setStyleSheet("background: transparent; border: none;")
        task_info_layout = QVBoxLayout(task_info_container)
        task_info_layout.setContentsMargins(0, 0, 0, 0)
        task_info_layout.setSpacing(2)

        # Task Label - main text
        self.label = QLabel(self.text)
        self.label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.label.setStyleSheet("color: white; background: transparent;")
        task_info_layout.addWidget(self.label)

        # Due date label - secondary text
        self.due_date_label = QLabel(f"Due: {self.due_datetime.strftime('%d/%m/%y %H:%M')}")
        self.due_date_label.setFont(QFont("Segoe UI", 9))
        self.due_date_label.setStyleSheet("color: #a0a0a0; background: transparent;")
        task_info_layout.addWidget(self.due_date_label)

        layout.addWidget(task_info_container, 1)  # Stretch factor of 1 to expand

        # Delete Button
        self.delete_button = QPushButton("✕")
        self.delete_button.setStyleSheet(self.styles.delete_button_style())
        self.delete_button.clicked.connect(self.delete_task)
        layout.addWidget(self.delete_button)

        # Enable dragging
        self.setMouseTracking(True)

        # Initialize drag properties
        self.setProperty("dragging", False)
        self.setProperty("dropBefore", False)
        self.setProperty("dropAfter", False)

    def toggle_done(self, checked):
        """Mark task as completed or uncompleted with animation"""
        self.completed = checked

        if checked:
            # Change task appearance when completed
            self.label.setStyleSheet("color: #888888; text-decoration: line-through; background: transparent;")
            self.due_date_label.setStyleSheet("color: #666666; background: transparent;")
            self.setStyleSheet(self.styles.task_completed_style())
            # Remove the priority indicator line
        else:
            # Restore original appearance
            self.label.setStyleSheet("color: white; background: transparent;")
            self.due_date_label.setStyleSheet("color: #a0a0a0; background: transparent;")
            self.setStyleSheet(self.styles.task_normal_style())
            # Remove the priority indicator line

        self.on_toggle(self)

    def delete_task(self):
        """Delete the task with fade out animation"""
        self.setStyleSheet(self.styles.task_delete_style())
        # Could add a QPropertyAnimation here for fade out effect
        self.on_delete(self)

    def enterEvent(self, event):
        """Mouse hover enter effect"""
        self.setStyleSheet(self.styles.task_hover_style())
        # Increase shadow effect
        shadow = self.graphicsEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 3)

    def leaveEvent(self, event):
        """Mouse hover leave effect"""
        if not self.completed:
            self.setStyleSheet(self.styles.task_normal_style())
        else:
            self.setStyleSheet(self.styles.task_completed_style())
        # Reset shadow effect
        shadow = self.graphicsEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 2)

    def mousePressEvent(self, event):
        """Handle mouse press events for drag and drop"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position().toPoint()
            # Set property to track dragging state
            self.setProperty("dragging", True)
            # Highlight the task when dragging starts
            self.setStyleSheet(self.styles.task_dragging_style())

    def mouseMoveEvent(self, event):
        """Handle mouse move events for drag and drop"""
        if not (event.buttons() & Qt.MouseButton.LeftButton) or not self.drag_start_position:
            return

        # Check if the minimum drag distance is met
        if (event.position().toPoint() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        # Start drag
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText("task")  # Identifier for the dragged content
        drag.setMimeData(mime_data)

        # Create a visual representation during dragging
        # Capture the widget appearance
        pixmap = self.grab()
        # Make it semi-transparent
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), QColor(0, 0, 0, 160))
        painter.end()

        drag.setPixmap(pixmap)
        drag.setHotSpot(event.position().toPoint())

        # Perform the drag operation
        drag.exec(Qt.DropAction.MoveAction)

    def mouseReleaseEvent(self, event):
        """Handle mouse release events"""
        # Reset dragging state
        self.setProperty("dragging", False)
        # Reset styling based on completion status
        if not self.completed:
            self.setStyleSheet(self.styles.task_normal_style())
        else:
            self.setStyleSheet(self.styles.task_completed_style())
        self.drag_start_position = None


class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Scheduler")
        self.setGeometry(100, 100, 500, 650)
        self.styles = TaskStyles()

        # Set application style
        self.setStyleSheet(self.styles.main_window_style())

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # App title and header
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 15)

        title_label = QLabel("Task Scheduler")
        title_label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #ff9100;")
        header_layout.addWidget(title_label)

        date_label = QLabel(f"Today: {datetime.now().strftime('%A, %d %B %Y')}")
        date_label.setFont(QFont("Segoe UI", 12))
        date_label.setStyleSheet("color: #a0a0a0;")
        header_layout.addWidget(date_label)

        main_layout.addWidget(header)

        # Task list with scroll
        self.task_list_widget = QWidget()
        self.task_list_layout = QVBoxLayout(self.task_list_widget)
        self.task_list_layout.setSpacing(10)  # Increased spacing between tasks
        self.task_list_layout.setContentsMargins(5, 5, 5, 5)
        self.task_list_layout.addStretch(1)  # Push content to the top

        # Add scroll effect to the task list
        scroll_area = QWidget()
        scroll_layout = QVBoxLayout(scroll_area)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.addWidget(self.task_list_widget)

        main_layout.addWidget(scroll_area, 1)  # Stretch factor to expand

        # Input section
        input_widget = QFrame()
        input_widget.setStyleSheet(self.styles.input_panel_style())

        # Add shadow to input panel
        input_shadow = QGraphicsDropShadowEffect()
        input_shadow.setBlurRadius(20)
        input_shadow.setColor(QColor(0, 0, 0, 100))
        input_shadow.setOffset(0, 4)
        input_widget.setGraphicsEffect(input_shadow)

        input_layout = QVBoxLayout(input_widget)
        input_layout.setContentsMargins(15, 15, 15, 15)
        input_layout.setSpacing(15)

        # Add "Add New Task" header
        new_task_label = QLabel("Add New Task")
        new_task_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        new_task_label.setStyleSheet("color: white;")
        input_layout.addWidget(new_task_label)

        # Task name input with icon
        task_input_container = QWidget()
        task_input_layout = QHBoxLayout(task_input_container)
        task_input_layout.setContentsMargins(0, 0, 0, 0)

        task_icon = QLabel("📋")  # Task icon
        task_icon.setStyleSheet("font-size: 16px;")
        task_input_layout.addWidget(task_icon)

        self.task_entry = QLineEdit()
        self.task_entry.setPlaceholderText("What needs to be done?")
        self.task_entry.setStyleSheet(self.styles.entry_style())
        self.task_entry.setMinimumHeight(40)
        task_input_layout.addWidget(self.task_entry)

        input_layout.addWidget(task_input_container)

        # Date and time inputs
        datetime_container = QWidget()
        datetime_layout = QHBoxLayout(datetime_container)
        datetime_layout.setContentsMargins(0, 0, 0, 0)
        datetime_layout.setSpacing(10)

        # Date Entry with icon
        date_container = QWidget()
        date_layout = QHBoxLayout(date_container)
        date_layout.setContentsMargins(0, 0, 0, 0)

        date_icon = QLabel("📅")  # Calendar icon
        date_icon.setStyleSheet("font-size: 16px;")
        date_layout.addWidget(date_icon)

        self.date_entry = QLineEdit()
        self.date_entry.setPlaceholderText("DDMMYY")
        self.date_entry.setStyleSheet(self.styles.entry_style())
        self.date_entry.setMinimumHeight(40)
        date_layout.addWidget(self.date_entry)

        datetime_layout.addWidget(date_container)

        # Time Entry with icon
        time_container = QWidget()
        time_layout = QHBoxLayout(time_container)
        time_layout.setContentsMargins(0, 0, 0, 0)

        time_icon = QLabel("🕒")  # Clock icon
        time_icon.setStyleSheet("font-size: 16px;")
        time_layout.addWidget(time_icon)

        self.time_entry = QLineEdit()
        self.time_entry.setPlaceholderText("HHMM")
        self.time_entry.setStyleSheet(self.styles.entry_style())
        self.time_entry.setMinimumHeight(40)
        time_layout.addWidget(self.time_entry)

        datetime_layout.addWidget(time_container)

        input_layout.addWidget(datetime_container)

        # Add Task Button
        self.add_btn = QPushButton("Add Task")
        self.add_btn.setStyleSheet(self.styles.button_style())
        self.add_btn.setMinimumHeight(45)
        self.add_btn.clicked.connect(self.add_task)
        input_layout.addWidget(self.add_btn)

        main_layout.addWidget(input_widget)

        # Store tasks
        self.tasks = []
        self.setAcceptDrops(True)

    def add_task(self):
        """Adds a new task with animation"""
        task_text = self.task_entry.text().strip()
        date_text = self.date_entry.text().strip()
        time_text = self.time_entry.text().strip()

        if not task_text:  # Prevent empty task addition
            # Could add a subtle shake animation to the input field
            self.task_entry.setStyleSheet(self.styles.input_error_style())
            # Reset styling after brief period
            QApplication.processEvents()
            import time
            time.sleep(0.3)
            self.task_entry.setStyleSheet(self.styles.entry_style())
            return

        due_datetime = self.get_due_datetime(date_text, time_text)

        # Create new task
        task = Task(
            self.task_list_widget,
            task_text,
            due_datetime,
            self.remove_task,
            self.toggle_task
        )

        # Insert at top of the list
        self.task_list_layout.insertWidget(0, task)
        self.tasks.append(task)

        # Clear inputs
        self.task_entry.clear()
        self.date_entry.clear()
        self.time_entry.clear()

        self.task_entry.setFocus()  # Set focus back to task entry

    def get_due_datetime(self, date_text, time_text):
        """Parses date and time, applies defaults if empty"""
        now = datetime.now()

        # Handle time input
        if time_text and time_text.isdigit() and len(time_text) == 4:
            try:
                hours, minutes = int(time_text[:2]), int(time_text[2:])
                if 0 <= hours < 24 and 0 <= minutes < 60:
                    pass  # Valid time
                else:
                    hours, minutes = now.hour, now.minute
            except ValueError:
                hours, minutes = now.hour, now.minute
        else:
            hours, minutes = now.hour, now.minute

        # Handle date input
        if date_text and date_text.isdigit() and len(date_text) == 6:
            try:
                day, month, year = int(date_text[:2]), int(date_text[2:4]), int(date_text[4:])
                year += 2000  # Convert YY to YYYY
            except ValueError:
                day, month, year = now.day, now.month, now.year
        else:
            day, month, year = now.day, now.month, now.year

        try:
            return datetime(year, month, day, hours, minutes)
        except ValueError:
            return now + timedelta(days=1)  # Default: Next day if invalid

    def remove_task(self, task):
        """Removes the task from the list"""
        if task in self.tasks:
            self.task_list_layout.removeWidget(task)
            task.deleteLater()
            self.tasks.remove(task)

    def toggle_task(self, task):
        """Handle task toggle event"""
        if task is None:
            print("Error: Task is None!")
            return  # Avoid further execution if the task is invalid

        task.completed = not task.completed  # Toggle completion status

        print(f"Task '{task}' toggled. Completed: {task.completed}")

        if task in self.tasks:
            self.tasks.remove(task)
            if task.completed:
                self.tasks.append(task)  # Move to end if completed
            else:
                self.tasks.insert(0, task)  # Move to beginning if active
            self.update_task_order()

    def update_task_order(self):
        """Updates the order of tasks in the UI"""
        # Remove all tasks safely
        for task in self.tasks:
            if task is not None and task in self.task_list_layout.children():
                self.task_list_layout.removeWidget(task)
                task.setParent(None)  # Detach widget safely

        # Re-add them in the correct order
        for i, task in enumerate(self.tasks):
            if task is not None:
                self.task_list_layout.insertWidget(i, task)

    def dragEnterEvent(self, event):
        """Handle when drag enters the main window"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            # Highlight potential drop area
            self.highlight_drop_zone(event.position().y())

    def dragMoveEvent(self, event):
        """Handle drag movement over the window"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            # Update highlighted drop area
            self.highlight_drop_zone(event.position().y())

    def dragLeaveEvent(self, event):
        """Handle when drag leaves the window"""
        # Remove any drop zone highlighting
        self.clear_drop_highlighting()

    def highlight_drop_zone(self, y_position):
        """Highlights the potential drop zone"""
        source_task = None
        target_index = -1

        # Find the dragged task
        for task in self.tasks:
            if task.property("dragging"):
                source_task = task
                break

        # Determine where it would be dropped
        for i, task in enumerate(self.tasks):
            if task == source_task:
                continue

            task_y = task.y()
            task_height = task.height()

            # Clear previous styling
            task.setProperty("dropBefore", False)
            task.setProperty("dropAfter", False)

            # If cursor is above the middle of this task
            if y_position < task_y + (task_height / 2):
                task.setProperty("dropBefore", True)
                task.setStyleSheet(task.styleSheet())  # Force style update
                target_index = i
                break
            # If this is the last task and cursor is below it
            elif i == len(self.tasks) - 1:
                task.setProperty("dropAfter", True)
                task.setStyleSheet(task.styleSheet())  # Force style update
                target_index = i + 1

        # Apply visual styling to all tasks based on properties
        for task in self.tasks:
            if task.property("dropBefore"):
                # Add top border or background highlight
                task.setStyleSheet(task.styleSheet() + "border-top: 2px solid #ff9100;")
            elif task.property("dropAfter"):
                # Add bottom border or background highlight
                task.setStyleSheet(task.styleSheet() + "border-bottom: 2px solid #ff9100;")

    def clear_drop_highlighting(self):
        """Clears all drop zone highlighting"""
        for task in self.tasks:
            task.setProperty("dropBefore", False)
            task.setProperty("dropAfter", False)
            # Reset to normal styling based on completion status
            if task.completed:
                task.setStyleSheet(self.styles.task_completed_style())
            else:
                task.setStyleSheet(self.styles.task_normal_style())

    def dropEvent(self, event):
        """Handle drop events to reorder tasks"""
        if event.mimeData().hasText() and event.source() in self.tasks:
            source_task = event.source()
            drop_y = event.position().y()

            # Determine insertion index based on drop position
            insert_index = 0
            for i, task in enumerate(self.tasks):
                if task == source_task:
                    continue

                task_y = task.y() + task.height() / 2
                if drop_y > task_y:
                    insert_index = i + 1

            # Only reorder if the position changed
            current_index = self.tasks.index(source_task)
            if current_index != insert_index and current_index + 1 != insert_index:
                # Remove from current position
                self.tasks.remove(source_task)

                # Insert at new position
                if current_index < insert_index:
                    insert_index -= 1  # Adjust index after removal

                self.tasks.insert(insert_index, source_task)
                self.update_task_order()

            # Clear any highlighting
            self.clear_drop_highlighting()
            event.acceptProposedAction()


def main():
    app = QApplication(sys.argv)

    # Try to load the preferred fonts if available
    QFontDatabase.addApplicationFont("SegoeUI.ttf")  # Load Segoe UI if available

    window = TaskManager()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
