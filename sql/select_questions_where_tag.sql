SELECT question_id, title
FROM questions
NATURAL JOIN question_have_tag
NATURAL JOIN tags
WHERE name=?
ORDER BY question_id DESC;

SELECT question_id, title, message_id
FROM questions
NATURAL JOIN question_have_tag
NATURAL JOIN tags
NATURAL JOIN question_have_message
WHERE name=?;
