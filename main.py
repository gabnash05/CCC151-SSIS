import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

class MyApp(QMainWindow):
  def __init__(self):
    super().__init__()
    uic.loadUi("gui/mainwindow.ui", self)

    self.apply_stylesheet()
  
  def apply_stylesheet(self):
    with open("gui/styles.qss", "r") as file:
      stylesheet = file.read()
      self.setStyleSheet(stylesheet)

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MyApp()
  window.show()
  sys.exit(app.exec())