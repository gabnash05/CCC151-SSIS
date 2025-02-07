from controllers.programControllers import addProgram, updateProgram, removeProgram
from controllers.studentControllers import addStudent, getAllStudents, searchStudentsByField
from controllers.collegeControllers import addCollege
from model.College import College
from model.Student import Student

# addCollege("CASS", "College of Arts and Social Sciences")
# addProgram("BS Psych", "Bachelor of Science in Psychology", "CASS")
# print(addStudent("2024-0012", "Francis", "Cejas", 1, "Male", "BS Psych"))

# addCollege("CSM", "College of Science and Mathematics")
# addProgram("BS Math", "Bachelor of Science in Mathematics", "CSM")

# print(addStudent("2024-0014", "Vincee", "Jandayan", 1, "Male", "BSCS"))

# addCollege("CED", "College of Education")
# addProgram("BTLED-HE", "Bachelor of Technology and Livelihood Education - Home Economics", "CED")
# print(addStudent("2024-0010", "Rene Jr", "Estrella", 1, "Male", "BTLED-HE"))

# print(getAllStudents())

# print(Student.getAllStudentRecordsByProgram("BTLED-HE"))

# addStudent("2024-0121", "Steve", "Jobs", 4, "Male", "BS Math")
# addStudent("2024-0122", "Steve", "Harvey", 4, "Male", "BS Math")
print(searchStudentsByField("College Code", "CASS"))