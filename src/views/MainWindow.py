from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QSizePolicy, QStatusBar
from PyQt6.QtGui import QIcon

from views.StudentTable import StudentTable
from views.AddStudentDialogue import AddStudentDialog
from views.UpdateStudentDialogue import UpdateStudentDialog

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
    self.studentTable.editStudentSignal.connect(self.openUpdateStudentDialog)
    self.sortByComboBox.currentIndexChanged.connect(self.studentTable.refreshDisplayStudents)
    self.sortingOrderComboBox.currentIndexChanged.connect(self.studentTable.refreshDisplayStudents)

    # FINISHED INITIALIZATION
    self.displayMessageToStatusBar("Main Window Loaded", 3000)

  # ---------------------------------------------------------
  
  # INIT FUNCTIONS
  # Display messages to QStatusBar
  def displayMessageToStatusBar(self, message, duration):
    self.status_bar.showMessage(message, duration)

  # Apply stylesheet to MainWindow
  def applyStylesheet(self):
    with open("../gui/styles/styles.qss", "r") as file:
      stylesheet = file.read()
      self.setStyleSheet(stylesheet)
  
  # UI FUNCTIONS
  def openAddStudentDialog(self):
    self.addDialog = AddStudentDialog(self)

    # Connect signal from AddStudentDialog to StudentTable
    self.addDialog.studentAddedTableSignal.connect(self.studentTable.addNewStudentToTable)
    
    # Connect signal from AddStudentDialog to MainWindow
    self.addDialog.studentAddedWindowSignal.connect(self.displayMessageToStatusBar)

    self.addDialog.exec()
  
  # Updates a student in the GUI and CSV
  def openUpdateStudentDialog(self, studentData):
    self.updateDialog = UpdateStudentDialog(self, studentData)

    # Connect signal from UpdateStudentDialog to StudentTable
    self.updateDialog.studentUpdatedTableSignal.connect(self.studentTable.editStudentInTable)
    
    # Connect signal from UpdateStudentDialog to MainWindow
    self.updateDialog.statusMessageSignal.connect(self.displayMessageToStatusBar)

    self.updateDialog.exec()