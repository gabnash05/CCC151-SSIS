import pytest
from model.Student import Student

STUDENT_ID = "2023-0001"

def test_initializeStudentStorage(mocker):
  mock_initializeCsv = mocker.patch("utils.csvUtils.initializeCsv")
  Student.intializeStudentStorage()
  mock_initializeCsv.assert_called_once()

def test_addStudentRecord(mocker):
  mock_appendRowCsv = mocker.patch("utils.csvUtils.appendRowCsv", return_value=True)
  student = Student(STUDENT_ID, "John", "Doe", 1, "Male", "CS")
  
  result = Student.addStudentRecord(student)
  
  mock_appendRowCsv.assert_called_once_with(Student.STUDENT_CSV_FILEPATH, student.toDict())
  assert result is True

def test_getStudentRecord(mocker):
  mock_getRowByIdCsv = mocker.patch("utils.csvUtils.getRowByIdCsv", return_value={"ID Number": STUDENT_ID, "First Name": "John"})
  
  result = Student.getStudentRecord(STUDENT_ID)
  
  mock_getRowByIdCsv.assert_called_once()
  assert result["ID Number"] == STUDENT_ID

def test_getAllStudentRecords(mocker):
  mock_readCsv = mocker.patch("utils.csvUtils.readCsv", return_value=[{"ID Number": STUDENT_ID, "First Name": "John"}])
  
  result = Student.getAllStudentRecords()
  
  mock_readCsv.assert_called_once()
  assert len(result) == 1

def test_getAllStudentRecordsByFirstName(mocker):
  mock_getRowsByFieldCsv = mocker.patch("utils.csvUtils.getRowsByFieldCsv", return_value=[{"ID Number": STUDENT_ID, "First Name": "John"}])
  
  result = Student.getAllStudentRecordsByFirstName("John")
  
  mock_getRowsByFieldCsv.assert_called_once()
  assert result[0]["First Name"] == "John"

def test_updateStudentRecordById(mocker):
  mock_updateRowByFieldCsv = mocker.patch("utils.csvUtils.updateRowByFieldCsv", return_value=True)
  updateData = {"First Name": "Johnny"}
  
  result = Student.updateStudentRecordById(STUDENT_ID, updateData)
  
  mock_updateRowByFieldCsv.assert_called_once()
  assert result is True

def test_removeStudentRecordById(mocker):
  mock_deleteRowByFieldCsv = mocker.patch("utils.csvUtils.deleteRowByFieldCsv", return_value=True)
  
  result = Student.removeStudentRecordById(STUDENT_ID)
  
  mock_deleteRowByFieldCsv.assert_called_once()
  assert result is True