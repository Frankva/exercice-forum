START TRANSACTION;

DROP DATABASE IF EXISTS forum20240213;
CREATE DATABASE forum20240213;
USE forum20240213;

CREATE TABLE tags (
    tag_id bigint auto_increment primary key,
    name varchar(255)
);

CREATE TABLE questions (
    question_id bigint auto_increment primary key,
    title varchar(255)
);

CREATE TABLE question_have_tag (
    question_have_tag bigint auto_increment primary key,
    question_id bigint,
    tag_id bigint,
    foreign key (question_id) REFERENCES questions (question_id),
    foreign key (tag_id) REFERENCES tags (tag_id)
);

CREATE TABLE people (
    person_id bigint auto_increment primary key,
    firstname varchar(255),
    lastname varchar(255)
);

CREATE TABLE messages (
    message_id bigint auto_increment primary key,
    text varchar(15000),
    person_id bigint,
    create_date datetime,
    foreign key (person_id) REFERENCES people (person_id)
);

CREATE TABLE question_have_message (
    question_have_message_id bigint auto_increment primary key,
    question_id bigint,
    message_id bigint,
    foreign key (question_id) REFERENCES questions (question_id),
    foreign key (message_id) REFERENCES messages (message_id)
);

CREATE TABLE message_answer_question (
    message_answer_question_id bigint auto_increment primary key,
    question_id bigint,
    message_id bigint,
    foreign key (question_id) REFERENCES questions (question_id),
    foreign key (message_id) REFERENCES messages (message_id)
);

CREATE TABLE person_vote_message (
    person_vote_message_id bigint auto_increment primary key,
    person_id bigint,
    message_id bigint,
    foreign key (person_id) REFERENCES people (person_id),
    foreign key (message_id) REFERENCES messages (message_id)
);

CREATE TABLE emails (
    email_id bigint auto_increment primary key,
    text varchar(255),
    person_id bigint,
    foreign key (person_id) REFERENCES people (person_id)
);

CREATE TABLE passwords (
    password_id bigint auto_increment primary key,
    hash varchar(255),
    person_id bigint,
    foreign key (person_id) REFERENCES people (person_id)
);

CREATE TABLE authorization_groups (
    authorization_group_id bigint auto_increment primary key,
    name varchar(255)
);

CREATE TABLE person_belong_group (
    id_person_belong_group bigint auto_increment primary key,
    person_id bigint,
    authorization_group_id bigint,
    foreign key (person_id) REFERENCES people (person_id),
    foreign key (authorization_group_id)
    REFERENCES authorization_groups (authorization_group_id)
);

COMMIT;
