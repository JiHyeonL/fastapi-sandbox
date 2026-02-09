from app.auth.core.application.outputs import RegisterOutput
from app.auth.core.domain.token import Token
from app.users.core.application.outputs import UserCreateOutput


class AuthOutputMapper:

    @staticmethod
    def domain_to_register_output(token: Token, user_create_output: UserCreateOutput):
        return RegisterOutput(
            access_token=token.access_token,
            refresh_token=token.refresh_token,
            user_create_output=user_create_output
        )
