SELECT message_id, text, firstname, lastname, create_date, name
FROM messages
NATURAL JOIN message_answer_question
NATURAL JOIN people
NATURAL JOIN person_belong_group
NATURAL JOIN authorization_groups
WHERE question_id = ?;
