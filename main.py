import os

from dotenv import load_dotenv
from fastapi import FastAPI

import secrets
from urllib.parse import urlencode

from fastapi.responses import RedirectResponsegit

load_dotenv()

app = FastAPI()

WHOOP_CLIENT_ID = os.getenv("WHOOP_CLIENT_ID")
WHOOP_CLIENT_SECRET = os.getenv("WHOOP_CLIENT_SECRET")
WHOOP_REDIRECT_URI = os.getenv("WHOOP_REDIRECT_URI")


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

