import os
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import pyqtSignal, Qt

from views.components.UpdateStudentDialog import UpdateStudentDialog
from controllers.studentControllers import removeStudent

class StudentRow(QtWidgets.QWidget):
  statusMessageSignal = pyqtSignal(str, int)
  editStudentSignal = pyqtSignal(list)

  def __init__(self, studentData, parent=None):
    super().__init__(parent)
    # Store StudentRow Variables
    self.studentData = studentData

    self.idNumber = studentData["ID Number"]
    self.studentName = studentData["Last Name"] + " " + studentData["First Name"]

    self.setupUI()

    # Initialize
  
  def setupUI(self):
    self.setMinimumSize(QtCore.QSize(400, 30))
    self.setMaximumSize(QtCore.QSize(16777215, 40))
    self.setObjectName("rowFrame")
    
    # StyleSheet
    rowFrameStyle = """
      QPushButton { 
        font: 9pt "Inter"; 
        font-weight: bold; 
        padding: 0px 15px; 
        border-radius: 3px; 
      } 
      #deleteButton { background-color: rgb(160, 63, 63); } 
      #editButton { background-color: rgb(63, 150, 160); } 
      #editButton::hover { background-color: rgb(83, 170, 180); } 
      #deleteButton::hover { background-color: rgb(180, 83, 83); } 
      QFrame { border: none; background: transparent; } 
      QLabel { border: none; background: transparent; font: 9pt "Inter"; }

      """
    self.setStyleSheet(rowFrameStyle)

    # Main Layout
    mainLayout = QtWidgets.QVBoxLayout(self)
    mainLayout.setContentsMargins(0, 0, 0, 0)

    # Create row frame
    self.rowFrame = QtWidgets.QFrame(self)
    rowLayout = QtWidgets.QHBoxLayout(self.rowFrame)
    rowLayout.setContentsMargins(15, 0, 15, 0)
    mainLayout.addWidget(self.rowFrame)

    # ID Number label
    idNumberLabel = QtWidgets.QLabel(self.rowFrame)
    idNumberLabel.setText(str(self.studentData["ID Number"]))
    idNumberLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    idNumberLabel.setMinimumWidth(60)
    idNumberLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    rowLayout.addWidget(idNumberLabel)

    # Name label
    studentName = str(self.studentData["First Name"]) + " " + str(self.studentData["Last Name"])
    nameLabel = QtWidgets.QLabel(self.rowFrame)
    nameLabel.setText(str(studentName))
    nameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    nameLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    nameLabel.setMinimumWidth(150)


    # ELITE STUDENTS
    if studentName == "Joaquin Ermita" or studentName == "Rene Jr Estrella":
      nameLabel.setStyleSheet("color: #FFD700; font-weight: bold;")
    elif studentName == "Kesa Sysn":
      nameLabel.setStyleSheet("color: pink; font-weight: bold;")
    elif studentName == "Vincee Jandayan":
      nameLabel.setStyleSheet("color: #B9FF66; font-weight: bold;")

    rowLayout.addWidget(nameLabel)

    # Gender label
    genderLabel = QtWidgets.QLabel(self.rowFrame)
    genderLabel.setText(str(self.studentData["Gender"]))
    genderLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    genderLabel.setMinimumWidth(60)
    genderLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    rowLayout.addWidget(genderLabel)

    # Year Level label
    yearLevelLabel = QtWidgets.QLabel(self.rowFrame)
    yearLevelLabel.setText(str(self.studentData["Year Level"]))
    yearLevelLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    yearLevelLabel.setMinimumWidth(60)
    yearLevelLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    rowLayout.addWidget(yearLevelLabel)

    # Program Code label
    programCodeLabel = QtWidgets.QLabel(self.rowFrame)
    programCodeLabel.setText(str(self.studentData["Program Code"]))
    programCodeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    programCodeLabel.setMinimumWidth(60)
    programCodeLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    rowLayout.addWidget(programCodeLabel)

    # College Code label
    collegeCodeLabel = QtWidgets.QLabel(self.rowFrame)
    collegeCodeLabel.setText(str(self.studentData["College Code"]))
    collegeCodeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    collegeCodeLabel.setMinimumWidth(60)
    collegeCodeLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    rowLayout.addWidget(collegeCodeLabel)

    # Operations Frame (for buttons)
    self.operationsFrame = QtWidgets.QFrame(self.rowFrame)
    operationsLayout = QtWidgets.QHBoxLayout(self.operationsFrame)
    operationsLayout.setContentsMargins(0, 0, 0, 0)
    self.operationsFrame.setFixedSize(90, 30)
    
    # Edit & Delete Buttons
    self.editButton = QtWidgets.QPushButton("", self.operationsFrame)
    self.editButton.setObjectName("editButton")
    self.deleteButton = QtWidgets.QPushButton("", self.operationsFrame)
    self.deleteButton.setObjectName("deleteButton")

    # Icons
    self.setButtonIcon(self.editButton, "assets/edit.png", 15)
    self.setButtonIcon(self.deleteButton, "assets/delete.png", 15)

    # Button Cursors
    self.editButton.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    self.deleteButton.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                        
    # Button Sizes
    self.editButton.setFixedSize(40, 30)
    self.deleteButton.setFixedSize(40, 30)

    # Apply opacity effect to buttons
    self.editOpacity = QGraphicsOpacityEffect()
    self.deleteOpacity = QGraphicsOpacityEffect()
    self.editButton.setGraphicsEffect(self.editOpacity)
    self.deleteButton.setGraphicsEffect(self.deleteOpacity)
    self.setButtonsVisible(False)

    # Connect Buttons
    self.deleteButton.clicked.connect(self.deleteRow)
    self.editButton.clicked.connect(self.sendStudentData)

    operationsLayout.addWidget(self.editButton)
    operationsLayout.addWidget(self.deleteButton)
    rowLayout.addWidget(self.operationsFrame)

    # Separator Line
    self.separator = QtWidgets.QFrame(self)
    self.separator.setMaximumSize(QtCore.QSize(16777215, 1))
    self.separator.setStyleSheet("background-color: rgb(120, 139, 140);")
    self.separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
    self.separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
    mainLayout.addWidget(self.separator)

  # ----------------------------------------------------------------------
  # Deletes a student in the GUI and CSV
  def deleteRow(self):
    # "Are you sure if you want to delete" POPUP
    if not self.showDeleteConfirmation(self, self.studentName):
      return

    # Remove from csv
    result = removeStudent(self.idNumber)
    
    # Remove the widget
    if result != "Student removed successfully.":
      self.statusMessageSignal.emit(result, 3000)
      return
    
    if self.parent():
      layout = self.parent().layout()
      if layout:
        layout.removeWidget(self)
        layout.removeWidget(self.separator)
      self.separator.deleteLater()
    self.deleteLater()
    self.statusMessageSignal.emit(result, 3000)

  # Sends Signal to update a student
  def sendStudentData(self):
    self.editStudentSignal.emit(self.studentData.values())

  # Creates a pop up when deleting a student
  def showDeleteConfirmation(self, parent, studentName):
    msgBox = QtWidgets.QMessageBox(parent)
    msgBox.setWindowTitle("Confirm Deletion")
    msgBox.setText(f"Are you sure you want to delete {studentName}?")
    msgBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
    msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

    for button in msgBox.findChildren(QtWidgets.QPushButton):
      button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

    msgBox.setStyleSheet("""
      QMessageBox {
        background-color: rgb(37, 37, 37);
        color: white;
        border-radius: 10px;
      }
      QMessageBox QLabel {
        color: white;
        font-family: \"Inter\";
      }
      QMessageBox QPushButton {
        font: 9pt "Inter";
        font-weight: bold;
        padding: 0px, 15px;
        background-color: rgb(63, 150, 160);
        border-radius: 3px;
        padding: 5px 15px;
      }
                         
      QMessageBox QPushButton::hover {
        background-color: rgb(83, 170, 180);
      }
    """)

    # Show the dialog and return the user's choice
    return msgBox.exec() == QtWidgets.QMessageBox.StandardButton.Yes
  
  # Helper function to add icons to buttons
  def setButtonIcon(self, button, relativePath, size):
    absolutePath = os.path.abspath(relativePath)
    icon = QtGui.QIcon(absolutePath)
    button.setIcon(icon)
    button.setIconSize(QtCore.QSize(size, size))

  # Sets button visibility in row
  def setButtonsVisible(self, visible):
    opacity = 1.0 if visible else 0.0
    self.editOpacity.setOpacity(opacity)
    self.deleteOpacity.setOpacity(opacity)

  # Checks if mouse enters row
  def enterEvent(self, event):
    self.setButtonsVisible(True)

  # Checks if mouse leaves row
  def leaveEvent(self, event):
    self.setButtonsVisible(False)