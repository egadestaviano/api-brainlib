from yoyo import step

__depends__ = {}

create_table_sql = """
CREATE TABLE IF NOT EXISTS `classes` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `description` TEXT NULL,
    `code` VARCHAR(64) NOT NULL,
    `creator_id` INT UNSIGNED NOT NULL,
    `visibility` VARCHAR(20) NOT NULL DEFAULT 'private',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_classes_code` (`code`),
    KEY `idx_classes_creator_id` (`creator_id`),
    CONSTRAINT `fk_classes_creator` FOREIGN KEY (`creator_id`) REFERENCES `users`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

drop_table_sql = """
DROP TABLE IF EXISTS `classes`;
"""

steps = [
    step(create_table_sql, drop_table_sql),
]
