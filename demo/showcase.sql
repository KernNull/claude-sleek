-- Survey report, used to show off SQL colors.
CREATE TABLE IF NOT EXISTS answers (
    id          INTEGER PRIMARY KEY,
    survey_id   INTEGER NOT NULL REFERENCES surveys (id),
    body        TEXT    NOT NULL,
    score       REAL    CHECK (score BETWEEN 0 AND 1),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT s.title,
       COUNT(a.id)         AS answers,
       ROUND(AVG(a.score), 2) AS average
FROM surveys AS s
LEFT JOIN answers AS a ON a.survey_id = s.id
WHERE s.created_at >= '2026-01-01'
  AND a.body LIKE '%warm%'
GROUP BY s.title
HAVING COUNT(a.id) > 5
ORDER BY average DESC
LIMIT 10;
