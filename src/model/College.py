from typing import List, Dict, Any
import utils.csvUtils as csvUtils
from pathlib import Path

COLLEGE_CSV_FILEPATH = Path(__file__).parent.parent.parent / "data" / "colleges.csv"
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
  def getCollegeRecord(collegeCode: str) -> Dict[str, str]:
    return csvUtils.getRowByIdCsv(COLLEGE_CSV_FILEPATH, collegeCode)
  
  # Get all college records
  @staticmethod
  def getAllCollegeRecords() -> List[Dict[str, str]]:
    return csvUtils.readCsv(COLLEGE_CSV_FILEPATH)

  ### UPDATE ###
  # Get program record
  @staticmethod
  def updateCollegeRecord(collegeCode: str, updateData: Dict[str, str]) -> bool:
    # update all programs under college
    return csvUtils.updateRowByFieldCsv(COLLEGE_CSV_FILEPATH, COLLEGE_HEADERS[0], collegeCode, updateData)
  
  ### UPDATE ###
  # Remove college
  @staticmethod
  def deleteCollegeRecord(collegeCode: str) -> bool:
    # update all students and programs under college
    return csvUtils.deleteRowByFieldCsv(COLLEGE_CSV_FILEPATH, COLLEGE_HEADERS[0], collegeCode)