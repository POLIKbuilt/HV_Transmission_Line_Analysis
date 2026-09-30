import sys
import logging
import traceback
from PyQt5.QtWidgets import QApplication,QMainWindow, QLabel
from app_settings import load_settings, save_settings

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()])

def excepthook(exc_type, exc_value, exc_traceback):
    logging.critical("Uncaught exception: \n%s", "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))

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
app.setApplicationName("Transmission Analyzer")
app.setOrganizationName("polikstarik dev.")
app.setApplicationVersion("1.0.0")
window = App()
window.show()
sys.excepthook = excepthook
sys.exit(app.exec_())
