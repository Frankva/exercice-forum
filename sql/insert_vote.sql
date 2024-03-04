INSERT person_vote_message (is_upvote, person_id, message_id)
VALUES
(?, ?, ?)
ON DUPLICATE KEY UPDATE
is_upvote=VALUES(is_vote);

