from model.Program import Program

# Initialize the CSV file
print("Initializing program storage...")
Program.intializeProgramStorage()

# Create new program instances
program1 = Program("BSCS", "Bachelor of Science in Computer Science", "CCS")
program2 = Program("BSIT", "Bachelor of Science in Information Technology", "CCS")
program3 = Program("BSA", "Bachelor of Science in Accounting", "CEBA")

# Add new programs
print("Adding new programs...")
Program.addNewProgram(program1)
Program.addNewProgram(program2)
Program.addNewProgram(program3)

# Retrieve a program by program code
print("Getting program record...")
record = Program.getProgramRecord("BSCS")
print(record)  # Should print program details for "BSCS"

# Retrieve all programs under a college
print("Getting programs by college code...")
ccs_programs = Program.getProgramRecordsByCollege("CCS")
print(ccs_programs)  # Should return BSCS and BSIT

# Update a program record
print("Updating program record...")
update_data = {"Program Name": "BS Computer Science"}
Program.updateProgramRecord("BSCS", update_data)

# Verify the update
updated_record = Program.getProgramRecord("BSCS")
print(updated_record)  # Should reflect updated program name

# Remove a program record
print("Deleting program record...")
Program.deleteProgramRecord("BSA")

# Verify deletion
deleted_record = Program.getProgramRecord("BSA")
print(deleted_record)  # Should return None

# Final check of all records
print("Final list of all programs...")
all_programs = Program.getProgramRecordsByCollege("CCS")  # Should only return BSCS and BSIT
print(all_programs)
