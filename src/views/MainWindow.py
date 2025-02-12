from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QSizePolicy, QStatusBar
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

    # STATUS BAR
    self.status_bar = QStatusBar()
    self.setStatusBar(self.status_bar)  

    # UI COMPONENTS
    self.studentTable = StudentTable(self)
    self.dataFrame.layout().addWidget(self.studentTable)

    # CONNECT SIGNALS
    # self.studentTable.statusMessage.connect(self.status_bar.showMessage)

    # FINISHED INITIALIZATION
    self.status_bar.showMessage("Main Window Loaded", 3000)

  # ---------------------------------------------------------
  
  # INIT FUNCTIONS
  def apply_stylesheet(self):
    with open("../gui/styles/styles.qss", "r") as file:
      stylesheet = file.read()
      self.setStyleSheet(stylesheet)