from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSignal, Qt

from controllers.collegeControllers import searchCollegesByField

from views.components.CollegeTable import CollegeTable
from views.components.AddCollegeDialog import AddCollegeDialog
from views.components.UpdateCollegeDialog import UpdateCollegeDialog


class CollegesPage(QtWidgets.QWidget):
  searchByFields = ["College Code", "College Name"]

  statusMessageSignal = pyqtSignal(str, int)
  spacebarPressedSignal = pyqtSignal()
  updateTablesSignal = pyqtSignal()

  def __init__(self, parent=None):
    super().__init__(parent)
    self.setupUi()

    self.collegeTable = CollegeTable(self)
    self.dataFrame.layout().addWidget(self.collegeTable)

    # CONNECT SIGNALS
    self.collegeTable.statusMessageSignal.connect(self.displayMessageToStatusBar)
    self.collegeTable.updateTablesSignal.connect(self.updateTablesSignal)

    self.addCollegeButton.clicked.connect(self.openAddCollegeDialog)
    self.collegeTable.editCollegeSignal.connect(self.openUpdateCollegeDialog)

    self.sortByComboBox.currentIndexChanged.connect(lambda: self.statusMessageSignal.emit("Sorting...", 2000))
    self.sortingOrderComboBox.currentIndexChanged.connect(lambda: self.statusMessageSignal.emit("Sorting...", 2000))
    self.sortByComboBox.currentIndexChanged.connect(self.collegeTable.refreshDisplayColleges)
    self.sortingOrderComboBox.currentIndexChanged.connect(self.collegeTable.refreshDisplayColleges)

    self.searchButton.clicked.connect(self.searchColleges)
    self.spacebarPressedSignal.connect(self.searchColleges)

    self.displayMessageToStatusBar("Programs Page Loaded", 3000)
      
  def setupUi(self):
    self.setObjectName("mainWindow")
    self.resize(1037, 715)

    font = QtGui.QFont()
    font.setFamily("Inter")
    font.setPointSize(9)
    font.setBold(False)
    font.setItalic(False)
    self.setFont(font)

    self.setAutoFillBackground(False)
    self.setStyleSheet(
"/* DROP DOWNS */\n"
"QComboBox {\n"
"    border-radius: 2px;\n"
"    border: 1px solid rgb(180, 180, 180) !important;\n"
"    font: 9pt \"Inter\";\n"
"    color: rgb(230, 230, 230);\n"
"    background-color: rgb(16, 16, 16);\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"  subcontrol-origin: padding;\n"
"  subcontrol-position: top right;\n"
"  width: 15px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item::hover {\n"
"    background-color: rgb(35, 35, 35);\n"
"}\n"
"\n"
"QComboBox::hover {\n"
"    background-color: rgb(35, 35, 35);\n"
"}\n"
"\n"
"/* BUTTONS */\n"
"QPushButton {\n"
"    font: 9pt \"Inter\";\n"
"    font-weight: bold;\n"
"    padding: 0px, 15px;\n"
"    background-color: rgb(63, 150, 160);\n"
"    border-radius: 3px;\n"
"    padding: 0px 15px;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    background-color: rgb(83, 170, 180);\n"
"}\n"
"\n"
"#sidebarFrame QPushButton {\n"
"    font: 12pt \"Inter\";\n"
"    font-weight: 600;\n"
"    background-color: rgb(37, 37, 37);\n"
"    border-radius: 0px;\n"
"    text-align: left;\n"
"    padding-left: 45px\n"
"}\n"
"\n"
"#sidebarFrame QPushButton::hover {\n"
"    background-color: rgb(47, 47, 47);\n"
"    border-radius: 0px;\n"
"}\n"
"\n"
"#sidebarFrame #collegesSidebarButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(71, 71, 71, 255), stop:1 rgba(95, 105, 106, 255));\n"
"    border-left: 4px solid rgb(93, 180, 190);\n"
"}\n"
"\n"
"#headerFrame QPushButton {\n"
"    background: none;\n"
"}\n"
"\n"
"#sortByLabel {\n"
"    color: rgb(100, 100, 100)\n"
"}\n"
"\n"
"/* LINE EDIT */\n"
"#searchBarLineEdit {\n"
"    background-color: rgb(37, 37, 37);\n"
"    border-radius: 2px;\n"
"    padding: 0px 15px;\n"
"}\n"
"\n"
"/* FRAMES */\n"
"QFrame {\n"
"  border: none;\n"
"}\n"
"\n"
"#dataFrame {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(37, 37, 37, 255), stop:1 rgba(52, 57, 57, 255));\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"#headerFrame {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(63, 150, 160, 255), stop:1 rgba(38, 85, 90, 255));\n"
"    border: 1px solid rgba(0, 0, 0, 30);\n"
"}\n"
"\n"
"#sidebarFrame {\n"
"    background-color: rgb(37, 37, 37);\n"
"}\n"
"\n"
"/* LABELS */\n"
"#collegeLabel {\n"
"  font: 20pt \"Inter\";\n"
"  font-weight: bold;\n"
"}\n"
"\n"
"#tableHeaderFrame QLabel {\n"
"    font: 9pt \"Inter\";\n"
"    font-weight: 500;\n"
"    color: rgb(120, 139, 140);\n"
"}\n"
"\n"
"#dataFrame Line {\n"
"    background-color: rgb(120, 139, 140);\n"
"}\n"
"\n"
"#userNameLabel {\n"
"    font: 9pt \"Inter\";\n"
"    font-weight: 600;\n"
"}\n"
"\n"
"#userRoleLabel {\n"
"    font: 9pt \"Inter\";\n"
"    font-style: italic;\n"
"}\n"
"\n"
"/* DATA TABLE */\n"
"#scrollArea QLabel {\n"
"    font: 9pt \"Inter\";\n"
"    font-weight: 500;\n"
"}\n"
"\n"
"#scrollArea Line {\n"
"    background-color: rgb(120, 139, 140);\n"
"}")
    self.setContentsMargins(0, 0, 0, 0)

    self.centralwidget = QtWidgets.QWidget(self)
    self.centralwidget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
    self.centralwidget.setStyleSheet("")
    self.centralwidget.setObjectName("centralwidget")

    self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
    self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
    self.verticalLayout_2.setSpacing(0)
    self.verticalLayout_2.setObjectName("verticalLayout_2")
    
    self.bodyFrame = QtWidgets.QFrame(parent=self.centralwidget)
    self.bodyFrame.setAutoFillBackground(False)
    self.bodyFrame.setStyleSheet("")
    self.bodyFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
    self.bodyFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
    self.bodyFrame.setObjectName("bodyFrame")
    self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.bodyFrame)
    self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
    self.horizontalLayout_7.setSpacing(0)
    self.horizontalLayout_7.setObjectName("horizontalLayout_7")
    self.sidebarFrame = QtWidgets.QFrame(parent=self.bodyFrame)
    self.sidebarFrame.setStyleSheet("")
    self.sidebarFrame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    self.sidebarFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
    self.sidebarFrame.setLineWidth(0)
    self.sidebarFrame.setObjectName("sidebarFrame")
    self.verticalLayout = QtWidgets.QVBoxLayout(self.sidebarFrame)
    self.verticalLayout.setContentsMargins(0, 0, 0, 0)
    self.verticalLayout.setSpacing(0)
    self.verticalLayout.setObjectName("verticalLayout")

    self.studentsSidebarButton = QtWidgets.QPushButton(parent=self.sidebarFrame)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.studentsSidebarButton.sizePolicy().hasHeightForWidth())
    self.studentsSidebarButton.setSizePolicy(sizePolicy)
    self.studentsSidebarButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

    icon2 = QtGui.QIcon()
    icon2.addPixmap(QtGui.QPixmap("assets/student.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
    self.studentsSidebarButton.setIcon(icon2)
    self.studentsSidebarButton.setIconSize(QtCore.QSize(30, 30))
    self.studentsSidebarButton.setObjectName("studentsSidebarButton")
    self.verticalLayout.addWidget(self.studentsSidebarButton)

    self.programsSidebarButton = QtWidgets.QPushButton(parent=self.sidebarFrame)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.studentsSidebarButton.sizePolicy().hasHeightForWidth())
    self.programsSidebarButton.setSizePolicy(sizePolicy)
    self.programsSidebarButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

    icon3 = QtGui.QIcon()
    icon3.addPixmap(QtGui.QPixmap("assets/program.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
    self.programsSidebarButton.setIcon(icon3)
    self.programsSidebarButton.setIconSize(QtCore.QSize(30, 30))
    self.programsSidebarButton.setObjectName("programsSidebarButton")
    self.verticalLayout.addWidget(self.programsSidebarButton)

    self.collegesSidebarButton = QtWidgets.QPushButton(parent=self.sidebarFrame)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.collegesSidebarButton.sizePolicy().hasHeightForWidth())
    self.collegesSidebarButton.setSizePolicy(sizePolicy)
    self.collegesSidebarButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

    icon4 = QtGui.QIcon()
    icon4.addPixmap(QtGui.QPixmap("assets/college.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
    self.collegesSidebarButton.setIcon(icon4)
    self.collegesSidebarButton.setIconSize(QtCore.QSize(30, 30))
    self.collegesSidebarButton.setAutoRepeat(False)
    self.collegesSidebarButton.setObjectName("collegesSidebarButton")
    self.verticalLayout.addWidget(self.collegesSidebarButton)

    spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
    self.verticalLayout.addItem(spacerItem1)
    self.verticalLayout.setStretch(0, 1)
    self.verticalLayout.setStretch(1, 1)
    self.verticalLayout.setStretch(2, 1)
    self.verticalLayout.setStretch(3, 10)

    self.horizontalLayout_7.addWidget(self.sidebarFrame)
    self.mainDisplayFrame = QtWidgets.QFrame(parent=self.bodyFrame)
    self.mainDisplayFrame.setStyleSheet("")
    self.mainDisplayFrame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    self.mainDisplayFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
    self.mainDisplayFrame.setLineWidth(0)
    self.mainDisplayFrame.setObjectName("mainDisplayFrame")
    self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.mainDisplayFrame)
    self.verticalLayout_3.setContentsMargins(35, 5, 35, 25)
    self.verticalLayout_3.setSpacing(5)
    self.verticalLayout_3.setObjectName("verticalLayout_3")
    self.searchBarFrame = QtWidgets.QFrame(parent=self.mainDisplayFrame)
    self.searchBarFrame.setMaximumSize(QtCore.QSize(16777215, 90))
    font = QtGui.QFont()
    font.setFamily("Inter 18pt")
    font.setPointSize(9)
    font.setBold(False)
    font.setItalic(False)
    self.searchBarFrame.setFont(font)
    self.searchBarFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
    self.searchBarFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
    self.searchBarFrame.setObjectName("searchBarFrame")
    self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.searchBarFrame)
    self.horizontalLayout_8.setContentsMargins(0, 15, 0, 20)
    self.horizontalLayout_8.setSpacing(10)
    self.horizontalLayout_8.setObjectName("horizontalLayout_8")
    self.searchBarLineEdit = QtWidgets.QLineEdit(parent=self.searchBarFrame)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.searchBarLineEdit.sizePolicy().hasHeightForWidth())
    self.searchBarLineEdit.setSizePolicy(sizePolicy)
    self.searchBarLineEdit.setMinimumSize(QtCore.QSize(100, 40))
    self.searchBarLineEdit.setMaximumSize(QtCore.QSize(16777215, 60))
    font = QtGui.QFont()
    font.setFamily("Inter")
    font.setPointSize(9)
    font.setBold(False)
    font.setItalic(False)
    self.searchBarLineEdit.setFont(font)
    self.searchBarLineEdit.setAutoFillBackground(False)
    self.searchBarLineEdit.setStyleSheet("")
    self.searchBarLineEdit.setObjectName("searchBarLineEdit")
    self.horizontalLayout_8.addWidget(self.searchBarLineEdit)
    self.searchButton = QtWidgets.QPushButton(parent=self.searchBarFrame)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
    self.searchButton.setSizePolicy(sizePolicy)
    self.searchButton.setMinimumSize(QtCore.QSize(0, 40))
    self.searchButton.setMaximumSize(QtCore.QSize(16777215, 60))
    font = QtGui.QFont()
    font.setFamily("Inter")
    font.setPointSize(9)
    font.setBold(True)
    font.setItalic(False)
    self.searchButton.setFont(font)
    self.searchButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    self.searchButton.setStyleSheet("")
    self.searchButton.setObjectName("searchButton")
    self.horizontalLayout_8.addWidget(self.searchButton)
    
    # searchByComboBox
    self.searchByComboBox = QtWidgets.QComboBox(parent=self.searchBarFrame)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.searchByComboBox.sizePolicy().hasHeightForWidth())

    self.searchByComboBox.setSizePolicy(sizePolicy)
    self.searchByComboBox.setMinimumSize(QtCore.QSize(120, 40))
    self.searchByComboBox.setMaximumSize(QtCore.QSize(16777215, 60))
    self.searchByComboBox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    self.searchByComboBox.setToolTipDuration(0)

    self.searchByComboBox.addItem("Search By")
    self.searchByComboBox.setCurrentIndex(0) 
    #self.searchByComboBox.model().item(0).setEnabled(False)

    self.searchByComboBox.setObjectName("searchByComboBox")
    self.searchByComboBox.addItem("")
    self.searchByComboBox.addItem("")
    self.horizontalLayout_8.addWidget(self.searchByComboBox)

    spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
    self.horizontalLayout_8.addItem(spacerItem2)
    self.horizontalLayout_8.setStretch(0, 8)
    self.horizontalLayout_8.setStretch(1, 1)
    self.horizontalLayout_8.setStretch(2, 1)
    self.horizontalLayout_8.setStretch(3, 2)
    self.verticalLayout_3.addWidget(self.searchBarFrame)
    self.controlsFrame = QtWidgets.QFrame(parent=self.mainDisplayFrame)
    self.controlsFrame.setMaximumSize(QtCore.QSize(16777215, 70))
    self.controlsFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
    self.controlsFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
    self.controlsFrame.setObjectName("controlsFrame")
    self.horizontalLayout = QtWidgets.QHBoxLayout(self.controlsFrame)
    self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
    self.horizontalLayout.setContentsMargins(-1, 11, 11, 11)
    self.horizontalLayout.setObjectName("horizontalLayout")
    self.collegeLabel = QtWidgets.QLabel(parent=self.controlsFrame)
    self.collegeLabel.setMinimumSize(QtCore.QSize(180, 0))
    self.collegeLabel.setMaximumSize(QtCore.QSize(200, 16777215))
    self.collegeLabel.setObjectName("collegeLabel")
    self.horizontalLayout.addWidget(self.collegeLabel)
    self.addCollegeButton = QtWidgets.QPushButton(parent=self.controlsFrame)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.addCollegeButton.sizePolicy().hasHeightForWidth())
    self.addCollegeButton.setSizePolicy(sizePolicy)
    self.addCollegeButton.setMaximumSize(QtCore.QSize(150, 16777215))
    font = QtGui.QFont()
    font.setFamily("Inter")
    font.setPointSize(9)
    font.setBold(True)
    font.setItalic(False)
    self.addCollegeButton.setFont(font)
    self.addCollegeButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    self.addCollegeButton.setStyleSheet("")
    self.addCollegeButton.setObjectName("addCollegeButton")
    self.horizontalLayout.addWidget(self.addCollegeButton)

    self.sortByComboBox = QtWidgets.QComboBox(parent=self.controlsFrame)
    self.sortByComboBox.setEnabled(True)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.sortByComboBox.sizePolicy().hasHeightForWidth())
    self.sortByComboBox.setSizePolicy(sizePolicy)
    self.sortByComboBox.setMinimumSize(QtCore.QSize(85, 40))
    self.sortByComboBox.setMaximumSize(QtCore.QSize(150, 16777215))
    font = QtGui.QFont()
    font.setFamily("Inter")
    font.setPointSize(9)
    font.setBold(False)
    font.setItalic(False)
    self.sortByComboBox.setFont(font)
    self.sortByComboBox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    self.sortByComboBox.setToolTipDuration(0)
    self.sortByComboBox.setStyleSheet("")
    self.sortByComboBox.setObjectName("sortByComboBox")

    self.sortByComboBox.addItem("Sort By")
    self.sortByComboBox.setCurrentIndex(0) 
    self.sortByComboBox.model().item(0).setEnabled(False)

    self.sortByComboBox.addItem("")
    self.sortByComboBox.addItem("")
    self.horizontalLayout.addWidget(self.sortByComboBox)

    self.sortingOrderComboBox = QtWidgets.QComboBox(parent=self.controlsFrame)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.sortingOrderComboBox.sizePolicy().hasHeightForWidth())
    self.sortingOrderComboBox.setSizePolicy(sizePolicy)
    self.sortingOrderComboBox.setMinimumSize(QtCore.QSize(105, 0))
    self.sortingOrderComboBox.setMaximumSize(QtCore.QSize(150, 16777215))
    self.sortingOrderComboBox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    self.sortingOrderComboBox.setPlaceholderText("")
    self.sortingOrderComboBox.setObjectName("sortingOrderComboBox")
    self.sortingOrderComboBox.addItem("")
    self.sortingOrderComboBox.addItem("")
    self.horizontalLayout.addWidget(self.sortingOrderComboBox)
    spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
    self.horizontalLayout.addItem(spacerItem3)
    self.horizontalLayout.setStretch(0, 1)
    self.horizontalLayout.setStretch(1, 1)
    self.horizontalLayout.setStretch(2, 2)
    self.horizontalLayout.setStretch(4, 5)
    self.verticalLayout_3.addWidget(self.controlsFrame)
    self.dataFrame = QtWidgets.QFrame(parent=self.mainDisplayFrame)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.dataFrame.sizePolicy().hasHeightForWidth())
    self.dataFrame.setSizePolicy(sizePolicy)
    self.dataFrame.setStyleSheet("")
    self.dataFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
    self.dataFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
    self.dataFrame.setObjectName("dataFrame")
    self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.dataFrame)
    self.verticalLayout_4.setContentsMargins(-1, 0, -1, 0)
    self.verticalLayout_4.setSpacing(0)
    self.verticalLayout_4.setObjectName("verticalLayout_4")
    self.line = QtWidgets.QFrame(parent=self.dataFrame)
    self.line.setMinimumSize(QtCore.QSize(0, 0))
    self.line.setMaximumSize(QtCore.QSize(16777215, 1))
    self.line.setStyleSheet("")
    self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
    self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
    self.line.setObjectName("line")
    self.verticalLayout_4.addWidget(self.line)
    self.frame = QtWidgets.QFrame(parent=self.dataFrame)
    self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
    self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
    self.frame.setObjectName("frame")
    self.verticalLayout_4.addWidget(self.frame)
    self.verticalLayout_3.addWidget(self.dataFrame)
    self.verticalLayout_3.setStretch(0, 1)
    self.verticalLayout_3.setStretch(1, 1)
    self.verticalLayout_3.setStretch(2, 8)
    self.horizontalLayout_7.addWidget(self.mainDisplayFrame)
    self.horizontalLayout_7.setStretch(0, 1)
    self.horizontalLayout_7.setStretch(1, 5)
    self.verticalLayout_2.addWidget(self.bodyFrame)
    self.verticalLayout_2.setStretch(0, 1)
    self.verticalLayout_2.setStretch(1, 10)

    main_layout = QtWidgets.QVBoxLayout(self)
    main_layout.addWidget(self.centralwidget)

    self.retranslateUi()
    QtCore.QMetaObject.connectSlotsByName(self)

  def retranslateUi(self):
    _translate = QtCore.QCoreApplication.translate
    self.studentsSidebarButton.setText(_translate("mainWindow", "Students"))
    self.programsSidebarButton.setText(_translate("mainWindow", "Programs"))
    self.collegesSidebarButton.setText(_translate("mainWindow", "Colleges"))
    self.searchBarLineEdit.setPlaceholderText(_translate("mainWindow", "Search College"))
    self.searchButton.setText(_translate("mainWindow", "Search"))
    self.searchByComboBox.setToolTip(_translate("mainWindow", "Search by"))
    self.searchByComboBox.setPlaceholderText(_translate("mainWindow", "Search by"))
    self.searchByComboBox.setItemText(1, _translate("mainWindow", "College Code"))
    self.searchByComboBox.setItemText(2, _translate("mainWindow", "College Name"))
    self.collegeLabel.setText(_translate("mainWindow", "Colleges"))
    self.addCollegeButton.setText(_translate("mainWindow", "Add College"))
    self.sortByComboBox.setToolTip(_translate("mainWindow", "Sort by"))
    self.sortByComboBox.setPlaceholderText(_translate("mainWindow", "Sort by"))
    self.sortByComboBox.setItemText(1, _translate("mainWindow", "College Code"))
    self.sortByComboBox.setItemText(2, _translate("mainWindow", "College Name"))
    self.sortingOrderComboBox.setItemText(0, _translate("mainWindow", "Ascending"))
    self.sortingOrderComboBox.setItemText(1, _translate("mainWindow", "Descending"))

  # Display messages to custom status bar
  def displayMessageToStatusBar(self, message, duration):
    self.statusMessageSignal.emit(message, duration)

  # Open Add Student Dialog
  def openAddCollegeDialog(self):
    self.addDialog = AddCollegeDialog(self)
    self.addDialog.collegeAddedTableSignal.connect(self.collegeTable.addNewCollegeToTable)
    self.addDialog.collegeAddedWindowSignal.connect(self.displayMessageToStatusBar)
    self.addDialog.exec()

  # Open Update Program Dialog
  def openUpdateCollegeDialog(self, collegeData):
    self.updateDialog = UpdateCollegeDialog(self, collegeData)
    self.updateDialog.collegeUpdatedTableSignal.connect(self.collegeTable.editCollegeInTable)
    self.updateDialog.updateTablesSignal.connect(self.updateTablesSignal)
    self.updateDialog.statusMessageSignal.connect(self.displayMessageToStatusBar)
    self.updateDialog.exec()

  # Search students
  def searchColleges(self):
    self.displayMessageToStatusBar("Searching...", 3000)
    
    searchValue = self.searchBarLineEdit.text().strip()
    searchField = self.searchByComboBox.currentText()

    if searchValue == "":
      colleges = searchCollegesByField(searchValue)
    else:
      if searchField == "Search By":
        colleges = searchCollegesByField(searchValue)
      else:
        colleges = searchCollegesByField(searchValue, searchField)

    if colleges:
      self.collegeTable.setColleges(colleges)
    else:
      self.statusMessageSignal.emit("No colleges found", 3000)
      self.collegeTable.clearScrollArea()

  # Handle key press events
  def keyPressEvent(self, event):
    if event.key() == Qt.Key.Key_Return:
      self.spacebarPressedSignal.emit()
