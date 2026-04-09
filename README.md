# AI Startup Idea Validator

## Description

An AI-powered tool that validates startup ideas with just a name and description. The AI automatically generates comprehensive analysis including:

- **Problem Statement** - What problem does this solve?
- **Target Customer** - Who will use this?
- **Market Analysis** - Market size and opportunity
- **Competitors** - Who else is in this space?
- **Tech Stack** - Recommended technologies
- **Risk Level** - Low/Medium/High assessment
- **Profitability Score** - 0-100 score

## Tech Stack

- **Backend:** FastAPI, SQLite, Uvicorn, ReportLab, python-dotenv
- **Frontend:** React + Vite, Tailwind CSS, React Router DOM, Axios
- **AI:** OpenRouter (GPT-3.5 Turbo)

## Features

✅ **Simple Input** - Just enter idea name and description
✅ **AI-Powered Analysis** - Automatic generation of all analysis fields
✅ **Comprehensive Reports** - Problem, Customer, Market, Competitors, Tech Stack, Risk, Score
✅ **Database Storage** - All ideas saved in SQLite
✅ **Dashboard** - Browse and manage all validated ideas
✅ **PDF Export** - Download professional reports
✅ **Delete Ideas** - Remove ideas you don't need

## Setup Instructions

### Backend Setup

```bash
cd server
python -m venv venv

# Windows CMD
venv\Scripts\activate

# Windows PowerShell
venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs on: `http://localhost:8000`

### Frontend Setup (New Terminal)

```bash
cd client
npm install
npm run dev
```

Frontend runs on: `http://localhost:5173`

## Environment Variables

The `.env` file in the `server` directory already contains an API key. If you want to use your own:

```
OPENROUTER_API_KEY=your_key_here
```

Get a free API key from [OpenRouter](https://openrouter.ai/)

## How to Use

1. **Home Page** - Enter your startup idea name and description
2. **Submit** - AI analyzes and generates all fields (takes 5-10 seconds)
3. **View Report** - See comprehensive validation report with:
   - Problem statement
   - Target customer analysis
   - Market opportunity
   - Competitor analysis
   - Recommended tech stack
   - Risk assessment
   - Profitability score
4. **Dashboard** - Browse all your validated ideas
5. **Export PDF** - Download professional reports
6. **Delete** - Remove ideas you don't need

## Example Input

**Idea Name:** EcoDelivery

**Idea Description:** A sustainable last-mile delivery service using electric vehicles and bicycles for urban areas. We partner with local restaurants and stores to provide carbon-neutral delivery options to environmentally conscious consumers.

**AI Will Generate:**
- Problem: High carbon emissions from traditional delivery services
- Customer: Environmentally conscious urban consumers aged 25-45
- Market: $50B last-mile delivery market with 15% annual growth
- Competitors: UberEats, DoorDash, Postmates
- Tech Stack: React Native, Node.js, PostgreSQL, Google Maps API
- Risk Level: Medium
- Profitability Score: 72/100

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ideas` | Create new idea (only name + description) |
| GET | `/ideas` | Get all ideas |
| GET | `/ideas/{id}` | Get single idea |
| DELETE | `/ideas/{id}` | Delete idea |
| GET | `/export/{id}` | Download PDF report |
| GET | `/` | Health check |

## Project Structure

```
├── server/                    # Backend (FastAPI)
│   ├── main.py               # Main application
│   ├── database.py           # Database configuration
│   ├── models.py             # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas
│   ├── ai_service.py         # AI analysis service
│   ├── pdf_service.py        # PDF generation
│   ├── routes/
│   │   ├── ideas.py          # CRUD endpoints
│   │   └── export.py         # PDF export
│   └── requirements.txt      # Python dependencies
│
├── client/                    # Frontend (React)
│   ├── src/
│   │   ├── App.jsx           # Main app
│   │   ├── pages/            # Page components
│   │   ├── components/       # Reusable components
│   │   └── api/              # Axios config
│   └── package.json          # Node dependencies
│
└── startup_ideas.db          # SQLite database (auto-created)
```

## Architecture Decisions

- **SQLite** - Simple deployment without database server
- **FastAPI** - Async performance and automatic API docs
- **OpenRouter** - Flexible AI access with multiple models
- **Simplified Input** - Only 2 fields required, AI generates everything else
- **Structured AI Prompts** - Ensures consistent, high-quality analysis

