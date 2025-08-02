import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from backend.db_manager import DBManager

st.set_page_config(page_title="Placement Eligibility Dashboard", layout="wide")

# Title
st.title("🎓 Placement Eligibility Streamlit Application")

# Create DBManager instance
db = DBManager()

# Sidebar - Eligibility Criteria
st.sidebar.header("📋 Filter Criteria")
min_problems = st.sidebar.slider("Minimum Problems Solved", 0, 100, 50)
min_soft_skill = st.sidebar.slider("Minimum Average Soft Skill Score", 0, 100, 75)

# Fetch eligible students
st.subheader("✅ Eligible Students")
df_eligible = db.fetch_eligible_students(min_problems, min_soft_skill)
st.dataframe(df_eligible)

# Insights Section
st.subheader("📊 Placement Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Top 5 Students Ready for Placement**")
    st.dataframe(db.get_top_5_students())

with col2:
    st.markdown("**Average Programming Performance by Batch**")
    st.dataframe(db.get_avg_programming_by_batch())

# Optional: Show soft skill score distribution
with st.expander("📈 Show Soft Skills Distribution"):
    st.dataframe(db.get_soft_skills_distribution())

# Close DB connection
db.close_connection()
