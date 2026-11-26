import json
import math

# Builds fixtures/expected.jsonl: the row the grader must write for every runner row in
# fixtures/runner_log.jsonl, plus the four rows it synthesizes. Worked out by hand from the
# prereg under decisions E1-E6 (lab log 11-20 to 11-23). No grading code runs here: every
# flag, count and code below is typed, and the only arithmetic is the hand arithmetic,
# written out where it is used.

MODEL_1B = 'gemma3:1b-it-q4_k_m'
MODEL_12B = 'gemma3:12b-it-q8_0'

def logprob(token, p):
    # The input logprob build_fixture_runner.py wrote for this candidate.
    return {'token': token, 'logprob': math.log(p)}

# Answer-level fields, read from the A response (Grader Spec): matched, matched aliases,
# negation, raw word count, compliance, multi-candidate. Then the A call's own truncation
# and exclusion. None everywhere means A has no valid response (E3).

#            matched  aliases              neg    words  compl  multi  trunc  exclusion
ANSWERS = {
    'fx_001': (True,  ['paris', 'paris france'], False, 2, True,  False, False, None),
    'fx_002': (False, [],                  False, 3,  True,  False, False, None),
    'fx_003': (True,  ['xiaowei yi'],      False, 2,  True,  False, False, None),
    'fx_004': (True,  ['o neil'],          False, 1,  True,  False, False, None),
    'fx_005': (True,  ['i'],               False, 3,  True,  False, False, None),
    'fx_006': (False, [],                  False, 0,  True,  False, False, None),
    'fx_007': (True,  ['paris'],           True,  2,  True,  False, False, None),
    'fx_008': (True,  ['vancouver'],       True,  5,  True,  False, False, None),
    'fx_009': (True,  ['vancouver'],       False, 6,  True,  False, False, None),
    'fx_010': (False, [],                  False, 2,  True,  False, False, None),
    'fx_011': (True,  ['chihuahua'],       False, 5,  True,  True,  False, None),
    'fx_012': (True,  ['13mm'],            False, 5,  True,  False, False, None),
    'fx_013': (True,  ['orwell'],          False, 2,  True,  False, False, None),
    'fx_014': (True,  ['paris'],           False, 11, False, False, False, None),
    'fx_015': (True,  ['paris'],           False, 21, False, False, True,  None),
    'fx_016': (False, [],                  False, 3,  True,  False, False, 'refusal'),
    'fx_017': (True,  ['1915'],            True,  6,  True,  False, False, None),
    'fx_018': (False, [],                  False, 6,  True,  False, False, 'refusal'),
    'fx_019': (False, [],                  False, 5,  True,  False, False, None),
    'fx_020': (None,  None,                None,  None, None, None, None, 'timeout'),
    'fx_021': (None,  None,                None,  None, None, None, None, 'no_valid_response'),
    'fx_040': (True,  ['fiddler on roof'], False, 4,  True,  False, False, None),
    'fx_043': (True,  ['paris'],           False, 10, True,  False, False, None),
    'fx_044': (True,  ['truth or dare'],   False, 3,  True,  True,  False, None),
    'fx_045': (True,  ['hague'],           False, 2,  True,  False, False, None),
    'fx_046': (False, [],                  False, 1,  True,  False, False, None),
    'fx_047': (False, [],                  False, 1,  True,  False, False, None),
    'fx_048': (True,  ['“casablanca”'], False, 1, True, False, False, None),
    'fx_049': (True,  ['vancouver'],       True,  4,  True,  False, False, None),
    'fx_050': (True,  ['vancouver'],       False, 5,  True,  False, False, None),
    'fx_051': (True,  ['vancouver'],       False, 3,  True,  False, False, None),
    'fx_052': (False, [],                  False, 1,  True,  False, False, None),
    'fx_053': (True,  ['paris'],           True,  2,  True,  False, False, None),
}
# Every other 1b case answered a plain 'Paris': one word, matched, nothing flagged.
PLAIN_PARIS = (True, ['paris'], False, 1, True, False, False, None)

ANSWERS_12B = {
    'fx_016': (True, ['1915'], False, 1, True, False, False, None),
    'fx_020': (True, ['paris'], False, 1, True, False, False, None),
}

# Template B, an ordinary row. Position 0: True 0.90, False 0.05, nothing else true or false.
STANDARD_B = {
    'truncation': False, 'exclusion_reason': None,
    'p_true': 0.90 / (0.90 + 0.05), 'retained_mass': 0.90 + 0.05,
    'matched_token_logprobs': [logprob('True', 0.90), logprob('False', 0.05)],
}
# Template C, an ordinary row: '90'.
STANDARD_C = {
    'truncation': False, 'exclusion_reason': None,
    'parsed_integer': 90, 'mapped_confidence': 0.90,
}
# A call with no valid response (E3): nothing read past done, so nothing derived.
NO_B = {'truncation': None, 'p_true': None, 'retained_mass': None, 'matched_token_logprobs': None}
NO_C = {'truncation': None, 'parsed_integer': None, 'mapped_confidence': None}
UNPARSEABLE_C = {'parsed_integer': None, 'mapped_confidence': None, 'exclusion_reason': 'unparseable'}

# Changes from STANDARD_B, by case.
B_CHANGES = {
    'fx_016': {'exclusion_reason': 'refusal'},
    'fx_018': {'exclusion_reason': 'refusal'},
    'fx_020': dict(NO_B, exclusion_reason='timeout'),
    'fx_021':dict(NO_B, exclusion_reason='no_valid_response'),
    # True 0.80 + TRUE 0.05 against False 0.10. Yes is outside the retained mass.
    'fx_023': {'p_true': (0.80 + 0.05) / (0.80 + 0.05 + 0.10), 'retained_mass': 0.80 + 0.05 + 0.10,
               'matched_token_logprobs': [logprob('True', 0.80), logprob('False', 0.10),
                logprob('TRUE', 0.05)]},
    # Truth is not true: no affirmative mass, False 0.30 alone.
    'fx_024': {'p_true': 0.0 / (0.0 + 0.30), 'retained_mass': 0.30,
               'matched_token_logprobs': [logprob('False', 0.30)]},
    # ' True' strips to true and 'false' lowercases to false: both count.
    'fx_025': {'p_true': 0.60 / (0.60 + 0.30), 'retained_mass': 0.60 + 0.30,
               'matched_token_logprobs': [logprob(' True', 0.60), logprob('false', 0.30)]},
    # The empty token (no bytes) is tolerated and counts for neither.
    'fx_026': {'p_true': 0.70 / (0.70 + 0.20), 'retained_mass': 0.70 + 0.20,
               'matched_token_logprobs': [logprob('True', 0.70), logprob('False', 0.20)]},
    # No true or false candidate at position 0: retained mass 0, unparseable.
    'fx_027': {'p_true': None, 'retained_mass': 0.0, 'matched_token_logprobs': [],
               'exclusion_reason': 'unparseable'},
    # Position 0 is '**'; True sits at position 1, which is never read.
    'fx_028': {'p_true': None, 'retained_mass': 0.0, 'matched_token_logprobs': [],
               'exclusion_reason': 'unparseable'},
    'fx_042': dict(NO_B, exclusion_reason='no_valid_response'),
}

# Changes from STANDARD_C, by case.
C_CHANGES = {
    'fx_016': {'exclusion_reason': 'refusal'},
    'fx_018': {'exclusion_reason': 'refusal'},
    'fx_020': dict(NO_C, exclusion_reason='timeout'),
    'fx_021': dict(NO_C, exclusion_reason='no_valid_response'),
    'fx_022': dict(NO_C, exclusion_reason='timeout'),
    'fx_029': {'parsed_integer': 85, 'mapped_confidence': 0.85},
    'fx_030': {'parsed_integer': 85, 'mapped_confidence': 0.85},
    'fx_031': {'parsed_integer': 85, 'mapped_confidence': 0.85},
    'fx_032': {'parsed_integer': 0, 'mapped_confidence': 0.0},
    'fx_033': {'parsed_integer': 100, 'mapped_confidence': 1.0},
    'fx_034': UNPARSEABLE_C,
    'fx_035': UNPARSEABLE_C,
    # int() reads 150, but it is outside [0, 100], so the rule yields no integer.
    'fx_036': UNPARSEABLE_C,
    'fx_037': UNPARSEABLE_C,
    # Truncated, still parses: flagged, never excluded.
    'fx_038': {'parsed_integer': 100, 'mapped_confidence': 1.0, 'truncation': True},
    'fx_039': UNPARSEABLE_C,
    # One trailing % is stripped; '85%' is left, which int() rejects.
    'fx_041': UNPARSEABLE_C,
    # int() rejects '85.5'; the rule takes integers only.
    'fx_054': UNPARSEABLE_C,
}

def make_rows(model, question_id, answer, b_changes, c_changes):
    matched, aliases, negation, words, compliance, multi, truncation, exclusion = answer
    shared = {
        'question_id': question_id,
        'model_tag': model,
        'matched': matched,
        'matched_aliases': aliases,
        'negation': negation,
        'raw_word_count': words,
        'compliance': compliance,
        'multi_candidate': multi,
    }
    a_row = dict(shared, elicitation_method='answer', truncation=truncation, exclusion_reason=exclusion)
    # E2: B and C carry the A response's fields; truncation and the rest are their own call's.
    b_row = dict(shared, elicitation_method='p_true')
    b_row.update(STANDARD_B)
    b_row.update(b_changes)
    c_row = dict(shared, elicitation_method='verbalized')
    c_row.update(STANDARD_C)
    c_row.update(c_changes)
    return [a_row, b_row, c_row]

rows = []
for number in range (1, 55):
    question_id = 'fx_%03d' % number
    rows += make_rows(MODEL_1B, question_id, ANSWERS.get(question_id, PLAIN_PARIS),
                      B_CHANGES.get(question_id, {}), C_CHANGES.get(question_id, {}))
for question_id, answer in ANSWERS_12B.items():
    rows += make_rows(MODEL_12B, question_id, answer, {}, {})

# E1: one key set per method, the same on every row of that method.
KEYS = ['question_id', 'model_tag', 'elicitation_method', 'matched', 'matched_aliases',
        'negation', 'raw_word_count', 'compliance', 'multi_candidate', 'truncation',
        'exclusion_reason']
EXTRA = {'answer': [], 'p_true': ['p_true', 'retained_mass', 'matched_token_logprobs'],
         'verbalized': ['parsed_integer', 'mapped_confidence']}
for row in rows:
    assert sorted(row) == sorted(KEYS + EXTRA[row['elicitation_method']])

# Every runner row has an expected row, and the only expected rows without a runner row
# are the four the grader synthesizes for the terminal A failures.
with open('fixtures/runner_log.jsonl', 'r', encoding='utf-8') as infile:
    runner = [json.loads(line) for line in infile]
runner_triples = {(r['question_id'], r['model_tag'], r['elicitation_method']) for r in runner}
expected_triples = {(r['question_id'], r['model_tag'], r['elicitation_method']) for r in rows}
assert len(expected_triples) == len(rows) == 168
assert runner_triples <= expected_triples
assert expected_triples - runner_triples == {
    ('fx_020', MODEL_1B, 'p_true'), ('fx_020', MODEL_1B, 'verbalized'),
    ('fx_021', MODEL_1B, 'p_true'), ('fx_021', MODEL_1B, 'verbalized')}

with open('fixtures/expected.jsonl', 'w', encoding='utf-8', newline='\n') as outfile:
    for row in rows:
        outfile.write(json.dumps(row) + '\n')

print('Wrote', len(rows), 'rows to fixtures/expected.jsonl')