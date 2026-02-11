from flask import jsonify
from app.schemas.user import UserSchema
from app.models.user import RolePermission, Permission, UserRole
from app.utils.auth import get_user_from_token
import logging

logging.basicConfig(level=logging.DEBUG)

user_schema = UserSchema()

def me_user_handler():
    user, profile, error = get_user_from_token()
    if error:
        return error

    user_roles = list(user.roles)  
    role_ids = [ur.role.id for ur in user_roles] 

    role_perms = (
        RolePermission.select(RolePermission, Permission)
        .join(Permission)
        .where(RolePermission.role.in_(role_ids))
    )
    permissions = [rp.permission.name for rp in role_perms]
    
    # profile
    data = user_schema.dump(user)
    if profile:
        data["profile"] = {
            "display_name": profile.display_name,
            "avatar_file_id": profile.avatar_file_id,
            "bio": profile.bio,
            "extra": profile.extra,
        }
    else:
        data["profile"] = None
    data["roles"] = [ur.role.name for ur in user_roles]
    data["permissions"] = permissions

    return jsonify(data), 200
