import sys

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import pyqtSignal

from views.components.CollegeRow import CollegeRow
from controllers.collegeControllers import getAllColleges

class CollegeTable(QtWidgets.QWidget):
  # Student variables
  headers = ["College Code", "College Name", "Operations"]
  sortByFields = [("College Code", "College Name"), ("College Name", "College Code")]

  # Signals
  statusMessageSignal = pyqtSignal(str, int)
  editCollegeSignal = pyqtSignal(list)

  def __init__(self, parent=None):
    super().__init__(parent)

    self.parentWidget = parent

    self.setupUI()

    self.colleges = []
    self.sortByIndex = 0
    self.sortingOrder = 0
    self.searchActive = False

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
    self.updateSortByIndex()

    if self.colleges == [None]:
      self.clearScrollArea()
      return

    # 2 Layer sorting based on predefined sortByField tuples
    if self.sortingOrder == 0:
      sortedColleges = sorted(self.colleges, 
                              key=lambda x: (x[self.sortByFields[self.sortByIndex][0]], x[self.sortByFields[self.sortByIndex][1]]))
    elif self.sortingOrder == 1:
      sortedColleges = sorted(self.colleges, 
                              key=lambda x: (x[self.sortByFields[self.sortByIndex][0]], x[self.sortByFields[self.sortByIndex][1]]),
                              reverse=True)
    
    self.clearScrollArea()
    
    for college in sortedColleges:
      self.addCollegeRowToTable(college)
  
  # Changes the set of programs in ProgramTable
  def setColleges(self, newColleges):
    if newColleges == None:
      self.statusMessageSignal.emit("No Colleges Found", 3000)
      return
    
    self.colleges.clear()

    self.colleges.extend(newColleges)

    self.refreshDisplayColleges()

  # Deletes all ProgramRows in ProgramTable
  def clearScrollArea(self):
    for i in reversed(range(self.scrollLayout.count())):
      widget = self.scrollLayout.itemAt(i).widget()
      if widget is not None:
        widget.deleteLater()

  # Generates ProgramRows into ProgramTable
  def addCollegeRowToTable(self, collegeData):
    collegeRow = CollegeRow(collegeData, self.scrollContent)
    collegeRow.statusMessageSignal.connect(self.statusMessageSignal)
    collegeRow.editCollegeSignal.connect(self.editCollegeSignal.emit)
    self.scrollLayout.addWidget(collegeRow)
    self.scrollLayout.addWidget(collegeRow.separator)
  
  # Reloads CollegeTable when new college is adden from AddCollegeDialog
  def addNewCollegeToTable(self, collegeData):
    newCollege = {
      "College Code": collegeData[0],
      "College Name": collegeData[1],
    }

    if any(college["College Code"] == newCollege["College Code"] for college in self.colleges):
      return

    if self.searchActive:
      self.parentWidget.searchColleges()
    else:
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
    self.colleges.clear()

    colleges = getAllColleges()
    self.colleges.extend(colleges)

    self.refreshDisplayColleges()
  
  # Sends signal for deleting college
  def handleCollegeDeleted(self, message, duration):
    self.refreshDisplayColleges()
    self.statusMessageSignal.emit(message, duration)

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
















if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  window = CollegeTable()
  window.show()
  sys.exit(app.exec())
