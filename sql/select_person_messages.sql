SELECT message_id, text, create_date
FROM messages
NATURAL JOIN people
WHERE person_id=?
ORDER BY create_date DESC;
