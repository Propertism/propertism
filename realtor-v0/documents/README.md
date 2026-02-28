# 🏠 Propertism - Modern Real Estate Platform

A modern, scalable real estate property management platform built with React, TypeScript, and FastAPI.

---

## 🚀 Features

- **Property Management** - Browse, search, and view property listings
- **Inquiry System** - Contact property owners with inquiry forms
- **Maintenance Requests** - Track and manage maintenance requests
- **Support Tickets** - Customer support ticketing system
- **Construction Updates** - Real-time construction progress updates
- **User Dashboard** - Personalized user experience
- **Admin Panel** - Comprehensive management interface

---

## 🛠 Tech Stack

### Frontend
- React 18 + TypeScript
- Tailwind CSS
- React Router
- Axios
- React Hook Form + Zod
- React Query

### Backend
- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT Authentication

### DevOps
- Docker + Docker Compose
- GitHub Actions
- Vercel (Frontend)
- Render (Backend)

---

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL 15+
- Docker (optional)

---

## 🚀 Quick Start

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/realtor.git
cd realtor

# Setup frontend
cd frontend
npm install
npm run dev

# Setup backend
cd ../backend
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up --build
```

---

## 📁 Project Structure

```
realtor/
├── frontend/              # React application
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── types/
│   │   └── App.tsx
│   └── package.json
│
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── database/
│   ├── requirements.txt
│   └── main.py
│
├── database/              # PostgreSQL migrations
│   ├── migrations/
│   └── seed_data/
│
├── docs/                  # Documentation
└── README.md
```

---

## 📖 Documentation

- [Implementation Plan](IMPLEMENTATION_PLAN.md) - Detailed development plan
- [Project Board](PROJECT_BOARD.md) - Task tracking and milestones
- [Database Schema](docs/DATABASE_SCHEMA.md) - Database design
- [API Documentation](docs/API_DOCUMENTATION.md) - API endpoints

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 📞 Contact

For questions or support, contact us at:
- Email: info@propertism.com
- Phone: +91 86670 20798

---

**Built with ❤️ for modern real estate management**
