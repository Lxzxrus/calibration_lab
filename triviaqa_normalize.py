# SPDX-License-Identifier: Apache-2.0
# normalize_answer, copied verbatim from TriviaQA's own evaluation script:
#   mandarjoshi90/triviaqa, evaluation/triviaqa_evaluation.py, commit 51b5359 (2017-05-05)
# License: Apache License 2.0, the license of that repository (copy in third_party/triviaqa/LICENSE).
#   This file is not under this repository's MIT License.
# Changes: none to the function body. It was extracted into this file and this header was added.
# The Grader Spec (prereg section 6, Normalize) cites this function. Do not change the function body.

import re
import string

def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""

    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def handle_punc(text):
        exclude = set(string.punctuation + "".join([u"‘", u"’", u"´", u"`"]))
        return ''.join(ch if ch not in exclude else ' ' for ch in text)

    def lower(text):
        return text.lower()

    def replace_underscore(text):
        return text.replace('_', ' ')

    return white_space_fix(remove_articles(handle_punc(lower(replace_underscore(s))))).strip()