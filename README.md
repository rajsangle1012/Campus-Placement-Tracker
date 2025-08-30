## 🎓 Placement Dashboard (Streamlit + SQLite)

This project is a **student placement tracking dashboard** built using **Python, Streamlit, and SQLite**. It includes functionalities like student data management, skill analysis, and placement insights.

## 🚀 Features

- Check eligibility of students by age and batch
- Programming skills tracking (language, problems solved, certifications)
- Soft skills evaluation (communication, teamwork, etc.)
- Placement tracking (status, company, package)
- Interactive Streamlit UI with sidebar navigation
- Data visualization and filtering capabilities
- Sample data generation using Faker library

## 🛠️ Tech Stack

- Python 
- Streamlit (for web interface)
- SQLite (database)
- Faker (for generating test data)
- python-dotenv (for environment variables)

## 🧾 How to Run this Project

- cd placement-eligibility-app
- pip install -r requirements.txt
- python db/create_tables.py
- python db/insert_fake_data.py

- streamlit run main.py
