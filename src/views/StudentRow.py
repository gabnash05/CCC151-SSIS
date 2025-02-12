import os
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtGui import QCursor

class StudentRow(QtWidgets.QWidget):
  def __init__(self, studentData, parent=None):
    super().__init__(parent)
    
    self.setMinimumSize(QtCore.QSize(400, 30))
    self.setMaximumSize(QtCore.QSize(16777215, 40))
    
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

    # Add student labels
    for index, value in enumerate(studentData):
      label = QtWidgets.QLabel(self.rowFrame)
      label.setText(str(value))
      label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
      
      if index == 1:
        label.setMinimumWidth(150)
      elif index == 6:
        label.setMinimumWidth(100)
      else:
        label.setMinimumWidth(60)

      rowLayout.addWidget(label)

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
    self.setButtonsVisible(False)  # Start with hidden buttons
    
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

  def setButtonIcon(self, button, relativePath, size):
    absolutePath = os.path.abspath(relativePath)
    icon = QtGui.QIcon(absolutePath)
    button.setIcon(icon)
    button.setIconSize(QtCore.QSize(size, size))

  def setButtonsVisible(self, visible):
    opacity = 1.0 if visible else 0.0
    self.editOpacity.setOpacity(opacity)
    self.deleteOpacity.setOpacity(opacity)

  def enterEvent(self, event):
    self.setButtonsVisible(True)

  def leaveEvent(self, event):
    self.setButtonsVisible(False)