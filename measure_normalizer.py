# measure_normalizer.py
#
# Measurements behind lab log 10-19, the figures the prereg cites as "lab log 10-19":
#   does TriviaQA's normalize_answer reproduce the dataset's own normalized fields, which characters does it
#   leave alone, and how often does the old Grader Spec rule fail a perfect answer?
#
# Run from the repository root, with the project's virtual environment:
#     python measure_normalizer.py
# It reads the TriviaQA validation split (config unfiltered.nocontext) at the revision pinned below, prints each
# figure with a label, and writes nothing. The function under test is triviaqa_normalize.py, TriviaQA's own
# function copied unchanged. The refusal phrases and negation markers are read from the prereg, not retyped.
#
# Written with Claude (Sonnet 5.5) for Laz. The 10-19 figures were first produced by scratch scripts that were
# not kept; this script recomputes them from the pinned revision.
import re

from datasets import load_dataset

from triviaqa_normalize import normalize_answer

REVISION = '0f7faf33a3908546c6fd5b73a660e0f8ff173c2f'
PREREG = 'calibration_lab_prereg_TEMPLATE.md'

# Characters the function leaves alone, written as code points so this file stays plain ASCII.
CURLY_DOUBLE_QUOTES = chr(0x201C) + chr(0x201D)
EN_DASH = chr(0x2013)
EM_DASH = chr(0x2014)
ELLIPSIS = chr(0x2026)
CURLY_APOSTROPHE = chr(0x2019)
MIDDLE_DOT = chr(0x00B7)


def old_rule(text):
    # The Grader Spec's Normalize bullet before 10-19: lowercase, every character that is not a word
    # character or whitespace becomes a space, whitespace collapsed.
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', text.lower())).strip()


def contains_key(response, keys):
    # The Match rule: a key counts when it is preceded and followed by a space or an end of the text.
    # An empty key never matches.
    padded = ' ' + response + ' '
    for key in keys:
        if key and (' ' + key + ' ') in padded:
            return True
    return False


dataset = load_dataset('mandarjoshi/trivia_qa', 'unfiltered.nocontext', split='validation', revision=REVISION)
items = []
for row in dataset:
    answer = row['answer']
    items.append({
        'id': row['question_id'],
        'value': answer['value'],
        'normalized_value': answer['normalized_value'],
        'aliases': list(answer['aliases']),
        'normalized_aliases': list(answer['normalized_aliases']),
    })
total = len(items)
print('revision %s | validation items: %d' % (REVISION, total))


def keys_of(item):
    return [item['normalized_value']] + item['normalized_aliases']


# ---------------------------------------------------------------------------------------------------------------
print()
print('1. Does normalize_answer reproduce the dataset normalized fields?')
value_mismatches = [it['id'] for it in items if normalize_answer(it['value']) != it['normalized_value']]
print('   normalized_value differs on %d of %d items' % (len(value_mismatches), total))

alias_mismatches = []
empty_only = []
for it in items:
    mine = {normalize_answer(alias) for alias in it['aliases']}
    theirs = set(it['normalized_aliases'])
    if mine != theirs:
        alias_mismatches.append(it['id'])
        if mine - {''} == theirs:
            empty_only.append(it['id'])
print('   normalized_aliases (compared as sets) differ on %d items; %d of them differ only by an empty string: %s'
      % (len(alias_mismatches), len(empty_only), empty_only))

blank_values = [it['id'] for it in items if it['normalized_value'] == '']
empty_alias_items = [it['id'] for it in items if '' in it['normalized_aliases']]
print('   in the dataset: blank normalized_value on %d item(s) %s; items with an empty-string alias: %d'
      % (len(blank_values), blank_values, len(empty_alias_items)))

all_keys = []
for it in items:
    all_keys.extend(keys_of(it))
alias_entries = sum(len(it['normalized_aliases']) for it in items)
changed = [key for key in all_keys if normalize_answer(key) != key]
print('   re-applying the function to the dataset keys (%d values + %d alias entries = %d keys) changes %d of them'
      % (total, alias_entries, len(all_keys), len(changed)))

# ---------------------------------------------------------------------------------------------------------------
print()
print('2. Standalone a, an or the inside the dataset keys')
article = re.compile(r'\b(a|an|the)\b')
aliases_with_article = sum(1 for it in items for key in it['normalized_aliases'] if article.search(key))
values_with_article = sum(1 for it in items if article.search(it['normalized_value']))
print('   normalized_aliases entries containing one: %d of %d | normalized_value containing one: %d of %d'
      % (aliases_with_article, alias_entries, values_with_article, total))

# ---------------------------------------------------------------------------------------------------------------
print()
print('3. Characters the function leaves alone, found inside keys')
left_alone = CURLY_DOUBLE_QUOTES + EN_DASH + EM_DASH + ELLIPSIS
items_left_alone = [it for it in items if any(ch in key for key in keys_of(it) for ch in left_alone)]
items_en_dash = [it for it in items if any(EN_DASH in key for key in keys_of(it))]
print('   items with a key containing a curly double quote, an en or em dash or an ellipsis: %d (%.2f%% of %d), %d of them an en dash'
      % (len(items_left_alone), 100 * len(items_left_alone) / total, total, len(items_en_dash)))
print('   the ASCII hyphen and a curly apostrophe are punctuation to the function:')
for sample in ['13mm-15mm', 'I don' + CURLY_APOSTROPHE + 't know']:
    print('      %-18s -> %s' % (ascii(sample), ascii(normalize_answer(sample))))

# ---------------------------------------------------------------------------------------------------------------
print()
print('4. Do the prereg refusal phrases and negation markers pass through the function unchanged?')
prereg_lines = open(PREREG, encoding='utf-8').read().split('\n')
refusal_line = [line for line in prereg_lines if line.startswith('Refusal pattern list')][0]
refusal_phrases = [part.strip().rstrip('.') for part in refusal_line.split(':', 1)[1].split(MIDDLE_DOT)]
marker_line = [line for line in prereg_lines if line.startswith('- Negation Marker List:')][0]
negation_markers = [part.strip() for part in marker_line.split(':', 1)[1].split(',')]
print('   refusal phrases read from the prereg: %d | unchanged by the function: %s'
      % (len(refusal_phrases), all(normalize_answer(p) == p for p in refusal_phrases)))
print('   negation markers read from the prereg: %d | unchanged by the function: %s'
      % (len(negation_markers), all(normalize_answer(m) == m for m in negation_markers)))

# ---------------------------------------------------------------------------------------------------------------
print()
print('5. A perfect answer (the gold value) matched against the item\'s own keys')
fail_old = []
fail_new = []
for it in items:
    if not contains_key(old_rule(it['value']), [old_rule(key) for key in keys_of(it)]):
        fail_old.append(it)
    if not contains_key(normalize_answer(it['value']), keys_of(it)):
        fail_new.append(it)
old_ids = [it['id'] for it in fail_old]
print('   old Normalize rule: %d of %d items match none of their own keys (%.2f%%)'
      % (len(fail_old), total, 100 * len(fail_old) / total))
named = [it for it in fail_old if it['id'] in ('qf_1637', 'sfq_15030')]
others = [it for it in fail_old if it['id'] not in ('qf_1637', 'sfq_15030')]
with_article = [it for it in others if article.search(old_rule(it['value']))]
print('      %d have a standalone a, an or the in the gold value | named separately: %s | other: %s'
      % (len(with_article), [it['id'] for it in named], [it['id'] for it in others if it not in with_article]))
pool = total - 1
pool_fail_old = len([i for i in old_ids if i != 'qf_1637'])
print('      without qf_1637 (dropped at draw): %d of %d (%.2f%%)' % (pool_fail_old, pool, 100 * pool_fail_old / pool))
print('   normalize_answer on the response: %d item(s) fail: %s' % (len(fail_new), [it['id'] for it in fail_new]))
rate = len(fail_old) / total
print('   at the old rule\'s rate: about %.1f such items in a 50-item draw, about %.0f at N = 2200' % (50 * rate, 2200 * rate))

# ---------------------------------------------------------------------------------------------------------------
print()
print('6. Counts listed for the grader session (each with its definition; lab log 10-20 compares them with 10-19)')
one_char_any = [it for it in items if any(len(key) == 1 for key in keys_of(it))]
one_char_alnum = [it for it in items if any(len(key) == 1 and key.isalnum() for key in keys_of(it))]
one_letter_value = [it for it in items if re.fullmatch(r'[a-z]', it['normalized_value'])]
print('   items with a one-character key (value or any alias), any character: %d (%.2f%% of %d)'
      % (len(one_char_any), 100 * len(one_char_any) / total, total))
print('   items with a one-character key that is a letter or digit in any script: %d (%.2f%%)'
      % (len(one_char_alnum), 100 * len(one_char_alnum) / total))
print('   items whose normalized_value is one ASCII letter: %d' % len(one_letter_value))
refusal_hits = []
for it in items:
    for key in set(keys_of(it)):
        if key and any((' ' + key + ' ') in (' ' + phrase + ' ') for phrase in refusal_phrases):
            refusal_hits.append((it['id'], key))
print('   items where a key sits inside a refusal phrase, so the phrase alone would hit it: %d %s'
      % (len(set(i for i, k in refusal_hits)), sorted(set(refusal_hits))))
