import sys

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import pyqtSignal

from views.components.ProgramRow import ProgramRow
from controllers.programControllers import getAllPrograms

class ProgramTable(QtWidgets.QWidget):
  # Student variables
  headers = ["Program Code", "Program Name", "College Code", "Operations"]
  sortByFields = [("Program Code", "Program Name"), ("Program Name", "College Code"), ("College Code", "Program Name")]

  # Signals
  statusMessageSignal = pyqtSignal(str, int)
  editProgramSignal = pyqtSignal(list)

  def __init__(self, parent=None):
    super().__init__(parent)

    self.parentWidget = parent

    self.setupUI()

    self.programs = []
    self.sortByIndex = 0
    self.sortingOrder = 0

    self.initialProgramsToDisplay()

  # UI Setup
  def setupUI(self):
    # Updating Status Bar
    self.statusMessageSignal.emit("Program Table Loading", 3000)
    
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
      # Set width constraints
      if i == 1:  # Name column
        label.setMinimumWidth(400)
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
  def refreshDisplayPrograms(self):
    self.updateSortByIndex()

    if self.programs == [None]:
      self.clearScrollArea()
      return

    # 2 Layer sorting based on predefined sortByField tuples
    if self.sortingOrder == 0:
      sortedPrograms = sorted(self.programs, 
                              key=lambda x: (x[self.sortByFields[self.sortByIndex][0]], x[self.sortByFields[self.sortByIndex][1]]))
    elif self.sortingOrder == 1:
      sortedPrograms = sorted(self.programs, 
                              key=lambda x: (x[self.sortByFields[self.sortByIndex][0]], x[self.sortByFields[self.sortByIndex][1]]),
                              reverse=True)
    
    self.clearScrollArea()

    for program in sortedPrograms:
      self.addProgramRowToTable(program)
  
  # Changes the set of programs in ProgramTable
  def setPrograms(self, newPrograms):
    if newPrograms == None:
      print("No records to set")
      return
    
    self.programs.clear()

    self.programs.extend(newPrograms)

    self.refreshDisplayPrograms()

  # Deletes all ProgramRows in ProgramTable
  def clearScrollArea(self):
    for i in reversed(range(self.scrollLayout.count())):
      widget = self.scrollLayout.itemAt(i).widget()
      if widget is not None:
        widget.deleteLater()

  # Generates ProgramRows into ProgramTable
  def addProgramRowToTable(self, programData):
    programRow = ProgramRow(programData, self.scrollContent)
    programRow.statusMessageSignal.connect(self.statusMessageSignal)
    programRow.editProgramSignal.connect(self.editProgramSignal.emit)
    self.scrollLayout.addWidget(programRow)
    self.scrollLayout.addWidget(programRow.separator)
  
  # Reloads ProgramTable when new student is adden from AddStudentDialog
  def addNewProgramToTable(self, programData):
    newProgram = {
      "Program Code": programData[0],
      "Program Name": programData[1],
      "College Code": programData[2],
    }

    if any(program["Program Code"] == newProgram["Program Code"] for program in self.programs):
      return

    self.programs.append(newProgram)
    self.refreshDisplayPrograms()

  # Edits a StudentRow in ProgramTable
  def editProgramInTable(self, programData):
    originalProgramCode = programData[0]

    newProgram = {
      "Program Code": programData[1],
      "Program Name": programData[2],
      "College Code": programData[3],
    }

    for program in self.programs:
      if program["Program Code"] == originalProgramCode:
        program.update(newProgram)
    
    self.refreshDisplayPrograms()

  # Gets all programs in the program.csv file
  def initialProgramsToDisplay(self):
    self.clearScrollArea()
    self.programs.clear()

    programs = getAllPrograms()
    if not programs:
      return
    
    self.programs.extend(programs)

    self.refreshDisplayPrograms()
  
  # Sends signal for deleting program
  def handleProgramDeleted(self, message, duration):
    self.refreshDisplayPrograms()
    self.statusMessageSignal.emit(message, duration)

  # Updates the sortByIndex for sorting in refreshDisplayPrograms
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

