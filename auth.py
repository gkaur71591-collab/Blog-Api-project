from jose import jwt, JWTError
from datetime import datetime,timedelta,timezone
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from config import setting



SECRET_KEY=setting.SECRET_KEY
ALGORITHM=setting.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES=setting.ACCESS_TOKEN_EXPIRE_MINUTES
print(ACCESS_TOKEN_EXPIRE_MINUTES)

oauth2_schema=OAuth2PasswordBearer(tokenUrl="login")

# token create
def create_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

#verify token
def verify_token(token:str=Depends(oauth2_schema)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            details="Invalid token"
        )