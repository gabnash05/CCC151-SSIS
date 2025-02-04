from model.Student import Student
from model.Program import Program
from typing import List, Dict, Any
from utils.inputUtils import *

STUDENT_SEARCH_FIELDS = ["ID Number", "First Name", "Last Name", "Program Code", "College Code"]

# ADD STUDENT FORM: add a student record
def addStudent(idNumber: str, firstName: str, lastName: str, yearLevel: int, gender: str, programCode: str) -> str:
  if not all([idNumber, firstName, lastName, gender, programCode]):
    return("Enter all required fields")
  
  if not validateYearLevel(yearLevel):
    return("Year Level must be a positive integer.")
  
  if not validateIdNumber(idNumber):
    return("Invalid ID Number")
  
  if not validateGender(gender):
    return "Gender must be Male, Female, or Others."
  
  if Student.idNumberExists(idNumber):
    return "ID number already exists"

  if not Program.programCodeExists(programCode):
    return "Program Code does not exist"
  
  newStudent = Student(idNumber, firstName, lastName, yearLevel, gender, programCode)
  isSuccessful = Student.addStudentRecord(newStudent)

  return "Student added successfully." if isSuccessful else "Failed to add student."

### UPDATE ###
# add pagination
# MAIN WINDOW: List of students display 
def getAllStudents() -> List[Dict[str, str]]:
  return Student.getAllStudentRecords()

# SEARCH BAR: Search Student by a specific field ("ID Number", "First Name", "Last Name", "Program Code", "College Code")
def searchStudentsByField(field: str, value: str) -> List[Dict[str, str]]:
  if field not in STUDENT_SEARCH_FIELDS:
    print("Search field not valid")
    return []
  
  if not isinstance(value, str):
    print("Search value not valid")
    return []
  
  if field == STUDENT_SEARCH_FIELDS[0]:
    if validateIdNumber(value):
      return [Student.getStudentRecord(value)]
  
  if field == STUDENT_SEARCH_FIELDS[1]:
    return Student.getAllStudentRecordsByFirstName(value)
    
  if field == STUDENT_SEARCH_FIELDS[2]:
    return Student.getAllStudentRecordsByLastName(value)
  
  if field == STUDENT_SEARCH_FIELDS[3]:
    return Student.getAllStudentRecordsByProgram(value)
  
  if field == STUDENT_SEARCH_FIELDS[4]:
    return Student.getAllStudentRecordsByCollege(value)

# may be depricated
# FILTER SEARCH: get list of all students by year level
def getStudentsByYearLevel(yearLevel: int) -> List[Dict[str, str]]:
  if not validateYearLevel(yearLevel):
    return None
  
  return Student.getAllStudentRecordsByYearLevel(yearLevel)

# may be depricated
# FILTER SEARCH: get list of all students by gender
def getStudentsByGender(gender: str) -> List[Dict[str, str]]:
  if not validateGender(gender):
    return None
  
  return Student.getAllStudentRecordsByGender(gender)

# UPDATE STUDENT FORM: updates a student record
def updateStudent(originalId, newIdNumber: str, newFirstName: str, newLastName: str, newYearLevel: int, newGender: str, newProgramCode: str) -> str:
  if not validateIdNumber(originalId):
    return("Invalid ID Number")
  
  if not validateYearLevel(newYearLevel):
    return("Year Level must be a positive integer.")
  
  if not validateGender(newGender):
    return "Gender must be Male, Female, or Others."
  
  updateData = {key: value for key, value in {
    "ID Number": newIdNumber,
    "First Name": newFirstName,
    "Last Name": newLastName,
    "Year Level": newYearLevel,
    "Gender": newGender,
    "Program Code": newProgramCode
  }.items() if value is not None}

  isSuccessful = Student.updateStudentRecordById(originalId, updateData)

  return "Student updated successfully." if isSuccessful else "Failed to update student."

# REMOVE STUDENT FORM: removes a student record
def removeStudent(idNumber: str) -> str:
  if not validateIdNumber(idNumber):
    return("Invalid ID Number")
  
  isSuccessful = Student.removeStudentRecordById(idNumber)

  return "Student removed successfully." if isSuccessful else "Failed to remove student."