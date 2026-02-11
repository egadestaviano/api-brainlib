from yoyo import step

__depends__ = {}

create_table_sql = """
CREATE TABLE IF NOT EXISTS `presigned_uploads` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` INT UNSIGNED NOT NULL,
    `key` VARCHAR(255) NOT NULL,
    `mime_type` VARCHAR(255) NULL,
    `filename` VARCHAR(255) NULL,
    `expires_at` DATETIME NOT NULL,
    `completed` TINYINT(1) NOT NULL DEFAULT 0,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_presigned_uploads_key` (`key`),
    KEY `idx_presigned_uploads_user_id` (`user_id`),
    KEY `idx_presigned_uploads_expires_at` (`expires_at`),
    CONSTRAINT `fk_presigned_uploads_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

drop_table_sql = """
DROP TABLE IF EXISTS `presigned_uploads`;
"""

steps = [
    step(create_table_sql, drop_table_sql),
]
