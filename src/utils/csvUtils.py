import csv
import os
from typing import List, Dict, Optional

# Creates a new csv file for data if csv file does not already exist
def initializeCsv(filepath: str, headers: List[str]) -> bool:
  try:
    if not os.path.exists(filepath):
      print(f"File does not exist. Creating: {filepath}")
      with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        return True

  except Exception as error:
    print(f"Error initializing CSV: {error}")
    return False

# Returns the whole csv file into an array of dicts
def readCsv(filepath: str) -> List[Dict[str,str]]:
  data = []
  try:
    if not os.path.exists(filepath):
      print(f"Error: File '{filepath}' does not exist")
      return []
    
    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
      reader = csv.DictReader(file)
      data = list(reader)
    
    return data
  
  except Exception as error:
    print(f"Error reading CSV: {error}")
    return []

# Overwrites the whole csv file
def writeCsv(filepath: str, data: List[Dict[str, str]]) -> bool:
  try:
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
      if not data:
        print("Warning: No data provided. Writing only headers.")
        file.write("")
        return True

      writer = csv.DictWriter(file, fieldnames=data[0].keys())
      writer.writeheader()
      writer.writerows(data)
      return True
    
  except Exception as error:
    print(f"Error writing to CSV: {error}")
    return False

# Gets rows from csv file that matches a field and value as an array of dicts
def getRowsByFieldCsv(filepath: str, searchValue: str, searchField: Optional[str] = None) -> List[Dict[str, str]]:
  try:
    matching_records = []

    with open(filepath, mode="r", encoding="utf-8") as file:
      reader = csv.DictReader(file)
      fieldnames = reader.fieldnames

      if not fieldnames:
        print("Error: Empty or malformed CSV file.")
        return []

      isStudentCsv = "First Name" in fieldnames and "Last Name" in fieldnames

      for record in reader:
        if searchField:
          if searchField not in fieldnames:
            print(f"Error: Field '{searchField}' not found in CSV")
            return []
          
          if searchValue.lower() == record[searchField].lower():
            matching_records.append(record)

        else:
          if isStudentCsv:
            # Handle special case for searching multiple words in student names or programs
            if " " in searchValue and searchValue.lower().startswith(("bs", "ba", "bt")):
              searchWords = [searchValue.lower()]
            else:
              searchWords = searchValue.lower().split()
              
            firstName = record["First Name"].lower()
            lastName = record["Last Name"].lower()
            fullName = f"{firstName} {lastName}"

            # Check if all search words appear in the full name
            if all(word in fullName for word in searchWords):
              matching_records.append(record)

            # If only one word, check all fields (e.g., searching for "Lucy" or "BSCS")
            elif len(searchWords) == 1:
              if any(searchWords[0] in value.lower() for value in record.values()):
                matching_records.append(record)
          else:
            if any(searchValue.lower() in value.lower() for value in record.values()):
              matching_records.append(record)

    return matching_records

  except Exception as error:
    print(f"Error reading CSV by Field: {error}")  
    return []

# Gets a single row from csv file as a dict
def getRowByIdCsv(filepath: str, id: str) -> Dict:
  try:
    data = readCsv(filepath)
    
    for record in data:
      key = list(record.keys())[0]
      recordId = record[key]
      if recordId.lower() == id.lower():
        return record

    print(f"No records found with ID: {id}")
    return {}
    
  except Exception as error:
    print(f"Error reading CSV by ID: {error}")  
    return {}

# Adds a new row to the csv file
def appendRowCsv(filepath: str, data: Dict) -> bool:
  
  if not isinstance(data, dict):
    print("Error: appendRowCsv() expects a dictionary as input")
    return False

  try:
    file_exists = os.path.exists(filepath)

    with open(filepath, mode='a', newline='', encoding='utf-8') as file:
      writer = csv.DictWriter(file, fieldnames=data.keys())

      # Write header if file does not exist or is empty
      if not file_exists or os.stat(filepath).st_size == 0:
        writer.writeheader()

      writer.writerow(data)
      return True

  except Exception as error:
    print(f"Error appending row to CSV: {error}")
    return False

# UPDATED
def updateRowByFieldCsv(filepath: str, searchField: str, searchValue: str, updateData: Dict) -> bool:
  try:
    temp_filepath = str(filepath) + ".tmp"
    fieldnames = None
    isUpdated = False

    with open(filepath, mode='r', newline='', encoding='utf-8') as input_file, \
          open(temp_filepath, mode='w', newline='', encoding='utf-8') as output_file:

      reader = csv.DictReader(input_file)
      fieldnames = reader.fieldnames
      writer = csv.DictWriter(output_file, fieldnames=fieldnames)

      writer.writeheader()

      for row in reader:
        if row[searchField].lower() == searchValue.lower():
          row.update(updateData)  # Update the row with new values
          isUpdated = True
        writer.writerow(row)  # Write (modified or unmodified) row

    if isUpdated:
      os.replace(temp_filepath, filepath)  # Safely replace original file
      return True
    else:
      os.remove(temp_filepath)  # Cleanup if no change was made
      print(f"No record found with {searchField} = {searchValue}")
      return False

  except Exception as error:
    print(f"Error updating CSV row: {error}")
    return False

# UPDATED
# Deletes a row in the csv file
def deleteRowByFieldCsv(filepath: str, searchField: str, searchValue: str) -> bool:
  try:
    temp_filepath = str(filepath) + ".tmp"
    fieldnames = None
    record_found = False

    with open(filepath, mode='r', newline='', encoding='utf-8') as input_file, \
      open(temp_filepath, mode='w', newline='', encoding='utf-8') as output_file:

      reader = csv.DictReader(input_file)
      fieldnames = reader.fieldnames
      writer = csv.DictWriter(output_file, fieldnames=fieldnames)

      writer.writeheader()

      for row in reader:
        if row[searchField].lower() == searchValue.lower():
          record_found = True  # Mark that a record was found
        else:
          writer.writerow(row)  # Keep this row

    if record_found:
      os.replace(temp_filepath, filepath)  # Overwrite original file with the modified version
      return True
    else:
      os.remove(temp_filepath)  # Cleanup unused temp file
      print(f"No record found with {searchField} = {searchValue}")
      return False

  except Exception as error:
      print(f"Error deleting CSV row: {error}")
      return False

# Checks if csv id row is unique
def checkIdIfExistsCsv(filepath: str, id: str) -> bool:
  try:
    records = readCsv(filepath)

    for record in records:
      first_value = next(iter(record.values()))
      if first_value == id:
        return True
    
    return False
  
  except Exception as error:
    print(f"Error checking if ID is : {error}")
    return False

