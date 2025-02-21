from model.Student import Student
from model.Program import Program
from model.College import College
from typing import List, Dict, Any
from utils.inputUtils import *

PROGRAM_SEARCH_FIELDS = ["Program Code", "Program Name", "College Code"]

# INITIALIZING
def initializeAllCsv():
  Student.intializeStudentStorage()
  Program.intializeProgramStorage()
  College.intializeProgramStorage()


# ADD PROGRAM FORM: adds a new program to a college
def addProgram(programCode: str, programName: str, collegeCode: str) -> bool:
  if not all([programCode, programName, collegeCode]):
    return("Enter all required fields")
  
  if not College.collegeCodeExists(collegeCode):
    return "College Code does not exist"
  
  if Program.programCodeExists(programCode):
    return "Program already exists"
  
  newProgram = Program(programCode, programName, collegeCode)
  isSuccessful = Program.addNewProgram(newProgram)

  return "Program added successfully." if isSuccessful else "Failed to add program."

def getAllPrograms() -> List[Dict[str, str]]:
  return Program.getAllProgramRecords()

# SEARCH BAR: searches for a program based on a specific field
def searchProgramsByField(value: str, field: str = None) -> List[Dict[str, str]]:
  if field and field not in PROGRAM_SEARCH_FIELDS:
    print("Search field not valid")
    return []
  
  if not isinstance(value, str):
    print("Search value not valid")
    return []
  
  if field == None:
    return Program.searchForProgram(value)
  
  if field == PROGRAM_SEARCH_FIELDS[0]:
    return [Program.getProgramRecordByCode(value)]
  
  if field == PROGRAM_SEARCH_FIELDS[1]:
    return Program.getProgramRecordsByName(value)
    
  if field == PROGRAM_SEARCH_FIELDS[2]:
    return Program.getProgramRecordsByCollege(value)

# UPDATE PROGRAM FORM: updates a program and the students under the program
def updateProgram(originalProgramCode: str, newProgramCode: Any, newProgramName: Any, newCollegeCode: Any) -> bool:
  
  if not College.collegeCodeExists(newCollegeCode):
    return "College Code does not exist"

  updateData = {
    "Program Code": newProgramCode,
    "Program Name": newProgramName,
    "College Code": newCollegeCode,
  }

  isSuccessful = Program.updateProgramRecordByCode(originalProgramCode, updateData)

  if isSuccessful and (newProgramCode or newCollegeCode):
    updateData = {
      "Program Code": newProgramCode,
      "College Code": newCollegeCode
    }

    studentsToUpdate = Student.getAllStudentRecordsByProgram(originalProgramCode)
    for student in studentsToUpdate:
      Student.updateStudentRecordById(student["ID Number"], updateData)

    return "Program updated successfully."
  
  else: 
    return "Failed to update program."

# REMOVE PROGRAM BUTTON: removes a program from its college and updates all the students under the program
def removeProgram(programCode: str) -> str:
  if not programCode:
    return "Program Code is required."

  isSuccessful = Program.deleteProgramRecord(programCode)

  if isSuccessful:
    updateData = {
      "Program Code": "N/A",
    }

    studentsToUpdate = Student.getAllStudentRecordsByProgram(programCode)
    for student in studentsToUpdate:
      Student.updateStudentRecordById(student["ID Number"], updateData)

  return "Program removed successfully." if isSuccessful else "Failed to remove program." 