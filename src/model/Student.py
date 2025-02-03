from typing import List, Dict, Any
import utils.csvUtils as csvUtils
from pathlib import Path

class Student:  
  STUDENT_CSV_FILEPATH = Path(__file__).parent.parent.parent / "data" / "students.csv"
  STUDENT_HEADERS = ["ID Number", "First Name", "Last Name", "Year Level", "Gender", "Program Code"]

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
    return csvUtils.initializeCsv(Student.STUDENT_CSV_FILEPATH, Student.STUDENT_HEADERS)
  
  # Adds a new student record
  @staticmethod
  def addStudentRecord(student: Any) -> bool:
    return csvUtils.appendRowCsv(Student.STUDENT_CSV_FILEPATH, student.toDict())
  
  # Gets a student record
  @staticmethod
  def getStudentRecord(studentId: str) -> Dict[str, str]:
    return csvUtils.getRowByIdCsv(Student.STUDENT_CSV_FILEPATH, studentId)
  
  ### UPDATE ###
  # Add pagination
  # Get all student records
  @staticmethod
  def getAllStudentRecords() -> List[Dict[str, str]]:
    return csvUtils.readCsv(Student.STUDENT_CSV_FILEPATH)
  
  # Get all student records by first name
  @staticmethod
  def getAllStudentRecordsByFirstName(firstName: str) -> List[Dict[str, str]]:
    return csvUtils.getRowsByFieldCsv(Student.STUDENT_CSV_FILEPATH, Student.STUDENT_HEADERS[1], firstName)
  
  # Get all student records by last name
  @staticmethod
  def getAllStudentRecordsByLastName(lastName: str) -> List[Dict[str, str]]:
    return csvUtils.getRowsByFieldCsv(Student.STUDENT_CSV_FILEPATH, Student.STUDENT_HEADERS[2], lastName)
  
  # Get all student records by year level
  @staticmethod
  def getAllStudentRecordsByYearLevel(yearLevel: int) -> List[Dict[str, str]]:
    return csvUtils.getRowsByFieldCsv(Student.STUDENT_CSV_FILEPATH, Student.STUDENT_HEADERS[3], str(yearLevel))

  # Get all student records by gender
  @staticmethod
  def getAllStudentRecordsByGender(gender: str) -> List[Dict[str, str]]:
    return csvUtils.getRowsByFieldCsv(Student.STUDENT_CSV_FILEPATH, Student.STUDENT_HEADERS[4], gender)

  # Get all student records by program code
  @staticmethod
  def getAllStudentRecordsByProgram(program: str) -> List[Dict[str, str]]:
    return csvUtils.getRowsByFieldCsv(Student.STUDENT_CSV_FILEPATH, Student.STUDENT_HEADERS[5], program)

  # Get all student records by college
  @staticmethod
  def getAllStudentRecordsByCollege(college: str) -> List[Dict[str, str]]:
    pass

  # Updates student information
  @staticmethod
  def updateStudentRecordById(studentId: str, updateData: Dict[str, str]) -> bool:
    return csvUtils.updateRowByFieldCsv(Student.STUDENT_CSV_FILEPATH, Student.STUDENT_HEADERS[0], studentId, updateData)
  
  # Removes a student record
  @staticmethod
  def removeStudentRecordById(studentId: str) -> bool:
    return csvUtils.deleteRowByFieldCsv(Student.STUDENT_CSV_FILEPATH, Student.STUDENT_HEADERS[0], studentId)