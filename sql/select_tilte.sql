SELECT question_id, title
FROM questions
NATURAL JOIN question_have_message
NATURAL JOIN messages
WHERE person_id=?;
