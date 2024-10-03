import subprocess
import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QStackedWidget
from PySide6.QtCore import Qt, QPoint, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QPalette

class DarkPalette:
    BACKGROUND = QColor("#1E1E1E")  # Dark background
    FOREGROUND = QColor("#FFFFFF")  # White (for high contrast elements)
    ACCENT = QColor("#2C2C2C")      # Slightly lighter than background
    SECONDARY = QColor("#252525")   # Between background and accent
    BORDER = QColor("#333333")      # Slightly lighter for borders
    BUTTON_NORMAL = QColor("#2A2A2A")  # Slightly lighter than background
    BUTTON_HOVER = QColor("#3A3A3A")   # Lighter than normal button
    BUTTON_PRESSED = QColor("#1A1A1A") # Darker than normal button
    TEXT = QColor("#CCCCCC")        # Light gray for text (unchanged)

class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title = QLabel("Berry's Utils")  # Updated window title here
        self.title.setStyleSheet(f"color: {DarkPalette.TEXT.name()}; padding: 4px;")
        layout.addWidget(self.title)

        layout.addStretch(1)

        self.minimize_button = QPushButton("—")
        self.minimize_button.clicked.connect(self.parent.showMinimized)
        layout.addWidget(self.minimize_button)

        self.maximize_button = QPushButton("□")
        self.maximize_button.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.maximize_button)

        self.close_button = QPushButton("✕")
        self.close_button.clicked.connect(self.parent.close)
        layout.addWidget(self.close_button)

        self.start = QPoint(0, 0)
        self.pressing = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = self.mapToGlobal(event.position().toPoint())
            self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            end = self.mapToGlobal(event.position().toPoint())
            movement = end - self.start
            self.parent.move(self.parent.pos() + movement)
            self.start = end

    def mouseReleaseEvent(self, event):
        self.pressing = False

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.maximize_button.setText("□")
        else:
            self.parent.showMaximized()
            self.maximize_button.setText("❐")

class TabButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(40, 100)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {DarkPalette.SECONDARY.name()};
                border: none;
                border-top-left-radius: 10px;
                border-bottom-left-radius: 10px;
                color: {DarkPalette.TEXT.name()};
                padding: 5px;
            }}
            QPushButton:checked {{
                background-color: {DarkPalette.ACCENT.name()};
            }}
            QPushButton:hover:!checked {{
                background-color: {DarkPalette.BUTTON_HOVER.name()};
            }}
        """)
        self.setCheckable(True)

class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(500, 300)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        self.main_layout = QHBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Tab bar
        self.tab_bar = QWidget()
        self.tab_bar.setFixedWidth(40)
        self.tab_layout = QVBoxLayout(self.tab_bar)
        self.tab_layout.setContentsMargins(0, 40, 0, 0)
        self.tab_layout.setSpacing(10)

        self.tab_buttons = []
        tab_names = ["Utils", "Tab 2", "Tab 3", "Tab 4"]
        for i, name in enumerate(tab_names):
            tab = TabButton(name)
            self.tab_layout.addWidget(tab)
            self.tab_buttons.append(tab)
            tab.clicked.connect(lambda checked, index=i: self.switch_tab(index))

        self.tab_layout.addStretch()
        self.main_layout.addWidget(self.tab_bar)

        # Content area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        self.title_bar = TitleBar(self)
        self.content_layout.addWidget(self.title_bar)

        self.stacked_widget = QStackedWidget()
        
        # Tab 1 content with MassGrave button
        tab1_widget = QWidget()
        tab1_layout = QVBoxLayout(tab1_widget)
        tab1_layout.setAlignment(Qt.AlignCenter)
        
        # MassGrave button
        mass_grave_button = QPushButton("MassGrave")
        mass_grave_button.setStyleSheet(self.get_button_style())
        mass_grave_button.clicked.connect(self.execute_skibidi)
        tab1_layout.addWidget(mass_grave_button)
        
        # Tooltip-like label below the MassGrave button
        info_label = QLabel("May take a while to load")
        info_label.setStyleSheet(f"color: {DarkPalette.TEXT.name()}; font-size: 12px;")
        info_label.setAlignment(Qt.AlignCenter)
        tab1_layout.addWidget(info_label)
        
        # Add some spacing between the button and the label
        tab1_layout.setSpacing(5)
        
        self.stacked_widget.addWidget(tab1_widget)

        for i in range(1, 4):  # Changed to start from 1 and create only 3 additional tabs
            page = QWidget()
            page_layout = QVBoxLayout(page)
            label = QLabel(f"Content for Tab {i+1}")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(f"color: {DarkPalette.TEXT.name()}; font-size: 16px;")
            page_layout.addWidget(label)
            self.stacked_widget.addWidget(page)

        self.content_layout.addWidget(self.stacked_widget)
        self.main_layout.addWidget(self.content_widget)

        self.snowflakes = []
        self.create_snowflakes()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_snow)
        self.timer.start(50)

        self.tab_buttons[0].setChecked(True)

    def create_snowflakes(self):
        self.snowflakes = [
            Snowflake(
                random.randint(0, self.width()),
                random.randint(-50, self.height()),
                random.randint(2, 5)
            ) for _ in range(50)
        ]

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.create_snowflakes()  # Recreate snowflakes when window is resized

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw rounded rectangle background
        painter.setBrush(DarkPalette.BACKGROUND)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

        # Draw rounded border
        painter.setPen(QPen(DarkPalette.BORDER, 2))
        painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 10, 10)

        # Draw snowflakes
        painter.setBrush(QBrush(QColor(255, 255, 255, 100)))
        painter.setPen(Qt.NoPen)
        for flake in self.snowflakes:
            painter.drawEllipse(QRectF(flake.x, flake.y, flake.size, flake.size))

    def update_snow(self):
        for flake in self.snowflakes:
            flake.fall(self.height(), self.width())
        self.update()

    def switch_tab(self, index):
        for i, button in enumerate(self.tab_buttons):
            button.setChecked(i == index)
        self.stacked_widget.setCurrentIndex(index)
        
        # Update the title bar text when switching tabs, but keep "Berry's Utils"
        tab_names = ["Utils", "Tab 2", "Tab 3", "Tab 4"]
        self.title_bar.title.setText(f"Berry's Utils - {tab_names[index]}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def get_button_style(self):
        return f"""
            QPushButton {{
                background-color: {DarkPalette.BUTTON_NORMAL.name()};
                border: none;
                color: {DarkPalette.TEXT.name()};
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {DarkPalette.BUTTON_HOVER.name()};
            }}
            QPushButton:pressed {{
                background-color: {DarkPalette.BUTTON_PRESSED.name()};
            }}
        """

    def print_click_me(self):
        print("Button clicked!")

    def print_hello_world(self):
        print("Hello World!")

    def execute_skibidi(self):
        try:
            import subprocess
            subprocess.run(["python", "Skibidi.py"])
        except Exception as e:
            print(f"Error executing Skibidi.py: {e}")

class Snowflake:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.speed = random.uniform(1, 3)

    def fall(self, height, width):
        self.y += self.speed
        if self.y > height:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, width)
        if self.x > width:
            self.x = random.randint(0, width)

def main():
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()