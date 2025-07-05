from typing import Dict
from jose import jwt, JWTError
from core.config import settings

class JWTService:
    @staticmethod
    def decode_access_token(token: str) -> Dict | None:
        try:
            decoded_token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return decoded_token
        except JWTError:
            return None