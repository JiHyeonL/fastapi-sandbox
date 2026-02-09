from app.auth.api.requests import RegisterRequest
from app.auth.api.responses import RegisterResponse
from app.auth.core.application.inputs import RegisterInput
from app.auth.core.application.outputs import RegisterOutput
from app.users.api.user_api_mapper import UserApiMapper


class AuthAPIMapper:

    @staticmethod
    def register_request_to_input(register_request: RegisterRequest) -> RegisterInput:
        return RegisterInput(
            email=register_request.email,
            password=register_request.password,
            name=register_request.name
        )

    @staticmethod
    def register_output_to_response(register_output: RegisterOutput) -> RegisterResponse:
        return RegisterResponse(
            access_token=register_output.access_token,
            user=UserApiMapper.create_output_to_response(register_output.user_create_output)
        )
