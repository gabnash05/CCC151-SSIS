import pytest
from unittest.mock import patch
from model.College import College


def test_initializeProgramStorage(mocker):
  mock_initializeCsv = mocker.patch("utils.csvUtils.initializeCsv", return_value=True)

  result = College.intializeProgramStorage()

  mock_initializeCsv.assert_called_once_with(College.COLLEGE_CSV_FILEPATH, College.COLLEGE_HEADERS)
  assert result is True


def test_addNewCollege(mocker):
  mock_appendRowCsv = mocker.patch("utils.csvUtils.appendRowCsv", return_value=True)
  college = College("COE", "College of Engineering")

  result = College.addNewCollege(college)

  mock_appendRowCsv.assert_called_once_with(College.COLLEGE_CSV_FILEPATH, college.toDict())
  assert result is True


def test_getCollegeRecordByCode(mocker):
  mock_getRowByIdCsv = mocker.patch("utils.csvUtils.getRowByIdCsv", return_value={"College Code": "CCS", "College Name": "College of Computer Studies"})

  result = College.getCollegeRecordByCode("CCS")

  mock_getRowByIdCsv.assert_called_once_with(College.COLLEGE_CSV_FILEPATH, "CCS")
  assert result["College Code"] == "CCS"
  assert result["College Name"] == "College of Computer Studies"

def test_getCollegeRecordByName(mocker):
    mock_getRowsByFieldCsv = mocker.patch(
        "utils.csvUtils.getRowsByFieldCsv", 
        return_value={"College Code": "CCS", "College Name": "College of Computer Studies"}
    )

    result = College.getCollegeRecordByName("College of Computer Studies")

    mock_getRowsByFieldCsv.assert_called_once_with(
        College.COLLEGE_CSV_FILEPATH, College.COLLEGE_HEADERS[1], "College of Computer Studies"
    )
    assert result["College Code"] == "CCS"
    assert result["College Name"] == "College of Computer Studies"

def test_getAllCollegeRecords(mocker):
  mock_readCsv = mocker.patch("utils.csvUtils.readCsv", return_value=[
    {"College Code": "CCS", "College Name": "College of Computer Studies"},
    {"College Code": "CSM", "College Name": "College of Science and Mathematics"},
    {"College Code": "COE", "College Name": "College of Engineering"},
  ])

  result = College.getAllCollegeRecords()

  mock_readCsv.assert_called_once_with(College.COLLEGE_CSV_FILEPATH)
  assert len(result) == 3
  assert result[0]["College Code"] == "CCS"
  assert result[1]["College Code"] == "CSM"
  assert result[2]["College Code"] == "COE"


def test_updateCollegeRecord(mocker):
  mock_updateRowByFieldCsv = mocker.patch("utils.csvUtils.updateRowByFieldCsv", return_value=True)

  result = College.updateCollegeRecord("CCS", {"College Name": "New College of Computer Studies"})

  mock_updateRowByFieldCsv.assert_called_once_with(College.COLLEGE_CSV_FILEPATH, College.COLLEGE_HEADERS[0], "CCS", {"College Name": "New College of Computer Studies"})
  assert result is True


def test_deleteCollegeRecord(mocker):
  mock_deleteRowByFieldCsv = mocker.patch("utils.csvUtils.deleteRowByFieldCsv", return_value=True)

  result = College.deleteCollegeRecord("CCS")

  mock_deleteRowByFieldCsv.assert_called_once_with(College.COLLEGE_CSV_FILEPATH, College.COLLEGE_HEADERS[0], "CCS")
  assert result is True
