<h1>
  <img src="assets/LogoIcon.png" width="30" alt="Project Logo">
  Lexis - a Student Information System
</h1>

This project is developed in fulfillment of the requirements for the subject **CCC151 - Information Management Systems**.

<br></br>
## About This Project

Lexis is a student information system built using Python, PyQt6, and using CSV data storage **without a DBMS**. It provides full CRUDL capabilities, including features such as **sorting**, **searching**, and **unique ID management**.

<br></br>

## **Features**
- Store **STUDENT**, **PROGRAM**, and **COLLEGE** records for any University
- **ADD**, **EDIT**, and **DELETE** records
- **SORT** and **SEARCH** records by multiple fields  
- Intuitive **PyQt6** UI  
- **CSV**-based database (lightweight storage)  

<br></br>

## **Demo**
*Screenshots Unavailable*

<br></br>

## **Setup Instructions**

### **1. Clone the Repository**

```sh
git clone https://github.com/gabnash05/CCC151-SSIS.git
cd CCC151-SSIS
```
### **2. Create and Activate a Virtual Environment**
- **Windows Command Prompt:**
  ```sh
  python -m venv ssis_env
  ```
- **Linux/macOS:**
  ```sh
  source venv/bin/activate
  ```
You’ll see (venv) appear in the terminal, indicating that you're inside the virtual environment.

### **3. Activate the Virtual Environment**

- **Windows Command Prompt:**
  ```sh
  ssis_env\Scripts\activate
  ```

- **Windows Powershell:**
  ```sh
  .\ssis_env\Scripts\Activate
  ```

- **Linux/macOS:**
  ```sh
  source ssis_env/bin/activate
  ```

### **4. Install Dependencies**

```sh
pip install -e .
```
This installs all required dependencies including PyQt6 and any other libraries listed in `requirements.txt`
___

<br></br>

## **Running the Project**

Make sure the virtual environment is activated and all dependencies were installed properly
```sh
python -m src.main
```
<br></br>

## **Deactivating the Virtual Environment**

When you're done working, deactivate the virtual environment:
```sh
deactivate
```

<br></br>

## **Troubleshooting**

If `pip install -e .` fails, try manually installing dependencies using:
```sh
pip install -r requirements.txt
```

If `pip install -r requirements.txt` fails, try updating `pip`:
```sh
pip install --upgrade pip
```

<br></br>

## **License**
This project is for educational purposes only.