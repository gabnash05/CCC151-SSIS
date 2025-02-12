import os
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

class StudentTable(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Layout
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

        headers = ["ID Number", "Name", "Gender", "Year Level", "Program", "College", "Operations"]
        stretch_values = [1, 1, 1, 1, 1, 1, 1]

        # Set Alignment and Resizing Policies
        for i, header in enumerate(headers):
            label = QtWidgets.QLabel(header, self.tableHeaderFrame)
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label.setObjectName(f"headerLabel_{i}")

            # Set width constraints
            if i == 1:  # Name column
                label.setMinimumWidth(150)
            elif i == 6:  # Operations column
                label.setMinimumWidth(100)
                label.setMaximumSize(QtCore.QSize(90, 16777215))  # Match operationsFrame in student rows
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
                label.setSizePolicy(sizePolicy)
            else:
                label.setMinimumWidth(60)

            self.horizontalLayout_2.addWidget(label, stretch_values[i])

        self.mainLayout.addWidget(self.tableHeaderFrame)



        #--------------------------------------------------------------
        # Separator Line (QFrame) between Header and Data
        self.headerSeparator = QtWidgets.QFrame(self)
        self.headerSeparator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.headerSeparator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.headerSeparator.setStyleSheet("background-color: rgb(120, 139, 140);")
        self.headerSeparator.setMaximumHeight(1)  # Thin line
        self.mainLayout.addWidget(self.headerSeparator)



        #---------------------------------------------------------------
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
        
        scrollAreaStyle = "QScrollArea { background: transparent; border: none; font: Inter; } QScrollArea::viewport { background: transparent; } QScrollArea QWidget { background: transparent; } QScrollBar:vertical, QScrollBar:horizontal { background: #222222; border-radius: 5px; width: 10px; height: 10px; } QScrollBar::handle:vertical, QScrollBar::handle:horizontal { background: #888888; border-radius: 5px; min-height: 20px; min-width: 20px; } QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover { background: #777777; }"
        self.scrollArea.setStyleSheet(scrollAreaStyle)

        self.scrollArea.setWidget(self.scrollContent)  # Attach the scrollable content
        self.mainLayout.addWidget(self.scrollArea)  # Add the scroll area to main layout
        
        students = [
            ("2023-0001", "Kim Gabriel A. Nasayao", "Male", "2", "BSCS", "CCS"),
            ("2023-0002", "Jane Doe", "Female", "3", "BSIT", "CCS"),
            ("2023-0003", "John Smith", "Male", "1", "BSECE", "COE"),
        ] * 10
        
        for student in students:
            self.addStudent(student)



    # FUNCTIONS
    # -----------------------------------------------------------------------

    def addStudent(self, studentData):
        row, separator = self.createStudentRow(self.scrollContent, studentData)
        self.scrollLayout.addWidget(row)
        self.scrollLayout.addWidget(separator)

    def createStudentRow(self, parent, studentData):
        rowFrame = QtWidgets.QFrame(parent)
        rowFrame.setMinimumSize(QtCore.QSize(400, 30))
        rowFrame.setMaximumSize(QtCore.QSize(16777215, 40))
        rowFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        rowFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        
        # Adds a stylesheet
        rowFrameStyle = "QPushButton { font: 9pt \"Inter\"; font-weight: bold; padding: 0px 15px; border-radius: 3px; } #deleteButton { background-color: rgb(160, 63, 63); } #editButton { background-color: rgb(63, 150, 160); } #editButton::hover { background-color: rgb(83, 170, 180); } #deleteButton::hover { background-color: rgb(180, 83, 83); } QFrame { border: none; background: transparent; } QLabel { border: none; background: transparent; font: 9pt \"Inter\"; }"

        rowFrame.setStyleSheet(rowFrameStyle)
        
        layout = QtWidgets.QHBoxLayout(rowFrame)
        layout.setContentsMargins(15, 0, 15, 0)

        # Create labels for student info
        for index, value in enumerate(studentData):
            label = QtWidgets.QLabel(rowFrame)
            label.setText(str(value))
            
            # Set alignment:
            if index == 1:
                label.setMinimumWidth(150)
            elif index == 6:
                label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                label.setMinimumWidth(100)
            else:
                label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                label.setMinimumWidth(60)

            layout.addWidget(label)
        
        # Operations frame
        operationsFrame = QtWidgets.QFrame(rowFrame)
        operationsLayout = QtWidgets.QHBoxLayout(operationsFrame)
        operationsLayout.setContentsMargins(0, 0, 0, 0)
        operationsFrame.setMinimumSize(QtCore.QSize(90, 16777215))
        operationsFrame.setMaximumSize(QtCore.QSize(90, 16777215))
        
        editButton = QtWidgets.QPushButton("", operationsFrame)
        editButton.setObjectName("editButton")
        deleteButton = QtWidgets.QPushButton("", operationsFrame)
        deleteButton.setObjectName("deleteButton")

        editIconRelativePath = "assets/edit.png"
        deleteIconRelativePath = "assets/delete.png"
        editIconAbsolutePath = os.path.abspath(editIconRelativePath)
        deleteIconAbsolutePath = os.path.abspath(deleteIconRelativePath)

        editIcon = QtGui.QIcon(editIconAbsolutePath)
        editButton.setIcon(editIcon)
        editButton.setIconSize(QtCore.QSize(15, 15))

        deleteIcon = QtGui.QIcon(deleteIconAbsolutePath)
        deleteButton.setIcon(deleteIcon)
        deleteButton.setIconSize(QtCore.QSize(15, 15))

        editButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        deleteButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                           
        editButton.setMaximumSize(QtCore.QSize(40, 16777215))
        editButton.setMinimumSize(QtCore.QSize(40, 30))
        deleteButton.setMaximumSize(QtCore.QSize(40, 16777215))
        deleteButton.setMinimumSize(QtCore.QSize(40, 30))
        
        operationsLayout.addWidget(editButton)
        operationsLayout.addWidget(deleteButton)
        layout.addWidget(operationsFrame)
        
        # Separator line
        separator = QtWidgets.QFrame(parent)
        separator.setMaximumSize(QtCore.QSize(16777215, 1))
        separator.setStyleSheet("background-color: rgb(120, 139, 140);")
        separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        
        return rowFrame, separator


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = StudentTable()
    window.show()
    sys.exit(app.exec())
