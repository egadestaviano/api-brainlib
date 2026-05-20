from yoyo import step

__depends__ = {"20260501_04_add_payment_gateway_column"}

def apply_step(backend):
    cursor = backend.cursor()
    
    # 1. Check/Add results_json
    cursor.execute("SHOW COLUMNS FROM `lesson_submissions` LIKE 'results_json'")
    if not cursor.fetchone():
        # Add results_json as nullable first
        cursor.execute("ALTER TABLE `lesson_submissions` ADD COLUMN `results_json` JSON NULL AFTER `user_id`")
        
        # If answers_json exists, copy data
        cursor.execute("SHOW COLUMNS FROM `lesson_submissions` LIKE 'answers_json'")
        if cursor.fetchone():
            cursor.execute("UPDATE `lesson_submissions` SET `results_json` = `answers_json` WHERE `results_json` IS NULL")
            
        # Update any remaining NULLs to default '{}'
        cursor.execute("UPDATE `lesson_submissions` SET `results_json` = '{}' WHERE `results_json` IS NULL")
        
        # Change results_json to NOT NULL
        cursor.execute("ALTER TABLE `lesson_submissions` MODIFY COLUMN `results_json` JSON NOT NULL")

    # 2. Check/Add score_correct
    cursor.execute("SHOW COLUMNS FROM `lesson_submissions` LIKE 'score_correct'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE `lesson_submissions` ADD COLUMN `score_correct` INT NOT NULL DEFAULT 0 AFTER `results_json`")

    # 3. Check/Add score_wrong
    cursor.execute("SHOW COLUMNS FROM `lesson_submissions` LIKE 'score_wrong'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE `lesson_submissions` ADD COLUMN `score_wrong` INT NOT NULL DEFAULT 0 AFTER `score_correct`")

def rollback_step(backend):
    cursor = backend.cursor()
    
    # Remove score_wrong
    cursor.execute("SHOW COLUMNS FROM `lesson_submissions` LIKE 'score_wrong'")
    if cursor.fetchone():
        cursor.execute("ALTER TABLE `lesson_submissions` DROP COLUMN `score_wrong`")
        
    # Remove score_correct
    cursor.execute("SHOW COLUMNS FROM `lesson_submissions` LIKE 'score_correct'")
    if cursor.fetchone():
        cursor.execute("ALTER TABLE `lesson_submissions` DROP COLUMN `score_correct`")
        
    # Remove results_json
    cursor.execute("SHOW COLUMNS FROM `lesson_submissions` LIKE 'results_json'")
    if cursor.fetchone():
        cursor.execute("ALTER TABLE `lesson_submissions` DROP COLUMN `results_json`")

steps = [
    step(apply_step, rollback_step)
]
