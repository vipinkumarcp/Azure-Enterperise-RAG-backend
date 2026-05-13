from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import jwt
from jose.exceptions import JWTError

import requests

from .config import settings

security = HTTPBearer()

ALGORITHMS = ["RS256"]

JWKS_URL = (
    f"https://login.microsoftonline.com/"
    f"{settings.AZURE_TENANT_ID}"
    f"/discovery/v2.0/keys"
)

jwks = requests.get(JWKS_URL).json()


def get_signing_key(token):

    unverified_header = jwt.get_unverified_header(token)

    kid = unverified_header.get("kid")

    for key in jwks["keys"]:
        if key["kid"] == kid:
            return key

    return None


def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
):

    token = credentials.credentials

    unverified_claims = jwt.get_unverified_claims(token)

    print(unverified_claims)

    try:
        

        signing_key = get_signing_key(token)

        if not signing_key:
            raise HTTPException(
                status_code=401,
                detail="Signing key not found"
            )

        payload = jwt.decode(
                token,
                signing_key,
                algorithms=ALGORITHMS,
                audience=settings.API_AUDIENCE,
                options={
                    "verify_iss": False
                }
            )

        valid_issuers = [
            f"https://sts.windows.net/{settings.AZURE_TENANT_ID}/",
            f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}/v2.0"
        ]

        if payload["iss"] not in valid_issuers:
            raise HTTPException(
                status_code=401,
                detail="Invalid issuer"
            )

        return payload

    except JWTError as e:

        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )