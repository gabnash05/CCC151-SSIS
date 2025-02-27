from PyQt6 import QtWidgets, QtCore, QtGui

from controllers.programControllers import updateProgram
from controllers.collegeControllers import getAllColleges

class UpdateProgramDialog(QtWidgets.QDialog):
  programUpdatedTableSignal = QtCore.pyqtSignal(list)
  statusMessageSignal = QtCore.pyqtSignal(str, int)
  updateTablesSignal = QtCore.pyqtSignal()

  def __init__(self, parent=None, programData=None):
    super().__init__(parent)
    self.setWindowTitle("Update Program")
    self.setModal(True)
    
    self.originalProgramCode = programData[0]

    self.setupUI(programData)

  def setupUI(self, programData):
    # Set Window Size
    self.setMinimumSize(QtCore.QSize(400, 300))
    self.setMaximumSize(QtCore.QSize(500, 300))

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
                          background-color: rgb(37, 37, 37);
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
    self.programCodeInput = QtWidgets.QLineEdit(self)
    self.programCodeInput.setText(programData[0])

    self.programNameInput = QtWidgets.QLineEdit(self)
    self.programNameInput.setText(programData[1])

    self.collegeCodeInput = QtWidgets.QComboBox(self)

    colleges = getAllColleges()
    collegeCodeList = [college["College Code"] for college in colleges]
    self.collegeCodeInput.addItems(collegeCodeList)

    if programData[2] != "N/A":
      collegeIndex = collegeCodeList.index(programData[2])
      self.collegeCodeInput.setCurrentIndex(collegeIndex)

    # Section Headers
    self.titleLabel = QtWidgets.QLabel("Update Program")
    self.titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
    self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    self.programInfoLabel = QtWidgets.QLabel("Program Information")
    self.programInfoLabel.setStyleSheet("font-size: 19px; font-weight: bold;")

    # Update Button
    self.updateButton = QtWidgets.QPushButton("Update Program")
    self.updateButton.setMinimumSize(QtCore.QSize(120, 40))
    self.updateButton.setMaximumSize(QtCore.QSize(140, 40))
    self.updateButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    self.updateButton.clicked.connect(self.updateProgram)

    # Layout
    formLayout = QtWidgets.QFormLayout()
    formLayout.addRow(self.titleLabel)
    formLayout.addRow(QtWidgets.QLabel(""))

    formLayout.addRow(self.programInfoLabel)
    formLayout.addRow("Program Code:", self.programCodeInput)
    formLayout.addRow("Name:", self.programNameInput)
    formLayout.addRow("College Code:", self.collegeCodeInput)
    formLayout.addRow(QtWidgets.QLabel(""))

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
  
  def updateProgram(self):
    programCode = self.programCodeInput.text().strip() or None
    programName = self.programNameInput.text().strip() or None
    collegeCode = self.collegeCodeInput.currentText() or None

    result = updateProgram(self.originalProgramCode, programCode, programName, collegeCode)

    if result == "Program updated successfully.":
      self.showStatusMessage(result)
      self.statusBar.setStyleSheet("background-color: none; color: green; border-top: 1px solid #666666; padding: 4px; text-align: center")

      # Send signal to MainWindow to call addStudent in StudentTable
      self.programUpdatedTableSignal.emit([[self.originalProgramCode, programCode, programName, collegeCode]])
      self.updateTablesSignal.emit()
      self.statusMessageSignal.emit("Updating Program", 1000)

      # Closes the QDialog
      self.accept()
    else:
      self.showStatusMessage(result)
      return

    # Emit signal
    self.statusMessageSignal.emit("Program Updated", 3000)

    # Close dialog
    self.accept()

  def showStatusMessage(self, message):
    self.statusBar.setText(message)

