from yoyo import step

__depends__ = {}

create_table_sql = """
CREATE TABLE IF NOT EXISTS `lessons_version` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `lesson_id` INT UNSIGNED NOT NULL,
    `version_number` INT UNSIGNED NOT NULL,
    `content_json` JSON NULL,
    `author_id` INT UNSIGNED NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_lessons_version_unique` (`lesson_id`,`version_number`),
    KEY `idx_lessons_version_lesson_id` (`lesson_id`),
    KEY `idx_lessons_version_author_id` (`author_id`),
    CONSTRAINT `fk_lessons_version_lesson` FOREIGN KEY (`lesson_id`) REFERENCES `lessons`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_lessons_version_author` FOREIGN KEY (`author_id`) REFERENCES `users`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

drop_table_sql = """
DROP TABLE IF EXISTS `lessons_version`;
"""

steps = [
    step(create_table_sql, drop_table_sql),
]
