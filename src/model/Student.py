from typing import List, Dict, Any
import utils.csvUtils as csvUtils
import os

relativePath = "data/students.csv"
STUDENT_CSV_FILEPATH = os.path.abspath(relativePath)
STUDENT_HEADERS = ["ID Number", "First Name", "Last Name", "Year Level", "Gender", "Program Code"]

class Student:
  def __init__(self, idNumber: str, firstName: str, lastName: str, yearLevel: int, gender: str, programCode: str):
    self.idNumber = idNumber
    self.firstName = firstName
    self.lastName = lastName
    self.yearLevel = str(yearLevel)
    self.gender = gender
    self.programCode = programCode

  def toDict(self) -> None:
    return {
      "ID Number": self.idNumber,
      "First Name": self.firstName,
      "Last Name": self.lastName,
      "Year Level": self.yearLevel,
      "Gender": self.gender,
      "Program Code": self.programCode
    }
  
  # Only for initializing when the application starts
  @staticmethod
  def intializeStudentStorage() -> bool:
    csvUtils.initializeCsv(STUDENT_CSV_FILEPATH, STUDENT_HEADERS)
  
  # Adds a new student record
  @staticmethod
  def addStudentRecord(student: Any) -> bool:
    csvUtils.appendRowCsv(STUDENT_CSV_FILEPATH, student.toDict())
  
  # Gets a student record
  @staticmethod
  def getStudentRecord(studentId: str) -> Dict:
    return csvUtils.getRowByIdCsv(STUDENT_CSV_FILEPATH, studentId)
  
  # Get all student records
  @staticmethod
  def getAllStudentRecords() -> List[Dict]:
    return csvUtils.readCsv(STUDENT_CSV_FILEPATH)
  
  # Get all student records by first name
  @staticmethod
  def getAllStudentRecordsByYearLevel(firstName: str) -> List[Dict]:
    return csvUtils.getRowsByFieldCsv(STUDENT_CSV_FILEPATH, STUDENT_HEADERS[1], firstName)
  
  # Get all student records by last name
  @staticmethod
  def getAllStudentRecordsByYearLevel(lastName: str) -> List[Dict]:
    return csvUtils.getRowsByFieldCsv(STUDENT_CSV_FILEPATH, STUDENT_HEADERS[2], lastName)
  
  # Get all student records by year level
  @staticmethod
  def getAllStudentRecordsByYearLevel(yearLevel: int) -> List[Dict]:
    return csvUtils.getRowsByFieldCsv(STUDENT_CSV_FILEPATH, STUDENT_HEADERS[3], str(yearLevel))

  # Get all student records by gender
  @staticmethod
  def getAllStudentRecordsByGender(gender: str) -> List[Dict]:
    return csvUtils.getRowsByFieldCsv(STUDENT_CSV_FILEPATH, STUDENT_HEADERS[4], gender)

  # Get all student records by program code
  @staticmethod
  def getAllStudentRecordsByProgram(program: str) -> List[Dict]:
    return csvUtils.getRowsByFieldCsv(STUDENT_CSV_FILEPATH, STUDENT_HEADERS[5], program)

  # Get all student records by college

  # Updates student information
  @staticmethod
  def updateStudentRecordById(studentId: str, updateData: Dict) -> bool:
    return csvUtils.updateRowByFieldCsv(STUDENT_CSV_FILEPATH, STUDENT_HEADERS[0], studentId, updateData)
  
  # Removes a student record
  @staticmethod
  def removeStudentRecordById(studentId: str) -> bool:
    return csvUtils.deleteRowByFieldCsv(STUDENT_CSV_FILEPATH, STUDENT_HEADERS[0], studentId)