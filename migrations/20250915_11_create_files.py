from yoyo import step

__depends__ = {}

create_table_sql = """
CREATE TABLE IF NOT EXISTS `files` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `owner_id` INT UNSIGNED NOT NULL,
    `filename` VARCHAR(255) NOT NULL,
    `mime_type` VARCHAR(255) NULL,
    `url` TEXT NULL,
    `path` TEXT NULL,
    `size_bytes` BIGINT UNSIGNED NOT NULL DEFAULT 0,
    `purpose` VARCHAR(64) NULL,
    `storage_backend` VARCHAR(64) NOT NULL DEFAULT 'local',
    `is_public` TINYINT(1) NOT NULL DEFAULT 0,
    `reference_count` INT UNSIGNED NOT NULL DEFAULT 0,
    `metadata` JSON NULL,
    `uploaded_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_files_owner_id` (`owner_id`),
    CONSTRAINT `fk_files_owner` FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

drop_table_sql = """
DROP TABLE IF EXISTS `files`;
"""

steps = [
    step(create_table_sql, drop_table_sql),
]
