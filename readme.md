# Enterprise Policy Assistant (RAG)

A local Retrieval-Augmented Generation (RAG) application for internal knowledge management. It uses AWS Bedrock for embeddings + LLMs, PostgreSQL with pgvector for vector search, and Streamlit for the UI.

## What This App Does

- Ingests PDFs/DOCX/TXT documents into a pgvector table
- Retrieves relevant chunks using semantic similarity
- Generates a grounded answer using a Bedrock model

## Prerequisites

- Python 3.9+
- PostgreSQL 13+ with `pgvector` extension
- AWS Bedrock access enabled for:
  - Embeddings model (default: Titan)
  - LLM model (default: Mistral 7B instruct)

## Quick Start (Clone + Run)

```bash
git clone <your-repo-url>
cd hr_portal_rag
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configure Environment

Create `.env` from the template and set your DB settings:

```bash
cp .env.example .env
```

Example `.env` (only DB shown below):

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hr_portal
DB_USER=postgres
DB_PASSWORD=your_password
```

If you use AWS CLI profiles for credentials, keep `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` empty. Bedrock will resolve credentials from your configured profile.

## Enable pgvector (One-Time)

Run once on your database (with a user that can create extensions):

```bash
psql -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -U "$DB_USER" -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

## Ingest Documents

Put your docs under `data/sample_documents/` (or any folder), then run:

```bash
python ingest.py --data-dir data/sample_documents
```

- `--reset` clears existing embeddings first.

## Launch the App

```bash
streamlit run app/streamlit_app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true
```

Open in your browser:

- `http://localhost:8501`


## Resync Documents

Put your docs under `data/sample_documents/` (or any folder), then run:

```bash
python ingest.py --data-dir data/sample_documents --reset
```

- `--reset` clears existing embeddings first.

## Common Issues

**1) `vector type not found in the database`**
- The pgvector extension isn’t enabled. Run the one-time SQL above.

**2) `relation \"documents\" does not exist`**
- Run ingestion at least once so the schema is created.

**3) `AccessDeniedException` for Bedrock model**
- Your AWS account doesn’t have access to the model. Enable it in the Bedrock console or pick a model you are subscribed to.

**4) `No results returned`**
- Ensure ingestion succeeded.
- Re-run: `python ingest.py --data-dir data/sample_documents --reset`

## Project Layout

```
hr_portal_rag/
├── app/                    # Streamlit UI
├── src/                    # Core RAG pipeline
├── scripts/                # DB setup + batch ingest
├── data/                   # Documents
├── ingest.py               # CLI ingest
└── requirements.txt
```

## Notes

- The app is configured to use Mistral by default in `.env.example`:
  - `BEDROCK_LLM_MODEL=mistral.mistral-7b-instruct-v0:2`
- Change `BEDROCK_LLM_MODEL` in `.env` to any Bedrock model ID you are subscribed to.
