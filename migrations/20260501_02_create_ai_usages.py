from yoyo import step

__depends__ = {}

create_table_sql = """
CREATE TABLE IF NOT EXISTS `ai_usages` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` INT UNSIGNED NOT NULL,
    `used_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_ai_usages_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

drop_table_sql = """
DROP TABLE IF EXISTS `ai_usages`;
"""

steps = [
    step(create_table_sql, drop_table_sql),
]
