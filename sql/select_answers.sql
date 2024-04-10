SELECT message_id, text, firstname, lastname, create_date,
    COALESCE(name, '')
FROM messages
NATURAL JOIN message_answer_question
NATURAL JOIN people
NATURAL LEFT JOIN person_belong_group
NATURAL LEFT JOIN authorization_groups
WHERE question_id = ?;

SELECT message_id, text, firstname, lastname, create_date,
    COALESCE(GROUP_CONCAT(name), '') AS 'group'
FROM messages
NATURAL JOIN message_answer_question
NATURAL JOIN people
NATURAL LEFT JOIN person_belong_group
NATURAL LEFT JOIN authorization_groups
WHERE question_id=?
GROUP BY message_id, text, firstname, lastname, create_date;
