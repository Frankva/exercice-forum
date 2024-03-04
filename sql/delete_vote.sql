DELETE
FROM person_vote_message
WHERE (person_id=?) AND (message_id=?);

DELETE
FROM person_vote_message
WHERE (person_id=1) AND (message_id=1);
