from PyQt6 import QtWidgets, QtCore, QtGui

from controllers.programControllers import searchProgramsByField
from controllers.collegeControllers import getAllColleges
from controllers.studentControllers import updateStudent

class UpdateStudentDialog(QtWidgets.QDialog):
  studentUpdatedTableSignal = QtCore.pyqtSignal(list)
  statusMessageSignal = QtCore.pyqtSignal(str, int) 

  def __init__(self, parent=None, studentData=None):
    super().__init__(parent)
    self.setWindowTitle("Update Student")
    self.setModal(True)
    
    # Store the student ID for reference
    self.originalStudentID = studentData[0]

    self.setupUI(studentData)

  def setupUI(self, studentData):
    # Set Window Size
    self.setMinimumSize(QtCore.QSize(400, 500))
    self.setMaximumSize(QtCore.QSize(500, 500))

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

                       QComboBox QAbstractItemView {
                          background-color: black;  /* Dropdown options have a black background */
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
    
    # Form Fields
    self.firstNameInput = QtWidgets.QLineEdit(self)
    self.firstNameInput.setText(studentData[1])

    self.lastNameInput = QtWidgets.QLineEdit(self)
    self.lastNameInput.setText(studentData[2])

    self.yearLevelInput = QtWidgets.QComboBox(self)
    self.yearLevelInput.addItems(["1", "2", "3", "4", "5"])
    self.yearLevelInput.setCurrentText(studentData[3])

    self.genderInput = QtWidgets.QComboBox(self)
    self.genderInput.addItems(["Male", "Female", "Others"])
    self.genderInput.setCurrentText(studentData[4])

    self.idInput = QtWidgets.QLineEdit(self)
    self.idInput.setText(studentData[0])
    # Prevent editing of student ID
    #self.idInput.setReadOnly(True)  

    self.programCodeInput = QtWidgets.QComboBox(self)
    self.collegeCodeInput = QtWidgets.QComboBox(self)

    colleges = getAllColleges()
    collegeCodeList = [college["College Code"] for college in colleges]
    self.collegeCodeInput.addItems(collegeCodeList)
    
    if studentData[6] != "N/A":
      collegeIndex = collegeCodeList.index(studentData[6])
      self.collegeCodeInput.setCurrentIndex(collegeIndex)

      programCodeList = self.updateProgramOptions(collegeIndex)
      if studentData[5] != "N/A":
        programIndex = programCodeList.index(studentData[5])
        self.programCodeInput.setCurrentIndex(programIndex)

    # Section Headers
    self.titleLabel = QtWidgets.QLabel("Update Student")
    self.titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
    self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    self.personalInfoLabel = QtWidgets.QLabel("Personal Information")
    self.personalInfoLabel.setStyleSheet("font-size: 19px; font-weight: bold;")

    self.studentInfoLabel = QtWidgets.QLabel("Student Information")
    self.studentInfoLabel.setStyleSheet("font-size: 19px; font-weight: bold;")

    # Update Button
    self.updateButton = QtWidgets.QPushButton("Update Student")
    self.updateButton.setMinimumSize(QtCore.QSize(120, 40))
    self.updateButton.setMaximumSize(QtCore.QSize(140, 40))
    self.updateButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    self.updateButton.clicked.connect(self.updateStudent)

    # Connect College ComboBox to Update Function
    self.collegeCodeInput.currentIndexChanged.connect(self.updateProgramOptions)

    # Layout
    formLayout = QtWidgets.QFormLayout()
    formLayout.addRow(self.titleLabel)
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

    # Spacer before button
    verticalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
    formLayout.addItem(verticalSpacer)

    # Center the button
    buttonLayout = QtWidgets.QHBoxLayout()
    buttonLayout.addStretch()
    buttonLayout.addWidget(self.updateButton)
    buttonLayout.addStretch()

    # Status Bar
    self.statusBar = QtWidgets.QLabel("")
    self.statusBar.setStyleSheet("background-color: none; color: red; border-top: 1px solid #666666; padding: 4px; text-align: center")
    self.statusBar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    # Main Layout
    mainLayout = QtWidgets.QVBoxLayout()
    mainLayout.addLayout(formLayout)
    mainLayout.addLayout(buttonLayout)
    mainLayout.addWidget(self.statusBar)

    mainLayout.setContentsMargins(15, 15, 15, 15)
    self.setLayout(mainLayout)
  
  def updateProgramOptions(self, index):
    if index < 0:
      return
    
    # Get selected college
    selectedCollege = self.collegeCodeInput.currentText()

    # Clear previous program options
    self.programCodeInput.clear()

    # Add new program options
    programs = searchProgramsByField(selectedCollege, "College Code")
    programCodeList = [program["Program Code"] for program in programs]
    self.programCodeInput.addItems(programCodeList)

    return programCodeList
  
  def updateStudent(self):
    idNumber = self.idInput.text().strip() or None
    firstName = self.firstNameInput.text().strip() or None
    lastName = self.lastNameInput.text().strip() or None
    yearLevel = self.yearLevelInput.currentText().strip() or None
    gender = self.genderInput.currentText() or None
    programCode = self.programCodeInput.currentText() or None
    collegeCode = self.collegeCodeInput.currentText() or None

    result = updateStudent(self.originalStudentID, idNumber, firstName, lastName, yearLevel, gender, programCode, collegeCode)

    if result == "Student updated successfully.":
      self.showStatusMessage(result)
      
      

      # Send signal to MainWindow to call addStudent in StudentTable
      self.studentUpdatedTableSignal.emit([[self.originalStudentID, idNumber, firstName, lastName, gender, yearLevel, programCode, collegeCode]])
      self.statusMessageSignal.emit("Updating Student", 1000)

      # Closes the QDialog
      self.accept()
    else:
      self.showStatusMessage(result)
      return

    # Emit signal
    self.statusMessageSignal.emit("Student Updated", 3000)

    # Close dialog
    self.accept()

  def showStatusMessage(self, message):
    self.statusBar.setText(message)

