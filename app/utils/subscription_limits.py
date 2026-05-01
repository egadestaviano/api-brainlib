from flask import jsonify
from app.models.subscription import Subscription, Plan
from app.models.lms_class import LmsClass
from app.models.class_membership import ClassMembership
from app.models.lesson import Lesson
from datetime import datetime

PLAN_LIMITS = {
    # Starter Monthly & Yearly
    1: {"max_classes": 1, "max_students": 10, "max_lessons": 5, "max_ai": 5},
    4: {"max_classes": 1, "max_students": 10, "max_lessons": 5, "max_ai": 5},
    # Medium Monthly & Yearly
    2: {"max_classes": 10, "max_students": 50, "max_lessons": 20, "max_ai": 50},
    5: {"max_classes": 10, "max_students": 50, "max_lessons": 20, "max_ai": 50},
    # Enterprise Monthly & Yearly (Use -1 for unlimited)
    3: {"max_classes": -1, "max_students": -1, "max_lessons": -1, "max_ai": -1},
    6: {"max_classes": -1, "max_students": -1, "max_lessons": -1, "max_ai": -1},
}

def get_user_plan_limits(user_id):
    subscription = (
        Subscription
        .select(Subscription, Plan)
        .join(Plan)
        .where((Subscription.user == user_id) & (Subscription.status == "active"))
        .order_by(Subscription.started_at.desc())
        .first()
    )
    
    if not subscription:
        # Default to Starter limits if no active sub (or maybe lower?)
        # Let's use Starter Monthly as baseline
        return PLAN_LIMITS[1]
    
    return PLAN_LIMITS.get(subscription.plan.id, PLAN_LIMITS[1])

def check_class_creation_limit(user_id):
    limits = get_user_plan_limits(user_id)
    if limits["max_classes"] == -1:
        return True, None
    
    current_count = LmsClass.select().where(LmsClass.creator == user_id).count()
    if current_count >= limits["max_classes"]:
        return False, jsonify({"error": f"Class creation limit reached ({limits['max_classes']}). Please upgrade your plan."}), 403
    
    return True, None

def check_student_limit(class_id, creator_id):
    limits = get_user_plan_limits(creator_id)
    if limits["max_students"] == -1:
        return True, None
    
    current_count = ClassMembership.select().where(ClassMembership.class_ref == class_id).count()
    if current_count >= limits["max_students"]:
        return False, jsonify({"error": f"Student limit reached for this class ({limits['max_students']}). Creator needs to upgrade their plan."}), 403
    
    return True, None

def check_lesson_limit(class_id, creator_id):
    limits = get_user_plan_limits(creator_id)
    if limits["max_lessons"] == -1:
        return True, None
    
    current_count = Lesson.select().where(Lesson.class_id == class_id).count()
    if current_count >= limits["max_lessons"]:
        return False, jsonify({"error": f"Lesson limit reached for this class ({limits['max_lessons']}). Please upgrade your plan."}), 403
    
    return True, None

def check_ai_limit(user_id):
    from app.models.subscription import AIUsage
    limits = get_user_plan_limits(user_id)
    if limits["max_ai"] == -1:
        return True, None
    
    # Check usage for the current month
    now = datetime.utcnow()
    first_day_of_month = datetime(now.year, now.month, 1)
    
    current_usage = AIUsage.select().where(
        (AIUsage.user == user_id) & 
        (AIUsage.used_at >= first_day_of_month)
    ).count()
    
    if current_usage >= limits["max_ai"]:
        return False, jsonify({"error": f"AI generation limit reached for this month ({limits['max_ai']}). Please upgrade your plan."}), 403
    
    return True, None

def record_ai_usage(user_id):
    from app.models.subscription import AIUsage
    AIUsage.create(user=user_id)
