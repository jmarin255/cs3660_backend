import hashlib
import jwt
import datetime
from repositories.user_repository import UserRepository
from config import settings

class LoginService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify a JWT token and decode its payload."""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

    def get_login_token(self, username: str, password: str) -> str:
        """Generate a JWT token after verifying user credentials."""
        try:
            # Fetch user from database
            user = self.user_repository.get_user_by_username(username)
            if not user:
                raise Exception("User not found")

            # Hash input password using SHA256
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Verify password match
            if user.password_hash != hashed_password:
                raise Exception("Invalid credentials")

            user_payload = {
                "username": user.username,
                "name": user.name
            }

            # Generate JWT token with expiration time
            expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
            token_payload = {
                "sub": user.username,  # Subject (user)
                "exp": expiration_time,  # Expiry time
                "user": user_payload  # Include user attributes if needed
            }
            token = jwt.encode(token_payload, settings.secret_key, algorithm=settings.algorithm)

            return token
        except Exception as e:
            raise Exception(f"Login failed: {str(e)}")


