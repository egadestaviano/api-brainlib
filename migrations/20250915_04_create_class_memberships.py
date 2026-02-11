from yoyo import step

__depends__ = {}

create_table_sql = """
CREATE TABLE IF NOT EXISTS `class_memberships` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `class_id` INT UNSIGNED NOT NULL,
    `user_id` INT UNSIGNED NOT NULL,
    `role` VARCHAR(32) NOT NULL DEFAULT 'member',
    `joined_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_class_memberships_class_user` (`class_id`,`user_id`),
    KEY `idx_class_memberships_user_id` (`user_id`),
    CONSTRAINT `fk_class_memberships_class` FOREIGN KEY (`class_id`) REFERENCES `classes`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_class_memberships_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

drop_table_sql = """
DROP TABLE IF EXISTS `class_memberships`;
"""

steps = [
    step(create_table_sql, drop_table_sql),
]
