"""Build listening audios on a Mac (uses macOS `say` + afconvert). Usage: python3 deploy/make_audio.py app/static/audio/<slug> [name-prefix ...]
Each script: list of (voice, text, pause_after_ms) -> one m4a."""
import os, re, subprocess, sys, tempfile, wave

sys.path.insert(0, os.path.dirname(__file__))
import tts  # noqa: E402

F = "Samantha"
M = "Reed (English (US))"
F2 = "Flo (English (US))"  # extra voices for 3+ speakers
M2 = "Eddy (English (US))"
FS, MJ = "SARAH", "JERRY"  # Básico 2 voices chosen by the user: Sarah (female) and Jerry B. (male)
RATE = "135"


def sp(spelling, pause=380):
    """'B, double O, K' -> letters spoken by name (literal mode), short pause between them."""
    out = []
    for tok in [t.strip() for t in spelling.split(",")]:
        if tok.startswith("double "):
            out.append(f"double [[char LTRL]]{tok[7:]}[[char NORM]]")
        else:
            out.append(f"[[char LTRL]]{tok}[[char NORM]]")
    return f" [[slnc {pause}]] ".join(out)


SCRIPTS = {
    "aula1-letters": [
        ("SARAH", f"Number {n}. [[slnc 500]] {sp(l)}.", 2800)
        for n, l in zip(["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"],
                        ["G", "Y", "V", "M", "E", "J", "W", "L", "F", "X"])],
    "aula1-words": [
        ("MAX", f"Number {n}. [[slnc 700]] {sp(w, 700)}.", 3000)
        for n, w in zip(["one", "two", "three", "four", "five", "six"],
                        ["B, U, S", "C, A, R", "P, E, N", "B, double O, K", "D, E, S, K", "N, O, T, E, B, double O, K"])],
    "aula1-names": [
        ("SARAH", "Hi! What's your name?", 500), ("JERRY", "My name is Daniel.", 500),
        ("SARAH", "How do you spell your name?", 500), ("JERRY", sp("D, A, N, I, E, L") + ".", 700),
        ("SARAH", "And what's your last name?", 500), ("JERRY", "Mitchell.", 500),
        ("SARAH", "How do you spell your last name?", 500), ("JERRY", sp("M, I, T, C, H, E, double L") + ".", 900),
        ("JERRY", "And you? What's your name?", 500), ("SARAH", "I'm Kelly. " + sp("K, E, double L, Y") + ".", 700),
        ("JERRY", "And your last name?", 500), ("SARAH", "Gibbs. " + sp("G, I, double B, S") + ".", 600),
        ("JERRY", "Nice to meet you, Kelly!", 300),
    ],
}
# Aula 01 speaking models: one file per letter / sentence
for _l in "AEIOUGJKQWYH":
    SCRIPTS[f"aula1-say-{_l.lower()}"] = [(F, sp(_l) + ".", 300)]
for _i, _t in enumerate(["What's your name?", "How do you spell your name?", "What's your last name?",
                          "How do you spell bus?"], 1):
    SCRIPTS[f"aula1-say-s{_i}"] = [(F, _t, 300)]
SCRIPTS["aula1-hotel"] = [
    (F, "Good evening! Welcome to the Sunset Hotel. What's your name, please?", 600),
    (M, "Hi! My name is Bruno Teixeira.", 600),
    (F, "How do you spell your last name?", 600),
    (M, sp("T, E, I, X, E, I, R, A") + ".", 700),
    (F, "Thank you, Mister Teixeira. And what's your first name? Is it " + sp("B, R, U, N, O") + "?", 600),
    (M, "Yes, that's right.", 600),
    (F, "Perfect. Your room is number twelve. Here's your key!", 600),
    (M, "Thank you very much!", 300),
]

# ---------- Aula 02 — Classroom Language ----------
_AULA2_DICT = ["I have a question.", "Can you repeat, please?", "You're frozen.", "My internet connection is slow today.",
               "What does spoon mean?", "How do I say copo in English?"]
SCRIPTS["aula2-dictation"] = [(F, "Listen and complete the sentences.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {t} [[slnc 1800]] {t}", 3200)
    for n, t in zip(["one", "two", "three", "four", "five", "six"], _AULA2_DICT)]
SCRIPTS["aula2-class"] = [
    (F, "Good morning! Can you hear me?", 700),
    (F, "Hello? Pedro? Can you hear me?", 900),
    (M, "Sorry, I was muted. Yes, I can hear you now.", 600),
    (F, "Great! Hmm, Pedro, you're breaking up.", 600),
    (M, "Sorry, teacher. My internet connection is slow today.", 600),
    (F, "No problem. Do you have any questions?", 600),
    (M, "Yes, I have a question. How do I say caderno in English?", 600),
    (F, "Notebook.", 500),
    (M, "Can you repeat, please?", 500),
    (F, "Notebook. " + sp("N, O, T, E, B, double O, K") + ".", 600),
    (M, "Thank you!", 500),
    (F, "You're welcome. Bye! See you next class.", 300),
]
for _k, _t in {"q1": "How do I say livro in English?", "q2": "What does spoon mean?", "q3": "How do you spell table?",
               "o1": "Can you hear me?", "o2": "You're breaking up.", "o3": "My internet connection is slow today.",
               "o4": "You're frozen.", "o5": "You're muted.",
               "e1": "I don't know.", "e2": "I have a question.", "e3": "Can you repeat, please?", "e4": "Thank you.",
               "e5": "Bye! See you next class."}.items():
    SCRIPTS[f"aula2-say-{_k}"] = [(F, _t, 300)]
SCRIPTS["aula2-chat"] = [
    (F, "Good morning, everybody! Can you hear me?", 600),
    (M, "Yes, I can hear you, teacher!", 600),
    (F2, "Teacher, you're breaking up. My internet connection is slow today.", 600),
    (F, "No problem, Julia. Lucas, you're muted! Turn on your microphone, please.", 600),
    (M2, "Sorry! I have a question. How do I say cadeira in English?", 600),
    (F, "Chair. " + sp("C, H, A, I, R") + ".", 600),
    (F2, "What does desk mean?", 600),
    (F, "Desk means carteira, or mesa de escritório.", 600),
    (M, "Can you repeat, please?", 600),
    (F, "Of course! Desk. " + sp("D, E, S, K") + ".", 600),
    (M, "Thank you!", 600),
    (F, "Bye, everybody! See you next class!", 300),
]

# ---------- Aula 03 — Greetings ----------
_AULA3_DICT = [("What is your name?", "What's your name?"), ("My name is Vanessa.", "My name's Vanessa."),
               ("How are you doing?", "How are you doing?"), ("I'm fine, thank you.", "I'm fine, thank you."),
               ("Good afternoon!", "Good afternoon!"), ("Take care!", "Take care!")]
SCRIPTS["aula3-dictation"] = [(F, "Listen and complete the sentences.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] [[rate 105]] {slow} [[rate 135]] [[slnc 1800]] [[rate 175]] {fast}", 3200)
    for n, (slow, fast) in zip(["one", "two", "three", "four", "five", "six"], _AULA3_DICT)]
SCRIPTS["aula3-situations"] = [
    (F, "Listen. What greeting do they use?", 1200),
    (F, "Number one.", 600), (M, "Good evening! Welcome to the party!", 2500),
    (F, "Number two.", 600), (F2, "OK, I'm going to bed now. Good night!", 2500),
    (F, "Number three.", 600), (M2, "Good afternoon, everybody. Let's start the meeting.", 2500),
    (F, "Number four.", 600), (F2, "Good morning! Here's your coffee.", 1000),
]
SCRIPTS["aula3-dialogue"] = [
    (M, "Good afternoon! Hi! What's your name?", 600),
    (F, "Hello! I'm Sarah. And you?", 600),
    (M, "My name's Daniel. Nice to meet you, Sarah.", 600),
    (F, "Nice to meet you too.", 500),
    (M, "So, how are you doing?", 600),
    (F, "I'm great, thanks! And you?", 600),
    (M, "I'm fine, thank you. Well, class is starting!", 600),
    (F, "Ha ha. OK! See you next class!", 600),
    (M, "Bye! Take care!", 300),
]
for _p, _list in {"g": ["Hello!", "Hi!", "Hey!", "Good morning!", "Good afternoon!", "Good evening!"],
                  "q": ["What's your name?", "My name's Vanessa.", "I'm Vanessa.", "How are you?", "How are you doing?",
                        "I'm fine, thank you. And you?", "All good!"],
                  "b": ["Goodbye!", "Bye bye!", "See you!", "See you next class!", "Take care!", "Good night!"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula3-say-{_p}{_i}"] = [(F, _t, 300)]
SCRIPTS["aula3-reading"] = [
    (F, "Good evening, everybody! Welcome to the English class!", 600),
    (M2, "Good evening, teacher!", 600),
    (F, "My name's Laura. What's your name?", 600),
    (M, "Hi, Laura! I'm Rafael.", 600),
    (F, "Nice to meet you, Rafael. How are you doing?", 600),
    (M, "I'm great, thanks! And you?", 600),
    (F, "I'm fine, thank you.", 600),
    (F2, "Hey! My name is Beatriz, but you can call me Bia.", 600),
    (F, "Hello, Bia! How are you?", 600),
    (F2, "All good!", 1500),
    (F, "OK, everybody. Good night! See you next class!", 600),
    (M, "Bye, teacher! Take care!", 600),
    (F2, "Good night!", 300),
]

# ---------- Aula 04 — Daily Routine ----------
SCRIPTS["aula4-hr"] = [(F, "H or R? Listen and choose the word.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w}. [[slnc 1400]] {w}.", 2400)
    for n, w in zip(["one", "two", "three", "four", "five", "six"], ["rat", "hope", "red", "hat", "ride", "have"])]
_AULA4_DICT = ["I take a shower.", "I brush my teeth.", "I get dressed.", "I have lunch at one o'clock.",
               "I go to the gym.", "I go to bed at eleven."]
SCRIPTS["aula4-dictation"] = [(F, "Listen and complete the sentences.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {t} [[slnc 1800]] {t}", 3000)
    for n, t in zip(["one", "two", "three", "four", "five", "six"], _AULA4_DICT)]
SCRIPTS["aula4-kevin"] = [
    (M, "Hi, I'm Kevin. What do I do in the morning? Well, I wake up at six thirty.", 600),
    (M, "First, I take a shower. Then I have coffee. Just coffee. I don't have breakfast at home.", 600),
    (M, "After that, I go to the gym. I love the gym!", 600),
    (M, "Next, I get dressed and I have breakfast at a cafe near my office.", 600),
    (M, "And finally, I start work at nine a.m.", 300),
]
for _p, _list in {"v": ["wake up", "have breakfast", "brush my teeth", "take a shower", "get dressed", "start work",
                        "have lunch", "go to the gym", "watch TV", "go to bed"],
                  "h": ["have", "house", "hospital", "helicopter", "hat", "read", "red", "rat"],
                  "s": ["What do you do in the morning?", "First, I take a shower.", "Then I have breakfast.",
                        "After that, I brush my teeth.", "Finally, I start work at 9 a.m."]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula4-say-{_p}{_i}"] = [(F, _t + ("." if _p != "s" else ""), 300)]
SCRIPTS["aula4-carol"] = [
    (F, "My day. By Carol.", 900),
    (F, "Hi! I'm Carol and I'm a nurse. My day is very busy!", 600),
    (F, "First, I wake up at five thirty a.m. Then I take a shower and I get dressed. "
        "After that, I have breakfast with my family: bread and coffee. Next, I brush my teeth "
        "and I go to the hospital. I start work at seven a.m.", 700),
    (F, "I have lunch at twelve o'clock at the hospital. I finish work at three p.m. "
        "Then I go to the gym. In the evening, I study English and I read a book.", 700),
    (F, "I don't watch TV. Finally, I go to bed at ten p.m.", 300),
]

# ---------- Aula 05 — Numbers ----------
_N = ["one", "two", "three", "four", "five", "six"]
SCRIPTS["aula5-teens"] = [(F, "Listen and choose the number.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w}. [[slnc 1400]] {w}.", 2400)
    for n, w in zip(_N, ["thirteen", "fifty", "sixteen", "seventy", "eighteen", "ninety"])]
SCRIPTS["aula5-dictation"] = [(F, "Listen and write the numbers.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w}. [[slnc 1400]] {w}.", 2400)
    for n, w in zip(_N, ["twelve", "twenty", "forty-five", "sixty-seven", "one hundred", "three thousand"])]
SCRIPTS["aula5-phones"] = [
    (F, "Listen and write the phone numbers.", 1200),
    (M, "Anna, what's your phone number?", 500), (F2, "It's two, double three, [[slnc 300]] four, eight, seven, oh.", 900),
    (M, "Two, double three, four, eight, seven, oh. Thanks!", 1800),
    (F, "Tom, what's your phone number?", 500), (M2, "My phone number is nine, one, six, [[slnc 300]] double oh, double five.", 900),
    (F, "Sorry? Can you repeat, please?", 500), (M2, "Nine, one, six, [[slnc 300]] double oh, double five.", 1800),
    (M, "And you, Lucy?", 500), (F, "It's seven, oh, four, [[slnc 300]] two, six, one, eight.", 900),
    (M, "Seven, oh, four, two, six, one, eight. Great!", 300),
]
SCRIPTS["aula5-times"] = [(F, "What time is it? Listen and write.", 1200)] + [
    (v, f"Number {n}. [[slnc 500]] What time is it? [[slnc 400]] It's {t}.", 2600)
    for n, v, t in zip(_N, [M, F2, M2, M, F2],
                       ["ten o'clock", "two twenty-five", "four fifteen", "ten forty", "five forty-five"])]
for _p, _list in {"n": ["one", "two", "three", "eight", "twelve", "twenty", "a hundred", "a thousand"],
                  "t": ["thirteen, [[slnc 500]] thirty", "fourteen, [[slnc 500]] forty",
                        "fifteen, [[slnc 500]] fifty", "sixteen, [[slnc 500]] sixty"],
                  "q": ["What's your phone number?", "My phone number is nine one six, double oh, double five.",
                        "How old are you?", "I'm thirty-six years old.",
                        "What time do you wake up?", "I wake up at six o'clock."]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula5-say-{_p}{_i}"] = [(F, _t + ("." if _p != "q" else ""), 300)]
SCRIPTS["aula5-reading"] = [
    (F, "Good afternoon! What's your name, please?", 600),
    (M, "Hi! My name's Marcos Oliveira.", 600),
    (F, "How old are you, Marcos?", 600),
    (M, "I'm twenty-seven years old.", 600),
    (F, "And what's your phone number?", 600),
    (M, "It's nine one six, double oh, double five.", 600),
    (F, "Sorry? Can you repeat, please?", 600),
    (M, "Sure! Nine one six, double oh, double five.", 600),
    (F, "Thank you. Your class is on Mondays at seven p.m., in room one oh two.", 600),
    (M, "Great! What time is it now?", 600),
    (F, "It's four fifteen.", 600),
    (M, "OK. Thank you! See you!", 300),
]

# ---------- Aula 06 — Days, Seasons, Months ----------
SCRIPTS["aula6-tt"] = [(F, "Tuesday or Thursday? Listen and choose.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w}. [[slnc 1400]] {w}.", 2400)
    for n, w in zip(["one", "two", "three", "four"], ["Thursday", "Tuesday", "Tuesday", "Thursday"])]
SCRIPTS["aula6-dictation"] = [(F, "Listen and write the days and the months.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w}. [[slnc 1400]] {w}.", 2600)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["Wednesday", "Saturday", "February", "August", "Friday", "June"])]
SCRIPTS["aula6-dialogue"] = [
    (F2, "Ben, what's your favorite day of the week?", 500),
    (M, "Sunday! Because I relax. And you, Clara?", 500),
    (F2, "My favorite day is Friday, because I go out with my friends.", 700),
    (M, "What's your favorite season?", 500),
    (F2, "Spring. I love flowers. And you?", 500),
    (M, "Winter! Because I love hot chocolate.", 700),
    (M, "And what's your favorite month?", 500),
    (F2, "July. Why? Because my birthday is in July!", 500),
    (M, "Ha ha! Cool!", 300),
]
for _p, _list in {"d": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                  "m": ["winter", "spring", "summer", "autumn", "fall", "January", "February", "August", "October"],
                  "q": ["What's your favorite day of the week?", "My favorite day of the week is Saturday because I relax.",
                        "What's your favorite season?", "My favorite season is summer because I can go to the beach.",
                        "What's your favorite month?", "My favorite month is December because I love Christmas."]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula6-say-{_p}{_i}"] = [(F, _t + ("." if _p != "q" else ""), 300)]
SCRIPTS["aula6-reading"] = [
    (M, "My favorites. By Lucas.", 900),
    (M, "Hi! I'm Lucas and I'm from Brazil. I'm nineteen years old.", 600),
    (M, "My favorite day of the week is Friday because I go to the gym with my friends. "
        "I don't like Monday because I start work at seven a.m.!", 700),
    (M, "My favorite season is summer because I love the beach. "
        "I don't like winter because I don't like cold weather.", 700),
    (M, "My favorite month is April because my birthday is on April tenth. "
        "And you? What's your favorite month? Why?", 300),
]

SCRIPTS["aula7-heshe"] = [(F, "He or she? Listen and choose.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w}. [[slnc 1400]] {w}.", 2400)
    for n, w in zip(["one", "two", "three", "four", "five"], ["she", "he", "he", "she", "she"])]
SCRIPTS["aula7-dictation"] = [(F, "Listen and write the pronoun.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1400]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["They are cats.", "We are friends.", "She is my sister.", "It is blue.", "You are students.", "He is my teacher."])]
SCRIPTS["aula7-photos"] = [
    (F2, "Hi! I'm Emma. Look at my photos!", 700),
    (F2, "This is me. I am from Canada.", 700),
    (F2, "This is my brother, Jack. He is fifteen years old.", 700),
    (F2, "This is my dog, Bob. It is small and very cute.", 700),
    (F2, "These are my friends, Mia and Kate. They are from Brazil.", 700),
    (F2, "This is my mother. She is a nurse.", 700),
    (F2, "And this is my brother and me at school. We are students.", 300),
]
for _p, _list in {"p": ["I", "you", "he", "she", "it", "we", "they"],
                  "s": ["It is a cat.", "They are cats.", "It is cute.", "They are cute.", "It is blue.", "They are colorful."],
                  "f": ["He is my friend.", "She is my teacher.", "We are students.", "You are my friends.", "They are from Brazil."]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula7-say-{_p}{_i}"] = [(F, _t + ("." if _p == "p" else ""), 300)]
SCRIPTS["aula7-reading"] = [
    (F, "My family. By Julia.", 900),
    (F, "Hi! I'm Julia. I'm twenty years old and I'm from Brazil.", 600),
    (F, "This is my mother, Ana. She is a teacher. This is my father, Carlos. He is a doctor.", 700),
    (F, "My brother Leo and I are students. We study English on Saturdays.", 700),
    (F, "This is my cat, Mimi. It is small and white. It is very cute!", 700),
    (F, "My grandparents have two dogs, Rex and Bolt. They are big and brown.", 300),
]

SCRIPTS["aula8-s"] = [(F, "With S or without S? Listen and choose.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w}. [[slnc 1400]] {w}.", 2400)
    for n, w in zip(["one", "two", "three", "four", "five", "six"], ["watches", "go", "studies", "have", "finishes", "take"])]
SCRIPTS["aula8-dictation"] = [(F, "Listen and write the verb.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1600]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["She takes a shower every day.", "They watch TV at night.", "He goes to the gym every day.",
                     "She has breakfast at eight a.m.", "I study English twice a week."])]
SCRIPTS["aula8-mark"] = [
    (F2, "This is my brother, Mark. He has a very busy routine!", 700),
    (F2, "He wakes up at six thirty and takes a shower. Then he has breakfast at seven.", 700),
    (F2, "He starts work at eight. He fixes computers.", 700),
    (F2, "He finishes work at five p.m. After that, he goes to the gym.", 700),
    (F2, "At night, he watches TV with his friends. Finally, he goes to bed at eleven.", 300),
]
for _p, _list in {"v": ["wake up. [[slnc 400]] wakes up", "watch. [[slnc 400]] watches", "go. [[slnc 400]] goes",
                        "do. [[slnc 400]] does", "study. [[slnc 400]] studies", "have. [[slnc 400]] has",
                        "finish. [[slnc 400]] finishes"],
                  "s": ["He wakes up at seven.", "She takes a shower every day.", "He watches TV at night.",
                        "She goes to bed at eleven p.m.", "She studies English twice a week.", "She has breakfast at eight a.m.",
                        "He goes to the gym every day.", "She always does her homework."],
                  "q": ["What time do you wake up?", "What time do you go to bed?", "What do you do in the afternoon?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula8-say-{_p}{_i}"] = [(F, _t + ("." if _p == "v" else ""), 300)]
SCRIPTS["aula8-reading"] = [
    (F, "Laura's day.", 900),
    (F, "This is Laura. She is a nurse and she works at a hospital in Sao Paulo.", 600),
    (F, "First, she wakes up at five thirty a.m. and takes a shower. Then she has breakfast with her husband, Pedro. "
        "She starts work at seven a.m.", 700),
    (F, "After that, she has lunch at the hospital at noon. She finishes work at three p.m.", 700),
    (F, "In the afternoon, she studies English. She goes to the gym at six p.m.", 700),
    (F, "Finally, she watches TV with Pedro and goes to bed at ten p.m.", 700),
    (F, "Pedro fixes cars. He wakes up at seven a.m. and goes to bed at midnight!", 300),
]

SCRIPTS["aula9-jobs"] = [(F, "Listen and choose the job.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w}. [[slnc 1400]] {w}.", 2400)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["lawyer", "musician", "waitress", "firefighter", "vet", "actress"])]
SCRIPTS["aula9-dictation"] = [(F, "Listen and write the job.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I'm a teacher.", "She's a nurse.", "He's a pilot.", "I'm a dentist.", "She's a singer."])]
SCRIPTS["aula9-party"] = [
    (M, "Hi, I'm Tom. Nice to meet you!", 400), (F2, "Nice to meet you, Tom. I'm Sophie.", 400),
    (M, "What do you do, Sophie?", 400),
    (F2, "I'm a flight attendant. I fly to London every week. And you?", 400),
    (M, "I'm an engineer.", 900),
    (M2, "Hello! I'm Ryan.", 400), (M, "Hi, Ryan. What do you do?", 400),
    (M2, "I'm a chef. I work in an Italian restaurant.", 900),
    (F, "Hi, guys! I'm Grace.", 400), (M, "Hi, Grace! What do you do?", 400),
    (F, "I'm a journalist. I work from home.", 400), (M, "Cool!", 300),
]
for _p, _list in {"j": ["doctor", "teacher", "nurse", "lawyer", "engineer", "accountant", "police officer", "musician",
                        "firefighter", "flight attendant", "hairdresser", "receptionist"],
                  "q": ["What do you do?", "I'm a teacher.", "I'm an engineer.", "I'm an accountant.",
                        "She works as a teacher in a school near here.", "He goes to work by car.", "I work for a big company.",
                        "They wear a uniform at work.", "How do you go to work?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula9-say-{_p}{_i}"] = [(F, _t + ("." if _p == "j" else ""), 300)]
SCRIPTS["aula9-reading"] = [
    (M, "My neighbors. By Bruno.", 900),
    (M, "I'm Bruno and I'm a musician. I play the guitar in a band and I work at night.", 700),
    (M, "My neighbor Helen is a pilot. She flies to Europe every month and she has a big house.", 700),
    (M, "Mister Costa is a police officer. He wears a uniform at work and he goes to work by bus.", 700),
    (M, "Daniel and Paula are vets. They have a small clinic near here. Daniel fixes old cars on the weekends.", 700),
    (M, "And Missus Lima? She is a teacher, but now she stays home and studies Italian!", 300),
]

SCRIPTS["aula10-likes"] = [(F, "Listen. Do they like it or not?", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I like sushi.", "He doesn't like bacon.", "We don't like coffee.", "She likes cake.", "They don't like tea."])]
SCRIPTS["aula10-dictation"] = [(F, "Listen and write the food or drink.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w}. [[slnc 1400]] {w}.", 2600)
    for n, w in zip(["one", "two", "three", "four", "five", "six"], ["cheese", "juice", "milk", "soup", "coffee", "salad"])]
SCRIPTS["aula10-picnic"] = [
    (F2, "Leo, let's have a picnic on Saturday!", 400), (M, "Great idea! I love sandwiches.", 400),
    (F2, "Me too! But no cheese, please. I don't like cheese.", 400), (M, "No problem. And to drink? Coffee?", 400),
    (F2, "Coffee for me, yes. And you?", 400), (M, "No, I don't drink coffee. I drink tea.", 400),
    (F2, "OK. And orange juice! I love juice!", 400), (M, "And chocolate?", 400),
    (F2, "Yes, chocolate cake! I love cake.", 400), (M, "Hmm, I don't eat chocolate. But cake is OK!", 300),
]
for _p, _list in {"f": ["chocolate", "cake", "cheese", "ice cream", "soup", "tea", "coffee", "milk", "juice", "vegetables"],
                  "s": ["I like sushi. I don't like soup.", "He likes pizza. He doesn't like salad.",
                        "She likes hot dog. She doesn't like salad.", "I don't go to the movies on Monday.", "We don't have a pet.",
                        "He doesn't live in a flat.", "She doesn't work in an office.", "I listen to music every day."],
                  "q": ["Say the food you like [[slnc 300]] and the food you don't like.",
                        "Make true sentences. [[slnc 400]] Live in an apartment. [[slnc 400]] Cook dinner every day. [[slnc 400]] Play the guitar."]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula10-say-{_p}{_i}"] = [(F, _t + ("." if _p == "f" else ""), 300)]
SCRIPTS["aula10-reading"] = [
    (F, "My roommate and I. By Bia.", 900),
    (F, "I live in a flat in Curitiba with my friend Nina. We are very different!", 700),
    (F, "I work in an office and I drive a car. Nina doesn't drive. She goes to work by bus.", 700),
    (F, "I love coffee, but Nina doesn't drink coffee. She drinks tea and juice.", 700),
    (F, "Nina cooks dinner every day. I don't cook. I do the housework!", 700),
    (F, "She eats vegetables and salad. I don't like salad, I like pizza and hot dogs.", 700),
    (F, "We don't have a pet, but we have a picnic in the park every Sunday.", 300),
]


ROLE = {F: "F", M: "M", F2: "F2", M2: "M2", "SARAH": "SARAH", "MAX": "MAX", "JERRY": "JERRY"}  # macOS voice -> ElevenLabs role in deploy/tts.py
def _breaks(ms):
    """ElevenLabs pause tags (max 3 s each)."""
    out = []
    while ms > 0:
        out.append(f'<break time="{min(ms, 3000) / 1000:.1f}s" />')
        ms -= 3000
    return " " + " ".join(out) + " "


USE_SAY = "--say" in sys.argv  # quick drafts with the macOS voices; default = ElevenLabs (natural voices)

SCRIPTS["aula11-dodoes"] = [(F, "Do or does? Listen and choose.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["Does he like pizza?", "Do you speak English?", "Do they live in Rio?", "Does she drink coffee?",
                     "Does it sleep a lot?"])]
SCRIPTS["aula11-answers"] = [(F, "Listen and write the short answers.", 1200)] + [
    item for n, (q, a) in zip(["one", "two", "three", "four"],
                               [("Do you like cake?", "Yes, I do."), ("Does she drink milk?", "No, she doesn't."),
                                ("Do they speak English?", "Yes, they do."), ("Does he wear glasses?", "No, he doesn't.")])
    for item in [(F, f"Number {n}. [[slnc 500]] {q}", 500), (M, f"{a} [[slnc 1600]] {a}", 2600)]]
SCRIPTS["aula11-classmates"] = [
    (F, "Hi! I'm Emma. Welcome to the class!", 400), (M, "Yes! I'm Jake. Nice to meet you.", 500),
    (F, "Nice to meet you too. Do you live near the school?", 400), (M, "Yes, I do. Five minutes from here.", 500),
    (F, "Cool. Do you work?", 400), (M, "No, I don't. I'm a student. And you? Do you work?", 400),
    (F, "Yes, I do. I work in an office.", 500),
    (M, "Do you like soccer? I play soccer every Saturday.", 400),
    (F, "No, I don't. I play the piano!", 500),
    (M, "Ha ha! OK. Do you like coffee?", 400), (F, "Yes, I do! Let's have a coffee!", 400), (M, "Great idea!", 300),
]
for _p, _list in {"q": ["Do you like sushi?", "Do you like salad?", "Does he like pizza?", "Does she like salad?",
                        "Do they like tea?", "Do you study English?", "Does she wake up at six?"],
                  "a": ["Yes, I do.", "No, I don't.", "Yes, he does.", "No, he doesn't.", "Yes, she does.", "No, they don't."],
                  "y": ["Do you like coffee?", "Do you have a pet?", "Do you speak English?", "Do you wake up early?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula11-say-{_p}{_i}"] = [(F if _p != "a" else M, _t, 300)]
SCRIPTS["aula11-reading"] = [
    (M, "Family quiz. By Leo.", 800),
    (M, "I ask my family some questions. Here are the answers!", 700),
    (M, "Mom, do you like coffee?", 300), (F, "Yes, I do. I drink coffee every morning.", 600),
    (M, "Dad, do you cook?", 300), (M, "No, I don't. But I do the housework!", 600),
    (M, "Ana, do you play the guitar?", 300), (F, "Yes, I do. I play every day.", 600),
    (M, "Mom and Dad, do you speak English?", 300), (F, "Yes, I do.", 300), (M, "No, I don't. I speak Spanish.", 600),
    (M, "And our dog, Toby? Does he sleep on the sofa? Yes, he does! Every night!", 300),
]

SCRIPTS["aula12-howwho"] = [(F, "How or who? Listen and choose.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["How do you go to work?", "Who do you admire?", "Who is your favorite singer?", "How are you?",
                     "How old are you?"])]
SCRIPTS["aula12-dictation"] = [(F, "Listen and write the question word.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1600]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["When do you have English class?", "Why do you wake up early?", "What time do you go to bed?",
                     "How many brothers do you have?", "Which do you prefer, tea or coffee?"])]
SCRIPTS["aula12-interview"] = [
    (M, "Good morning! Today on the radio we talk to Sofia. Sofia, what do you do?", 400),
    (F, "Hi! I'm a nurse. I work at a hospital.", 500),
    (M, "Where do you live?", 300), (F, "I live in Recife.", 500),
    (M, "What time do you start work?", 300), (F, "I start work at seven in the morning.", 500),
    (M, "How do you go to work?", 300), (F, "By bike! The hospital is near my house.", 500),
    (M, "How many children do you have?", 300), (F, "I have two children, a boy and a girl.", 500),
    (M, "Why do you love your job?", 300), (F, "Because I help people every day.", 500),
    (M, "Who do you admire?", 300), (F, "I admire my mother. She is a nurse too!", 500),
    (M, "Last question: which do you prefer, cats or dogs?", 300), (F, "Cats! I have three cats.", 500),
    (M, "Thank you, Sofia!", 300),
]
for _p, _list in {"w": ["what", "where", "when", "who", "why", "which", "how", "what time", "what kind of", "how many", "how often"],
                  "q": ["What time do you have breakfast?", "When do you study English?", "How do you go to work?",
                        "What kind of food do you like?", "Who do you admire?", "Why do you wake up early?",
                        "How many sisters do you have?", "Which do you prefer, cats or dogs?"],
                  "y": ["Where do you live?", "What do you do?", "Why do you study English?", "What kind of music do you like?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula12-say-{_p}{_i}"] = [(F, _t + ("." if _p == "w" else ""), 300)]
SCRIPTS["aula12-reading"] = [
    (F, "Meet Daniel.", 800),
    (F, "Daniel is thirty-two years old. He lives in Porto Alegre with his wife and their cat.", 600),
    (F, "He is an engineer, but he doesn't go to an office: he works from home.", 600),
    (F, "He wakes up at six thirty because he runs in the park before work.", 600),
    (F, "He has two siblings: one sister and one brother.", 600),
    (F, "He loves rock music and Japanese food. He admires his mother, a doctor.", 600),
    (F, "He studies English on Tuesdays and Thursdays because he wants to work in Canada.", 300),
]

SCRIPTS["aula13-verbs"] = [(F, "Listen and choose: play, do or go.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I do karate.", "We go fishing.", "They play hockey.", "I go hiking.", "You do aerobics."])]
SCRIPTS["aula13-dictation"] = [(F, "Listen and write the sport.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w}. [[slnc 1800]] {w}.", 2800)
    for n, w in zip(["one", "two", "three", "four", "five"], ["basketball", "swimming", "yoga", "surfing", "boxing"])]
SCRIPTS["aula13-dialogue"] = [
    (M, "Hi, Laura! Do you practice any sports or activities?", 400),
    (F, "Yes, I do! I do pilates on Tuesdays and Thursdays. And on Sundays, I go cycling with my husband.", 500),
    (F, "And you, Mike? What sports do you practice?", 400),
    (M, "I go to the gym every day. I go swimming on Saturdays, and I play tennis with my brother.", 500),
    (F, "Wow! Does your son practice any sports?", 400),
    (M, "Yes, he does. He does judo after school. What about your daughter? Does she go cycling with you?", 400),
    (F, "No, she doesn't. She plays volleyball at school.", 300),
]
for _p, _list in {"w": ["soccer", "basketball", "volleyball", "tennis", "karate", "yoga", "pilates", "weightlifting",
                        "swimming", "running", "cycling", "climbing"],
                  "v": ["play soccer", "play tennis", "do judo", "do yoga", "go swimming", "go hiking",
                        "Do you practice any sports or activities?", "Does she go cycling in the afternoon?"],
                  "y": ["Do you practice any sports or activities?", "What sports or activities do you practice?",
                        "Do you go to the gym every day?", "What sports does your best friend practice?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula13-say-{_p}{_i}"] = [(F, _t + ("" if _t.endswith("?") else "."), 300)]
SCRIPTS["aula13-reading"] = [
    (F, "A sporty family.", 800),
    (F, "Hi! I'm Carol, and my family loves sports.", 600),
    (F, "My father, Jorge, goes running in the park every morning. On Saturdays, he plays soccer with his friends.", 600),
    (F, "My mother, Helena, does yoga at home and goes swimming on Wednesdays.", 600),
    (F, "My brother, Tiago, plays basketball at school and does karate on Fridays.", 600),
    (F, "And me? I go surfing on the weekend, and I do pilates on Mondays.", 600),
    (F, "We all go hiking together in the summer. It's my favorite day of the year!", 300),
]
SCRIPTS["aula14-adverbs"] = [(F, "Listen and choose the adverb.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I usually get up early.", "She hardly ever goes to bed late.", "We sometimes go to a restaurant.",
                     "They never watch TV.", "He often goes for a walk."])]
SCRIPTS["aula14-dictation"] = [(F, "Listen and write the expression of frequency.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["I go to the dentist twice a year.", "We go to the beach once a month.",
                     "She goes running every other day.", "I go to the hairdresser every two months."])]
SCRIPTS["aula14-survey"] = [
    (M, "Hello! Can I ask you some questions about healthy habits?", 300), (F, "Sure!", 500),
    (M, "What's your name?", 300), (F, "Jenny.", 500),
    (M, "OK, Jenny. How often do you have breakfast?", 300), (F, "Every day. I always have breakfast.", 500),
    (M, "How often do you go to the gym?", 300), (F, "Three times a week: on Mondays, Wednesdays and Fridays.", 500),
    (M, "And how often do you go for a walk?", 300), (F, "Every other day, with my dog.", 500),
    (M, "How often do you eat fast food?", 300), (F, "Hardly ever. Maybe once a month.", 500),
    (M, "Do you drink water every day?", 300), (F, "Yes, I do. Two liters every day!", 500),
    (M, "How often do you go to bed late?", 300), (F, "Sometimes, on the weekend. I usually go to bed at ten.", 500),
    (M, "And how often do you go to the doctor?", 300), (F, "Once a year.", 500),
    (M, "Last question: how often do you watch TV?", 300), (F, "I watch TV twice a week. I prefer books!", 500),
    (M, "Thank you, Jenny!", 300),
]
for _p, _list in {"w": ["always", "often", "usually", "sometimes", "hardly ever", "never", "once a week", "twice a month",
                        "every other day", "How often?"],
                  "v": ["go to the beach", "go for a walk", "go to the hairdresser", "have breakfast", "have a good time",
                        "get up early", "get dressed", "get home late"],
                  "y": ["How often do you go to the gym?", "How often do you watch TV?", "How often do you travel by car?",
                        "How often do you go to the beach?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula14-say-{_p}{_i}"] = [(F, _t + ("" if _t.endswith("?") else "."), 300)]
SCRIPTS["aula14-reading"] = [
    (F, "Grandpa Joe.", 800),
    (F, "My grandfather Joe is seventy-eight years old, and he has a very active life.", 600),
    (F, "He always gets up early, at five thirty, and he has breakfast with my grandmother.", 600),
    (F, "He goes for a walk every other day, and he goes swimming twice a week.", 600),
    (F, "He never watches TV in the morning, but he sometimes watches soccer at night.", 600),
    (F, "He goes to the doctor every three months, and he goes to the hairdresser once a month.", 600),
    (F, "He hardly ever goes to bed late. He says: Early to bed, early to rise!", 300),
]
SCRIPTS["aula15-words"] = [(F, "Country or nationality? Listen and choose.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["France.", "Japanese.", "Germany.", "Italian.", "China."])]
SCRIPTS["aula15-dictation"] = [(F, "Listen and write the nationality.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["He's British.", "We're Brazilian.", "They're Spanish.", "I'm Canadian.", "She's Portuguese."])]
SCRIPTS["aula15-school"] = [
    (F, "Good morning, everybody! Welcome to our English school in London. I'm Emma, your teacher.", 500),
    (F, "What's your name, and where are you from?", 300),
    (M, "Hi! I'm Carlos. I'm from Mexico. I'm Mexican, and I speak Spanish.", 500),
    (F, "Welcome, Carlos! And you?", 300),
    (F, "Hello. My name is Yuki. I'm Japanese. I'm from Tokyo.", 500),
    (F, "Nice to meet you, Yuki. And you? Are you Italian?", 300),
    (M, "No, I'm not. My name is Luca, and I'm Swiss. I'm from Switzerland. I speak Italian and German.", 500),
    (F, "Great! And you? Are you from France?", 300),
    (F, "No, I'm not French. I'm Marie, and I'm from Canada. I speak English and French.", 500),
    (F, "Wonderful! Welcome, everybody!", 300),
]
for _p, _list in {"c": ["Brazil", "the USA", "the UK", "Canada", "Italy", "Japan", "Germany", "France", "Australia", "Switzerland"],
                  "n": ["Brazilian", "American", "British", "Canadian", "Italian", "Japanese", "German", "French", "Australian", "Swiss"],
                  "y": ["Where are you from?", "What nationality are you?", "What language do you speak?", "Are you a teacher?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula15-say-{_p}{_i}"] = [(F, _t.replace("the USA", "the U.S.A.").replace("the UK", "the U.K.")
                                            + ("" if _t.endswith("?") else "."), 300)]
SCRIPTS["aula15-reading"] = [
    (F, "Friends around the world.", 800),
    (F, "Hi! I'm Bruna. I'm Brazilian, and I'm from Salvador. I'm a tour guide.", 600),
    (F, "I have friends from many countries. Kenji is from Japan. He's Japanese, and he speaks Japanese and English.", 600),
    (F, "Anna and Paul are from Germany. They're German, but they live in Switzerland now.", 600),
    (F, "Sophie isn't French. She's Canadian! She's from Montreal, and she speaks English and French.", 600),
    (F, "And Diego? He's from Argentina. He speaks Spanish and a little Portuguese.", 600),
    (F, "We're from different countries, but we're good friends!", 300),
]
SCRIPTS["aula16-pairs"] = [(F, "Listen and choose the word you hear.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I'm hungry.", "The baby is sleepy.", "She's angry.", "I feel good.", "We're sad."])]
SCRIPTS["aula16-dictation"] = [(F, "Listen and write the feeling.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I'm bored.", "She's excited.", "They're thirsty.", "He's scared.", "We're cold."])]
SCRIPTS["aula16-phone"] = [
    (F, "Hello?", 300), (M, "Hi, Lisa! It's Tom. How are you?", 400),
    (F, "Hi, Tom! I'm great, thanks. And you? How do you feel today?", 400),
    (M, "Oh, I'm tired. I work twelve hours today. And I'm very hungry!", 500),
    (F, "Oh no! Have a big dinner, then!", 400),
    (M, "Yes! And you? Why are you so happy?", 400),
    (F, "I have a new job! I start on Monday. I'm very excited!", 400),
    (M, "Wow, congratulations! I'm proud of you!", 400),
    (F, "Thank you! But I'm a little scared about the first day.", 400),
    (M, "Don't worry! You're a great teacher.", 300),
]
for _p, _list in {"w": ["happy", "sad", "scared", "angry", "hungry", "bored", "excited", "tired", "sleepy", "thirsty", "proud", "lonely"],
                  "s": ["I feel happy.", "I'm cold.", "She isn't angry.", "He doesn't feel tired.", "Are you hungry?", "The baby is sleepy."],
                  "y": ["How do you feel today?", "Are you hungry now?", "Are you shy?", "How do you feel on Mondays?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula16-say-{_p}{_i}"] = [(F, _t + ("." if _p == "w" else ""), 300)]
SCRIPTS["aula16-reading"] = [
    (F, "A long day.", 800),
    (F, "I'm Rafael, and today is a long day.", 600),
    (F, "In the morning, I'm sleepy because I go to bed late every night.", 600),
    (F, "At ten o'clock, I have a meeting with my boss. I'm a little scared, but the meeting is good. He's happy with my work, and I feel proud!", 600),
    (F, "At lunch, I'm very hungry. I eat a big sandwich.", 600),
    (F, "In the afternoon, I'm bored. My work isn't interesting on Fridays.", 600),
    (F, "At seven p.m., I get home. I'm tired, but I'm not sad: tomorrow is Saturday, and I go to the beach with my friends. I'm excited!", 300),
]
SCRIPTS["aula17-words"] = [(F, "Listen and choose the word you hear.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["He has a beard.", "She has curly hair.", "He is tall.", "I have hazel eyes.", "She is thin."])]
SCRIPTS["aula17-dictation"] = [(F, "Listen and complete.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 2000]] {w}", 3000)
    for n, w in zip(["one", "two", "three", "four"],
                    ["My brother has straight black hair.", "My grandmother has white hair and wrinkles.",
                     "Ana has freckles and green eyes.", "Mr. Silva is bald."])]
SCRIPTS["aula17-airport"] = [
    (F, "Hi, Uncle Beto! I'm at the airport, but I don't remember Leo. What does he look like?", 400),
    (M, "Well, he's tall and thin.", 400), (F, "Is he old now?", 300),
    (M, "No, he isn't! He's young. He's twenty-two.", 400),
    (F, "OK. Does he have long hair?", 300),
    (M, "No, he doesn't. He has short curly black hair. And he has a beard now.", 400),
    (F, "A beard! And a mustache?", 300), (M, "No, only a beard.", 400),
    (F, "What color are his eyes?", 300), (M, "Green, like my eyes.", 400),
    (F, "Oh, I see him! Tall, thin, curly black hair, a beard... Leo! Over here!", 300),
]
for _p, _list in {"w": ["tall", "short", "thin", "middle-aged", "bald", "straight", "wavy", "curly", "blond", "hazel eyes", "beard", "freckles"],
                  "s": ["She has wavy brown hair.", "He is tall and thin.", "My mother has green eyes.", "Is she old? No, she isn't.",
                        "Does he have a beard? Yes, he does."],
                  "y": ["Are you tall?", "What hair do you have?", "What color are your eyes?", "Describe your best friend."]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula17-say-{_p}{_i}"] = [(F, _t + ("." if _p == "w" else ""), 300)]
SCRIPTS["aula17-reading"] = [
    (F, "A family photo.", 800),
    (F, "This is a photo of my family on my birthday.", 600),
    (F, "My father is tall and a little chubby. He's middle-aged, and he has a grey beard and a mustache.", 600),
    (F, "My mother is short and slim. She has long wavy brown hair and hazel eyes.", 600),
    (F, "My grandfather is old, and he's bald. He has a lot of wrinkles, but he's always happy!", 600),
    (F, "My brother, Pedro, is young. He's eleven. He has short curly red hair and freckles.", 600),
    (F, "And me? I'm medium height. I have shoulder-length straight black hair and brown eyes.", 300),
]
SCRIPTS["aula18-words"] = [(F, "Listen and choose the word you hear.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["She's very nice.", "These are my parents.", "This is my aunt.", "I have two children.", "He's my cousin."])]
SCRIPTS["aula18-dictation"] = [(F, "Listen and write the family member.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["This is my grandmother.", "These are my grandparents.", "This is my nephew.", "These are my siblings.",
                     "This is my daughter."])]
SCRIPTS["aula18-photos"] = [
    (M, "Mia, are these your family photos?", 300), (F, "Yes, they are! Look. These are my grandparents.", 400),
    (M, "Where do they live?", 300), (F, "They live in Portugal. My grandfather is Portuguese.", 500),
    (M, "And who is this?", 300), (F, "This is my aunt Carla. She's my mother's sister.", 400),
    (M, "Does she have children?", 300), (F, "Yes, she does. She has two children, my cousins Bia and Rafa.", 500),
    (M, "And this little boy?", 300), (F, "That's Davi, my nephew. He's my brother's son. And I'm his godmother!", 500),
    (M, "How many siblings do you have?", 300), (F, "Two. One brother and one sister.", 300),
]
for _p, _list in {"w": ["daughter", "son", "parents", "siblings", "child", "children", "grandparents", "aunt", "uncle", "niece",
                        "nephew", "cousin", "mother-in-law"],
                  "s": ["This is my father.", "These are my sisters.", "I have one sibling.", "Marta is Lucas's mother.",
                        "My cousins live in Recife."],
                  "y": ["Do you have siblings?", "Do you have children?", "Where do your parents live?",
                        "How many cousins do you have?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula18-say-{_p}{_i}"] = [(F, _t + ("." if _p == "w" else ""), 300)]
SCRIPTS["aula18-reading"] = [
    (F, "The Costa family.", 800),
    (F, "Hi! I'm Lucas Costa, and I'm fourteen. I live in Campinas with my parents and my sister, Nina.", 600),
    (F, "My mother's name is Marta. She's a nurse. My father, Rui, is a teacher.", 600),
    (F, "My grandparents, Lúcia and Jorge, live on a farm. They have four grandchildren: me, Nina and our two cousins.", 600),
    (F, "Our cousins are Gabi and Tiago. They're my uncle Beto's children. Beto is my father's brother.", 600),
    (F, "My aunt Sônia is Beto's wife. She's very nice, and she's my godmother!", 600),
    (F, "We all have lunch at the farm on Sundays. I love my family!", 300),
]
SCRIPTS["aula19-words"] = [(F, "Singular or plural? Listen and choose.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"], ["a watch.", "boxes.", "a woman.", "men.", "a child."])]
SCRIPTS["aula19-dictation"] = [(F, "Listen and write the object.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["a wallet.", "an umbrella.", "sunglasses.", "a charger.", "credit cards."])]
SCRIPTS["aula19-bag"] = [
    (M, "Olivia, your bag is so big! What do you have in it?", 300),
    (F, "Ha ha! Let's see. I have my wallet, my cell phone and a phone charger.", 400),
    (M, "OK. And?", 300), (F, "I have two lipsticks, a comb and my sunglasses.", 400),
    (M, "Two lipsticks?", 300), (F, "Yes! A red lipstick and a pink lipstick.", 400),
    (M, "Do you have your keys?", 300), (F, "Yes, I do. Three keys on a key ring: my house, my car and my office.", 400),
    (M, "And your passport?", 300), (F, "No, my passport is at home.", 400),
    (M, "What's this?", 300), (F, "It's an umbrella. It's a rainy city!", 400),
    (M, "And these are... pens?", 300), (F, "Yes, five pens. I'm a teacher!", 300),
]
for _p, _list in {"w": ["a key", "a key ring", "sunglasses", "a wallet", "a charger", "an umbrella", "a passport", "a toothbrush",
                        "a comb", "a backpack"],
                  "p": ["a watch, watches", "a city, cities", "a man, men", "a woman, women", "a child, children", "a foot, feet",
                        "a tooth, teeth", "a person, people"],
                  "y": ["What do you have in your bag?", "How many keys do you have?", "Do you have an umbrella?",
                        "What do you have on your desk?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula19-say-{_p}{_i}"] = [(F, _t + ("" if _p == "y" else "."), 300)]
SCRIPTS["aula19-reading"] = [
    (F, "My backpack.", 800),
    (F, "I'm Leo, and I'm a university student. I always have my backpack with me.", 600),
    (F, "In my backpack, I have a notebook, three pens, a pencil and an eraser.", 600),
    (F, "I also have a tablet and a charger, because I study on the bus.", 600),
    (F, "I have my wallet with two credit cards, and I have my keys on a key ring.", 600),
    (F, "I usually have an apple or a banana for lunch.", 600),
    (F, "And on rainy days, I have an umbrella too. My backpack is very heavy!", 300),
]
SCRIPTS["aula20-rooms"] = [(F, "Bedroom or bathroom? Listen and choose.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four"],
                    ["The mirror is in the bathroom.", "My bed is in the bedroom.", "It's in my bedroom.",
                     "The bathroom is small."])]
SCRIPTS["aula20-dictation"] = [(F, "Listen and write the word.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["the kitchen.", "the mirror.", "the fridge.", "the window.", "the pillows."])]
SCRIPTS["aula20-apartment"] = [
    (M, "Good afternoon, Ana! Welcome. This is the apartment.", 400), (F, "Hello, Mr. Lopes! Oh, it's nice!", 400),
    (M, "This is the living room. It has a sofa and an armchair.", 400), (F, "How many bedrooms does it have?", 300),
    (M, "Two bedrooms. And this is the kitchen. It has a stove, an oven and a new fridge.", 400),
    (F, "Does it have a dishwasher?", 300), (M, "No, it doesn't. Sorry!", 400),
    (F, "And the bathroom? Does it have a bathtub?", 300), (M, "No, it has a shower.", 400),
    (F, "Does it have a garage?", 300), (M, "No, it doesn't. But look: a balcony!", 400),
    (F, "Wow! I love the balcony!", 300),
]
for _p, _list in {"r": ["living room", "bedroom", "bathroom", "dining room", "kitchen", "garage", "office", "balcony"],
                  "t": ["sofa", "armchair", "rug", "stove", "fridge", "oven", "wardrobe", "pillows", "mirror", "faucet"],
                  "y": ["Do you live in a house or in an apartment?", "How many bedrooms does your home have?",
                        "What's your favorite room?", "Do you have a balcony?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula20-say-{_p}{_i}"] = [(F, _t + ("" if _p == "y" else "."), 300)]
SCRIPTS["aula20-reading"] = [
    (F, "My new apartment.", 800),
    (F, "Hi, Carol! I have a new apartment in Florianópolis! It's small, but it's very nice.", 600),
    (F, "It has a living room, a kitchen, one bedroom, one bathroom and a balcony.", 600),
    (F, "In the living room, I have a blue sofa, an armchair and a lot of plants. I don't have a TV!", 600),
    (F, "The kitchen is small. It has a stove, a fridge and a microwave, but it doesn't have an oven.", 600),
    (F, "My bedroom has a big window, a bed, a wardrobe and a bedside table with a lamp.", 600),
    (F, "The bathroom has a shower and a big mirror.", 600),
    (F, "My favorite room? The balcony! I have breakfast there every morning, and I see the sea.", 300),
]
SCRIPTS["aula21-forms"] = [(F, "Listen and choose what you hear.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["There's a clock on the wall.", "There are two beds.", "There isn't a garage.",
                     "Are there pictures on the wall?", "Is there a TV in the bedroom?"])]
SCRIPTS["aula21-dictation"] = [(F, "Listen and complete.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["There is a rug in the living room.", "There are three boxes in the garage.",
                     "There isn't a microwave in the kitchen.", "There are many plants on the balcony."])]
SCRIPTS["aula21-hotel"] = [
    (F, "Good morning, Sunset Hotel!", 300), (M, "Hi! I want a room for the weekend. Is there a TV in the room?", 400),
    (F, "Yes, there is. There's a TV and a small fridge.", 400), (M, "Great. How many beds are there?", 300),
    (F, "There are two beds.", 400), (M, "Is there a bathtub in the bathroom?", 300),
    (F, "No, there isn't. There's a shower.", 400), (M, "OK. Is there a balcony?", 300),
    (F, "Yes, there is. There are two chairs and a small table on the balcony.", 400),
    (M, "And is there a restaurant in the hotel?", 300),
    (F, "Yes, there is. And there's a pool in the garden.", 400), (M, "Perfect! Thank you!", 300),
]
for _p, _list in {"s": ["There's a chair in the bedroom.", "There's a TV in the living room.", "There's a pillow on the bed.",
                        "There are four pillows on the bed.", "There are two chairs in the office.",
                        "There isn't a sofa in the living room."],
                  "q": ["Is there a cushion? Yes, there is.", "Is there a TV in the bedroom? No, there isn't.",
                        "Are there pictures on the wall? Yes, there are.", "Is there homework?"],
                  "y": ["Is there a TV in your bedroom?", "How many chairs are there in your kitchen?",
                        "Are there plants in your home?", "What is there in your living room?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula21-say-{_p}{_i}"] = [(F, _t, 300)]
SCRIPTS["aula21-reading"] = [
    (F, "Beach house for rent, in Ubatuba.", 800),
    (F, "This beautiful beach house is perfect for families!", 600),
    (F, "There are three bedrooms and two bathrooms. In the main bedroom, there's a big bed and a balcony.", 600),
    (F, "In the living room, there's a big sofa, two armchairs and a TV.", 600),
    (F, "There's a kitchen with a stove, a big fridge and a microwave. There isn't a dishwasher.", 600),
    (F, "There are four bikes in the garage, and there's a small pool in the garden.", 600),
    (F, "Are there restaurants near the house? Yes, there are! And the beach is only five minutes from the house.", 300),
]
SCRIPTS["aula22-preps"] = [(F, "Listen and choose the preposition.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["The ball is under the box.", "The cat is behind the sofa.", "The lamp is next to the bed.",
                     "The bank is across from the park.", "The picture is above the sofa."])]
SCRIPTS["aula22-dictation"] = [(F, "Listen and complete.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["My phone is in my bag.", "The keys are on the table.", "The dog is between the chairs.",
                     "The car is in front of the garage."])]
SCRIPTS["aula22-where"] = [
    (M, "Mom! I'm late for school! Where are my shoes?", 300), (F, "Calm down, Ben. Your shoes are under the bed.", 400),
    (M, "OK! And where is my backpack?", 300), (F, "It's behind the door.", 400),
    (M, "Thanks! And my phone? Where is my phone?", 300), (F, "Ben... it's in your pocket!", 400),
    (M, "Oh, yes! Ha ha. And my keys?", 300), (F, "They're on the kitchen table, next to your sandwich.", 400),
    (M, "Thank you, Mom! Bye!", 300), (F, "Bye! The bus stop is across from the bakery. Run!", 300),
]
for _p, _list in {"w": ["in", "on", "under", "between", "next to", "behind", "in front of", "across from", "above", "over"],
                  "s": ["The cat is on the sofa.", "The cat is under the chair.", "The cat is between the dogs.",
                        "The cat is next to the clock.", "The cat is behind the wall.", "The cat is in front of the computer.",
                        "Where is the dog? The dog is on the bed."],
                  "y": ["Where is your phone now?", "Where is your TV?", "Where are your keys?", "What is next to your bed?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula22-say-{_p}{_i}"] = [(F, _t + ("." if _p == "w" else ""), 300)]
SCRIPTS["aula22-reading"] = [
    (F, "My neighborhood.", 800),
    (F, "I live in a small apartment on Flores Street. I love my neighborhood!", 600),
    (F, "There's a bakery next to my building. I buy bread there every morning.", 600),
    (F, "Across from my building, there's a big park with a lake. There are many trees in the park.", 600),
    (F, "The supermarket is between the bank and the pharmacy.", 600),
    (F, "My gym is behind the supermarket, and there's a bus stop in front of the gym.", 600),
    (F, "And my favorite place? A small Japanese restaurant over the bakery, on the second floor!", 300),
]
SCRIPTS["aula23-verbs"] = [(F, "Listen and choose the verb you hear.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["He's sitting.", "They're shopping.", "I'm talking.", "She's riding a bike.", "We're listening to music."])]
SCRIPTS["aula23-dictation"] = [(F, "Listen and write the verb.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["She's swimming.", "They're dancing.", "He's driving.", "I'm studying.", "We're watching TV."])]
SCRIPTS["aula23-call"] = [
    (M, "Hello?", 300), (F, "Hi, Dan! It's me. I'm still at work. What are you doing?", 400),
    (M, "I'm cooking dinner. I'm making pasta!", 400), (F, "Great! And the kids? What is Sophie doing?", 300),
    (M, "She's in her bedroom. She's studying for her test, and she's listening to music.", 400),
    (F, "And Max?", 300), (M, "Max is playing video games in the living room, of course!", 400),
    (F, "Ha ha. And the dog?", 300), (M, "The dog is sleeping on the sofa.", 400),
    (F, "OK. I'm working late today. See you at nine!", 300), (M, "See you! Love you!", 300),
]
for _p, _list in {"w": ["cook, cooking", "watch, watching", "read, reading", "talk, talking", "listen, listening", "dance, dancing",
                        "drive, driving", "swim, swimming", "sit, sitting", "shop, shopping"],
                  "s": ["What is he doing? He's cooking.", "She's watching TV.", "They're riding a bike.", "He's taking a shower.",
                        "I'm wearing a uniform.", "My best friend is watching TV."],
                  "y": ["What are you doing now?", "What are you wearing today?", "What is your family doing now?",
                        "Are you sitting or standing?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula23-say-{_p}{_i}"] = [(F, _t + ("." if _p == "w" else ""), 300)]
SCRIPTS["aula23-reading"] = [
    (F, "A postcard from Rio.", 800), (F, "Dear Grandma,", 500),
    (F, "I'm writing this postcard on the beach in Copacabana! It's a beautiful day, and it's very hot.", 600),
    (F, "Right now, Dad is swimming in the sea, and Mom is reading a book under an umbrella.", 600),
    (F, "My brother Jack is playing volleyball with some Brazilian boys. He's having a great time!", 600),
    (F, "I'm sitting on the sand, and I'm drinking coconut water. It's delicious!", 600),
    (F, "People here are very friendly. A man is selling ice cream next to me, and some girls are dancing.", 600),
    (F, "Love, Emma.", 300),
]
SCRIPTS["aula24-forms"] = [(F, "Affirmative or negative? Listen and choose.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["She isn't cooking.", "They're running.", "I'm not sleeping.", "We aren't watching TV.", "He's driving."])]
SCRIPTS["aula24-dictation"] = [(F, "Listen and complete.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 2000]] {w}", 3000)
    for n, w in zip(["one", "two", "three"],
                    ["They aren't eating. They're cooking.", "He isn't working. He's sleeping.",
                     "I'm not studying. I'm reading."])]
SCRIPTS["aula24-babysitter"] = [
    (M, "Hello?", 300), (F, "Hi, Ryan! It's Clara. Is everything OK? Are the children sleeping?", 400),
    (M, "Hi, Clara! Everything is fine. No, they aren't sleeping. Mia is drawing in her bedroom.", 400),
    (F, "And Leo? Is he doing his homework?", 300),
    (M, "No, he isn't. He's playing soccer in the garden with his friend.", 400),
    (F, "Oh, Leo! And the baby? Is she crying?", 300),
    (M, "No, she isn't crying. She's sleeping.", 400), (F, "Great! Are they watching TV?", 300),
    (M, "No, they aren't. And I'm cooking dinner now.", 400), (F, "Thank you, Ryan! See you at ten.", 300),
]
for _p, _list in {"w": ["I'm not", "you aren't", "he isn't", "she isn't", "we aren't", "they aren't"],
                  "s": ["He's sleeping. He isn't working.", "They're cooking. They aren't eating.",
                        "They aren't running. They're riding a bike.", "She isn't walking. She's driving.",
                        "I'm not watching TV. I'm studying."],
                  "y": ["Are you sleeping now?", "Are you watching TV?", "Are you working right now?",
                        "Is your best friend studying now?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula24-say-{_p}{_i}"] = [(F, _t + ("." if _p == "w" else ""), 300)]
SCRIPTS["aula24-reading"] = [
    (F, "A lazy Sunday.", 800),
    (F, "Hi, Rafa! Today is Sunday, and nobody in my family is working!", 600),
    (F, "My father isn't reading the newspaper today. He's sleeping on the sofa.", 600),
    (F, "My mother isn't cooking. We're ordering pizza for lunch!", 600),
    (F, "My sister isn't studying for her test. She's talking to her boyfriend on the phone.", 600),
    (F, "And me? I'm not doing my homework. I'm writing to you and listening to music.", 600),
    (F, "It's raining, so we aren't going to the beach. But it's a good day!", 300),
]
SCRIPTS["aula25-questions"] = [(F, "Listen and choose the question you hear.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["Are they working?", "What is she eating?", "Why is he crying?", "Are you listening?", "Where are you going?"])]
SCRIPTS["aula25-dictation"] = [(F, "Listen and complete the questions.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["Are you studying?", "What is he doing?", "How are you feeling?", "Am I speaking too fast?"])]
SCRIPTS["aula25-call"] = [
    (F, "Hi, Pedro! Wow, where are you? Are you at work?", 300),
    (M, "Hi, Nina! No, I'm not. I'm at the airport!", 400), (F, "The airport! Where are you going?", 300),
    (M, "I'm going to London. My sister is studying there, and I'm visiting her.", 400),
    (F, "That's great! Are you traveling for work too?", 300), (M, "No, I'm not. It's a vacation!", 400),
    (M, "And you? What are you doing?", 300), (F, "I'm at home. I'm eating sushi and watching a movie.", 400),
    (F, "How are you feeling?", 300), (M, "I'm very excited, but a little tired. It's five a.m.!", 300),
]
for _p, _list in {"q": ["Is he cooking?", "Are they working?", "Is she feeling OK?", "Am I speaking too fast?",
                        "Are they eating sushi? No, they aren't."],
                  "w": ["What is she eating?", "Why is he crying?", "How is she feeling?", "Where are you going?",
                        "What are you doing?"],
                  "y": ["What are you doing?", "How are you feeling today?", "Are you wearing a uniform?",
                        "What is your best friend doing now?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula25-say-{_p}{_i}"] = [(F, _t, 300)]
SCRIPTS["aula25-reading"] = [
    (F, "Hi, Bia! What are you doing? Are you studying?", 500), (F, "Hi, Mom! No, I'm not. I'm at the mall with Carol.", 500),
    (F, "The mall? Why are you shopping on a Tuesday?", 500),
    (F, "Because it's Carol's birthday on Friday! We're buying a present for her mother.", 500),
    (F, "Oh, OK. Is Dad driving you home?", 500), (F, "No, he isn't. He's working late. We're taking the bus.", 500),
    (F, "And how are you feeling? Is your head OK now?", 500), (F, "Yes, I'm feeling great, thanks! See you at dinner!", 300),
]
SCRIPTS["aula26-routine"] = [(F, "Routine or now? Listen and choose.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I work in an office.", "I'm studying right now.", "She's cooking.", "He plays tennis on Fridays.",
                     "We usually have lunch at noon."])]
SCRIPTS["aula26-dictation"] = [(F, "Listen and complete.", 1200)] + [
    (F, f"Number {n}. [[slnc 500]] {w} [[slnc 2000]] {w}", 3000)
    for n, w in zip(["one", "two", "three"],
                    ["He cooks very well, but now he's sleeping.", "They play soccer on Saturdays. Today they're playing tennis.",
                     "What does she do? What is she doing?"])]
SCRIPTS["aula26-chef"] = [
    (F, "Welcome to the show, Chef Lucas! What do you do, exactly?", 300),
    (M, "Hi! I'm a chef. I have an Italian restaurant. I love Italian food!", 400),
    (F, "What time do you usually start work?", 300), (M, "I usually start at ten a.m., and I finish at eleven p.m.", 400),
    (F, "Wow! And today? Are you working?", 300), (M, "No, I'm not! Today is Monday. I don't work on Mondays.", 400),
    (F, "So what are you doing today?", 300), (M, "Right now, I'm doing jiu-jitsu at the gym. I do jiu-jitsu twice a week.", 400),
    (F, "And who is cooking at the restaurant today?", 300), (M, "My sister! She's a chef too.", 300),
]
for _p, _list in {"s": ["I go to the park on Sundays. I'm watching TV now.",
                        "They play basketball twice a week, but now they're playing tennis.",
                        "He takes a shower every day. He's having a coffee now.",
                        "What does he do? He's a chef.", "What is he doing? He's doing jiu-jitsu."],
                  "q": ["Does she have a cat? Yes, she does.", "Is she reading a book? No, she isn't.",
                        "How often do you watch TV?", "What are you doing right now?"],
                  "y": ["What do you do?", "What are you doing now?", "What do you usually do on Saturdays?",
                        "What is your family doing now?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"aula26-say-{_p}{_i}"] = [(F, _t, 300)]
SCRIPTS["aula26-reading"] = [
    (F, "A nurse on vacation.", 800),
    (F, "Helena is a nurse. She works at a big hospital in São Paulo.", 600),
    (F, "She usually wakes up at five a.m., and she takes the subway to work. She works twelve hours a day, and she hardly ever has lunch at home.", 600),
    (F, "But this week is different: Helena is on vacation!", 600),
    (F, "Right now, she isn't working. She's sitting on the beach in Bahia, and she's reading a book.", 600),
    (F, "Her husband is swimming in the sea, and her children are playing volleyball.", 600),
    (F, "Helena doesn't usually have time to relax, so she's very happy today!", 300),
]
SCRIPTS["b2-aula1-cancant"] = [(FS, "Can or can't? Listen and choose.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["She can cook.", "I can't swim.", "He can drive.", "They can't dance.", "We can speak English.",
                     "My father can't sing."])]
SCRIPTS["b2-aula1-dictation"] = [(FS, "Listen and write the verb.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["She can dance.", "Birds can fly.", "I can't sing.", "Can you run fast?", "He can speak French."])]
SCRIPTS["b2-aula1-interview"] = [
    (FS, "Hello, Ben! Welcome. So, you want a job at our summer camp. Can you swim?", 400),
    (MJ, "Yes, I can. I swim every morning.", 400), (FS, "Great. Can you drive? We have a camp bus.", 400),
    (MJ, "No, I can't. Sorry! I don't have a driver's license.", 400), (FS, "That's OK. What languages can you speak?", 400),
    (MJ, "I can speak English and Spanish.", 400), (FS, "Can you cook?", 300),
    (MJ, "Well... I can make sandwiches!", 400), (FS, "Ha ha. And music? Can you sing or play an instrument?", 400),
    (MJ, "Yes! I can sing, and I can play the guitar. The kids love it!", 400),
    (FS, "Perfect! You can start on Monday!", 300),
]
for _p, _list in {"s": ["I can swim.", "I can't swim.", "She can dance.", "She can't cook.", "They can dance.", "They can't dance.",
                        "We can speak English."],
                  "q": ["Can you swim? Yes, I can.", "Can she cook? No, she can't.", "Can he drive? Yes, he can.",
                        "What can you do?"],
                  "y": ["Can you swim?", "Can you cook?", "Can you drive?", "What can you do very well?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula1-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b2-aula1-reading"] = [
    (FS, "The school talent show.", 800),
    (FS, "Every year, our school has a talent show on the last Friday of June.", 600),
    (FS, "This year, Lucas is singing a Brazilian song. He can sing very well, but he can't dance!", 600),
    (FS, "Mia and her sister can dance ballet. They practice three times a week.", 600),
    (FS, "Tom is only seven, but he can play the piano. His teacher is very proud of him.", 600),
    (FS, "And our English teacher, Mrs. Carter? She can speak four languages: English, Spanish, French and Italian.", 600),
    (FS, "And me? I can't sing, and I can't dance... but I can take great photos!", 300),
]
SCRIPTS["b2-aula2-forms"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["She was happy.", "They weren't at school.", "We were tired.", "There were some people at the door.",
                     "He wasn't at work."])]
SCRIPTS["b2-aula2-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["You were at school in the morning.", "She wasn't very happy last night.", "Were they at home?",
                     "There was a person at the door."])]
SCRIPTS["b2-aula2-party"] = [
    (MJ, "Hello?", 300), (FS, "Hi, Sam! It's Kate. How was the party last night?", 400),
    (MJ, "Kate! It was great! But where were you?", 400), (FS, "I was at home. I was sick, with a bad cold.", 400),
    (MJ, "Oh, no! Are you OK now?", 300), (FS, "Yes, I'm better, thanks. So, where was the party?", 400),
    (MJ, "It was at Mark's house. There were about thirty people!", 400), (FS, "Wow! Was the music good?", 300),
    (MJ, "Yes, it was. The music was great, and there was a lot of food. But there wasn't a cake!", 400),
    (FS, "Ha ha. And were you tired this morning?", 300), (MJ, "Yes, I was. Very tired!", 300),
]
for _p, _list in {"s": ["I was at home yesterday.", "You were at school in the morning.", "She was very happy last night.",
                        "I wasn't at home yesterday.", "They weren't at school.", "There was a person at the door.",
                        "There were some people at the door."],
                  "q": ["Was she happy? Yes, she was.", "Were they at home? No, they weren't.", "Was there a mirror? Yes, there was.",
                        "Were there plants? Yes, there were."],
                  "y": ["Where were you yesterday at 8 p.m.?", "Were you tired last night?",
                        "Was there a TV in your bedroom when you were a child?", "Where were you last Sunday?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula2-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b2-aula2-reading"] = [
    (FS, "Grandma's old house.", 800),
    (FS, "When I was a child, my favorite place was my grandmother's house in Minas Gerais.", 600),
    (FS, "It was a big old house. There were five bedrooms and a very big kitchen.", 600),
    (FS, "In the kitchen, there was an old stove, and there were always cakes on the table!", 600),
    (FS, "There wasn't a TV in the living room, but there were a lot of books and an old radio.", 600),
    (FS, "In the garden, there were many trees and some chickens.", 600),
    (FS, "My cousins and I were very happy there. Grandma's house was the best place in the world!", 300),
]
PAST_READ = '<phoneme alphabet="cmu-arpabet" ph="R EH1 D">read</phoneme>'  # past of read sounds "red"
SCRIPTS["b2-aula4-presentpast"] = [(FS, "Present or past? Listen and choose.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I worked at home.", "They go to the beach.", "She cooked dinner.", "We had lunch together.",
                     "He buys a new car."])]
SCRIPTS["b2-aula4-daniel"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 2000]] {w}", 3000)
    for n, w in zip(["one", "two", "three", "four", "five", "six", "seven"],
                    ["Daniel woke up at seven a.m. yesterday.", "He had breakfast with his wife.", "After that, he went to the gym.",
                     "He started work at one p.m.", "He finished work at seven p.m.",
                     "They had dinner together and watched a movie.", "They went to bed at eleven p.m."])]
SCRIPTS["b2-aula4-trip"] = [
    (MJ, "Hi, Julia! Welcome back! How was Italy?", 300),
    (FS, "Hi, Pedro! It was amazing! I went there last month with my sister.", 400),
    (MJ, "Cool! Where were you?", 300),
    (FS, "First, we were in Rome. We visited the Colosseum, and we walked a lot!", 400),
    (MJ, "And the food?", 300), (FS, "Oh, I ate pizza and ice cream every day!", 400),
    (MJ, "Ha ha. And after Rome?", 300),
    (FS, "We traveled to Florence by train. And guess what? I met an old friend from school there!", 400),
    (MJ, "Wow! And shopping?", 300), (FS, "I bought a nice bag. Only one!", 400),
    (MJ, "Ha ha. I'm happy you enjoyed the trip!", 300),
]
for _p, _list in {"v": ["cook, cooked", "watch, watched", "start, started", "finish, finished", "walk, walked", "work, worked",
                        "go, went", "eat, ate", "have, had", "wake up, woke up", "buy, bought", "read, read"],
                  "s": ["I went to the supermarket on Saturday.", "I watched TV.", "I had lunch with my family on Sunday.",
                        "Last Sunday, I went to the park and read a book.",
                        "I saw beautiful places on my trip to Italy last month."],
                  "y": ["Tell me three things you did last weekend.", "Tell me what you had for breakfast today.",
                        "Tell me what time you woke up today."]}.items():
    for _i, _t in enumerate(_list, 1):
        _say = _t.replace("read, read", "read, " + PAST_READ).replace("park and read", "park and " + PAST_READ)
        SCRIPTS[f"b2-aula4-say-{_p}{_i}"] = [(FS, _say + ("." if _p == "v" else ""), 300)]
SCRIPTS["b2-aula4-reading"] = [
    (FS, "A weekend in Gramado.", 800),
    (FS, "Last weekend, my husband and I went to Gramado. We traveled by car on Friday night.", 600),
    (FS, "On Saturday, we woke up early and had a big breakfast at the hotel.", 600),
    (FS, "Then we walked around the city center and visited a chocolate factory. I bought a lot of chocolate for my kids!", 600),
    (FS, "In the afternoon, it rained, so we stayed at the hotel and <phoneme alphabet=\"cmu-arpabet\" ph=\"R EH1 D\">read</phoneme> our books.", 600),
    (FS, "At night, we had dinner at a small Italian restaurant, and we met a very nice couple from Argentina.", 600),
    (FS, "On Sunday, we drove back home. We loved the trip!", 300),
]
SCRIPTS["b2-aula5-sounds"] = [(FS, "Listen and choose the sound.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w}. [[slnc 1500]] {w}.", 2600)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["watched", "started", "listened", "stayed", "kissed", "needed"])]
SCRIPTS["b2-aula5-presentpast"] = [(FS, "Present or past? Listen.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I watched TV.", "We play soccer.", "They cleaned the house.", "I love this song.", "She danced at the party."])]
SCRIPTS["b2-aula5-story"] = [
    (MJ, "Last year, I traveled to Chile with my brother.", 500),
    (MJ, "I visited Santiago and the mountains. It was beautiful!", 500),
    (MJ, "We walked a lot every day, and we tried a lot of Chilean food.", 500),
    (MJ, "One day, it rained all afternoon, so we stayed at the hotel and watched movies.", 500),
    (MJ, "I loved the trip, and I decided to go back next year!", 300),
]
for _p, _list in {"id": ["wanted", "visited", "started", "needed", "ended", "decided"],
                  "t": ["watch, watched", "cook, cooked", "laugh, laughed", "kiss, kissed", "help, helped", "dance, danced"],
                  "d": ["play, played", "call, called", "love, loved", "clean, cleaned", "use, used", "travel, traveled"],
                  "s": ["I traveled to Chile last year.", "She danced and laughed all night.", "We visited my grandmother on Sunday.",
                        "They cleaned the house and cooked dinner."]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula5-say-{_p}{_i}"] = [(FS, _t + ("" if _p == "s" else "."), 300)]
SCRIPTS["b2-aula5-reading"] = [
    (FS, "A busy Saturday.", 800),
    (FS, "Last Saturday was a busy day! I woke up at seven and cleaned the whole house.", 600),
    (FS, "Then I cooked lunch for my parents. They visited me at noon, and we talked for hours.", 600),
    (FS, "In the afternoon, my sister called me. She needed help with her English homework, so I helped her.", 600),
    (FS, "At night, my friends and I danced at a party. We laughed a lot!", 600),
    (FS, "When I arrived home, I watched a movie and slept on the sofa.", 300),
]
SCRIPTS["b2-aula6-forms"] = [(FS, "Affirmative or negative? Listen and choose.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["She didn't go to work.", "We watched a movie.", "They didn't eat pizza.", "He bought a car.",
                     "I didn't sleep well."])]
SCRIPTS["b2-aula6-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["She didn't see her friends last weekend.", "They didn't go to the beach on Saturday.",
                     "He didn't do his homework.", "We didn't have breakfast today."])]
SCRIPTS["b2-aula6-lucas"] = [
    (FS, "Hi, Lucas! How was school today?", 300), (MJ, "Hi, Mom. It was OK.", 400),
    (FS, "Here's your lunch box. It's full! You didn't eat your lunch?", 400),
    (MJ, "No, I didn't eat it. I didn't like the food. Sorry!", 400),
    (FS, "Oh, Lucas. And your homework?", 300),
    (MJ, "I didn't do it. I played soccer with my friends after school, and I didn't have time.", 400),
    (FS, "Hmm. And where's your jacket?", 300),
    (MJ, "Oh no! I forgot it at school. I didn't see my jacket after the game.", 400),
    (FS, "Lucas! Do your homework now, please!", 300),
]
for _p, _list in {"v": ["cooked, didn't cook", "watched, didn't watch", "went, didn't go", "ate, didn't eat", "had, didn't have",
                        "bought, didn't buy"],
                  "s": ["I didn't take a nap last Sunday.", "She didn't see her friends last weekend.",
                        "They didn't go to the beach on Saturday.", "She didn't go to the park yesterday.",
                        "He didn't do his homework."],
                  "y": ["Tell me something you didn't do yesterday.", "Tell me something you didn't eat last week.",
                        "Tell me a place you didn't go last weekend."]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula6-say-{_p}{_i}"] = [(FS, _t + ("." if _p == "v" else ""), 300)]
SCRIPTS["b2-aula6-reading"] = [
    (FS, "A terrible day.", 800),
    (FS, "Yesterday was a terrible day! My alarm clock didn't ring, so I woke up very late.", 600),
    (FS, "I didn't take a shower, and I didn't have breakfast.", 600),
    (FS, "I ran to the bus stop, but I didn't catch the bus. I took a taxi, and it was very expensive.", 600),
    (FS, "At work, my computer didn't work all morning, and I didn't finish my report.", 600),
    (FS, "In the evening, I went to the gym, but I didn't exercise: I forgot my sneakers at home!", 600),
    (FS, "I didn't watch TV at night. I went to bed at nine p.m. Today is a better day!", 300),
]
SCRIPTS["b2-aula3-preps"] = [(FS, "Listen and choose the preposition.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["The keys are under the bed.", "The cat is behind the door.", "My phone is next to the computer.",
                     "The bank is across from the supermarket.", "The lamp is above the table.",
                     "The ball is between the boxes."])]
SCRIPTS["b2-aula3-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["The cat is in the box.", "The books are on the shelf.", "The ball is in front of the box.",
                     "My glasses were under the sofa."])]
SCRIPTS["b2-aula3-moving"] = [
    (MJ, "OK, Anna. Where can I put the sofa?", 300), (FS, "Put it in front of the TV, please.", 400),
    (MJ, "And the lamp? Is it OK next to the sofa?", 300), (FS, "Yes, perfect! And the plants can go between the windows.", 400),
    (MJ, "Where were the plants in your old apartment?", 300),
    (FS, "They were on the balcony. But this apartment doesn't have a balcony.", 400),
    (MJ, "And the big picture? Over the sofa?", 300), (FS, "No. Put it on the wall, above the bookcase.", 400),
    (MJ, "OK. And this box? What's in it?", 300), (FS, "My books! Put it under the table, please.", 400),
    (FS, "Thank you, Tom! You're a great friend!", 400), (MJ, "No problem! But… where is my pizza?", 300),
    (FS, "Ha ha! It's in the kitchen, next to the fridge!", 300),
]
for _i, _t in enumerate(["The ball is in the box.", "The ball is on the box.", "The ball is in front of the box.",
                         "The ball is under the box.", "The ball is between the boxes.", "The ball is behind the box.",
                         "The ball is next to the box.", "The ball is above the box."], 1):
    SCRIPTS[f"b2-aula3-say-s{_i}"] = [(FS, _t, 300)]
for _i, (_q, _a) in enumerate([("Where is the cat?", "It's under the chair."), ("Where are my keys?", "They're on the table."),
                               ("Where was the dog?", "It was behind the sofa."),
                               ("Where were the children?", "They were in the garden.")], 1):
    SCRIPTS[f"b2-aula3-say-q{_i}"] = [(MJ, _q, 400), (FS, _a, 300)]
for _i, _t in enumerate(["What is on your desk or table now?", "What is in front of your house or building?",
                         "Where was your bed when you were a child?", "What was next to your bed?"], 1):
    SCRIPTS[f"b2-aula3-say-y{_i}"] = [(FS, _t, 300)]
SCRIPTS["b2-aula3-reading"] = [
    (FS, "Where is Mimi?", 800),
    (FS, "My name is Paula, and Mimi is my cat. She is small and white, and she loves boxes.", 600),
    (FS, "Last night, Mimi wasn't in her bed, and my family and I were very worried. Where was she?", 600),
    (FS, "She wasn't under the sofa. She wasn't behind the curtains. She wasn't in the kitchen.", 600),
    (FS, "My brother was in the garden with a flashlight, but she wasn't there.", 600),
    (FS, "Then there was a small noise in my bedroom. There was a big box next to my wardrobe.", 600),
    (FS, "And guess what? Mimi was in the box! She was asleep between two old sweaters.", 600),
    (FS, "Today, her bed is in my bedroom, next to my bed. And the box? It's on the wardrobe now, and Mimi can't sleep in it!", 300),
]
SCRIPTS["b2-aula7-forms"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["Did you sleep well?", "Did she watch TV?", "Yes, they did.", "No, he didn't.",
                     "Where did you go last night?"])]
SCRIPTS["b2-aula7-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["Did they play soccer yesterday?", "No, he didn't.", "Where did you stay?",
                     "How long did you stay there?"])]
SCRIPTS["b2-aula7-vacation"] = [
    (MJ, "Hi, Carla! Welcome back! Did you travel on your vacation?", 300),
    (FS, "Yes, I did! I went to Salvador with my family.", 400),
    (MJ, "Cool! When did you go?", 300), (FS, "We went in January. It was very hot!", 400),
    (MJ, "Where did you stay?", 300), (FS, "We stayed at a small hotel near the beach.", 400),
    (MJ, "How long did you stay there?", 300), (FS, "For ten days.", 400),
    (MJ, "What did you eat? Did you try acarajé?", 300),
    (FS, "Yes, I did! I loved it. But my brother didn't like it. It was too spicy for him!", 400),
    (MJ, "Ha ha. Did you take a lot of pictures?", 300), (FS, "No, I didn't. My phone was broken!", 300),
]
for _i, (_q, _a) in enumerate([("Did she cook last night?", "Yes, she did."),
                               ("Did you go to the movies last weekend?", "No, I didn't."),
                               ("Did they have a picnic in the park on Saturday?", "Yes, they did."),
                               ("Did he buy a bike?", "No, he didn't.")], 1):
    SCRIPTS[f"b2-aula7-say-q{_i}"] = [(MJ, _q, 400), (FS, _a, 300)]
for _p, _list in {"w": ["Where did you go last night?", "What did you eat for dinner?", "When did you travel?",
                        "Why did you call me?", "How did you meet your best friend?"],
                  "y": ["Did you travel on your last vacation?", "When did you travel?", "Where did you go?",
                        "Where did you stay?", "How long did you stay there?", "Did you like the trip?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula7-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b2-aula7-reading"] = [
    (FS, "My first trip abroad.", 800),
    (FS, "Marina is 25 and lives in Curitiba. Last year, she traveled to another country for the first time. "
         "We asked her some questions.", 700),
    (MJ, "Where did you go?", 300), (FS, "I went to Buenos Aires, in Argentina.", 500),
    (MJ, "Did you go alone?", 300), (FS, "No, I didn't. I went with my best friend, Júlia.", 500),
    (MJ, "When did you travel?", 300), (FS, "We traveled in July. It was winter there, and it was very cold!", 500),
    (MJ, "Where did you stay?", 300), (FS, "We stayed in a small apartment in the city center.", 500),
    (MJ, "What did you do there?", 300), (FS, "We visited museums, walked a lot and watched a tango show.", 500),
    (MJ, "What did you eat?", 300), (FS, "We ate a lot of meat and empanadas. Delicious!", 500),
    (MJ, "Did you speak Spanish?", 300), (FS, "Yes, I did, but only a little!", 500),
    (MJ, "Did you like the trip?", 300), (FS, "Yes, I did. I loved it! I want to go back next year.", 300),
]
SCRIPTS["b2-aula9-forms"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I was sleeping when I heard a noise.", "They were cooking when the lights went out.",
                     "He was playing soccer when he broke his arm.", "When I left home, my cat was sleeping.",
                     "She was taking a shower when the water got cold."])]
SCRIPTS["b2-aula9-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 2000]] {w}", 3000)
    for n, w in zip(["one", "two", "three", "four"],
                    ["I was putting on makeup when I broke the mirror.", "Do you believe in ghosts?",
                     "Seven is my lucky number.", "We were walking in the cemetery when we saw a ghost."])]
SCRIPTS["b2-aula9-story"] = [
    (FS, "Hey, Pedro. You look tired! What happened?", 300),
    (MJ, "Oh, Lucy… Last night was crazy! I was staying at my grandfather's old house.", 400),
    (FS, "The old house near the cemetery?", 300),
    (MJ, "Yes! There was a full moon. I was reading in bed when I heard a noise in the kitchen.", 400),
    (FS, "Oh, no! What did you do?", 300),
    (MJ, "I was walking to the kitchen when the lights went out!", 400),
    (FS, "Really? Were you scared?", 300),
    (MJ, "Yes, I was! Then I saw a white shape next to the window.", 400),
    (FS, "A ghost?!", 300),
    (MJ, "No… it was my grandfather! He was eating cake in the dark!", 400),
    (FS, "Ha ha ha! So the house isn't haunted?", 300),
    (MJ, "No, it isn't. But I didn't sleep very well!", 300),
]
for _p, _list in {"w": ["good luck", "bad luck", "broken mirror", "magic", "ghost", "haunted", "cemetery",
                        "lucky number", "full moon", "fear"],
                  "s": ["I was sleeping when I heard a noise in the kitchen.", "I was putting on makeup when I broke the mirror.",
                        "My parents were cooking when the lights went out.", "He was playing soccer when he broke his arm.",
                        "When I left home, my cat was sleeping.", "When the water got cold, he was taking a shower."],
                  "y": ["Are you a superstitious person?", "Do you believe in ghosts?",
                        "Do you have a lucky number? If you do, what number is it?",
                        "What were you doing at eight o'clock last night?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula9-say-{_p}{_i}"] = [(FS, _t + ("." if _p == "w" else ""), 300)]
SCRIPTS["b2-aula9-reading"] = [
    (FS, "The broken mirror.", 800),
    (FS, "My grandmother is very superstitious. She says a broken mirror brings seven years of bad luck.", 600),
    (FS, "Last Friday, I was getting ready for a party. I was putting on makeup in the bathroom when my cat jumped "
         "on the sink. I dropped the mirror, and it broke!", 600),
    (FS, "My grandmother was watching TV in the living room when she heard the noise. She ran to the bathroom and said, "
         "\"Oh, no! Seven years of bad luck!\"", 600),
    (FS, "I don't believe in superstitions, but that night, some bad things happened.", 600),
    (FS, "I was walking to the bus stop when it started to rain. And when I arrived at the party, I was all wet!", 600),
    (FS, "But then, I was dancing with my friends when I met a very nice boy. His name is Rafael, and today he is "
         "my boyfriend!", 600),
    (FS, "So, was the broken mirror bad luck? I don't think so!", 300),
]
SCRIPTS["b2-aula8-forms"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["She was working last Saturday.", "They weren't playing basketball.", "Was the baby crying?",
                     "We were dancing at the party.", "He wasn't sleeping."])]
SCRIPTS["b2-aula8-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["They were playing soccer at this time yesterday.", "She wasn't baking a cake last Saturday.",
                     "Were you having a party yesterday?", "My brother was singing in the shower."])]
SCRIPTS["b2-aula8-detective"] = [
    (MJ, "Good morning, Ms. Lane. Someone took some money from the office last night. "
         "Where were you at nine o'clock?", 400),
    (FS, "I was at home. I was watching TV with my husband.", 400),
    (MJ, "What were you watching?", 300), (FS, "We were watching a soccer game. Brazil was playing!", 400),
    (MJ, "Hmm. And what was your husband doing at ten?", 300),
    (FS, "He was sleeping on the sofa. He always sleeps during soccer games!", 400),
    (MJ, "Were you talking on the phone at ten thirty?", 300),
    (FS, "Yes, I was. I was talking to my sister. She lives in Portugal.", 400),
    (MJ, "OK. And was your assistant, Mark, working late last night?", 300),
    (FS, "No, he wasn't. He was having dinner at a restaurant with his friends.", 400),
    (MJ, "Thank you, Ms. Lane. That's all for now.", 300),
]
for _p, _list in {"w": ["dance", "work", "sleep", "swim", "read", "study", "play", "watch", "walk", "eat", "drive", "drink"],
                  "s": ["She was working last Saturday.", "They were playing soccer at this time yesterday.",
                        "She wasn't baking a cake last Saturday.", "They weren't having a party yesterday.",
                        "Was the baby crying at two o'clock in the morning?", "Were they dancing? No, they weren't."],
                  "y": ["What were you doing at seven p.m. last night?", "What were you doing at this time yesterday?",
                        "Were you studying English last Saturday?", "What was your best friend doing yesterday afternoon?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula8-say-{_p}{_i}"] = [(FS, _t + ("." if _p == "w" else ""), 300)]
SCRIPTS["b2-aula8-reading"] = [
    (FS, "The blackout.", 800),
    (FS, "Yesterday at eight p.m., all the lights in my building went out for an hour. "
         "This is what my neighbors were doing at that time.", 600),
    (FS, "Mrs. Rosa, in apartment 101, was baking a cake. Her oven stopped, and the cake wasn't ready!", 600),
    (FS, "The Silva kids, in 102, weren't doing their homework. They were playing video games!", 600),
    (FS, "Mr. Tanaka, in 201, was taking a shower… in the dark!", 600),
    (FS, "Julia, in 202, was studying for a test, and her dog was sleeping under the table.", 600),
    (FS, "And in my apartment? I was cooking dinner. And my husband? He wasn't helping me. "
         "He was watching a soccer game on TV.", 600),
    (FS, "After the blackout, we all were in the hall, with candles, talking and laughing. It was a fun night!", 300),
]
SCRIPTS["b2-aula10-preps"] = [(FS, "Listen and choose the preposition.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["I was born in 1990.", "My birthday is on May 28th.", "I start work at 9 a.m.",
                     "She lives on Paulista Avenue.", "We live at 35 Flores Street.", "I'm at home."])]
SCRIPTS["b2-aula10-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["I study English on Mondays and Wednesdays.", "My father was born in 1945.",
                     "My brother's birthday is in July.", "I have English class at 7 p.m."])]
SCRIPTS["b2-aula10-school"] = [
    (MJ, "Good afternoon! Welcome to Sunshine English School. I need some information for your registration.", 300),
    (FS, "Sure!", 300), (MJ, "What's your name?", 300), (FS, "Laura Costa.", 400),
    (MJ, "Where were you born, Laura?", 300), (FS, "I was born in Recife, but I live in São Paulo now.", 400),
    (MJ, "And when were you born?", 300), (FS, "I was born on March 3rd, 1995.", 400),
    (MJ, "What's your address?", 300), (FS, "I live at 120 Augusta Street.", 400),
    (MJ, "OK. When do you want to have classes?", 300), (FS, "On Tuesdays and Thursdays, please.", 400),
    (MJ, "We have a class at 7 p.m. Is that OK?", 300), (FS, "Perfect! I finish work at 6.", 400),
    (MJ, "Great! Your first class is on Tuesday, at 7 p.m. See you!", 300),
]
for _p, _list in {"s": ["I have English class on Monday at 7 p.m.", "I was born in 1990.", "I was born on May 28th.",
                        "I live in Brazil.", "I live on Paulista Avenue.", "I'm at home."],
                  "y": ["Where were you born?", "When were you born?", "When is your birthday?",
                        "When do you have English class?", "What day is it today?", "What time do you get up?",
                        "Where do you live?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula10-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b2-aula10-reading"] = [
    (FS, "My grandfather's story.", 800),
    (FS, "My grandfather, Antônio, was born in Italy, in a small village, in 1945. "
         "He was born on a cold winter day: on January 10th.", 600),
    (FS, "In 1960, his family moved to Brazil. They lived in São Paulo, on Liberdade Street.", 600),
    (FS, "He met my grandmother in 1968, at a party. They got married on June 15th, 1970, at a small church.", 600),
    (FS, "Today, my grandparents live at 45 Flores Street, in Campinas.", 600),
    (FS, "Every Sunday, we have lunch at their house at noon. My grandfather always says: "
         "\"Lunch is at twelve o'clock, not at five past twelve!\"", 300),
]
SCRIPTS["b2-aula11-ordinals"] = [(FS, "Listen and choose the number you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["third", "fifth", "twelfth", "eighth", "twenty-first", "thirtieth"])]
SCRIPTS["b2-aula11-dictation"] = [(FS, "Listen and write the dates and years in numbers.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["It's October twenty-fifth.", "I was born in nineteen ninety-seven.", "It's the fifteenth of April.",
                     "My birthday is on March twenty-second.", "My grandfather was born in nineteen fifty."])]
SCRIPTS["b2-aula11-party"] = [
    (MJ, "Julia, Grandma's birthday is next month, right?", 300),
    (FS, "Yes! Her birthday is on June twelfth.", 400),
    (MJ, "June twelfth… That's a Friday this year.", 300),
    (FS, "Right. So let's have the party on Saturday, June thirteenth.", 400),
    (MJ, "Good idea! How old is she this year?", 300),
    (FS, "She was born in nineteen fifty-one, so she's seventy-five.", 400),
    (MJ, "Wow! Seventy-five!", 300),
    (FS, "And your birthday, Mike? It's in July, right?", 300),
    (MJ, "Yes, it's on the fourth of July! Like the American holiday!", 400),
    (FS, "Ha ha! Fireworks for you every year!", 300),
]
for _p, _list in {"o": ["first, second, third", "fourth, fifth, sixth", "seventh, eighth, ninth, tenth",
                        "eleventh, twelfth, thirteenth", "twentieth, twenty-first, twenty-second", "thirtieth, thirty-first"],
                  "d": ["It's October twenty-fifth.", "It's the fifteenth of April.", "Christmas is on December twenty-fifth.",
                        "the Fourth of July", "I was born in nineteen ninety-seven.", "It's February ninth, twenty twenty-six."],
                  "y": ["When is your birthday?", "When were you born?", "What's the date today?",
                        "When is your mother's birthday?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula11-say-{_p}{_i}"] = [(FS, _t + ("." if _p == "o" else ""), 300)]
SCRIPTS["b2-aula11-reading"] = [
    (FS, "Important dates in my life.", 800),
    (FS, "My name is Emma. I'm British, so I say the day first: I was born on the third of April, nineteen ninety-five, "
         "in London.", 600),
    (FS, "I started school on the fifth of September, two thousand. My first teacher was Mrs. Brown. I loved her!", 600),
    (FS, "On the twelfth of June, twenty fifteen, I travelled to Brazil. I met my husband, Pedro, in São Paulo. "
         "We got married on the twenty-first of December, twenty eighteen.", 600),
    (FS, "Our daughter, Sofia, was born on the second of February, twenty twenty-one.", 600),
    (FS, "Pedro's favourite date? The thirty-first of December! We have a big party every year.", 300),
]
SCRIPTS["b2-aula12-words"] = [(FS, "Listen and choose the word you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["snack", "steak", "meatballs", "jam", "soup", "chips"])]
SCRIPTS["b2-aula12-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["I usually have bread and coffee for breakfast.", "I hate mashed potato.",
                     "She has a snack in the afternoon.", "We don't like soda."])]
SCRIPTS["b2-aula12-friends"] = [
    (MJ, "Lucy, what's your favorite meal?", 300),
    (FS, "Breakfast! I love breakfast. I usually have coffee, yogurt and fruit.", 400),
    (MJ, "No eggs and bacon?", 300),
    (FS, "No, I don't like eggs. What about you, Tom? What do you usually have for lunch?", 400),
    (MJ, "I usually have rice, beans and steak. And french fries, of course!", 400),
    (FS, "And do you have a snack in the afternoon?", 300),
    (MJ, "No, I don't. I'm always very busy at work. And you?", 300),
    (FS, "I have a smoothie. Strawberry smoothie is my favorite.", 400),
    (MJ, "Hmm, nice. Let's have dinner together tonight. Do you like fish?", 300),
    (FS, "Yes, I love fish!", 300),
    (MJ, "Oh, no. I hate fish!", 300),
    (FS, "OK, OK. Pizza, then?", 300),
    (MJ, "Pizza! Perfect!", 300),
]
for _p, _list in {"w": ["breakfast, lunch, dinner", "a snack, a snake", "eggs and bacon", "rice and beans", "roast chicken",
                        "mashed potato", "shrimp risotto", "sandwich", "yogurt", "smoothie"],
                  "y": ["What's your favorite meal?", "What do you usually have for breakfast?",
                        "What do you usually have for lunch?", "What do you usually have for a snack?",
                        "Do you like hot dog?", "Do you like watermelon?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula12-say-{_p}{_i}"] = [(FS, _t + ("." if _p == "w" else ""), 300)]
SCRIPTS["b2-aula12-reading"] = [
    (FS, "A day of food.", 800),
    (FS, "Hi! I'm Camila, and I love food! My favorite meal is lunch.", 600),
    (FS, "For breakfast, I usually have coffee with milk, bread and cheese. I don't like eggs.", 600),
    (FS, "For lunch, I have rice and beans, salad and roast chicken. On Sundays, my mother makes meatballs "
         "with mashed potato. Delicious!", 600),
    (FS, "In the afternoon, I have a snack at work: fruit, nuts or yogurt. I hate chips!", 600),
    (FS, "For dinner, I usually have soup. My husband doesn't like soup, so he has a sandwich.", 600),
    (FS, "And on Fridays? Pizza and soda, of course!", 300),
]
SCRIPTS["b2-aula13-words"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["an orange", "two carrots", "some bananas", "a pineapple", "three tomatoes", "a cup of coffee"])]
SCRIPTS["b2-aula13-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["The bananas are fresh.", "I need some carrots.", "Milk is good for you.",
                     "My favorite fruit is watermelon."])]
SCRIPTS["b2-aula13-market"] = [
    (MJ, "Good morning! Fruit and vegetables! Very fresh!", 300),
    (FS, "Good morning! I want some bananas, please.", 300),
    (MJ, "Sure. How many bananas?", 300),
    (FS, "Six, please. And a watermelon for my son. He loves watermelon!", 400),
    (MJ, "Here you are. And the strawberries are very fresh today!", 300),
    (FS, "Hmm, no, thank you. I need some vegetables: two carrots and an onion.", 400),
    (MJ, "Two carrots and an onion. Anything else?", 300),
    (FS, "Do you have bread?", 300),
    (MJ, "No, sorry. Only fruit and vegetables here. The bakery is over there.", 400),
    (FS, "OK, thank you!", 300),
]
for _p, _list in {"w": ["orange, apple, pineapple", "watermelon, grape, banana", "papaya, coconut, strawberry, melon",
                        "potato, carrot, tomato, onion", "peas, corn, broccoli", "lettuce, cabbage, cucumber"],
                  "s": ["The banana is fresh.", "The bananas are fresh.", "Bacon is salty.", "I want a cup of coffee.",
                        "Two loaves of bread, please.", "My favorite fruit is watermelon."],
                  "y": ["What's your favorite fruit?", "What's your favorite vegetable?", "Do you like broccoli?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula13-say-{_p}{_i}"] = [(FS, _t + ("." if _p == "w" else ""), 300)]
SCRIPTS["b2-aula13-reading"] = [
    (MJ, "Saturday at the street market.", 800),
    (MJ, "Every Saturday morning, I go to the street market with my daughter, Lia.", 600),
    (MJ, "First we buy fruit: some bananas, two pineapples and a big watermelon. Lia loves strawberries, "
         "so we buy some strawberries for her too.", 600),
    (MJ, "Then we buy vegetables: carrots, tomatoes, onions and a lettuce for the salad. I don't buy broccoli. "
         "Lia hates broccoli!", 600),
    (MJ, "After the market, we go to the bakery. Bread is uncountable, so I say: \"Two loaves of bread, please.\"", 600),
    (MJ, "At home, I have a cup of coffee and Lia has a glass of milk. Saturday is my favorite day!", 300),
]
SCRIPTS["b2-aula14-words"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["There is an egg.", "There are some oranges.", "We don't need any rice.", "Is there any milk?",
                     "My favorite dessert is ice cream."])]
SCRIPTS["b2-aula14-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["There is some coffee.", "There aren't any tomatoes.", "Do you need an egg?",
                     "She wants some orange juice."])]
SCRIPTS["b2-aula14-cake"] = [
    (FS, "Dad, let's make a chocolate cake!", 300),
    (MJ, "Good idea, Bia! Let's see. We need some eggs. Are there any eggs?", 400),
    (FS, "Yes, there are three eggs in the fridge.", 400),
    (MJ, "Great. Is there any milk?", 300),
    (FS, "Yes, there is some milk.", 400),
    (MJ, "And flour? Is there any flour?", 300),
    (FS, "Yes, there's some flour in the cupboard. And there's some sugar, too.", 400),
    (MJ, "OK. And the chocolate?", 300),
    (FS, "Hmm… There isn't any chocolate, Dad!", 400),
    (MJ, "A chocolate cake without chocolate? No way! I can go to the supermarket. We need some chocolate!", 300),
]
for _p, _list in {"s": ["I need an orange.", "We need some oranges.", "We don't need any rice.", "Do we need any oranges?",
                        "There is some butter.", "There are two slices of bread.", "There aren't any apples.",
                        "Are there any apples in the fridge?", "dessert, desert"],
                  "y": ["What's your favorite dessert?", "Is there any milk in your fridge?", "Are there any eggs in your kitchen?",
                        "Are there any apples in your kitchen?", "Is there any chocolate in your house?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula14-say-{_p}{_i}"] = [(FS, _t + ("." if _t == "dessert, desert" else ""), 300)]
SCRIPTS["b2-aula14-reading"] = [
    (MJ, "The empty fridge.", 800),
    (MJ, "I'm Lucas. I'm a student, and I live alone. It's Sunday night and I'm very hungry!", 600),
    (MJ, "I open the fridge. Hmm… There isn't any meat, and there aren't any vegetables. "
         "There is some butter and there is an egg. Only one egg!", 600),
    (MJ, "I look in the kitchen cupboard. There is some rice, but there isn't any bread. "
         "There are some cookies, but they're my roommate's cookies.", 600),
    (MJ, "So, what's for dinner? Rice with a fried egg! And for dessert? An apple.", 600),
    (MJ, "Tomorrow I need to go to the supermarket. I need some bread, some milk, some fruit and some eggs.", 300),
]
SCRIPTS["b2-aula15-words"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["a jar of honey", "two cans of soda", "a carton of milk", "two loaves of bread",
                     "three scoops of ice cream", "a packet of pasta"])]
SCRIPTS["b2-aula15-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["There are a lot of tomatoes in the fridge.", "I don't eat much chocolate.",
                     "How many cups of coffee do you drink?", "I have a little money left."])]
SCRIPTS["b2-aula15-list"] = [
    (MJ, "Marta, let's make a shopping list for the picnic on Saturday. How many people are coming?", 300),
    (FS, "Six people: us, my sister, her husband and their two kids.", 400),
    (MJ, "OK. How much bread do we need?", 300),
    (FS, "Two loaves of bread. And some cheese. There isn't much cheese at home.", 400),
    (MJ, "Right. A packet of cheese slices… And drinks? How much water do we need?", 300),
    (FS, "Four bottles of water. It's hot on Saturday.", 400),
    (MJ, "And the kids love soda. Let's buy some cans of soda, too.", 300),
    (FS, "Good idea. And for dessert? A box of chocolate!", 400),
    (MJ, "Chocolate again? You eat a lot of chocolate, Marta!", 300),
    (FS, "Ha ha. Yes, I do!", 300),
]
for _p, _list in {"s": ["a bottle of water", "a can of soda", "a carton of milk", "a jar of honey", "a packet of pasta",
                        "two loaves of bread", "three slices of cheese", "two scoops of ice cream", "a bar of chocolate",
                        "There are a lot of tomatoes in the fridge.", "I don't eat much chocolate.",
                        "I have a few oranges left."],
                  "y": ["How many cups of coffee do you drink in a day?", "How much water do you drink in a day?",
                        "Do you eat much chocolate?", "How many scoops of ice cream do you usually have?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula15-say-{_p}{_i}"] = [(FS, _t if _t[-1] in ".?" else _t + ".", 300)]
SCRIPTS["b2-aula15-reading"] = [
    (FS, "Grandma's kitchen.", 800),
    (FS, "My grandma loves cooking, and her kitchen is always full of food!", 600),
    (FS, "In her cupboard, there are a lot of packets of pasta and rice, and there are many tins of tuna. "
         "There are three jars of honey, too. Grandma has a little honey in her tea every morning.", 600),
    (FS, "In her fridge, there are two cartons of milk, a few eggs and a lot of cheese. "
         "But there isn't much juice. Grandma doesn't drink much juice. She prefers water.", 600),
    (FS, "Every Sunday, she buys two loaves of bread at the bakery. And on my birthday? A big cake and three "
         "scoops of ice cream for me!", 600),
    (FS, "How much sugar does Grandma eat? Not much. But how many cookies does she make? A lot!", 300),
]
SCRIPTS["b2-aula16-numbers"] = [(FS, "Listen and choose the number you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["a hundred and fifty", "a thousand and five", "ten thousand and eighty-six",
                     "a thousand, two hundred and fifty-five", "a hundred thousand"])]
SCRIPTS["b2-aula16-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["Brasília is hotter than Curitiba.", "English is easier than Chinese.",
                     "A car is more expensive than a bike.", "My English is better now."])]
SCRIPTS["b2-aula16-apartments"] = [
    (FS, "Bruno, look! Two apartments. One is on Flores Street and one is on Ocean Avenue.", 300),
    (MJ, "How much is the apartment on Flores Street?", 300),
    (FS, "Two thousand, five hundred reais a month. And the apartment on Ocean Avenue is one thousand, "
         "eight hundred reais.", 400),
    (MJ, "So the apartment on Ocean Avenue is cheaper.", 300),
    (FS, "Yes, but the apartment on Flores Street is bigger. It has a bigger kitchen.", 400),
    (MJ, "Hmm. And which one is closer to your work?", 300),
    (FS, "Ocean Avenue. Flores Street is further from my work. It's ten kilometers!", 400),
    (MJ, "And Ocean Avenue is closer to the beach!", 300),
    (FS, "That's true. But I love big kitchens…", 400),
    (MJ, "Carla, the beach is better than a big kitchen!", 300),
    (FS, "OK, OK. Ocean Avenue, then!", 300),
]
for _p, _list in {"n": ["a hundred and five", "a hundred and fifty-five", "a thousand",
                        "a thousand, two hundred and fifty-five", "ten thousand and eighty-six", "a hundred thousand"],
                  "s": ["The boy is taller than the girl.", "The cat is smaller than the dog.", "Canada is colder than Brazil.",
                        "A car is more expensive than a bike.", "Salad is healthier than pizza.",
                        "Pizza is more delicious than salad."],
                  "y": ["Who is taller, you or your best friend?", "Which is colder, Curitiba or Rio de Janeiro?",
                        "Which is more expensive, a car or a bike?", "Which is healthier, salad or pizza?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula16-say-{_p}{_i}"] = [(FS, _t + ("." if _p == "n" else ""), 300)]
SCRIPTS["b2-aula16-reading"] = [
    (FS, "Two sisters.", 800),
    (FS, "My name is Paula, and I have a sister, Renata. We are very different!", 600),
    (FS, "Renata is older than me. She's thirty and I'm twenty-five. But I'm taller than her: "
         "I'm one meter seventy, and she's one meter sixty-two.", 600),
    (FS, "Renata lives in Curitiba, and I live in Salvador. Curitiba is colder than Salvador, of course! "
         "Salvador is about two thousand, four hundred kilometers from Curitiba. That's far!", 600),
    (FS, "Renata is a doctor. She works more than me, but her salary is bigger: she makes about "
         "fifteen thousand reais a month.", 600),
    (FS, "I'm a teacher. My job is easier, and I think I'm happier. I have more free time, "
         "and the beach is near my house!", 600),
    (FS, "But Renata is a better cook than me. Her lasagna is more delicious than my lasagna!", 300),
]
SCRIPTS["b2-aula17-places"] = [(FS, "Listen and choose the place you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["drugstore", "post office", "museum", "theater", "railway station", "square"])]
SCRIPTS["b2-aula17-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["This is the biggest park in the city.", "Soccer is the most popular sport in Brazil.",
                     "It's the best bakery in town.", "August is the coldest month here."])]
SCRIPTS["b2-aula17-tour"] = [
    (MJ, "Welcome to Pinewood! I'm your guide today. This is the main square.", 300),
    (FS, "It's beautiful! What's that old building?", 300),
    (MJ, "That's Saint Mary's Church. It's the oldest building in town. It's three hundred years old.", 400),
    (FS, "Wow! And where do people go on weekends?", 300),
    (MJ, "To the park. It's the most popular place on weekends. It's also the biggest park in the region.", 400),
    (FS, "Is there a museum?", 300),
    (MJ, "Yes, the Train Museum. The most interesting thing there is an old train from eighteen ninety. "
         "And it's free on Sundays.", 400),
    (FS, "Great! Today is Sunday! But first… I need a cup of coffee!", 300),
    (MJ, "Ha ha. Rosa's Bakery has the best coffee in town. It's next to the church.", 300),
    (FS, "Perfect! Let's go to the bakery first!", 300),
]
for _p, _list in {"p": ["drugstore, church, hospital", "street market, park, police station", "post office, mall, supermarket",
                        "town hall, museum, theater", "zoo, bus station, railway station", "square, bank, cinema",
                        "bookstore, gym, school", "bakery, restaurant, pet shop"],
                  "s": ["Josh is the tallest in the family.", "Orange juice is the healthiest of the four drinks.",
                        "Soccer is the most popular sport in Brazil.", "My best friend is Ana."],
                  "y": ["Who is the tallest person in your family?", "What is the best restaurant in your city?",
                        "What is the most beautiful city in Brazil?", "What is the most delicious food you can cook?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula17-say-{_p}{_i}"] = [(FS, _t + ("." if _p == "p" else ""), 300)]
SCRIPTS["b2-aula17-reading"] = [
    (MJ, "The best town in the world.", 800),
    (MJ, "I live in Santa Luz, a small town in Minas Gerais. For me, it's the best town in the world!", 600),
    (MJ, "The most important place is the main square. On Sundays, there is a street market there, "
         "and all the families go.", 600),
    (MJ, "Next to the square, there is São José Church. It's the oldest building in town: it's two hundred and fifty "
         "years old.", 600),
    (MJ, "The best bakery is Dona Maria's Bakery. Her cheese bread is the most delicious in Minas!", 600),
    (MJ, "We don't have a mall or a zoo, but we have a beautiful park and a small museum.", 600),
    (MJ, "July is the coldest month, and January is the hottest. The happiest time of the year? "
         "The town party in June!", 300),
]
SCRIPTS["b2-aula18-words"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["turn right", "go straight on", "at the roundabout", "walk two blocks", "at the intersection",
                     "take the U-turn"])]
SCRIPTS["b2-aula18-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["Go straight on and turn right at the traffic light.", "Go past the school.",
                     "Is there a drugstore near here?", "The bank is next to the post office."])]
SCRIPTS["b2-aula18-tourist"] = [
    (MJ, "Excuse me. I'm looking for the bus station. Can you help me?", 300),
    (FS, "Sure! It's not far. It's a ten-minute walk.", 400),
    (MJ, "Great!", 300),
    (FS, "Go straight on this street. At the traffic light, turn left.", 400),
    (MJ, "At the traffic light, turn left. OK.", 300),
    (FS, "Then go past the hospital. It's a big white building.", 400),
    (MJ, "Go past the hospital…", 300),
    (FS, "Walk two blocks. The bus station is at the corner, on the right.", 400),
    (MJ, "Two blocks, at the corner, on the right. Is there a drugstore near the bus station?", 300),
    (FS, "Yes, there's a drugstore next to the bus station.", 400),
    (MJ, "Thank you very much!", 300),
    (FS, "You're welcome!", 300),
]
for _p, _list in {"d": ["Turn right.", "Turn left.", "Go straight on.", "Turn around.", "Take the U-turn.", "at the corner",
                        "at the traffic light", "at the intersection", "at the roundabout", "Walk one block.",
                        "Go past the church."],
                  "q": ["Is there a mall near here?", "Where can I find a drugstore?", "How far is the hospital from here?",
                        "Excuse me, I'm looking for the city hall. Can you help me?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula18-say-{_p}{_i}"] = [(FS, _t if _t[-1] in ".?" else _t + ".", 300)]
SCRIPTS["b2-aula18-reading"] = [
    (FS, "How to get to my party.", 800),
    (FS, "Hi, everyone! My birthday party is on Saturday at eight p.m. Here are the directions from the subway station.", 600),
    (FS, "Leave the station and go straight on Rio Branco Avenue. Go past the big supermarket and the post office.", 600),
    (FS, "At the traffic light, turn right on Flores Street. Walk two blocks.", 600),
    (FS, "At the roundabout, turn left. You can see a small square with a fountain.", 600),
    (FS, "My building is at the corner, next to the bakery. It's number forty-five. "
         "The bakery has the best cake in town, so I have a big cake for you!", 600),
    (FS, "It's a fifteen-minute walk. See you there!", 300),
]
SCRIPTS["b2-aula19-jobs"] = [(FS, "Listen and choose the job you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["painter", "actor", "writer", "designer", "programmer", "manager"])]
SCRIPTS["b2-aula19-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["She is an actor.", "I have English class twice a week.", "The moon is beautiful tonight.",
                     "It's the best pizza in town."])]
SCRIPTS["b2-aula19-party"] = [
    (MJ, "Hi! I'm Sam. Nice to meet you.", 300),
    (FS, "Hi, Sam! I'm Rita. So, what do you do?", 300),
    (MJ, "I'm a programmer. I work at home. And you?", 400),
    (FS, "I'm a designer. And at night, I'm a singer in a band!", 400),
    (MJ, "Really? How often does your band play?", 300),
    (FS, "Twice a month, at a bar near the beach.", 400),
    (MJ, "Cool! Is your family artistic, too?", 300),
    (FS, "Yes! My brother is an actor. He was in a play last year. But now he's a manager at a restaurant!", 400),
    (MJ, "Ha ha. Life is difficult for actors!", 300),
]
for _p, _list in {"j": ["teacher, inventor, singer, actor", "manager, programmer, director", "painter, writer, composer",
                        "conductor, editor, designer"],
                  "s": ["It's a photo of my daughter.", "He is a doctor.", "She is an architect.",
                        "They have classes three times a week.", "Can you close the window, please?",
                        "I have a cat and a dog. The cat is very old, but the dog is just a puppy."],
                  "y": ["What do you do?", "What does your mother do?", "How often do you study English?",
                        "Do you have a pet?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula19-say-{_p}{_i}"] = [(FS, _t + ("." if _p == "j" else ""), 300)]
SCRIPTS["b2-aula19-reading"] = [
    (MJ, "An artistic family.", 800),
    (MJ, "My family is very artistic! My mother is a painter. She paints every day, and she has an exhibition "
         "twice a year. My father is a writer. He writes books for children.", 600),
    (MJ, "My sister is an actor. She's in a play at the Municipal Theater. The play is about the moon and "
         "the sun. It's beautiful!", 600),
    (MJ, "And me? I'm not an artist. I'm a programmer. I work at home three days a week.", 600),
    (MJ, "We live in Belo Horizonte, in a big old house. We have a dog and a parrot. The dog is quiet, "
         "but the parrot sings all day. Maybe the parrot is the real singer in my family!", 600),
    (MJ, "We have dinner together every night. It's the best part of my day.", 300),
]
SCRIPTS["b2-aula20-words"] = [(FS, "Listen and choose the word you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["happily", "bathe", "gently", "well", "owl", "slowly"])]
SCRIPTS["b2-aula20-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["It runs and plays happily.", "I gently groom my puppy.", "It learns quickly.",
                     "She speaks English fluently."])]
SCRIPTS["b2-aula20-petshop"] = [
    (FS, "Hello! Welcome to Happy Pets. Can I help you?", 300),
    (MJ, "Hi! This is my new puppy, Toby. He needs a bath today.", 400),
    (FS, "Oh, he's so cute! Does he like water?", 300),
    (MJ, "No, he doesn't. He hates baths!", 400),
    (FS, "Don't worry. I bathe the dogs very gently and carefully.", 400),
    (MJ, "Thank you. Oh, and he eats very quickly. Is that OK?", 300),
    (FS, "Some puppies eat fast. Give him a little food, three times a day.", 400),
    (MJ, "OK. He's very smart, too. He learns quickly!", 300),
    (FS, "Great! You can pick him up at four p.m.", 400),
    (MJ, "Perfect. See you later, Toby!", 300),
]
for _p, _list in {"w": ["donkey, deer, cat, chameleon", "owl, dog, hedgehog", "hamster, fish, alligator",
                        "play, clean up, walk, pet", "feed, train, groom", "bathe, cuddle"],
                  "s": ["My puppy eats very well.", "It runs and plays happily.", "I gently groom my puppy.",
                        "It learns quickly.", "She sings beautifully.", "He drives very carefully."],
                  "y": ["Do you have a pet?", "How do you speak English?", "How do you drive?",
                        "Who sings well in your family?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b2-aula20-say-{_p}{_i}"] = [(FS, _t + ("." if _p == "w" else ""), 300)]
SCRIPTS["b2-aula20-reading"] = [
    (FS, "My new puppy.", 800),
    (FS, "I have a new puppy. Every morning, I feed it. My puppy eats very well.", 600),
    (FS, "Then, I walk my puppy in the park. It runs and plays happily. It runs fast to catch the ball.", 600),
    (FS, "In the afternoon, I gently groom my puppy. It likes being brushed.", 600),
    (FS, "I also train my puppy with simple commands. It learns quickly.", 600),
    (FS, "Taking care of a puppy is fun and rewarding.", 300),
]
SCRIPTS["b3-aula1-verbs"] = [(FS, "Listen and choose the verb you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["I visited my grandma.", "She bought a new phone.", "We met at the mall.", "They played soccer.",
                     "He wore a blue jacket.", "I stayed at home."])]
SCRIPTS["b3-aula1-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["They watched a movie yesterday.", "I ate pizza last Sunday.", "My friends bought a new house.",
                     "We studied English a week ago."])]
SCRIPTS["b3-aula1-office"] = [
    (MJ, "Good morning, Ana! How was your weekend?", 300),
    (FS, "Hi, Leo! It was great! On Saturday, I went to the beach with my sister. The weather was perfect.", 400),
    (MJ, "Nice!", 300),
    (FS, "We swam, we walked a lot, and then we had lunch at a small restaurant. I ate fish and rice. Delicious! "
         "And you? How was your weekend?", 400),
    (MJ, "Busy! On Saturday, I painted my bedroom. It's blue now!", 400),
    (FS, "Wow! And on Sunday?", 300),
    (MJ, "On Sunday, I was very tired. But in the afternoon, I met an old friend from school. "
         "We watched a movie and talked for hours.", 400),
    (FS, "That sounds fun. OK, coffee time!", 300),
]
for _p, _list in {"v": ["cook, cooked", "watch, watched", "start, started", "finish, finished", "do, did", "go, went",
                        "see, saw", "eat, ate", "buy, bought", "read, read", "meet, met", "wear, wore"],
                  "s": ["I explored the city center yesterday.", "We enjoyed the trip last weekend.", "She studied a lot last night.",
                        "I saw beautiful places on my trip to Italy last month.", "I met amazing people on my last trip.",
                        "I had lunch with my family on Sunday."],
                  "y": ["Tell me three things you did last weekend.", "Tell me what you did yesterday morning.",
                        "Tell me about something you did when you were a kid."]}.items():
    for _i, _t in enumerate(_list, 1):
        _s = _t + "." if _p == "v" else _t
        if _t == "read, read":
            _s = "read, " + PAST_READ + "."
        SCRIPTS[f"b3-aula1-say-{_p}{_i}"] = [(FS, _s, 300)]
SCRIPTS["b3-aula1-reading"] = [
    (FS, "When my grandma was a kid.", 800),
    (FS, "A long time ago, in nineteen fifty-five, my grandma Rosa lived on a small farm in Minas Gerais.", 600),
    (FS, "Every morning, she woke up at five o'clock. She helped her mother in the kitchen and carried water "
         "from the river.", 600),
    (FS, "She walked to school with her brothers. The school was very far, and they arrived tired!", 600),
    (FS, "There was no TV, so in the evenings the family played cards and listened to the radio.", 600),
    (FS, "When she was eighteen, she moved to Belo Horizonte. There, she met my grandpa at a party. "
         "They danced all night!", 600),
    (FS, "Last week, she showed me some old photos and told me these stories. I loved them!", 300),
]
SCRIPTS["b3-aula2-sounds"] = [(FS, "Listen and choose the sound of E D.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["laughed", "decided", "used", "helped", "educated", "loved"])]
SCRIPTS["b3-aula2-tense"] = [(FS, "Present or past? Listen carefully.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["They traveled a lot.", "I help my mom.", "We kissed the baby.", "You use my computer.",
                     "She laughed a lot."])]
SCRIPTS["b3-aula2-portugal"] = [
    (FS, "Last year, I traveled to Portugal with my husband. It was our first trip to Europe!", 500),
    (FS, "My husband and I decided to visit Lisbon first. We walked a lot every day, and I loved the old trams.", 500),
    (FS, "One night, we listened to fado at a small bar.", 500),
    (FS, "Then we visited Porto. We tasted the famous wine and watched the sunset by the river.", 500),
    (FS, "My husband laughed all the time. He loved the food!", 500),
    (FS, "On the last day, I cried a little. I wanted to stay in Portugal forever!", 300),
]
for _p, _list in {"i": ["want, wanted", "need, needed", "decide, decided", "educate, educated", "collect, collected",
                        "divide, divided"],
                  "t": ["cook, cooked", "laugh, laughed", "kiss, kissed", "help, helped", "play, played", "love, loved",
                        "use, used", "travel, traveled"],
                  "s": ["I traveled to Chile last year.", "We laughed and danced all night.", "She decided to study English.",
                        "They cleaned the house and cooked dinner.", "He helped me and I thanked him."]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula2-say-{_p}{_i}"] = [(FS, _t if _p == "s" else _t + ".", 300)]
SCRIPTS["b3-aula2-reading"] = [
    (MJ, "The surprise party.", 800),
    (MJ, "Last Saturday was my mom's sixtieth birthday. My sister and I planned a surprise party for her.", 600),
    (MJ, "In the morning, my dad invited her to the mall. While they were out, we cleaned the house, "
         "cooked lots of food and decorated the living room with balloons.", 600),
    (MJ, "At six o'clock, all our relatives arrived. We turned off the lights and waited in silence.", 600),
    (MJ, "When my mom opened the door, we shouted: Surprise! She screamed, then laughed and cried at the same time.", 600),
    (MJ, "We danced, talked and played old songs until midnight. My mom hugged everybody. She loved it!", 300),
]
SCRIPTS["b3-aula3-forms"] = [(FS, "Affirmative or negative? Listen and choose.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["He didn't call me.", "We met at school.", "She didn't wear a dress.", "They slept well.",
                     "I didn't take a nap."])]
SCRIPTS["b3-aula3-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["She didn't sleep for many hours.", "We didn't watch TV last night.",
                     "My friend didn't give me a present.", "They didn't do their homework."])]
SCRIPTS["b3-aula3-vacation"] = [
    (FS, "Tiago! Welcome back! How was your vacation in the mountains?", 300),
    (MJ, "Terrible! It rained every day. It didn't stop raining!", 400),
    (FS, "Oh, no!", 300),
    (MJ, "We didn't go hiking, and I didn't see the famous waterfall.", 400),
    (FS, "What a shame. And the hotel?", 300),
    (MJ, "My wife didn't like the hotel. The rooms were cold, and the restaurant was closed.", 400),
    (FS, "Really?", 300),
    (MJ, "Yes. We didn't eat well, and I didn't take any good photos. Everything was gray!", 400),
    (FS, "So you were in the hotel all week?", 300),
    (MJ, "Yes! But I read three books. That was the good part!", 300),
]
for _p, _list in {"v": ["cooked, didn't cook", "watched, didn't watch", "went, didn't go", "ate, didn't eat",
                        "saw, didn't see", "slept, didn't sleep", "gave, didn't give", "wore, didn't wear"],
                  "s": ["I didn't take a nap last Sunday.", "She didn't see her friends last weekend.",
                        "They didn't go to the beach on Saturday.", "He didn't do his homework.",
                        "My father didn't see an accident.", "His girlfriend didn't wear a red dress last night."],
                  "y": ["Yesterday, I didn't…", "Last weekend, I didn't…", "When I was a kid, I didn't…",
                        "This morning, I didn't…"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula3-say-{_p}{_i}"] = [(FS, _t + "." if _p == "v" else _t, 300)]
SCRIPTS["b3-aula3-reading"] = [
    (FS, "A week without my phone.", 800),
    (FS, "Last month, I tried an experiment: one week without my phone!", 600),
    (FS, "On the first day, it was difficult. I didn't know the time, because I don't have a watch. "
         "I didn't check my messages, and I didn't watch videos before bed.", 600),
    (FS, "But then, things changed. I didn't spend hours on social media, so I had more time. "
         "I read two books and I cooked new recipes.", 600),
    (FS, "I didn't take photos of my food. I ate it! I talked to my neighbors and I walked in the park every day.", 600),
    (FS, "There was one problem: my mom called me ten times and I didn't answer. She wasn't happy!", 600),
    (FS, "I didn't stop using my phone forever, but now I use it less.", 300),
]
SCRIPTS["b3-aula4-questions"] = [(FS, "Listen and choose the question you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["Did you like it?", "Where do they live?", "Did she work there?", "What did you eat?",
                     "How long do you stay?"])]
SCRIPTS["b3-aula4-dictation"] = [(FS, "Listen and complete the questions.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["Why did you call me?", "How did you meet your best friend?", "Did they have a picnic?",
                     "Where did you stay?"])]
SCRIPTS["b3-aula4-marathon"] = [
    (MJ, "Congratulations, Sofia! You won the city marathon! How long did you run?", 300),
    (FS, "Thank you! I ran for two hours and thirty minutes.", 400),
    (MJ, "Amazing! When did you start running?", 300),
    (FS, "When I was twelve. I ran on the beach with my father every morning.", 400),
    (MJ, "Did you sleep well last night?", 300),
    (FS, "No, I didn't! I was very nervous. I slept only four hours.", 400),
    (MJ, "And what did you eat before the race?", 300),
    (FS, "I ate bread with banana and drank some water. That's all.", 400),
    (MJ, "Who did you call after the race?", 300),
    (FS, "My grandmother! She watched the race on TV, and she cried a lot.", 400),
    (MJ, "Ha ha. Congratulations again, Sofia!", 300),
]
for _p, _list in {"s": ["Did you go to the park? Yes, I did.", "Did she cook dinner? No, she didn't.",
                        "Did they play soccer yesterday? Yes, they did.", "Did he buy a bike? No, he didn't.",
                        "What did you eat in the morning?", "Where did she go last night?", "Why did you call me?",
                        "How did you meet your best friend?"],
                  "y": ["Did you travel on your last vacation?", "When did you travel?", "Where did you go?",
                        "Where did you stay?", "How long did you stay there?", "Did you like the trip?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula4-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b3-aula4-reading"] = [
    (FS, "An interview with my grandpa.", 800),
    (FS, "Where did you grow up, Grandpa?", 300), (MJ, "I grew up in a small town in Paraná.", 500),
    (FS, "Did you like school?", 300), (MJ, "No, I didn't! I liked soccer. I played every afternoon.", 500),
    (FS, "What was your first job?", 300), (MJ, "I worked at a bakery. I started at four in the morning!", 500),
    (FS, "How did you meet Grandma?", 300),
    (MJ, "She bought bread at the bakery every day. One day, I gave her a cake for free.", 500),
    (FS, "Did she like the cake?", 300),
    (MJ, "Yes, she did. And she liked me, too! We got married two years later.", 300),
]
SCRIPTS["b3-aula5-words"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["It's Peter's car.", "That's my brother's room.", "These are the children's toys.",
                     "Whose bag is this?", "Who's your teacher?"])]
SCRIPTS["b3-aula5-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["That's my mom's restaurant.", "We went to my parents' house.", "Whose watch is this?",
                     "Kim and Kyle's mom is a doctor."])]
SCRIPTS["b3-aula5-lost"] = [
    (FS, "Mr. Silva, look at all these things in my classroom!", 300),
    (MJ, "Oh, the lost and found box again! Whose jacket is this? The blue one.", 300),
    (FS, "That's Tom's jacket. He wears it every day.", 400),
    (MJ, "And these glasses?", 300),
    (FS, "Oh! Those are my glasses! I looked for them all morning!", 400),
    (MJ, "Ha ha. And this notebook? It says: Ana and Leo.", 300),
    (FS, "That's Ana and Leo's notebook. They share it for the science project.", 400),
    (MJ, "And the umbrella?", 300),
    (FS, "It's Carol's umbrella. She left it here yesterday.", 400),
    (MJ, "And whose water bottle is this?", 300),
    (FS, "Hmm, I don't know. Who's the owner?", 400),
    (MJ, "Oh, wait… It's my bottle! Sorry!", 300),
]
for _p, _list in {"s": ["Whose hat is it? It's Justin's hat.", "Whose watch is this? It's Neymar's watch.",
                        "Whose dress is it? It's Shakira's dress.", "Whose guitar is it? It's Madonna's guitar.",
                        "It's Peter's car.", "That is my parents' garden.", "These are the children's toys.",
                        "Kim and Kyle's mom is a doctor."],
                  "y": ["What's your mother's name?", "What's your best friend's name?", "Who's your favorite singer?",
                        "Where is your parents' house?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula5-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b3-aula5-reading"] = [
    (FS, "My family's restaurant.", 800),
    (FS, "My grandparents started a small restaurant in nineteen eighty. Its name is Nonna Lucia's. "
         "Lucia is my grandmother's name!", 600),
    (FS, "Today, it's my mom's restaurant. My dad is the chef, and my aunt is the manager.", 600),
    (FS, "The most famous dish is my grandma's lasagna. People come from other cities to try it!", 600),
    (FS, "On weekends, I help at the restaurant. My cousins help too, and the children's corner is their idea: "
         "there are toys and books for the kids.", 600),
    (FS, "My brother Marcus doesn't work there. Marcus's dream is different: he wants to open a bakery. "
         "Maybe one day we can say: Let's buy bread at Marcus's!", 300),
]
SCRIPTS["b3-aula6-words"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["It's hers.", "Is this yours?", "That's our car.", "They're theirs.", "It's his phone."])]
SCRIPTS["b3-aula6-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["Is this your laptop or mine?", "These keys are ours.", "That isn't their house.",
                     "Whose jacket is this? It's his."])]
SCRIPTS["b3-aula6-party"] = [
    (FS, "What a mess! Look, sunglasses. Are they yours, Rick?", 300),
    (MJ, "No, they aren't mine. They're Julia's. She wore them yesterday.", 400),
    (FS, "OK. And this phone? Is it Marco's?", 300),
    (MJ, "No, it's mine! I looked for my phone all morning!", 400),
    (FS, "Ha ha. And this scarf? It's beautiful.", 300),
    (MJ, "It's your mother's scarf, I think.", 400),
    (FS, "Oh, yes, it's hers. I can take it to her tomorrow.", 400),
    (MJ, "Paula… whose dog is that in our garden?", 300),
    (FS, "It's the neighbors' dog. It's theirs. He comes here every day!", 300),
]
for _p, _list in {"w": ["my, your, his, her", "its, our, your, their", "mine, yours, his, hers", "its, ours, yours, theirs"],
                  "s": ["It's my castle. It's mine.", "It's Josh's jacket. It's his jacket. It's his.",
                        "It's Sarah's t-shirt. It's her t-shirt. It's hers.", "They're Mike's glasses. They're his.",
                        "This book is hers.", "Is this your laptop or mine?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula6-say-{_p}{_i}"] = [(FS, _t + ("." if _p == "w" else ""), 300)]
SCRIPTS["b3-aula6-reading"] = [
    (MJ, "Sharing a house.", 800),
    (MJ, "I live with three friends in a big old house near our university.", 600),
    (MJ, "My bedroom is small, but it's mine and I love it. Lara's bedroom is the biggest. Hers has a balcony!", 600),
    (MJ, "Pedro and Davi share a bedroom. Theirs is always messy: clothes everywhere!", 600),
    (MJ, "We share the kitchen. There's one rule: our food is on the shelves, and each person has a shelf. "
         "The top shelf is mine, the second is Lara's…", 600),
    (MJ, "Last week, someone ate my yogurt. I asked: Whose spoon is this? Pedro said: It's not mine! "
         "But the spoon was his. Ha!", 600),
    (MJ, "It's not always easy, but this house is ours, and we're like a family.", 300),
]
SCRIPTS["b3-aula7-words"] = [(FS, "Listen and choose the pronoun you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["Call him later.", "Can you help us?", "I don't know her.", "We visit them every Sunday.",
                     "She texts me every day."])]
SCRIPTS["b3-aula7-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["My parents love us.", "I can see it in the garden.", "Emily visits them on weekends.",
                     "I always play with them."])]
SCRIPTS["b3-aula7-neighbor"] = [
    (FS, "Honey, I met our new neighbor today!", 300),
    (MJ, "Really? I don't know her. What's her name?", 300),
    (FS, "Helen. I met her at the elevator. She's very nice.", 400),
    (MJ, "Does she live alone?", 300),
    (FS, "Yes, with two cats. She loves them! And look: she gave me a cake.", 400),
    (MJ, "A cake? Wow, I like her already!", 300),
    (FS, "Ha ha. She invited us to her apartment on Saturday.", 400),
    (MJ, "Great. Let's take her some flowers.", 300),
]
for _p, _list in {"s": ["me, you, him, her, it, us, you, them.", "Sarah calls him every day.", "My parents love us.",
                        "I can see it in the garden.", "Emily visits them on weekends.", "Yes, I do. I read it twice a year.",
                        "Yes, I do. I always play with them."],
                  "y": ["Do you have a favorite book? How often do you read it?",
                        "Do you have any pets? How often do you play with them?",
                        "Do you have a car? Do you drive it very often?",
                        "Do you call your parents? How often do you call them?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula7-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b3-aula7-reading"] = [
    (MJ, "My best friend.", 800),
    (MJ, "My best friend is Felipe. I met him at school when we were seven.", 600),
    (MJ, "Felipe has a big family: two sisters and a little brother. I love them! His mother makes amazing cakes, "
         "and she always gives me a piece.", 600),
    (MJ, "Now Felipe lives in Portugal. I miss him, but we talk every week. I call him on Sundays, or he calls me.", 600),
    (MJ, "Last year, I visited him in Lisbon. He showed me the city, and his girlfriend, Inês, cooked for us. "
         "I liked her a lot!", 600),
    (MJ, "Felipe has an old guitar. He plays it every night. And me? I sing with him… badly!", 300),
]
SCRIPTS["b3-aula8-words"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I'm gonna travel.", "She isn't going to study.", "We're going to relax.", "Are they going to come?",
                     "He's gonna cook."])]
SCRIPTS["b3-aula8-rachel"] = [
    (FS, "This weekend, I have a lot of plans. On Saturday morning, I'm going to visit my grandparents.", 400),
    (FS, "We're going to have lunch together.", 400),
    (FS, "In the afternoon, my friends and I are going to play volleyball at the beach, and then we're going to eat açaí.", 400),
    (FS, "On Sunday, I'm going to clean my apartment.", 400),
    (FS, "At night, my family and I are going to watch a movie. It's going to be a very fun weekend!", 300),
]
for _p, _list in {"s": ["going to, gonna.", "I'm going to call you later.", "She's going to study tonight.",
                        "We are going to watch a movie.", "I'm going to relax a lot this weekend.",
                        "My friends are going to go to the beach on Saturday."],
                  "y": ["What are you not going to do this weekend?", "What are you going to do on Saturday?",
                        "What are you going to do on Sunday?", "Are you going to study English this week?"]}.items():
    for _i, _t in enumerate(_list, 1):
        _s = _t.replace("I'm going to call", "I'm gonna call").replace("She's going to study", "She's gonna study") \
               .replace("We are going to watch", "We're gonna watch")
        SCRIPTS[f"b3-aula8-say-{_p}{_i}"] = [(FS, _s, 300)]
SCRIPTS["b3-aula8-reading"] = [
    (MJ, "Our big trip.", 800),
    (MJ, "We have big plans for July! My wife, my two kids and I are going to travel to Chile.", 600),
    (MJ, "We bought the tickets last month. We're going to fly to Santiago on July tenth.", 600),
    (MJ, "In Santiago, we're going to stay at a small hotel downtown. My wife is going to visit the museums. "
         "She loves art. The kids are going to see snow for the first time in the mountains!", 600),
    (MJ, "I'm going to try the famous Chilean food. And we aren't going to rent a car: "
         "we're going to use the subway.", 600),
    (MJ, "We aren't going to stay long, only eight days, but it's going to be amazing!", 300),
]
SCRIPTS["b3-aula9-predictions"] = [(FS, "Listen and choose the prediction.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["Look at the sky! It's going to rain.", "Look at those cars! They're going to crash.",
                     "Be careful! She's gonna fall!", "It's eight thirty and he's still in bed. He's going to be late.",
                     "The baby is hungry. She's gonna cry."])]
SCRIPTS["b3-aula9-beach"] = [
    (FS, "Dad, look at the sky! Those clouds are very dark.", 300),
    (MJ, "Oh, no. It's going to rain.", 300),
    (FS, "And look at that dog! He's near our bag!", 300),
    (MJ, "Whose dog is that? Oh, no! He's going to eat our sandwiches!", 400),
    (FS, "Too late! And Dad, your back is very red. Where's your sunscreen?", 400),
    (MJ, "I don't have any! I'm going to get a sunburn.", 300),
    (FS, "You already have one!", 300),
    (MJ, "OK, OK. Let's pick up our things. We're going to go home now.", 300),
]
for _p, _list in {"s": ["Look at the sky! It's going to rain.", "Look at the cars! They're going to crash.",
                        "Look at her! She's going to sleep.", "He's gonna fall.", "They're gonna get married.",
                        "Lunch is going to be ready in five minutes."],
                  "y": ["What's going to happen with cars in 20 years?", "Are people going to work at home?",
                        "Are we going to travel to the moon?", "What's going to happen with your city?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula9-say-{_p}{_i}"] = [(FS, _t.replace("20 years", "twenty years"), 300)]
SCRIPTS["b3-aula9-reading"] = [
    (MJ, "The soccer final.", 800),
    (MJ, "It's Sunday, and we're watching the final on TV. It's one to one, and there are only two minutes left!", 600),
    (MJ, "Look! Our best player has the ball. He's running very fast… He's going to score!", 600),
    (MJ, "Oh, no! The goalkeeper is going to catch the ball… No! It's a goal! We're going to win!", 600),
    (MJ, "My dad is standing on the sofa. He's going to fall! My mom is looking at him. She's going to be angry.", 600),
    (MJ, "And my little brother has a big glass of juice in his hand, and he's jumping. "
         "He's going to drop it on the carpet!", 600),
    (MJ, "It's a crazy day. But tonight, the whole city is going to celebrate!", 300),
]
SCRIPTS["b3-aula10-words"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I'll be late for work.", "You won't like it.", "She'll miss the train.", "It'll rain tomorrow.",
                     "We'll go on holiday."])]
SCRIPTS["b3-aula10-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["You'll break your leg.", "He'll win the match.", "She won't get the job.",
                     "Will the meeting be long?"])]
SCRIPTS["b3-aula10-fortune"] = [
    (FS, "Welcome, Paulo. Give me your hand. Hmm… I see a lot of things.", 300),
    (MJ, "Great! I'm an optimist. Tell me everything!", 300),
    (FS, "Next month, you'll get a new job.", 400),
    (MJ, "A new job! Wonderful!", 300),
    (FS, "And you'll travel to Italy. In Italy, you'll meet a beautiful woman.", 400),
    (MJ, "Wow! Will I be rich?", 300),
    (FS, "Hmm… No, you won't. Sorry.", 400),
    (MJ, "Oh. OK. And tomorrow? What will happen tomorrow?", 300),
    (FS, "Tomorrow… you'll lose your wallet.", 400),
    (MJ, "What? Oh, no! Maybe I'm a pessimist now…", 300),
]
for _p, _list in {"s": ["I'll. I'll be late. I'll be late for work.", "You'll. You'll break. You'll break your leg.",
                        "He'll. He'll win. He'll win the match.", "She'll. She'll miss. She'll miss the train.",
                        "It'll. It'll rain. It'll rain tomorrow.", "We'll. We'll go. We'll go on holiday.",
                        "They'll. They'll pass. They'll pass the exam."],
                  "y": ["Do you think you'll have a nice weekend?", "Do you think you'll have a better job in the future?",
                        "Do you think you'll make some new friends this year?", "Do you think you'll live to be a hundred?",
                        "Do you think you'll read more than one book this year?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula10-say-{_p}{_i}"] = [(FS, _t.replace(". ", ". [[slnc 400]] ") if _p == "s" else _t, 300)]
SCRIPTS["b3-aula10-reading"] = [
    (FS, "Life in twenty fifty: what do you think?", 800),
    (FS, "Carla, the optimist: I think life will be better. People will live to be a hundred and twenty, and doctors "
         "will cure many diseases. We'll work only four days a week!", 700),
    (MJ, "José, the pessimist: I don't think it'll be better. The summers will be very hot, and there won't be "
         "enough water. Robots will do our jobs, so a lot of people won't have work.", 700),
    (FS, "Amanda: I'm not sure. Maybe cars will fly, and we'll travel to Mars on vacation. But I think people "
         "will still love pizza and soccer. Some things will never change!", 300),
]
SCRIPTS["b3-aula11-words"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I'll have the chicken.", "Shall I open the window?", "I won't forget.", "We'll call you later.",
                     "Shall we go?"])]
SCRIPTS["b3-aula11-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["Shall I make you a sandwich?", "I'll lend you some money.", "I'll love you forever.",
                     "I'll help you when I finish."])]
SCRIPTS["b3-aula11-cafe"] = [
    (MJ, "What will you have, Nina?", 300),
    (FS, "Hmm… I'll have a cappuccino and a piece of chocolate cake.", 400),
    (MJ, "Good choice. I'll have an espresso. Brr, it's cold in here.", 300),
    (FS, "Yes, the window is open.", 300),
    (MJ, "Shall I close it?", 300),
    (FS, "Yes, please! Oh, no! I left my wallet at home!", 400),
    (MJ, "Don't worry. I'll pay today.", 300),
    (FS, "Thank you, Lucas! I'll pay next time, I promise.", 400),
    (MJ, "Ha ha. OK. I won't forget!", 300),
]
for _p, _list in {"s": ["Yes, I'll have a diet coke, please.", "I'll help you when I finish.", "I'll change, I promise.",
                        "I'll love you forever.", "Shall I help you open the window?", "Shall we do the washing up?"],
                  "y": ["It's hot in here.", "I'm thirsty.", "I have a headache.", "These bags are heavy.", "I'm hungry."]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula11-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b3-aula11-reading"] = [
    (FS, "New Year's promises.", 800),
    (FS, "Every December thirty-first, my family writes promises for the new year. Here are this year's promises:", 600),
    (MJ, "Dad: I'll stop eating so much junk food, and I'll walk to work.", 500),
    (FS, "Mom: I won't work on weekends. I'll spend more time with my family.", 500),
    (FS, "My sister, Clara: I'll study harder, and I won't use my phone at dinner.", 500),
    (FS, "Me: I'll learn English! I'll practice every day with my English course.", 500),
    (FS, "Grandma: I'll teach my grandchildren how to make my famous chocolate cake.", 500),
    (FS, "Last year, we didn't keep all our promises… but this year will be different!", 300),
]
SCRIPTS["b3-aula12-words"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I'm going to visit my parents.", "I'll have the chicken.", "It's going to rain.",
                     "I think Brazil will win.", "I promise I'll call you."])]
SCRIPTS["b3-aula12-birthday"] = [
    (FS, "Leo, Mom's birthday is on Sunday. I have a plan: I'm going to make a chocolate cake. "
         "I bought the ingredients yesterday.", 400),
    (MJ, "Great! And flowers? She loves flowers.", 300),
    (FS, "We don't have any flowers.", 300),
    (MJ, "OK, I'll buy the flowers.", 400),
    (FS, "Perfect. I wanted to have the party in the park, but look at the weather app. It's going to rain on Sunday.", 400),
    (MJ, "Then we'll have the party at home.", 300),
    (FS, "Good. It's a surprise, so don't tell Mom! And please, don't be late.", 400),
    (MJ, "I promise I won't be late.", 300),
]
for _p, _list in {"s": ["I'll have the chicken, please.", "I'm going to visit my parents next weekend.",
                        "I think Brazil will win the next World Cup.", "I see clouds. It's going to rain.",
                        "I will help you with your homework tonight.", "Look! The bomb is going to explode!"],
                  "y": ["Will it be cold tomorrow where you live?", "What are your plans for next Christmas?",
                        "Which country do you think will win the next World Cup?",
                        "What do you promise you will do better this year?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula12-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b3-aula12-reading"] = [
    (FS, "Saturday.", 800),
    (FS, "Mari: Hi, guys! We're going to go to the beach on Saturday. We decided last week. Who wants to come?", 500),
    (MJ, "Tom: Me! I'll bring the volleyball.", 500),
    (FS, "Julia: Hmm, I checked the weather app. There are a lot of clouds. I think it's going to rain.", 500),
    (FS, "Mari: Oh no! OK, new plan: I'll check the weather again on Friday.", 500),
    (MJ, "Tom: If it rains, we can watch a movie at my place. I'll make popcorn!", 500),
    (FS, "Julia: Great idea. I'll bring the drinks. I promise I won't be late this time.", 500),
    (FS, "Mari: Ha ha. I don't believe you, Julia!", 300),
]
SCRIPTS["b3-aula13-nowfuture"] = [(FS, "Listen. Now or future?", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I'm having lunch with my boss tomorrow.", "I'm cooking dinner right now.",
                     "We're flying to Rome next week.", "Shh! She's taking a shower.", "They're getting married in June."])]
SCRIPTS["b3-aula13-call"] = [
    (MJ, "Hi, Laura! It's Daniel.", 300),
    (FS, "Daniel! Great to hear from you! Are you in Lisbon?", 300),
    (MJ, "Yes, I arrived last night. I'm here for work until Friday. Can we meet?", 400),
    (FS, "Of course! What are you doing on Wednesday?", 300),
    (MJ, "Wednesday is impossible. I'm visiting a factory outside the city all day.", 400),
    (FS, "And Thursday evening?", 300),
    (MJ, "Sorry, I'm having dinner with my old teacher at seven thirty. And on Thursday I'm having a breakfast meeting "
         "with clients at eight, and I'm giving a presentation at two.", 400),
    (FS, "Wow, you're busy! What about Thursday morning, at ten thirty?", 300),
    (MJ, "Perfect. Coffee at ten thirty!", 300),
    (FS, "There's a lovely café near the river. Let's meet there.", 300),
    (MJ, "Great. On Friday I'm flying home, so Thursday is perfect. See you then!", 300),
]
for _p, _list in {"s": ["I'm watching a movie tonight.", "I'm going to a party on Saturday night.",
                        "I'm running in the park on Sunday morning.", "I'm seeing an old friend tonight.",
                        "She isn't leaving until Friday.", "What are you doing this weekend?"],
                  "y": ["What are you doing tonight?", "Who are you meeting on Monday?", "Where are you going on Sunday?",
                        "What are you doing on Saturday night?", "Are you traveling next month?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula13-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b3-aula13-reading"] = [
    (FS, "Hi, Júlia! Everything is ready for my brother's wedding! Here's the plan for the weekend.", 600),
    (FS, "On Friday, we're picking up Grandma at the airport at six p.m. She's flying from Recife.", 600),
    (FS, "On Saturday morning, my mom and I are going to the hairdresser at nine. The ceremony is starting at four p.m. "
         "at Santa Rita Church, and the party is at the Blue Garden restaurant.", 600),
    (FS, "On Sunday, we're having a family lunch at my parents' house. And on Monday, the couple is flying to Chile "
         "for their honeymoon!", 600),
    (FS, "Are you coming on Friday or Saturday? Tell me! Love, Ana.", 300),
]
SCRIPTS["b3-aula14-words"] = [(FS, "Listen and choose the word you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["bored", "interesting", "tired", "embarrassing", "scary", "relaxed"])]
SCRIPTS["b3-aula14-movie"] = [
    (FS, "Gabriel, the horror movie yesterday was so frightening! I was very scared.", 300),
    (MJ, "Really? I thought it was boring. I fell asleep in the middle!", 400),
    (FS, "You slept? I screamed in the cinema! Everybody looked at me. It was so embarrassing.", 400),
    (MJ, "Ha ha. I didn't hear you. And the cinema was crowded!", 300),
    (FS, "And the end was surprising. I didn't expect it.", 400),
    (MJ, "OK, next time we're watching a comedy. And I'm choosing!", 300),
]
for _p, _list in {"w": ["excited, exciting", "interested, interesting", "surprised, surprising", "bored, boring",
                        "confused, confusing", "frightened, frightening", "embarrassed, embarrassing", "tired, tiring",
                        "scared, scary", "stressed, stressful"],
                  "s": ["The movie was so interesting that I watched it twice.", "She has nothing to do. She is bored.",
                        "The movie was so boring that I fell asleep.", "The beach was crowded on Sunday.",
                        "She's so stressed. Her routine is very stressful."],
                  "y": ["What's something boring for you?", "When do you feel tired?", "What's the most interesting movie you know?",
                        "What makes you stressed?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula14-say-{_p}{_i}"] = [(FS, _t + "." if _p == "w" else _t, 300)]
SCRIPTS["b3-aula14-reading"] = [
    (FS, "My first day at work.", 800),
    (FS, "Last Monday was my first day at a new company. I was so excited, but I was also a little frightened.", 600),
    (FS, "The morning was very interesting. My boss showed me the office, and I met a lot of people. "
         "Then I had a training session about the computer system. It was really confusing, and I was confused all "
         "afternoon!", 600),
    (FS, "At lunch, something embarrassing happened: I dropped my coffee on my new boss's shoes. I was so embarrassed!", 600),
    (FS, "But my boss laughed and said: Don't worry! That was surprising.", 600),
    (FS, "At the end of the day, I was tired, but happy. It was a tiring day, but a good one.", 300),
]
SCRIPTS["b3-aula15-words"] = [(FS, "Listen and choose the word you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five", "six"], ["knees", "teeth", "toes", "mouth", "feet", "back"])]
SCRIPTS["b3-aula15-yoga"] = [
    (FS, "Good morning, everyone. Sit on your mat and close your eyes.", 700),
    (FS, "Breathe in through your nose… and out through your mouth. Put your hands on your belly. Feel your breath.", 700),
    (FS, "Now, move your shoulders slowly, up and down. Move your neck to the left… and to the right. Very good.", 700),
    (FS, "Now, stand up. Don't bend your knees too much. Try to touch your toes with your fingers. Can you do it? "
         "Great job!", 300),
]
for _p, _list in {"w": ["mouth, head, toes, neck", "hand, arms, foot, back", "face, belly, teeth, shoulders",
                        "eyes, fingers, tongue, ears", "legs, nose, knees, lips"],
                  "s": ["Head, shoulders, knees and toes.", "I can see with my eyes.", "I can hear with my ears.",
                        "I can smell with my nose.", "When I was a baby, I couldn't walk on my feet.",
                        "When I was younger, I could touch my toes with my fingers."]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula15-say-{_p}{_i}"] = [(FS, _t + "." if _p == "w" else _t, 300)]
SCRIPTS["b3-aula15-reading"] = [
    (MJ, "The soccer player's body.", 800),
    (MJ, "Rafael is a professional soccer player. His most important tools are his legs and feet. "
         "He kicks the ball with his right foot, but he can use his left foot, too.", 600),
    (MJ, "He also uses his head a lot to score goals. Goalkeepers are different: they use their hands and arms.", 600),
    (MJ, "Rafael takes care of his body. Every morning, he stretches his back, his shoulders and his neck. "
         "He has a strong belly from a lot of exercise.", 600),
    (MJ, "Last year, he had a problem with his left knee. He couldn't play for three months! "
         "Now his knee is fine, and he can run again.", 600),
    (MJ, "And his smile? He has perfect white teeth. He goes to the dentist every six months!", 300),
]
SCRIPTS["b3-aula16-words"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["She can drive.", "He can't sing.", "I could swim.", "They couldn't come.", "Could you help me?"])]
SCRIPTS["b3-aula16-swim"] = [
    (FS, "When you were a child, could you swim?", 300),
    (MJ, "No, I couldn't. I was afraid of water.", 400),
    (FS, "Really? I could swim when I was five.", 300),
    (MJ, "Wow. I couldn't even go into the pool!", 400),
    (FS, "And now, can you swim?", 300),
    (MJ, "Yes, now I can swim very well!", 300),
]
for _p, _list in {"s": ["could, couldn't.", "can, can't.", "She can drive.", "I could swim when I was younger.",
                        "He can't sing.", "I couldn't swim when I was five.", "Can I use your phone?", "Could you help me?"],
                  "y": ["Could you swim when you were a child?", "Could you read before you started school?",
                        "Can you cook very well?", "Can you drive?", "What can you do now that you couldn't do as a child?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula16-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b3-aula16-reading"] = [
    (MJ, "My grandmother, then and now.", 800),
    (MJ, "My grandmother Helena is eighty-two, and she's amazing!", 600),
    (MJ, "When she was young, she lived on a farm. She could ride a horse, and she could cook for twenty people. "
         "But she couldn't go to school after the age of ten, so she couldn't read very well.", 600),
    (MJ, "At sixty, she decided to study. Now she can read books and newspapers, and she can write long letters to me!", 600),
    (MJ, "Two years ago, she bought a smartphone. At first, she couldn't use it. Now she can send messages, "
         "make video calls and watch cooking videos.", 600),
    (MJ, "There's one thing she can't do: she can't stay awake after nine o'clock!", 300),
]
SCRIPTS["b3-aula17-tenses"] = [(FS, "Listen. Present, past or future?", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I was able to finish the report.", "We'll be able to help you tomorrow.",
                     "She's able to speak three languages.", "They're going to be able to travel next year.",
                     "He wasn't able to sleep last night."])]
SCRIPTS["b3-aula17-guitar"] = [
    (MJ, "When I was sixteen, I loved a famous rock band, and I wanted to play the guitar like them.", 600),
    (MJ, "My parents paid for guitar classes. My teacher was very patient, but I wasn't able to move my fingers fast "
         "enough. It was very frustrating!", 600),
    (MJ, "After a year, I was able to play three easy songs, but only very slowly. My friends started a band, but I "
         "wasn't able to play with them.", 600),
    (MJ, "Now I know I won't be able to play in a band, and that's OK. Next month, I'm going to try the drums. "
         "Maybe I'll be able to play them!", 300),
]
for _p, _list in {"s": ["able, able to.", "She is able to dance salsa.", "I'm not able to ride a horse.",
                        "He was able to speak Japanese.", "They will be able to scuba dive.",
                        "She won't be able to scuba dive.", "I was able to win the gold medal."],
                  "y": ["Is there anything you tried to learn, but you weren't able to?", "Are you able to ride a horse?",
                        "What will you be able to do after this English course?", "What were you able to do last year?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula17-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b3-aula17-reading"] = [
    (FS, "My first marathon.", 800),
    (FS, "Three years ago, I wasn't able to run for five minutes. I was always tired!", 600),
    (FS, "Then a friend invited me to a running group. In the beginning, it was very hard. "
         "After two months, I was able to run five kilometers without stopping.", 600),
    (FS, "Last year, I decided to try a marathon: forty-two kilometers! On the day of the race, it was very hot. "
         "At kilometer thirty, my legs hurt a lot, but I could hear my family cheering for me.", 600),
    (FS, "After four hours and fifty minutes, I was able to finish the race. I cried!", 600),
    (FS, "Now I'm training for a marathon in Chile. I hope I'll be able to finish it in less than four and a half hours.", 300),
]
SCRIPTS["b3-aula18-words"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["May I come in?", "It might snow tonight.", "You may leave now.", "She might not come.",
                     "May the force be with you."])]
SCRIPTS["b3-aula18-weekend"] = [
    (MJ, "Tati, what are we doing this weekend? The beach?", 300),
    (FS, "Maybe. But look at the forecast: it might rain on Saturday.", 400),
    (MJ, "Hmm. It might not rain. Forecasts are often wrong.", 300),
    (FS, "True. But if it rains, we might go to the cinema.", 400),
    (MJ, "Good idea. There's a new comedy. Is anybody coming with us?", 300),
    (FS, "My sister might come. She might bring her kids, too.", 400),
    (MJ, "OK! So, beach or cinema?", 300),
    (FS, "Let's check the weather app on Saturday morning.", 300),
]
for _p, _list in {"s": ["may, day, say, play.", "might, night, right, light.", "May I drink some water, please?",
                        "It might rain later.", "You might try calling her.", "May all your dreams come true.",
                        "May the force be with you.", "May I speak with the manager?"],
                  "y": ["What might you do this weekend?", "Where might you travel next year?",
                        "What might you have for dinner tonight?", "Who might you call today?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula18-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b3-aula18-reading"] = [
    (FS, "School trip to the Science Museum. Dear students, on Friday, we are visiting the Science Museum. "
         "Please read this information.", 600),
    (FS, "We are leaving at eight a.m. The traffic might be bad, so we might arrive a little late.", 600),
    (FS, "You may bring your phone, but you may not use it during the guided tour.", 600),
    (FS, "The museum café might be crowded, so you might want to bring a snack and a bottle of water.", 600),
    (FS, "It might rain in the afternoon. Bring a jacket!", 600),
    (FS, "If you have questions, you may send me an e-mail. May you all have a wonderful day of learning! Ms. Carter.", 300),
]
SCRIPTS["b3-aula19-words"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["You should sleep more.", "He shouldn't drive fast.", "Should I call her?", "We should go now.",
                     "You shouldn't worry."])]
SCRIPTS["b3-aula19-tired"] = [
    (MJ, "Lia, you look tired. Are you OK?", 300),
    (FS, "I didn't sleep well. I was checking my notifications all night.", 400),
    (MJ, "In bed? You shouldn't use your phone in bed. The blue light affects your sleep.", 300),
    (FS, "I know… I couldn't stop scrolling. My screen time was nine hours yesterday!", 400),
    (MJ, "Nine hours?!", 300),
    (FS, "Yes. And then I binge-watched a series until midnight.", 400),
    (MJ, "Lia, you should try a digital detox. And you should turn off your notifications at night.", 300),
    (FS, "You're right. I should do it this weekend.", 300),
]
for _p, _list in {"s": ["should, shouldn't.", "She should go to bed early.", "You should drink more water.",
                        "You shouldn't smoke. It's bad for your health.", "Should I call him?", "Should I stay or should I go?",
                        "You should set a screen time limit.", "You shouldn't scroll for hours."],
                  "y": ["I'm always tired.", "I want to speak English better.", "I spend six hours a day on social media.",
                        "I have a headache.", "My friend gets anxious without his phone."]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula19-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b3-aula19-reading"] = [
    (FS, "Ask Anna.", 800),
    (FS, "Dear Anna, my fourteen-year-old son spends all his time on his phone. He plays games until two a.m., and in "
         "the morning he can't wake up for school. His grades are bad now. What should I do? Worried Mom.", 800),
    (FS, "Dear Worried Mom, you should talk to your son calmly. He shouldn't feel that you are angry. "
         "Together, you should set a screen time limit, maybe two hours a day.", 600),
    (FS, "He shouldn't take his phone to bed: the blue light affects sleep. "
         "You should also find activities for the family without screens: a walk in the park, a board game, cooking.", 600),
    (FS, "And you shouldn't use your phone at dinner either! Children copy what we do. Anna.", 300),
]
SCRIPTS["b3-aula20-problems"] = [(FS, "Listen and choose the problem you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2600)
    for n, w in zip(["one", "two", "three", "four", "five", "six"],
                    ["She has a stomachache.", "He has a cough.", "She is sneezing.", "I have a sore throat.",
                     "She has a rash.", "He has the flu."])]
SCRIPTS["b3-aula20-doctor"] = [
    (MJ, "Good morning, Mrs. Lopes. What's the matter?", 300),
    (FS, "Good morning, doctor. I have a terrible sore throat, and I'm coughing a lot.", 400),
    (MJ, "When did it start?", 300),
    (FS, "On Monday. And last night I had a fever.", 400),
    (MJ, "Let me check your temperature… Hmm, thirty-nine degrees. That's high. Does your body ache?", 300),
    (FS, "Yes, my whole body aches.", 400),
    (MJ, "You have the flu. You should stay in bed and drink a lot of water and tea.", 300),
    (FS, "Can I go to work tomorrow?", 300),
    (MJ, "No. You shouldn't go to work this week. You need to rest.", 300),
    (FS, "OK, doctor. Thank you.", 300),
]
for _p, _list in {"w": ["ache.", "She has a stomachache.", "She has a toothache.", "He has a backache.", "She has an earache.",
                        "She has a headache.", "He has sunburn.", "She is throwing up.", "He has a cough.",
                        "She is sneezing.", "Her ankle is swollen.", "She has a sore throat."],
                  "y": ["What's the matter?", "Do you have a fever?", "What should I do for a sore throat?",
                        "What should I do for sunburn?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula20-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b3-aula20-reading"] = [
    (MJ, "A terrible trip.", 800),
    (MJ, "Last summer, my family went to Bahia for a week. It was a disaster!", 600),
    (MJ, "On the first day, my dad slept on the beach without sunscreen. He had terrible sunburn!", 600),
    (MJ, "On the second day, my sister ate shrimp at a beach kiosk. That night, she had a stomachache and she was "
         "throwing up.", 600),
    (MJ, "My mom walked a lot in new sandals, and she had blisters on both feet.", 600),
    (MJ, "And me? I swam in the cold sea for hours, and I got a sore throat and a cough. On the last day, I had a fever, too.", 600),
    (MJ, "The only person who was fine was my little brother. He was sneezing a bit, but he said he was great!", 600),
    (MJ, "Next year, we should stay at home. Or we should take a doctor with us!", 300),
]
SCRIPTS["b3-aula21-words"] = [(FS, "Listen. Must or mustn't?", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["You must rest.", "You mustn't run.", "She must drink water.", "They mustn't be late.",
                     "I must call my mom."])]
SCRIPTS["b3-aula21-surgery"] = [
    (FS, "Hello, Pedro. The surgery on your knee went very well. Now, listen carefully.", 400),
    (MJ, "OK, doctor.", 300),
    (FS, "You must rest for a week. And you mustn't play soccer for two months.", 400),
    (MJ, "Two months? Oh, no!", 300),
    (FS, "Sorry, but it's very important. You must take this medicine every eight hours. It makes you sleepy, "
         "so you mustn't drive this week.", 400),
    (MJ, "OK. Can I take a shower?", 300),
    (FS, "Yes, but you mustn't get the bandage wet. And you must come back in two weeks.", 400),
    (MJ, "Thank you, doctor. I'll follow everything.", 300),
]
for _p, _list in {"s": ["must, mustn't.", "I must talk to my boss about the new project.", "It's a fantastic movie. You must watch it.",
                        "I'm very hungry. I must eat something.", "You must not touch the animals at the zoo.",
                        "You mustn't touch the pictures.", "You must take this medicine."],
                  "y": ["What must you do this week?", "Tell me a movie that people must watch.",
                        "What mustn't you do at work or at school?", "What must you do to speak English well?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula21-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b3-aula21-reading"] = [
    (FS, "Sunny Club. Swimming pool rules.", 800),
    (FS, "You must take a shower before you enter the pool. You must wear a swimming cap. "
         "Children under ten must be with an adult.", 600),
    (FS, "You mustn't run around the pool. The floor is wet! You mustn't eat or drink in the water.", 600),
    (FS, "You mustn't dive in the shallow area. You mustn't use glass bottles near the pool.", 600),
    (FS, "The pool is open from seven a.m. to eight p.m. You must leave the water at seven forty-five. "
         "Have fun and be safe!", 300),
]
SCRIPTS["b3-aula22-situations"] = [
    (FS, "Situation one.", 600),
    (MJ, "Hmm, it's busy again. The line is busy! I'll try again later.", 1200),
    (FS, "Situation two.", 600),
    (FS, "Hi, Marcos, it's Julia. You're not answering, so I'm leaving a message on your voicemail. Call me back, OK? Bye!", 1200),
    (FS, "Situation three.", 600),
    (FS, "Thank you for calling. All our agents are busy. Please hold.", 400),
    (MJ, "Again? I'm waiting on hold for twenty minutes!", 1200),
    (FS, "Situation four.", 600),
    (MJ, "So, the meeting is on Tuesday at… Hello? Hello? Are you there? Oh, no. I was cut off!", 1200),
    (FS, "Situation five.", 600),
    (FS, "And these are our sales results for this year…", 300),
    (MJ, "Oh, sorry! Sorry, everybody! That's my phone! I'm so embarrassed.", 300),
]
SCRIPTS["b3-aula22-dictation"] = [(FS, "Listen and complete.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1800]] {w}", 2800)
    for n, w in zip(["one", "two", "three", "four"],
                    ["I'll call you back later.", "Don't forget to hang up.", "Put your phone on silent mode.",
                     "She left a message on his voicemail."])]
for _p, _list in {"s": ["He's dialing a number.", "She's texting a friend.", "He hung up.", "He's calling back.",
                        "She left a message on his voicemail.", "The line's busy.", "They put her on hold.",
                        "He was cut off in the middle of a conversation.", "Please hold. I'll be back in two minutes."],
                  "y": ["What's your ringtone?", "Do you prefer calling or texting?", "Do you listen to your voicemail?",
                        "When do you put your phone on silent mode?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula22-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b3-aula22-reading"] = [
    (FS, "The phone call disaster.", 800),
    (FS, "Yesterday, I needed to talk to my bank about a problem with my card. I dialed the helpline number, "
         "and a recorded voice said: Please hold. They put me on hold for twenty-five minutes!", 600),
    (FS, "Finally, a woman answered. But in the middle of the conversation, I was cut off. I called back, "
         "but the line was busy.", 600),
    (FS, "Then, at three p.m., I had an important meeting with my boss. I forgot to put my phone on silent mode, "
         "and it went off in the middle of the meeting. My ringtone is a very loud rock song. How embarrassing!", 600),
    (FS, "It was the bank. I couldn't answer, so they left a message on my voicemail.", 600),
    (FS, "In the evening, I texted my best friend: Worst phone day ever!", 300),
]
SCRIPTS["b3-aula23-words"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["She has to work today.", "I had to wear a uniform.", "You don't have to pay.",
                     "Do you have to cook tonight?", "You mustn't smoke here."])]
SCRIPTS["b3-aula23-job"] = [
    (FS, "Welcome to the store, Lucas! Let me explain the rules. You have to arrive at eight forty-five. "
         "The store opens at nine.", 300),
    (MJ, "OK. Do I have to wear a suit and tie?", 300),
    (FS, "No, you don't have to wear a tie. But you have to wear the store T-shirt.", 400),
    (MJ, "Great. Do I have to work on Sundays?", 300),
    (FS, "No, you don't. The store is closed on Sundays.", 400),
    (MJ, "Good! At my old job, I had to work on weekends.", 300),
    (FS, "Here, you mustn't use your phone in front of customers, and you mustn't eat in the store. "
         "There's a kitchen in the back.", 400),
    (MJ, "Do I have to bring my lunch?", 300),
    (FS, "No, you don't have to. We have lunch for the employees.", 400),
    (MJ, "Perfect!", 300),
]
for _p, _list in {"s": ["You have to wear a mask.", "She has to wear glasses.", "I had to wear a uniform at school.",
                        "Do you have to cook tonight?", "You don't have to pay. This museum is free.",
                        "You mustn't drive along this street.", "I have to be punctual."],
                  "y": ["What time do you have to get up tomorrow?", "Did you have to cook lunch yesterday?",
                        "What time do you have to arrive at work?", "Did you have to wear a uniform at school?",
                        "What don't you have to do on weekends?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula23-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b3-aula23-reading"] = [
    (FS, "Social media manners. Good manners are important online, too! Here are some tips.", 600),
    (FS, "You have to be careful with personal information. Your address and your phone number are private.", 600),
    (FS, "You mustn't post a private message or conversation without permission. That's very rude!", 600),
    (FS, "You don't have to answer every comment. It's OK to ignore some people.", 600),
    (FS, "You don't have to post all the details of your breakup with a partner. Some things are better offline.", 600),
    (FS, "And you must think before you post. Remember: the internet never forgets!", 300),
]
SCRIPTS["b3-aula24-words"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I'd like to ride a horse.", "Would you like to go surfing?", "She wouldn't like to get a tattoo.",
                     "We'd like to learn Spanish.", "Yes, I would."])]
SCRIPTS["b3-aula24-lists"] = [
    (FS, "Rafa, do you have a bucket list?", 300),
    (MJ, "Of course! I'd like to go to New York and get in a yellow taxi, like in the movies!", 400),
    (FS, "Ha ha, that's easy! I'd like to go to Japan in spring and see the cherry blossoms.", 400),
    (MJ, "Beautiful. Would you like to go bungee jumping? It's on my list.", 300),
    (FS, "No, I wouldn't! I'm afraid of heights. But I'd like to learn to ride a horse.", 400),
    (MJ, "Nice. And I'd really like to cook a traditional recipe from every country I visit.", 400),
    (FS, "Then I'd like to visit you and try them all!", 300),
]
for _p, _list in {"s": ["would, wouldn't.", "I'd, you'd, he'd, she'd, it'd, we'd, they'd.",
                        "I have so many things on my bucket list yet to do.", "I would really like to go bungee jumping.",
                        "I wouldn't like to go on a cruise.", "One of my dreams is to visit Paris."],
                  "y": ["Would you like to visit Antarctica?", "Would you like to climb Mount Everest?",
                        "Would you like to fly first class?", "Would you like to go surfing?", "Would you like to become famous?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula24-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b3-aula24-reading"] = [
    (FS, "Grandpa's bucket list.", 800),
    (FS, "My grandpa Jorge is seventy-five, and last year he made a bucket list. He says: I'm not going to kick the "
         "bucket before I do all these things!", 600),
    (FS, "The first thing on his list was: go on a hot-air balloon. In March, we went together. He loved it. "
         "I was a little scared!", 600),
    (FS, "Now he would like to learn a new language. He chose Italian, because his parents were from Italy. "
         "He'd also like to visit their village there.", 600),
    (FS, "He wouldn't like to go bungee jumping. I'm old, not crazy! But he'd really like to run a five-kilometer "
         "race. He walks every morning to practice.", 600),
    (FS, "The last item on his list? Make a dream come true for my granddaughter. I think I'd like to go to Italy with him!", 300),
]
SCRIPTS["b3-aula25-words"] = [(FS, "Listen and choose what you hear.", 1200)] + [
    (FS, f"Number {n}. [[slnc 500]] {w} [[slnc 1500]] {w}", 2400)
    for n, w in zip(["one", "two", "three", "four", "five"],
                    ["I'd like a room, please.", "Would you like some tea?", "I want to go home.",
                     "She wouldn't like to sleep in a tent.", "They'd like to see the pyramids."])]
SCRIPTS["b3-aula25-hotel"] = [
    (MJ, "Good evening! Welcome to the Ocean Hotel. How can I help you?", 300),
    (FS, "Good evening. We'd like a room for two, please. With a sea view, if possible.", 400),
    (MJ, "Of course. How many nights would you like to stay?", 300),
    (FS, "Three nights, please.", 400),
    (MJ, "Perfect. Would you like anything to drink while you wait?", 300),
    (FS, "Yes, please. I'd like a glass of orange juice, and my husband would like a coffee.", 400),
    (MJ, "Certainly. Would you like breakfast in your room?", 300),
    (FS, "No, thank you. We'd like to have breakfast in the restaurant. And tomorrow, we'd like to go on a boat tour. "
         "Is that possible?", 400),
    (MJ, "Yes! I can book it for you.", 300),
]
for _p, _list in {"s": ["I would like to visit Japan.", "I'd like to travel to New Zealand. It looks incredible.",
                        "I wouldn't like to go bungee jumping.", "What would she like to do next year?",
                        "Would you like to dance?", "Would you like anything to drink?", "I'd like a glass of wine, please.",
                        "I'd like some water, please."],
                  "y": ["Would you like to surf?", "Would you like to visit Paris?", "Would you like to eat insects?",
                        "What would you like to do if you had one free year?", "Would you like anything to drink?"]}.items():
    for _i, _t in enumerate(_list, 1):
        SCRIPTS[f"b3-aula25-say-{_p}{_i}"] = [(FS, _t, 300)]
SCRIPTS["b3-aula25-reading"] = [
    (FS, "My gap year.", 800),
    (FS, "Next year, I'm taking a gap year: one free year before university! So, what would I like to do?", 600),
    (FS, "First, I'd like to travel to New Zealand. It looks incredible! I'd also like to see the pyramids in Egypt.", 600),
    (FS, "My best friend, Duda, would like to come with me, but she wouldn't like to go to Egypt. She says it's too hot!", 600),
    (FS, "I'd really like to learn to surf, and I want to improve my English, so I'd like to work in a café in Australia.", 600),
    (FS, "My parents asked: Would you like to stay with your aunt in Sydney? Yes, I would! It's cheaper than a hotel.", 600),
    (FS, "One thing I wouldn't like to do: sleep in a tent. I prefer a comfortable bed!", 300),
]

def wav_for(voice, text, path):
    if USE_SAY:
        aiff = path + ".aiff"
        subprocess.run(["say", "-v", voice, "-r", RATE, "-o", aiff, text], check=True)
        subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@22050", "-c", "1", aiff, path], check=True)
        os.remove(aiff)
        return
    # ElevenLabs: one request per line (or per speed change), so the voice keeps the same tone and the English context.
    # [[slnc ms]] becomes a <break/> inside the request; spelled letters get an exact American pronunciation tag (tts.letter).
    text = re.sub(r"\[\[char LTRL\]\](.+?)\[\[char NORM\]\]", lambda m: tts.letter(m.group(1)), text)
    pcm, speed = b"", None
    for k, chunk in enumerate(re.split(r"\[\[rate (\d+)\]\]", text)):
        if k % 2:
            # words per minute (135 = normal) -> ElevenLabs speed, e.g. slow then natural speed in dictations
            speed = max(0.7, min(1.15, 0.9 * int(chunk) / int(RATE)))
            continue
        lead = re.match(r"^\s*\[\[slnc (\d+)\]\]", chunk)
        if lead:
            pcm += b"\0\0" * int(22050 * int(lead.group(1)) / 1000)
            chunk = chunk[lead.end():]
        trail = re.search(r"\[\[slnc (\d+)\]\]\s*$", chunk)
        if trail:
            chunk = chunk[:trail.start()]
        chunk = re.sub(r"\[\[slnc (\d+)\]\]", lambda m: _breaks(int(m.group(1))), chunk).strip(" ,")
        if re.sub(r"<[^>]+>|[\s.,!?]", "", chunk):
            part = f"{path}.{k}.wav"
            tts.speak(ROLE[voice], chunk, part, rate=22050, speed=speed)
            with wave.open(part) as w:
                pcm += w.readframes(w.getnframes())
            os.remove(part)
        if trail:
            pcm += b"\0\0" * int(22050 * int(trail.group(1)) / 1000)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(22050); w.writeframes(pcm)


def build(name, lines, outdir):
    tmp = tempfile.mkdtemp()
    frames, params = [], None
    for i, (voice, text, pause) in enumerate(lines):
        p = os.path.join(tmp, f"{i}.wav")
        wav_for(voice, text, p)
        with wave.open(p) as w:
            params = w.getparams()
            frames.append(w.readframes(w.getnframes()))
        frames.append(b"\0\0" * int(22050 * pause / 1000))
    joined = os.path.join(tmp, "all.wav")
    with wave.open(joined, "wb") as w:
        w.setparams(params)
        w.writeframes(b"".join(frames))
    out = os.path.join(outdir, (name[3:] if name[:3] in ("b2-", "b3-") else name) + ".m4a")  # b2-/b3- = Básico 2/3 (own folders)
    subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "64000", joined, out], check=True)
    secs = sum(len(f) for f in frames) / 2 / 22050
    print(f"{out}  {secs:.0f}s")


if __name__ == "__main__":
    outdir = sys.argv[1]
    only = [a for a in sys.argv[2:] if not a.startswith("--")]  # optional: names (or prefixes) to build; default = all
    os.makedirs(outdir, exist_ok=True)
    for name, lines in SCRIPTS.items():
        if not only or any(name.startswith(o) for o in only):
            build(name, lines, outdir)
