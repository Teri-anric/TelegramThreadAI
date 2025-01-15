# Contributing to TelegramThreadAI

## 🌈 Welcome Contributors!

We value your contribution! Our goal is to make the contribution process as simple and transparent as possible.

## 🎯 Ways to Help
- 🐛 Bug reporting
- 💡 Feature suggestions
- 🔧 Fixing existing code
- 📖 Documentation improvements
- 🌐 Localization

## 🛠 Technical Requirements

### Development Environment
- Python 3.12+
- Node.js 20+
- Docker 20.10+
- PostgreSQL 13+

### 1. Environment Preparation
```bash
# Repository Cloning
git clone https://github.com/Teri-anric/TelegramThreadAI.git
cd TelegramThreadAI

# Backend Virtual Environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# Frontend Dependencies
cd frontend
npm install
```

### 2. Local Environment Setup
```bash
# Copy Configuration Example
cp .env.example .env

# Database Configuration
docker-compose -f docker-compose.dev.yml up -d postgres
```

### 3. Working with Code

#### Backend (Python)
- Using FastAPI
- Following PEP 8
- Type hinting
- Docstrings for all functions
- Testing with pytest

#### Frontend (React)
- TypeScript
- Functional Components style
- React Hooks
- CSS Modules styling

### 4. Running Tests
```bash
# Backend tests
make test

# Linting
make lint
```

### 5. Commits and Pull Requests
- Use conventional commits
- Examples:
  - `feat: add JWT authentication`
  - `fix: resolve memory leak in message stream`
  - `docs: update API documentation`

### 6. Code Review
- All PRs go through mandatory ReviewHub
- Minimum 1 approval from maintainers
- CI/CD testing of all tests

## 🏗 Conventions and Standards

### Branch Naming
- `feat/` - new features
- `fix/` - bug fixes(and code refactoring)
- `docs/` - documentation changes


### Commit Structure
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

## 🔒 Security
- Do not commit secret data
- Use `.env`

## 📜 Code of Conduct
- Mutual respect
- Constructive criticism
- Diversity and inclusivity

## 📄 License
By contributing, you agree to the MIT License terms.

**Happy Coding! 🚀** 