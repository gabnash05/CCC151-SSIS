import pytest
from unittest.mock import patch
from model.Program import Program

def test_initializeProgramStorage(mocker):
  mock_initializeCsv = mocker.patch("utils.csvUtils.initializeCsv", return_value=True)
  
  result = Program.intializeProgramStorage()
  
  mock_initializeCsv.assert_called_once_with(Program.PROGRAM_CSV_FILEPATH, Program.PROGRAM_HEADERS)
  assert result is True

def test_addNewProgram(mocker):
  mock_appendRowCsv = mocker.patch("utils.csvUtils.appendRowCsv", return_value=True)
  program = Program("BSCS", "Bachelor of Science in Computer Science", "CCS")
  
  result = Program.addNewProgram(program)
  
  mock_appendRowCsv.assert_called_once_with(Program.PROGRAM_CSV_FILEPATH, program.toDict())
  assert result is True

def test_getProgramRecord(mocker):
  mock_getRowByIdCsv = mocker.patch("utils.csvUtils.getRowByIdCsv", return_value={"Program Code": "BSCS", "Program Name": "Bachelor of Science in Computer Science", "College Code": "CCS"})
  
  result = Program.getProgramRecord("BSCS")
  
  mock_getRowByIdCsv.assert_called_once_with(Program.PROGRAM_CSV_FILEPATH, "BSCS")
  assert result["Program Code"] == "BSCS"
  assert result["Program Name"] == "Bachelor of Science in Computer Science"
  assert result["College Code"] == "CCS"

def test_getProgramRecordsByCollege(mocker):
  mock_getRowsByFieldCsv = mocker.patch("utils.csvUtils.getRowsByFieldCsv", return_value=[{"Program Code": "BSCS", "Program Name": "Bachelor of Science in Computer Science", "College Code": "CCS"}])
  
  result = Program.getProgramRecordsByCollege("CCS")
  
  mock_getRowsByFieldCsv.assert_called_once_with(Program.PROGRAM_CSV_FILEPATH, Program.PROGRAM_HEADERS[2], "CCS")
  assert len(result) == 1
  assert result[0]["College Code"] == "CCS"

def test_updateProgramRecord(mocker):
  mock_updateRowByFieldCsv = mocker.patch("utils.csvUtils.updateRowByFieldCsv", return_value=True)
  
  result = Program.updateProgramRecord("BSCS", {"Program Name": "Software Engineering"})
  
  mock_updateRowByFieldCsv.assert_called_once_with(Program.PROGRAM_CSV_FILEPATH, Program.PROGRAM_HEADERS[0], "BSCS", {"Program Name": "Software Engineering"})
  assert result is True