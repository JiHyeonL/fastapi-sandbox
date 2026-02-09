from app.users.api.responses import UserResponse
from app.users.core.application.outputs import UserCreateOutput


class UserApiMapper:

    @staticmethod
    def create_output_to_response(user_create_output: UserCreateOutput) -> UserResponse:
        return UserResponse(
            id=user_create_output.id,
            email=user_create_output.email,
            name=user_create_output.name,
            is_active=user_create_output.is_active,
            created_at=user_create_output.created_at,
            updated_at=user_create_output.updated_at,
            last_login=user_create_output.last_login,
        )
