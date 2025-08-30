from faker import Faker
import random
from datetime import datetime
from db_connection import get_connection

fake = Faker()

# tbl_students table mein fake student data daalna
def insert_fake_students(n=10):
    conn = get_connection()
    cursor = conn.cursor()

    for _ in range(n):
        name = fake.name()
        age = random.randint(18, 25)
        gender = random.choice(['Male', 'Female'])
        email = fake.email()
        phone = fake.msisdn()[:15]
        enroll_year = random.randint(2019, 2023)
        batch = f"Batch-{random.randint(1, 5)}"
        city = fake.city()
        grad_year = enroll_year + 4

        cursor.execute("""
            INSERT INTO tbl_students (name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, age, gender, email, phone, enroll_year, batch, city, grad_year))

    conn.commit()
    conn.close()
    print("Students data inserted")

# tbl_programming table mein data daalna
def insert_fake_programming():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT student_id FROM tbl_students LIMIT 10") 
    student_ids = cursor.fetchall()

    for student_id in student_ids:
        cursor.execute("""
            INSERT INTO tbl_programming (student_id, language, problems_solved, assessments_completed, mini_projects, certifications_earned, latest_project_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id['student_id'],
            random.choice(['Python', 'JavaScript', 'SQL']),
            random.randint(10, 200),
            random.randint(1, 10),
            random.randint(0, 5),
            random.randint(0, 3),
            random.randint(40, 100)
        ))

    conn.commit()
    conn.close()
    print("Programming data inserted")

# tbl_softskills table mein soft skills data daalna
def insert_fake_soft_skills():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT student_id FROM tbl_students LIMIT 10")  
    student_ids = cursor.fetchall()

    for student_id in student_ids:
        cursor.execute("""
            INSERT INTO tbl_softskills (student_id, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id['student_id'],
            random.randint(50, 100),
            random.randint(50, 100),
            random.randint(50, 100),
            random.randint(50, 100),
            random.randint(50, 100),
            random.randint(50, 100)
        ))

    conn.commit()
    conn.close()
    print("Softskills data inserted")

# tbl_placements table mein placement info daalna
def insert_fake_placements():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT student_id FROM tbl_students LIMIT 10") 
    student_ids = cursor.fetchall()

    for student_id in student_ids:
        status = random.choice(['Ready', 'Not Ready', 'Placed'])
        company = fake.company() if status == 'Placed' else None
        package = round(random.uniform(4.0, 15.0), 2) if status == 'Placed' else None
        date = fake.date_this_decade().isoformat() if status == 'Placed' else None  # 👈 FIXED

        cursor.execute("""
            INSERT INTO tbl_placements (student_id, mock_interview_score, internships_completed, placement_status, company_name, placement_package, interview_rounds_cleared, placement_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id['student_id'],
            random.randint(50, 100),
            random.randint(0, 3),
            status,
            company,
            package,
            random.randint(0, 5),
            date
        ))

    conn.commit()
    conn.close()
    print("Placement data inserted")

if __name__ == "__main__":
    insert_fake_students(10)
    insert_fake_programming()
    insert_fake_soft_skills()
    insert_fake_placements()