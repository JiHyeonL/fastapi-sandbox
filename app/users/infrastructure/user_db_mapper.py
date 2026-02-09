from app.users.core.domain.user import User
from app.users.infrastructure.models import UserDB


class UserDBMapper:

    @staticmethod
    def domain_to_db(user: User) -> UserDB:
        return UserDB(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            name=user.name,
            is_active=user.is_active,
            last_login=user.last_login,
        )

    @staticmethod
    def db_to_domain(user_db: UserDB) -> User:
        return User(
            id=user_db.id,
            email=user_db.email,
            password_hash=user_db.password_hash,
            name=user_db.name,
            is_active=user_db.is_active,
            last_login=user_db.last_login,
            created_at=getattr(user_db, 'created_at', None),
            updated_at=getattr(user_db, 'updated_at', None)
        )
