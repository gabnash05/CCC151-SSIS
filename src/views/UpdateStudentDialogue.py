from PyQt6 import QtWidgets, QtCore, QtGui

from controllers.programControllers import searchProgramsByField
from controllers.collegeControllers import getAllColleges
from controllers.studentControllers import updateStudent

class UpdateStudentDialog(QtWidgets.QDialog):
  statusMessageSignal = QtCore.pyqtSignal(str, int)  # Emits (studentID, updatedData)

  def __init__(self, studentData, parent=None):
    super().__init__(parent)
    self.setWindowTitle("Update Student")
    self.setModal(True)
    
    # Store the student ID for reference
    self.studentID = studentData[0]  # Assuming first item is Student ID

    # Set Window Size
    self.setMinimumSize(QtCore.QSize(400, 475))
    self.setMaximumSize(QtCore.QSize(500, 475))

    # Stylesheet
    self.setStyleSheet("QDialog { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(37, 37, 37, 255), stop:1 rgba(52, 57, 57, 255)); }")

    # Form Fields
    self.idInput = QtWidgets.QLineEdit(self)
    self.idInput.setText(studentData[0])
    self.idInput.setReadOnly(True)  # Prevent editing of student ID

    self.firstNameInput = QtWidgets.QLineEdit(self)
    self.firstNameInput.setText(studentData[1])

    self.lastNameInput = QtWidgets.QLineEdit(self)
    self.lastNameInput.setText(studentData[2])

    self.yearLevelInput = QtWidgets.QLineEdit(self)
    self.yearLevelInput.setText(studentData[3])

    self.genderInput = QtWidgets.QComboBox(self)
    self.genderInput.addItems(["Male", "Female", "Others"])
    self.genderInput.setCurrentText(studentData[4])

    self.programCodeInput = QtWidgets.QComboBox(self)
    self.collegeCodeInput = QtWidgets.QComboBox(self)

    self.programCodeInput.addItems(["Select Program"])
    self.programCodeInput.model().item(0).setEnabled(False)

    self.collegeCodeInput.addItems(["Select College"])
    colleges = getAllColleges()
    collegeCodeList = [college["College Code"] for college in colleges]
    self.collegeCodeInput.addItems(collegeCodeList)
    self.collegeCodeInput.setCurrentText(studentData[5])  # Set current college
    self.collegeCodeInput.model().item(0).setEnabled(False)

    # Section Headers
    self.titleLabel = QtWidgets.QLabel("Update Student")
    self.titleLabel.setFont(QtGui.QFont("Inter", 18, QtGui.QFont.Weight.Bold))
    self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    self.personalInfoLabel = QtWidgets.QLabel("Personal Information")
    self.personalInfoLabel.setFont(QtGui.QFont("Inter", 14, QtGui.QFont.Weight.Bold))

    self.studentInfoLabel = QtWidgets.QLabel("Student Information")
    self.studentInfoLabel.setFont(QtGui.QFont("Inter", 14, QtGui.QFont.Weight.Bold))

    # Update Button
    self.updateButton = QtWidgets.QPushButton("Update Student")
    self.updateButton.setMinimumSize(QtCore.QSize(100, 40))
    self.updateButton.setMaximumSize(QtCore.QSize(100, 40))
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
    if index <= 0:
      return  # Ignore the placeholder selection
    
    # Get selected college
    selectedCollege = self.collegeCodeInput.currentText()

    # Clear previous program options
    self.programCodeInput.clear()
    self.programCodeInput.addItem("Select Program")  # Placeholder
    self.programCodeInput.model().item(0).setEnabled(False)

    # Add new program options
    programs = searchProgramsByField("College Code", selectedCollege)
    programCodeList = [program["Program Code"] for program in programs]
    self.programCodeInput.addItems(programCodeList)
  
  def updateStudent(self):
    updatedData = [
      self.idInput.text(),
      self.firstNameInput.text(),
      self.lastNameInput.text(),
      self.yearLevelInput.text(),
      self.genderInput.currentText(),
      self.collegeCodeInput.currentText(),
      self.programCodeInput.currentText(),
    ]

    # Emit signal
    self.statusMessageSignal.emit("Student Updated", 3000)

    # Close dialog
    self.accept()