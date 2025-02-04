import pytest
from unittest.mock import patch
from controllers.studentControllers import (
    addStudent, getAllStudents, searchStudentsByField,
    getStudentsByYearLevel, getStudentsByGender,
    updateStudent, removeStudent
)

# Mock Data
mock_student = {
    "ID Number": "2023-0001",
    "First Name": "John",
    "Last Name": "Doe",
    "Year Level": 2,
    "Gender": "Male",
    "Program Code": "CS"
}

@pytest.fixture
def valid_student():
    return ("2023-0001", "John", "Doe", 2, "Male", "CS")

@pytest.fixture
def invalid_student():
    return ("2023-XYZ", "", "", -1, "Unknown", "")

# Test addStudent
@patch("model.Program.Program.programCodeExists", return_value=True)
@patch("model.Student.Student.idNumberExists", return_value=False)
@patch("model.Student.Student.addStudentRecord", return_value=True)
def test_add_student_success(mock_add, mock_id_exists, mock_program_exists, valid_student):
    result = addStudent(*valid_student)
    assert result == "Student added successfully."

@patch("model.Program.Program.programCodeExists", return_value=True)
@patch("model.Student.Student.idNumberExists", return_value=False)
@patch("model.Student.Student.addStudentRecord", return_value=False)
def test_add_student_fail(mock_add, mock_id_exists, mock_program_exists, valid_student):
    result = addStudent(*valid_student)
    assert result == "Failed to add student."

@pytest.mark.parametrize("id_number", [None, ""])
def test_add_student_missing_fields(id_number):
    result = addStudent(id_number, "John", "Doe", 2, "Male", "CS")
    assert result == "Enter all required fields"

def test_add_student_invalid_id():
    result = addStudent("123-ABC", "John", "Doe", 2, "Male", "CS")
    assert result == "Invalid ID Number"

def test_add_student_invalid_year():
    result = addStudent("2023-0001", "John", "Doe", -1, "Male", "CS")
    assert result == "Year Level must be a positive integer."

def test_add_student_invalid_gender():
    result = addStudent("2023-0001", "John", "Doe", 2, "Unknown", "CS")
    assert result == "Gender must be Male, Female, or Others."

# Test getAllStudents
@patch("model.Student.Student.getAllStudentRecords", return_value=[mock_student])
def test_get_all_students(mock_get):
    result = getAllStudents()
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["ID Number"] == "2023-0001"

# Test searchStudentsByField
@patch("model.Student.Student.getStudentRecord", return_value=mock_student)
def test_search_students_by_id(mock_search):
    result = searchStudentsByField("ID Number", "2023-0001")
    assert result == [mock_student]

def test_search_students_invalid_field():
    result = searchStudentsByField("Invalid Field", "2023-0001")
    assert result == []

def test_search_students_invalid_value():
    result = searchStudentsByField("First Name", None)
    assert result == []

# Test updateStudent
@patch("model.Student.Student.updateStudentRecordById", return_value=True)
def test_update_student_success(mock_update):
    result = updateStudent("2023-0001", "2023-0002", "Jane", "Doe", 3, "Female", "IT")
    assert result == "Student updated successfully."

@patch("model.Student.Student.updateStudentRecordById", return_value=False)
def test_update_student_fail(mock_update):
    result = updateStudent("2023-0001", "2023-0002", "Jane", "Doe", 3, "Female", "IT")
    assert result == "Failed to update student."

def test_update_student_invalid_id():
    result = updateStudent("123-XYZ", "2023-0002", "Jane", "Doe", 3, "Female", "IT")
    assert result == "Invalid ID Number"

# Test removeStudent
@patch("model.Student.Student.removeStudentRecordById", return_value=True)
def test_remove_student_success(mock_remove):
    result = removeStudent("2023-0001")
    assert result == "Student removed successfully."

@patch("model.Student.Student.removeStudentRecordById", return_value=False)
def test_remove_student_fail(mock_remove):
    result = removeStudent("2023-0001")
    assert result == "Failed to remove student."

def test_remove_student_invalid_id():
    result = removeStudent("123-XYZ")
    assert result == "Invalid ID Number"