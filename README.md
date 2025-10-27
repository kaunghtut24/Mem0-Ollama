# Mem0 + Ollama Local Integration — Project Scaffold

This scaffold provides example code, setup scripts, and instructions to integrate **Mem0 / OpenMemory**
with **Ollama** as an LLM provider for a local chatbot. It includes both **Python** and **Node** examples,
setup scripts for **Linux** and **Windows (PowerShell)**, Docker guidance for running OpenMemory,
and placeholders for secrets and model names.

> NOTE: This repository is a scaffold to help you test locally. It **does not** install large LLM models for you.
> You must install and run Ollama and OpenMemory separately (instructions below).

## Contents
- `python_example/` — Python example chat handler that uses `mem0ai` configured to use Ollama.
- `node_example/` — Node/TypeScript example chat handler.
- `scripts/` — convenience scripts:
  - `scripts/setup_linux.sh` — Linux setup helper (installs deps where possible).
  - `scripts/setup_windows.ps1` — Windows PowerShell setup helper.
  - `scripts/start_openmemory_docker.sh` — Example to start OpenMemory using docker-compose (requires Docker).
- `docker/` — example docker-compose override (persistent volumes).
- `.env.example` — environment variable placeholders.
- `README.md` — this file.
- `LICENSE.txt` — MIT license for the scaffold.

## Quick overview (High level)
1. Install and run Ollama on your machine. Verify with `ollama ls` and `ollama run <model>`.
2. Start OpenMemory (self-hosted) — either use official `run.sh` or the included `docker` compose example.
3. Fill `.env` from `.env.example`.
4. Choose Python or Node example and run the test script. The scripts perform:
   - `memory.search()` using Mem0
   - Build prompt with retrieved memories
   - Calls your LLM via Mem0 configured to use Ollama
   - `memory.add()` to store new memories

## Windows and Linux
Follow the `scripts/setup_*` files to install prerequisites (Python, Node, pip packages, or npm packages) and to guide
you through starting Ollama and OpenMemory. The scripts include helpful comments and placeholders — run them in a terminal.

## Security & Persistence
- The `docker/docker-compose.override.yml` binds Qdrant and Postgres data to `./data/qdrant` and `./data/postgres` to avoid data loss.
- Do **not** commit real API keys or secrets. Use `.env` for secrets.

## Next steps
- Replace placeholder model names with your Ollama model (e.g., `mixtral:8x7b`).
- Optionally change the embedder provider or model.
- Add production hardening: API keys, TLS, backups, retention policies.

--- End of README
