from model.Student import Student
from model.Program import Program
from model.College import College
from typing import List, Dict, Any
from utils.inputUtils import *

COLLEGE_SEARCH_FIELDS = ["College Code", "College Name"]

# INITIALIZING
def initializeAllCsv():
  Student.intializeStudentStorage()
  Program.intializeProgramStorage()
  College.intializeProgramStorage()

# ADD COLLEGE FORM: adds a new college
def addCollege(collegeCode: str, collegeName: str) -> bool:
  if not all([collegeCode, collegeName]):
    return "Enter all required fields"
  
  if College.collegeCodeExists(collegeCode):
    return "College already exists"
  
  newCollege = College(collegeCode, collegeName)
  isSuccessful = College.addNewCollege(newCollege)

  return "College added successfully." if isSuccessful else "Failed to add college."

# SEARCH BAR: searches for a college based on a specific field
def searchCollegesByField(field: str, value: str) -> List[Dict[str, str]]:
  if field not in COLLEGE_SEARCH_FIELDS:
    print("Search field not valid")
    return []
  
  if not isinstance(value, str):
    print("Search value not valid")
    return []
  
  if field == COLLEGE_SEARCH_FIELDS[0]:
    return [College.getCollegeRecordByCode(value)]
  
  if field == COLLEGE_SEARCH_FIELDS[1]:
    return Program.College.getCollegeRecordByCode(value)

# UPDATE PROGRAM FORM: updates a program and the students under the program
def updateCollege(originalCollegeCode: str, newCollegeCode: Any, newCollegeName: Any) -> bool:

  if not College.collegeCodeExists(originalCollegeCode):
    return "College Code does not exist"

  updateData = {key: value for key, value in {
    "College Code": newCollegeCode, 
    "College Name": newCollegeName,
  }.items() if value is not None}

  isSuccessful = College.updateCollegeRecord(originalCollegeCode, updateData)

  if isSuccessful and newCollegeCode:
    updateData = {
      "College Code": newCollegeCode
    }

    # Update programs under college
    programsToUpdate = Program.getProgramRecordsByCollege(originalCollegeCode)
    for program in programsToUpdate:
      Program.updateProgramRecordByCode(program["Program Code"], updateData)
    
    # Update students under college
    studentsToUpdate = Student.getAllStudentRecordsByCollege(originalCollegeCode)
    for student in studentsToUpdate:
      Student.updateStudentRecordById(student["ID Number"], updateData)

    return "College updated successfully."
  
  else: 
    return "Failed to update college."
  
# REMOVE PROGRAM BUTTON: removes a program from its college and updates all the students under the program
def removeCollege(collegeCode: str) -> str:
  if not collegeCode:
    return "College Code is required."

  isSuccessful = College.deleteCollegeRecord(collegeCode)

  if isSuccessful:
    updateData = {
      "College Code": "N/A",
    }

    # Updates all programs under College
    programsToUpdate = Program.getProgramRecordsByCollege(collegeCode)
    for program in programsToUpdate:
      Program.updateProgramRecordByCode(program["Program Code"], updateData)
    
    # Update students under college
    studentsToUpdate = Student.getAllStudentRecordsByCollege(collegeCode)
    for student in studentsToUpdate:
      Student.updateStudentRecordById(student["ID Number"], updateData)

  return "College removed successfully." if isSuccessful else "Failed to remove college." 