import pytest
from unittest.mock import patch
from controllers.programControllers import (
    addProgram, searchProgramsByField, updateProgram, removeProgram
)
from model.Program import Program
from model.Student import Student
from model.College import College

# Mock Data
mock_program = {
    "Program Code": "BSCS",
    "Program Name": "Bachelor of Science in Computer Science",
    "College Code": "CCS"
}

@pytest.fixture
def valid_program():
    return ("BSCS", "Bachelor of Science in Computer Science", "CCS")

@pytest.fixture
def invalid_program():
    return ("XYZ123", "", "")

# Test addProgram
@patch("model.Program.Program.addNewProgram", return_value=True)
@patch("model.College.College.collegeCodeExists", return_value=True)
def test_add_program_success(mock_add, mock_college_exist,valid_program):
    result = addProgram(*valid_program)
    assert result == "Program added successfully."

@patch("model.Program.Program.addNewProgram", return_value=False)
@patch("model.College.College.collegeCodeExists", return_value=True)
def test_add_program_fail(mock_add, mock_college_exist, valid_program):
    result = addProgram(*valid_program)
    assert result == "Failed to add program."

def test_add_program_missing_fields():
    result = addProgram(None, "Computer Science", "CCS")
    assert result == "Enter all required fields"

@patch("model.College.College.collegeCodeExists", return_value=False)
def test_add_program_invalid_college(mock_college_exist, valid_program):
    result = addProgram(*valid_program)
    assert result == "College Code does not exist"

@patch("model.Program.Program.programCodeExists", return_value=True)
@patch("model.College.College.collegeCodeExists", return_value=True)
def test_add_program_already_exists(mock_program_exist, mock_college_exist, valid_program):
    result = addProgram(*valid_program)
    assert result == "Program already exists"

# Test searchProgramsByField
@patch("model.Program.Program.getProgramRecordByCode", return_value=mock_program)
def test_search_program_by_code(mock_search):
    result = searchProgramsByField("Program Code", "BSCS")
    assert result == [mock_program]

@patch("model.Program.Program.getProgramRecordsByName", return_value=[mock_program])
def test_search_program_by_name(mock_search):
    result = searchProgramsByField("Program Name", "Computer Science")
    assert result == [mock_program]

@patch("model.Program.Program.getProgramRecordsByCollege", return_value=[mock_program])
def test_search_program_by_college(mock_search):
    result = searchProgramsByField("College Code", "CCS")
    assert result == [mock_program]

def test_search_program_invalid_field():
    result = searchProgramsByField("Invalid Field", "BSCS")
    assert result == []

def test_search_program_invalid_value():
    result = searchProgramsByField("Program Name", None)
    assert result == []

# Test updateProgram
@patch("model.Program.Program.updateProgramRecordByCode", return_value=True)
@patch("model.Student.Student.getAllStudentRecordsByProgram", return_value=[{"ID Number": "12345"}])
@patch("model.Student.Student.updateStudentRecordById", return_value=True)
@patch("model.College.College.collegeCodeExists", return_value=True)
def test_update_program_success(mock_update_program, mock_get_students, mock_update_student, mock_college_exists):
    result = updateProgram("BSCS", "CS102", "Software Engineering", "COE")
    assert result == "Program updated successfully."

@patch("model.Program.Program.updateProgramRecordByCode", return_value=False)
@patch("model.College.College.collegeCodeExists", return_value=True)
def test_update_program_fail(mock_update, mock_college_exists):
    result = updateProgram("BSCS", "CS102", "Software Engineering", "COE")
    assert result == "Failed to update program."

@patch("model.College.College.collegeCodeExists", return_value=True)
def test_update_program_missing_fields(mock_college_exists):
    result = updateProgram("None", "BSCS", "Software Engineering", "COE")
    assert result == "Failed to update program."

@patch("model.College.College.collegeCodeExists", return_value=False)
def test_update_program_invalid_college(mock_college_exists):
    result = updateProgram("BSCS", "CS102", "Software Engineering", "INVALID")
    assert result == "College Code does not exist"

# Test removeProgram
@patch("model.Program.Program.deleteProgramRecord", return_value=True)
@patch("model.Student.Student.getAllStudentRecordsByProgram", return_value=[{"ID Number": "12345"}])
@patch("model.Student.Student.updateStudentRecordById", return_value=True)
def test_remove_program_success(mock_update_student, mock_get_students, mock_remove):
    result = removeProgram("BSCS")
    assert result == "Program removed successfully."

@patch("model.Program.Program.deleteProgramRecord", return_value=False)
def test_remove_program_fail(mock_remove):
    result = removeProgram("BSCS")
    assert result == "Failed to remove program."

def test_remove_program_invalid_code():
    result = removeProgram("")
    assert result == "Program Code is required."
