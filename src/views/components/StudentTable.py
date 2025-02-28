from operator import itemgetter

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QTableWidgetItem
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon

from controllers.studentControllers import getAllStudents, removeStudent
from views.components.UpdateStudentDialog import UpdateStudentDialog
from views.components.UpdateBatchStudentDialog import UpdateBatchStudentDialog

class StudentTable(QtWidgets.QTableWidget):
  # Student variables
  headers = ["ID Number", "Name", "Gender", "Year Level", "Program", "College", "Operations"]
  sortByFields = [("ID Number", "Last Name"), ("First Name", "Last Name"), ("Last Name", "First Name"), ("Gender", "Last Name"), ("Year Level", "Last Name"), ("Program Code", "Last Name"), ("College Code", "Last Name")]

  # Signals
  statusMessageSignal = pyqtSignal(str, int)
  editStudentSignal = pyqtSignal(list)
  deleteStudentSignal = pyqtSignal(str)

  def __init__(self, parent=None):
    super().__init__(parent)
    self.parentWidget = parent

    self.setupUI()
    self.students = []
    self.sortByIndex = 0
    self.sortingOrder = 0

    self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
    
    # For mouse features
    self.setMouseTracking(True)
    self.viewport().setMouseTracking(True)
    self.viewport().installEventFilter(self)

    self.initialStudentsToDisplay()

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
    header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeMode.Fixed)
    
    self.setHorizontalHeaderLabels(self.headers)

  #--------------------------------------------------------------------------
  
  def refreshDisplayStudents(self):
    if not self.students or "ID Number" not in self.students[0]:
      self.setRowCount(0)
      self.statusMessageSignal.emit("No students found", 3000)
      return
    
    self.updateSortByIndex()
    primaryField, secondaryField = self.sortByFields[self.sortByIndex]
    reverseOrder = (self.sortingOrder == 1)
    
    self.students.sort(key=itemgetter(primaryField, secondaryField), reverse=reverseOrder)
    self.populateTable()

  def setStudents(self, newStudents):
    if newStudents is None:
      print("No records to set")
      return
    
    self.students = newStudents
    self.refreshDisplayStudents()

  def populateTable(self):
    self.setRowCount(len(self.students))
    
    for row, student in enumerate(self.students):
      self.setItem(row, 0, QtWidgets.QTableWidgetItem(str(student["ID Number"])))

      nameItem = QTableWidgetItem(f"{student['First Name']} {student['Last Name']}")
      self.setItem(row, 1, nameItem)

      genderItem = QTableWidgetItem(student["Gender"])
      genderItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      self.setItem(row, 2, genderItem)

      yearLevelItem = QTableWidgetItem(student["Year Level"])
      yearLevelItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      self.setItem(row, 3, yearLevelItem)

      programCodeItem = QTableWidgetItem(student["Program Code"])
      programCodeItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      self.setItem(row, 4, programCodeItem)

      collegeCodeItem = QTableWidgetItem(student["College Code"])
      collegeCodeItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      self.setItem(row, 5, collegeCodeItem)
      
      operationsWidget = QtWidgets.QWidget()
      operationsLayout = QtWidgets.QHBoxLayout()
      operationsLayout.setContentsMargins(0, 0, 0, 0)
      operationsLayout.setSpacing(0)

      editButton = QtWidgets.QPushButton()
      editButton.setObjectName("editButton")
      editButton.setIcon(QIcon("assets/edit.png"))
      editButton.setFixedSize(30, 30)
      editButton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
      editButton.clicked.connect(lambda _, s=student: self.openUpdateStudentDialog(s))
      
      self.editOpacity = QGraphicsOpacityEffect()
      editButton.setGraphicsEffect(self.editOpacity)
      self.editOpacity.setOpacity(0.0) 

      deleteButton = QtWidgets.QPushButton()
      deleteButton.setObjectName("deleteButton")
      deleteButton.setIcon(QIcon("assets/delete.png"))
      deleteButton.setFixedSize(30, 30)
      deleteButton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
      deleteButton.clicked.connect(lambda _, s=student: self.deleteSelectedRow(s))

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
      
      self.setCellWidget(row, 6, operationsWidget)

    self.viewport().installEventFilter(self)

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
    
    self.students.append(newStudent)
    self.refreshDisplayStudents()

  def editStudentsInTable(self, studentsData):
    for studentData in studentsData:
      originalIDNumber = studentData[0]
      newStudent = {
        key: value
        for key, value in {
          "ID Number": studentData[1],
          "First Name": studentData[2],
          "Last Name": studentData[3],
          "Year Level": studentData[5],
          "Gender": studentData[4],
          "Program Code": studentData[6],
          "College Code": studentData[7]
        }.items()
        if value is not None
      }
        
      for student in self.students:
        if student["ID Number"] == originalIDNumber:
          student.update(newStudent)
    
    self.refreshDisplayStudents()

  def initialStudentsToDisplay(self):
    self.setRowCount(0)
    students = getAllStudents()
    if not students:
      return
    
    self.students = students
    self.refreshDisplayStudents()

  def updateSortByIndex(self):
    sortByIndex = self.parentWidget.sortByComboBox.currentIndex()
    sortingOrder = self.parentWidget.sortingOrderComboBox.currentIndex()
    
    self.sortByIndex = max(0, sortByIndex - 1)
    self.sortingOrder = max(0, sortingOrder)
  
  def openUpdateStudentDialog(self, studentRowData):
    selectedRows = list(set(index.row() for index in self.selectedIndexes()))
    if not selectedRows or len(selectedRows) == 1:
      studentData = list(studentRowData.values())
      self.updateDialog = UpdateStudentDialog(self, studentData)
      self.updateDialog.studentUpdatedTableSignal.connect(self.editStudentsInTable)
      self.updateDialog.statusMessageSignal.connect(self.parentWidget.displayMessageToStatusBar)
      self.updateDialog.exec()
      return

    studentsData = [
      [
        self.item(row, 0).text() if self.item(row, 0) else "",  # ID Number
        self.item(row, 1).text().split()[0] if self.item(row, 1) else "",  # First Name
        " ".join(self.item(row, 1).text().split()[1:]) if self.item(row, 1) else "",  # Last Name
        self.item(row, 3).text() if self.item(row, 3) else "",  # Year Level
        self.item(row, 2).text() if self.item(row, 2) else "",  # Gender
        self.item(row, 4).text() if self.item(row, 4) else "",  # Program Code
        self.item(row, 5).text() if self.item(row, 5) else "",  # College Code
      ]
      for row in selectedRows
    ]

    self.updateDialog = UpdateBatchStudentDialog(self, studentsData)
    self.updateDialog.studentUpdatedTableSignal.connect(self.editStudentsInTable)
    self.updateDialog.statusMessageSignal.connect(self.parentWidget.displayMessageToStatusBar)
    self.updateDialog.exec()

  def deleteSelectedRow(self, student):
    selectedRows = sorted(set(index.row() for index in self.selectedIndexes()), reverse=True)
    selectedRowCount = len(selectedRows)

    # Single Deletion
    if len(selectedRows) > 1:
      studentNames = f'\n{"\n".join(f'{self.item(row, 1).text()}' for row in selectedRows)}'

      promptText = f"the following students?\n{studentNames}" if selectedRowCount < 20 else f"{selectedRowCount} students"

      if not self.showDeleteConfirmation(self, promptText):
        return
      
      failedDeletions = []

      for row in sorted(selectedRows, reverse=True):  # Reverse to avoid shifting indices
        student = self.students[row]
        result = removeStudent(student["ID Number"])

        if result == "Student removed successfully.":
          self.students.pop(row)
          self.removeRow(row)
        else:
          failedDeletions.append(student["ID Number"])

      # Emit status message
      if failedDeletions:
        self.statusMessageSignal.emit(f"Failed to remove: {', '.join(failedDeletions)}", 3000)
      else:
        self.statusMessageSignal.emit("Selected students removed successfully.", 3000)
    
    # Multiple Deletions
    else:
      if not self.showDeleteConfirmation(self, f'{student["First Name"]} {student["Last Name"]}'):
        return

      # Remove from CSV
      result = removeStudent(student["ID Number"])

      if result != "Student removed successfully.":
        self.statusMessageSignal.emit(result, 3000)
        return

      # Find the row index of the student
      rowToRemove = -1
      for row in range(self.rowCount()):
        if self.item(row, 0) and self.item(row, 0).text() == str(student["ID Number"]):
          rowToRemove = row
          break

      if rowToRemove == -1:
        self.statusMessageSignal.emit("Error: Student not found in table.", 3000)
        return

      # Remove student from internal list
      self.students.remove(student)

      # Remove row from QTableWidget
      self.removeRow(rowToRemove)

      self.statusMessageSignal.emit(result, 3000)

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
  
  def handleStudentDeleted(self, message, duration):
    self.refreshDisplayStudents()
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
      operationsWidget = self.cellWidget(r, 6)
      if operationsWidget:
        for i in range(operationsWidget.layout().count()):
          widget = operationsWidget.layout().itemAt(i).widget()
          if widget and isinstance(widget.graphicsEffect(), QGraphicsOpacityEffect):
            widget.graphicsEffect().setOpacity(1.0 if r == row else 0.0)