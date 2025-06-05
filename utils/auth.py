import os
from fastapi import Header, HTTPException

def verify_token(authorization: str = Header(...)):
    expected = os.environ.get("API_AUTH_TOKEN")
    if not expected:
        raise HTTPException(status_code=500, detail="API_AUTH_TOKEN não configurado.")
    if authorization != f"Bearer {expected}":
        raise HTTPException(status_code=401, detail="Token inválido.")
