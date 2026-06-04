# SpecMem Example: Session Auth

A small, realistic repository that shows what an external memory layer for coding
agents actually does. It uses [SpecMem](https://github.com/SuperagenticAI/specmem)
with **Qdrant** as the vector store (running embedded, no server required) and a
local embedding model.

Ask a plain-English question about the codebase and get back the specifications,
decisions, and tests that constrain the change you are about to make. Not ten raw
text chunks, but the memory that matters.

## What you will see

This query:

```bash
uv run specmem query "What should I know before changing src/auth/service.py?" -k 5
```

returns the specs that constrain the change, ranked by relevance:

```
1. (0.581) session-auth/tasks.md    Task 4: refresh-token rotation in src/auth/service.py
2. (0.554) session-auth/design.md   Architecture: AuthService / SessionManager
3. (0.526) session-auth/design.md   Testing Strategy: tests/auth/test_session_expiry.py
4. (0.281) session-auth/design.md   Decision: inactivity expiry lives in SessionManager
5. (0.280) session-auth/design.md   Overview
```

The agent now knows the task that touches this file, the design rationale, and the
test that protects the behavior, before writing a single line.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (the only thing you install yourself).
- That is it. `uv` creates the environment and pulls in SpecMem for you.

> This project currently runs SpecMem from a local checkout next to this repo
> (see `pyproject.toml`). Clone both repositories side by side:
>
> ```
> parent/
> ├── specmem/          # https://github.com/SuperagenticAI/specmem
> └── specmem-example/  # this repo
> ```

## Quick start

Every command is a plain `uv run`, so you always see exactly what is running.
`uv` builds the environment automatically on first use.

**Step 1. Build the memory index (once).** This detects the specs and embeds them
into Qdrant. The first run also downloads the embedding model (about 80 MB).

```bash
uv run specmem scan .      # detect and type the spec blocks
uv run specmem build .     # embed them into Qdrant
```

**Step 2. Ask questions.** Fast and read-only.

```bash
uv run specmem query "What should I know before changing src/auth/service.py?" -k 5
uv run specmem query "why did we move off database sessions?" -k 3
```

**Step 3. Run the test the specs reference.**

```bash
uv run --with pytest pytest -q
```

### Make shortcuts (optional)

The same commands are wrapped in a `Makefile` for convenience. The Makefile also
sets `HF_HUB_OFFLINE=1` so queries load the cached model with no network calls and
no log noise.

| Shortcut | Runs |
|----------|------|
| `make setup` | `uv run specmem scan .` then `uv run specmem build .` |
| `make q1` | `uv run specmem query "What should I know before changing src/auth/service.py?" -k 5` |
| `make q2` | `uv run specmem query "why did we move off database sessions?" -k 3` |
| `make test` | `uv run --with pytest pytest -q` |

To get the same clean, offline output from the raw `uv` commands, export the flag
yourself first:

```bash
export HF_HUB_OFFLINE=1
```

## What is in here

```
.kiro/specs/
  session-auth/            The active feature: token auth with inactivity expiry
    requirements.md          user stories and acceptance criteria
    design.md                architecture, key decisions, testing strategy
    tasks.md                 implementation plan linked to requirements
  legacy-db-sessions/      The deprecated predecessor, kept for context
    requirements.md
    design.md
src/auth/
  service.py               AuthService: issues and validates access tokens
  session.py               SessionManager: owns sessions and inactivity expiry
tests/auth/
  test_session_expiry.py   protects the inactivity-expiry behavior
.specmem.toml              SpecMem config (vector store = qdrant)
```

The specs are written in the spec-driven format that agents like Kiro produce:
numbered requirements with acceptance criteria, a design document, and a task plan.
SpecMem treats them as structured, typed memory rather than loose Markdown.

## How it works

```
specs  ->  scan (detect & type)  ->  build (embed into Qdrant)  ->  query (retrieve)
```

1. **scan** reads the specs and classifies each block by type: requirement, design,
   decision, or task. Run `uv run specmem scan .` to see the breakdown.
2. **build** turns each block into an embedding with a local model
   (`all-MiniLM-L6-v2`) and stores it in Qdrant along with its type, source, and
   status.
3. **query** embeds your question, searches Qdrant, and returns the most relevant
   blocks with a similarity score and a link back to the source file.

Qdrant runs embedded and on-disk under `.specmem/vectordb/`, so there is no server
to start. The same configuration scales up to a Qdrant server or Qdrant Cloud by
setting one URL (see below).

## Try your own questions

```bash
uv run specmem query "how long do access tokens live?" -k 5
uv run specmem query "where is inactivity expiry enforced?" -k 5
uv run specmem query "what tests cover session expiry?" -k 5
```

Each result shows its similarity score, so you can see retrieval working rather
than taking it on faith.

## Run the test

The `session-auth` design points to `tests/auth/test_session_expiry.py` as the
test that protects inactivity expiry. You can run it:

```bash
uv run --with pytest pytest -q     # or: make test
```

This closes the loop the memory layer cares about: a requirement, the code that
implements it, and the test that guards it.

## Use a real Qdrant server (optional)

Embedded mode is perfect for local use. To point at a running Qdrant instead:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Then set the URL in `.specmem.toml` and rebuild:

```toml
[vectordb]
backend = "qdrant"
qdrant_url = "http://localhost:6333"
# qdrant_api_key = "..."   # or set QDRANT_API_KEY for Qdrant Cloud
```

```bash
uv run specmem build .     # or: make build
```

## Configuration

`.specmem.toml` controls the vector store and the embedding model:

```toml
[vectordb]
backend = "qdrant"           # embedded on-disk when qdrant_url is unset
path = ".specmem/vectordb"

[embedding]
provider = "local"           # no API key needed
model = "all-MiniLM-L6-v2"
```

## Troubleshooting

- **"No data in memory"**: run `uv run specmem build .` first.
- **Slow first run**: the embedding model (about 80 MB) downloads once and is then
  cached. Run `uv run specmem build .` while online the first time.
- **Network noise during a query**: set `export HF_HUB_OFFLINE=1` so the model
  loads from cache with no network calls (the `Makefile` does this for you). Cache
  the model once online first.

## About

An example of using SpecMem as an external memory layer for coding agents.
SpecMem is open source: https://github.com/SuperagenticAI/specmem
