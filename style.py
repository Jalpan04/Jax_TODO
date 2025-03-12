class TaskStyles:
    """
    Class for storing all styling information for the Task Manager application.
    This separation allows for easier maintenance and theme changes.
    """
    
    def __init__(self):
        # Theme colors - can be easily changed here to modify the entire app's appearance
        self.color_bg_dark = "#121212"
        self.color_bg_medium = "#1a1a1a"
        self.color_bg_light = "#232323"
        self.color_accent = "#ff9100"
        self.color_accent_hover = "#ffa122"
        self.color_accent_pressed = "#e57f00"
        self.color_text_primary = "white"
        self.color_text_secondary = "#a0a0a0"
        self.color_text_disabled = "#666666"
        self.color_border = "#3c3c3c"
        self.color_task_bg = "#252525"
        self.color_task_hover = "#2d2d2d"
        
    def main_window_style(self):
        """Main window styling"""
        return f"""
            QMainWindow {{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                               stop:0 {self.color_bg_medium}, stop:1 {self.color_bg_dark});
            }}
            QScrollBar:vertical {{
                border: none;
                background: #202020;
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: #505050;
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """
    
    def input_panel_style(self):
        """Input panel styling"""
        return f"""
            QFrame {{
                background-color: {self.color_bg_light};
                border-radius: 10px;
                border: 1px solid {self.color_border};
            }}
        """
    
    def entry_style(self):
        """Input field styling"""
        return f"""
            QLineEdit {{
                background-color: #2c2c2c;
                color: {self.color_text_primary};
                border: 1px solid {self.color_border};
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
                font-family: 'Segoe UI';
            }}
            QLineEdit:focus {{
                border: 1px solid {self.color_accent};
                background-color: #333333;
            }}
            QLineEdit::placeholder {{
                color: #888888;
            }}
        """
    
    def input_error_style(self):
        """Error styling for input fields"""
        return """
            QLineEdit {
                background-color: rgba(255, 0, 0, 0.1);
                color: white;
                border: 1px solid #ff0000;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
            }
        """
    
    def button_style(self):
        """Button styling"""
        return f"""
            QPushButton {{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                               stop:0 {self.color_accent}, stop:1 {self.color_accent_pressed});
                color: {self.color_text_primary};
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                               stop:0 {self.color_accent_hover}, stop:1 #ff8811);
            }}
            QPushButton:pressed {{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                               stop:0 {self.color_accent_pressed}, stop:1 #d67400);
            }}
        """
    
    def delete_button_style(self):
        """Delete button styling"""
        return f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                min-width: 30px;
                min-height: 30px;
                font-size: 25px;
                color: {self.color_accent};
                font-weight: bold;
            }}
            QPushButton:hover {{
                color: {self.color_accent_hover};
            }}
            QPushButton:pressed {{
                color: {self.color_accent_pressed};
            }}
        """

    def checkbox_style(self):
        """Checkbox styling with an orange fill when checked and a grey border"""
        return f"""
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #6c6c6c;
                background-color: {self.color_task_bg};
                transition: background-color 0.2s, border-color 0.2s;
            }}
            QCheckBox::indicator:hover {{
                border: 2px solid {self.color_accent};
                background-color: rgba(255, 145, 0, 0.2);
            }}
            QCheckBox::indicator:checked {{
                background-color: {self.color_accent};  /* Filled with orange when checked */
                border: 2px solid {self.color_task_bg};  /* Grey border when checked */
            }}
        """

    def task_normal_style(self):
        """Normal task styling"""
        return f"""
            QFrame {{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                               stop:0 #323232, stop:1 {self.color_task_bg});
                border-radius: 8px;
                border: 1px solid {self.color_border};
            }}
        """
    
    def task_completed_style(self):
        """Completed task styling"""
        return """
            QFrame {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                               stop:0 #2a2a2a, stop:1 #222222);
                border-radius: 8px;
                border: 1px solid #333333;
            }
        """
    
    def task_hover_style(self):
        """Task hover styling"""
        return f"""
            QFrame {{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                               stop:0 #3a3a3a, stop:1 {self.color_task_hover});
                border-radius: 8px;
                border: 1px solid #4c4c4c;
            }}
        """
    
    def task_dragging_style(self):
        """Task dragging styling"""
        return """
            QFrame {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                               stop:0 #444444, stop:1 #333333);
                border-radius: 8px;
                border: 1px solid #555555;
            }
        """
    
    def task_delete_style(self):
        """Task delete styling"""
        return """
            QFrame {
                background-color: rgba(255, 0, 0, 0.2);
                border-radius: 8px;
                border: 1px solid #3c3c3c;
            }
        """
