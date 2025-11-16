# MVP Analyzer

Minimal analytical service MVP: fetches data from an external API, caches it, normalizes the dataset and returns an AI-based summary
via REST API.

## Full technical documentation

| Language        | Link                                                                 |
|-----------------|----------------------------------------------------------------------|
| English(.md)    | [Technical Documentation (ENG)](https://github.com/p95max/mvp-analyzer/blob/master/docs/Technical%20Documentation_ENG.md) |
| English(.pdf)   | [Technical Documentation (ENG)](https://github.com/p95max/mvp-analyzer/blob/master/docs/Technical%20documentation_ENG.pdf) |
| Ukrainian(.md)  | [Technical Documentation (UKR)](https://github.com/p95max/mvp-analyzer/blob/master/docs/Technical%20Documentation_UKR.md) |
| Ukrainian(.pdf) | [Technical Documentation (UKR)](https://github.com/p95max/mvp-analyzer/blob/master/docs/Technical%20documentation_UKR.pdf) |




**The service uses a public free test API (jsonplaceholder.typicode.com) as a mock external data source.**

## Stack

- Python 3.14
- FastAPI
- Pydantic v2
- httpx
- In-memory TTL cache
- Docker + Docker Compose v2
- Poetry

## Pipeline
`client → /analyze → fetch → cache → normalize → ai_summary → response`

External data is pulled from the free test endpoint:
https://jsonplaceholder.typicode.com/{resource}

## Testing (docker)
### Run container
```bash
    docker compose up
```
### Open http://127.0.0.1:8000/docs -> POST Analyze -> Try it out
Request example
```json
{
  "query": "posts",
  "options": {
    "max_sample_items": 5
  }
}
```
Response shape:
```json
{
  "status": "ok",
  "source_items": 100,
  "items_count": 100,
  "summary": "Dataset contains 100 items with fields: id, user_id, title, body. Example: ...",
  "sample": [ { "...": "..." } ]
}
```
## Testing (curl)
## curl Request example
```bash
    curl -X POST http://localhost:8000/analyze \
      -H "Content-Type: application/json" \
      -d '{"query": "posts", "options": {"max_sample_items": 10}}'
```