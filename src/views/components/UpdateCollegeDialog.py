from PyQt6 import QtWidgets, QtCore, QtGui

from controllers.collegeControllers import getAllColleges, updateCollege

class UpdateCollegeDialog(QtWidgets.QDialog):
  collegeUpdatedTableSignal = QtCore.pyqtSignal(list)
  statusMessageSignal = QtCore.pyqtSignal(str, int)
  updateTablesSignal = QtCore.pyqtSignal()

  def __init__(self, parent=None, collegeData=None):
    super().__init__(parent)
    self.setWindowTitle("Update College")
    self.setModal(True)
    
    self.originalCollegeCode = collegeData[0]

    self.setupUI(collegeData)

  def setupUI(self, collegeData):
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
    self.collegeCodeInput = QtWidgets.QLineEdit(self)
    self.collegeCodeInput.setText(collegeData[0])

    self.collegeNameInput = QtWidgets.QLineEdit(self)
    self.collegeNameInput.setText(collegeData[1])

    # Section Headers
    self.titleLabel = QtWidgets.QLabel("Update College")
    self.titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
    self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    self.collegeInfoLabel = QtWidgets.QLabel("College Information")
    self.collegeInfoLabel.setStyleSheet("font-size: 19px; font-weight: bold;")

    # Update Button
    self.updateButton = QtWidgets.QPushButton("Update College")
    self.updateButton.setMinimumSize(QtCore.QSize(120, 40))
    self.updateButton.setMaximumSize(QtCore.QSize(140, 40))
    self.updateButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    self.updateButton.clicked.connect(self.updateCollege)

    # Layout
    formLayout = QtWidgets.QFormLayout()
    formLayout.addRow(self.titleLabel)
    formLayout.addRow(QtWidgets.QLabel(""))

    formLayout.addRow(self.collegeInfoLabel)
    formLayout.addRow("College Code:", self.collegeCodeInput)
    formLayout.addRow("Name:", self.collegeNameInput)
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
  
  def updateCollege(self):
    collegeCode = self.collegeCodeInput.text().strip() or None
    collegeName = self.collegeNameInput.text().strip() or None

    result = updateCollege(self.originalCollegeCode, collegeCode, collegeName)

    if result == "College updated successfully.":
      self.showStatusMessage(result)
      self.statusBar.setStyleSheet("background-color: none; color: green; border-top: 1px solid #666666; padding: 4px; text-align: center")

      # Send signal to MainWindow to call addStudent in StudentTable
      self.collegeUpdatedTableSignal.emit([[self.originalCollegeCode, collegeCode, collegeName]])
      self.updateTablesSignal.emit()
      self.statusMessageSignal.emit("Updating College", 1000)

      # Closes the QDialog
      self.accept()
    else:
      self.showStatusMessage(result)
      return

    # Emit signal
    self.statusMessageSignal.emit("College Updated", 3000)

    # Close dialog
    self.accept()

  def showStatusMessage(self, message):
    self.statusBar.setText(message)

