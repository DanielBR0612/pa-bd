import requests
import json

def menu():
    print("Escolha uma opção:")
    print("1 - criar projeto  2 - listar projetos   3 - criar tarefa   4 - listar tarefas   5 - testar token:")
    
    return int(input())

URL = ''
URL_signup = "http://127.0.0.1:8000/api/signup/" 
URL_login = "http://127.0.0.1:8000/api/login/"
URL_test = "http://127.0.0.1:8000/api/test_token/"
URL_projetos = "http://127.0.0.1:8000/api/projetos/"
URL_tarefas = "http://127.0.0.1:8000/api/tarefas/"

def main():
    abrirconta = input("Gostaria de criar uma conta? (sim/não) ")
    if abrirconta.lower() == "sim":
        URL = URL_signup
        signup(URL)
    elif abrirconta.lower() == "nao":
        URL = URL_login
        login(URL)
        
    op = 0
    while op != 9:
        op = menu()
        if op == 1:
            URL = URL_projetos
            criar_projeto(URL, token_salvo)
        if op == 2:
            URL = URL_projetos
            requisicao_get(URL, token_salvo)
        if op == 3:
            URL = URL_tarefas
            criar_tarefa(URL, token_salvo)
        if op == 4:
            URL = URL_tarefas
            requisicao_get(URL, token_salvo)
        if op == 5:
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
    
    requisicao_conta(URL, novo_usuario)

def login(URL):
    username = str(input("Digite o seu username: "))
    senha = str(input("Digite a sua senha: "))
    
    usuario = {
        "username": username,
        "password": senha,
    }
    
    requisicao_conta(URL, usuario)

def criar_projeto(URL, token):
    try:
        nome = input("Digite o nome do projeto: ")
        descricao = input("Digite a descrição do projeto: ")
        
        projeto = {
            "nome": nome,
            "descricao_projeto": descricao
        }
        headers = {
            'Authorization': f'Token {token}'
        }
        
        response = requests.post(URL, json=projeto, headers=headers)
        
        print(f"\nStatus Code: {response.status_code}")
        try:
            print("Resposta do Servidor (JSON):")
            print(json.dumps(response.json(), indent=2))
        except requests.exceptions.JSONDecodeError:
            print("Resposta do Servidor (Texto):")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print(f"\nERRO: Não foi possível conectar a {URL}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def criar_tarefa(URL, token):
    titulo = str(input("Digite o titulo da tarefa: "))
    descricao = str(input("Digite a descricao da tarefa: "))
    id_projeto = int(input("Digite o id do projeto: "))
    
    tarefa = {
        "titulo": titulo,
        "descricao_tarefa": descricao,
        "projeto": id_projeto
    }
    
    headers = {
            'Authorization': f'Token {token}'
        }
    
    response = requests.post(URL, json=tarefa, headers=headers)
        
    print(f"\nStatus Code: {response.status_code}")
    try:
        print("Resposta do Servidor (JSON):")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.JSONDecodeError:
        print("Resposta do Servidor (Texto):")
        print(response.text)

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

    
def requisicao_get(URL, token):
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

def requisicao_conta(URL, user):
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