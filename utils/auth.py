from datetime import datetime, timedelta
from jose import JWTError, jwt

# Secret key for signing JWTs (Keep it safe and secret in production)
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "H256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise ValueError("Invalid token payload")
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token {str(e)}")
    
