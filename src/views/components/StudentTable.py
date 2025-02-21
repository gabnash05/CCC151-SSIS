import sys

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import pyqtSignal

from views.components.StudentRow import StudentRow
from controllers.studentControllers import getAllStudents

class StudentTable(QtWidgets.QWidget):
  # Student variables
  headers = ["ID Number", "Name", "Gender", "Year Level", "Program", "College", "Operations"]
  sortByFields = [("ID Number", "Last Name"), ("First Name", "Last Name"), ("Last Name", "First Name"), ("Gender", "Last Name"), ("Year Level", "Last Name"), ("Program Code", "Last Name"), ("College Code", "Last Name")]

  # Signals
  statusMessageSignal = pyqtSignal(str, int)
  editStudentSignal = pyqtSignal(list)

  def __init__(self, parent=None):
    super().__init__(parent)

    self.parentWidget = parent

    self.setupUI()

    self.students = []
    self.sortByIndex = 0
    self.sortingOrder = 0

    self.initialStudentsToDisplay()

  # UI Setup
  def setupUI(self):
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
      label.setStyleSheet("font: 9pt 'Inter'; font-weight: bold;")
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

  #--------------------------------------------------------------------------
  
  # Displays data provided to the table
  def refreshDisplayStudents(self):
    self.updateSortByIndex()

    # 2 Layer sorting based on predefined sortByField tuples
    if self.sortingOrder == 0:
      sortedStudents = sorted(self.students, 
                              key=lambda x: (x[self.sortByFields[self.sortByIndex][0]], x[self.sortByFields[self.sortByIndex][1]]))
    elif self.sortingOrder == 1:
      sortedStudents = sorted(self.students, 
                              key=lambda x: (x[self.sortByFields[self.sortByIndex][0]], x[self.sortByFields[self.sortByIndex][1]]),
                              reverse=True)
    
    self.clearScrollArea()

    for student in sortedStudents:
      self.addStudentRowToTable(student)
  
  # Changes the set of students in StudentTable
  def setStudents(self, newStudents):
    if newStudents == None:
      self.statusMessageSignal.emit("No Students Found", 3000)
      return
    
    self.students.clear()

    self.students.extend(newStudents)

    self.refreshDisplayStudents()

  # Deletes all StudentRows in StudentTable
  def clearScrollArea(self):
    for i in reversed(range(self.scrollLayout.count())):
      widget = self.scrollLayout.itemAt(i).widget()
      if widget is not None:
        widget.deleteLater()

  # Generates StudentRows into StudentTable
  def addStudentRowToTable(self, studentData):
    studentRow = StudentRow(studentData, self.scrollContent)
    studentRow.statusMessageSignal.connect(self.statusMessageSignal)
    studentRow.editStudentSignal.connect(self.editStudentSignal.emit)
    self.scrollLayout.addWidget(studentRow)
    self.scrollLayout.addWidget(studentRow.separator)
  
  # Reloads StudentTable when new student is adden from AddStudentDialog
  def addNewStudentToTable(self, studentData):
    newStudent = {
      "ID Number": studentData[0],
      "First Name": studentData[1],
      "Last Name": studentData[2],
      "Gender": studentData[3],
      "Year Level": studentData[4],
      "Program Code": studentData[5],
      "College Code": studentData[6]
    }

    if any(student["ID Number"] == newStudent["ID Number"] for student in self.students):
      return

    if self.searchActive:
      self.parentWidget.searchStudents()
    else:
      self.students.append(newStudent)
      self.refreshDisplayStudents()

  # Edits a StudentRow in StudentTable
  def editStudentInTable(self, studentData):
    originalIDNumber = studentData[0]

    newStudent = {
      "ID Number": studentData[1],
      "First Name": studentData[2],
      "Last Name": studentData[3],
      "Gender": studentData[4],
      "Year Level": studentData[5],
      "Program Code": studentData[6],
      "College Code": studentData[7]
    }

    for student in self.students:
      if student["ID Number"] == originalIDNumber:
        student.update(newStudent)
    
    self.refreshDisplayStudents()

  # Gets all students in the student.csv file
  def initialStudentsToDisplay(self):
    self.clearScrollArea()
    self.students.clear()

    students = getAllStudents()
    if not students:
      return
    
    self.students.extend(students)

    self.refreshDisplayStudents()
  
  # Sends signal for deleting student
  def handleStudentDeleted(self, message, duration):
    self.refreshDisplayStudents()
    self.statusMessageSignal.emit(message, duration)

  # Updates the sortByIndex for sorting in refreshDisplayStudents
  def updateSortByIndex(self):
    sortByIndex = self.parentWidget.sortByComboBox.currentIndex()
    sortingOrder = self.parentWidget.sortingOrderComboBox.currentIndex()

    if sortByIndex <= 0:
      self.sortByIndex = 0
    else:
      self.sortByIndex = sortByIndex - 1
    
    if sortingOrder < 0:
      self.sortingOrder = 0
    else:
      self.sortingOrder = sortingOrder


