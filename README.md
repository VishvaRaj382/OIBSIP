<<<<<<< HEAD
I have added specific README.md for specific project in respective project folder
=======
# Python Body Mass Index (BMI) Calculator & Health Tracker 🏋️‍♂️📊

A feature-rich Python application providing both a **Beginner Command-Line Interface (CLI)** and an **Advanced Desktop GUI Application (PyQt6)** with multi-user persistence, SQLite database, color-coded health indicators, and interactive Matplotlib trend visualization charts.

---

## 🌟 Features Breakdown

### 🟢 Beginner Tier Features
- **CLI Interface**: Interactive terminal prompt for weight (kg) and height (m or cm).
- **Exact BMI Calculation**: Uses standard formula $\text{BMI} = \frac{\text{weight (kg)}}{\text{height (m)}^2}$ rounded to 2 decimal places.
- **Health Classifications**:
  - **Underweight**: BMI < 18.5
  - **Normal Weight**: 18.5 – 24.9
  - **Overweight**: 25.0 – 29.9
  - **Obese**: BMI ≥ 30.0
- **Input Validation**: Rejects invalid strings, non-numeric values, negative numbers, and unrealistic zero/extreme inputs with helpful error messages.

### 🔵 Advanced Tier Features
- **Modern PyQt6 GUI**: Clean dark glassmorphism interface with custom styled widgets.
- **Color-Coded Feedback**: Dynamic card styling with custom color badges:
  - 🩵 Sky Blue: Underweight
  - 🟩 Emerald Green: Normal
  - 🟨 Amber Yellow: Overweight
  - 🟥 Coral Red: Obese
- **Multi-User Profiles**: Switch between different user profiles or create new profiles on the fly.
- **SQLite Database Persistence**: Full historical tracking stored in `bmi_tracker.db` with database error handling.
- **Matplotlib Trend Charts**: Interactive line graph showing weight and BMI progress over time, complete with highlighted normal weight reference zone (18.5 - 24.9).
- **History Log Management**: Tabular view of all previous measurements with row selection and record deletion.

---

## 🚀 Quickstart Guide

### 1. Prerequisites & Virtual Environment Setup
Ensure Python 3.9+ is installed. Activate the provided virtual environment or create one:

```bash
# Navigate to workspace
cd Python-Task2-BMI-Calculator

# Activate virtual environment
source .venv/bin/activate  # macOS / Linux
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

---

### 2. Launching the Application

#### 🖥️ Launch Advanced GUI Application (Default)
```bash
python main.py
```
*or directly:*
```bash
python gui.py
```

#### 💻 Launch Beginner CLI Tool
```bash
python main.py --cli
```
*or directly:*
```bash
python bmi_cli.py
```

---

## 🧪 Project Structure

```
Python-Task2-BMI-Calculator/
├── bmi_calculator.py   # Core logic: BMI calculations, classification, validation
├── database.py         # SQLite CRUD manager with error handling & multi-user support
├── bmi_cli.py          # Beginner Tier: Interactive Command-Line Interface
├── gui.py              # Advanced Tier: Modern PyQt6 GUI with Matplotlib trend chart
├── main.py             # Entry point launcher (GUI default, CLI via --cli)
├── requirements.txt    # Project dependencies (PyQt6, matplotlib)
└── README.md           # Documentation and guide
```

---

## 🔬 Unit & System Testing

Run Python automated checks:

```bash
# Test calculation logic and DB persistence
source .venv/bin/activate
python -c "
from bmi_calculator import calculate_bmi, classify_bmi, parse_and_validate_inputs
from database import DatabaseManager

# Test BMI formula
assert round(calculate_bmi(70, 1.75), 2) == 22.86
print('✅ BMI Calculation test passed!')

# Test Validation
w, h, err = parse_and_validate_inputs('-70', '1.75')
assert err is not None
print('✅ Input Validation test passed!')

# Test DB
db = DatabaseManager('test_bmi.db')
u = db.get_or_create_user('TestUser')
rec_id = db.add_bmi_record(u['id'], 70, 1.75, 22.86, 'Normal Weight')
assert rec_id > 0
print('✅ SQLite Database test passed!')
"
```

---

## 🛡️ License
Distributed under the MIT License.
>>>>>>> 47ddea2 (Add Python BMI Calculator & Health Analytics Suite (CLI + GUI))
