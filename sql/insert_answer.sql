INSERT messages (text)
VALUES
('a');

INSERT message_answer_question (message_id, question_id)
VALUES
((SELECT max(message_id)
    FROM messages), 1);



INSERT messages (text)
VALUES
(?);

INSERT message_answer_question (message_id, question_id)
VALUES
((SELECT max(message_id)
    FROM messages), ?);
