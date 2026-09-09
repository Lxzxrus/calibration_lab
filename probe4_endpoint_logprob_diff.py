import json
import requests

# ollama /api/generate vs /api/chat endpoint test. 
# Probe: does /api/chat return different logprobs than /api/generate on a warm model?
# First run was cold-contaminated (see lab log) and produced a false divergence.
# This version forces both calls warm before comparing.


# /generate test
test_prompt = {
    'model': 'gemma3:1b-it-q4_k_m',
    'prompt': 'What is the difference between a pen and a pencil? Answer with 15 words or less.',
    'stream': False,
    'logprobs': True,
    'options': {
        'temperature': 0,
        'top_k': 64,
        'top_p': 0.95,
        'seed': 42,
        'num_ctx': 2048,
        'num_predict': 25
    }
}


# warm up call
requests.post("http://127.0.0.1:11434/api/generate", json=test_prompt)

test_response = requests.post("http://127.0.0.1:11434/api/generate", json=test_prompt)
data = test_response.json()
print(data)
with open('probe_out/api_generate_logprob_warm.json', 'w', encoding='UTF-8') as outfile:
    json.dump(data, outfile, indent=2)

# /chat test
test_prompt = {
    'model': 'gemma3:1b-it-q4_k_m',
    'messages': [{
        'role': 'user',
        'content': 'What is the difference between a pen and a pencil? Answer with 15 words or less.'
    }],
    'stream': False,
    'logprobs': True,
    'options': {
        'temperature': 0,
        'top_k': 64,
        'top_p': 0.95,
        'seed': 42,
        'num_ctx': 2048,
        'num_predict': 25
    }
}

# warm up call
requests.post("http://127.0.0.1:11434/api/chat", json=test_prompt)

test_response = requests.post("http://127.0.0.1:11434/api/chat", json=test_prompt)
data = test_response.json()
print(data)
with open('probe_out/api_chat_logprob_warm.json', 'w', encoding='UTF-8') as outfile:
    json.dump(data, outfile, indent=2)