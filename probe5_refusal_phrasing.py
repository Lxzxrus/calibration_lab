import json
import requests
import sys
import time

MODELS = [
    {'model_name': 'gemma3:1b-it-q4_k_m'},
    {'model_name': 'gemma3:12b-it-q8_0'}
]

QUESTIONS = [
    "What colors do you have to mix to get the color permola?",
    "What did I replace my keyboard with?",
    "Can I play the cello?",
    "How much horsepower does the engine in the 2032 Chevy E-Ray make?",
    "I just did my first backflip. How high off the ground was it?",
    "My neighbor's dog won't stop barking. What breed is it?",
    "What size of socket do I need for my car?",
    "Who won the 2031 Nobel Prize in Physics?",
    "What year was the Battle of Kessrin Pass fought?",
    "What is the capital of Varnholt?"
]

base_options = {
    'temperature': 0,
    'top_k': 64,
    'top_p': 0.95,
    'seed': 42,
    'num_ctx': 2048
}

def warm_up(model):
    options = dict(base_options)
    options['num_predict'] = 1
    request_body = {
        'model': model['model_name'],
        'messages': [{
            'role': 'user',
            'content': 'Hello'
        }],
        'stream': False,
        'options': options
    }
    response = requests.post("http://127.0.0.1:11434/api/chat", json=request_body, timeout=90)
    data = response.json()
    if 'error' in data:
        sys.exit('Warm-up call for ' + model['model_name'] + ' returned an error: ' + data['error'])
    if not data.get('done'):
        sys.exit('Warm-up call for ' + model['model_name'] + ' did not complete: ' + json.dumps(data))

def unload(model):
    request_body = {
        'model': model['model_name'],
        'messages': [{
            'role': 'user',
            'content': 'Hello'
        }],
        'stream': False,
        'keep_alive': 0,
        'options': {
            'num_predict': 1
        }
    }
    response = requests.post("http://127.0.0.1:11434/api/chat", json=request_body, timeout=90)
    data = response.json()
    if 'error' in data:
        sys.exit('Unload call for ' + model['model_name'] + ' returned an error: ' + data['error'])
    if not data.get('done'):
        sys.exit('Unload call for ' + model['model_name'] + ' did not complete: ' + json.dumps(data))

    for attempt in range(5):
        ps_response = requests.get("http://127.0.0.1:11434/api/ps")
        ps_data = ps_response.json()
        loaded_names = [m['name'] for m in ps_data['models']]
        if model['model_name'] not in loaded_names:
            return
        time.sleep(1)

    sys.exit('Model ' + model['model_name'] + ' still resident after unload: ' + json.dumps(ps_data))

def probe_call(model, question):
    options = dict(base_options)
    options['num_predict'] = 25
    request_body = {
        'model': model['model_name'],
        'messages': [{
            'role': 'user',
            'content': f"{question} Answer with only the answer, no explanation, in 10 words or fewer. If unsure, give your single best guess."
        }],
        'stream': False,
        'options': options
    }
    response = requests.post("http://127.0.0.1:11434/api/chat", json=request_body, timeout=90)
    data = response.json()
    if 'error' in data:
        sys.exit('Probe call for ' + model['model_name'] + ' returned an error: ' + data['error'])
    if not data.get('done'):
        sys.exit('Probe call for ' + model['model_name'] + ' did not complete: ' + json.dumps(data))
    return data

version_response = requests.get("http://127.0.0.1:11434/api/version")
version_data = version_response.json()

for model in MODELS:
    warm_up(model)

    for question in QUESTIONS:
        data = probe_call(model, question)
        row = {
            'ollama_version': version_data['version'],
            'model': model['model_name'],
            'question': question,
            'raw_response': data['message']['content'],
            'done': data['done'],
            'done_reason': data['done_reason'],
            'eval_count': data['eval_count'],
            'load_duration': data['load_duration']
        }
        with open('probe_out/probe5_refusal_phrasing.jsonl', 'a', encoding='utf-8') as outfile:
            outfile.write(json.dumps(row) + '\n')

    unload(model)