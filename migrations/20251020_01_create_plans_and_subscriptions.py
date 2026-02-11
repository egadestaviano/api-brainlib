from yoyo import step

__depends__ = {}

create_plans = """
CREATE TABLE IF NOT EXISTS `plans` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(64) NOT NULL UNIQUE,
    `stripe_price_id` VARCHAR(128) NOT NULL,
    `description` VARCHAR(255) NULL,
    `price` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

drop_plans = "DROP TABLE IF EXISTS `plans`;"

create_subscriptions = """
CREATE TABLE IF NOT EXISTS `subscriptions` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` INT UNSIGNED NOT NULL,
    `plan_id` INT UNSIGNED NOT NULL,
    `stripe_subscription_id` VARCHAR(128) NOT NULL,
    `status` ENUM('active','canceled','expired') NOT NULL DEFAULT 'active',
    `started_at` DATETIME NOT NULL,
    `expires_at` DATETIME NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`plan_id`) REFERENCES `plans`(`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

drop_subscriptions = "DROP TABLE IF EXISTS `subscriptions`;"

create_payment_logs = """
CREATE TABLE IF NOT EXISTS `payment_logs` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` INT UNSIGNED NOT NULL,
    `stripe_session_id` VARCHAR(128) NOT NULL,
    `amount` DECIMAL(10,2) NOT NULL,
    `currency` VARCHAR(10) NOT NULL DEFAULT 'usd',
    `status` VARCHAR(64) NOT NULL,
    `created_at` DATETIME NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

drop_payment_logs = "DROP TABLE IF EXISTS `payment_logs`;"

steps = [
    step(create_plans, drop_plans),
    step(create_subscriptions, drop_subscriptions),
    step(create_payment_logs, drop_payment_logs),
]
