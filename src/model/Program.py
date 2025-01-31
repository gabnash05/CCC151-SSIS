from typing import List, Dict, Any
import utils.csvUtils as csvUtils
from pathlib import Path

PROGRAM_CSV_FILEPATH = Path(__file__).parent.parent.parent / "data" / "programs.csv"
PROGRAM_HEADERS = ["Program Code", "Program Name", "College Code"]

class Program:
  def __init__(self, programCode: str, name: str, collegeCode: str):
    self.programCode = programCode
    self.name = name
    self.collegeCode = collegeCode
  
  def toDict(self) -> Dict:
    return {
      "Program Code": self.programCode, 
      "Program Name": self.name,
      "College Code": self.collegeCode,
    }
  
  # Only for initializing when the application starts
  @staticmethod
  def intializeProgramStorage() -> bool:
    return csvUtils.initializeCsv(PROGRAM_CSV_FILEPATH, PROGRAM_HEADERS)
  
  # Add new program
  @staticmethod
  def addNewProgram(program: Any) -> bool:
    return csvUtils.appendRowCsv(PROGRAM_CSV_FILEPATH, program.toDict())
  
  # Get program record
  @staticmethod
  def getProgramRecord(programCode: str) -> Dict[str, str]:
    return csvUtils.getRowByIdCsv(PROGRAM_CSV_FILEPATH, programCode)
  
  # Get program record
  @staticmethod
  def getProgramRecordsByCollege(collegeCode: str) -> List[Dict[str, str]]:
    return csvUtils.getRowsByFieldCsv(PROGRAM_CSV_FILEPATH, PROGRAM_HEADERS[2], collegeCode)
  
  ### UPDATE ###
  # Get program record
  @staticmethod
  def updateProgramRecord(programCode: str, updateData: Dict[str, str]) -> bool:
    # update all students under program
    return csvUtils.updateRowByFieldCsv(PROGRAM_CSV_FILEPATH, PROGRAM_HEADERS[0], programCode, updateData)
  
  ### UPDATE ###
  # Remove program from college
  @staticmethod
  def deleteProgramRecord(programCode: str) -> bool:
    # update all students under program
    return csvUtils.deleteRowByFieldCsv(PROGRAM_CSV_FILEPATH, PROGRAM_HEADERS[0], programCode)