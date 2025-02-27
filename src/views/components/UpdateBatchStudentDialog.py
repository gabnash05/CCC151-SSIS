from PyQt6 import QtWidgets, QtCore, QtGui
from controllers.programControllers import searchProgramsByField
from controllers.collegeControllers import getAllColleges
from controllers.studentControllers import updateStudent

class UpdateBatchStudentDialog(QtWidgets.QDialog):
  studentUpdatedTableSignal = QtCore.pyqtSignal(list)
  statusMessageSignal = QtCore.pyqtSignal(str, int)

  def __init__(self, parent=None, studentsData=None):
    super().__init__(parent)
    self.setWindowTitle("Update Multiple Students")
    self.setModal(True)

    # Store only student IDs
    self.studentsData = studentsData
    self.studentIDs = [student[0] for student in studentsData]

    self.setupUI()

  def setupUI(self):
    self.setMinimumSize(QtCore.QSize(400, 350))
    self.setMaximumSize(QtCore.QSize(500, 400))
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
    

    self.titleLabel = QtWidgets.QLabel("Update Multiple Students")
    self.titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
    self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    formLayout = QtWidgets.QFormLayout()

    # Only show selected student IDs
    studentNames = ", ".join(str(student[2]) for student in self.studentsData) if len(self.studentsData) <= 5 else f"{len(self.studentsData)} students selected"
    self.idLabel = QtWidgets.QLabel(studentNames)
    
    # Year Level
    self.yearLevelInput = QtWidgets.QComboBox(self)
    self.yearLevelInput.addItems(["", "1", "2", "3", "4", "5"])
    self.yearLevelInput.model().item(0).setEnabled(False)

    # Gender
    self.genderInput = QtWidgets.QComboBox(self)
    self.genderInput.addItems(["", "Male", "Female", "Others"])
    self.genderInput.model().item(0).setEnabled(False)

    # College and Program
    self.collegeCodeInput = QtWidgets.QComboBox(self)
    self.programCodeInput = QtWidgets.QComboBox(self)

    colleges = getAllColleges()
    collegeCodeList = [college["College Code"] for college in colleges]
    self.collegeCodeInput.addItems([""] + collegeCodeList)

    # Update programs when college changes
    self.collegeCodeInput.currentIndexChanged.connect(self.updateProgramOptions)

    formLayout.addRow("Students:", self.idLabel)
    formLayout.addRow("Year Level:", self.yearLevelInput)
    formLayout.addRow("Gender:", self.genderInput)
    formLayout.addRow("College Code:", self.collegeCodeInput)
    formLayout.addRow("Program Code:", self.programCodeInput)

    # Update Button
    self.updateButton = QtWidgets.QPushButton("Update Students")
    self.updateButton.setMinimumSize(QtCore.QSize(120, 40))
    self.updateButton.setMaximumSize(QtCore.QSize(140, 40))
    self.updateButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    self.updateButton.clicked.connect(self.updateStudents)

    buttonLayout = QtWidgets.QHBoxLayout()
    buttonLayout.addStretch()
    buttonLayout.addWidget(self.updateButton)
    buttonLayout.addStretch()

    self.statusBar = QtWidgets.QLabel("")
    self.statusBar.setStyleSheet("background-color: none; color: red; border-top: 1px solid #666666; padding: 4px; text-align: center")
    self.statusBar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    mainLayout = QtWidgets.QVBoxLayout()
    mainLayout.addWidget(self.titleLabel)
    mainLayout.addLayout(formLayout)
    mainLayout.addLayout(buttonLayout)
    mainLayout.addWidget(self.statusBar)

    mainLayout.setContentsMargins(15, 15, 15, 15)
    self.setLayout(mainLayout)

  def updateProgramOptions(self):
    selectedCollege = self.collegeCodeInput.currentText()
    programs = searchProgramsByField(selectedCollege, "College Code")
    programCodeList = [program["Program Code"] for program in programs]

    self.programCodeInput.clear()
    self.programCodeInput.addItems(programCodeList)

  def updateStudents(self):
    updatedStudents = []
    
    yearLevel = self.yearLevelInput.currentText() if self.yearLevelInput.currentText() != "" else None
    gender = self.genderInput.currentText() if self.genderInput.currentText() != "" else None
    programCode = self.programCodeInput.currentText() if self.programCodeInput.currentText() != "" else None
    collegeCode = self.collegeCodeInput.currentText() if self.collegeCodeInput.currentText() != "" else None

    for idNumber in self.studentIDs:
      result = updateStudent(idNumber, idNumber, None, None, yearLevel, gender, programCode, collegeCode)
      if result != "Student updated successfully.":
        self.showStatusMessage(result)
        return
      updatedStudents.append([idNumber, idNumber, None, None, gender, yearLevel, programCode, collegeCode])

    self.studentUpdatedTableSignal.emit(updatedStudents)
    self.statusMessageSignal.emit("Students Updated", 3000)
    self.accept()

  def showStatusMessage(self, message):
      self.statusBar.setText(message)
