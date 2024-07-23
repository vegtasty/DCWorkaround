import importlib
import os
import sqlite3
import sys
import threading
import time

from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFont, QPainter, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QProgressBar, \
    QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MainMenu(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):

        
        # Import the QSS file
        path = os.path.abspath('material.qss')
        with open(path, "r") as qss:
            self.setStyleSheet(qss.read())

        # Create a label for the title
        title = QLabel("DEFUSE CODE")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20))
        title.setStyleSheet("""
        background: transparent;
        color: white;
        """)

        start_game_button = QPushButton("START GAME")
        settings_button = QPushButton("SETTINGS")
        about_button = QPushButton("ABOUT")





        # Create a layout for the buttons
        layout = QVBoxLayout()

        layout.addWidget(title)
        layout.addWidget(start_game_button)
        layout.addWidget(settings_button)
        layout.addWidget(about_button)

        # Set the layout for the window
        self.setLayout(layout)

        # Connect buttons to methods
        # settings_button.clicked.connect(self.parent().show_settings_page)
        start_game_button.clicked.connect(self.parent().show_level_selection)

        about_button.clicked.connect(self.parent().show_about_page)


class LevelSelection(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        path = os.path.abspath('material.qss')
        with open(path, "r") as qss:
            self.setStyleSheet(qss.read())

        layout = QVBoxLayout()

        # Create buttons for level selection
        level1_button = QPushButton("Level 1")
        level2_button = QPushButton("Level 2")
        level3_button = QPushButton("Level 3")

        # Connect buttons to select_level method
        level1_button.clicked.connect(lambda: self.select_level("Level 1"))
        level2_button.clicked.connect(lambda: self.select_level("Level 2"))
        level3_button.clicked.connect(lambda: self.select_level("Level 3"))

        # Add buttons to layout
        layout.addWidget(level1_button)
        layout.addWidget(level2_button)
        layout.addWidget(level3_button)

        # Create a back button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.parent().show_main_menu)  # Zurück zum Hauptmenü wechseln
        layout.addWidget(back_button)

        self.setLayout(layout)

    def select_level(self, level_name):
        self.parent().show_game_window(level_name)


class SettingsPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Settings Page")
        layout.addWidget(label)
        self.setLayout(layout)


class AboutPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("About Defuse Code")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 20))

        # Informationen über die App
        info_text = """
        <p><strong>Defuse Code Game</strong></p>
        <p>Version: 1.0</p>
        <p>Created with ♥ by VT Defuse Code</p>
        <p>Description: Decrypt the code to defuse the bomb!</p>
        """
        info_label = QLabel(info_text)
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setWordWrap(True)

        layout.addWidget(label)
        layout.addWidget(info_label)

        # Zurück Button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.parent().show_main_menu)
        layout.addWidget(back_button)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Variablen zur Steuerung des Punktes
        self.point_color = Qt.red
        self.show_point = True

        self.setWindowTitle("Defuse Code")
        #change to fit screen
        self.setGeometry(300, 300, 1024, 580)  # Set initial position and size
        self.setFixedSize(1024, 580)  # Prevent resizing
        self.background_label = QLabel(self)
        #CHOOSE BACKGROUND IMAGE 2 TIMES
        self.set_background('image (2).webp')
        self.show_main_menu()



    def set_background(self, image_path):
        pixmap = QPixmap(image_path)
        self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding))
        self.background_label.resize(self.size())

    

    def resizeEvent(self, event):
        #CHOOSE BACKGROUND IMAGE 2 TIMES
        self.set_background('image (2).webp')
        super().resizeEvent(event)


    def show_main_menu(self):
        self.setCentralWidget(MainMenu(self))

    def show_level_selection(self):
        self.level_selection_page = LevelSelection(self)  # LevelSelection-Seite erstellen
        self.setCentralWidget(self.level_selection_page)  # LevelSelection-Seite anzeigen

    def show_settings_page(self):
        self.setCentralWidget(SettingsPage(self))

    def show_about_page(self):
        self.setCentralWidget(AboutPage(self))

    def show_success_page(self, elapsed_time):
        self.setCentralWidget(PuzzleSolvedPage(self, elapsed_time))

    def show_failure_page(self):
        self.setCentralWidget(PuzzleFailedPage(self))

    def show_game_window(self, level_name):
        self.setCentralWidget(GameWindow(self, level_name))  # GameWindow erstellen

    def paintEvent(self, event):
        super().paintEvent(event)  # Aufruf der Elternklasse-Methode

        if self.show_point:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(self.point_color))

            # Koordinaten des Punkts anpassen
            point_size = 20
            point_x = self.width() - point_size - 10
            point_y = self.height() - point_size - 10
            painter.drawEllipse(point_x, point_y, point_size, point_size)

    def set_point_color(self, color):
        self.point_color = color
        self.update()


class GameWindow(QWidget):

    max_steps = 1
    current_step = 0

    @staticmethod
    def set_max_steps(number):
        GameWindow.max_steps = number

    def __init__(self, parent, level_name):
        super().__init__(parent)
        self.paused = None
        self.main_window = parent
        self.is_running = None
        self.elapsed_time = None
        self.timer = None
        self.level_name = level_name
        self.stopwatch_label = None  # Declare as instance variable
        self.progress_bar = None  # Declare as instance variable
        self.init_ui()
        self.local_current_step = 0

    def init_ui(self):
        path = os.path.abspath('material.qss')
        with open(path, "r") as qss:
            self.setStyleSheet(qss.read())
        layout = QVBoxLayout()

        # Create title label
        title_label = QLabel(self.level_name)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 20))
        layout.addWidget(title_label)

        # Create stopwatch label
        self.stopwatch_label = QLabel("00:00.000")  # Assign to instance variable
        self.stopwatch_label.setAlignment(Qt.AlignCenter)
        self.stopwatch_label.setFont(QFont("Arial", 40))
        layout.addWidget(self.stopwatch_label)

        # Create progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Create buttons layout
        buttons_layout = QHBoxLayout()

        # Create start level button
        start_button = QPushButton("Start Level")
        start_button.clicked.connect(self.start_level)
        buttons_layout.addWidget(start_button)

        # Create pause level button
        abort_button = QPushButton("Pause Level")
        abort_button.clicked.connect(self.pause_level)
        buttons_layout.addWidget(abort_button)

        # Create reset level button
        abort_button = QPushButton("Reset Level")
        abort_button.clicked.connect(self.reset_level)
        buttons_layout.addWidget(abort_button)

        # Create abort level button
        abort_button = QPushButton("Abort Level")
        abort_button.clicked.connect(self.abort_level)
        buttons_layout.addWidget(abort_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Set background color
        self.setStyleSheet("background-color: white;")

        # Create timer for stopwatch
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stopwatch)

        # Initialize variables
        self.elapsed_time = QTime(0, 0)
        self.is_running = False

    def start_level(self):
        if not self.is_running:
            # Start the stopwatch
            from DefuseCode import DefuseCode
            DefuseCode.interrupt = False
            GameWindow.max_steps = 1
            GameWindow.current_step = 0
            if self.level_name == 'Level 1':
                import Level.Level1
                Level.Level1.Level1().start()
            elif self.level_name == 'Level 2':
                from Level.Level2 import Level2
                Level2().start()
            elif self.level_name == 'Level 3':
                from Level.Level3 import Level3
                Level3().start()
        self.timer.start(10)  # Update every 10 milliseconds (for milliseconds precision)
        self.is_running = True

    def pause_level(self):
        if self.is_running:
            # Stop the stopwatch
            self.timer.stop()
            self.paused = True

    def reset_level(self):
        if self.is_running:
            # Stop the stopwatch
            self.timer.stop()
            self.is_running = False
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_stopwatch)
            self.stopwatch_label.setText("00:00.000")  # Assign to instance variable
            from DefuseCode import DefuseCode
            DefuseCode.interrupt = True

    def abort_level(self):
        if self.is_running:
            # Stop the stopwatch
            reply = QMessageBox.question(self, "Abort Level", "Are you sure you want to abort the level?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.timer.stop()
                self.is_running = False
                from DefuseCode import DefuseCode
                DefuseCode.interrupt = True
                self.main_window.show_level_selection()  # LevelSelection-Seite erneut anzeigen
        else:
            self.main_window.show_level_selection()  # LevelSelection-Seite erneut anzeigen

    def update_stopwatch(self):
        self.elapsed_time = self.elapsed_time.addMSecs(10)  # Increase elapsed time by 10 milliseconds
        self.stopwatch_label.setText(self.elapsed_time.toString("mm:ss.zzz"))  # Format as minutes:seconds.milliseconds
        progress = int((GameWindow.current_step / GameWindow.max_steps) * 100)
        self.progress_bar.setValue(progress)

        from DefuseCode import DefuseCode
        if DefuseCode.interrupt:
            self.timer.stop()
            self.is_running = False
            self.main_window.show_failure_page()

        if progress == 100:
            self.timer.stop()
            self.is_running = False
            self.main_window.show_success_page(self.elapsed_time.toString("mm:ss.zzz"))


class PuzzleSolvedPage(QWidget):
    def __init__(self, parent, elapsed_time):
        super().__init__(parent)
        self.init_ui(elapsed_time)

    def init_ui(self, elapsed_time):
        path = os.path.abspath('material.qss')
        with open(path, "r") as qss:
            self.setStyleSheet(qss.read())
        layout = QVBoxLayout()

        # Create label for puzzle solved message
        puzzle_solved_label = QLabel("Rätsel gelöst")
        puzzle_solved_label.setAlignment(Qt.AlignCenter)
        puzzle_solved_label.setFont(QFont("Arial", 40))
        layout.addWidget(puzzle_solved_label)

        # Create label for elapsed time
        elapsed_time_label = QLabel(f"Benötigte Zeit: {elapsed_time}")
        elapsed_time_label.setAlignment(Qt.AlignCenter)
        elapsed_time_label.setFont(QFont("Arial", 20))
        layout.addWidget(elapsed_time_label)

        # Create back button
        back_button = QPushButton("Zurück zur Levelübersicht")
        back_button.clicked.connect(self.parent().show_level_selection)  # Zurück zur LevelSelection-Seite wechseln
        layout.addWidget(back_button)

        self.setLayout(layout)


class PuzzleFailedPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        path = os.path.abspath('material.qss')
        with open(path, "r") as qss:
            self.setStyleSheet(qss.read())
        layout = QVBoxLayout()

        # Create label for puzzle failed message
        puzzle_failed_label = QLabel("Rätsel fehlgeschlagen")
        puzzle_failed_label.setAlignment(Qt.AlignCenter)
        puzzle_failed_label.setFont(QFont("Arial", 40))
        layout.addWidget(puzzle_failed_label)

        # Create back button
        back_button = QPushButton("Zurück zur Levelübersicht")
        back_button.clicked.connect(self.parent().show_level_selection)  # Zurück zur LevelSelection-Seite wechseln
        layout.addWidget(back_button)

        self.setLayout(layout)


class UserInterface():
    def __init__(
            self
    ):
        super().__init__()
        self.window = None

    def run(self):
        app = QApplication(sys.argv)
        self.window = MainWindow()
        self.window.show()
        self.window.set_point_color(Qt.green)
        sys.exit(app.exec_())

    def change_button_color(self, color):
        self.window.set_point_color(color)

    def get_levels(self):
        conn = sqlite3.connect('defuse_code.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM LEVEL")
        rows = cursor.fetchall()
        return rows

    @staticmethod
    def instantiate_class(class_name):
        module_name = f"Level.{class_name}"
        module_path = os.path.join(os.path.dirname(__file__), "Level", f"{class_name}.py")
        if os.path.exists(module_path):
            module = importlib.import_module(module_name)
            class_object = getattr(module, class_name)
            instance = class_object()
            return instance
        else:
            print(module_path)
            raise ImportError(f"Module {module_name} not found")

    def initialize_level(self, level_class_name):
        instance = self.instantiate_class(level_class_name)
        instance.init_level("")
        instance.start()


if __name__ == '__main__':
    ui = UserInterface()
    ui.run()