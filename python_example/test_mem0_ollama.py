"""Python test script for Mem0 + Ollama integration.

- Configure .env (see .env.example)
- This script demonstrates:
  - Creating a Memory client configured to use Ollama
  - Searching memories
  - Building a prompt and simulating an LLM call via Mem0 config (you can adapt to your LLM client)
  - Adding new memory

This is a minimal example — adapt to your chatbot codebase.
"""
import os
import requests
from dotenv import load_dotenv
load_dotenv()

# --- Configuration ---
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mixtral:8x7b')
OPENMEMORY_URL = os.getenv('OPENMEMORY_URL', 'http://localhost:8765')
LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', 0.1))
LLM_MAX_TOKENS = int(os.getenv('LLM_MAX_TOKENS', 512))

print(f"""--- Configuration ---
OLLAMA_URL: {OLLAMA_URL}
OLLAMA_MODEL: {OLLAMA_MODEL}
OPENMEMORY_URL: {OPENMEMORY_URL}
LLM_TEMPERATURE: {LLM_TEMPERATURE}
LLM_MAX_TOKENS: {LLM_MAX_TOKENS}
--------------------""")

# --- Health Checks ---
def check_service(name, url):
    """Simple health check for a service."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"✅ {name} is running.")
            return True
        else:
            print(f"❌ {name} is not running (status code: {response.status_code}).")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {name} is not reachable at {url}.")
        return False

print("\n--- Running Health Checks ---")
ollama_ok = check_service("Ollama", OLLAMA_URL)
openmemory_ok = check_service("OpenMemory", OPENMEMORY_URL)

if not (ollama_ok and openmemory_ok):
    print("\nPlease ensure all services are running before proceeding.")
    exit(1)
print("---------------------------\n")


# --- Main Logic ---
try:
    from mem0 import Memory
except ImportError:
    print("❌ mem0 import failed — make sure you installed mem0ai (pip install mem0ai)")
    exit(1)

config = {
    "llm": {
        "provider": "ollama",
        "config": {
            "model": OLLAMA_MODEL,
            "temperature": LLM_TEMPERATURE,
            "max_tokens": LLM_MAX_TOKENS
        }
    },
    "server": {
        "url": OPENMEMORY_URL
    }
}

print("🚀 Initializing Memory client...")
memory = Memory(config=config)
user_id = "test_user_123"
query = "My favorite food is pizza. Remind me later."

try:
    print(f"\n🔍 Searching memories for query: '{query}'")
    res = memory.search(query=query, user_id=user_id, limit=3)
    print("✅ Search successful.")
    print("Search results:", res)

    mem_texts = [r.get('memory', str(r)) for r in (res.get('results') or [])]
    system_prompt = "You are a helpful assistant. Use these memories:\n" + "\n".join([f"- {m}" for m in mem_texts])
    print("\n📝 Constructed System Prompt:")
    print(system_prompt)

    fake_reply = "Thanks — I noted that you like pizza. I'll remember that."
    print(f"\n💬 Simulated LLM Reply: {fake_reply}")

    print(f"\n💾 Adding new memory...")
    memory.add([{"role":"user","content": query}, {"role":"assistant","content": fake_reply}], user_id=user_id)
    print("✅ Memory added successfully.")
    print("\n🎉 Done. Check OpenMemory UI or run the script again to see the new memory.")

except Exception as e:
    print(f"\n❌ An error occurred during memory operations: {e}")
    print("Please check your OpenMemory server and network connection.")
    exit(1)