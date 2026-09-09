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
    if flag_match_found == False:
        sys.exit('No match found. Missing model: ' + model['model_name'])