from db_connection import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Students table (SQLite compatible)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            email TEXT,
            phone TEXT,
            enrollment_year INTEGER,
            course_batch TEXT,
            city TEXT,
            graduation_year INTEGER
        )
    """)

    # 2. Programming table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_programming (
            programming_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            language TEXT,
            problems_solved INTEGER,
            assessments_completed INTEGER,
            mini_projects INTEGER,
            certifications_earned INTEGER,
            latest_project_score INTEGER,
            FOREIGN KEY (student_id) REFERENCES tbl_students(student_id)
        )
    """)

    # 3. Soft skills table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_softskills (
            soft_skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            communication INTEGER,
            teamwork INTEGER,
            presentation INTEGER,
            leadership INTEGER,
            critical_thinking INTEGER,
            interpersonal_skills INTEGER,
            FOREIGN KEY (student_id) REFERENCES tbl_students(student_id)
        )
    """)

    # 4. Placements table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_placements (
            placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            mock_interview_score INTEGER,
            internships_completed INTEGER,
            placement_status TEXT,
            company_name TEXT,
            placement_package REAL,
            interview_rounds_cleared INTEGER,
            placement_date TEXT,
            FOREIGN KEY (student_id) REFERENCES tbl_students(student_id)
        )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully in SQLite database!")

if __name__ == "__main__":
    create_tables()