import re

ID_NUMBER_PATTERN = r'^\d{4}-\d{4}$'
GENDER_LIST = ["male", "female", "others"]

def validateIdNumber(idNumber: str) -> bool:
  if re.match(ID_NUMBER_PATTERN, idNumber):
    return True
  else:
    return False

def validateYearLevel(yearLevel: int) -> bool:
  if isinstance(yearLevel, int) and yearLevel > 0:
    return True
  else:
    return False

def validateGender(gender: str) -> bool:
  if gender.lower() in GENDER_LIST:
    return True
  else:
    return False