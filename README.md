# PharmaAssist AI

A simple AI-powered pharmaceutical product intelligence assistant for small pharmacy retailers and distributors.

## Features

- Chat interface to ask questions about medicines
- Search product catalog
- Inventory dashboard with low-stock alerts
- AI-generated product summaries using Google Gemini
- Clear distinction between database information and AI-generated content

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Google Gemini API key

### Local Development

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd pharmaassist-ai
   ```

2. Create `.env` file:
   ```bash
   cp .env.example .env
   ```

3. Add your Gemini API key to `.env`:
   ```
   GEMINI_API_KEY=your_key_here
   ```

4. Start the application:
   ```bash
   docker compose up --build
   ```

5. Open browser:
   ```
   http://localhost:8000
   ```

## Project Structure

```
pharmaassist-ai/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── services/
│   │   └── gemini.py     # Gemini API integration
│   └── requirements.txt
├── data/
│   └── medicines.json    # Product database
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── tests/
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## API Endpoints

- `GET /health` - Health check
- `GET /api/medicines` - Get all medicines
- `GET /api/medicines/search?q=query` - Search medicines
- `POST /api/chat` - Chat with AI assistant

## Testing

Run tests:
```bash
pytest
```

## Demo Scenario

1. Open http://localhost:8000
2. Ask "What is Pantop 40?"
3. Search for "Azithro"
4. View low-stock items
5. Ask "What medicines are low in stock?"

## Tech Stack

- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Backend**: Python, FastAPI, Uvicorn
- **AI**: Google Gemini API
- **Database**: JSON (no SQL)
- **Container**: Docker, Docker Compose

## Database

### Testing (Phase 1)
- `data/medicines_test.json` - Test database with 20 sample products for development

### Production (When Ready)
- `data/medicines.json` - Real product database (not tracked in git)
- The backend automatically loads `medicines_test.json` if it exists, otherwise `medicines.json`
- Copy your real products to `data/medicines.json` to use them

## Notes

- No authentication in V1
- No database persistence (JSON only)
- No vector search
- Minimal dependencies

## Future Enhancements (Not in V1)

- PostgreSQL database
- Authentication
- Vector embeddings for semantic search
- Redis caching
- AWS deployment
- Advanced reporting
