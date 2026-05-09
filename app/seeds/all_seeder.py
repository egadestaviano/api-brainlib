"""
all_seeder.py – Main entry point for bulk demo seeding.
"""

import random
import json
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

from app.db import database
from app.models.user import User, Role, UserRole
from app.models.user_profile import UserProfile
from app.models.lms_class import LmsClass
from app.models.class_membership import ClassMembership
from app.models.lesson import Lesson
from app.models.lesson_submission import LessonSubmission

from app.config import init_database_from_env
from app.seeds.data.students_data import STUDENTS
from app.seeds.data.classes_data import TEACHERS, CLASSES, LESSONS_BY_CLASS

# ─────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────

def _now():
    return datetime.utcnow()

def _rand_dt(days_ago_max=90):
    return _now() - timedelta(days=random.randint(0, days_ago_max),
                              hours=random.randint(0, 23),
                              minutes=random.randint(0, 59))

def _get_or_create_user(email, password, role_name, display_name, bio):
    now = _now()
    user, created = User.get_or_create(
        email=email,
        defaults={
            "password_hash": generate_password_hash(password),
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        },
    )

    try:
        role = Role.get(Role.name == role_name)
    except Role.DoesNotExist:
        print(f"  ⚠️  Role '{role_name}' not found — run roles seeder first.")
        return user

    UserRole.get_or_create(user=user, role=role)

    profile, p_created = UserProfile.get_or_create(
        user=user,
        defaults={
            "display_name": display_name,
            "bio": bio,
            "extra": "{}",
            "created_at": now,
            "updated_at": now,
        },
    )
    if not p_created:
        profile.display_name = display_name
        profile.bio = bio
        profile.updated_at = now
        profile.save()

    return user

# ─────────────────────────────────────────────────────────
# Seed Logic
# ─────────────────────────────────────────────────────────

def seed_demo_accounts():
    print("\n🔑 Seeding core demo accounts...")
    # Admin
    _get_or_create_user("admin@example.com", "password", "admin", "Admin Demo", "System Administrator")
    # Teacher
    teacher_demo = _get_or_create_user("teacher@example.com", "password", "teacher", "Teacher Demo", "Lead Instructor")
    # Student
    student_demo = _get_or_create_user("student@example.com", "password", "student", "Student Demo", "Active Learner")
    
    return teacher_demo, student_demo

def seed_teachers():
    print("\n📚 Seeding 10+ teachers...")
    teacher_map = {}
    for t in TEACHERS:
        user = _get_or_create_user(
            email=t["email"],
            password="password",
            role_name="teacher",
            display_name=t["display_name"],
            bio=t["bio"],
        )
        teacher_map[t["email"]] = user
        print(f"  ✅ Teacher: {t['email']}")
    return teacher_map

def seed_students(student_demo):
    print("\n🎓 Seeding 100 students...")
    student_users = [student_demo] # Include demo student
    
    for s in STUDENTS:
        user = _get_or_create_user(
            email=s["email"],
            password="password",
            role_name="student",
            display_name=s["display_name"],
            bio=s["bio"],
        )
        student_users.append(user)
        # print(f"  ✅ Student: {s['email']}")
    
    print(f"  Total students: {len(student_users)}")
    return student_users

def seed_classes(teacher_map, student_users):
    print("\n🏫 Seeding 10 classes and memberships...")
    class_map = {}
    now = _now()

    for cls_data in CLASSES:
        teacher = teacher_map.get(cls_data["teacher_email"])
        if not teacher:
            continue

        lms_class, created = LmsClass.get_or_create(
            code=cls_data["code"],
            defaults={
                "title": cls_data["title"],
                "description": cls_data["description"],
                "creator": teacher,
                "visibility": "public",
                "created_at": now,
                "updated_at": now,
            },
        )
        if not created:
            lms_class.creator = teacher
            lms_class.title = cls_data["title"]
            lms_class.description = cls_data["description"]
            lms_class.save()
        
        print(f"  {'✅' if created else '🔄'} Class: {cls_data['code']} - {cls_data['title']}")

        # Teacher membership
        ClassMembership.get_or_create(
            class_ref=lms_class,
            user=teacher,
            defaults={"role": "teacher", "joined_at": now, "is_active": True},
        )

        # Student memberships
        enrolled_count = 0
        for idx in cls_data["student_indices"]:
            # +1 because student_demo is at index 0 in student_users
            s_idx = idx + 1
            if s_idx >= len(student_users):
                continue
            
            student = student_users[s_idx]
            _, c = ClassMembership.get_or_create(
                class_ref=lms_class,
                user=student,
                defaults={"role": "member", "joined_at": _rand_dt(30), "is_active": True},
            )
            if c: enrolled_count += 1

        # Always enroll the demo student in every class for easy viewing
        ClassMembership.get_or_create(
            class_ref=lms_class,
            user=student_users[0], # student@example.com
            defaults={"role": "member", "joined_at": now, "is_active": True},
        )

        print(f"       ↳ {enrolled_count} students enrolled.")
        class_map[lms_class.code] = lms_class

    return class_map

def seed_lessons(class_map, teacher_map):
    print("\n📖 Seeding lessons...")
    lesson_map = {}
    for cls_code, lessons in LESSONS_BY_CLASS.items():
        lms_class = class_map.get(cls_code)
        if not lms_class: continue
        
        # Get class author
        cls_info = next(c for c in CLASSES if c["code"] == cls_code)
        author = teacher_map.get(cls_info["teacher_email"])
        
        lesson_map[cls_code] = []
        for l_data in lessons:
            now = _now()
            lesson, created = Lesson.get_or_create(
                class_ref=lms_class,
                title=l_data["title"],
                defaults={
                    "summary": l_data["summary"],
                    "content_json": l_data["content_json"],
                    "author": author,
                    "is_published": True,
                    "created_at": now,
                    "updated_at": now,
                }
            )
            print(f"  {'✅' if created else '🔄'} Lesson: [{cls_code}] {l_data['title']}")
            lesson_map[cls_code].append(lesson)
    return lesson_map

def seed_submissions(class_map, student_users, lesson_map):
    print("\n📝 Seeding random submissions...")
    count = 0
    for cls_code, lessons in lesson_map.items():
        lms_class = class_map.get(cls_code)
        # Get students in this class
        memberships = ClassMembership.select().where(ClassMembership.class_ref == lms_class, ClassMembership.role == 'member')
        
        for m in memberships:
            # 50% chance to have a submission for each lesson
            for lesson in lessons:
                if random.random() > 0.5:
                    # Generate simple results_json
                    res = [{"question": "Q1", "chosen": 0, "correct": 0, "is_correct": True}]
                    now = _now()
                    _, created = LessonSubmission.get_or_create(
                        lesson=lesson,
                        user=m.user,
                        defaults={
                            "results_json": json.dumps(res),
                            "score_correct": 1,
                            "score_wrong": 0,
                            "submitted_at": _rand_dt(10),
                            "created_at": now,
                            "updated_at": now,
                        }
                    )
                    if created: count += 1
    print(f"  ✅ Created {count} submissions.")

def run_all():
    print("🚀 Starting Mega Seeder...")
    teacher_demo, student_demo = seed_demo_accounts()
    teacher_map = seed_teachers()
    student_users = seed_students(student_demo)
    class_map = seed_classes(teacher_map, student_users)
    lesson_map = seed_lessons(class_map, teacher_map)
    # seed_submissions(class_map, student_users, lesson_map)
    print("\n🎉 Seeding completed successfully!")

if __name__ == "__main__":
    init_database_from_env()
    if database.is_closed():
        database.connect()
    try:
        run_all()
    finally:
        if not database.is_closed():
            database.close()
