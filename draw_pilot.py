from datasets import load_dataset 
import json
from datetime import datetime

DRAW_SEED = 8
PILOT_N = 50
DATASET = 'mandarjoshi/trivia_qa'
CONFIG = 'unfiltered.nocontext'
SPLIT = 'validation'
DRAW = 'pilot'


# section 5: unfiltered.nocontext, validation split. nocontext strips evidence docs, validation because test answers aren't public.
dataset = load_dataset(DATASET, CONFIG, split=SPLIT)

# qf_1637 is corrupted in the source. I found that it was mis-wired: The answer entity is intact but its normalized_value field is blank.
# blankness is a symptom, not the defect itself. So I filtered on id because it is fixed, filtering on the blank would be filtering on the tell.
# the assert line guards against if the filter silently matches zero rows or two, which wouldn't crash, it'd produce a wrong draw file. 
kept = dataset.filter(lambda row: row['question_id'] != 'qf_1637')
assert len(kept) == len(dataset) - 1

# shuffling before selection prevents inheriting TriviaQA's storage order, without it the selector would just take the first 50 items in the 
# order the dataset gives them, which is not a random sample. Seed fixed and recorded that way a replicator can genuinely replicate the study
#  - they could run DRAW_SEED = 8 and receive the same batch of questions I did, true replication. I shuffled kept and not dataset that way
# the corrupted row is excluded.
# I used shuffled.select(range(PILOT_N)) instead of shuffled[0:50] because .select() returns a dataset while shuffled[0:50] returns a column 
# dictionary. I need rows, not columns.
# assert line verifies the sample = N - crashes if draw sized wrong.
shuffled = kept.shuffle(seed=DRAW_SEED)
pilot_items = shuffled.select(range(PILOT_N))
assert len(pilot_items) == PILOT_N

# Creates a list for items, then the loop takes the 5 needed values from reach row and assigns them to one item in the list. 
# The value field is kept for self-containment because it's the field that reveals corruption. The answer.type field was dropped because
# nothing uses it and unlabeled optionality cuts against having E1 as my only labeled exploratory.
# assert line verifies that the items list has 50 items. Crashes if it doesn't - loop dropped rows.
items = []
for row in pilot_items:
    item = {
        'question_id': row['question_id'],
        'question': row['question'],
        'normalized_value': row['answer']['normalized_value'],
        'normalized_aliases': row['answer']['normalized_aliases'],
        'value': row['answer']['value']
    }
    items.append(item)
assert len(items) == PILOT_N

# opens items_pilot.jsonl and writes 50 lines, each line containing one of the items in the items list, and each item 
# containing the 5 values needed. + '\n' creates a new line on every iteration, without it the file would be one line with 50 items on it.
# jsonl instead of json because one item per line means git diff shows which item changed rather than the whole file changed - and it's 
# readable in any editor.
with open('items_pilot.jsonl', 'w', encoding='utf-8', newline='\n') as outfile:
    for item in items:
        outfile.write(json.dumps(item) + '\n') 

# items_manifest.json is a sidecar file that contains info on how and when the pilot was ran. I chose this over a header in items_pilot.jsonl
# because JSONL has one object per line. That makes the manifest a single ~400-character line  and every reviewer would have to special-case 
# line 1 (for line in f breaks; line counts go N+1). Every value is derived from the run rather than typed by hand because a manifest is a 
# record of what the run did - a hand typed seed that disagrees with DRAW_SEED is worse than no manifest at all.
manifest = {
    'timestamp': datetime.now().isoformat(),
    'dataset': DATASET,
    'config': CONFIG,
    'split': SPLIT,
    'draw': DRAW,
    'draw_seed': DRAW_SEED,
    'source_rows': len(dataset),
    'skipped': ['qf_1637'],
    'items_drawn': len(items)
}

with open('items_manifest.json', 'w', encoding='utf-8', newline='\n') as outfile:
    json.dump(manifest, outfile, indent=2)