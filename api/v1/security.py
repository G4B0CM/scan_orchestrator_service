import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from application.services.jwt_service import JWTService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login") # Point to auth service's login

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> uuid.UUID:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = JWTService.decode_access_token(token)
    if payload is None:
        raise credentials_exception
        
    user_id_str = payload.get("user_id")
    if user_id_str is None:
        raise credentials_exception
        
    return uuid.UUID(user_id_str)