SELECT is_upvote
FROM person_vote_message
WHERE  (message_id=?) AND (person_id=?);
