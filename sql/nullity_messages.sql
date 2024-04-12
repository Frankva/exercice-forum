select *
from messages
where message_id=?

UPDATE messages SET text = NULL
WHERE message_id = ?;
