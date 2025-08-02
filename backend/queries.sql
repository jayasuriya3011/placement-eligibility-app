-- 1. Average programming performance per batch
SELECT course_batch, AVG(problems_solved) AS avg_problems
FROM Students s
JOIN Programming p ON s.student_id = p.student_id
GROUP BY course_batch;

-- 2. Top 5 students by problems solved
SELECT s.name, p.problems_solved
FROM Students s
JOIN Programming p ON s.student_id = p.student_id
ORDER BY problems_solved DESC
LIMIT 5;

-- 3. Students who are "Ready" for placement
SELECT s.name, pl.placement_status
FROM Students s
JOIN Placements pl ON s.student_id = pl.student_id
WHERE placement_status = 'Ready';

-- 4. Students placed with package > 10 LPA
SELECT s.name, pl.company_name, pl.placement_package
FROM Students s
JOIN Placements pl ON s.student_id = pl.student_id
WHERE pl.placement_package > 10;

-- 5. Batch-wise average soft skills
SELECT s.course_batch, AVG((ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills)/6) AS avg_soft_skills
FROM Students s
JOIN SoftSkills ss ON s.student_id = ss.student_id
GROUP BY s.course_batch;

-- 6. Students with more than 1 internship
SELECT s.name, pl.internships_completed
FROM Students s
JOIN Placements pl ON s.student_id = pl.student_id
WHERE pl.internships_completed > 1;

-- 7. Number of students placed in each company
SELECT company_name, COUNT(*) AS total_placed
FROM Placements
WHERE placement_status = 'Placed'
GROUP BY company_name;

-- 8. Students who solved < 40 problems and not ready
SELECT s.name, p.problems_solved, pl.placement_status
FROM Students s
JOIN Programming p ON s.student_id = p.student_id
JOIN Placements pl ON s.student_id = pl.student_id
WHERE p.problems_solved < 40 AND pl.placement_status != 'Ready';

-- 9. Average mock interview score by city
SELECT city, AVG(pl.mock_interview_score) AS avg_mock_score
FROM Students s
JOIN Placements pl ON s.student_id = pl.student_id
GROUP BY city;

-- 10. Top 5 cities with most placed students
SELECT city, COUNT(*) AS placed_count
FROM Students s
JOIN Placements pl ON s.student_id = pl.student_id
WHERE placement_status = 'Placed'
GROUP BY city
ORDER BY placed_count DESC
LIMIT 5;
