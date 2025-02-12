from controllers.programControllers import addProgram, updateProgram, removeProgram, searchProgramsByField
from controllers.studentControllers import addStudent, getAllStudents, searchStudentsByField, initializeAllCsv
from controllers.collegeControllers import addCollege, searchCollegesByField, updateCollege
from model.College import College
from model.Student import Student
from model.Program import Program

initializeAllCsv()

# print(getAllStudents())

# print(Student.getAllStudentRecordsByProgram("BTLED-HE"))

# addCollege("CED", "College of Education")
# addProgram("BTLED-HE", "Bachelor of Technology and Livelihood Education - Home Economics", "CED")
# print(addStudent("2024-0010", "Rene Jr", "Estrella", 1, "Male", "BTLED-HE", "CED"))

# addCollege("CASS", "College of Arts and Social Sciences")
# addProgram("BS Psych", "Bachelor of Science in Psychology", "CASS")
# print(addStudent("2024-0012", "Francis", "Cejas", 1, "Male", "BS Psych", "CASS"))

# addCollege("CSM", "College of Science and Mathematics")
# addProgram("BS Math", "Bachelor of Science in Mathematics", "CSM")
# print(addStudent("2024-0014", "Vincee", "Jandayan", 1, "Male", "BS Math", "CSM"))

# addCollege("CCS", "College of Computer Studies")
# addProgram("BSCS", "Bachelor of Science Computer Science", "CCS")
# print(addStudent("2024-0015", "Kim", "Nasayao", 1, "Male", "BSCS", "CCS"))

# print(updateCollege("CAS", "CSM", "College of Science and Mathematics"))
# print()
# print(getAllStudents())
# print()
# print(searchProgramsByField("College Code", "CSM"))