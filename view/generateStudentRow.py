from PyQt6 import QtWidgets, QtCore

def create_student_row(parent, student_data):
    row_frame = QtWidgets.QFrame(parent)
    row_frame.setMinimumSize(QtCore.QSize(400, 30))
    row_frame.setMaximumSize(QtCore.QSize(16777215, 40))
    row_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
    row_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
    
    # Adds a stylesheet
    row_frame.setStyleSheet("QMainWindow {\n"
        "    background-color: rgb(22, 22, 22);\n"
        "    font: 9pt \"Inter\";\n"
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
        "/* FRAMES */\n"
        "QFrame {\n"
        "  border: none;\n"
        "}\n"
        "\n"
        "/* LABELS */\n"
        "\n"
        "#tableHeaderFrame QLabel {\n"
        "    color: rgb(120, 139, 140);\n"
        "}\n"
        "\n"
        "#dataFrame Line {\n"
        "    background-color: rgb(120, 139, 140);\n"
        "}")
    
    layout = QtWidgets.QHBoxLayout(row_frame)
    layout.setContentsMargins(0, 0, 0, 0)

    # Create labels for student info
    for index, value in enumerate(student_data):
        label = QtWidgets.QLabel(row_frame)
        label.setText(str(value))
        
        # Set alignment: Left for ID and Name, Center for others
        if index == 0:  # First (ID) and Second (Name) column
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
            label.setMinimumWidth(60)
        elif index == 1:
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
            label.setMinimumWidth(150)
        elif index == 6:
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label.setMinimumWidth(100)
        else:
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label.setMinimumWidth(60)

        layout.addWidget(label)
    
    # Operations frame
    operations_frame = QtWidgets.QFrame(row_frame)
    operations_layout = QtWidgets.QHBoxLayout(operations_frame)
    operations_layout.setContentsMargins(0, 0, 0, 0)
    
    edit_button = QtWidgets.QPushButton("/", operations_frame)
    delete_button = QtWidgets.QPushButton("x", operations_frame)
    edit_button.setMaximumSize(QtCore.QSize(50, 16777215))
    edit_button.setMinimumSize(QtCore.QSize(40, 30))
    delete_button.setMaximumSize(QtCore.QSize(50, 16777215))
    delete_button.setMinimumSize(QtCore.QSize(40, 30))
    
    operations_layout.addWidget(edit_button)
    operations_layout.addWidget(delete_button)
    layout.addWidget(operations_frame)
    
    # Separator line
    separator = QtWidgets.QFrame(parent)
    separator.setMaximumSize(QtCore.QSize(16777215, 1))
    separator.setStyleSheet("background-color: rgb(120, 139, 140);")
    separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
    separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
    
    return row_frame, separator

class StudentTableApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Table")
        self.setGeometry(100, 100, 600, 400)
        
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QtWidgets.QVBoxLayout(central_widget)
        
        # Scroll Area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        self.scroll_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize)
        
        scroll_area.setWidget(scroll_content)
        
        # Sample student data
        students = [
            ("2023-0001", "Kim Gabriel A. Nasayao", "Male", "2", "BSCS", "CCS"),
            ("2023-0002", "Jane Doe", "Female", "3", "BSIT", "CCS"),
            ("2023-0003", "John Smith", "Male", "1", "BSECE", "COE"),
            ("2023-0001", "Kim Gabriel A. Nasayao", "Male", "2", "BSCS", "CCS"),
            ("2023-0002", "Jane Doe", "Female", "3", "BSIT", "CCS"),
            ("2023-0003", "John Smith", "Male", "1", "BSECE", "COE"),
            ("2023-0001", "Kim Gabriel A. Nasayao", "Male", "2", "BSCS", "CCS"),
            ("2023-0002", "Jane Doe", "Female", "3", "BSIT", "CCS"),
            ("2023-0003", "John Smith", "Male", "1", "BSECE", "COE"),
            ("2023-0001", "Kim Gabriel A. Nasayao", "Male", "2", "BSCS", "CCS"),
            ("2023-0002", "Jane Doe", "Female", "3", "BSIT", "CCS"),
            ("2023-0003", "John Smith", "Male", "1", "BSECE", "COE"),
            ("2023-0001", "Kim Gabriel A. Nasayao", "Male", "2", "BSCS", "CCS"),
            ("2023-0002", "Jane Doe", "Female", "3", "BSIT", "CCS"),
            ("2023-0003", "John Smith", "Male", "1", "BSECE", "COE"),
            ("2023-0001", "Kim Gabriel A. Nasayao", "Male", "2", "BSCS", "CCS"),
            ("2023-0002", "Jane Doe", "Female", "3", "BSIT", "CCS"),
            ("2023-0003", "John Smith", "Male", "1", "BSECE", "COE"),
            ("2023-0001", "Kim Gabriel A. Nasayao", "Male", "2", "BSCS", "CCS"),
            ("2023-0002", "Jane Doe", "Female", "3", "BSIT", "CCS"),
            ("2023-0003", "John Smith", "Male", "1", "BSECE", "COE"),
            ("2023-0001", "Kim Gabriel A. Nasayao", "Male", "2", "BSCS", "CCS"),
            ("2023-0002", "Jane Doe", "Female", "3", "BSIT", "CCS"),
            ("2023-0003", "John Smith", "Male", "1", "BSECE", "COE"),
            ("2023-0001", "Kim Gabriel A. Nasayao", "Male", "2", "BSCS", "CCS"),
            ("2023-0002", "Jane Doe", "Female", "3", "BSIT", "CCS"),
            ("2023-0003", "John Smith", "Male", "1", "BSECE", "COE"),
            ("2023-0001", "Kim Gabriel A. Nasayao", "Male", "2", "BSCS", "CCS"),
            ("2023-0002", "Jane Doe", "Female", "3", "BSIT", "CCS"),
            ("2023-0003", "John Smith", "Male", "1", "BSECE", "COE"),
            ("2023-0001", "Kim Gabriel A. Nasayao", "Male", "2", "BSCS", "CCS"),
            ("2023-0002", "Jane Doe", "Female", "3", "BSIT", "CCS"),
            ("2023-0003", "John Smith", "Male", "1", "BSECE", "COE"),
        ]
        
        for student in students:
            row, separator = create_student_row(scroll_content, student)
            self.scroll_layout.addWidget(row)
            self.scroll_layout.addWidget(separator)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = StudentTableApp()
    window.show()
    sys.exit(app.exec())
