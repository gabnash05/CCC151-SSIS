import csv
import os
from typing import List, Dict

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
      return None
    
    with(open(filepath, mode='r', newline='', encoding='utf-8') as file):
      reader = csv.DictReader(file)
      data = list(reader)
    
    return data
  
  except Exception as error:
    print(f"Error reading CSV: {error}")
    return None

# Overwrites the whole csv file
def writeCsv(filepath: str, data: List[Dict[str,str]]) -> bool:
  if not data:
    print("No data provided to writeCsv(). Rewriting entire file into blank")
    return True
  
  fieldnames = data[0].keys()
  try:
    if not os.path.exists(filepath):
      print(f"Error: File '{filepath}' does not exist")
      return None

    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
      writer = csv.DictWriter(file, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(data)
      return True
    
  except Exception as error:
    print(f"Error writing to CSV: {error}")
    return False

# Gets rows from csv file that matches a field and value as an array of dicts
def getRowsByFieldCsv(filepath: str, searchValue: str, searchField: str = None) -> List[Dict[str, str]]:
  try:
    data = readCsv(filepath)
    if not data:
      return []
    
    # Searching by a specific field
    if searchField:
      if searchField not in data[0]:
        print(f"Error: Field '{searchField}' not found in CSV")
        return []
      
      return [
        record for record in data
        if searchValue.lower() in record[searchField].lower()
      ]
    
    # Searching without a search field
    
    # Check if searching for Student
    isStudentCsv = "First Name" in data[0] and "Last Name" in data[0]
    if isStudentCsv:
      # Check if searching for multiple words (e.g., "Lucy Smith" or "BS Bi") and split if its a name
      if " " in searchValue and (searchValue.startswith(("BS", "BA", "BT"))):
        searchWords = [searchValue.lower()]
      else:
        searchWords = searchValue.lower().split()

      filteredRecords = []
      for record in data:
        firstName = record["First Name"].lower()
        lastName = record["Last Name"].lower()
        fullName = f"{firstName} {lastName}"

        # Check if all search words appear in the full name
        if all(word in fullName for word in searchWords):
          filteredRecords.append(record)

        # If only one word, check all fields (e.g., searching for "Lucy" or "BSCS")
        elif len(searchWords) == 1:
          if any(searchWords[0] in value.lower() for value in record.values()):
            filteredRecords.append(record)

      return filteredRecords
  
    return [
      record for record in data
      if any(searchValue.lower() in value.lower() for value in record.values())
    ]

    
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
      if recordId == id:
        return record

    print(f"No records found with ID: {id}")
    return None
    
  except Exception as error:
    print(f"Error reading CSV by ID: {error}")  
    return None

# Adds a new row to the csv file
def appendRowCsv(filepath: str, data: str) -> bool:
  if not isinstance(data, dict):
    print("Error: appendRowCsv() expects a dictionary as input")
    return False
  
  try:
    if not os.path.exists(filepath):
      print(f"Error: File '{filepath}' does not exist")
      return False

    with open(filepath, mode='a', newline='', encoding='utf-8') as file:
      writer = csv.DictWriter(file, fieldnames=data.keys())
      writer.writerow(data)
      return True

  except Exception as error:
    print(f"Error appending row to CSV: {error}")
    return False

# Updates a row in the csv file
def updateRowByFieldCsv(filepath: str, searchField: str, searchValue: str, updateData: Dict) -> bool:
  try:
    records = readCsv(filepath)
    isUpdated = False

    for record in records:
      if record[searchField].lower() == searchValue.lower():
        record.update(updateData)
        isUpdated = True
        break

    if isUpdated:
      return writeCsv(filepath, records)
    
    print(f"No record found with {searchField} = {searchValue}")
    return False
    
  except Exception as error:
    print(f"Error updating CSV row: {error}")
    return False

# Deletes a row in the csv file
def deleteRowByFieldCsv(filepath: str, searchField: str, searchValue: str) -> bool:
  try:
    records = readCsv(filepath)
    newRecords = [record for record in records if record[searchField].lower() != searchValue.lower()]

    if len(newRecords) < len(records):
      return writeCsv(filepath, newRecords)
    
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

