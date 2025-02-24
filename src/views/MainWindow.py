from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon
from PyQt6 import uic

from controllers.studentControllers import initializeAllCsv
from views.pages.StudentsPage import StudentsPage
from views.pages.ProgramsPage import ProgramsPage 
from views.pages.CollegesPage import CollegesPage

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    uic.loadUi("src/gui/ui/mainWindow.ui", self)

    self.setWindowIcon(QIcon("assets/LogoIcon.png"))
    self.setWindowTitle("Lexis")

    # Initialize CSV storage
    initializeAllCsv()

    # Create pages
    self.studentsPage = StudentsPage()
    self.programsPage = ProgramsPage()
    self.collegesPage = CollegesPage()

    # Add pages to stacked widget
    self.stackedWidget.addWidget(self.studentsPage)
    self.stackedWidget.addWidget(self.programsPage)
    self.stackedWidget.addWidget(self.collegesPage)

    self.stackedWidget.setCurrentWidget(self.studentsPage)

    # Connect buttons to switch views
    self.studentsPage.programsSidebarButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.programsPage))
    self.studentsPage.collegesSidebarButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.collegesPage))

    self.programsPage.studentsSidebarButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.studentsPage))
    self.programsPage.collegesSidebarButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.collegesPage))

    self.collegesPage.studentsSidebarButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.studentsPage))
    self.collegesPage.programsSidebarButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.programsPage))

    # self.programsPage.studentsSidebarButton.clicked.connect(self.studentsPage.studentTable.refreshDisplayStudents)
    # self.collegesPage.studentsSidebarButton.clicked.connect(self.studentsPage.studentTable.refreshDisplayStudents)
    # self.studentsPage.programsSidebarButton.clicked.connect(self.programsPage.programTable.refreshDisplayPrograms)
    # self.collegesPage.programsSidebarButton.clicked.connect(self.programsPage.programTable.refreshDisplayPrograms)
    # self.studentsPage.collegesSidebarButton.clicked.connect(self.collegesPage.collegeTable.refreshDisplayColleges)
    # self.programsPage.collegesSidebarButton.clicked.connect(self.collegesPage.collegeTable.refreshDisplayColleges)

    # Connect signals
    self.studentsPage.statusMessageSignal.connect(self.handleStatusMessage)
    self.programsPage.statusMessageSignal.connect(self.handleStatusMessage)
    self.collegesPage.statusMessageSignal.connect(self.handleStatusMessage)

    self.programsPage.updateTablesSignal.connect(self.studentsPage.searchStudents)
    self.collegesPage.updateTablesSignal.connect(self.studentsPage.searchStudents)
    self.collegesPage.updateTablesSignal.connect(self.programsPage.searchPrograms)
  
  def handleStatusMessage(self, message, duration):
    self.statusBar.showMessage(message, duration)

