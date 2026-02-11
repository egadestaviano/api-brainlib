from yoyo import step

__depends__ = {}

create_table_sql = """
CREATE TABLE IF NOT EXISTS `user_profiles` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` INT UNSIGNED NOT NULL,
    `display_name` VARCHAR(255) NULL,
    `avatar_file_id` BIGINT UNSIGNED NULL,
    `bio` TEXT NULL,
    `extra` JSON NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_user_profiles_user_id` (`user_id`),
    CONSTRAINT `fk_user_profiles_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

drop_table_sql = """
DROP TABLE IF EXISTS `user_profiles`;
"""

steps = [
    step(create_table_sql, drop_table_sql),
]
