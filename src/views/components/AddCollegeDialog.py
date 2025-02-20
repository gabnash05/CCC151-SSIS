from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt, pyqtSignal

from controllers.collegeControllers import addCollege

class AddCollegeDialog(QtWidgets.QDialog):
  collegeAddedTableSignal = pyqtSignal(list)
  collegeAddedWindowSignal = pyqtSignal(str, int)

  def __init__(self, parent=None):
    super().__init__(parent)
    self.setWindowTitle("Add Program")
    self.setModal(True)

    self.setupUI()
    
  def setupUI(self):
    # Window Init
    self.setMinimumSize(QtCore.QSize(400, 250))
    self.setMaximumSize(QtCore.QSize(500, 250))

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
    self.collegeCodeInput = QtWidgets.QLineEdit(self)
    self.collegeNameInput = QtWidgets.QLineEdit(self)

    # Section headers
    self.titleLabel = QtWidgets.QLabel("Add College")
    self.titleLabel.setFont(QtGui.QFont("Inter", 18, QtGui.QFont.Weight.Bold))
    self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    self.titleLayout = QtWidgets.QHBoxLayout()
    self.titleLayout.addStretch()
    self.titleLayout.addWidget(self.titleLabel)
    self.titleLayout.addStretch()

    self.collegeInfoLabel = QtWidgets.QLabel("College Information")
    self.collegeInfoLabel.setFont(QtGui.QFont("Inter", 14, QtGui.QFont.Weight.Bold))

    # Button to add student
    self.addButton = QtWidgets.QPushButton("Add College")
    self.addButton.setMinimumSize(QtCore.QSize(120, 40))
    self.addButton.setMaximumSize(QtCore.QSize(140, 40))
    self.addButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

    # Connect Button
    self.addButton.clicked.connect(self.addCollege)

    # Layout
    formLayout = QtWidgets.QFormLayout()
    formLayout.addRow(self.titleLayout)
    formLayout.addRow(QtWidgets.QLabel(""))  # Spacer under title

    formLayout.addRow(self.collegeInfoLabel)
    formLayout.addRow("College Code:", self.collegeCodeInput)
    formLayout.addRow("College Name:", self.collegeNameInput)

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
  def addCollege(self):
    collegeCode = self.collegeCodeInput.text().strip() or None
    collegeName = self.collegeNameInput.text().strip() or None

    result = addCollege(collegeCode, collegeName)

    if result == "College added successfully.":
      self.showStatusMessage(result)

      # Send signal to ProgramPage to call addProgram in ProgramTable
      self.collegeAddedTableSignal.emit([collegeCode, collegeName])
      self.collegeAddedWindowSignal.emit("College Added", 1000)

      # Closes the QDialog
      self.accept()
    else:
      self.showStatusMessage(result)
      return

  def showStatusMessage(self, message):
    self.statusBar.setText(message)
















# Example usage in Main Window
class MainWindow(QtWidgets.QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Student Management")

    self.add_student_button = QtWidgets.QPushButton("Add Student", self)
    self.add_student_button.clicked.connect(self.open_add_student_dialog)

    self.setCentralWidget(self.add_student_button)

  def open_add_student_dialog(self):
    dialog = AddCollegeDialog(self)
    dialog.exec()


if __name__ == "__main__":
  app = QtWidgets.QApplication([])
  window = MainWindow()
  window.show()
  app.exec()
