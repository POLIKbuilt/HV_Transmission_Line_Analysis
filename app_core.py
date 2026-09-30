import sys
import logging
import traceback
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFormLayout, QLineEdit, QSpinBox, QComboBox, QDateEdit, \
    QCheckBox, QPushButton, QMessageBox, QWidget, QVBoxLayout
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

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        outer_layout = QVBoxLayout(central_widget)
        form_layout = QFormLayout()

        # Cable data input
        self.cable_type = QComboBox()
        self.cable_type.addItems(["LTV", "MTV", "Steel", "Aluminium"])

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.age_input = QSpinBox()
        self.age_input.setRange(0,120)

        self.role_input = QComboBox()
        self.role_input.addItems(["IT", "HR", "FM"])

        self.birthday_input = QDateEdit()
        self.birthday_input.setDate(QDate(2000, 1 ,1))
        self.birthday_input.setCalendarPopup(True)

        self.subscribe_checkbox = QCheckBox("Subscribe")

        # Rows
        form_layout.addRow("Cable Type", self.cable_type)
        form_layout.addRow("Name", self.name_input)
        form_layout.addRow("Email", self.email_input)
        form_layout.addRow("Age", self.age_input)
        form_layout.addRow("Role", self.role_input)
        form_layout.addRow("Birthday", self.birthday_input)
        form_layout.addRow("Subscribe", self.subscribe_checkbox)

        # Submit
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.handle_submit)

        outer_layout.addLayout(form_layout)
        outer_layout.addWidget(self.submit_button)

    def handle_submit(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()

        if not name:
            QMessageBox.information(self, "Error", "Name is required")
            return

        if "@" not in email:
            QMessageBox.information(self, "Error", "Email is not valid")
            return

        contact = {
            "name": name,
            "email": email,
            "age": self.age_input.value(),
            "role": self.role_input.currentText(),
            "birthday": self.birthday_input.date().toString("yyyy-MM-dd"),
            "subscribe": self.subscribe_checkbox.isChecked()
        }

        print("Contact saved: ", contact)
        QMessageBox.information(self, "Success", f"Contact {name} saved to database")
        self.clear_form()

    def clear_form(self):
        self.cable_type.clear()
        self.name_input.clear()
        self.email_input.clear()
        self.age_input.setValue(0)
        self.role_input.setCurrentIndex(0)
        self.subscribe_checkbox.setChecked(False)

    def closeEvent(self, event):
        self.settings["window_width"] = self.width()
        self.settings["window_height"] = self.height()
        save_settings(self.settings)
        event.accept()

app = QApplication(sys.argv)
app.setApplicationName("Transmission Analyzer")
app.setOrganizationName("polikstarik dev.")
app.setApplicationVersion("1.0.1")
window = App()
window.show()
sys.excepthook = excepthook
sys.exit(app.exec_())
