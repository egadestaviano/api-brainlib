from yoyo import step

__depends__ = {"20251020_01_create_plans_and_subscriptions"}

update_status_column = "ALTER TABLE `subscriptions` MODIFY COLUMN `status` VARCHAR(64) NOT NULL DEFAULT 'active';"
restore_status_column = "ALTER TABLE `subscriptions` MODIFY COLUMN `status` ENUM('active','canceled','expired', 'pending') NOT NULL DEFAULT 'active';"

make_expires_at_nullable = "ALTER TABLE `subscriptions` MODIFY COLUMN `expires_at` DATETIME NULL;"
make_expires_at_not_null = "ALTER TABLE `subscriptions` MODIFY COLUMN `expires_at` DATETIME NOT NULL;"

make_stripe_sub_id_nullable = "ALTER TABLE `subscriptions` MODIFY COLUMN `stripe_subscription_id` VARCHAR(128) NULL;"
make_stripe_sub_id_not_null = "ALTER TABLE `subscriptions` MODIFY COLUMN `stripe_subscription_id` VARCHAR(128) NOT NULL;"

steps = [
    step(update_status_column, restore_status_column),
    step(make_expires_at_nullable, make_expires_at_not_null),
    step(make_stripe_sub_id_nullable, make_stripe_sub_id_not_null),
]
