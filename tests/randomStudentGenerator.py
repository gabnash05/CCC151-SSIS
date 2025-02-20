import random

# Sample first and last names
first_names = [
    "Liam", "Olivia", "Noah", "Emma", "Oliver", "Ava", "Elijah", "Sophia", "James", "Isabella",
    "William", "Mia", "Benjamin", "Charlotte", "Lucas", "Amelia", "Henry", "Harper", "Alexander", "Evelyn",
    "Michael", "Abigail", "Daniel", "Ella", "Matthew", "Scarlett", "Ethan", "Grace", "Joseph", "Lily",
    "Samuel", "Aria", "David", "Chloe", "Sebastian", "Madison", "Jackson", "Layla", "Aiden", "Riley",
    "John", "Zoey", "Owen", "Nora", "Luke", "Hannah", "Gabriel", "Hazel", "Anthony", "Violet",
    "Isaac", "Aurora", "Dylan", "Penelope", "Leo", "Luna", "Julian", "Stella", "Wyatt", "Ellie",
    "Nathan", "Paisley", "Caleb", "Skylar", "Ryan", "Savannah", "Adrian", "Nova", "Hunter", "Leah",
    "Christian", "Audrey", "Jaxon", "Brooklyn", "Andrew", "Bella", "Joshua", "Aaliyah", "Christopher", "Claire",
    "Theodore", "Lucy", "Thomas", "Alice", "Charles", "Maya", "Eli", "Sadie", "Landon", "Eva",
    "Connor", "Emilia", "Josiah", "Autumn", "Isaiah", "Valentina", "Jonathan", "Naomi", "Cameron", "Everly"
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
    "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
    "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
    "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennet", "Gray", "Mendoza", "Ruiz", "Hughes",
    "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez"
]

# Programs with corresponding colleges
programs = [
  # College of Education (CED)
  ("BTLED-HE", "CED"), ("BTLED-IA", "CED"), ("BSEd-Eng", "CED"), ("BSEd-Math", "CED"), ("BSEd-Sci", "CED"),
  ("BSEd-Fil", "CED"), ("BSEd-SocSci", "CED"), ("BSEd-PE", "CED"), ("BSEd-Values", "CED"), ("BSEd-SpEd", "CED"),

  # College of Arts and Social Sciences (CASS)
  ("BS Psych", "CASS"), ("BA SocSci", "CASS"), ("BA Comm", "CASS"), ("BA Hist", "CASS"), ("BA Phil", "CASS"),
  ("BA Eng", "CASS"), ("BA Filipino", "CASS"), ("BA IR", "CASS"), ("BA DevCom", "CASS"), ("BA Journ", "CASS"),

  # College of Science and Mathematics (CSM)
  ("BS Math", "CSM"), ("BS Bio", "CSM"), ("BS Chem", "CSM"), ("BS EnvSci", "CSM"), ("BS Stat", "CSM"),
  ("BS Applied Physics", "CSM"), ("BS Marine Bio", "CSM"), ("BS Geology", "CSM"), ("BS Forensic Sci", "CSM"), ("BS Biotech", "CSM"),

  # College of Engineering (COE)
  ("BSCE", "COE"), ("BSEE", "COE"), ("BSME", "COE"), ("BSChE", "COE"), ("BSIE", "COE"),
  ("BSECE", "COE"), ("BSRE", "COE"), ("BSGE", "COE"), ("BS AeroEng", "COE"), ("BS NavalEng", "COE"),

  # College of Computer Studies (CCS)
  ("BSCS", "CCS"), ("BSIT", "CCS"), ("BSIS", "CCS"), ("BSEMC", "CCS"), ("BSDA", "CCS"),
  ("BS CyberSec", "CCS"), ("BS AI", "CCS"), ("BSSE", "CCS"), ("BS DataSci", "CCS"), ("BS GameDev", "CCS"),

  # College of Economics, Business, and Accountancy (CEBA)
  ("BSBA-FM", "CEBA"), ("BSBA-MM", "CEBA"), ("BSBA-HRM", "CEBA"), ("BS Accountancy", "CEBA"), ("BS Entrepreneurship", "CEBA"),
  ("BSBA-OM", "CEBA"), ("BSBA-IB", "CEBA"), ("BS Econ", "CEBA"), ("BS Finance", "CEBA"), ("BS Public Ad", "CEBA"),

  # College of Health Sciences (CHS)
  ("BSN", "CHS"), ("BSPT", "CHS"), ("BSMLS", "CHS"), ("BSPH", "CHS"), ("BPharm", "CHS"),
  ("BS Radiology", "CHS"), ("BSOT", "CHS"), ("BSDent", "CHS"), ("BSRT", "CHS"), ("BSN Midwifery", "CHS")
]

# Generate 200 random students
students = []
for i in range(200):
  student_id = f"{random.randint(2021, 2024)}-{random.randint(1000, 9999)}"
  first_name = random.choice(first_names)
  last_name = random.choice(last_names)
  year_level = random.randint(1, 4)
  gender = random.choice(["Male", "Female"])
  program, college = random.choice(programs)

  students.append(f"{student_id},{first_name},{last_name},{year_level},{gender},{program},{college}")

# Join into a formatted string
students_data = "\n".join(students)

print("\n".join(students))