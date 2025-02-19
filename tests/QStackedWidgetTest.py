from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QPushButton, QVBoxLayout
import sys

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    # Create QStackedWidget
    self.stackedWidget = QStackedWidget(self)
    self.setCentralWidget(self.stackedWidget)

    # Create pages
    self.page1 = QWidget()
    self.page2 = QWidget()

    # Add pages to stackedWidget
    self.stackedWidget.addWidget(self.page1)
    self.stackedWidget.addWidget(self.page2)

    # Layout for Page 1
    layout1 = QVBoxLayout()
    button1 = QPushButton("Go to Page 2")
    button1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
    layout1.addWidget(button1)
    self.page1.setLayout(layout1)

    # Layout for Page 2
    layout2 = QVBoxLayout()
    button2 = QPushButton("Go to Page 1")
    button2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
    layout2.addWidget(button2)
    self.page2.setLayout(layout2)

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
