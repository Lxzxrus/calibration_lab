import json
import requests
import sys
import subprocess
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
# both models verified here even though only MODEL_1B_Q4 is called below;
# 12b gets used once the full sweep (Step 6+) exercises the whole roster.

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
        # testing print. remove before finalize.
        print(item['question'], item['question_id'])
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



# pulls the question with a specified question_id instead of just hand typing the question and risking the text silently drifting.
# I chose question sfq_1586 because it is easy to quickly verify that the answer the model produces is intended for that question
# due to the question's simple structure - the model should give a simple answer. I deliberately avoided question qw_402 due to
# its CSV quote mess - it would be a garbled input to the model, which risks garbled output - overall messy.

# scaffolding, delete after step 6 is built
chosen_question_id = 'sfq_1586'

found_match = False
for item in items:
    if item['question_id'] == chosen_question_id:
        question = item['question']
        found_match = True
        break

if not found_match:
    sys.exit('Could not find match for question: ' + chosen_question_id)

# combined the frozen Template A text with the stored question to be fed to the model through the ollama chat api call.
# a prompt that drifts from the frozen wording is an undocumented deviation from the prereg.
prompt_a = f"{question} Answer with only the answer, no explanation, in 10 words or fewer. If unsure, give your single best guess."

# logprobs deliberately absent because they aren't needed here: Template A generates an answer; its confidence contribution is zero,
# so logprobs are useless for it. That is Template B's exclusive job, later.

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


options_a = dict(base_options)
options_a['num_predict'] = 25

request_body_a = {
    'model': MODEL_1B_Q4['model_name'],
    'messages': [{
        'role': 'user',
        'content': prompt_a
    }],
    'stream': False,
    'options': options_a
}

# confirms against the real templated call. This block is the end-to-end smoke test that Step 6 will scale up to all 50 items. 
# one retry on failure, not retry-until-success - section 9's timeout and no_valid_response rules.
for attempt_count_a in range(1, 3):
    try:
        response_a = requests.post("http://127.0.0.1:11434/api/chat", json=request_body_a, timeout=90)
        data_a = response_a.json()
        # model/server fault, not a data condition - crash loudly rather than retry or exclude.
        if 'error' in data_a:
            sys.exit('Ollama returned an error for the A call: ' + data_a['error'])
        done_a = data_a['done']
        timed_out_a = False
        if done_a:
            answer_a_raw = data_a['message']['content']
            break
    except requests.exceptions.Timeout:
        timed_out_a = True
        done_a = False


# row_a: the runner-file schema from section 6, for the A call.
row_a = dict(per_run_fields)
row_a['question_id'] = chosen_question_id
row_a['model_tag'] = MODEL_1B_Q4['model_name']
row_a['model_digest'] = MODEL_1B_Q4['observed_digest']
row_a['quantization'] = MODEL_1B_Q4['quantization']
row_a['elicitation_method'] = 'answer'
row_a['num_predict'] = options_a['num_predict']
row_a['top_logprobs'] = None # unset on Templates A and C - only P(True) calls populate this (section 5 Parameters).
row_a['attempt_count'] = attempt_count_a
row_a['timed_out'] = timed_out_a

# log whichever response fields are actually present - line 298 only guarantees absence on a timeout, not on done: false.
if not timed_out_a:
    row_a['done'] = done_a
    if 'done_reason' in data_a:
        row_a['done_reason'] = data_a['done_reason']
    if 'load_duration' in data_a:
        row_a['load_duration'] = data_a['load_duration']
    if 'eval_count' in data_a:
        row_a['eval_count'] = data_a['eval_count']
    if 'eval_duration' in data_a:
        row_a['eval_duration'] = data_a['eval_duration']
    if 'prompt_eval_count' in data_a:
        row_a['prompt_eval_count'] = data_a['prompt_eval_count']
    if 'prompt_eval_duration' in data_a:
        row_a['prompt_eval_duration'] = data_a['prompt_eval_duration']
    if 'message' in data_a:
        row_a['raw_response'] = data_a['message']['content']


# append and close immediately - each row is durable on disk before the next call starts.
with open(RUNNER_OUTPUT_FILE, 'a', encoding='utf-8') as outfile:
    outfile.write(json.dumps(row_a) + '\n')


if not timed_out_a and done_a:
    print(answer_a_raw)

    # strip leading and trailing whitespaces. Whitespace behavior correlates with model size, so if one model returns more
    # whitespaces than another model, the two cells get slightly differently-formed prompts, which is a size effect riding inside
    #  an instrument, on a size hypothesis.
    answer_a = answer_a_raw.strip()

    # using triple quotes I can construct prompt_c in accordance to the exact frozen structure of Template C from the prereg.
    prompt_c = f"""Question: {question}

Answer: {answer_a}

How confident are you that the answer is correct? Respond with any integer between 0 and 100 where 0 is not confident and 100 is certain that the answer is correct. Respond with only that integer and nothing else."""

    print(repr(prompt_c))

    # same call pattern as Template A above. Logprobs still purposefully excluded despite the confidence being in question because
    # the confidence measure is read as text, not the literal probabilities. Note num_predict here is 10 instead of 25 according to
    # frozen values in the prereg.

    options_c = dict(base_options)
    options_c['num_predict'] = 10

    request_body_c = {
        'model': MODEL_1B_Q4['model_name'],
        'messages': [{
            'role': 'user',
            'content': prompt_c
        }],
        'stream': False,
        'options': options_c
    }

    for attempt_count_c in range(1, 3):
        try:
            response_c = requests.post("http://127.0.0.1:11434/api/chat", json=request_body_c, timeout=90)
            data_c = response_c.json()
            if 'error' in data_c:
                sys.exit('Ollama returned an error for the C call: ' + data_c['error'])
            done_c = data_c['done']
            timed_out_c = False
            if done_c:
                answer_c = data_c['message']['content']
                break
        except requests.exceptions.Timeout:
            timed_out_c = True
            done_c = False


    # row_c: same schema as row_a - 'verbalized' is Template C's elicitation method (section 6 Identity).
    row_c = dict(per_run_fields)
    row_c['question_id'] = chosen_question_id
    row_c['model_tag'] = MODEL_1B_Q4['model_name']
    row_c['model_digest'] = MODEL_1B_Q4['observed_digest']
    row_c['quantization'] = MODEL_1B_Q4['quantization']
    row_c['elicitation_method'] = 'verbalized'
    row_c['num_predict'] = options_c['num_predict']
    row_c['top_logprobs'] = None
    row_c['attempt_count'] = attempt_count_c
    row_c['timed_out'] = timed_out_c

    # same reasoning as row_a's conditional above.
    if not timed_out_c:
        row_c['done'] = done_c
        if 'done_reason' in data_c:
            row_c['done_reason'] = data_c['done_reason']
        if 'load_duration' in data_c:
            row_c['load_duration'] = data_c['load_duration']
        if 'eval_count' in data_c:
            row_c['eval_count'] = data_c['eval_count']
        if 'eval_duration' in data_c:
            row_c['eval_duration'] = data_c['eval_duration']
        if 'prompt_eval_count' in data_c:
            row_c['prompt_eval_count'] = data_c['prompt_eval_count']
        if 'prompt_eval_duration' in data_c:
            row_c['prompt_eval_duration'] = data_c['prompt_eval_duration']
        if 'message' in data_c:
            row_c['raw_response'] = data_c['message']['content']


    # same durability reasoning as row_a's write above.
    with open(RUNNER_OUTPUT_FILE, 'a', encoding='utf-8') as outfile:
        outfile.write(json.dumps(row_c) + '\n')


    if not timed_out_c and done_c:
        print(answer_c)

else: 
    print('Request A did not produce a usable answer.')




# Step 6 needs warm up call - not complete without it.