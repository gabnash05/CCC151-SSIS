import sys
from typing import List, Dict, Any
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, pyqtSignal

from views.StudentRow import StudentRow
from controllers.studentControllers import getAllStudents

class StudentTable(QtWidgets.QWidget):
  # Student variables
  headers = ["ID Number", "Name", "Gender", "Year Level", "Program", "College", "Operations"]
  sortByFields = ["ID Number", "Name", "Gender", "Year Level", "Program", "College", "Operations"]
  statusMessageSignal = pyqtSignal(str, int)

  def __init__(self, parent=None):
    super().__init__(parent)

    # Updating Status Bar
    self.statusMessageSignal.emit("Student Table Loading", 3000)
    
    # Main Layout
    self.mainLayout = QtWidgets.QVBoxLayout(self)
    self.mainLayout.setContentsMargins(0, 0, 0, 0)
    self.mainLayout.setSpacing(0)
    
    # Table Header Frame
    self.tableHeaderFrame = QtWidgets.QFrame(self)
    self.tableHeaderFrame.setMinimumSize(QtCore.QSize(0, 50))
    self.tableHeaderFrame.setMaximumSize(QtCore.QSize(16777215, 50))
    self.tableHeaderFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
    self.tableHeaderFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

    self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tableHeaderFrame)
    self.horizontalLayout_2.setContentsMargins(15, 0, 15, 0)

    # Set Alignment and Resizing Policies
    for i, header in enumerate(self.headers):
      label = QtWidgets.QLabel(header, self.tableHeaderFrame)
      label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
      label.setObjectName(f"headerLabel_{i}")

      # Set width constraints
      if i == 1:  # Name column
        label.setMinimumWidth(150)
      elif i == 6:  # Operations column
        label.setMinimumWidth(100)
        label.setMaximumSize(QtCore.QSize(90, 16777215)) 
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        label.setSizePolicy(sizePolicy)
      else:
        label.setMinimumWidth(60)

      self.horizontalLayout_2.addWidget(label, 1)

    self.mainLayout.addWidget(self.tableHeaderFrame)

    # Separator Line (QFrame) between Header and Data
    self.headerSeparator = QtWidgets.QFrame(self)
    self.headerSeparator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
    self.headerSeparator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
    self.headerSeparator.setStyleSheet("background-color: rgb(120, 139, 140);")
    self.headerSeparator.setMaximumHeight(1)  # Thin line
    self.mainLayout.addWidget(self.headerSeparator)
    
    # Scroll Area
    self.scrollArea = QtWidgets.QScrollArea(self)
    self.scrollArea.setWidgetResizable(True)
    self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    # Scroll Content Widget
    self.scrollContent = QtWidgets.QWidget()
    self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollContent)
    self.scrollLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
    self.scrollLayout.setContentsMargins(0, 0, 0, 0)
    self.scrollLayout.setSpacing(2)
    
    scrollAreaStyle = """
      QScrollArea { background: transparent; border: none; font: Inter; }
      QScrollArea::viewport { background: transparent; }
      QScrollArea QWidget { background: transparent; }
      QScrollBar:vertical, QScrollBar:horizontal { background: #222222; border-radius: 5px; width: 10px; height: 10px; }
      QScrollBar::handle:vertical, QScrollBar::handle:horizontal { background: #AAAAAA; border-radius: 5px; min-height: 20px; min-width: 20px; }
      QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover { background: #777777; }
    """
    self.scrollArea.setStyleSheet(scrollAreaStyle)

    self.scrollArea.setWidget(self.scrollContent)
    self.mainLayout.addWidget(self.scrollArea)
    
    # Displaying initial data to display
    students = self.initialSetStudentsToDisplay()
    
    for student in students:
      self.addStudentToTable(student)

  #--------------------------------------------------------------------------

  # Generates StudentRows into Student Table
  # Connected to an emitted signal from AddStudentDialogue
  def addStudentToTable(self, studentData):
    studentRow = StudentRow(studentData, self.scrollContent)
    studentRow.statusMessageSignal.connect(self.statusMessageSignal)
    self.scrollLayout.addWidget(studentRow)
    self.scrollLayout.addWidget(studentRow.separator)

  # Gets all students in the student.csv file
  def initialSetStudentsToDisplay(self) -> List[List[str]]:
    students = getAllStudents()
    studentsList = [
    [student["ID Number"], f"{student["First Name"]} {student["Last Name"]}", student["Gender"], student["Year Level"], student["Program Code"], student["College Code"]]
      for student in students
    ]

    return studentsList
  
  # WIP
  # Displays data provided to the table
  def displayStudents(self, parent, students: List[Dict[str, str]], sortBy: str) -> None:
    if sortBy not in self.sortByFields:
      # display error message to status bar
      return
    
    # delete all qframes in scroll area

    for student in students:
      self.addStudentToTable(student)

  def handleStudentDeleted(self, message, duration):
    self.statusMessageSignal.emit(message, duration)

if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  window = StudentTable()
  window.show()
  sys.exit(app.exec())
