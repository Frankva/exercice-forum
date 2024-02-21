SELECT text, firstname, lastname, create_date
FROM messages
NATURAL JOIN message_answer_question
NATURAL JOIN people
WHERE question_id = ?;
