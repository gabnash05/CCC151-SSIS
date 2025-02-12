from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QSizePolicy
from PyQt6.QtGui import QIcon

from views.StudentTable import StudentTable

class MainWindow(QMainWindow):
  def __init__(self):

    # WINDOW INITIALIZATION
    super().__init__()
    uic.loadUi("src/gui/ui/studentMainWindow.ui", self)

    #self.apply_stylesheet()
    self.setWindowIcon(QIcon("assets/LogoIcon.png"))
    self.setWindowTitle("Lexis")

    # UI COMPONENTS
    self.studentTable = StudentTable(self)
    self.dataFrame.layout().addWidget(self.studentTable)

    # Ensure StudentTable expands freely inside scroll area
    self.studentTable.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

  # ---------------------------------------------------------
  
  # INIT FUNCTIONS
  def apply_stylesheet(self):
    with open("../gui/styles/styles.qss", "r") as file:
      stylesheet = file.read()
      self.setStyleSheet(stylesheet)