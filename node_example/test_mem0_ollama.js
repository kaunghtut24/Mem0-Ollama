/**
 * Node example for Mem0 + Ollama integration.
 * - Copy .env.example to .env and edit values.
 * - npm install
 * - node test_mem0_ollama.js
 */
require('dotenv').config();
const fetch = require('node-fetch');

// --- Configuration ---
const OPENMEMORY_URL = process.env.OPENMEMORY_URL || 'http://localhost:8765';
const OLLAMA_URL = process.env.OLLAMA_URL || 'http://localhost:11434';
const OLLAMA_MODEL = process.env.OLLAMA_MODEL || 'mixtral:8x7b';
const LLM_TEMPERATURE = parseFloat(process.env.LLM_TEMPERATURE || 0.1);
const LLM_MAX_TOKENS = parseInt(process.env.LLM_MAX_TOKENS || 512, 10);

console.log(`--- Configuration ---
OPENMEMORY_URL: ${OPENMEMORY_URL}
OLLAMA_URL: ${OLLAMA_URL}
OLLAMA_MODEL: ${OLLAMA_MODEL}
LLM_TEMPERATURE: ${LLM_TEMPERATURE}
LLM_MAX_TOKENS: ${LLM_MAX_TOKENS}
--------------------`);

// --- Health Checks ---
async function checkService(name, url) {
    try {
        const response = await fetch(url);
        if (response.ok) {
            console.log(`✅ ${name} is running.`);
            return true;
        } else {
            console.log(`❌ ${name} is not running (status code: ${response.status}).`);
            return false;
        }
    } catch (error) {
        console.log(`❌ ${name} is not reachable at ${url}.`);
        return false;
    }
}

async function runHealthChecks() {
    console.log("\n--- Running Health Checks ---");
    const ollamaOk = await checkService("Ollama", OLLAMA_URL);
    const openmemoryOk = await checkService("OpenMemory", OPENMEMORY_URL);

    if (!ollamaOk || !openmemoryOk) {
        console.log("\nPlease ensure all services are running before proceeding.");
        process.exit(1);
    }
    console.log("---------------------------\n");
}

// --- Main Logic ---
let Memory;
try {
  Memory = require('mem0ai').Memory;
} catch (e) {
  console.error('❌ Please install mem0ai: npm install mem0ai');
  process.exit(1);
}

async function main(){
  await runHealthChecks();

  const config = {
    llm: {
      provider: 'ollama',
      config: { 
          model: OLLAMA_MODEL, 
          temperature: LLM_TEMPERATURE, 
          max_tokens: LLM_MAX_TOKENS 
        }
    },
    server: { url: OPENMEMORY_URL }
  };

  console.log('🚀 Initializing Memory client...');
  const memory = new Memory(config);
  const userId = 'test_user_node_1';
  const query = 'I like spicy food - remember that for me.';

  try {
    console.log(`\n🔍 Searching memories for query: '${query}'`);
    const res = await memory.search(query, { user_id: userId, limit: 3 });
    console.log("✅ Search successful.");
    console.log('Search results:', res);

    const fakeReply = 'Got it — noted that you like spicy food.';
    console.log(`\n💬 Simulated LLM Reply: ${fakeReply}`);

    console.log('\n💾 Adding new memory...');
    await memory.add([{ role: 'user', content: query }, { role: 'assistant', content: fakeReply }], { user_id: userId });
    console.log('✅ Memory added successfully.');
    console.log("\n🎉 Done. Check OpenMemory UI or run the script again to see the new memory.");

  } catch (error) {
      console.error(`\n❌ An error occurred during memory operations: ${error.message}`);
      console.error("Please check your OpenMemory server and network connection.");
      process.exit(1);
  }
}

main().catch(e => {
    console.error("\nAn unexpected error occurred:", e);
    process.exit(1);
});