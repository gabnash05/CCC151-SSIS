from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QSizePolicy, QStatusBar
from PyQt6.QtGui import QIcon

from views.StudentTable import StudentTable
from views.AddStudentDialogue import AddStudentDialog

class MainWindow(QMainWindow):
  def __init__(self):

    # WINDOW INITIALIZATION
    super().__init__()
    uic.loadUi("src/gui/ui/studentMainWindow.ui", self)

    #self.applyStylesheet()
    self.setWindowIcon(QIcon("assets/LogoIcon.png"))
    self.setWindowTitle("Lexis")

    # STATUS BAR
    self.status_bar = QStatusBar()
    self.setStatusBar(self.status_bar)  

    # UI COMPONENTS
    self.studentTable = StudentTable(self)
    self.dataFrame.layout().addWidget(self.studentTable)

    # CONNECT SIGNALS
    self.studentTable.statusMessageSignal.connect(self.displayMessageToStatusBar)
    self.addStudentButton.clicked.connect(self.openAddStudentDialog)

    # FINISHED INITIALIZATION
    self.displayMessageToStatusBar("Main Window Loaded", 3000)

  # ---------------------------------------------------------
  
  # INIT FUNCTIONS
  def displayMessageToStatusBar(self, message, duration):
    self.status_bar.showMessage(message, duration)

  def applyStylesheet(self):
    with open("../gui/styles/styles.qss", "r") as file:
      stylesheet = file.read()
      self.setStyleSheet(stylesheet)
  
  # UI FUNCTIONS
  def openAddStudentDialog(self):
    self.dialog = AddStudentDialog(self)

    # Connect signal from AddStudentDialog to StudentTable
    self.dialog.studentAddedTableSignal.connect(self.studentTable.addStudentToTable)

    # Connect signal from AddStudentDialog to StudentTable
    self.dialog.studentAddedWindowSignal.connect(self.displayMessageToStatusBar)

    self.dialog.exec()