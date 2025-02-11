<h1>
  <img src="assets/LogoIcon.png" width="30" alt="Project Logo">
  Lexis - a Student Information System
</h1>

## About This Project

This project is developed in fulfillment of the requirements for the subject **CCC151 - Information Management Systems**.

<br><br>

## **Setup Instructions**

### **1. Clone the Repository**

```sh
git clone <https://github.com/gabnash05/CCC151-SSIS.git>
cd <your-project-folder>
```
### **2. Create and Activate a Virtual Environment**

```sh
python -m venv ssis_env
```

### **3. Activate the Virtual Environment**

```sh
ssis_env\Scripts\activate
```

### **4. Install Dependencies**

```sh
pip install -r requirements.txt
```

---

<br><br>

## **Running the Project**

Make sure the virtual environment is activated and all dependencies are installed
```sh
python src/main.py
```

## **Deactivating the Virtual Environment**

When you're done working, deactivate the virtual environment:
```sh
deactivate
```

---
<br><br>

## **Troubleshooting**

If `pip install -r requirements.txt` fails, try updating ``pip` first:
```sh
pip install --upgrade pip
```

(Optional) Run tests:
```sh
pytest
```

If `pytest` is not found, install:
```sh
pip install pytest pytest-mock
```