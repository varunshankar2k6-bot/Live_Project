from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt_utils import verify_access_token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
# Get current user from JWT
def get_current_user(
        token: str = Depends(oauth2_scheme)
):
    payload = verify_access_token(token)
    if payload is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    return payload


# Get current admin from JWT
def get_current_admin(
        token: str = Depends(oauth2_scheme)
):

    payload = verify_access_token(token)

    if payload is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    if payload.get("role") != "admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return payload