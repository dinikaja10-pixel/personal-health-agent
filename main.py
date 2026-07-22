import os
import httpx

from dotenv import load_dotenv
from fastapi import FastAPI

import secrets
from urllib.parse import urlencode

from fastapi.responses import RedirectResponse

load_dotenv()

app = FastAPI()

WHOOP_CLIENT_ID = os.getenv("WHOOP_CLIENT_ID")
WHOOP_CLIENT_SECRET = os.getenv("WHOOP_CLIENT_SECRET")
WHOOP_REDIRECT_URI = os.getenv("WHOOP_REDIRECT_URI")

ACCESS_TOKEN = None


@app.get("/")
def home():
    return {"message": "Dini Health API läuft!"}

@app.get("/login")
def login():
    state = secrets.token_urlsafe(6)[:8]

    params = {
        "client_id": WHOOP_CLIENT_ID,
        "redirect_uri": WHOOP_REDIRECT_URI,
        "response_type": "code",
        "scope": "read:recovery read:cycles read:sleep read:workout read:profile read:body_measurement",
        "state": state,
    }

    authorization_url = (
        "https://api.prod.whoop.com/oauth/oauth2/auth?"
        + urlencode(params)
    )

    return RedirectResponse(authorization_url)

@app.get("/callback")
def callback(code: str):
    global ACCESS_TOKEN

    token_url = "https://api.prod.whoop.com/oauth/oauth2/token"

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": WHOOP_CLIENT_ID,
        "client_secret": WHOOP_CLIENT_SECRET,
        "redirect_uri": WHOOP_REDIRECT_URI,
    }

    response = httpx.post(token_url, data=data)
    token_data = response.json()

    ACCESS_TOKEN = token_data.get("access_token")

    return {"message": "WHOOP erfolgreich verbunden"}

@app.get("/whoop/profile")
def whoop_profile():
    if not ACCESS_TOKEN:
        return {"error": "Noch nicht mit WHOOP verbunden"}

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = httpx.get(
        "https://api.prod.whoop.com/developer/v2/user/profile/basic",
        headers=headers
    )

    return response.json()

