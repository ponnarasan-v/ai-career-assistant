# AI Resume & Job Match Platform

A production-oriented, local-first AI application for comparing resumes against job descriptions. The platform is designed for a GitHub portfolio and resume showcase, with a FastAPI backend, Streamlit frontend, environment-based configuration, and centralized logging.

This repository currently implements **Milestone 1 only**: a working project skeleton with a health-checked API and a basic Streamlit application shell.

## Features

- FastAPI backend with automatic OpenAPI documentation
- `/health` endpoint for service status
- Streamlit frontend with a navigation sidebar
- Frontend health check against the FastAPI backend
- Configuration through `.env`
- Centralized application logging
- Modular folder structure prepared for incremental development

Planned product capabilities include resume upload, resume parsing, job matching, ATS scoring, semantic similarity, local Ollama-powered generation, and interview preparation.

## Tech Stack

- Python 3.12
- FastAPI
- Streamlit
- Pydantic Settings
- Uvicorn
- python-dotenv

Future milestones will add Ollama, sentence-transformers, FAISS, PyMuPDF, python-docx, Docker, and pytest.

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file:

```bash
copy .env.example .env
```

## Running Locally

Start the FastAPI backend:

```bash
uvicorn app.api.main:app --host 127.0.0.1 --port 8000 --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

In a second terminal, start the Streamlit app:

```bash
streamlit run app/ui/streamlit_app.py
```

Streamlit will display the project overview and the current FastAPI health status.

## Folder Structure

```text
ai-resume-job-match/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   └── health.py
│   │   └── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   ├── domain/
│   │   ├── models/
│   │   └── schemas/
│   ├── services/
│   ├── repositories/
│   ├── prompts/
│   ├── utils/
│   └── ui/
│       ├── components/
│       ├── pages/
│       └── streamlit_app.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── data/
│   ├── uploads/
│   ├── indexes/
│   └── skill_taxonomy/
├── docker/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Verification

Check the API health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "AI Resume & Job Match Platform",
  "version": "0.1.0",
  "environment": "development"
}
```
