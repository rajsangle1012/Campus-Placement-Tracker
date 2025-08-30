import streamlit as st
from db.db_connection import get_connection

st.set_page_config(page_title="Placement Eligibility App", layout="wide")
st.title("Placement Eligibility App")

# Sidebar Menu
menu = st.sidebar.radio("Menu", ["Eligibility Checker", "Insights Dashboard"])

conn = get_connection()
cursor = conn.cursor()

# ------------------ ELIGIBILITY CHECKER -------------------
if menu == "Eligibility Checker":
    st.subheader("Check Eligible Students")
    
    if st.button("Show All Students"):
        cursor.execute("SELECT * FROM tbl_students")
        rows = cursor.fetchall()
        st.dataframe([dict(row) for row in rows])
    
    st.markdown("#### Advanced Filters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age_range = st.slider("Age Range", 18, 25, (20, 22))
        gender_filter = st.multiselect(
            "Gender",
            options=['Male', 'Female'],
            default=['Male', 'Female']
        )
        cursor.execute("SELECT DISTINCT city FROM tbl_students")
        cities = [row['city'] for row in cursor.fetchall()]
        city_filter = st.multiselect("City", options=cities)
        
    with col2:
        batch_filter = st.multiselect(
            "Batch",
            options=['Batch-1', 'Batch-2', 'Batch-3', 'Batch-4', 'Batch-5'],
            default=['Batch-1', 'Batch-2', 'Batch-3', 'Batch-4', 'Batch-5']
        )
        grad_year_filter = st.multiselect(
            "Graduation Year",
            options=[2023, 2024, 2025, 2026, 2027],
            default=[2023, 2024, 2025, 2026, 2027]
        )
        problems_solved = st.slider(
            "Minimum Problems Solved", 
            min_value=0, 
            max_value=200, 
            value=50
        )
    
    placement_filter = st.selectbox(
        "Placement Status",
        options=["All", "Placed", "Ready", "Not Ready"]
    )
    
    if st.button("Apply Filters"):
        query = """
            SELECT s.*, p.placement_status, pr.problems_solved
            FROM tbl_students s
            LEFT JOIN tbl_placements p ON s.student_id = p.student_id
            LEFT JOIN tbl_programming pr ON s.student_id = pr.student_id
            WHERE 1=1
        """
        
        params = []
        query += " AND s.age BETWEEN ? AND ?"
        params.extend([age_range[0], age_range[1]])
        
        if gender_filter:
            query += " AND s.gender IN ({})".format(",".join(["?"]*len(gender_filter)))
            params.extend(gender_filter)
        
        if city_filter:
            query += " AND s.city IN ({})".format(",".join(["?"]*len(city_filter)))
            params.extend(city_filter)
        
        if batch_filter:
            query += " AND s.course_batch IN ({})".format(",".join(["?"]*len(batch_filter)))
            params.extend(batch_filter)
        
        if grad_year_filter:
            query += " AND s.graduation_year IN ({})".format(",".join(["?"]*len(grad_year_filter)))
            params.extend(grad_year_filter)
        
        query += " AND pr.problems_solved >= ?"
        params.append(problems_solved)
        
        if placement_filter != "All":
            query += " AND p.placement_status = ?"
            params.append(placement_filter)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        if rows:
            st.dataframe([dict(row) for row in rows])
            st.success(f"Found {len(rows)} students matching your criteria")
        else:
            st.warning("No students found matching your criteria")

# ------------------ INSIGHTS DASHBOARD -------------------
elif menu == "Insights Dashboard":
    st.subheader("Placement Statistics")
    
    # Question 1: Total placed students
    st.markdown("### 1. No. of students who get placed?")
    cursor.execute("""
        SELECT COUNT(*) as placed_count 
        FROM tbl_placements 
        WHERE placement_status = 'Placed'
    """)
    placed_count = cursor.fetchone()['placed_count']
    cursor.execute("SELECT COUNT(*) as total FROM tbl_students")
    total_count = cursor.fetchone()['total']
    st.info(f"Total students: {total_count}")
    st.info(f"Placed students: {placed_count} ({placed_count/total_count*100:.1f}%)")
    
    # Question 2: Placement by gender
    st.markdown("### 2.  placement status accordinng to gender?")
    cursor.execute("""
        SELECT 
            s.gender,
            COUNT(CASE WHEN p.placement_status = 'Placed' THEN 1 END) as placed,
            COUNT(*) as total,
            COUNT(CASE WHEN p.placement_status = 'Placed' THEN 1 END)*100.0/COUNT(*) as percentage
        FROM tbl_students s
        JOIN tbl_placements p ON s.student_id = p.student_id
        GROUP BY s.gender
    """)
    gender_data = cursor.fetchall()
    st.table([dict(row) for row in gender_data])
    
    # Question 3: Top programming languages
    st.markdown("### 3. most popular programming languages?")
    cursor.execute("""
        SELECT language, COUNT(*) as count 
        FROM tbl_programming 
        GROUP BY language 
        ORDER BY count DESC
    """)
    lang_data = cursor.fetchall()
    st.bar_chart({row['language']: row['count'] for row in lang_data})
    
    # Question 4: Average package by language
    st.markdown("### 4.average package according to Programming language?")
    cursor.execute("""
        SELECT pr.language, AVG(pl.placement_package) as avg_package
        FROM tbl_programming pr
        JOIN tbl_placements pl ON pr.student_id = pl.student_id
        WHERE pl.placement_status = 'Placed'
        GROUP BY pr.language
        ORDER BY avg_package DESC
    """)
    lang_pkg_data = cursor.fetchall()
    st.table([dict(row) for row in lang_pkg_data])
    
    # Question 5: City-wise placement
    st.markdown("### 5.  most placed student according to city?")
    cursor.execute("""
        SELECT s.city, COUNT(*) as placements
        FROM tbl_placements p
        JOIN tbl_students s ON p.student_id = s.student_id
        WHERE p.placement_status = 'Placed'
        GROUP BY s.city
        ORDER BY placements DESC
        LIMIT 5
    """)
    city_data = cursor.fetchall()
    st.table([dict(row) for row in city_data])
    
    # Question 6: Problems solved vs placement
    st.markdown("### 6. Problems solved and placement ka relation?")
    cursor.execute("""
        SELECT 
            CASE 
                WHEN pr.problems_solved >= 100 THEN '100+'
                WHEN pr.problems_solved >= 50 THEN '50-99'
                ELSE '0-49'
            END as problem_range,
            COUNT(CASE WHEN p.placement_status = 'Placed' THEN 1 END) as placed,
            COUNT(*) as total,
            AVG(p.placement_package) as avg_package
        FROM tbl_programming pr
        JOIN tbl_placements p ON pr.student_id = p.student_id
        GROUP BY problem_range
        ORDER BY problem_range
    """)
    problem_data = cursor.fetchall()
    st.table([dict(row) for row in problem_data])
    
    # Question 7: Top students by project score
    st.markdown("### 7. Top 5 students by project score?")
    cursor.execute("""
        SELECT s.name, pr.latest_project_score
        FROM tbl_programming pr
        JOIN tbl_students s ON pr.student_id = s.student_id
        ORDER BY pr.latest_project_score DESC
        LIMIT 5
    """)
    top_students = cursor.fetchall()
    st.table([dict(row) for row in top_students])
    
    # Question 8: Internships vs placement
    st.markdown("### 8. Internships and placement  relation?")
    cursor.execute("""
        SELECT 
            internships_completed,
            COUNT(CASE WHEN placement_status = 'Placed' THEN 1 END) as placed,
            COUNT(*) as total
        FROM tbl_placements
        GROUP BY internships_completed
        ORDER BY internships_completed
    """)
    internship_data = cursor.fetchall()
    st.table([dict(row) for row in internship_data])
    
    # Question 9: Soft skills comparison
    st.markdown("### 9. Placed vs non-placed students  soft skills?")
    cursor.execute("""
        SELECT 
            p.placement_status,
            AVG(s.communication) as avg_communication,
            AVG(s.teamwork) as avg_teamwork,
            AVG(s.presentation) as avg_presentation
        FROM tbl_softskills s
        JOIN tbl_placements p ON s.student_id = p.student_id
        GROUP BY p.placement_status
    """)
    skill_data = cursor.fetchall()
    st.table([dict(row) for row in skill_data])
    
    # Question 10: Batch-wise performance
    st.markdown("### 10.placement status according to batch ?")
    cursor.execute("""
        SELECT 
            s.course_batch,
            COUNT(CASE WHEN p.placement_status = 'Placed' THEN 1 END) as placed,
            COUNT(*) as total,
            AVG(p.placement_package) as avg_package
        FROM tbl_students s
        JOIN tbl_placements p ON s.student_id = p.student_id
        GROUP BY s.course_batch
        ORDER BY s.course_batch
    """)
    batch_data = cursor.fetchall()
    st.table([dict(row) for row in batch_data])

conn.close()