# TelegramThreadAI

## 🤖 Project Overview
TelegramThreadAI is a platform designed to enhance user connectivity on Telegram, facilitating engaging group conversations and interactions. It enables users to participate in group chats where AI-generated responses ensure meaningful and relevant discussions.

## 🌟 Features
- 🧠 AI-enhanced Telegram thread management
- 📊 Intelligent conversation context tracking
- 🤝 Group chat creation and management
- 🔒 Role-based access control
- 🤖 Configurable AI interaction triggers
- 🐳 Docker containerization

## 🚀 Chat Features
- Create public and private group chats
- Customize AI chat instructions
- Set AI response triggers:
  - Respond after specific message count
  - Respond after time interval
  - Quick @ai mention responses
- Invite and manage chat members
- Admin-level chat management

## 🛠 Technology Stack
- **Backend**: 
  - Python 3.12+
  - FastAPI
  - SQLAlchemy
  - Alembic (migrations)
  - Asyncpg (async database)
- **Frontend**:
  - React.js
  - TypeScript
  - Axios
- **Database**: 
  - PostgreSQL 16
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Testing**: 
  - Backend: pytest
  - Frontend: Jest, React Testing Library

## 🔐 Authentication
- Telegram Login Widget
- JWT tokens
- Dynamic profile creation/update
- Secure credential storage

## 📦 Prerequisites
- Docker 20.10+
- Python 3.12+
- Node.js 20+
- npm 8+

## 🚀 Quick Start

### Repository Cloning
```bash
git clone https://github.com/Teri-anric/TelegramThreadAI.git
cd TelegramThreadAI
```

### Environment Setup
1. Create `.env` files
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

2. Launch Application
   ```bash
   docker-compose up --build
   ```

### Local Development
- Backend: `http://localhost:8000`
- Swagger API: `http://localhost:8000/docs`
- Frontend: `http://localhost:3000`
- PostgreSQL: `localhost:5432`

## 🧪 Testing
```bash
# Backend tests
make test

# Linting
make lint
```

## 🌈 Architectural Solutions
- Microservice architecture
- Asynchronous programming
- Type checking and static code analysis
- Service responsibility separation

## 🤝 Project Contribution
Detailed instructions in [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License
Project is distributed under MIT License - details in [LICENSE](LICENSE)

## 🔗 Useful Links
- [Issue Tracker](https://github.com/yourusername/TelegramThreadAI/issues)

**⭐ Don't forget to star the project!** 