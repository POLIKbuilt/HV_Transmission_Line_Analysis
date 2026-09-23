import sys
from PyQt5.QtWidgets import QApplication,QMainWindow, QLabel

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transmission Analyzer")
        self.setGeometry(300, 300, 300, 300)
        self.setCentralWidget(QLabel("Shit!"))

app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())
