import json
import requests
import sys

OLLAMA_VERSION = "0.32.14"
PILOT_N = 50
MODEL_1B_Q4 = {
    'model_name': 'gemma3:1b-it-q4_k_m',
    'digest': '8648f39daa8fbf5b18c7b4e6a8fb4990c692751d49917417b8842ca5758e7ffc'
}
MODEL_12B_Q8 = {
    'model_name': 'gemma3:12b-it-q8_0',
    'digest': '997a7c2c09753e9011ec18a3fcb498e27c0ba330599dfb26a2e05b58cfbdc1bc'
}
MODELS = [MODEL_1B_Q4, MODEL_12B_Q8]
# both models verified here even though only MODEL_1B_Q4 is called below;
# 12b gets used once the full sweep (Step 6+) exercises the whole roster.

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
request_body_a = {
    'model': MODEL_1B_Q4['model_name'],
    'messages': [{
        'role': 'user',
        'content': prompt_a
    }],
    'stream': False,
    'options': {
        'temperature': 0,
        'top_k': 64,
        'top_p': 0.95,
        'seed': 42,
        'num_ctx': 2048,
        'num_predict': 25
    }
}

# confirms against the real templated call. This block is the end-to-end smoke test that Step 6 will scale up to all 50 items. 
response_a = requests.post("http://127.0.0.1:11434/api/chat", json=request_body_a)
data_a = response_a.json()
answer_a_raw = data_a['message']['content']
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
request_body_c = {
    'model': MODEL_1B_Q4['model_name'],
    'messages': [{
        'role': 'user',
        'content': prompt_c
    }],
    'stream': False,
    'options': {
        'temperature': 0,
        'top_k': 64,
        'top_p': 0.95,
        'seed': 42,
        'num_ctx': 2048,
        'num_predict': 10
    }
}

response_c = requests.post("http://127.0.0.1:11434/api/chat", json=request_body_c)
data_c = response_c.json()
answer_c = data_c['message']['content']
print(answer_c)



# Step 6 needs warm up call - not complete without it.