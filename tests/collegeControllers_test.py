import pytest
from unittest.mock import patch
from controllers.collegeControllers import (
  addCollege, searchCollegesByField, updateCollege, removeCollege
)
from model.College import College
from model.Program import Program

# Mock Data
mock_college = {
  "College Code": "CCS",
  "College Name": "College of Computer Studies"
}

@pytest.fixture
def valid_college():
  return ("CCS", "College of Computer Studies")

@pytest.fixture
def invalid_college():
  return ("", "")

# Test addCollege
@patch("model.College.College.addNewCollege", return_value=True)
def test_add_college_success(mock_add, valid_college):
  result = addCollege(*valid_college)
  assert result == "College added successfully."

@patch("model.College.College.addNewCollege", return_value=False)
def test_add_college_fail(mock_add, valid_college):
  result = addCollege(*valid_college)
  assert result == "Failed to add college."

def test_add_college_missing_fields():
  result = addCollege("", "College of Engineering")
  assert result == "Enter all required fields"

@patch("model.College.College.collegeCodeExists", return_value=True)
def test_add_college_already_exists(mock_college_exist, valid_college):
  result = addCollege(*valid_college)
  assert result == "College already exists"

# Test searchCollegesByField
@patch("model.College.College.getCollegeRecordByCode", return_value=mock_college)
def test_search_college_by_code(mock_search):
  result = searchCollegesByField("College Code", "CCS")
  assert result == [mock_college]

def test_search_college_invalid_field():
  result = searchCollegesByField("Invalid Field", "CCS")
  assert result == []

def test_search_college_invalid_value():
  result = searchCollegesByField("College Name", None)
  assert result == []

# Test updateCollege
@patch("model.College.College.updateCollegeRecord", return_value=True)
@patch("model.Program.Program.getProgramRecordsByCollege", return_value=[{"Program Code": "BSCS"}])
@patch("model.College.College.collegeCodeExists", return_value=True)
def test_update_college_success(mock_update_college, mock_get_programs, mock_college_exists):
  result = updateCollege("CCS", "COE", "College of Engineering")
  assert result == "College updated successfully."

@patch("model.Program.Program.updateProgramRecordByCode", return_value=False)
@patch("model.College.College.collegeCodeExists", return_value=True)
def test_update_college_fail(mock_update, mock_college_exists):
  result = updateCollege("CCS", "COE", "College of Engineering")
  assert result == "Failed to update college."

@patch("model.College.College.collegeCodeExists", return_value=False)
def test_update_college_invalid_code(mock_college_exists):
  result = updateCollege("INVALID", "COE", "College of Engineering")
  assert result == "College Code does not exist"

# Test removeCollege
@patch("model.College.College.deleteCollegeRecord", return_value=True)
@patch("model.Program.Program.getProgramRecordsByCollege", return_value=[{"Program Code": "BSCS"}])
@patch("model.Program.Program.updateProgramRecordByCode", return_value=True)
def test_remove_college_success(mock_update_program, mock_get_programs, mock_remove):
  result = removeCollege("CCS")
  assert result == "College removed successfully."

@patch("model.College.College.deleteCollegeRecord", return_value=False)
def test_remove_college_fail(mock_remove):
  result = removeCollege("CCS")
  assert result == "Failed to remove college."

def test_remove_college_invalid_code():
  result = removeCollege("")
  assert result == "College Code is required."
