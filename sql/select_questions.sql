SELECT question_id, title
FROM questions
ORDER BY question_id DESC;

SELECT question_id, title, message_id
FROM questions
NATURAL JOIN question_have_message;
