import json
import os

from triviaqa_normalize import normalize_answer

def make_row(question_id, description, value, extra_aliases=()):
    normalized_value = normalize_answer(value)
    normalized_aliases = [normalized_value]
    for alias in extra_aliases:
        normalized_alias = normalize_answer(alias)
        if normalized_alias not in normalized_aliases:
            normalized_aliases.append(normalized_alias)

    return {
        "question_id": question_id,
        "question": 'Fixture: ' + description,
        "normalized_value": normalized_value,
        "normalized_aliases": normalized_aliases,
        "value": value
    }

CASES = [
    ('fx_001', 'two hits, list order', 'Paris', ['Paris France']),
    ('fx_002', 'substring must not match', 'exile', []),
    ('fx_003', 'markdown punctuation', 'Xiaowei Yi', []),
    ('fx_004', 'curly apostrophe in the response', "O'Neil", []),
    ('fx_005', 'single-character alias, refusal collision', 'I', []),
    ('fx_006', 'whitespace-only answer', 'Paris', []),
    ('fx_007', 'negation: not Paris', 'Paris', []),
    ('fx_008', 'negation: marker 4 words back', 'Vancouver', []),
    ('fx_009', 'negation: marker 5 words back', 'Vancouver', []),
    ('fx_010', 'negation: marker but no match', 'Vancouver', []),
    ('fx_011', 'multi-candidate true', 'Chihuahua', []),
    ('fx_012', 'multi-candidate miss', '13mm', []),
    ('fx_013', 'or inside a word', 'Orwell', []),
    ('fx_014', 'eleven-word answer', 'Paris', []),
    ('fx_015', 'truncation', 'Paris', []),
    ('fx_016', 'refusal', '1915', []),
    ('fx_017', 'refusal, hedged right', '1915', []),
    ('fx_018', 'refusal, hedged wrong', '1915', []),
    ('fx_019', '"not sure" is off the list', 'Lyon', []),
    ('fx_020', 'A row timed out', 'Paris', []),
    ('fx_021', 'A row not done', 'Paris', []),
    ('fx_022', 'C row timed out', 'Paris', []),
    ('fx_023', 'P(True): case variants and a Yes', 'Paris', []),
    ('fx_024', 'P(True): near-miss word', 'Paris', []),
    ('fx_025', 'P(True): leading space and lowercase', 'Paris', []),
    ('fx_026', 'P(True): empty token without bytes', 'Paris', []),
    ('fx_027', 'P(True): no true or false candidate', 'Paris', []),
    ('fx_028', 'P(True): True only at position 1', 'Paris', []),
    ('fx_029', 'confidence: plain integer', 'Paris', []),
    ('fx_030', 'confidence: percent sign', 'Paris', []),
    ('fx_031', 'confidence: leading zero', 'Paris', []),
    ('fx_032', 'confidence: zero', 'Paris', []),
    ('fx_033', 'confidence: surrounding whitespace', 'Paris', []),
    ('fx_034', 'confidence: a range', 'Paris', []),
    ('fx_035', 'confidence: spelled out', 'Paris', []),
    ('fx_036', 'confidence: out of range', 'Paris', []),
    ('fx_037', 'confidence: the word percent', 'Paris', []),
    ('fx_038', 'confidence: cut off at the token limit', 'Paris', []),
    ('fx_039', 'confidence: empty', 'Paris', []),
    ('fx_040', 'article inside the answer', 'Fiddler on the Roof', []),
    ('fx_041', 'confidence: doubled percent sign', 'Paris', []),
    ('fx_042', 'B row not done', 'Paris', []),
    ('fx_043', 'ten-word answer', 'Paris', []),
    ('fx_044', 'or inside the gold answer', 'Truth or Dare', []),
    ('fx_045', 'article at the start of the answer', 'The Hague', []),
    ('fx_046', 'empty alias', 'Paris', ['']),
    ('fx_047', 'en dash in the key', '1939\u20131945', []),
    ('fx_048', 'curly double quote in the key', '\u201cCasablanca\u201d', []),
    ('fx_049', 'negation: two-word marker', 'Vancouver', []),
    ('fx_050', 'negation: two-word marker straddling the window edge', 'Vancouver', []),
    ('fx_051', 'negation: marker inside another word', 'Vancouver', []),
    ('fx_052', 'curly double quotes around a plain key', 'Casablanca', []),
]

rows = []
for question_id, description, value, extra_aliases in CASES:
    rows.append(make_row(question_id, description, value, extra_aliases))

os.makedirs('fixtures', exist_ok=True)
with open('fixtures/items.jsonl', 'w', encoding='utf-8', newline='\n') as outfile:
    for row in rows:
        outfile.write(json.dumps(row) + '\n')

print('Wrote', len(rows), 'rows to fixtures/items.jsonl')