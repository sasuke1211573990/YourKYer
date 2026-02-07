# AI Post-Graduate Entrance Exam Platform

An AI-powered platform for post-graduate entrance exam information, Q&A, and recommendations.

## Features
- **Data Crawler**: Automatically scrapes authoritative sources for latest exam info.
- **AI Q&A**: Smart Q&A engine based on LLM/Knowledge Graph.
- **User System**: Personal profile, history, and notifications.
- **Data Visualization**: Structured database of universities and majors.

## Tech Stack
- **Backend**: Python FastAPI, PostgreSQL, Redis, Scrapy
- **Frontend**: Vue 3, Element Plus, Vite
- **Infrastructure**: Docker, Docker Compose

## Quick Start

1. **Start Services**
   ```bash
   docker-compose up -d --build
   ```

2. **Initialize Data**
   ```bash
   docker-compose exec backend python -m app.init_data
   ```

3. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

## Documentation
See [docs/deployment.md](docs/deployment.md) for detailed deployment instructions.
