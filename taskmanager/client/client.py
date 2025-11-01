import requests
import json

def menu():
    print("Escolha uma opção:")
    print("1 - signup   2 - login:")
    
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
            test(URL)
        

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

def test(URL):
    response = requests.get(URL)
    
    print(f"\nStatus Code: { response.status_code}")
    try:
        print("Resposta do Servidor (JSON):")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.JSONDecodeError:
        # Se a resposta não for JSON (ex: um erro 500)
        print("Resposta do Servidor (Texto):")
        print(response.text)
    
def requisicao(URL, user):
    try:
        # Faz a requisição POST, enviando os dados como JSON
        response = requests.post(URL, json=user)
        
        # Imprime o código de status (ex: 200, 201, 400)
        print(f"\nStatus Code: {response.status_code}")
        
        # Tenta imprimir a resposta JSON formatada
        try:
            print("Resposta do Servidor (JSON):")
            print(json.dumps(response.json(), indent=2))
        except requests.exceptions.JSONDecodeError:
            # Se a resposta não for JSON (ex: um erro 500)
            print("Resposta do Servidor (Texto):")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print(f"\nERRO: Não foi possível conectar a {URL}")
        print("Verifique se o seu servidor Django está rodando (python manage.py runserver)")
    
main()