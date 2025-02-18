import random

# Sample first and last names
first_names = [
    "Ethan", "Ava", "Noah", "Charlotte", "Liam", "Amelia", "Benjamin", "Evelyn", "Elijah", "Abigail",
    "Mason", "Harper", "Logan", "Ella", "Jacob", "Grace", "William", "Chloe", "Henry", "Lily",
    "Samuel", "Victoria", "Sebastian", "Hannah", "Jack", "Zoey", "Owen", "Nora", "Caleb", "Madison"
]

last_names = [
    "Castillo", "De Leon", "Domingo", "Estrada", "Ferrer", "Galvez", "Herrera", "Inocencio", "Javier", "Lazaro",
    "Magbanua", "Natividad", "Osorio", "Pangilinan", "Ramirez", "Salazar", "Torres", "Urbano", "Velasco", "Zamora"
]

# Programs with corresponding colleges
programs = [
  ("BTLED-HE", "CED"), ("BTLED-IA", "CED"), ("BSEd-Eng", "CED"), ("BSEd-Math", "CED"), ("BSEd-Sci", "CED"),
  ("BS Psych", "CASS"), ("BA SocSci", "CASS"), ("BA Comm", "CASS"), ("BA Hist", "CASS"), ("BA Phil", "CASS"),
  ("BS Math", "CSM"), ("BS Bio", "CSM"), ("BS Chem", "CSM"), ("BS EnvSci", "CSM"), ("BS Stat", "CSM"),
  ("BSCE", "COE"), ("BSEE", "COE"), ("BSME", "COE"), ("BSChE", "COE"), ("BSIE", "COE"),
  ("BSCS", "CCS"), ("BSIT", "CCS"), ("BSIS", "CCS"), ("BSEMC", "CCS"), ("BSDA", "CCS"),
  ("BSBA-FM", "CEBA"), ("BSBA-MM", "CEBA"), ("BSBA-HRM", "CEBA"), ("BS Accountancy", "CEBA"), ("BS Entrepreneurship", "CEBA"),
  ("BSN", "CHS"), ("BSPT", "CHS"), ("BSMLS", "CHS"), ("BSPH", "CHS"), ("BPharm", "CHS")
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