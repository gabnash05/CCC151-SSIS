from typing import List, Dict, Any
import utils.csvUtils as csvUtils
from pathlib import Path


class Program:
  PROGRAM_CSV_FILEPATH = Path(__file__).parent.parent.parent / "data" / "programs.csv"

  PROGRAM_HEADERS = ["Program Code", "Program Name", "College Code"]

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
    return csvUtils.initializeCsv(Program.PROGRAM_CSV_FILEPATH, Program.PROGRAM_HEADERS)
  
  # Checks if Program Code already exists
  @staticmethod
  def programCodeExists(programCode: str) -> bool:
    return csvUtils.checkIdIfExistsCsv(Program.PROGRAM_CSV_FILEPATH, programCode)

  # Add new program
  @staticmethod
  def addNewProgram(program: Any) -> bool:
    return csvUtils.appendRowCsv(Program.PROGRAM_CSV_FILEPATH, program.toDict())
  
  # Get all program records
  def getAllProgramRecords() -> List[Dict[str, str]]:
    return csvUtils.readCsv(Program.PROGRAM_CSV_FILEPATH)
  
  # Get program record by code
  @staticmethod
  def getProgramRecordByCode(programCode: str) -> Dict[str, str]:
    return csvUtils.getRowByIdCsv(Program.PROGRAM_CSV_FILEPATH, programCode)
  
  # Get program record by name
  @staticmethod
  def getProgramRecordsByName(programName: str) -> Dict[str, str]:
    return csvUtils.getRowsByFieldCsv(Program.PROGRAM_CSV_FILEPATH, programName, Program.PROGRAM_HEADERS[1])
  
  # Get program record by college
  @staticmethod
  def getProgramRecordsByCollege(collegeCode: str) -> List[Dict[str, str]]:
    return csvUtils.getRowsByFieldCsv(Program.PROGRAM_CSV_FILEPATH, collegeCode, Program.PROGRAM_HEADERS[2])
  
  # Get program record
  @staticmethod
  def updateProgramRecordByCode(programCode: str, updateData: Dict[str, str]) -> bool:
    return csvUtils.updateRowByFieldCsv(Program.PROGRAM_CSV_FILEPATH, Program.PROGRAM_HEADERS[0], programCode, updateData)
  
  # Remove program from college
  @staticmethod
  def deleteProgramRecord(programCode: str) -> bool:
    return csvUtils.deleteRowByFieldCsv(Program.PROGRAM_CSV_FILEPATH, Program.PROGRAM_HEADERS[0], programCode)
  
  # Searches for program records without a search field
  @staticmethod
  def searchForProgram(searchValue: str) -> List[Dict[str, str]]:
    return csvUtils.getRowsByFieldCsv(Program.PROGRAM_CSV_FILEPATH, searchValue, None)