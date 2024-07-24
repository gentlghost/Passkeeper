from math import floor
import sys
from utilities import (
    create_user, verify_user, get_user_id, get_name, create_account, get_accounts,
    delete_account, decrypt_password
)
from pages.account import AccountUi
from pages.add_account import AddAccountUi
from pages.create_user import CreateUserUi
from pages.home import HomeUi
from pages.login import LoginUi

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QDesktopWidget, QMessageBox, QLineEdit
)
from PyQt5.QtCore import Qt, QSize


class Account(QWidget):
    def __init__(self, parent: QWidget, user_id: int, account_id: int, service: str, username: str, password: str):
        super(QWidget, self).__init__(parent)
        
        self.user_id = user_id
        self.account_id = account_id
        
        self.ui = AccountUi()
        self.ui.setupUi(self)
        self.ui.service.setText(service)
        self.ui.username.setText(username)
        self.ui.password.setText(decrypt_password(self.user_id, password.encode()))

        self.ui.password.setEchoMode(QLineEdit.Password)

        self.ui.viewButton.clicked.connect(self.on_view)
        self.ui.deleteButton.clicked.connect(self.on_delete)


    def on_view(self):
        if self.ui.password.echoMode() == QLineEdit.Password:
            self.ui.password.setEchoMode(QLineEdit.Normal)
            self.ui.viewButton.setText("Hide")
        else:
            self.ui.password.setEchoMode(QLineEdit.Password)
            self.ui.viewButton.setText("View")


    def on_delete(self, s):
        confirm = QMessageBox(self)
        confirm.setText("Are you sure you want to delete the account?")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setIcon(QMessageBox.Question)
        result = confirm.exec()

        if result == QMessageBox.No:
            return
        
        if result == QMessageBox.Yes:
            delete_account(self.account_id)
            self.parentWidget().layout().removeWidget(self)


class AddAccount(QWidget):
    def __init__(self, parent: QWidget):
        super(QWidget, self).__init__(parent)

        self.ui = AddAccountUi()
        self.ui.setupUi(self)

        self.ui.addButton.clicked.connect(self.on_add_account)
        self.ui.backButton.clicked.connect(self.on_back)
        self.ui.viewButton.clicked.connect(self.on_view)

    def on_add_account(self):
        result = create_account(
            self.parent().user_id, self.ui.service.text(), 
            self.ui.username.text(), self.ui.password.text()
            )
        if result == 1:
            error = Error(self, "Service cannot be empty.")
            error.exec()
        elif result == 2:
            error = Error(self, "User name cannot be empty.")
            error.exec()
        elif result == 3:
            error = Error(self, "Password cannot be empty.")
            error.exec()
        elif result == 4:
            error = Error(self, "User on service already exists.")
            error.exec()
        else:
            self.parent().setCentralWidget(Home(self.parent()))


    def on_back(self):
        self.parent().setCentralWidget(Home(self.parent()))


    def on_view(self):
        if self.ui.password.echoMode() == QLineEdit.Password:
            self.ui.password.setEchoMode(QLineEdit.Normal)
            self.ui.viewButton.setText("Hide")
        else:
            self.ui.password.setEchoMode(QLineEdit.Password)
            self.ui.viewButton.setText("View")


class CreateUser(QWidget):
    def __init__(self, parent: QWidget):
        super(QWidget, self).__init__(parent)
        
        self.ui = CreateUserUi()
        self.ui.setupUi(self)

        self.ui.createUser.clicked.connect(self.on_add_user)
        self.ui.backButton.clicked.connect(self.on_back)
        self.ui.viewButton.clicked.connect(self.on_view)


    def on_add_user(self):
        status = create_user(self.ui.name.text(), self.ui.username.text(), self.ui.password.text())
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


    def on_back(self):
        self.parent().setCentralWidget(Login(self.parent()))


    def on_view(self):
        if self.ui.password.echoMode() == QLineEdit.Password:
            self.ui.password.setEchoMode(QLineEdit.Normal)
            self.ui.viewButton.setText("Hide")
        else:
            self.ui.password.setEchoMode(QLineEdit.Password)
            self.ui.viewButton.setText("View")


class Error(QMessageBox):
    def __init__(self, parent: QWidget, error: str):
        super(QMessageBox, self).__init__(parent)

        self.setWindowTitle("Error")
        self.setText(error)


class Home(QWidget):
    def __init__(self, parent: QWidget):
        super(QWidget, self).__init__(parent)
        self.ui = HomeUi()
        self.ui.setupUi(self)

        if self.parent().user_id == -1:
            self.ui.welcome.setText("Hello")
        else:
            self.ui.welcome.setText(f"Hello, {get_name(self.parent().user_id)}")

        # This doesn't work, and I have no idea why!
        self.container = QWidget()
        self.grid = QtWidgets.QGridLayout(self.container)

        for account in get_accounts(self.parent().user_id).fetchall():
            acc_widget = Account(self.container, account[1], account[0], account[2], account[3], account[4])
            self.grid.addWidget(acc_widget)

        self.password_holder = QtWidgets.QScrollArea(self)
        self.password_holder.setGeometry(25, 150, 750, 400)
        self.password_holder.setWidget(self.container)
        self.password_holder.setWidgetResizable(True)

        self.password_holder.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui.addButton.clicked.connect(self.on_add_account)
        

    def on_add_account(self):
        self.parent().setCentralWidget(AddAccount(self.parent()))


class Login(QWidget):
    def __init__(self, parent: QWidget):
        super(QWidget, self).__init__(parent)
        
        self.ui = LoginUi()
        self.ui.setupUi(self)

        self.ui.login.clicked.connect(self.on_login)
        self.ui.createUser.clicked.connect(self.on_create_user)


    def on_login(self):
        if verify_user(self.ui.username.text(), self.ui.password.text()):
            self.parent().user_id = get_user_id(self.ui.username.text())
            self.parent().setCentralWidget(Home(self.parent()))
        else:
            error = Error(self, "User name or password is invalid.")
            error.exec()


    def on_create_user(self):
        self.parent().setCentralWidget(CreateUser(self.parent()))


class MainWindow(QMainWindow):
    def __init__(self):
        # Initialize the Main Window
        super(QMainWindow, self).__init__()

        self.user_id = -1

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
    sys.exit(app.exec())