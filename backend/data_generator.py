from faker import Faker
import random
import sqlite3

fake = Faker()
conn = sqlite3.connect("placement.db")
cursor = conn.cursor()

# Drop existing tables to avoid duplicates
cursor.executescript("""
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Programming;
DROP TABLE IF EXISTS SoftSkills;
DROP TABLE IF EXISTS Placements;
""")

# Create tables
cursor.executescript("""
CREATE TABLE Students (
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
);

CREATE TABLE Programming (
    programming_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    language TEXT,
    problems_solved INTEGER,
    assessments_completed INTEGER,
    mini_projects INTEGER,
    certifications_earned INTEGER,
    latest_project_score INTEGER,
    FOREIGN KEY(student_id) REFERENCES Students(student_id)
);

CREATE TABLE SoftSkills (
    soft_skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    communication INTEGER,
    teamwork INTEGER,
    presentation INTEGER,
    leadership INTEGER,
    critical_thinking INTEGER,
    interpersonal_skills INTEGER,
    FOREIGN KEY(student_id) REFERENCES Students(student_id)
);

CREATE TABLE Placements (
    placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    mock_interview_score INTEGER,
    internships_completed INTEGER,
    placement_status TEXT,
    company_name TEXT,
    placement_package REAL,
    interview_rounds_cleared INTEGER,
    placement_date TEXT,
    FOREIGN KEY(student_id) REFERENCES Students(student_id)
);
""")

# Insert 100 students
def generate_students(n=100):
    for _ in range(n):
        name = fake.name()
        age = random.randint(20, 26)
        gender = random.choice(["Male", "Female", "Other"])
        email = fake.email()
        phone = fake.phone_number()
        enrollment_year = random.choice([2021, 2022])
        course_batch = f"Batch-{random.randint(1, 5)}"
        city = fake.city()
        graduation_year = enrollment_year + 3

        cursor.execute("""
            INSERT INTO Students (name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year))

generate_students()

# Get list of all student_ids
student_ids = [row[0] for row in cursor.execute("SELECT student_id FROM Students")]

# Insert data into other 3 tables
for sid in student_ids:
    # Programming
    cursor.execute("""
        INSERT INTO Programming (student_id, language, problems_solved, assessments_completed, mini_projects, certifications_earned, latest_project_score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        sid, "Python", random.randint(30, 100),
        random.randint(2, 10), random.randint(1, 5),
        random.randint(0, 3), random.randint(50, 100)
    ))

    # Soft Skills
    cursor.execute("""
        INSERT INTO SoftSkills (student_id, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        sid, random.randint(60, 100), random.randint(60, 100),
        random.randint(60, 100), random.randint(60, 100),
        random.randint(60, 100), random.randint(60, 100)
    ))

    # Placement
    status = random.choice(["Ready", "Not Ready", "Placed"])
    company = fake.company() if status == "Placed" else None
    package = round(random.uniform(4, 15), 2) if status == "Placed" else None
    date = fake.date_this_year()
    cursor.execute("""
        INSERT INTO Placements (student_id, mock_interview_score, internships_completed, placement_status, company_name, placement_package, interview_rounds_cleared, placement_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        sid, random.randint(60, 100), random.randint(0, 2),
        status, company, package, random.randint(1, 5), date
    ))

conn.commit()
conn.close()

print("✅ Data generation complete! Database saved as placement.db")
