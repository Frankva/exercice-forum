SELECT title, text, firstname, lastname, create_date,
    message_id, name
FROM questions
NATURAL JOIN people
NATURAL JOIN question_have_message
NATURAL JOIN messages
NATURAL LEFT JOIN person_belong_group
NATURAL LEFT JOIN authorization_groups
WHERE question_id=?;
