# Convenience shortcuts, driven entirely by uv.
#
# The embedding model is cached locally after the first build, so we run the
# Hugging Face stack in offline mode. This keeps the output clean (no network
# log noise) and works without network access.

export HF_HUB_OFFLINE := 1
export TRANSFORMERS_OFFLINE := 1
export TOKENIZERS_PARALLELISM := false

.PHONY: help setup scan build q1 q2 test clean

help:
	@echo "make setup   - build the memory index (run once)"
	@echo "make q1      - ask: what to know before changing the auth service"
	@echo "make q2      - ask: why we moved off database sessions"
	@echo "make scan    - show detected, typed spec blocks"
	@echo "make build   - rebuild the Qdrant-backed memory index"
	@echo "make test    - run the test that the specs reference"
	@echo "make clean   - remove the built index"

# One-time setup (downloads the embedding model on first run if needed).
setup: scan build

scan:
	uv run specmem scan .

build:
	uv run specmem build .

# Queries (fast, read-only, clean output).
q1:
	uv run specmem query "What should I know before changing src/auth/service.py?" -k 5

q2:
	uv run specmem query "why did we move off database sessions?" -k 3

# Run the unit test that the session-auth spec points to.
test:
	uv run --with pytest pytest -q

clean:
	rm -rf .specmem/vectordb
