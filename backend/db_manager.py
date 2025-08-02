import sqlite3
import pandas as pd

class DBManager:
    def __init__(self, db_path="placement.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def fetch_eligible_students(self, min_problems=50, min_soft_skills=75):
        query = """
        SELECT s.student_id, s.name, s.course_batch, p.problems_solved,
               ss.communication, ss.teamwork, ss.presentation,
               pl.placement_status
        FROM Students s
        JOIN Programming p ON s.student_id = p.student_id
        JOIN SoftSkills ss ON s.student_id = ss.student_id
        JOIN Placements pl ON s.student_id = pl.student_id
        WHERE p.problems_solved >= ?
          AND ((ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills)/6) >= ?
        """
        df = pd.read_sql_query(query, self.conn, params=(min_problems, min_soft_skills))
        return df

    def run_query(self, sql_query):
        return pd.read_sql_query(sql_query, self.conn)

    def get_top_5_students(self):
        query = """
        SELECT s.name, p.problems_solved, ss.communication, pl.mock_interview_score
        FROM Students s
        JOIN Programming p ON s.student_id = p.student_id
        JOIN SoftSkills ss ON s.student_id = ss.student_id
        JOIN Placements pl ON s.student_id = pl.student_id
        ORDER BY p.problems_solved DESC, pl.mock_interview_score DESC
        LIMIT 5
        """
        return pd.read_sql_query(query, self.conn)

    def get_avg_programming_by_batch(self):
        query = """
        SELECT s.course_batch, AVG(p.problems_solved) AS avg_problems_solved
        FROM Students s
        JOIN Programming p ON s.student_id = p.student_id
        GROUP BY s.course_batch
        ORDER BY avg_problems_solved DESC
        """
        return pd.read_sql_query(query, self.conn)

    def get_soft_skills_distribution(self):
        query = """
        SELECT communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills
        FROM SoftSkills
        """
        return pd.read_sql_query(query, self.conn)

    def close_connection(self):
        self.conn.close()