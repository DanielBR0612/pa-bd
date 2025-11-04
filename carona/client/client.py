import requests
import json
from datetime import datetime
from typing import Optional, Dict, List

class CaronaCLI:
    """CLI para interagir com a API de Carona Compartilhada"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Faz requisição HTTP para a API"""
        url = f"{self.base_url}/{endpoint}"
        try:
            if method == "GET":
                response = self.session.get(url)
            elif method == "POST":
                response = self.session.post(url, json=data)
            elif method == "PUT":
                response = self.session.put(url, json=data)
            elif method == "DELETE":
                response = self.session.delete(url)
            
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return {}
    
    def listar_caronas(self):
        """Lista todas as caronas disponíveis"""
        print("\nCARONAS DISPONÍVEIS")
        print("=" * 80)
        
        caronas = self._make_request("GET", "caronas/disponiveis/")
        
        if not caronas:
            print("Nenhuma carona disponível no momento.")
            return
        
        for carona in caronas:
            print(f"\nID: {carona['id']}")
            print(f"   Origem: {carona['origem']} → Destino: {carona['destino']}")
            print(f"   Motorista: {carona['motorista_nome']}")
            print(f"   Data/Hora: {carona['data_hora_saida']}")
            print(f"   Vagas: {carona['vagas_disponiveis']}")
            print(f"   Preço: R$ {carona['preco_por_pessoa']}")
            if carona['observacoes']:
                print(f"   Obs: {carona['observacoes']}")
    
    def criar_carona(self):
        """Cria uma nova carona"""
        print("\nCRIAR NOVA CARONA")
        print("=" * 80)
        
        try:
            motorista_id = int(input("ID do motorista: "))
            veiculo_id = int(input("ID do veículo: "))
            origem = input("Origem: ")
            destino = input("Destino: ")
            data_hora = input("Data/Hora de saída (YYYY-MM-DD HH:MM): ")
            vagas = int(input("Vagas disponíveis: "))
            preco = float(input("Preço por pessoa: "))
            observacoes = input("Observações (opcional): ")
            
            data = {
                "motorista": motorista_id,
                "veiculo": veiculo_id,
                "origem": origem,
                "destino": destino,
                "data_hora_saida": data_hora,
                "vagas_disponiveis": vagas,
                "preco_por_pessoa": preco,
                "observacoes": observacoes,
                "status": "DISPONIVEL"
            }
            
            resultado = self._make_request("POST", "caronas/", data)
            
            if resultado:
                print(f"\nCarona criada com sucesso! ID: {resultado.get('id')}")
            else:
                print("\nErro ao criar carona.")
                
        except ValueError:
            print("Erro: Valores inválidos inseridos.")
    
    def solicitar_carona(self):
        """Solicita participação em uma carona"""
        print("\nSOLICITAR CARONA")
        print("=" * 80)
        
        try:
            carona_id = int(input("ID da carona: "))
            passageiro_id = int(input("ID do passageiro: "))
            num_lugares = int(input("Número de lugares solicitados: "))
            
            data = {
                "carona": carona_id,
                "passageiro": passageiro_id,
                "num_lugares": num_lugares,
                "status": "PENDENTE"
            }
            
            resultado = self._make_request("POST", "solicitacoes/", data)
            
            if resultado:
                print(f"\nSolicitação enviada com sucesso! ID: {resultado.get('id')}")
            else:
                print("\nErro ao solicitar carona.")
                
        except ValueError:
            print("Erro: Valores inválidos inseridos.")
    
    def listar_solicitacoes(self):
        """Lista todas as solicitações"""
        print("\nSOLICITAÇÕES")
        print("=" * 80)
        
        solicitacoes = self._make_request("GET", "solicitacoes/")
        
        if not solicitacoes.get('results'):
            print("Nenhuma solicitação encontrada.")
            return
        
        for sol in solicitacoes['results']:
            print(f"\n🎫 ID: {sol['id']}")
            print(f"   Carona: {sol['carona_info']}")
            print(f"   Passageiro: {sol['passageiro_nome']}")
            print(f"   Lugares: {sol['num_lugares']}")
            print(f"   Status: {sol['status']}")
            print(f"   Data: {sol['data_solicitacao']}")
    
    def gerenciar_solicitacao(self):
        """Aceitar ou recusar solicitação"""
        print("\nGERENCIAR SOLICITAÇÃO")
        print("=" * 80)
        
        try:
            sol_id = int(input("ID da solicitação: "))
            acao = input("Ação (aceitar/recusar): ").lower()
            
            if acao not in ['aceitar', 'recusar']:
                print("Ação inválida!")
                return
            
            resultado = self._make_request("POST", f"solicitacoes/{sol_id}/{acao}/")
            
            if resultado:
                print(f"\nSolicitação {acao}a com sucesso!")
            else:
                print(f"\n Erro ao {acao} solicitação.")
                
        except ValueError:
            print("Erro: Valores inválidos inseridos.")
    
    def criar_veiculo(self):
        """Cadastra um novo veículo"""
        print("\nCADASTRAR VEÍCULO")
        print("=" * 80)
        
        try:
            motorista_id = int(input("ID do motorista: "))
            modelo = input("Modelo: ")
            marca = input("Marca: ")
            cor = input("Cor: ")
            ano = int(input("Ano: "))
            placa = input("Placa: ")
            num_lugares = int(input("Número de lugares: "))
            
            data = {
                "motorista": motorista_id,
                "modelo": modelo,
                "marca": marca,
                "cor": cor,
                "ano": ano,
                "placa": placa,
                "num_lugares": num_lugares,
                "ativo": True
            }
            
            resultado = self._make_request("POST", "veiculos/", data)
            
            if resultado:
                print(f"\nVeículo cadastrado com sucesso! ID: {resultado.get('id')}")
            else:
                print("\n Erro ao cadastrar veículo.")
                
        except ValueError:
            print(" Erro: Valores inválidos inseridos.")
    
    def menu_principal(self):
        """Menu principal do CLI"""
        while True:
            print("\n" + "=" * 80)
            print("SISTEMA DE CARONA COMPARTILHADA - CLI")
            print("=" * 80)
            print("1. Listar caronas disponíveis")
            print("2. Criar nova carona")
            print("3. Solicitar carona")
            print("4. Listar solicitações")
            print("5. Gerenciar solicitação (aceitar/recusar)")
            print("6. Cadastrar veículo")
            print("0. Sair")
            print("=" * 80)
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.listar_caronas()
            elif opcao == "2":
                self.criar_carona()
            elif opcao == "3":
                self.solicitar_carona()
            elif opcao == "4":
                self.listar_solicitacoes()
            elif opcao == "5":
                self.gerenciar_solicitacao()
            elif opcao == "6":
                self.criar_veiculo()
            elif opcao == "0":
                print("\n FIM!")
                break
            else:
                print("\n Opção inválida!")
            
            input("\nPressione ENTER para continuar...")


def main():
    """Função principal"""
    cli = CaronaCLI()
    cli.menu_principal()


if __name__ == "__main__":
    main()