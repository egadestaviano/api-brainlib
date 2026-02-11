from werkzeug.security import generate_password_hash
from app.db import database
from app.models.user import User, Role, UserRole
from app.models.user_profile import UserProfile
from datetime import datetime

def seed_users():
    users = [
        {
            "email": "admin@example.com",
            "password": "password",
            "role": "admin",
            "user_profile": {
                "display_name": "admin",
                "bio": "",
                "extra": "{}" 
            }
        },
        {
            "email": "teacher@example.com",
            "password": "password",
            "role": "teacher",
            "user_profile": {
                "display_name": "Teacher",
                "bio": "",
                "extra": "{}" 
            }
        },
        {
            "email": "student@example.com",
            "password": "password",
            "role": "student",
            "user_profile": {
                "display_name": "Stundent",
                "bio": "",
                "extra": "{}" 
            }
        },
    ]

    for u in users:
        now = datetime.utcnow()

        user, created = User.get_or_create(
            email=u["email"],
            defaults={
                "password_hash": generate_password_hash(u["password"]),
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
        )

        # role
        try:
            role = Role.get(Role.name == u["role"])
        except Role.DoesNotExist:
            print(f"⚠️ Role {u['role']} belum ada, jalankan seed_roles_permissions dulu.")
            continue

        UserRole.get_or_create(user=user, role=role)

        # profile
        if "user_profile" in u:
            profile_data = u["user_profile"]
            profile, p_created = UserProfile.get_or_create(
                user=user,
                defaults={
                    "display_name": profile_data.get("display_name", ""),
                    "bio": profile_data.get("bio", ""),
                    "extra": profile_data.get("extra", "{}"),
                    "created_at": now,
                    "updated_at": now,
                },
            )
            if not p_created:
                profile.display_name = profile_data.get("display_name", profile.display_name)
                profile.bio = profile_data.get("bio", profile.bio)
                profile.extra = profile_data.get("extra", profile.extra)
                profile.updated_at = now
                profile.save()

        if created:
            print(f"✅ User {u['email']} created with role {u['role']}")
        else:
            print(f"ℹ️ User {u['email']} already exists, ensured role {u['role']}")

if __name__ == "__main__":
    if database.is_closed():
        database.connect()

    seed_users()

    if not database.is_closed():
        database.close()
