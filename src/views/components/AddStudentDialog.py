from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import pyqtSignal

from controllers.programControllers import searchProgramsByField
from controllers.collegeControllers import getAllColleges
from controllers.studentControllers import addStudent

class AddStudentDialog(QtWidgets.QDialog):
  studentAddedTableSignal = pyqtSignal(list)
  studentAddedWindowSignal = pyqtSignal(str, int)

  def __init__(self, parent=None):
    super().__init__(parent)
    self.setWindowTitle("Add Student")
    self.setModal(True)

    self.setupUI()
    
  def setupUI(self):
    # Window Init
    self.setMinimumSize(QtCore.QSize(400, 475))
    self.setMaximumSize(QtCore.QSize(500, 475))

    # Set stylesheet
    self.setStyleSheet("""
                       QDialog { 
                          background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(37, 37, 37, 255), stop:1 rgba(52, 57, 57, 255)); 
                       }

                       QLineEdit:focus { 
                          border:  1px solid rgb(63, 150, 160); border-radius: 4px; 
                       }

                       QComboBox { 
                          background-color: rgba(0, 0, 0, 0); 
                       }  
                       
                       QComboBox::drop-down { 
                          subcontrol-origin: padding; subcontrol-position: top right; width: 15px; 
                       } 
                       
                       QComboBox QAbstractItemView::item::hover { 
                          background-color: rgb(25, 25, 25); 
                       } 
                       
                       QComboBox::hover { 
                          background-color: rgb(35, 35, 35); 
                       }""")

    # Create form fields
    self.firstNameInput = QtWidgets.QLineEdit(self)
    self.lastNameInput = QtWidgets.QLineEdit(self)
    self.genderInput = QtWidgets.QComboBox(self)
    self.genderInput.addItems(["Male", "Female", "Others"])
    self.idInput = QtWidgets.QLineEdit(self)
    self.yearLevelInput = QtWidgets.QLineEdit(self)
    self.programCodeInput = QtWidgets.QComboBox(self)
    self.collegeCodeInput = QtWidgets.QComboBox(self)

    self.programCodeInput.addItems(["Select Program"])
    self.programCodeInput.model().item(0).setEnabled(False)

    # Getting all college codes
    self.collegeCodeInput.addItems(["Select College"])
    colleges = getAllColleges()
    collegeCodeList = [college["College Code"] for college in colleges]

    self.collegeCodeInput.addItems(collegeCodeList)
    self.collegeCodeInput.model().item(0).setEnabled(False)

    # Section headers
    self.titleLabel = QtWidgets.QLabel("Add Student")
    self.titleLabel.setFont(QtGui.QFont("Inter", 18, QtGui.QFont.Weight.Bold))
    self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    self.titleLayout = QtWidgets.QHBoxLayout()
    self.titleLayout.addStretch()
    self.titleLayout.addWidget(self.titleLabel)
    self.titleLayout.addStretch()

    self.personalInfoLabel = QtWidgets.QLabel("Personal Information")
    self.personalInfoLabel.setFont(QtGui.QFont("Inter", 14, QtGui.QFont.Weight.Bold))

    self.studentInfoLabel = QtWidgets.QLabel("Student Information")
    self.studentInfoLabel.setFont(QtGui.QFont("Inter", 14, QtGui.QFont.Weight.Bold))

    # Button to add student
    self.addButton = QtWidgets.QPushButton("Add Student")
    self.addButton.setMinimumSize(QtCore.QSize(120, 40))
    self.addButton.setMaximumSize(QtCore.QSize(140, 40))
    self.addButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

    # Connect Button
    self.addButton.clicked.connect(self.addStudent)

    # Connect College ComboBox to Update Function
    self.collegeCodeInput.currentIndexChanged.connect(self.updateProgramOptions)

    # Layout
    formLayout = QtWidgets.QFormLayout()
    formLayout.addRow(self.titleLayout)
    formLayout.addRow(QtWidgets.QLabel(""))  # Spacer under title

    formLayout.addRow(self.personalInfoLabel)
    formLayout.addRow("First Name:", self.firstNameInput)
    formLayout.addRow("Last Name:", self.lastNameInput)
    formLayout.addRow("Gender:", self.genderInput)
    formLayout.addRow(QtWidgets.QLabel(""))  # Spacer under personal info

    formLayout.addRow(self.studentInfoLabel)
    formLayout.addRow("ID Number:", self.idInput)
    formLayout.addRow("Year Level:", self.yearLevelInput)
    formLayout.addRow("College Code:", self.collegeCodeInput)
    formLayout.addRow("Program Code:", self.programCodeInput)

    # Add vertical spacer to create a gap before the button
    verticalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
    formLayout.addItem(verticalSpacer)

    # Center the button using a horizontal layout
    buttonLayout = QtWidgets.QHBoxLayout()
    buttonLayout.addStretch()
    buttonLayout.addWidget(self.addButton)
    buttonLayout.addStretch()

    # Create a status bar (QLabel at the bottom)
    self.statusBar = QtWidgets.QLabel("")
    self.statusBar.setStyleSheet("background-color: none; color: red; border-top: 1px solid #666666; padding: 4px; text-align: center")
    self.statusBar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    # Main layout
    mainLayout = QtWidgets.QVBoxLayout()
    mainLayout.addLayout(formLayout)
    mainLayout.addLayout(buttonLayout)
    mainLayout.addWidget(self.statusBar)

    mainLayout.setContentsMargins(15, 15, 15, 15)
    self.setLayout(mainLayout)

  #----------------------------------------------------------

  # Adds a student to the csv file and to StudentTable
  def addStudent(self):
    idNumber = self.idInput.text().strip() or None
    firstName = self.firstNameInput.text().strip() or None
    lastName = self.lastNameInput.text().strip() or None
    yearLevel = self.yearLevelInput.text().strip() or None
    gender = self.genderInput.currentText() or None
    programCode = self.programCodeInput.currentText() or None
    collegeCode = self.collegeCodeInput.currentText() or None

    result = addStudent(idNumber, firstName, lastName, yearLevel, gender, programCode, collegeCode)

    if result == "Student added successfully.":
      self.showStatusMessage(result)
      self.statusBar.setStyleSheet("background-color: none; color: green; border-top: 1px solid #666666; padding: 4px; text-align: center")

      # Send signal to MainWindow to call addStudent in StudentTable
      self.studentAddedTableSignal.emit([idNumber, firstName, lastName, gender, yearLevel, programCode, collegeCode])
      self.studentAddedWindowSignal.emit("Student Added", 1000)

      # Closes the QDialog
      self.accept()
    else:
      self.showStatusMessage(result)
      return

  def updateProgramOptions(self, index):
    if index <= 0:
      return  # Ignore the placeholder selection
    
    # Get selected college
    selectedCollege = self.collegeCodeInput.currentText()

    # Clear previous program options
    self.programCodeInput.clear()
    self.programCodeInput.addItem("Select Program")  # Placeholder
    self.programCodeInput.model().item(0).setEnabled(False)

    # Add new program options
    programs = searchProgramsByField(selectedCollege, "College Code")
    programCodeList = [program["Program Code"] for program in programs]
    self.programCodeInput.addItems(programCodeList)

  def showStatusMessage(self, message):
    self.statusBar.setText(message)

