import requests
import json

def menu():
    print("Escolha uma opção:")
    print("1 - signup   2 - login.  3 - testar o token:")
    
    return int(input())

URL = ''
URL_signup = "http://127.0.0.1:8000/api/signup/" 
URL_login = "http://127.0.0.1:8000/api/login/"
URL_test = "http://127.0.0.1:8000/api/test_token/"

def main():
    op = 0
    while op != 3:
        op = menu()
        if op == 1:
            URL = URL_signup
            signup(URL)
        if op == 2:
            URL = URL_login
            login(URL)
        if op == 3:
            URL = URL_test
            if not token_salvo:
                print("\nERRO: Você precisa fazer login (Opção 2) primeiro.")
            else:
                testar_token(URL, token_salvo)
        

def signup(URL):
    username = str(input("Digite o seu username: "))
    senha = str(input("Digite a sua senha: "))
    email = str(input("Digite o seu email"))
    
    novo_usuario = {
        "username": username,
        "password": senha,
        "email": email
    }
    
    requisicao(URL, novo_usuario)

def login(URL):
    username = str(input("Digite o seu username: "))
    senha = str(input("Digite a sua senha: "))
    
    usuario = {
        "username": username,
        "password": senha,
    }
    
    requisicao(URL, usuario)

def testar_token(URL, token):
    print(f"\nEnviando requisição GET para {URL} com token {token}")
    
    headers = {
        'Authorization': f'Token {token}'
    }
    
    try:
        response = requests.get(URL, headers=headers)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            print("RESPOSTA (sucesso):")
            print(response.text) 
        else:
            print("RESPOSTA (falha):")
            print(response.text) 

    except requests.exceptions.ConnectionError:
        print(f"\nERRO: Não foi possível conectar a {URL}")

    
def requisicao(URL, user):
    global token_salvo
    try:
        response = requests.post(URL, json=user)
        
        print(f"\nStatus Code: {response.status_code}")
        
        try:
            resposta_json = response.json()
            print("Resposta do Servidor (JSON):")
            print(json.dumps(response.json(), indent=2))
            
            if 'token' in resposta_json and response.status_code in [200]:
                token_salvo = resposta_json['token']
                print(f"\n--- TOKEN SALVO: {token_salvo} ---")
                
        except requests.exceptions.JSONDecodeError:
            print("Resposta do Servidor (Texto):")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print(f"\nERRO: Não foi possível conectar a {URL}")
        print("Verifique se o seu servidor Django está rodando (python manage.py runserver)")
    
main()