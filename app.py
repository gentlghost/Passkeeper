import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QDesktopWidget
from PyQt5.QtCore import QSize


class Login(QWidget):
    def __init__(self, parent: QWidget):
        QWidget.__init__(self, parent=parent)
        layout = QGridLayout(self)
        parent.setLayout(layout)

        label = QLabel("PassKeeper", self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)


class MainWindow(QMainWindow):
    def __init__(self):
        # Initialize the Main Window
        QMainWindow.__init__(self)

        # Set the size for the window
        self.setMinimumSize(QSize(800, 600))
        self.setWindowTitle("PassKeeper")

        # Set the login widget
        login = Login(self)
        self.setCentralWidget(login)

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