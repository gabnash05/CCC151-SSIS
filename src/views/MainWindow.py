from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QSizePolicy, QStatusBar
from PyQt6.QtGui import QIcon

from controllers.studentControllers import searchStudentsByField
from views.StudentTable import StudentTable
from views.AddStudentDialogue import AddStudentDialog
from views.UpdateStudentDialogue import UpdateStudentDialog

class MainWindow(QMainWindow):
  searchByFields = ["ID Number", "First Name", "Last Name", "Program Code", "College Code"]

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
    self.searchButton.clicked.connect(self.searchStudents)

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
  
  # Changes the students list in StudentTable
  def searchStudents(self):
    searchValue = self.searchBarLineEdit.text()
    searchField = self.searchByComboBox.currentText()

    if searchValue == "":
      self.studentTable.initialStudentsToDisplay()
      return
    
    if searchField == "":
      searchField = self.searchByFields[0]

    students = searchStudentsByField(searchField, searchValue)

    self.studentTable.setStudents(students)