# AI Portfolio — Backend

FastAPI service behind the AI Portfolio chat. It answers questions about
Noorullah using a Groq LLM, with a local keyword router as the offline
fallback when no API key is configured.

## Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The server listens on port 8000 by default
(`uvicorn main:app --reload --port 8000` to be explicit).

## Configuration

| Variable | Required | Description |
| --- | --- | --- |
| `GROQ_API_KEY` | No | Groq API key. When unset, the server uses the local keyword router in `main.py` instead of the LLM. |
| `FRONTEND_URL` | No | Comma-separated list of allowed frontend origins for CORS. When unset, all origins are allowed (without credentials). |

Put variables in a `.env` file in this directory or export them in the
shell; `main.py` loads `.env` on startup.

## API

### `POST /api/chat`

Request body:

```json
{
  "query": "What projects has Noorullah built?",
  "history": [{ "role": "user", "content": "..." }]
}
```

- `query`: required, 1–2000 characters (blank queries are rejected).
- `history`: optional, up to 50 messages; each message is
  `{"role": "user" | "assistant", "content": "..."}` (1–4000 characters).

Returns `{"intent": "...", "ai_text": "..."}`. LLM calls time out after
30 seconds; the frontend gives up after 60 seconds.

## Knowledge base

Answers are grounded in `knowledge_base.md`, which is loaded into the
system prompt. The prompt is cached (`get_system_prompt` uses
`lru_cache`), so **restart the server after editing
`knowledge_base.md`** for changes to take effect.
