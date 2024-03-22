SELECT question_id, title
FROM questions
NATURAL JOIN question_have_tag
NATURAL JOIN tags
WHERE name=?;
