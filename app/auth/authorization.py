import requests

def authorization(username:str, password:str) -> dict or None:
    url:str = 'http://localhost:8000/api/auth/login/'
    payload:dict = {'username': username, 'password': password}
    headers:dict = {'Content-Type': 'application/json'}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        token_response:dict = response.json()

        return token_response
    else:
        return None


def tokenization(token: str) -> bool:
    url:str = 'http://localhost:8000/api/shop-post/'
    headers:dict = {'Authorization': f'Bearer {token}'}

    request = requests.post(url, headers=headers)

    if request.status_code == 200:
        return True
    else:
        return False