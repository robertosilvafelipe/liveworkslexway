"""Create the public Past Perfect practice page (/curso/past-perfect).

Usage: python -m app.seed_past_perfect [--slug past-perfect]
Safe to run again: exercises already on that page (matched by title) are kept.
"""
import argparse

from .public_seed import publish

FORM = {
    "title": "1. Past Perfect — a forma (had + particípio)",
    "description": "O past perfect é formado por HAD + PAST PARTICIPLE (particípio). "
                   "Ele é igual para todas as pessoas: I had, you had, she had, they had…",
    "topic": "Forma",
    "items": [
        {"type": "match", "prompt": "Match the verb to its past participle.",
         "pairs": [
             {"left": "go", "right": "gone"}, {"left": "see", "right": "seen"}, {"left": "take", "right": "taken"},
             {"left": "write", "right": "written"}, {"left": "eat", "right": "eaten"}, {"left": "be", "right": "been"},
         ]},
        {"type": "group", "prompt": "Regular or irregular past participle?",
         "categories": ["Regular (-ed)", "Irregular"],
         "words": [
             {"text": "worked", "category": "Regular (-ed)"}, {"text": "finished", "category": "Regular (-ed)"},
             {"text": "visited", "category": "Regular (-ed)"}, {"text": "played", "category": "Regular (-ed)"},
             {"text": "broken", "category": "Irregular"}, {"text": "forgotten", "category": "Irregular"},
             {"text": "flown", "category": "Irregular"}, {"text": "left", "category": "Irregular"},
         ]},
        {"type": "dropdown", "prompt": "Choose the correct form.",
         "text": "1. She had [*finished|finish|finishing] her homework before dinner.\n"
                 "2. They had [went|*gone|go] home when I arrived.\n"
                 "3. I [have|*had|has] never seen snow before that trip.\n"
                 "4. He had [*written|wrote|write] three books by 2010.\n"
                 "5. We had [ate|*eaten|eat] all the cake before Mom got home."},
        {"type": "fill", "prompt": "Complete with the PAST PERFECT of the verb in parentheses.",
         "text": "1. When I arrived, the movie [had started|'d started] (start).\n"
                 "2. My friends [had left|'d left] the party when I got there. (leave)\n"
                 "3. Paula [had lost|'d lost] her keys, so she couldn't open the door. (lose)\n"
                 "4. By the end of the year, we [had saved|'d saved] enough money. (save)\n"
                 "5. I was tired because I [had worked|'d worked] all day. (work)"},
    ],
}

VS_SIMPLE = {
    "title": "2. Past Perfect x Past Simple",
    "description": "Use o past perfect para a ação que aconteceu ANTES de outra ação no passado. "
                   "A ação mais recente fica no past simple.\n"
                   "Ex.: When I got to the station (2º), the train had left (1º).",
    "topic": "Past perfect x past simple",
    "items": [
        {"type": "choice", "prompt": "\"When I got home, my sister had cooked dinner.\"\nWhat happened FIRST?",
         "options": ["I got home.", "My sister cooked dinner.", "Both happened at the same time."], "correct": 1},
        {"type": "truefalse", "prompt": "\"When Paul called, I had already gone to bed.\"\nTrue or false?",
         "statements": [
             {"text": "I went to bed before Paul called.", "answer": True},
             {"text": "Paul called before I went to bed.", "answer": False},
             {"text": "I was awake when Paul called.", "answer": False},
         ]},
        {"type": "dropdown", "prompt": "Past perfect or past simple? Choose the best option.",
         "text": "1. When we got to the station, the train [*had already left|already leaves].\n"
                 "2. By the time the police arrived, the thief [*had escaped|escapes].\n"
                 "3. Yesterday I [*went|had gone] to the cinema with my friends.\n"
                 "4. She was nervous because she [*had never flown|never flies] before.\n"
                 "5. I didn't recognize him because he [*had changed|changes] a lot."},
        {"type": "fill", "prompt": "Complete with the verbs in parentheses. Use the past simple for the later action and the past perfect for the earlier one.",
         "text": "1. When I [arrived] (arrive), the class [had started|'d started] (start).\n"
                 "2. After she [had finished|'d finished] (finish) the report, she [went] (go) home.\n"
                 "3. We [didn't eat|did not eat] (not eat) at the party because we [had had|'d had] (have) dinner before."},
        {"type": "order", "prompt": "Put the words in the correct order.",
         "tokens": ["By", "the", "time", "we", "arrived,", "the", "party", "had", "finished."],
         "alternatives": ["The party had finished by the time we arrived."]},
    ],
}

NEG_QUESTIONS = {
    "title": "3. Negativas e perguntas",
    "description": "Negativa: HAD NOT (hadn't) + particípio → I hadn't seen it.\n"
                   "Pergunta: HAD + sujeito + particípio → Had you seen it?\n"
                   "Resposta curta: Yes, I had. / No, I hadn't.",
    "topic": "Negativas e perguntas",
    "items": [
        {"type": "fill", "prompt": "Complete with the NEGATIVE form of the past perfect.",
         "text": "1. I [hadn't seen|had not seen] that movie before. (see)\n"
                 "2. They [hadn't met|had not met] before the wedding. (meet)\n"
                 "3. She [hadn't studied|had not studied] for the test, so she was worried. (study)\n"
                 "4. We [hadn't booked|had not booked] a table, so we waited for an hour. (book)"},
        {"type": "dropdown", "prompt": "Choose the correct word to complete the question.",
         "text": "1. [*Had|Did|Have] you finished your homework before the class started?\n"
                 "2. Had she ever [*been|was|be] to Paris before 2015?\n"
                 "3. [*Had|Did|Were] they left before you arrived?"},
        {"type": "order", "prompt": "Put the words in the correct order to make a question.",
         "tokens": ["Had", "you", "ever", "been", "to", "London", "before", "2020?"], "alternatives": []},
        {"type": "match", "prompt": "Match the questions to the short answers.",
         "pairs": [
             {"left": "Had you eaten before the movie?", "right": "No, I hadn't."},
             {"left": "Had he left when you called?", "right": "Yes, he had."},
             {"left": "Had they arrived before the rain?", "right": "No, they hadn't."},
             {"left": "Had she called you before the meeting?", "right": "Yes, she had."},
             {"left": "Had it stopped raining when you left?", "right": "No, it hadn't."},
         ]},
    ],
}

READING = {
    "title": "4. Reading & writing — A bad day",
    "description": "Leia o texto e responda. No final, escreva sobre um dia ruim que você teve usando o past perfect.",
    "topic": "Leitura e escrita",
    "items": [
        {"type": "truefalse",
         "prompt": "Read the text and choose True or False.\n\n"
                   "\"Last Monday was a terrible day for Lucy. When she woke up, she saw that her alarm hadn't rung, "
                   "so she was late. When she got to the bus stop, the bus had already left. She took a taxi, but when "
                   "she arrived at the office, the meeting had started. Her boss was angry because Lucy had forgotten to "
                   "send an important report the day before. At lunch, she realized she had left her wallet at home! "
                   "Fortunately, her friend Mark had brought sandwiches for two.\"",
         "statements": [
             {"text": "Lucy's alarm rang on time.", "answer": False},
             {"text": "The bus left before Lucy got to the bus stop.", "answer": True},
             {"text": "The meeting started before Lucy arrived.", "answer": True},
             {"text": "Lucy had sent the report the day before.", "answer": False},
             {"text": "Mark had brought food for Lucy too.", "answer": True},
         ]},
        {"type": "fill", "prompt": "Complete the sentences about Lucy's day with the past perfect.",
         "text": "1. Lucy was late because her alarm [hadn't rung|had not rung].\n"
                 "2. When she got to the bus stop, the bus [had already left|had left].\n"
                 "3. Her boss was angry because she [had forgotten] to send the report.\n"
                 "4. She couldn't pay for lunch because she [had left] her wallet at home."},
        {"type": "free", "prompt": "Write 3 to 5 sentences about a bad day you had. Use the past perfect at least twice.",
         "model_answer": "Last year I had a terrible day at work. When I got to the office, I realized I had left my laptop "
                         "at home. I went back to get it, but when I returned, the meeting had already finished. "
                         "My boss was upset because I hadn't sent him the presentation.",
         "keywords": ["had"], "min_words": 25, "points": 3},
    ],
}

SPECS = (FORM, VS_SIMPLE, NEG_QUESTIONS, READING)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", default="past-perfect")
    publish(ap.parse_args().slug, "B1", SPECS)


if __name__ == "__main__":
    main()
