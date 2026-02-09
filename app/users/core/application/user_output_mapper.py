from app.users.core.application.outputs import UserCreateOutput
from app.users.core.domain.user import User


class UserOutputMapper:

    @staticmethod
    def domain_to_create_output(user: User) -> UserCreateOutput:
        return UserCreateOutput(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            name=user.name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login,
        )
