from datasets import load_dataset 

DRAW_SEED = 8
PILOT_N = 50

# section 5: unfiltered.nocontext, validation split. nocontext strips evidence docs, validation because test answers aren't public.
dataset = load_dataset('mandarjoshi/trivia_qa', 'unfiltered.nocontext', split='validation')
print(len(dataset))

# qf_1637 is corrupted in the source. I found that it was mis-wired: The answer entity is intact but its normalized_value field is blank.
# blankness is a symptom, not the defect itself. So I filtered on id because it is fixed, filtering on the blank would be filtering on the tell.
# the assert line guards against if the filter silently matches zero rows or two, which wouldn't crash, it'd produce a wrong draw file. 
kept = dataset.filter(lambda row: row['question_id'] != 'qf_1637')
print(len(kept))
assert len(kept) == len(dataset) - 1

# shuffling before selection guarantees true pseudorandom selection, without it the selector would just take the first 50 items in the order the 
# dataset gives them, which is not a random sample. Seed fixed and recorded that way a replicator can genuinely replicate the study - 
# they could run DRAW_SEED = 8 and receive the same batch of questions I did, true replication. I shuffled kept and not dataset that way 
# the corrupted row is excluded.
shuffled = kept.shuffle(seed=DRAW_SEED)
pilot_items = shuffled.select(range(PILOT_N))
print(len(pilot_items))
assert len(pilot_items) == PILOT_N