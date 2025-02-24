import sys
from operator import itemgetter

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication

from views.components.CollegeRow import CollegeRow
from controllers.collegeControllers import getAllColleges

class CollegeTable(QtWidgets.QWidget):
  # Student variables
  headers = ["College Code", "College Name", "Operations"]
  sortByFields = [("College Code", "College Name"), ("College Name", "College Code")]

  # Signals
  statusMessageSignal = pyqtSignal(str, int)
  editCollegeSignal = pyqtSignal(list)
  updateTablesSignal = pyqtSignal()

  def __init__(self, parent=None):
    super().__init__(parent)

    self.parentWidget = parent

    self.setupUI()

    self.colleges = []
    self.sortByIndex = 0
    self.sortingOrder = 0

    self.initialCollegesToDisplay()
    

  # UI Setup
  def setupUI(self):
    # Updating Status Bar
    self.statusMessageSignal.emit("College Table Loading", 3000)
    
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
        label.setMinimumWidth(500)
      else:
        label.setMinimumWidth(100)

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
  def refreshDisplayColleges(self):
    if not self.colleges or "College Code" not in self.colleges[0]:
      self.clearScrollArea()
      self.statusMessageSignal.emit("No students found", 3000)
      return
    
    self.updateSortByIndex()
    
    primaryField, secondaryField = self.sortByFields[self.sortByIndex]
    reverseOrder = (self.sortingOrder == 1)
    
    # In-place sorting using Timsort (O(n log n))
    self.colleges.sort(key=itemgetter(primaryField, secondaryField), reverse=reverseOrder)
    
    self.clearScrollArea()

    self.scrollArea.setUpdatesEnabled(False)

    for college in self.colleges:
      self.addCollegeRowToTable(college)
      QApplication.processEvents()
    
    self.scrollArea.setUpdatesEnabled(True)
  
  # Changes the set of programs in ProgramTable
  def setColleges(self, newColleges):
    if newColleges == None:
      self.statusMessageSignal.emit("No Colleges Found", 3000)
      return

    self.colleges = newColleges

    self.refreshDisplayColleges()

  # Deletes all ProgramRows in ProgramTable
  def clearScrollArea(self):
    if self.scrollLayout.count() == 0:
      return

    self.scrollArea.setUpdatesEnabled(False)

    while self.scrollLayout.count():
      item = self.scrollLayout.takeAt(0)
      widget = item.widget()
      if widget:
        widget.setParent(None)
    
    self.scrollArea.setUpdatesEnabled(True)

  # Generates ProgramRows into ProgramTable
  def addCollegeRowToTable(self, collegeData):
    collegeRow = CollegeRow(collegeData, self.scrollContent)
    collegeRow.statusMessageSignal.connect(self.statusMessageSignal)
    collegeRow.editCollegeSignal.connect(self.editCollegeSignal.emit)
    collegeRow.updateTablesSignal.connect(self.updateTablesSignal)
    self.scrollLayout.addWidget(collegeRow)
    self.scrollLayout.addWidget(collegeRow.separator)
  
  # Reloads CollegeTable when new college is adden from AddCollegeDialog
  def addNewCollegeToTable(self, collegeData):
    newCollege = {
      "College Code": collegeData[0],
      "College Name": collegeData[1],
    }

    self.colleges.append(newCollege)
    self.refreshDisplayColleges()

  # Edits a CollegeRow in CollegeTable
  def editCollegeInTable(self, collegeData):
    originalCollegeCode = collegeData[0]

    newCollege = {
      "College Code": collegeData[1],
      "College Name": collegeData[2],
    }

    for college in self.colleges:
      if college["College Code"] == originalCollegeCode:
        college.update(newCollege)
    
    self.refreshDisplayColleges()

  # Gets all colleges in the college.csv file
  def initialCollegesToDisplay(self):
    self.clearScrollArea()

    colleges = getAllColleges()
    if not colleges:
      return
    
    self.colleges = colleges

    self.refreshDisplayColleges()
  
  # Updates the sortByIndex for sorting in refreshDisplayColleges
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

