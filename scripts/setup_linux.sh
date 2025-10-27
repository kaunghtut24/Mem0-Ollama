#!/usr/bin/env bash
set -e
echo "Linux setup helper — will attempt to install python and node if missing (user confirmation needed)."

# Check for python3
if ! command -v python3 &>/dev/null; then
  echo "python3 not found. Please install Python 3.10+ (apt, yum, or your distro package manager)."
else
  echo "python3 found: $(python3 --version)"
fi

# Check for pip
if ! command -v pip3 &>/dev/null; then
  echo "pip3 not found. Attempting to install pip3..."
  python3 -m ensurepip --upgrade || echo "Please install pip manually."
fi

# Check for node
if ! command -v node &>/dev/null; then
  echo "node not found. Please install Node.js 18+ from https://nodejs.org/ or your package manager."
else
  echo "node found: $(node --version)"
fi

echo ""
echo "To continue:"
echo "1) Install and run Ollama: https://ollama.com/docs (use `ollama pull <model>` then `ollama run <model>`)"
echo "2) Start OpenMemory: either use their official run.sh, or `scripts/start_openmemory_docker.sh` included in this repo."
echo "3) Copy .env.example to .env and edit values."
echo "4) For Python example:"
echo "   python3 -m venv venv && source venv/bin/activate"
echo "   pip install -r python_example/requirements.txt"
echo "   python python_example/test_mem0_ollama.py"
echo "5) For Node example:"
echo "   cd node_example && npm install"
echo "   node node_example/test_mem0_ollama.js"
