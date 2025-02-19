from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6 import uic

from views.StudentsPage import StudentsPage
from views.ProgramsPage import ProgramsPage 
from views.CollegesPage import CollegesPage

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    uic.loadUi("src/gui/ui/mainWindow.ui", self)

    self.setWindowIcon(QIcon("assets/LogoIcon.png"))
    self.setWindowTitle("Lexis")

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

    # Connect signals
    self.studentsPage.statusMessageSignal.connect(self.handleStatusMessage)
    self.programsPage.statusMessageSignal.connect(self.handleStatusMessage)
    self.collegesPage.statusMessageSignal.connect(self.handleStatusMessage)
  
  def handleStatusMessage(self, message, duration):
    self.statusBar.showMessage(message, duration)
