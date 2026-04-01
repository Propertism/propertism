# 🚀 Phase 1: Project Setup Guide

**Project**: New Propertism Website  
**Duration**: 2 weeks  
**Status**: Ready to Execute

---

## 📋 Overview

This guide walks you through setting up the complete project structure for the new Propertism website.

---

## 🛠️ Prerequisites

Before starting, ensure you have:

- Node.js 18+ installed
- Python 3.11+ installed
- PostgreSQL 15+ installed
- Git installed
- GitHub account
- Vercel account
- Render account

---

## 📁 Step 1: Create Project Structure

```bash
# Navigate to your development directory
cd C:\tamil

# Create main project directory
mkdir realtor
cd realtor

# Create subdirectories
mkdir frontend backend database docs docker

# Verify structure
ls -la
```

**Expected Structure:**
```
realtor/
├── frontend/
├── backend/
├── database/
├── docs/
└── docker/
```

---

## 🎨 Step 2: Initialize Frontend (React + TypeScript)

```bash
# Navigate to frontend directory
cd frontend

# Create React TypeScript project with Vite
npm create vite@latest . -- --template react-ts

# Answer prompts:
# - Project name: realtor-frontend
# - Select a variant: React + TypeScript

# Install dependencies
npm install

# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer

# Initialize Tailwind
npx tailwindcss init -p
```

### Configure Tailwind CSS

Edit `tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Edit `src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Create Folder Structure

```bash
# Create component directories
mkdir -p src/components/{layout,ui,properties,forms,dashboard}
mkdir -p src/pages
mkdir -p src/services
mkdir -p src/hooks
mkdir -p src/types
```

### Test Frontend Setup

```bash
# Start development server
npm run dev

# Open browser to http://localhost:5173
# You should see the Vite + React + TypeScript welcome page
```

---

## 🔧 Step 3: Initialize Backend (FastAPI + Python)

```bash
# Navigate to backend directory
cd ../backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
# source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic-settings
pip install alembic python-jose[cryptography] passlib[bcrypt]
pip install python-multipart python-dotenv
```

### Create Folder Structure

```bash
# Create app directory structure
mkdir -p app/api/v1/endpoints
mkdir -p app/core
mkdir -p app/models
mkdir -p app/schemas
mkdir -p app/database
```

### Create Basic Files

**`app/main.py`:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Propertism API",
    description="Real Estate Property Management API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Propertism API v1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**`app/core/config.py`:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = 24
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**`app/database/session.py`:**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**`app/core/security.py`:**
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from ..core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRY_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception
```

### Test Backend Setup

```bash
# Start development server
uvicorn main:app --reload

# Open browser to http://localhost:8000
# You should see the API documentation
```

---

## 🗄️ Step 4: Initialize Database (PostgreSQL + Alembic)

```bash
# Navigate to database directory
cd ../database

# Initialize Alembic
alembic init migrations
```

### Configure Alembic

Edit `alembic.ini`:
```ini
sqlalchemy.url = postgresql://user:password@localhost:5432/propertism_dev
```

Edit `migrations/env.py`:
```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

config = context.config
fileConfig(config.config_file_name)

target_metadata = None

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Create Development Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE propertism_dev;
CREATE USER propertism_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE propertism_dev TO propertism_user;
\q
```

---

## 🐳 Step 5: Setup Docker (Optional but Recommended)

```bash
# Navigate to docker directory
cd ../docker
```

### Create Docker Compose

**`docker-compose.yml`:**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: propertism_postgres
    environment:
      POSTGRES_USER: propertism_user
      POSTGRES_PASSWORD: your_password
      POSTGRES_DB: propertism_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build:
      context: ../backend
      dockerfile: Dockerfile
    container_name: propertism_backend
    environment:
      DATABASE_URL: postgresql://propertism_user:your_password@postgres:5432/propertism_dev
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  frontend:
    build:
      context: ../frontend
      dockerfile: Dockerfile
    container_name: propertism_frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend

volumes:
  postgres_data:
```

**`backend/Dockerfile`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**`frontend/Dockerfile`:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

---

## 📝 Step 6: Setup Version Control

```bash
# Navigate to project root
cd ../..

# Initialize Git repository
git init

# Create .gitignore
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Node
node_modules/
dist/
dist-ssr/
*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment
.env
.env.local
.env.*.local

# Database
*.db
*.sqlite
*.sqlite3

# Logs
logs/
*.log
EOF

# Create README.md
cat > README.md << EOF
# Propertism - Modern Real Estate Platform

A modern, scalable real estate property management platform.

## Tech Stack

- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Backend**: Python FastAPI + PostgreSQL
- **DevOps**: Docker + GitHub Actions

## Quick Start

### Development

\`\`\`bash
# Setup frontend
cd frontend
npm install
npm run dev

# Setup backend
cd ../backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
\`\`\`

## Documentation

- [Implementation Plan](IMPLEMENTATION_PLAN.md)
- [Project Board](PROJECT_BOARD.md)
- [API Documentation](BACKEND_API_SPEC.md)
- [Frontend Routes](FRONTEND_ROUTES.md)

## License

MIT
EOF

# Create initial commit
git add .
git commit -m "Initial commit: Project setup complete"
```

---

## ✅ Verification Checklist

After completing all steps, verify:

- [ ] Frontend runs on http://localhost:5173
- [ ] Backend runs on http://localhost:8000
- [ ] API docs available at http://localhost:8000/docs
- [ ] PostgreSQL running on localhost:5432
- [ ] Docker Compose works (if configured)
- [ ] Git repository initialized
- [ ] README.md created
- [ ] .gitignore created

---

## 🎯 Next Steps

Once setup is complete:

1. **Review the setup** - Ensure everything works
2. **Create GitHub repository** - Push code to GitHub
3. **Begin Phase 2** - Start database design
4. **Set up GitHub Projects** - Create task board

---

**Setup Complete! Ready to start development. 🚀**
