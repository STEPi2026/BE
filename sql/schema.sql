-- STEPi Database Schema
-- Generated from SQLAlchemy models
-- Database: MySQL 8.4
-- Tables: 21

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE badges (
	id INTEGER NOT NULL AUTO_INCREMENT,
	code VARCHAR(30) NOT NULL,
	name VARCHAR(100) NOT NULL,
	description TEXT,
	condition_type VARCHAR(50) NOT NULL,
	threshold INTEGER NOT NULL,
	reward_xp INTEGER NOT NULL,
	created_at DATETIME NOT NULL DEFAULT (now()),
	PRIMARY KEY (id),
	UNIQUE (code)
);

CREATE TABLE concepts (
	id INTEGER NOT NULL AUTO_INCREMENT,
	code VARCHAR(30) NOT NULL,
	name VARCHAR(100) NOT NULL,
	description TEXT,
	subject VARCHAR(50) NOT NULL,
	grade_level VARCHAR(20) NOT NULL,
	parent_concept_id INTEGER,
	created_at DATETIME NOT NULL DEFAULT (now()),
	PRIMARY KEY (id),
	UNIQUE (code),
	FOREIGN KEY(parent_concept_id) REFERENCES concepts (id)
);

CREATE TABLE problems (
	id INTEGER NOT NULL AUTO_INCREMENT,
	problem_code VARCHAR(30) NOT NULL,
	question TEXT NOT NULL,
	answer TEXT NOT NULL,
	difficulty INTEGER NOT NULL,
	problem_type VARCHAR(20) NOT NULL,
	`usage` VARCHAR(30) NOT NULL,
	explanation TEXT,
	created_at DATETIME NOT NULL DEFAULT (now()),
	updated_at DATETIME NOT NULL DEFAULT (now()),
	PRIMARY KEY (id),
	UNIQUE (problem_code)
);

CREATE TABLE users (
	id INTEGER NOT NULL AUTO_INCREMENT,
	email VARCHAR(255) NOT NULL,
	password_hash VARCHAR(255) NOT NULL,
	name VARCHAR(100) NOT NULL,
	`role` VARCHAR(20) NOT NULL,
	created_at DATETIME NOT NULL DEFAULT (now()),
	updated_at DATETIME NOT NULL DEFAULT (now()),
	PRIMARY KEY (id),
	UNIQUE (email)
);

CREATE TABLE captured_problems (
	id INTEGER NOT NULL AUTO_INCREMENT,
	problem_image_url VARCHAR(500) NOT NULL,
	extracted_problem_text TEXT,
	created_at DATETIME NOT NULL DEFAULT (now()),
	student_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(student_id) REFERENCES users (id)
);

CREATE TABLE learning_sessions (
	id INTEGER NOT NULL AUTO_INCREMENT,
	started_at DATETIME NOT NULL,
	ended_at DATETIME,
	duration_seconds INTEGER,
	student_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(student_id) REFERENCES users (id)
);

CREATE TABLE misconceptions (
	id INTEGER NOT NULL AUTO_INCREMENT,
	code VARCHAR(50) NOT NULL,
	name VARCHAR(100) NOT NULL,
	description TEXT,
	concept_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (code),
	FOREIGN KEY(concept_id) REFERENCES concepts (id)
);

CREATE TABLE problem_concepts (
	problem_id INTEGER NOT NULL,
	concept_id INTEGER NOT NULL,
	PRIMARY KEY (problem_id, concept_id),
	FOREIGN KEY(problem_id) REFERENCES problems (id),
	FOREIGN KEY(concept_id) REFERENCES concepts (id)
);

CREATE TABLE skills (
	id INTEGER NOT NULL AUTO_INCREMENT,
	code VARCHAR(30) NOT NULL,
	name VARCHAR(100) NOT NULL,
	description TEXT,
	created_at DATETIME NOT NULL DEFAULT (now()),
	concept_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (code),
	FOREIGN KEY(concept_id) REFERENCES concepts (id)
);

CREATE TABLE student_badges (
	student_id INTEGER NOT NULL,
	badge_id INTEGER NOT NULL,
	earned_at DATETIME NOT NULL DEFAULT (now()),
	PRIMARY KEY (student_id, badge_id),
	FOREIGN KEY(student_id) REFERENCES users (id),
	FOREIGN KEY(badge_id) REFERENCES badges (id)
);

CREATE TABLE student_gamification (
	id INTEGER NOT NULL AUTO_INCREMENT,
	xp INTEGER NOT NULL,
	level INTEGER NOT NULL,
	current_streak INTEGER NOT NULL,
	longest_streak INTEGER NOT NULL,
	last_study_date DATE,
	updated_at DATETIME NOT NULL DEFAULT (now()),
	student_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	CONSTRAINT uq_student_gamification_student UNIQUE (student_id),
	FOREIGN KEY(student_id) REFERENCES users (id)
);

CREATE TABLE student_profiles (
	id INTEGER NOT NULL AUTO_INCREMENT,
	grade_level VARCHAR(20) NOT NULL,
	learning_goal VARCHAR(255),
	created_at DATETIME NOT NULL DEFAULT (now()),
	updated_at DATETIME NOT NULL DEFAULT (now()),
	user_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (user_id),
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE student_states (
	id INTEGER NOT NULL AUTO_INCREMENT,
	mastery_score DECIMAL(5, 4) NOT NULL,
	knowledge_state VARCHAR(30) NOT NULL,
	weakness_score DECIMAL(5, 4) NOT NULL,
	updated_at DATETIME NOT NULL DEFAULT (now()),
	student_id INTEGER NOT NULL,
	concept_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	CONSTRAINT uq_student_state_student_concept UNIQUE (student_id, concept_id),
	FOREIGN KEY(student_id) REFERENCES users (id),
	FOREIGN KEY(concept_id) REFERENCES concepts (id)
);

CREATE TABLE attempts (
	id INTEGER NOT NULL AUTO_INCREMENT,
	student_answer TEXT,
	is_correct BOOL NOT NULL,
	solution_image_url VARCHAR(500),
	solve_time_seconds INTEGER,
	hint_count INTEGER NOT NULL,
	attempted_at DATETIME NOT NULL,
	retry_count INTEGER NOT NULL,
	student_id INTEGER NOT NULL,
	session_id INTEGER NOT NULL,
	problem_id INTEGER,
	captured_problem_id INTEGER,
	parent_attempt_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(student_id) REFERENCES users (id),
	FOREIGN KEY(session_id) REFERENCES learning_sessions (id),
	FOREIGN KEY(problem_id) REFERENCES problems (id),
	FOREIGN KEY(captured_problem_id) REFERENCES captured_problems (id),
	FOREIGN KEY(parent_attempt_id) REFERENCES attempts (id)
);

CREATE TABLE learning_logs (
	id INTEGER NOT NULL AUTO_INCREMENT,
	event_type VARCHAR(50) NOT NULL,
	metadata JSON,
	created_at DATETIME NOT NULL DEFAULT (now()),
	student_id INTEGER NOT NULL,
	session_id INTEGER,
	problem_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(student_id) REFERENCES users (id),
	FOREIGN KEY(session_id) REFERENCES learning_sessions (id),
	FOREIGN KEY(problem_id) REFERENCES problems (id)
);

CREATE TABLE problem_skills (
	problem_id INTEGER NOT NULL,
	skill_id INTEGER NOT NULL,
	PRIMARY KEY (problem_id, skill_id),
	FOREIGN KEY(problem_id) REFERENCES problems (id),
	FOREIGN KEY(skill_id) REFERENCES skills (id)
);

CREATE TABLE skill_prerequisites (
	skill_id INTEGER NOT NULL,
	prerequisite_skill_id INTEGER NOT NULL,
	description TEXT,
	PRIMARY KEY (skill_id, prerequisite_skill_id),
	FOREIGN KEY(skill_id) REFERENCES skills (id),
	FOREIGN KEY(prerequisite_skill_id) REFERENCES skills (id)
);

CREATE TABLE student_misconceptions (
	id INTEGER NOT NULL AUTO_INCREMENT,
	confidence DECIMAL(5, 4) NOT NULL,
	detected_at DATETIME NOT NULL DEFAULT (now()),
	resolved_at DATETIME,
	student_id INTEGER NOT NULL,
	misconception_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(student_id) REFERENCES users (id),
	FOREIGN KEY(misconception_id) REFERENCES misconceptions (id)
);

CREATE TABLE student_skill_states (
	id INTEGER NOT NULL AUTO_INCREMENT,
	mastery_score NUMERIC(5, 4) NOT NULL,
	weakness_score NUMERIC(5, 4) NOT NULL,
	consecutive_wrong_count INTEGER NOT NULL,
	last_practiced_at DATETIME,
	updated_at DATETIME NOT NULL DEFAULT (now()),
	student_id INTEGER NOT NULL,
	skill_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	CONSTRAINT uq_student_skill_states_student_skill UNIQUE (student_id, skill_id),
	FOREIGN KEY(student_id) REFERENCES users (id),
	FOREIGN KEY(skill_id) REFERENCES skills (id)
);

CREATE TABLE ai_analysis_results (
	id INTEGER NOT NULL AUTO_INCREMENT,
	mastery_score DECIMAL(5, 4) NOT NULL,
	first_error_step INTEGER,
	confidence DECIMAL(5, 4) NOT NULL,
	raw_result JSON NOT NULL,
	created_at DATETIME NOT NULL DEFAULT (now()),
	attempt_id INTEGER NOT NULL,
	misconception_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(attempt_id) REFERENCES attempts (id),
	FOREIGN KEY(misconception_id) REFERENCES misconceptions (id)
);

CREATE TABLE tutor_actions (
	id INTEGER NOT NULL AUTO_INCREMENT,
	action_type VARCHAR(50) NOT NULL,
	message TEXT NOT NULL,
	next_difficulty INTEGER,
	raw_result JSON,
	created_at DATETIME NOT NULL DEFAULT (now()),
	student_id INTEGER NOT NULL,
	attempt_id INTEGER NOT NULL,
	ai_analysis_id INTEGER NOT NULL,
	next_problem_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(student_id) REFERENCES users (id),
	FOREIGN KEY(attempt_id) REFERENCES attempts (id),
	FOREIGN KEY(ai_analysis_id) REFERENCES ai_analysis_results (id),
	FOREIGN KEY(next_problem_id) REFERENCES problems (id)
);

SET FOREIGN_KEY_CHECKS = 1;
