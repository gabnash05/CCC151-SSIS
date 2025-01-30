import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from model.Student import Student

# Initialize the CSV file with the correct headers
Student.intializeStudentStorage()

# Create new students
student1 = Student("2023-0001", "Kim ", "Nasayao", 2, "Male", "BSCS")
student2 = Student("2023-0002", "Franxine", "Gamboa", 3, "Female", "BSN")

# Add student records
print("Adding student records...")
Student.addStudentRecord(student1)
Student.addStudentRecord(student2)

print("Getting all 2nd year records...")
all_records = Student.getAllStudentRecordsByProgram("BSN")
print(all_records)