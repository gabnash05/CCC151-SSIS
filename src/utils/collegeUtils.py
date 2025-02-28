import csv
import os
from typing import List, Dict, Optional
from pathlib import Path
  
STUDENT_CSV_FILEPATH = Path(__file__).parent.parent.parent / "data" / "students.csv"
PROGRAM_CSV_FILEPATH = Path(__file__).parent.parent.parent / "data" / "programs.csv"

def getCollegeCode(studentId: str) -> Optional[str]:
  programCode = None

  # Open students.csv and find the program code
  try:
    with open(STUDENT_CSV_FILEPATH, mode='r', newline='', encoding='utf-8') as file:
      reader = csv.reader(file)
      headers = next(reader)  # Read the header row
      for row in reader:
        if row[0] == studentId:  # Assuming Student ID is in the first column
          programCode = row[5]  # Get 6th column (index 5)
          break

  except Exception as error:
    print(f"Error reading students.csv: {error}")
    return None

  if not programCode:
    print(f"Error: Student ID '{studentId}' not found or missing program code")
    return None

  # Open programs.csv and find the college code
  try:
    with open(PROGRAM_CSV_FILEPATH, mode='r', newline='', encoding='utf-8') as file:
      reader = csv.reader(file)
      headers = next(reader)
      for row in reader:
        if row[0] == programCode:
          return row[2] 
        
  except Exception as error:
    print(f"Error reading programs.csv: {error}")
    return None

  return None

  