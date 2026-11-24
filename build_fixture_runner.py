import json
import math

# Builds fixtures/runner_log.jsonl: hand designed runner rows for the grader to grade.
# Key names and key order copy run_pilot.py's run_call row build. Nothing here grades
# anything - expected values live in fixtures/expected.jsonl, worked out by hand.

# The nine "per run" fields, as run_pilot.py's per_run_fields writes them.
# Fixture values: the hash is git's null hash, so no row can pass for a real run.

PER_RUN = {
    'ollama_version': '0.32.14',
    'kv_cache_type': 'f16',
    'temperature': 0,
    'seed': 42,
    'num_ctx': 2048,
    'top_k': 64,
    'top_p': 0.95,
    'timestamp': '2026-11-20T00:00:00',
    'harness_commit_hash': '0' * 40
}

MODEL_1B = {
    'model_tag': 'gemma3:1b-it-q4_k_m',
    'model_digest': '8648f39daa8fbf5b18c7b4e6a8fb4990c692751d49917417b8842ca5758e7ffc',
    'quantization': 'Q4_K_M',
}

MODEL_12B = {
    'model_tag': 'gemma3:12b-it-q8_0',
    'model_digest': '997a7c2c09753e9011ec18a3fcb498e27c0ba330599dfb26a2e05b58cfbdc1bc',
    'quantization': 'Q8_0',
}

# num_predict per template, section 6 parameters.
NUM_PREDICT = {'answer': 25, 'p_true': 5, 'verbalized': 10}

def candidate(token, p, has_bytes=True):
    # One top_logprobs entry, in the key order probe_out/api_chat_logprob_warm.json shows.
    # logprob is computed from p, never typed, so every probability below is exact.
    entry = {'token': token, 'logprob': math.log(p)}
    if has_bytes:
        entry['bytes'] = list(token.encode('utf-8'))
    return entry

def position(candidates):
    # candidates: ten (token, p) or (token, p, has_bytes) tuples, highest p first.
    probabilities = [c[1] for c in candidates]
    assert len(candidates) == 10
    assert probabilities == sorted(probabilities, reverse=True)
    # fx_023 and fx_024 were first drafted summing above 1 (lab log 10-19)
    assert sum(probabilities) <= 1.0
    top = [candidate(*c) for c in candidates]
    # At temperature 0 the generated token is the most likely candidate.
    chosen = dict(top[0])
    chosen['top_logprobs'] = top
    return chosen

# Position-0 and position-1 lists shared by every ordinary Template B row.
# Expected for this position 0: P(True) = 0.90 / (0.90 + 0.05), retained mass 0.95.
STANDARD_POS0 = [('True', 0.90), ('False', 0.05), ('Yes', 0.01), ('Correct', 0.008), ('**', 0.006), (' ', 0.005), ('The', 0.004), ('Answer', 0.003),
                 ('I', 0.002), ('It', 0.001)]
NEWLINE_POS = [('\n', 0.95), (' ', 0.02), ('.', 0.01), ('\n\n', 0.005), ('**', 0.004),
               (',', 0.003), ('!', 0.002), ('<', 0.001), ('-', 0.0005), (':', 0.0004)]
STANDARD_B = {'raw': 'True\n', 'positions': [STANDARD_POS0, NEWLINE_POS]}

def make_row(model, question_id, method, call):
    # Same key order as run_pilot.py's run_call.
    row = dict(PER_RUN)
    row['question_id'] = question_id
    row['model_tag'] = model['model_tag']
    row['model_digest'] = model['model_digest']
    row['quantization'] = model['quantization']
    row['elicitation_method'] = method
    row['num_predict'] = NUM_PREDICT[method]
    row['top_logprobs'] = 10 if method == 'p_true' else None
    state = call.get('state', 'ok')
    row['attempt_count'] = 1 if state == 'ok' else 2
    row['timed_out'] = state == 'timeout'
    if state == 'timeout':
        # On a timeout nothing came back, so run_call writes nothing past timed_out.
        return row
    row['done'] = state =='ok'
    if state == 'ok':
        row['done_reason'] = call.get('done_reason', 'stop')
        row['load_duration'] = 215500000
        row['eval_count'] = call['eval_count']
        row['eval_duration'] = 25000000
        row['prompt_eval_count'] = {'answer': 44, 'p_true': 39, 'verbalized': 77}[method]
        row['prompt_eval_duration'] = 15000000
    # A done: false row keeps its raw text and logprobs, so a grader that reads them
    # before checking done is caught. Not observed: the prereg's section 6 Findings
    # say only "no metadata fields".
    row['raw_response'] = call['raw']
    if method == 'p_true':
        row['raw_logprobs'] = [position(p) for p in call['positions']]
    return row

def a_call(raw, eval_count=6, **extra):
    return dict(raw=raw, eval_count=eval_count, **extra)

def b_call(raw='True\n', positions=None, **extra):
    if positions is None:
        positions = STANDARD_B['positions']
    return dict(raw=raw, positions=positions, eval_count=len(positions), **extra)

def c_call(raw='90', eval_count=3, **extra):
    return dict(raw=raw, eval_count=eval_count, **extra)

FILLERS = [('Yes', 0.03), ('Correct', 0.02), ('**', 0.01), (' ', 0.008),
           ('The', 0.006), ('I', 0.004), ('It', 0.002), ('Answer', 0.001)]

# One entry per fixture case: the A, B, and C calls the runner would have made.
# B and C left out mean the standard call. 'skip' means the runner writes no row.
CASES = {
    'fx_001': {'A': a_call('Paris, France.')},
    'fx_002': {'A': a_call('He was exiled.')},
    'fx_003': {'A': a_call('**Xiaowei Yi**')},
    'fx_004': {'A': a_call('O’Neil')},
    'fx_005': {'A': a_call("I don't know")},
    'fx_006': {'A': a_call(' \n', eval_count=2)},
    'fx_007': {'A': a_call('not Paris')},
    'fx_008': {'A': a_call('never really truly said Vancouver')},
    'fx_009': {'A': a_call('never really truly once said Vancouver')},
    'fx_010': {'A': a_call('not Toronto')},
    'fx_011': {'A': a_call('Possibly a terrier or chihuahua.')},
    'fx_012': {'A': a_call('13mm - 15mm, likely 13mm.')},
    'fx_013': {'A': a_call('George Orwell')},
    'fx_014': {'A': a_call('I think the answer you are looking for is probably Paris')},
    'fx_015': {'A': a_call('Paris is the capital of France and is famous for the Eiffel '
                           'Tower, the Louvre, and its many cafes along the',
                           eval_count=25, done_reason='length')},
    'fx_016': {'A': a_call("I don't know")},
    'fx_017': {'A': a_call('I cannot know, but probably 1915')},
    'fx_018': {'A': a_call('I cannot know, but probably 1914')},
    'fx_019': {'A': a_call("I'm not sure, maybe Paris")},
    'fx_020': {'A': {'state': 'timeout'}, 'B': 'skip', 'C': 'skip'},
    'fx_021': {'A': {'state': 'not_done', 'raw': 'Paris Paris Paris Paris'},
               'B': 'skip', 'C': 'skip'},
    'fx_022': {'A': a_call('Paris'), 'C': {'state': 'timeout'}},
    'fx_023': {'A': a_call('Paris'), 'B': b_call(positions=[
        [('True', 0.80), ('False', 0.10), ('TRUE', 0.05), ('Yes', 0.02), ('Correct', 0.005),
         ('**', 0.004), (' ', 0.003), ('The', 0.002), ('I', 0.001), ('It', 0.0005)],
        NEWLINE_POS])},
    'fx_024': {'A': a_call('Paris'), 'B': b_call(raw='Truth\n', positions=[
        [('Truth', 0.60), ('False', 0.30)] + FILLERS, NEWLINE_POS])},
    'fx_025': {'A': a_call('Paris'), 'B': b_call(raw=' True\n', positions=[
        [(' True', 0.60), ('false', 0.30)] + FILLERS, NEWLINE_POS])},
    'fx_026': {'A': a_call('Paris'), 'B': b_call(positions=[
        [('True', 0.70), ('False', 0.20), ('', 0.05, False), ('Yes', 0.01), ('Correct', 0.008),
         ('**', 0.006), (' ', 0.004), ('The', 0.002), ('I', 0.001), ('It', 0.0005)],
        NEWLINE_POS])},
    'fx_027': {'A': a_call('Paris'), 'B': b_call(raw='Yes\n', positions=[
        [('Yes', 0.70), ('yes', 0.10), ('Correct', 0.05), ('No', 0.04), ('**', 0.03),
         (' ', 0.02), ('The', 0.01), ('I', 0.005), ('It', 0.003), ('Answer', 0.002)],
        NEWLINE_POS])},
    'fx_028': {'A': a_call('Paris'), 'B': b_call(raw='**True**', positions=[
        [('**', 0.85), ('*', 0.05), ('Yes', 0.03), ('Correct', 0.02), (' ', 0.01),
         ('The', 0.008), ('I', 0.006), ('It', 0.004), ('Answer', 0.002), ('\n', 0.001)],
        STANDARD_POS0,
        [('**', 0.95), ('*', 0.02), ('.', 0.01), ('\n', 0.005), (' ', 0.004),
         (',', 0.003), ('!', 0.002), ('<', 0.001), ('-', 0.0005), (':', 0.0004)]])},
    'fx_029': {'A': a_call('Paris'), 'C': c_call('85')},
    'fx_030': {'A': a_call('Paris'), 'C': c_call('85%')},
    'fx_031': {'A': a_call('Paris'), 'C': c_call('085', eval_count=4)},
    'fx_032': {'A': a_call('Paris'), 'C': c_call('0', eval_count=2)},
    'fx_033': {'A': a_call('Paris'), 'C': c_call(' 100\n', eval_count=6)},
    'fx_034': {'A': a_call('Paris'), 'C': c_call('80-90', eval_count=6)},
    'fx_035': {'A': a_call('Paris'), 'C': c_call('eighty-five', eval_count=5)},
    'fx_036': {'A': a_call('Paris'), 'C': c_call('150', eval_count=4)},
    'fx_037': {'A': a_call('Paris'), 'C': c_call('85 percent', eval_count=4)},
    # DECISION D3: digits then padding, the one truncated response that still parses.
    'fx_038': {'A': a_call('Paris'), 'C': c_call('100\n\n\n\n\n\n\n', eval_count=10,
                                                done_reason='length')},
    'fx_039': {'A': a_call('Paris'), 'C': c_call('', eval_count=1)},
    'fx_040': {'A': a_call('Fiddler on the Roof')},
    'fx_041': {'A': a_call('Paris'), 'C': c_call('85%%', eval_count=4)},
    'fx_042': {'A': a_call('Paris'), 'B': b_call(state='not_done')},
    'fx_043': {'A': a_call('I think the answer you are looking for is Paris')},
    'fx_044': {'A': a_call('Truth or Dare')},
    'fx_045': {'A': a_call('The Hague')},
    # DECISION D4: a response that normalizes to empty, the only kind an unguarded
    # empty alias can match under every whitespace-delimited implementation.
    'fx_046': {'A': a_call('?', eval_count=2)},
    'fx_047': {'A': a_call('1939-1945')},
    'fx_048': {'A': a_call('“Casablanca”')},
    'fx_049': {'A': a_call("couldn't ever be Vancouver")},
    'fx_050': {'A': a_call("couldn't ever really be Vancouver")},
    'fx_051': {'A': a_call('I know Vancouver')},
    'fx_052': {'A': a_call('“Casablanca”')},
}

# DECISION D5: two items also run on the 12b, so the grader's join and both cascades
# must key on the model as well as the item.
CASES_12B = {
    'fx_016': {'A': a_call('1915')},
    'fx_020': {'A': a_call('Paris')},
}

rows = []
# Models outer, items inner, A then B then C: run_pilot.py's loop order.
for model, cases in [(MODEL_1B, CASES), (MODEL_12B, CASES_12B)]:
    for question_id, calls in cases.items():
        for method, letter, default in [('answer', 'A', None),
                                        ('p_true', 'B', b_call()),
                                        ('verbalized', 'C', c_call())]:
            call = calls.get(letter, default)
            if call == 'skip':
                continue
            rows.append(make_row(model, question_id, method, call))

# Checks against fixtures/items.jsonl: every case has an items row and every items
# row has an A row on the 1b. No triple appears twice.
with open('fixtures/items.jsonl', 'r', encoding='utf-8') as infile:
    item_ids = [json.loads(line)['question_id'] for line in infile]
assert sorted(CASES) == sorted(item_ids)
assert set(CASES_12B) <= set(item_ids)
triples = [(r['question_id'], r['model_tag'], r['elicitation_method']) for r in rows]
assert len(triples) == len(set(triples))

with open('fixtures/runner_log.jsonl', 'w', encoding='utf-8', newline='\n') as outfile:
    for row in rows:
        outfile.write(json.dumps(row) + '\n')

print('Wrote', len(rows), 'rows to fixtures/runner_log.jsonl')