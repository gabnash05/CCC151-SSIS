from model.Student import Student
from model.Program import Program
from model.College import College
from typing import List, Dict, Any
from utils.inputUtils import *

STUDENT_SEARCH_FIELDS = ["ID Number", "First Name", "Last Name", "Program Code", "College Code"]

# INITIALIZING
def initializeAllCsv():
  Student.intializeStudentStorage()
  Program.intializeProgramStorage()
  College.intializeProgramStorage()

# ADD STUDENT FORM: add a student record
def addStudent(idNumber: str, firstName: str, lastName: str, yearLevel: str, gender: str, programCode: str, collegeCode: str) -> str:
  if not all([idNumber, firstName, lastName, gender, programCode]):
    return("Enter all required fields")
  
  # converts year level into an int
  if isinstance(yearLevel, str) and yearLevel.isdigit():
    yearLevel = int(yearLevel)
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
  
  if not College.collegeCodeExists(collegeCode):
    return "College Code does not exist"
  
  newStudent = Student(idNumber, firstName, lastName, yearLevel, gender, programCode, collegeCode)
  isSuccessful = Student.addStudentRecord(newStudent)

  return "Student added successfully." if isSuccessful else "Failed to add student."

### UPDATE ###
# add pagination
# MAIN WINDOW: List of students display 
def getAllStudents() -> List[Dict[str, str]]:
  return Student.getAllStudentRecords()

# SEARCH BAR: Search Student by a specific field ("ID Number", "First Name", "Last Name", "Program Code", "College Code")
def searchStudentsByField(value: str, field: str = None ) -> List[Dict[str, str]]:
  if field and field not in STUDENT_SEARCH_FIELDS:
    print("Search field not valid")
    return []
  
  if not isinstance(value, str):
    print("Search value not valid")
    return []
  
  # No search field
  if field == None:
    return Student.searchForStudent(value)
  
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

#FIXME: handle when updating college code for students
# UPDATE STUDENT FORM: updates a student record
def updateStudent(originalId, newIdNumber: str, newFirstName: str, newLastName: str, newYearLevel: int, newGender: str, newProgramCode: str, newCollegeCode: str) -> str:
  if not validateIdNumber(originalId):
    return("Invalid ID Number")
  
  # converts year level into an int
  if isinstance(newYearLevel, str) and newYearLevel.isdigit():
    newYearLevel = int(newYearLevel)
  if newYearLevel and not validateYearLevel(newYearLevel):
    return("Year Level must be a positive integer.")
  
  if newGender and not validateGender(newGender):
    return "Gender must be Male, Female, or Others."
  
  if newProgramCode and not Program.programCodeExists(newProgramCode):
    return "Program Code does not exist"
  
  if newCollegeCode and not College.collegeCodeExists(newCollegeCode):
    return "College Code does not exist"
  
  updateData = {
    key: value
    for key, value in {
      "ID Number": newIdNumber,
      "First Name": newFirstName,
      "Last Name": newLastName,
      "Year Level": newYearLevel,
      "Gender": newGender,
      "Program Code": newProgramCode,
    }.items()
    if value is not None
  }

  isSuccessful = Student.updateStudentRecordById(originalId, updateData)

  return "Student updated successfully." if isSuccessful else "Failed to update student."

# REMOVE STUDENT FORM: removes a student record
def removeStudent(idNumber: str) -> str:
  if not validateIdNumber(idNumber):
    return("Invalid ID Number")
  
  isSuccessful = Student.removeStudentRecordById(idNumber)

  return "Student removed successfully." if isSuccessful else "Failed to remove student."