# Sistema de Agendamento de Veículos

Sistema web para gerenciamento de frota de veículos empresarial com controle de acesso por usuários.

## Stack

- **Backend:** Python 3, Flask, SQLAlchemy, Flask-Migrate, Alembic
- **Frontend:** Bootstrap 5, Bootstrap Icons, Jinja2, FullCalendar
- **Banco de Dados:** PostgreSQL (produção) / SQLite (desenvolvimento)
- **Deploy:** Render

## Módulos

- ✅ Dashboard
- ✅ Veículos (CRUD completo + exclusão lógica + reativação)
- ✅ Agendamentos (CRUD + validação de conflito de horários)
- ✅ Calendário (FullCalendar com modal de detalhes)
- ✅ Agenda (visão operacional)
- ✅ Manutenções (CRUD completo + integração com status do veículo)
- ✅ Relatórios (utilização da frota)
- ✅ Configurações (informações do sistema)
- ✅ Usuários e Autenticação (login, permissões, níveis de acesso)

## Níveis de Acesso

| Papel | Permissões |
|-------|-----------|
| **Administrador** | Acesso total: veículos, manutenções, usuários, todos os agendamentos |
| **Usuário Comum** | Visualiza tudo, cria/edita/exclui apenas seus próprios agendamentos |
| **Não logado** | Apenas tela de login |

## Arquitetura

```
Routes → Services → Models → Banco de Dados
```

## Instalação

```bash
# Clone o repositório
git clone https://github.com/GreisonRohr/agendamento-veiculos.git
cd agendamento-veiculos

# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env

# Criar banco de dados
flask db init
flask db migrate -m "initial"
flask db upgrade

# Criar usuários iniciais (admin + usuário comum)
python criar_admin.py

# Executar
python run.py
```

## Acesso Inicial

Após executar `python criar_admin.py`, use:

| E-mail | Senha | Tipo |
|--------|-------|------|
| admin@garagemlab.com | admin123 | Administrador |
| usuario@garagemlab.com | usuario123 | Usuário Comum |

## Deploy no Render

1. Crie um novo Web Service no Render
2. Conecte o repositório GitHub
3. Configure as variáveis de ambiente:
   - `SECRET_KEY`
   - `DATABASE_URL` (PostgreSQL do Render)
4. Defina o comando de start: `gunicorn run:app`

## Licença

MIT
