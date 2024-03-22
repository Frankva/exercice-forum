use forum20240213;
start transaction;

INSERT INTO people (firstname, lastname)
VALUES
('Bob', 'Morice');


INSERT INTO questions (title)
VALUES
('test titre question');
INSERT INTO messages (text, person_id)
VALUES
('message test dans question', 1);
INSERT INTO question_have_message (question_id, message_id)
VALUES
((SELECT MAX(question_id) FROM questions),
    (SELECT MAX(message_id) FROM messages));

INSERT INTO tags (name)
VALUES
('test-tag');

INSERT INTO question_have_tag (question_id, tag_id)
VALUES
((SELECT MAX(question_id) FROM questions), 
        (SELECT tag_id FROM tags WHERE name='test-tag'));


INSERT messages (text)
VALUES
('test réponse');

INSERT message_answer_question (message_id, question_id)
VALUES
((SELECT max(message_id)
    FROM messages), 1);

INSERT person_vote_message (is_upvote, person_id, message_id)
VALUES
(TRUE, 1, 1);

INSERT emails (text, person_id)
VALUES
('bob.morice@email.org', 1);

INSERT passwords (hash, person_id)
VALUES
(sha2('a', 512), 1);

INSERT authorization_groups (name)
VALUES
('formateur'),
('apprenti');

INSERT person_belong_group (person_id, authorization_group_id)
VALUES
(1, 2);

