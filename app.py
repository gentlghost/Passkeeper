import sys
from utilities import create_user, verify_user, get_user_id, get_name
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QGridLayout, QWidget, QDesktopWidget, 
    QPushButton, QLineEdit, QMessageBox, QListWidget, QListWidgetItem
) 
from PyQt5.QtCore import QSize


class AccountItem(QListWidgetItem):
    def __init__(self, parent: QWidget, id: int, account: str, username: str, password: str):
        super(QWidget, self).__init__(parent)
        
        self.id = id
        
        """TODO: Make item for password list"""


class CreateUser(QWidget):
    def __init__(self, parent: QWidget):
        super(QWidget, self).__init__(parent)
        
        layout = QGridLayout(self)
        self.setLayout(layout)

        label = QLabel("Create User", self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        self.name = QLineEdit(self)
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        self.username = QLineEdit(self)
        self.username.setPlaceholderText("User name");
        layout.addWidget(self.username)
        
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Password")
        layout.addWidget(self.password)

        button = QPushButton("Create User")
        button.clicked.connect(self.add_user)
        layout.addWidget(button)


    def add_user(self):
        status = create_user(self.name.text(), self.username.text(), self.password.text())
        if status == 1:
            error = Error(self, "Name cannot be empty.")
            error.exec()
        elif status == 2:
            error = Error(self, "User name cannot be empty.")
            error.exec()
        elif status == 3:
            error = Error(self, "Password cannot be empty.")
            error.exec()
        elif status == 4:
            error = Error(self, "User already exists.")
            error.exec()
        else:
            self.parent().setCentralWidget(Login(self.parent()))


class Error(QMessageBox):
    def __init__(self, parent: QWidget, error: str):
        super(QMessageBox, self).__init__(parent)

        self.setWindowTitle("Error")
        self.setText(error)


class Home(QWidget):
    def __init__(self, parent: QWidget):
        super(QWidget, self).__init__(parent)
        layout = QGridLayout(self)
        self.setLayout(layout)

        if self.parent().user_id == -1:
            text = "Hello"
        else:
            text = f"Hello, {get_name(self.parent().user_id)}"

        label = QLabel(text, self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)


class Login(QWidget):
    def __init__(self, parent: QWidget):
        super(QWidget, self).__init__(parent)
        
        layout = QGridLayout(self)
        self.setLayout(layout)

        label = QLabel("PassKeeper", self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        self.username = QLineEdit(self)
        self.username.setPlaceholderText("User name")
        layout.addWidget(self.username)
        
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Password")
        layout.addWidget(self.password)

        login_btn = QPushButton("Log In")
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)
        
        create_user_btn = QPushButton("Create New User")
        create_user_btn.clicked.connect(self.create_user)
        layout.addWidget(create_user_btn)


    def login(self):
        if verify_user(self.username.text(), self.password.text()):
            self.parent().user_id = get_user_id(self.username.text())
            self.parent().setCentralWidget(Home(self.parent()))
        else:
            error = Error(self, "User name or password is invalid.")
            error.exec()


    def create_user(self):
        self.parent().setCentralWidget(CreateUser(self.parent()))


class MainWindow(QMainWindow):
    user_id = -1


    def __init__(self):
        # Initialize the Main Window
        super(QMainWindow, self).__init__()

        # Set the size for the window
        self.setMinimumSize(QSize(800, 600))
        self.setWindowTitle("PassKeeper")

        # Set the login widget
        self.setCentralWidget(Login(self.parent()))

        # Move to center
        qt_rect = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        qt_rect.moveCenter(center)
        self.move(qt_rect.topLeft())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())