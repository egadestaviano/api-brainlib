from yoyo import step

__depends__ = {}

create_table_sql = """
CREATE TABLE IF NOT EXISTS `ai_edits` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `target_table` VARCHAR(255) NOT NULL,
    `target_id` BIGINT UNSIGNED NOT NULL,
    `original_content` LONGTEXT NULL,
    `edited_content` LONGTEXT NULL,
    `editor_service` VARCHAR(64) NOT NULL,
    `user_id` INT UNSIGNED NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_ai_edits_target` (`target_table`, `target_id`),
    KEY `idx_ai_edits_user_id` (`user_id`),
    CONSTRAINT `fk_ai_edits_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

drop_table_sql = """
DROP TABLE IF EXISTS `ai_edits`;
"""

steps = [
    step(create_table_sql, drop_table_sql),
]
