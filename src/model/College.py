from typing import List, Dict, Any
import utils.csvUtils as csvUtils

COLLEGE_CSV_FILEPATH = "../../data/colleges.csv"
COLLEGE_HEADERS = ["College Code", "College Name"]

class College:
  def __init__(self, collegeCode, name):
    self.collegeCode = collegeCode
    self.name = name
  
  def toDict(self) -> Dict:
    return {
      "College Code": self.collegeCode,
      "College Name": self.name,
    }
  
  # Only for initializing when the application starts
  @staticmethod
  def intializeProgramStorage() -> bool:
    return csvUtils.initializeCsv(COLLEGE_CSV_FILEPATH, COLLEGE_HEADERS)
  
  # Add new college
  @staticmethod
  def addNewCollege(college: Any) -> bool:
    return csvUtils.appendRowCsv(COLLEGE_CSV_FILEPATH, college.toDict())
  
  # Get college record
  @staticmethod
  def getCollegeRecord(collegeCode: str) -> Dict:
    return csvUtils.getRowByIdCsv(COLLEGE_CSV_FILEPATH, collegeCode)

  ### UPDATE ###
  # Get program record
  @staticmethod
  def updateCollegeRecord(collegeCode: str, updateData: Dict) -> bool:
    # update all programs under college
    return csvUtils.updateRowByFieldCsv(COLLEGE_CSV_FILEPATH, COLLEGE_HEADERS[0], collegeCode, updateData)
  
  ### UPDATE ###
  # Remove college
  @staticmethod
  def deleteCollegeRecord(collegeCode: str) -> bool:
    # update all students and programs under college
    return csvUtils.deleteRowByFieldCsv(COLLEGE_CSV_FILEPATH, COLLEGE_HEADERS[0], collegeCode)