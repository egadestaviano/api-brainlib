from app.models.user import Role, Permission, RolePermission


def seed_roles_permissions():
    # ==========================
    # 1. Daftar role
    # ==========================
    roles = {
        "admin": "Full access to system",
        "teacher": "Can manage lessons and classes",
        "student": "Can join classes and submit assignments",
    }

    # ==========================
    # 2. Resource list
    # ==========================
    resources = [
        "ai_edit",
        "assignment",
        "assignment_file",
        "audit_log",
        "class",
        "class_membership",
        "file",
        "grade",
        "lesson",
        "lesson_version",
        "notification",
        "presigned_upload",
        "submission",
        "submission_file",
        "user",
        "user_profile",
    ]

    # ==========================
    # 3. Generate permissions
    # ==========================
    permission_templates = [
        ("view", "View single {res}"),
        ("view_all", "View all {res_plural}"),
        ("create", "Create {res}"),
        ("update", "Update {res}"),
        ("delete", "Delete {res}"),
    ]

    permissions = {}
    for res in resources:
        res_plural = res + "s" if not res.endswith("s") else res
        for action, desc_tpl in permission_templates:
            perm_name = f"{res}.{action}"
            desc = desc_tpl.format(res=res.replace("_", " "), res_plural=res_plural.replace("_", " "))
            permissions[perm_name] = desc

    # ==========================
    # 4. Insert roles
    # ==========================
    role_objs = {}
    for name, desc in roles.items():
        role, _ = Role.get_or_create(name=name, defaults={"description": desc})
        role_objs[name] = role

    # ==========================
    # 5. Insert permissions
    # ==========================
    perm_objs = {}
    for name, desc in permissions.items():
        perm, _ = Permission.get_or_create(name=name, defaults={"description": desc})
        perm_objs[name] = perm

    # ==========================
    # 6. Mapping role → permission
    # ==========================
    mapping = {
        "admin": list(perm_objs.keys()),
        "teacher": [
            "class.view_all", "class.view", "class.create", "class.update", "class.delete",
            "lesson.view_all", "lesson.view", "lesson.create", "lesson.update", "lesson.delete",
            "assignment.view_all", "assignment.view", "assignment.create", "assignment.update", "assignment.delete",
            "grade.view_all", "grade.view", "grade.update", 
            "submission.view_all", "submission.view",
        ],
        "student": [
            "class.view_all", "class.view",
            "lesson.view_all", "lesson.view",
            "assignment.view_all", "assignment.view",
            "submission.create", "submission.view", "submission_file.create", "submission_file.view",
        ],
    }

    for role_name, perms in mapping.items():
        role = role_objs[role_name]
        for perm_name in perms:
            if perm_name in perm_objs:
                RolePermission.get_or_create(role=role, permission=perm_objs[perm_name])

    print("✅ Roles & permissions seeded successfully!")
