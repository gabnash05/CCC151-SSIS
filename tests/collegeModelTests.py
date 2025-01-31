from model.College import College

# Initialize the CSV file
print("Initializing college storage...")
College.intializeProgramStorage()

# Create new college instances
college1 = College("CCS", "College of Computer Studies")
college2 = College("CBA", "College of Business Administration")
college3 = College("COE", "College of Engineering")

# Add new colleges
print("Adding new colleges...")
College.addNewCollege(college1)
College.addNewCollege(college2)
College.addNewCollege(college3)

# Retrieve a college by college code
print("Getting college record...")
record = College.getCollegeRecord("CCS")
print(record)  # Should print details for "CCS"

# Update a college record
print("Updating college record...")
update_data = {"College Name": "College of Computing and Information Sciences"}
College.updateCollegeRecord("CCS", update_data)

# Verify the update
updated_record = College.getCollegeRecord("CCS")
print(updated_record)  # Should reflect updated college name

# Remove a college record
print("Deleting college record...")
College.deleteCollegeRecord("CBA")

# Verify deletion
deleted_record = College.getCollegeRecord("CBA")
print(deleted_record)  # Should return None

# Final check of all records
print("Final list of all colleges...")
print(College.getCollegeRecord("CCS"))  # Should return the updated CCS record
print(College.getCollegeRecord("COE"))  # Should return COE record
