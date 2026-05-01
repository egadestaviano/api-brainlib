from yoyo import step

__depends__ = {}

create_table_sql = """
CREATE TABLE IF NOT EXISTS `lesson_submissions` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `lesson_id` INT UNSIGNED NOT NULL,
    `user_id` INT UNSIGNED NOT NULL,
    `results_json` JSON NOT NULL,
    `score_correct` INT NOT NULL DEFAULT 0,
    `score_wrong` INT NOT NULL DEFAULT 0,
    `submitted_at` DATETIME NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `idx_lesson_user` (`lesson_id`, `user_id`),
    KEY `idx_lesson_submissions_lesson_id` (`lesson_id`),
    KEY `idx_lesson_submissions_user_id` (`user_id`),
    CONSTRAINT `fk_lesson_submissions_lesson` FOREIGN KEY (`lesson_id`) REFERENCES `lessons`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_lesson_submissions_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

drop_table_sql = """
DROP TABLE IF EXISTS `lesson_submissions`;
"""

steps = [
    step(create_table_sql, drop_table_sql),
]
