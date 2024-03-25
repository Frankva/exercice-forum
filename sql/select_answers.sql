SELECT message_id, text, firstname, lastname, create_date,
    COALESCE(name, '')
FROM messages
NATURAL JOIN message_answer_question
NATURAL JOIN people
NATURAL LEFT JOIN person_belong_group
NATURAL LEFT JOIN authorization_groups
WHERE question_id = ?;
