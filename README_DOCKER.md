# Docker Instructions — Sai Baba Guidance Chatbot

This document explains how to build and run the chatbot API using Docker and docker-compose.

## Build the Docker image

Build a local image named `sai-chatbot`:

```bash
docker build -t sai-chatbot .
```

## Run the container (single)

```bash
# Run container mapping host port 8000 to container port 8000
docker run --rm -p 8000:8000 \
  -v "${PWD}/data:/app/data" \
  -e PORT=8000 \
  sai-chatbot
```

Notes:
- `-v "${PWD}/data:/app/data"` mounts your local `data/` (PDFs, sample_teachings.txt) into the container so the app can read sources.
- Use `--rm` for a temporary container (it will be removed when stopped).

## Run with docker-compose

```bash
docker-compose up --build
```

To run in background:

```bash
docker-compose up -d --build
```

To stop:

```bash
docker-compose down
```

## Healthcheck and API endpoints

- Health: `http://localhost:8000/health`
- Interactive API docs: `http://localhost:8000/docs`
- POST `/ask` accepts JSON `{ "question": "...", "language": "en" }`

Example curl POST:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"How should I live? as god", "language":"en"}'
```

Example GET:

```bash
curl "http://localhost:8000/ask?question=What%20is%20devotion?&language=en"
```

## Rebuilding vector DB / indexes

If you remove `vector_db/index.faiss` or `index.pkl` or rebuild the `data/` folder, re-run the ingestion pipeline (on the host or inside container) to regenerate the vector index. Example (host):

```bash
python ingest.py
```

Or inside the running container (container name from `docker ps`):

```bash
docker exec -it <container-name> python ingest.py
```

## Environment and scaling notes

- The `Dockerfile` uses the `requirements.txt` from the repository — ensure it contains required libs for FAISS or embeddings if you need vector search.
- For production, consider running with multiple workers or behind a reverse proxy (NGINX) and enable TLS.
- If you require GPU acceleration or specialized libs (FAISS with GPU), the Dockerfile needs additional changes and a GPU-enabled base image.

## Troubleshooting

- If container fails with import errors, check `requirements.txt` contains missing packages and rebuild the image.
- If long retrieval outputs are too large for frontend, enable summarization in `ask.py` or add a post-processing step before returning results.

## Questions for Frontend

- Do you want a short/concise answer (1–2 sentences) or longer passages from sources? I can add a `summary` flag in the API.
- Confirm the frontend expects JSON in the shape: `{answer, language, sources, is_safe}` — that's what `/ask` returns.

---

If you want, I can also add a `README_DOCKER.md` link in the main `README.md` or create a `docker-compose.override.yml` with environment variables for production.