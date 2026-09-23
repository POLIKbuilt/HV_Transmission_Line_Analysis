import sys
from PyQt5.QtWidgets import QApplication,QMainWindow, QLabel
from app_settings import load_settings, save_settings

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()


        self.setWindowTitle("Transmission Analyzer")
        self.setGeometry(300, 300, self.settings["window_width"], self.settings["window_height"])
        self.setCentralWidget(QLabel(f"Theme: {self.settings['theme']}"))

    def closeEvent(self, event):
        self.settings["window_width"] = self.width()
        self.settings["window_height"] = self.height()
        save_settings(self.settings)
        event.accept()

app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())
