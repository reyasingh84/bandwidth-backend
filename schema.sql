CREATE DATABASE IF NOT EXISTS task_manager
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE task_manager;

-- TEAMS
CREATE TABLE teams (
    id           VARCHAR(36)  NOT NULL,
    name         VARCHAR(100) NOT NULL,
    short_name   VARCHAR(20)  NOT NULL,
    description  TEXT,
    created_at   BIGINT NOT NULL,
    updated_at   BIGINT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_teams_name (name),
    UNIQUE KEY uq_teams_short_name (short_name)
) ENGINE=InnoDB;

-- USERS
CREATE TABLE users (
    id            VARCHAR(36)  NOT NULL,
    first_name    VARCHAR(100) NOT NULL,
    last_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(255) NOT NULL,
    username      VARCHAR(50)  NOT NULL,
    password      VARCHAR(255) NOT NULL,
    phone         VARCHAR(20),
    role          VARCHAR(20)  NOT NULL,
    team_id       VARCHAR(36),
    department    VARCHAR(20)  NOT NULL,
    designation   VARCHAR(100),
    is_active     BOOLEAN NOT NULL DEFAULT TRUE,
    created_at    BIGINT NOT NULL,
    updated_at    BIGINT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_email (email),
    UNIQUE KEY uq_users_username (username),
    CONSTRAINT chk_users_role
        CHECK (role IN ('admin','director','manager','employee')),
    CONSTRAINT chk_users_department
        CHECK (department IN ('it','engineering','qa','security','devops')),
    CONSTRAINT fk_users_team
        FOREIGN KEY (team_id) REFERENCES teams(id)
) ENGINE=InnoDB;

-- TASKS
CREATE TABLE tasks (
    id                  VARCHAR(36)  NOT NULL,
    team_id             VARCHAR(36)  NOT NULL,
    title               VARCHAR(255) NOT NULL,
    description         TEXT,
    acpt_criteria       TEXT,
    category            VARCHAR(20)  NOT NULL,
    status              VARCHAR(20)  NOT NULL DEFAULT 'open',
    reporter_id         VARCHAR(36)  NOT NULL,
    reporter_username   VARCHAR(50)  NOT NULL,
    assignee_id         VARCHAR(36),
    assignee_username   VARCHAR(50),
    priority            TINYINT UNSIGNED NOT NULL DEFAULT 3,
    proj_name           VARCHAR(100),
    history             TEXT NOT NULL,
    deadline            BIGINT,
    created_at          BIGINT NOT NULL,
    updated_at          BIGINT NOT NULL,
    PRIMARY KEY (id),
    KEY idx_tasks_status (status),
    KEY idx_tasks_deadline (deadline),
    CONSTRAINT chk_tasks_category
        CHECK (category IN ('bug','testing','task')),
    CONSTRAINT chk_tasks_status
        CHECK (status IN ('open','in_progress','review','testing','closed','on_hold')),
    CONSTRAINT chk_tasks_priority
        CHECK (priority BETWEEN 1 AND 5),
    CONSTRAINT fk_tasks_team
        FOREIGN KEY (team_id) REFERENCES teams(id),
    CONSTRAINT fk_tasks_reporter
        FOREIGN KEY (reporter_id) REFERENCES users(id),
    CONSTRAINT fk_tasks_assignee
        FOREIGN KEY (assignee_id) REFERENCES users(id)
) ENGINE=InnoDB;

-- COMMENTS
CREATE TABLE comments (
    id              VARCHAR(36) NOT NULL,
    message         TEXT NOT NULL,
    author_id       VARCHAR(36) NOT NULL,
    author_username VARCHAR(50) NOT NULL,
    task_id         VARCHAR(36) NOT NULL,
    created_at      BIGINT NOT NULL,
    updated_at      BIGINT NOT NULL,
    PRIMARY KEY (id),
    KEY idx_comments_task_id (task_id),
    CONSTRAINT fk_comments_author
        FOREIGN KEY (author_id) REFERENCES users(id),
    CONSTRAINT fk_comments_task
        FOREIGN KEY (task_id) REFERENCES tasks(id)
) ENGINE=InnoDB;