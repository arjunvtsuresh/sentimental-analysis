import os
from fastapi import HTTPException

def verify_api_key(api_key: str):
    if api_key != os.getenv("API_KEY", "mysecretkey"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return True