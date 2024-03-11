SELECT person_id
FROM emails
NATURAL JOIN people
NATURAL JOIN passwords
WHERE (text=?) AND (hash=sha2(?, 512));
