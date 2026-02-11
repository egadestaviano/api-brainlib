from yoyo import step

__depends__ = {}

create_table_sql = """
CREATE TABLE IF NOT EXISTS `audit_logs` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `actor_id` INT UNSIGNED NULL,
    `action` VARCHAR(64) NOT NULL,
    `object_type` VARCHAR(64) NOT NULL,
    `object_id` BIGINT UNSIGNED NULL,
    `details` JSON NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_audit_logs_actor_id` (`actor_id`),
    KEY `idx_audit_logs_object` (`object_type`, `object_id`),
    CONSTRAINT `fk_audit_logs_actor` FOREIGN KEY (`actor_id`) REFERENCES `users`(`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

drop_table_sql = """
DROP TABLE IF EXISTS `audit_logs`;
"""

steps = [
    step(create_table_sql, drop_table_sql),
]
