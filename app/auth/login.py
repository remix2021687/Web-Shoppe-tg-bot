import requests

def auth_login(username:str, password:str):
    url:str = 'http://localhost:8000/api/auth/login/'
    payload = {'username': username, 'password': password}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        token_response = response.json().get('access')

        return token_response
    else:
        return None