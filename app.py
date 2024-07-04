import sys
from utilities import verify_user
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QDesktopWidget, QPushButton, QLineEdit, QDialog
from PyQt5.QtCore import QSize

widgets = dict()


class AccountItem(QWidget):
    def __init__(self, parent: QWidget, id: int, account: str, username: str, password: str):
        super(QWidget, self).__init__(self, parent)
        
        self.id = id
        
        """TODO: Make item for password list"""


class Home(QWidget):
    def __init__(self, parent: QWidget):
        super(QWidget, self).__init__(parent)
        layout = QGridLayout(self)
        self.setLayout(layout)

        label = QLabel("Home", self)
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
        layout.addWidget(self.username)
        
        self.password = QLineEdit(self)
        layout.addWidget(self.password)

        button = QPushButton("Log In")
        button.clicked.connect(self.login)
        layout.addWidget(button)


    def login(self):
        if verify_user(self.username.text(), self.password.text()):
            home = Home(self.parent())
            self.parent().setCentralWidget(home)
        else:
            dialog = QDialog(self)


class MainWindow(QMainWindow):
    def __init__(self):
        # Initialize the Main Window
        QMainWindow.__init__(self)

        # Set the size for the window
        self.setMinimumSize(QSize(800, 600))
        self.setWindowTitle("PassKeeper")

        # Create the widgets
        widgets["Login"] = Login(self)
        widgets["Home"] = Home(self)

        # Set the login widget
        self.setCentralWidget(widgets["Login"])

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