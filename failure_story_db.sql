select Version();
SHOW DATABASES;
CREATE DATABASE failure_story_db;
SELECT DATABASE();
USE failure_story_db;

drop table posts_v_tfidf, Post_v_Writers_initialdata, Post_v_Writers_dinamicdata, Post_v_Readers, userResponseCache_Search_function, url;

CREATE TABLE users(
user_id 				VARCHAR(50)  	NOT NULL,
user_name				VARCHAR(50)		NOT NULL,
displayed_name			VARCHAR(50) 	NULL,
hashed_password			VARCHAR(50)		NOT NULL,
certified				BOOL            NOT NULL DEFAULT FALSE,
age 					INT				NULL,
gender 					ENUM ('M','F')  NOT NULL,
occupation 				VARCHAR(50)     NOT NULL,
mbti 					VARCHAR(50)     NULL,
PRIMARY KEY (user_id)
);

CREATE TABLE posts(
post_id			INT				NOT NULL auto_increment,
title 			VARCHAR(50) 	NULL,
content			VARCHAR(500)	NOT NULL,
category_id		INT      		NOT NULL,
age_at_failure 	INT  			NULL,
good 			INT  			NOT NULL,
impossible		INT				NOT NULL,
tell_me_earlier INT 			NOT NULL,
posting_date 	DATE 			NOT NULL,
anonimous		BOOL            NOT NULL DEFAULT FALSE,
PRIMARY KEY (post_id),
FOREIGN KEY (category_id) REFERENCES tags (category_id)
);

CREATE TABLE tags(
category_id	INT      		NOT NULL auto_increment,
key_words	VARCHAR(200)	NOT NULL,
PRIMARY KEY (category_id)
);

CREATE TABLE posts_v_tfidf(
post_id			INT				NOT NULL, 
tfidf_0			DOUBLE			NOT NULL,
tfidf_1			DOUBLE			NOT NULL,
tfidf_2			DOUBLE			NOT NULL,
tfidf_3			DOUBLE			NOT NULL,
tfidf_4			DOUBLE			NOT NULL,
tfidf_5			DOUBLE			NOT NULL,
tfidf_6			DOUBLE			NOT NULL,
tfidf_7			DOUBLE			NOT NULL,
tfidf_8			DOUBLE			NOT NULL,
tfidf_9			DOUBLE			NOT NULL,
tfidf_10		DOUBLE			NOT NULL,
tfidf_11		DOUBLE			NOT NULL,
tfidf_12		DOUBLE			NOT NULL,
tfidf_13		DOUBLE			NOT NULL,
tfidf_14		DOUBLE			NOT NULL,
tfidf_15		DOUBLE			NOT NULL,
tfidf_16		DOUBLE			NOT NULL,
tfidf_17		DOUBLE			NOT NULL,
tfidf_18		DOUBLE			NOT NULL,
tfidf_19		DOUBLE			NOT NULL,
PRIMARY KEY (post_id),
FOREIGN KEY (post_id) REFERENCES posts (post_id)
);

CREATE TABLE interested_tags(
id				VARCHAR(50)  	NOT NULL,
user_id 		VARCHAR(50)  	NOT NULL,
category_id		INT      		NOT NULL,
PRIMARY KEY (id)
);


CREATE TABLE Post_v_Writers_initialdata(
user_id 		VARCHAR(50)  	NOT NULL,
post_id			INT				NOT NULL, 
category_id		INT      		NOT NULL,
age 			INT				NULL,
gender 			ENUM ('M','F')  NOT NULL,
occupation 		VARCHAR(50)     NOT NULL,
PRIMARY KEY (user_id, post_id),
FOREIGN KEY (user_id) 		REFERENCES users (user_id),
FOREIGN KEY (post_id) 		REFERENCES posts (post_id),
FOREIGN KEY (category_id) 	REFERENCES tags  (category_id)
);

CREATE TABLE Post_v_Writers_dinamicdata(
user_id 		VARCHAR(50)  	NOT NULL,
post_id			INT				NOT NULL, 
category_id		INT      		NOT NULL,
age 			INT				NULL,
gender 			ENUM ('M','F')  NOT NULL,
occupation 		VARCHAR(50)     NOT NULL,
mbti 			VARCHAR(50)     NULL,
PRIMARY KEY (user_id, post_id),
FOREIGN KEY (user_id) 		REFERENCES users (user_id),
FOREIGN KEY (post_id) 		REFERENCES posts (post_id),
FOREIGN KEY (category_id) 	REFERENCES tags  (category_id)
);

CREATE TABLE Post_v_Readers(
user_id 				VARCHAR(50)  	NOT NULL,
post_id					INT				NOT NULL,
Good_post_ids			BOOL            NOT NULL DEFAULT FALSE,
Impossible_post_ids		BOOL            NOT NULL DEFAULT FALSE,
Tell_me_early_post_ids	BOOL            NOT NULL DEFAULT FALSE,
PRIMARY KEY (user_id, post_id),
FOREIGN KEY (user_id) REFERENCES users (user_id),
FOREIGN KEY (post_id) REFERENCES posts (post_id)
);

CREATE TABLE hiddennode(
create_key				VARCHAR(50)  	NOT NULL,
PRIMARY KEY (create_key)
);
CREATE TABLE wordhidden(
fromid					VARCHAR(50)  	NOT NULL,
toid					VARCHAR(50)  	NOT NULL,
strength				float			NOT NULL,
PRIMARY KEY (fromid)
);

CREATE TABLE hiddenhidden(
fromid					VARCHAR(50)  	NOT NULL,
toid					VARCHAR(50)  	NOT NULL,
strength				float			NOT NULL,
PRIMARY KEY (fromid)
);

CREATE TABLE hiddenurl(
fromid					VARCHAR(50)  	NOT NULL,
toid					VARCHAR(50)  	NOT NULL,
strength				float			NOT NULL,
PRIMARY KEY (fromid)
);

CREATE TABLE userResponseCache(
id				VARCHAR(50)  							NOT NULL,
sessionvalue	VARCHAR(50)  							NOT NULL,
querys			VARCHAR(50) 							NOT NULL,
selectedurl		VARCHAR(50)								NOT NULL,
actions			ENUM("search", "clic", "good", "early", "impossible")	NOT NULL,
PRIMARY KEY (id)
);

CREATE TABLE url(
url_id				VARCHAR(50)  		NOT NULL,
url					VARCHAR(50)  		NOT NULL,
category			ENUM("post", "user")	NOT NULL,
user_id 				VARCHAR(50)  	NOT NULL,
post_id					INT				NOT NULL
);
