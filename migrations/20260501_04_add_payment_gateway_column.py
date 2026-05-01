from yoyo import step

__depends__ = {"20260501_03_fix_subscription_table"}

def add_payment_gateway_if_missing(backend):
    # Check if column exists
    cursor = backend.cursor()
    cursor.execute("SHOW COLUMNS FROM `subscriptions` LIKE 'payment_gateway'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE `subscriptions` ADD COLUMN `payment_gateway` VARCHAR(32) NOT NULL DEFAULT 'stripe' AFTER `stripe_subscription_id` ")

def remove_payment_gateway(backend):
    cursor = backend.cursor()
    cursor.execute("SHOW COLUMNS FROM `subscriptions` LIKE 'payment_gateway'")
    if cursor.fetchone():
        cursor.execute("ALTER TABLE `subscriptions` DROP COLUMN `payment_gateway` ")

steps = [
    step(add_payment_gateway_if_missing, remove_payment_gateway)
]
