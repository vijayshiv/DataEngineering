DELETE FROM applications WHERE candidate_id IN (
		SELECT candidate_id FROM(
		SELECT *, ROW_NUMBER() OVER(PARTITION BY candidate_id, skills ORDER BY candidate_id) AS rownumber
		FROM applications) x
		WHERE x.rownumber > 1);	

SELECT candidate_id, COUNT(skills) as skillcount
FROM applications
WHERE skills IN ('Python', 'SQL', 'Power BI')
GROUP BY candidate_id
HAVING COUNT(skills) = 3
ORDER BY candidate_id