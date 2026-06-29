# 🏥 Health Prediction Application 
(https://health-prediction-app-kcsrrvkgpgjzpyzcpqqecc.streamlit.app/)

A beginner-friendly web application for managing patient health records and predicting health risks using AI/ML. Built with **Streamlit** (frontend) and **Python** (backend) with **SQLite** database.

---

## 📋 Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Installation Guide](#installation-guide)
4. [How to Run](#how-to-run)
5. [Application Features Explained](#application-features-explained)
6. [Code Explanations](#code-explanations)
7. [Database Schema](#database-schema)
8. [API Integration](#api-integration)
9. [Troubleshooting](#troubleshooting)

---

## ✨ Features

✅ **CRUD Operations** - Create, Read, Update, Delete patient records
✅ **Patient Management** - Store patient information (Name, DOB, Email, etc.)
✅ **Blood Test Tracking** - Record Glucose, Hemoglobin, Cholesterol levels
✅ **AI Health Predictions** - Automatic health risk assessment
✅ **Data Validation** - Email, date, and value validation
✅ **Persistent Storage** - SQLite database
✅ **Beautiful UI** - Modern, responsive Streamlit interface
✅ **Search & Filter** - Find patients by name or email
✅ **Dashboard** - Overview of all patient records
✅ **Health Metrics** - Visual display of patient health data

---

## 📁 Project Structure

```
health-prediction-app/
│
├── app.py                      # Main Streamlit application (Frontend UI)
├── database.py                 # Database operations (CRUD)
├── health_predictor.py         # AI/ML health prediction logic
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
└── patients.db                 # SQLite database (created automatically)
```

### File Descriptions:

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit UI with all pages (Dashboard, Add, View, Update, Delete) |
| `database.py` | SQLite database operations - handles all data persistence |
| `health_predictor.py` | Health prediction logic using medical guidelines and optional APIs |
| `requirements.txt` | List of required Python packages |
| `patients.db` | SQLite database file (auto-generated on first run) |

---

## 🚀 Installation Guide

### Prerequisites

- **Python 3.8+** installed on your computer
- **pip** (Python package manager) - usually comes with Python
- A code editor (VS Code, PyCharm, or any text editor)

### Step-by-Step Installation

#### 1. **Check Python Installation**

Open Command Prompt (Windows) or Terminal (Mac/Linux) and run:

```bash
python --version
pip --version
```

You should see version numbers like `Python 3.10.x` and `pip 23.x.x`

#### 2. **Create a Project Folder**

```bash
# Create a new folder
mkdir health-prediction-app
cd health-prediction-app
```

#### 3. **Create a Virtual Environment** (Recommended)

A virtual environment keeps your project dependencies separate from your system Python.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

#### 4. **Install Required Dependencies**

Copy all three Python files (`app.py`, `database.py`, `health_predictor.py`) and the `requirements.txt` file into your project folder.

Then install dependencies:

```bash
pip install -r requirements.txt
```

This will install:
- **streamlit** - Web framework for UI
- **pandas** - Data manipulation and display
- **requests** - For API calls (if using external APIs)
- **python-dateutil** - Date utilities

---

## ▶️ How to Run

### 1. **Navigate to Project Directory**

```bash
cd health-prediction-app
```

### 2. **Activate Virtual Environment** (if created)

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. **Run the Streamlit App**

```bash
streamlit run app.py
```

### 4. **Access the Application**

Your browser should automatically open to:
```
http://localhost:8501
```

If not, manually open this URL in your browser.

### 5. **Stop the Application**

Press `Ctrl+C` in the terminal to stop the server.

---

## 📖 Application Features Explained

### 1. **📊 Dashboard Page**

**What it does:**
- Shows overview statistics (total patients, high glucose count, etc.)
- Displays all patient records in a table
- Provides quick health metrics at a glance

**Key Elements:**
- **Total Patients Card** - Count of all registered patients
- **High Glucose Count** - Patients with glucose > 126 mg/dL
- **High Cholesterol** - Patients with cholesterol > 200 mg/dL
- **Low Hemoglobin** - Patients with hemoglobin < 12 g/dL
- **Patient Table** - Complete list with all metrics and remarks

### 2. **➕ Add Patient Page**

**What it does:**
- Create new patient records
- Collects patient information and health metrics
- Automatically generates AI health predictions

**Input Fields:**
```
├── Full Name (text) - Patient's complete name
├── Date of Birth (date picker) - Cannot be future date
├── Email (email) - Must be valid format (example@email.com)
├── Glucose Level (number) - In mg/dL (0-500)
├── Hemoglobin (number) - In g/dL (0-20)
└── Cholesterol (number) - In mg/dL (0-500)
```

**Validation Checks:**
- ✅ Name must be at least 2 characters
- ✅ Valid email format required
- ✅ DOB cannot be future date
- ✅ All blood values must be greater than 0
- ✅ Values within reasonable medical ranges

**After Submission:**
- Data is validated
- AI health prediction is generated
- Record is saved to database
- Success message is displayed

### 3. **👁️ View Patients Page**

**What it does:**
- Display all patient records
- Search patients by name or email
- View detailed patient information

**Features:**
- **Search Bar** - Type to filter patients
- **Patient Table** - Shows all records with health metrics
- **Detailed View** - Click dropdown to see full patient details
- **Age Calculation** - Automatically calculates age from DOB

### 4. **✏️ Update Patient Page**

**What it does:**
- Modify existing patient records
- Update blood test values
- Regenerate health predictions

**Process:**
1. Select patient from dropdown
2. Update any field
3. Submit to save changes
4. AI prediction is recalculated

### 5. **🗑️ Delete Patient Page**

**What it does:**
- Remove patient records from database
- Shows warning before deletion

**Safety Features:**
- ⚠️ Warning message displayed
- Patient details shown before deletion
- Confirmation required to delete
- Cannot be undone

---

## 💻 Code Explanations

### **app.py - Main Application**

#### Page Configuration
```python
st.set_page_config(
    page_title="Health Prediction App",
    page_icon="🏥",
    layout="wide"
)
```
This sets up the Streamlit page with title, icon, and layout.

#### Navigation Menu
```python
page = st.sidebar.radio(
    "Select Operation",
    ["📊 Dashboard", "➕ Add Patient", ...]
)
```
Creates radio buttons in the sidebar for navigation.

#### Form Input
```python
full_name = st.text_input(
    "Full Name *",
    placeholder="Enter patient's full name",
    help="Patient's complete name"
)
```
Creates a text input field with help text.

#### Data Validation Example
```python
if not full_name or len(full_name.strip()) < 2:
    errors.append("❌ Full name must be at least 2 characters")
```
Checks if name is valid before submission.

---

### **database.py - Database Operations**

#### Database Connection
```python
def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn
```
Creates and returns a connection to SQLite database.

#### Create Table
```python
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        ...
    )
''')
```
Creates the `patients` table if it doesn't exist.

#### Add Patient
```python
cursor.execute('''
    INSERT INTO patients 
    (full_name, date_of_birth, email, ..., remarks)
    VALUES (?, ?, ?, ..., ?)
''', (full_name, dob, email, ...))
```
Inserts a new patient record with parameterized queries (safe from SQL injection).

#### Retrieve Patients
```python
cursor.execute('''
    SELECT * FROM patients 
    WHERE id = ?
''', (patient_id,))
patient = cursor.fetchone()
```
Retrieves patient data safely.

---

### **health_predictor.py - AI/ML Logic**

#### Main Prediction Function
```python
def predict_health_status(glucose, haemoglobin, cholesterol):
    # Try API first
    api_prediction = predict_with_api(...)
    if api_prediction:
        return api_prediction
    
    # Fall back to rule-based
    return predict_with_rules(...)
```
Uses API if available, otherwise uses built-in rules.

#### Rule-Based Prediction
```python
if glucose >= 70 and glucose <= 100:
    risk_factors.append("Normal glucose levels")
    recommendations.append("✅ Glucose levels are healthy")
elif glucose > 100 and glucose <= 125:
    risk_level = "MEDIUM"
    risk_factors.append("Prediabetes")
    recommendations.append("⚠️ Reduce sugar intake")
```
Checks glucose value against medical guidelines and generates recommendations.

#### Health Score Calculation
```python
def calculate_health_score(glucose, haemoglobin, cholesterol):
    score = 100
    
    if 70 <= glucose <= 100:
        score -= 0  # Good
    elif glucose > 125:
        score -= 30  # Bad
    
    return max(0, score)
```
Calculates overall health from 0-100.

---

## 🗄️ Database Schema

### Patients Table

```sql
CREATE TABLE patients (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name         TEXT NOT NULL,
    date_of_birth     TEXT NOT NULL,
    email             TEXT NOT NULL UNIQUE,
    glucose           REAL NOT NULL,
    haemoglobin        REAL NOT NULL,
    cholesterol       REAL NOT NULL,
    remarks           TEXT,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Column Descriptions

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Unique patient ID (auto-generated) |
| `full_name` | TEXT | Patient's complete name |
| `date_of_birth` | TEXT | DOB in YYYY-MM-DD format |
| `email` | TEXT | Patient's email (unique) |
| `glucose` | REAL | Blood glucose in mg/dL |
| `hemoglobin` | REAL | Hemoglobin level in g/dL |
| `cholesterol` | REAL | Cholesterol level in mg/dL |
| `remarks` | TEXT | AI-generated health prediction |
| `created_at` | TIMESTAMP | When record was created |
| `updated_at` | TIMESTAMP | When record was last updated |

---

## 🔌 API Integration

### Current Implementation

The application uses **rule-based prediction** by default, which doesn't require external APIs.

### Optional: Adding External API

If you want to use an external health prediction API, uncomment the code in `health_predictor.py`:

#### Example 1: Hugging Face API

```python
API_URL = "https://api-inference.huggingface.co/models/medical-model"
headers = {"Authorization": f"Bearer YOUR_API_KEY"}

response = requests.post(API_URL, headers=headers, json=payload)
```

**Steps:**
1. Get API key from [Hugging Face](https://huggingface.co/)
2. Replace `YOUR_API_KEY` with your actual key
3. Uncomment the code in `health_predictor.py`

#### Example 2: Custom ML Model Endpoint

```python
response = requests.post(
    'http://localhost:5000/predict',
    json={'glucose': glucose, 'hemoglobin': hemoglobin, 'cholesterol': cholesterol}
)
```

**Requirements:**
- Flask/FastAPI server running on port 5000
- Endpoint should accept and return JSON

---

## 📊 Medical Reference Ranges

### Glucose (Fasting)
- **Normal:** 70-100 mg/dL
- **Prediabetic:** 100-125 mg/dL
- **Diabetic:** > 125 mg/dL

### Hemoglobin
- **Normal (Male):** 13.5-17.5 g/dL
- **Normal (Female):** 12.0-15.5 g/dL
- **Anemia:** < 12 g/dL

### Cholesterol
- **Desirable:** < 200 mg/dL
- **Borderline:** 200-239 mg/dL
- **High Risk:** ≥ 240 mg/dL

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: "Address already in use" error

**Solution:**
The port 8501 is already in use. Stop other Streamlit apps or use:
```bash
streamlit run app.py --server.port 8502
```

### Problem: Database file keeps resetting

**Solution:**
Make sure `patients.db` is in the same folder as your Python files. SQLite will create it automatically.

### Problem: Email already exists error

**Solution:**
Email addresses must be unique. Use a different email address or delete the previous record.

### Problem: Date of Birth validation fails

**Solution:**
- Use format: YYYY-MM-DD (e.g., 2000-05-15)
- DOB cannot be today or in the future
- Check that the date is valid

### Problem: Streamlit keeps rerunning

**Solution:**
This is normal Streamlit behavior. To avoid rerunning, use:
```python
@st.cache_data
def load_data():
    ...
```

---

## 🎨 Customization Guide

### Change App Title
In `app.py`, modify:
```python
st.set_page_config(page_title="Your Title Here")
```

### Change Colors
Update CSS in `app.py`:
```python
st.markdown("""
    <style>
    .header-container {
        background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
    }
    </style>
""", unsafe_allow_html=True)
```

### Add New Fields
In `database.py`:
1. Add column to CREATE TABLE
2. Update INSERT statement
3. Update all SELECT statements

In `app.py`:
1. Add input field to form
2. Add validation logic
3. Pass to database function

---

## 📚 Learning Resources

### Python Basics
- [Python Official Documentation](https://docs.python.org/3/)
- [Real Python Tutorials](https://realpython.com/)

### SQLite
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)

### Streamlit
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit API Reference](https://docs.streamlit.io/library/api-reference)

### Health Metrics
- [WebMD Health Reference](https://www.webmd.com/)
- [Mayo Clinic Lab Tests](https://www.mayoclinic.org/)

---

## 🤝 Contributing

Want to improve this app? Here are some ideas:

1. **Add Export Feature** - Export patient data to CSV/PDF
2. **Add Charts** - Visualize patient health trends over time
3. **Add Notifications** - Alert when metrics are abnormal
4. **Add Multi-User** - User accounts and role-based access
5. **Add Mobile App** - React Native or Flutter frontend
6. **Add Reports** - Generate health reports for doctors

---

## 📄 License

This project is open-source and available for educational purposes.

---

## 📧 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the code comments
3. Check Streamlit and SQLite documentation

---

**Happy Coding! 🚀**
