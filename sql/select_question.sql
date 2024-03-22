SELECT title, text, firstname, lastname, create_date,
    message_id, name
FROM questions
NATURAL JOIN people
NATURAL JOIN question_have_message
NATURAL JOIN messages
NATURAL JOIN person_belong_group
NATURAL JOIN authorization_groups
WHERE question_id=?;
