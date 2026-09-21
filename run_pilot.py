import json
import requests
import sys
import subprocess
import time
from datetime import datetime

OLLAMA_VERSION = "0.32.14"
PILOT_N = 50
# gitignored - a live output file would dirty the tree on every row (section 6).
RUNNER_OUTPUT_FILE = 'pilot_runner_log.jsonl'

MODEL_1B_Q4 = {
    'model_name': 'gemma3:1b-it-q4_k_m',
    'digest': '8648f39daa8fbf5b18c7b4e6a8fb4990c692751d49917417b8842ca5758e7ffc',
    'quantization': 'Q4_K_M'
}
MODEL_12B_Q8 = {
    'model_name': 'gemma3:12b-it-q8_0',
    'digest': '997a7c2c09753e9011ec18a3fcb498e27c0ba330599dfb26a2e05b58cfbdc1bc',
    'quantization': 'Q8_0'
}
MODELS = [MODEL_1B_Q4, MODEL_12B_Q8]
# both models verified here;
# 12b gets used when the full sweep (Step 6+) exercises the whole roster farther below.

# API never reports this - server setting, declared here and verified via server log (environment section).
KV_CACHE_TYPE = 'f16'
# taken once, not per call - every row from this process shares one timestamp and one commit hash.
run_timestamp = datetime.now().isoformat()
harness_commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()

# items is a list, so it preserves file order - needed for section 2's identical-item-set design.
items = []

# Reads items_pilot.jsonl (draw_pilot.py's output) rather than that script's variables - 
# keeps this file decoupled if draw_pilot.py's internals change.
with open('items_pilot.jsonl', 'r', encoding='utf-8') as infile:
    for line in infile:
        # Raw file lines are text, not dicts. json.loads() parses each into one.
        row = json.loads(line)
        # Keeps only question/question_id, which get sent to one model, one method. 
        # Answer fields (normalized_value/aliases/value) are dropped here because the grader rejoins on question_id against 
        # the frozen items_pilot.jsonl.
        item = {
            'question': row['question'],
            'question_id': row['question_id']
        }
        items.append(item)
assert len(items) == PILOT_N

# The following blocks are a verification of ollama version and model names and digests, as ollama has silently auto-updated
# and moved versions on me (see prereg for more), so this block will crash loudly if such a shift has occurred. 

# pulls current ollama version and stores it to be matched later.
version_response = requests.get("http://127.0.0.1:11434/api/version")
version_data = version_response.json()
print(version_data['version'])

# if pulled ollama version does not match frozen ollama version, exits with expected and received values - version has shifted.
if OLLAMA_VERSION != version_data['version']:
    sys.exit('Ollama version mismatch: Expected: ' + OLLAMA_VERSION + ' Received: ' + version_data['version'])

# pulls ollama tags list, which contains the list of models currently on disk and info about each model, to be matched later.
tags_response = requests.get("http://127.0.0.1:11434/api/tags")
tags_data = tags_response.json()

# the model name and digest match verification block. If a match is found, flags true, prints matched digest, and exits loop.
# If no match is found, crashes and states missing model. The whole point is to verify that the models on disk are an exact
#  match to the models frozen in the prereg section 4 roster. If this crashes, the models are not exact, and the correct 
# models need downloaded.
for model in MODELS:
    flag_match_found = False
    for info_field in tags_data['models']:
        if info_field['name'] == model['model_name']:
            if info_field['digest'] != model['digest']:
                sys.exit('Model digest mismatch: Expected: ' + model['digest'] + ' Received: ' + info_field['digest'])
            flag_match_found = True
            # what was actually seen, not the frozen expectation - rows log this, not model['digest'].
            model['observed_digest'] = info_field['digest']
            print('Match found. Digest: ' + info_field['digest'])
            break
    if not flag_match_found:
        sys.exit('No match found. Missing model: ' + model['model_name'])

# check the whole tree is clean via git status at process start - section 6, checked once, not retriggered by later edits.
tree_status = subprocess.check_output(['git', 'status', '--porcelain']).decode()
if tree_status:
    sys.exit('Working tree is not clean:\n' + tree_status)

resumed_triples = set()
resumed_answers = {}
resumed_commit_hashes = set()
resumed_ollama_versions = set()

try:
    with open(RUNNER_OUTPUT_FILE, 'r', encoding='utf-8') as infile:
        for line in infile:
            try:
                old_row = json.loads(line)
            except json.JSONDecodeError:
                continue
            triple = (old_row['question_id'], old_row['model_tag'], old_row['elicitation_method'])
            resumed_triples.add(triple)
            if old_row['elicitation_method'] == 'answer' and old_row.get('done'):
                resumed_answers[(old_row['question_id'], old_row['model_tag'])] = old_row['raw_response'].strip()
            resumed_commit_hashes.add(old_row['harness_commit_hash'])
            resumed_ollama_versions.add(old_row['ollama_version'])
except FileNotFoundError:
    pass

if resumed_commit_hashes and resumed_commit_hashes != {harness_commit_hash}:
    sys.exit('Existing rows were written by a different harness commit: ' + str(resumed_commit_hashes) + ' vs current ' + harness_commit_hash)
if resumed_ollama_versions and resumed_ollama_versions != {version_data['version']}:
    sys.exit('Existing rows were written by a different Ollama version: ' + str(resumed_ollama_versions) + ' vs current ' + version_data['version'])


# shared across every call this pilot makes - one home for these five values instead of retyping them per template.
base_options = {
    'temperature': 0,
    'top_k': 64,
    'top_p': 0.95,
    'seed': 42,
    'num_ctx': 2048
}

# the nine fields section 6 calls "per run" - identical on every row this process writes, built once instead of retyped per row.
per_run_fields = {
    'ollama_version': version_data['version'],
    'kv_cache_type': KV_CACHE_TYPE,
    'temperature': base_options['temperature'],
    'seed': base_options['seed'],
    'num_ctx': base_options['num_ctx'],
    'top_k': base_options['top_k'],
    'top_p': base_options['top_p'],
    'timestamp': run_timestamp,
    'harness_commit_hash': harness_commit_hash
}


def run_call(model, item, method, prompt, num_predict, top_logprobs=None):
    options = dict(base_options)
    options['num_predict'] = num_predict

    request_body = {
        'model': model['model_name'],
        'messages': [{
            'role': 'user',
            'content': prompt
        }],
        'stream': False,
        'options': options,
        'keep_alive': '5m'
    }
    if top_logprobs is not None:
        request_body['logprobs'] = True
        request_body['top_logprobs'] = top_logprobs

    for attempt_count in range(1, 3):
        try:
            response = requests.post("http://127.0.0.1:11434/api/chat", json=request_body, timeout=90)
            data = response.json()
            if 'error' in data:
                sys.exit('Ollama returned an error for the ' + method + ' call: ' + data['error'])
            done = data['done']
            timed_out = False
            if done:
                break
        except requests.exceptions.Timeout:
            timed_out = True
            done = False

    row = dict(per_run_fields)
    row['question_id'] = item['question_id']
    row['model_tag'] = model['model_name']
    row['model_digest'] = model['observed_digest']
    row['quantization'] = model['quantization']
    row['elicitation_method'] = method
    row['num_predict'] = num_predict
    row['top_logprobs'] = top_logprobs
    row['attempt_count'] = attempt_count
    row['timed_out'] = timed_out

    if not timed_out:
        row['done'] = done
        if 'done_reason' in data:
            row['done_reason'] = data['done_reason']
        if 'load_duration' in data:
            row['load_duration'] = data['load_duration']
        if 'eval_count' in data:
            row['eval_count'] = data['eval_count']
        if 'eval_duration' in data:
            row['eval_duration'] = data['eval_duration']
        if 'prompt_eval_count' in data:
            row['prompt_eval_count'] = data['prompt_eval_count']
        if 'prompt_eval_duration' in data:
            row['prompt_eval_duration'] = data['prompt_eval_duration']
        if 'message' in data:
            row['raw_response'] = data['message']['content']
        if 'logprobs' in data:
            row['raw_logprobs'] = data['logprobs']

    with open(RUNNER_OUTPUT_FILE, 'a', encoding='utf-8') as outfile:
        outfile.write(json.dumps(row) + '\n')

    return row

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



for model in MODELS:
    warm_up(model)

    for item in items:
        question_id = item['question_id']
        model_tag = model['model_name']
        answer_pair = (question_id, model_tag)

        a_triple = (question_id, model_tag, 'answer')
        if a_triple in resumed_triples:
            a_answer = resumed_answers.get(answer_pair)
        else:
            prompt_a = f"{item['question']} Answer with only the answer, no explanation, in 10 words or fewer. If unsure, give your single best guess."
            row_a = run_call(model, item, 'answer', prompt_a, 25)
            if not row_a['timed_out'] and row_a.get('done'):
                a_answer = row_a['raw_response'].strip()
            else:
                a_answer = None

        if a_answer is not None:
            b_triple = (question_id, model_tag, 'p_true')
            if b_triple not in resumed_triples:
                prompt_b = f"""Question: {item['question']}

Answer: {a_answer}

Is the Answer correct? Respond with only True or False."""
                run_call(model, item, 'p_true', prompt_b, 5, top_logprobs=10)

            c_triple = (question_id, model_tag, 'verbalized')
            if c_triple not in resumed_triples:
                prompt_c = f"""Question: {item['question']}

Answer: {a_answer}

How confident are you that the answer is correct? Respond with any integer between 0 and 100 where 0 is not confident and 100 is certain that the answer is correct. Respond with only that integer and nothing else."""
                run_call(model, item, 'verbalized', prompt_c, 10)

    unload(model)

