SELECT title, text
FROM questions
NATURAL JOIN question_have_message
NATURAL JOIN messages;
