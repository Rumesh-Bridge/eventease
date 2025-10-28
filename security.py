from passlib.context import CryptContext

# bcrypt hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_password_hash(password: str) -> str:
    """Return the bcrypt hash of the given password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


# JWT configuration
from datetime import datetime, timedelta
from jose import JWTError, jwt

# --- config for JWT ---
SECRET_KEY = "enventease-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    "Generate a JWT token for the given data"
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str,credentials_exception):
    "Verify a JWT token and return the data"
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        
        email: str | None = payload.get("sub")
        
        if email is None:
            raise credentials_exception
            
        return email
    
    except JWTError:
        
        raise credentials_exception


