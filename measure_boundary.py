# measure_boundary.py
#
# Measurements behind lab log 10-20, the figures the prereg cites as "lab log 10-20":
#   which word boundary the Match rule uses, what regex \b would have done instead, and what the characters
#   TriviaQA's normalizer leaves alone (en and em dashes, curly double quotes, the ellipsis) cost under it.
#
# Run from the repository root, with the project's virtual environment:
#     python measure_boundary.py
# It reads the TriviaQA validation split (config unfiltered.nocontext) at the revision pinned below, prints each
# figure with a label, and writes nothing. The function under test is triviaqa_normalize.py, TriviaQA's own
# function copied unchanged.
#
# Written with Claude (Sonnet 5.5) for Laz. measure_normalizer.py holds the 10-19 figures.
import re
import unicodedata
from collections import Counter

from datasets import load_dataset

from triviaqa_normalize import normalize_answer

REVISION = '0f7faf33a3908546c6fd5b73a660e0f8ff173c2f'

# Characters the function leaves alone, written as code points so this file stays plain ASCII.
EN_DASH = chr(0x2013)
EM_DASH = chr(0x2014)
ELLIPSIS = chr(0x2026)
LEFT_QUOTE = chr(0x201C)
RIGHT_QUOTE = chr(0x201D)
CURLY_DOUBLE_QUOTES = LEFT_QUOTE + RIGHT_QUOTE


def old_rule(text):
    # The Grader Spec's Normalize bullet before 10-19: lowercase, every character that is not a word
    # character or whitespace becomes a space, whitespace collapsed.
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', text.lower())).strip()


# Three ways to ask "is this key in the response as a whole word or phrase?". An empty key never matches.
def match_space(response, key):
    # The Match rule: preceded and followed by a space or an end of the text.
    return (' ' + key + ' ') in (' ' + response + ' ')


def match_lookaround(response, key):
    # The same rule written as a regex: not preceded and not followed by a non-space character.
    return re.search(r'(?<!\S)' + re.escape(key) + r'(?!\S)', response) is not None


def match_word_boundary(response, key):
    # Literal regex \b on both sides, the wording the Match bullet used before 10-20.
    return re.search(r'\b' + re.escape(key) + r'\b', response) is not None


def any_key_matches(response, keys, matcher):
    for key in keys:
        if key and matcher(response, key):
            return True
    return False


dataset = load_dataset('mandarjoshi/trivia_qa', 'unfiltered.nocontext', split='validation', revision=REVISION)
items = []
for row in dataset:
    answer = row['answer']
    items.append({
        'id': row['question_id'],
        'value': answer['value'],
        'aliases': list(answer['aliases']),
        'keys': [answer['normalized_value']] + list(answer['normalized_aliases']),
    })
total = len(items)
by_id = {it['id']: it for it in items}
print('revision %s | validation items: %d' % (REVISION, total))


def name(ch):
    return 'U+%04X %s' % (ord(ch), unicodedata.category(ch))


# ---------------------------------------------------------------------------------------------------------------
print()
print('1. A perfect answer (the gold value) against the item\'s own keys, by boundary')
matchers = [('space-padding', match_space), ('lookarounds', match_lookaround), ('literal \\b', match_word_boundary)]
failing = {}
for label, matcher in matchers:
    ids = [it['id'] for it in items
           if not any_key_matches(old_rule(it['value']), [old_rule(k) for k in it['keys']], matcher)]
    failing[('old', label)] = set(ids)
    print('   old Normalize rule, %-13s fails on %d items (%.2f%%)' % (label, len(ids), 100 * len(ids) / total))
print('   old rule: same failing items under space-padding and \\b: %s' % (failing[('old', 'space-padding')] == failing[('old', 'literal \\b')]))
for label, matcher in matchers:
    ids = [it['id'] for it in items if not any_key_matches(normalize_answer(it['value']), it['keys'], matcher)]
    failing[('new', label)] = set(ids)
    print('   normalize_answer,   %-13s fails on %d items %s' % (label, len(ids), sorted(ids) if len(ids) < 12 else ''))
print('   lookarounds fail on exactly the same items as space-padding: %s'
      % (failing[('new', 'lookarounds')] == failing[('new', 'space-padding')]))
extra = sorted(failing[('new', 'literal \\b')] - failing[('new', 'space-padding')])
print('   fail under literal \\b but not under space-padding: %d' % len(extra))
for item_id in extra:
    it = by_id[item_id]
    response = normalize_answer(it['value'])
    print('      %-10s response %-34s first %-16s last %s' % (item_id, ascii(response)[:34], name(response[0]), name(response[-1])))

# ---------------------------------------------------------------------------------------------------------------
print()
print('2. Keys that begin or end with a non-word character (where \\b cannot match even identical text)')
edge_keys = 0
edge_items = set()
edge_chars = Counter()
for it in items:
    for key in it['keys']:
        if key and (re.match(r'\W', key) or re.search(r'\W$', key)):
            edge_keys += 1
            edge_items.add(it['id'])
            for ch in {key[0], key[-1]}:
                if re.match(r'\W', ch):
                    edge_chars[ch] += 1
print('   keys: %d | items: %d (%.2f%% of %d)' % (edge_keys, len(edge_items), 100 * len(edge_items) / total, total))
print('   commonest edge characters (number of keys): %s' % [(name(ch), n) for ch, n in edge_chars.most_common(8)])

# ---------------------------------------------------------------------------------------------------------------
print()
print('3. Dash and quote counts that section 10 cites')
items_en = [it for it in items if any(EN_DASH in key for key in it['keys'])]
items_em = [it for it in items if any(EM_DASH in key for key in it['keys'])]
items_quote = [it for it in items if any(ch in key for key in it['keys'] for ch in CURLY_DOUBLE_QUOTES)]
print('   a key holds the character: en dash %d items | em dash %d items | curly double quote %d items'
      % (len(items_en), len(items_em), len(items_quote)))
print('   Definition for the next two lines: for each key that holds the character, write the response as that key')
print('   with the character swapped for what a typist would use (an ASCII hyphen for the en dash, which')
print('   normalization turns into a space; nothing for the curly double quotes), then apply the Match rule')
print('   against all of the item\'s keys. "Matches no key" means none of them is found.')


def typed_variant_misses(candidates, swap):
    missed = []
    for it in candidates:
        variants = [normalize_answer(swap(key)) for key in it['keys'] if key and swap(key) != key]
        if not any(any_key_matches(v, it['keys'], match_space) for v in variants):
            missed.append(it['id'])
    return missed


missed_en = typed_variant_misses(items_en, lambda key: key.replace(EN_DASH, '-'))
missed_quote = typed_variant_misses(items_quote, lambda key: key.replace(LEFT_QUOTE, '').replace(RIGHT_QUOTE, ''))
print('   en dash typed as a hyphen: matches no key for %d of %d items %s' % (len(missed_en), len(items_en), missed_en))
print('   curly double quotes left out: matches no key for %d of %d items %s' % (len(missed_quote), len(items_quote), missed_quote))

print()
print('   The gold value holds an ASCII hyphen, so the keys hold a space.')
HYPHEN_BETWEEN = re.compile(r'(?<=[A-Za-z0-9])-(?=[A-Za-z0-9])')
hyphen_items = [it for it in items if HYPHEN_BETWEEN.search(it['value'])]
no_en_key = [it for it in hyphen_items if not any(EN_DASH in key for key in it['keys'])]
digit_ranges = [it for it in no_en_key if re.search(r'\d-\d', it['value']) and not re.search(r'[A-Za-z]-|-[A-Za-z]', it['value'])]
print('   gold value has a hyphen between two letters or digits: %d items (%.2f%%)' % (len(hyphen_items), 100 * len(hyphen_items) / total))
print('      of those, no key holds an en dash: %d | of the %d, digit-to-digit ranges: %d'
      % (len(no_en_key), len(no_en_key), len(digit_ranges)))
alias_or_value = [it for it in items if (HYPHEN_BETWEEN.search(it['value']) or any(HYPHEN_BETWEEN.search(a) for a in it['aliases']))
                  and not any(EN_DASH in key for key in it['keys'])]
print('   gold value or some raw alias has such a hyphen, no key holds an en dash: %d items (%.2f%%)'
      % (len(alias_or_value), 100 * len(alias_or_value) / total))
print('   TESTED: the gold value with each of those hyphens typed as another dash, normalized, then the Match rule')
print('   against all of the item\'s keys:')
for dash_name, dash in (('en dash', EN_DASH), ('em dash', EM_DASH)):
    results = {}
    for it in hyphen_items:
        response = normalize_answer(HYPHEN_BETWEEN.sub(dash, it['value']))
        results[it['id']] = any_key_matches(response, it['keys'], match_space)
    none_all = [i for i, ok in results.items() if not ok]
    none_no_en = [it['id'] for it in no_en_key if not results[it['id']]]
    still = [it['id'] for it in no_en_key if results[it['id']]]
    print('      typed as %s: matches no key for %d of %d items; among the %d with no en-dash key: %d match none, %d still match some key'
          % (dash_name, len(none_all), len(hyphen_items), len(no_en_key), len(none_no_en), len(still)))
    for item_id in still:
        it = by_id[item_id]
        response = normalize_answer(HYPHEN_BETWEEN.sub(dash, it['value']))
        hit = [k for k in it['keys'] if k and match_space(response, k)]
        print('         still matches: %-10s value %-30s response %-34s via key %s'
              % (item_id, ascii(it['value'])[:30], ascii(response)[:34], ascii(hit[0])[:30]))

# ---------------------------------------------------------------------------------------------------------------
print()
print('4. A correct answer next to a character the normalizer leaves alone (plain key casablanca)')
demo = [
    ('plain, trailing period', 'Casablanca.'),
    ('ASCII double quotes', '"Casablanca"'),
    ('markdown bold', '**Casablanca**'),
    ('spaced en dash', 'Casablanca ' + EN_DASH + ' the film'),
    ('curly double quotes', LEFT_QUOTE + 'Casablanca' + RIGHT_QUOTE),
    ('em dash attached', 'Casablanca' + EM_DASH + 'a film'),
    ('en dash attached', 'Casablanca' + EN_DASH + 'the film'),
    ('ellipsis attached', 'Casablanca' + ELLIPSIS),
]
for label, response in demo:
    normalized = normalize_answer(response)
    print('   %-24s -> %-28s whitespace rule: %-5s | literal \\b: %s'
          % (label, ascii(normalized), match_space(normalized, 'casablanca'), match_word_boundary(normalized, 'casablanca')))

print()
print('5. The two curly-quote fixtures')
curly_key = normalize_answer(LEFT_QUOTE + 'Casablanca' + RIGHT_QUOTE)
cases = [
    ('fx_048: curly key, identical curly-quoted response', curly_key, LEFT_QUOTE + 'Casablanca' + RIGHT_QUOTE),
    ('fx_052: plain key, curly-quoted response', 'casablanca', LEFT_QUOTE + 'Casablanca' + RIGHT_QUOTE),
    ('(not planned) curly key, straight-quoted response', curly_key, '"Casablanca"'),
]
for label, key, response in cases:
    normalized = normalize_answer(response)
    print('   %-52s whitespace rule: %-5s | literal \\b: %s'
          % (label, match_space(normalized, key), match_word_boundary(normalized, key)))
