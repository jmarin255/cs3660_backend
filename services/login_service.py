import hashlib
import jwt
import datetime
from repositories.user_repository import UserRepository


SECRET_KEY= "your_secret_key_your_secret_key_your_secret_key_your_secret_key" 
ALGORITHM="HS256"


class LoginService:
    @staticmethod
    def get_login_token(username: str, password: str) -> str:
        user=UserRepository.get_user_by_username(username)
        if not user:
            raise Exception("User not found")
        

        hashed_password= hashlib.sha256(password.encode()).hexidigest

        if user.password_hash!= hashed_password:
            raise Exception("Invalid credentials")
        
        user_payload={
            "username": user.username,
            "name": user.name
        }

        expiration_time=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=1)
        token_payload={
            "sub": user.username,
            "exp": expiration_time,
            "user": user_payload
        }
        token=jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
        return token
    