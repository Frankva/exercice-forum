SELECT title, text, firstname, lastname, create_date
FROM questions
NATURAL JOIN people
NATURAL JOIN question_have_message
NATURAL JOIN messages
WHERE question_id=?;
