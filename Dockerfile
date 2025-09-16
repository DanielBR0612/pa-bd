# Dockerfile

# 1. Use uma imagem base oficial do Python
FROM python:3.11-slim

# 2. Defina o diretório de trabalho dentro do container
WORKDIR /app

RUN pip install psycopg2-binary

# 4. Copie o resto do código da sua aplicação para o container
COPY . .

# 5. Defina o comando que será executado quando o container iniciar
CMD ["python", "sistema_vendas_cli.py"]