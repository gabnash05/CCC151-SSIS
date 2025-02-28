from operator import itemgetter

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QTableWidgetItem
from PyQt6.QtGui import QIcon

from views.components.UpdateProgramDialog import UpdateProgramDialog

from controllers.programControllers import getAllPrograms
from controllers.programControllers import removeProgram

class ProgramTable(QtWidgets.QTableWidget):
  # Program variables
  headers = ["Program Code", "Program Name", "College Code", "Operations"]
  sortByFields = [("Program Code", "Program Name"), ("Program Name", "College Code"), ("College Code", "Program Name")]

  # Signals
  statusMessageSignal = pyqtSignal(str, int)
  editProgramSignal = pyqtSignal(list)
  deleteProgramSignal = pyqtSignal(str)
  updateTablesSignal = pyqtSignal()

  def __init__(self, parent=None):
    super().__init__(parent)

    self.parentWidget = parent

    self.setupUI()
    self.programs = []
    self.sortByIndex = 0
    self.sortingOrder = 0

    self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)

    # For mouse features
    self.setMouseTracking(True)
    self.viewport().setMouseTracking(True)
    self.viewport().installEventFilter(self)

    self.initialProgramsToDisplay()

  def setupUI(self):
    self.setColumnCount(len(self.headers))
    self.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
    self.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
    self.setSortingEnabled(False)
    self.setStyleSheet("""
                        QHeaderView::section { 
                          font-weight: bold; 
                          font-size: 9pt;
                        }
                       QHeaderView::section:vertical {
                          font-weight: normal; 
                          font-size: 9pt;
                        }
                        QPushButton { 
                          font: 9pt "Inter"; 
                          font-weight: bold; 
                          padding: 0px 15px; 
                          border-radius: 3px; 
                        } 
                       
                        QTableWidget {
                            gridline-color: transparent;
                        }
                        QTableWidget::item {
                            border-bottom: 1px solid rgb(120, 139, 140); 
                            border-right: 1px solid transparent;
                        }
                        QTableWidget::item:selected {
                          background-color: rgb(105, 105, 105); 
                        }
                        #deleteButton { background-color: rgb(160, 63, 63); } 
                        #editButton { background-color: rgb(63, 150, 160); } 
                        #editButton::hover { background-color: rgb(83, 170, 180); } 
                        #deleteButton::hover { background-color: rgb(180, 83, 83); } 
                        QFrame { border: none; background: transparent; } 
                        QLabel { border: none; background: transparent; font: 9pt "Inter"; }
                      """)
    
    self.verticalHeader().setDefaultSectionSize(40)  # Increase row height
    self.verticalHeader().setFixedWidth(35)
    self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
    
    header = self.horizontalHeader()
    header.setMinimumHeight(40)
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Fixed)
    
    self.setHorizontalHeaderLabels(self.headers)

  #--------------------------------------------------------------------------
  
  def refreshDisplayPrograms(self):
    if not self.programs or "Program Code" not in self.programs[0]:
      self.setRowCount(0)
      self.statusMessageSignal.emit("No programs found", 3000)
      return
    
    self.updateSortByIndex()
    primaryField, secondaryField = self.sortByFields[self.sortByIndex]
    reverseOrder = (self.sortingOrder == 1)
    
    self.programs.sort(key=itemgetter(primaryField, secondaryField), reverse=reverseOrder)
    self.populateTable()
  
  def setPrograms(self, newPrograms):
    if newPrograms is None:
      print("No records to set")
      return

    self.programs = newPrograms
    self.refreshDisplayPrograms()

  def populateTable(self):
    self.setRowCount(len(self.programs))
    
    for row, program in enumerate(self.programs):
      self.setItem(row, 0, QtWidgets.QTableWidgetItem(str(program["Program Code"])))

      programName = QTableWidgetItem(program["Program Name"])
      self.setItem(row, 1, programName)

      collegeCode = QTableWidgetItem(program["College Code"])
      collegeCode.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      self.setItem(row, 2, collegeCode)
      
      operationsWidget = QtWidgets.QWidget()
      operationsLayout = QtWidgets.QHBoxLayout()
      operationsLayout.setContentsMargins(0, 0, 0, 0)
      operationsLayout.setSpacing(0)

      editButton = QtWidgets.QPushButton()
      editButton.setObjectName("editButton")
      editButton.setIcon(QIcon("assets/edit.png"))
      editButton.setFixedSize(30, 30)
      editButton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
      editButton.clicked.connect(lambda _, s=program: self.openUpdateProgramDialog(s))
      
      self.editOpacity = QGraphicsOpacityEffect()
      editButton.setGraphicsEffect(self.editOpacity)
      self.editOpacity.setOpacity(0.0) 

      deleteButton = QtWidgets.QPushButton()
      deleteButton.setObjectName("deleteButton")
      deleteButton.setIcon(QIcon("assets/delete.png"))
      deleteButton.setFixedSize(30, 30)
      deleteButton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
      deleteButton.clicked.connect(lambda _, s=program: self.deleteSelectedRow(s))

      self.deleteOpacity = QGraphicsOpacityEffect()
      deleteButton.setGraphicsEffect(self.deleteOpacity)
      self.deleteOpacity.setOpacity(0.0)

      operationsLayout.addWidget(editButton)
      operationsLayout.addWidget(deleteButton)
      operationsWidget.setLayout(operationsLayout)
      operationsWidget.setStyleSheet(operationsWidget.setStyleSheet("""
        QPushButton { font: 9pt "Inter"; font-weight: bold; padding: 0px 15px; border-radius: 3px; }
        QPushButton#editButton { background-color: rgb(63, 150, 160); }
        QPushButton#deleteButton { background-color: rgb(160, 63, 63); }
        QPushButton#editButton:hover { background-color: rgb(83, 170, 180); }
        QPushButton#deleteButton:hover { background-color: rgb(180, 83, 83); }
      """))
      
      self.setCellWidget(row, 3, operationsWidget)

    self.viewport().installEventFilter(self)

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

  def editProgramInTable(self, programsData):
    for programData in programsData:
      originalProgramCode = programData[0]

      newProgram = {
        key: value
        for key, value in {
          "Program Code": programData[1],
          "Program Name": programData[2],
          "College Code": programData[3],
        }.items()
        if value is not None
      }

    for program in self.programs:
      if program["Program Code"] == originalProgramCode:
        program.update(newProgram)
    
    self.refreshDisplayPrograms()

  def initialProgramsToDisplay(self):
    self.setRowCount(0)
    programs = getAllPrograms()
    if not programs:
      return
    
    self.programs = programs
    self.refreshDisplayPrograms()

  def updateSortByIndex(self):
    sortByIndex = self.parentWidget.sortByComboBox.currentIndex()
    sortingOrder = self.parentWidget.sortingOrderComboBox.currentIndex()

    self.sortByIndex = max(0, sortByIndex - 1)
    self.sortingOrder = max(0, sortingOrder)

  def openUpdateProgramDialog(self, programRowData):
    selectedRows = list(set(index.row() for index in self.selectedIndexes()))
    programData = list(programRowData.values())
    self.updateDialog = UpdateProgramDialog(self, programData)
    self.updateDialog.programUpdatedTableSignal.connect(self.editProgramInTable)
    self.updateDialog.updateTablesSignal.connect(self.updateTablesSignal)
    self.updateDialog.statusMessageSignal.connect(self.parentWidget.displayMessageToStatusBar)

    if len(selectedRows) > 1:
      self.statusMessageSignal.emit("Programs can only be updated one at a time.", 3000)
      
    self.updateDialog.exec()

  def deleteSelectedRow(self, program):
    selectedRows = sorted(set(index.row() for index in self.selectedIndexes()), reverse=True)
    selectedRowCount = len(selectedRows)

    # Multiple Deletions
    if len(selectedRows) > 1:
      programCodes = f'\n{"\n".join(f'{self.item(row, 0).text()}' for row in selectedRows)}'

      promptText = f"the following programs?\n{programCodes}" if selectedRowCount < 20 else f"{selectedRowCount} programs"

      if not self.showDeleteConfirmation(self, promptText):
        return
      
      failedDeletions = []

      for row in sorted(selectedRows, reverse=True):  # Reverse to avoid shifting indices
        program = self.programs[row]
        result = removeProgram(program["Program Code"])

        if result == "Program removed successfully.":
          self.programs.pop(row)
          self.removeRow(row)
        else:
          failedDeletions.append(program["Program Code"])

      # Emit status message
      if failedDeletions:
        self.statusMessageSignal.emit(f"Failed to remove: {', '.join(failedDeletions)}", 3000)
      else:
        self.statusMessageSignal.emit("Selected programs removed successfully.", 3000)
    
    # Single Deletion
    else:
      if not self.showDeleteConfirmation(self, program["Program Name"]):
        return

      # Remove from CSV
      result = removeProgram(program["Program Code"])

      if result != "Program removed successfully.":
        self.statusMessageSignal.emit(result, 3000)
        return

      # Find the row index of the program
      rowToRemove = -1
      for row in range(self.rowCount()):
        if self.item(row, 0) and self.item(row, 0).text() == str(program["Program Code"]):
          rowToRemove = row
          break

      if rowToRemove == -1:
        self.statusMessageSignal.emit("Error: Program not found in table.", 3000)
        return

      # Remove program from internal list
      self.programs.remove(program)

      # Remove row from QTableWidget
      self.removeRow(rowToRemove)
      self.statusMessageSignal.emit(result, 3000)
    
    self.updateTablesSignal.emit()

  def showDeleteConfirmation(self, parent, programName):
    msgBox = QtWidgets.QMessageBox(parent)
    msgBox.setWindowTitle("Confirm Deletion")
    msgBox.setText(f"Are you sure you want to delete {programName}?")
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
  
  def handleProgramDeleted(self, message, duration):
    self.refreshDisplayPrograms()
    self.statusMessageSignal.emit(message, duration)

  def eventFilter(self, obj, event):
    if obj == self.viewport():
      if event.type() == QtCore.QEvent.Type.MouseMove:
        index = self.indexAt(event.pos())  # Get index of row under mouse
        if index.isValid():
          self.toggleButtons(index.row())
        else:
          self.toggleButtons(-1)  # Hide buttons when not over a valid row
      elif event.type() == QtCore.QEvent.Type.Leave:
        self.toggleButtons(-1)  # Hide buttons when mouse leaves the table
    return super().eventFilter(obj, event)

  def toggleButtons(self, row):
    for r in range(self.rowCount()):
      operationsWidget = self.cellWidget(r, 3)
      if operationsWidget:
        for i in range(operationsWidget.layout().count()):
          widget = operationsWidget.layout().itemAt(i).widget()
          if widget and isinstance(widget.graphicsEffect(), QGraphicsOpacityEffect):
            widget.graphicsEffect().setOpacity(1.0 if r == row else 0.0)