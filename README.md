# Diário da Mulher

O **Diário da Mulher** é um site no qual, a partir de registros diários feitos pela usuária, o sistema identifica padrões do ciclo da violência em relacionamentos. O projeto visa auxiliar mulheres na percepção de comportamentos abusivos e oferecer dados que ajudem na tomada de decisões.

---

## Instalação e Configuração

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Passos para instalação

1. **Clone o repositório**

```bash
git clone <URL-do-repositório>
cd Diario-da-Mulher-main
```

2. **Crie um ambiente virtual**

```bash
python3 -m venv venv
```

3. **Ative o ambiente virtual**

Para shell bash/zsh:
```bash
source venv/bin/activate
```

Para shell fish:
```bash
source venv/bin/activate.fish
```

Para Windows (PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```

4. **Instale as dependências**

```bash
pip install -r requirements.txt
```

5. **Configure o banco de dados**

Apague o banco de dados "databe.db" e a pasta "migrations" (caso existam).

Escreva no terminal:

```bash
flask db init
flask db migrate
flask db upgrade
```

### Executando o projeto

1. **Inicie o servidor Flask**

```bash
python main.py
```

2. **Acesse a aplicação**

Abra seu navegador e acesse: http://127.0.0.1:5000

### Para encerrar a aplicação

Pressione `CTRL+C` no terminal onde a aplicação está sendo executada.

### Executando em próximas sessões

Sempre que quiser executar a aplicação novamente, siga estes passos:

1. Navegue até o diretório do projeto
2. Ative o ambiente virtual
3. Execute a aplicação

```bash
cd caminho/para/Diario-da-Mulher-main
source venv/bin/activate.fish  # ou outro comando de ativação adequado ao seu shell
python main.py
```

## Ferramentas para Desenvolvedores

Para facilitar o desenvolvimento e manutenção do projeto, disponibilizamos ferramentas específicas na pasta `development_tools`.

- [Documentação das Ferramentas de Desenvolvimento](development_tools/README.md) - Scripts para consulta e manutenção do banco de dados
