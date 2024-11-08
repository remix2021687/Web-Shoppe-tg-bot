import os
import jwt
import requests

from dotenv import load_dotenv

load_dotenv()


def authorization(username: str, password: str) -> dict | None:
    url: str = 'http://localhost:8000/api/auth/login/'
    payload: dict = {'username': username, 'password': password}
    headers: dict = {'Content-Type': 'application/json'}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        token_response: dict = response.json()

        return token_response
    else:
        return None


def refresh_token(token: str) -> str | None:
    url: str = 'http://localhost:8000/api/auth/login/refresh/'
    payload: dict = {'refresh': token}
    headers: dict = {'Content-Type': 'application/json'}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        token_response: dict = response.json()

        return token_response['access']
    else:
        return None

def tokenization(token: str) -> bool:
    try:
        jwt.decode(token, f'{os.getenv('SECRET_KEY')}', algorithms=['HS256'])

        return True
    except jwt.ExpiredSignatureError:
        return False

    except jwt.InvalidTokenError:
        return False

