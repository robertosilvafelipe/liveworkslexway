"""Básico 2 public course page (/curso/basico-2): 6 activities per lesson + an interactive video extra.

Run on the server: python -m app.seed_basico_2  (creates or updates; ids and past attempts are kept).
Audios: app/static/audio/basico-2 (deploy/make_audio.py, scripts named b2-…); videos: app/static/video/basico-2.
Voices (user's choice for Básico 2): Sarah (female) and Jerry B. (male).
"""
import json
import os

from .public_seed import publish

SLUG = "basico-2"
AUDIO = f"/static/audio/{SLUG}"
VIDEO = f"/static/video/{SLUG}"


def video_item(name, prompt, translation, questions):
    """Interactive video item: question k pauses the video where scene k (with "stop") ends, per <name>.json."""
    meta = json.load(open(os.path.join(os.path.dirname(__file__), "static", "video", SLUG, name + ".json")))
    assert len(meta["stops"]) == len(questions), name
    return {"type": "video", "prompt": prompt, "translation": translation,
            "video": f"{VIDEO}/{name}.mp4", "subtitles": f"{VIDEO}/{name}.vtt", "poster": f"{VIDEO}/{name}.jpg",
            "stops": [dict(q, at=at) for q, at in zip(questions, meta["stops"])]}


def _video(n, topic, title, description, name, questions):
    return {"title": title, "lesson": n, "subject": "Video", "topic": topic,
            "description": "🎬 Atividade extra: " + description + " O vídeo pausa sozinho e faz uma pergunta; responda e continue "
                           "assistindo. Tente primeiro sem legenda!",
            "items": [video_item(name, "Watch the video. Answer the questions when it stops.",
                                 "Assista ao vídeo. Responda às perguntas quando ele pausar.", questions)]}


def _q(question, translation, *options):
    """First option is the right one (the seed shuffles them)."""
    return {"question": question, "translation": translation, "options": list(options), "correct": 0}


# ---------- Aula 01 — Can & Can't (https://youtu.be/g0b9-6IsXFM) ----------

AULA1_TOPIC = "Aula 01 — Can & Can't"

AULA1_FORMS = {
    "title": "Can & can't: abilities",
    "lesson": 1,
    "description": "CAN = saber / conseguir fazer algo (habilidade). CAN'T = não saber / não conseguir.\n"
                   "AFFIRMATIVE: sujeito + CAN + verbo na forma básica → I can swim. (Eu sei nadar.) · She can dance.\n"
                   "NEGATIVE: sujeito + CAN'T + verbo → I can't swim. · We can't speak English.\n"
                   "Igual para TODAS as pessoas: I can, you can, he can, she can… (sem S: \"she cans\" ✗)\n"
                   "Depois do can: verbo puro, sem TO e sem ING (\"can to swim\" ✗ · \"can swimming\" ✗).",
    "topic": AULA1_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the verbs to Portuguese.",
         "translation": "Ligue os verbos ao português.",
         "example": "swim → nadar",
         "pairs": [
             {"left": "dance", "right": "dançar"},
             {"left": "fly", "right": "voar"},
             {"left": "run", "right": "correr"},
             {"left": "sing", "right": "cantar"},
             {"left": "drive", "right": "dirigir"},
             {"left": "speak", "right": "falar"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta.",
         "example": "She [can dance]. (Ela sabe dançar.)",
         "text": "1. I [*can swim|can to swim|can swimming].\n"
                 "2. He [*can cook|cans cook|can cooks].\n"
                 "3. We [*can't speak|don't can speak|can't to speak] Chinese.\n"
                 "4. She [*can drive|can drives|cans drive].\n"
                 "5. They [*can't fly|can't flying|doesn't can fly]."},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza (can = saber fazer algo).",
         "example": "Eu sei nadar. → I can swim.",
         "text": "1. Ela sabe dançar. → [She can dance.]\n"
                 "2. Nós sabemos falar inglês. → [We can speak English.]\n"
                 "3. Eu não sei cozinhar. → [I can't cook.|I cannot cook.]\n"
                 "4. Ele não sabe dirigir. → [He can't drive.|He cannot drive.]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Can\" is the same for I, you, he, she… → True",
         "statements": [
             {"text": "We say \"She cans dance\".", "answer": False, "translation": "Dizemos \"She cans dance\"."},
             {"text": "After \"can\", the verb has no TO and no ING.", "answer": True,
              "translation": "Depois de \"can\", o verbo não tem TO nem ING."},
             {"text": "In negative sentences, we stress \"can't\".", "answer": True,
              "translation": "Nas frases negativas, enfatizamos o \"can't\"."},
             {"text": "In affirmative sentences, \"can\" is strong, and the verb is weak.", "answer": False,
              "translation": "Nas frases afirmativas, o \"can\" é forte e o verbo é fraco."},
         ]},
    ],
}

AULA1_QUESTIONS = {
    "title": "Can you swim?",
    "lesson": 1,
    "description": "QUESTION: comece com CAN → CAN + sujeito + verbo? → Can you swim? (Você sabe nadar?) · Can she dance?\n"
                   "SHORT ANSWERS: Yes, I can. / No, I can't. · Yes, she can. / No, she can't.\n"
                   "Responda com o MESMO sujeito da pergunta: Can THEY dance? → Yes, THEY can.\n"
                   "Wh-: What can you do? (O que você sabe fazer?) → I can sing and play the guitar.",
    "topic": AULA1_TOPIC,
    "items": [
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Você sabe nadar?)",
         "example": "she / Can / dance → Can she dance?",
         "tokens": ["Can", "you", "swim?"], "alternatives": []},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Nós sabemos falar inglês?)",
         "example": "he / Can / drive → Can he drive?",
         "tokens": ["Can", "we", "speak", "English?"], "alternatives": []},
        {"type": "dropdown",
         "prompt": "Choose the right short answer.",
         "translation": "Escolha a resposta curta certa (mesmo sujeito da pergunta).",
         "example": "Can you dance? (✓) → [Yes, I can.]",
         "text": "1. Can they dance? (✗) → [*No, they can't.|No, they don't.|No, I can't.]\n"
                 "2. Can she cook? (✓) → [*Yes, she can.|Yes, she does.|Yes, she cans.]\n"
                 "3. Can he drive? (✓) → [*Yes, he can.|Yes, he is.|Yes, I can.]\n"
                 "4. Can the baby speak? (✗) → [*No, he can't.|No, he doesn't.|No, he isn't.]"},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas.",
         "example": "Can you swim? → Yes, I can.",
         "pairs": [
             {"left": "Can your mother drive?", "right": "Yes, she can. She drives every day."},
             {"left": "Can birds fly?", "right": "Yes, they can."},
             {"left": "What can you do?", "right": "I can sing and play the guitar."},
             {"left": "Can your father cook?", "right": "No, he can't. He can only make coffee!"},
         ]},
        {"type": "fill",
         "prompt": "Write the questions.",
         "translation": "Escreva as perguntas em inglês.",
         "example": "Ela sabe dançar? → Can she dance?",
         "text": "1. Você sabe cozinhar? → [Can you cook?]\n2. Eles sabem nadar? → [Can they swim?]\n"
                 "3. O que você sabe fazer? → [What can you do?]"},
    ],
}

AULA1_LISTENING = {
    "title": "Listening — can or can't?",
    "lesson": 1,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica da aula: na afirmativa o CAN é rápido e fraco (\"kən\"); na negativa o CAN'T é forte (\"kænt\"), "
                   "e o T quase some.",
    "topic": AULA1_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Can or can't? Listen and choose.",
         "translation": "Can ou can't? Ouça e escolha.",
         "example": "Você ouve: \"They can't dance.\" → can't",
         "audio": f"{AUDIO}/aula1-cancant.m4a",
         "text": "1. She [*can|can't] cook.\n2. I [*can't|can] swim.\n3. He [*can|can't] drive.\n4. They [*can't|can] dance.\n"
                 "5. We [*can|can't] speak English.\n6. My father [*can't|can] sing."},
        {"type": "fill",
         "prompt": "Dictation: listen and write the verb.",
         "translation": "Ditado: ouça e escreva o verbo.",
         "example": "Você ouve: \"I can swim.\" → I can [swim].",
         "audio": f"{AUDIO}/aula1-dictation.m4a",
         "text": "1. She can [dance].\n2. Birds can [fly].\n3. I can't [sing].\n4. Can you [run] fast?\n5. He can [speak] French."},
        {"type": "info",
         "prompt": "Now listen to a job interview at a summer camp.",
         "translation": "Agora ouça uma entrevista de emprego num acampamento de férias para crianças. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula1-interview.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "The candidate's name is [Ben].",
         "text": "1. Can Ben swim? → [*Yes, he can.|No, he can't.|Yes, he does.]\n"
                 "2. Can he drive? → [*No, he can't.|Yes, he can.|No, he doesn't.]\n"
                 "3. What languages can he speak? → [*English and Spanish.|English and French.|Only English.]\n"
                 "4. What musical instrument can he play? → [*The guitar.|The piano.|The drums.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the interview.",
         "translation": "Verdadeiro ou falso? Responda de acordo com a entrevista.",
         "example": "Ben wants a job. → True",
         "statements": [
             {"text": "Ben can cook very well.", "answer": False, "translation": "O Ben sabe cozinhar muito bem."},
             {"text": "Ben can sing.", "answer": True, "translation": "O Ben sabe cantar."},
             {"text": "Ben gets the job.", "answer": True, "translation": "O Ben consegue o emprego."},
         ]},
    ],
}

AULA1_SPEAKING = {
    "title": "Speaking — what can you do?",
    "lesson": 1,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica da aula: fale a frase inteira, ligando as palavras (\"They can DANCE\"). "
                   "Na negativa, enfatize o CAN'T (\"They CAN'T dance\").",
    "topic": AULA1_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat: affirmative and negative.",
         "translation": "Ouça e repita: afirmativa (can fraco) e negativa (can't forte).",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula1-say-s{i}.m4a"} for i, t in enumerate(
             ["I can swim.", "I can't swim.", "She can dance.", "She can't cook.", "They can dance.", "They can't dance.",
              "We can speak English."], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the questions and answers.",
         "translation": "Ouça e repita as perguntas e as respostas.",
         "example": "\"Can you swim? Yes, I can.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula1-say-q{i}.m4a"} for i, t in enumerate(
             ["Can you swim? Yes, I can.", "Can she cook? No, she can't.", "Can he drive? Yes, he can.",
              "What can you do?"], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOU.",
         "translation": "Agora responda às perguntas sobre VOCÊ com uma frase completa.",
         "example": "\"Can you swim?\" → \"Yes, I can.\" / \"No, I can't.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula1-say-y{i}.m4a"} for i, t in enumerate(
             ["Can you swim?", "Can you cook?", "Can you drive?", "What can you do very well?"], 1)]},
    ],
}

AULA1_READING = {
    "title": "Reading — the talent show",
    "lesson": 1,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA1_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text about the school talent show.",
         "translation": "Leia e ouça o texto sobre o show de talentos da escola. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula1-reading.m4a",
         "text": "THE SCHOOL TALENT SHOW\n\n"
                 "Every year, our school has a talent show on the last Friday of June.\n"
                 "This year, Lucas is singing a Brazilian song. He can sing very well, but he can't dance!\n"
                 "Mia and her sister can dance ballet. They practice three times a week.\n"
                 "Tom is only seven, but he can play the piano. His teacher is very proud of him.\n"
                 "And our English teacher, Mrs. Carter? She can speak four languages: English, Spanish, French and Italian.\n"
                 "And me? I can't sing, and I can't dance... but I can take great photos!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "When is the talent show? → [On the last Friday of June.]",
         "text": "1. Can Lucas dance? → [*No, he can't.|Yes, he can.|No, he doesn't.]\n"
                 "2. What can Mia and her sister do? → [*They can dance ballet.|They can sing.|They can play the piano.]\n"
                 "3. How old is Tom? → [*Seven.|Ten.|Four.]\n"
                 "4. How many languages can Mrs. Carter speak? → [*Four.|Two.|Three.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Lucas can sing. → True",
         "statements": [
             {"text": "Tom can play the piano.", "answer": True, "translation": "O Tom sabe tocar piano."},
             {"text": "Mrs. Carter can speak German.", "answer": False, "translation": "A Sra. Carter sabe falar alemão."},
             {"text": "The writer can take great photos.", "answer": True,
              "translation": "A pessoa que escreve o texto sabe tirar ótimas fotos."},
         ]},
        {"type": "fill",
         "prompt": "Complete with can or can't, according to the text.",
         "translation": "Complete com can ou can't, de acordo com o texto.",
         "example": "Lucas [can] sing very well.",
         "text": "1. Lucas [can't|cannot] dance.\n2. Tom [can] play the piano.\n3. The writer [can't|cannot] sing."},
    ],
}

AULA1_WRITING = {
    "title": "Writing — my abilities",
    "lesson": 1,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ I can + verbo · I can't + verbo · Can you…? → Yes, I can. / No, I can't.",
    "topic": AULA1_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Correct the mistakes.",
         "translation": "Corrija os erros. Escreva a frase certa.",
         "example": "She cans swim. → She can swim.",
         "text": "1. He can to drive. → [He can drive.]\n2. I can cooking. → [I can cook.]\n"
                 "3. She don't can dance. → [She can't dance.|She cannot dance.]\n4. You can swim? → [Can you swim?]"},
        {"type": "fill",
         "prompt": "Write the short answers.",
         "translation": "Escreva as respostas curtas.",
         "example": "Can you swim? (✓) → Yes, I can.",
         "text": "1. Can your brother cook? (✗) → [No, he can't.|No, he cannot.]\n"
                 "2. Can your friends dance? (✓) → [Yes, they can.]"},
        {"type": "free",
         "prompt": "Write about your abilities and your family's abilities. What can you do? What can't you do?",
         "translation": "Escreva sobre as suas habilidades e as da sua família. O que vocês sabem fazer? O que não sabem?",
         "example": "I can cook, but I can't swim.",
         "model_answer": "I can cook very well, and I can speak a little English, but I can't swim.\n"
                         "My mother can sing, and she can play the guitar.\n"
                         "My brother can drive, but he can't cook!\n"
                         "My grandmother can't use a computer, but she can make wonderful cakes.",
         "keywords": ["I can", "I can't", "can"], "min_words": 30, "points": 4},
    ],
}

AULA1_VIDEO = _video(1, AULA1_TOPIC, "Video — What can they do?",
                     "pessoas e suas habilidades: o que elas sabem e não sabem fazer.",
                     "aula1-video", [
    _q("What can Maria do?", "O que a Maria sabe fazer?", "She can dance.", "She can fly.", "She can drive.",
       "She can't dance."),
    _q("Can Leo cook?", "O Leo sabe cozinhar?", "Yes, he can.", "No, he can't.", "Yes, he does.", "Yes, he cans."),
    _q("Can baby Theo speak?", "O bebê Theo sabe falar?", "No, he can't.", "Yes, he can.", "No, he doesn't.",
       "No, he isn't."),
    _q("What can Ana do?", "O que a Ana sabe fazer?", "She can swim very well.", "She can't swim.",
       "She can play the guitar.", "She can fly."),
    _q("Which sentence is correct?", "Qual frase está correta?", "Paulo can play the guitar.",
       "Paulo cans play the guitar.", "Paulo can plays the guitar.", "Paulo can to play the guitar."),
])


# ---------- Aula 02 — Was & Were (https://youtu.be/obsJByonPTw) ----------

AULA2_TOPIC = "Aula 02 — Was & Were"

AULA2_WASWERE = {
    "title": "Was & were",
    "lesson": 2,
    "description": "WAS / WERE = passado do verb to be (era / estava / foi).\n"
                   "AM e IS → WAS: I was · he was · she was · it was.   ARE → WERE: you were · we were · they were.\n"
                   "I was at home yesterday. (Eu estava em casa ontem.) · You were at school in the morning. · "
                   "She was very happy last night.\n"
                   "NEGATIVE: was not = WASN'T · were not = WEREN'T → I wasn't at home. · You weren't at school.\n"
                   "QUESTION: WAS / WERE antes do sujeito → Was she happy? → Yes, she was. / No, she wasn't. · "
                   "Were they at home? → Yes, they were. / No, they weren't.",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "Was or were? Put each subject in the right group.",
         "translation": "Was ou were? Coloque cada sujeito no grupo certo.",
         "example": "I → was · they → were",
         "categories": ["was", "were"],
         "words": [
             {"text": "I", "category": "was"}, {"text": "he", "category": "was"}, {"text": "she", "category": "was"},
             {"text": "it", "category": "was"}, {"text": "my mother", "category": "was"},
             {"text": "you", "category": "were"}, {"text": "we", "category": "were"}, {"text": "they", "category": "were"},
             {"text": "my friends", "category": "were"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose was or were.",
         "translation": "Escolha was ou were.",
         "example": "I [was] at home yesterday.",
         "text": "1. You [*were|was] at school in the morning.\n2. She [*was|were] very happy last night.\n"
                 "3. We [*were|was] at the beach on Sunday.\n4. Lisa [*was|were] tired yesterday.\n"
                 "5. My parents [*were|was] in Italy last year.\n6. It [*was|were] a beautiful day."},
        {"type": "fill",
         "prompt": "Make the sentences negative (use contractions).",
         "translation": "Passe as frases para a negativa (use contractions).",
         "example": "I was at home. → I wasn't at home.",
         "text": "1. She was happy. → [She wasn't happy.|She was not happy.]\n"
                 "2. They were at school. → [They weren't at school.|They were not at school.]\n"
                 "3. He was tired. → [He wasn't tired.|He was not tired.]"},
        {"type": "dropdown",
         "prompt": "Choose the right short answer.",
         "translation": "Escolha a resposta curta certa.",
         "example": "Was she happy? (✓) → [Yes, she was.]",
         "text": "1. Were they at home? (✗) → [*No, they weren't.|No, they wasn't.|No, they didn't.]\n"
                 "2. Was he at work yesterday? (✓) → [*Yes, he was.|Yes, he were.|Yes, he is.]\n"
                 "3. Were you tired last night? (✓) → [*Yes, I was.|Yes, I were.|Yes, I am.]\n"
                 "4. Was it cold? (✗) → [*No, it wasn't.|No, it weren't.|No, it isn't.]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Was\" is the past of \"am\" and \"is\". → True",
         "statements": [
             {"text": "\"Were\" is the past of \"are\".", "answer": True, "translation": "\"Were\" é o passado de \"are\"."},
             {"text": "We say \"I were at home\".", "answer": False, "translation": "Dizemos \"I were at home\"."},
             {"text": "\"Wasn't\" = was not.", "answer": True, "translation": "\"Wasn't\" = was not."},
             {"text": "In questions, \"was\" or \"were\" comes after the subject.", "answer": False,
              "translation": "Nas perguntas, \"was\" ou \"were\" vem depois do sujeito."},
         ]},
    ],
}

AULA2_THEREWAS = {
    "title": "There was / There were",
    "lesson": 2,
    "description": "Presente → THERE IS (singular) / THERE ARE (plural) = tem, existe.\n"
                   "Passado → THERE WAS (singular) / THERE WERE (plural) = tinha, havia.\n"
                   "There was a person at the door. (Tinha uma pessoa na porta.) · There were some people at the door.\n"
                   "Negative: there wasn't / there weren't. Question: Was there…? / Were there…? → Yes, there was. / No, there weren't.\n"
                   "Lembre: nada de have para \"tem / tinha\" no sentido de existir! · singular → a / an · plural → some, many ou um número.",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "There was or there were?",
         "translation": "There was (singular) ou there were (plural)?",
         "example": "[There was] a person at the door.",
         "text": "1. [*There were|There was] some people at the door.\n2. [*There was|There were] a TV in the living room.\n"
                 "3. [*There were|There was] three cushions on the sofa.\n4. [*There was|There were] an armchair next to the window.\n"
                 "5. [*There were|There was] many books on the table."},
        {"type": "dropdown",
         "prompt": "Present or past? Before and after the renovation.",
         "translation": "Presente ou passado? A sala antes (before) e depois (after) da reforma.",
         "example": "Before: [There was] a TV. → After: [There isn't] a TV.",
         "text": "1. Before: [*There was|There is] an orange cushion.\n"
                 "2. After: [*There are|There were] three pink cushions on the sofa.\n"
                 "3. Before: [*There wasn't|There isn't] a picture on the wall.\n"
                 "4. After: [*There is|There was] a picture on the wall."},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Tinha um espelho no quarto?)",
         "example": "there / Was / a TV → Was there a TV?",
         "tokens": ["Was", "there", "a", "mirror", "in", "the", "bedroom?"], "alternatives": []},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Tinha uma pessoa na porta. → There was a person at the door.",
         "text": "1. Tinha algumas plantas na sala. → [There were some plants in the living room.]\n"
                 "2. Não tinha uma TV no quarto. → [There wasn't a TV in the bedroom.|There was not a TV in the bedroom.]\n"
                 "3. Tinha um chapéu na cama? → [Was there a hat on the bed?]"},
        {"type": "choice",
         "prompt": "Which sentence is correct?",
         "translation": "Qual frase está correta?",
         "example": "There isn't a chair in my bedroom. ✓",
         "options": ["There wasn't a chair in my bedroom.", "There wasn't chair in my bedroom.",
                     "There weren't a chair in my bedroom.", "It didn't have a chair in my bedroom."],
         "correct": 0},
    ],
}

AULA2_LISTENING = {
    "title": "Listening — where were you?",
    "lesson": 2,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Pronúncia: WAS = \"uóz\" (fraco: \"uəz\") · WERE = \"uâr\" (enrole a língua no R).",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"I was at home.\" → was",
         "audio": f"{AUDIO}/aula2-forms.m4a",
         "text": "1. She [*was|wasn't] happy.\n2. They [*weren't|were] at school.\n3. We [*were|weren't] tired.\n"
                 "4. [*There were|There was] some people at the door.\n5. He [*wasn't|was] at work."},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"I was at home yesterday.\" → I [was] at home yesterday.",
         "audio": f"{AUDIO}/aula2-dictation.m4a",
         "text": "1. You [were] at school in the morning.\n2. She [wasn't] very happy last night.\n"
                 "3. [Were] they at home?\n4. There [was] a person at the door."},
        {"type": "info",
         "prompt": "Now listen: Kate calls her friend Sam on Sunday.",
         "translation": "Agora ouça: no domingo, a Kate liga para o amigo dela, o Sam, e pergunta sobre a noite de sábado. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula2-party.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Kate calls [Sam].",
         "text": "1. Where was Kate last night? → [*At home.|At the party.|At work.]\n"
                 "2. Why was she at home? → [*Because she was sick.|Because she was sad.|Because it was cold.]\n"
                 "3. Where was the party? → [*At Mark's house.|At a restaurant.|At the beach.]\n"
                 "4. How many people were there? → [*About thirty.|About ten.|About a hundred.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "There was a party on Saturday. → True",
         "statements": [
             {"text": "The music was great.", "answer": True, "translation": "A música estava ótima."},
             {"text": "There was a big cake.", "answer": False, "translation": "Tinha um bolo grande."},
             {"text": "Sam was tired on Sunday.", "answer": True, "translation": "O Sam estava cansado no domingo."},
         ]},
    ],
}

AULA2_SPEAKING = {
    "title": "Speaking — was & were",
    "lesson": 2,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: WAS = \"uóz\" · WERE = \"uâr\" · WASN'T = \"uózent\" · WEREN'T = \"uârent\".",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula2-say-s{i}.m4a"} for i, t in enumerate(
             ["I was at home yesterday.", "You were at school in the morning.", "She was very happy last night.",
              "I wasn't at home yesterday.", "They weren't at school.", "There was a person at the door.",
              "There were some people at the door."], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the questions and answers.",
         "translation": "Ouça e repita as perguntas e as respostas.",
         "example": "\"Was she happy? Yes, she was.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula2-say-q{i}.m4a"} for i, t in enumerate(
             ["Was she happy? Yes, she was.", "Were they at home? No, they weren't.", "Was there a mirror? Yes, there was.",
              "Were there plants? Yes, there were."], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOU.",
         "translation": "Agora responda às perguntas sobre VOCÊ com uma frase completa.",
         "example": "\"Where were you yesterday at 8 p.m.?\" → \"I was at home.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula2-say-y{i}.m4a"} for i, t in enumerate(
             ["Where were you yesterday at 8 p.m.?", "Were you tired last night?", "Was there a TV in your bedroom "
              "when you were a child?", "Where were you last Sunday?"], 1)]},
    ],
}

AULA2_READING = {
    "title": "Reading — Grandma's old house",
    "lesson": 2,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Rita's text.",
         "translation": "Leia e ouça o texto da Rita sobre a casa da avó. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula2-reading.m4a",
         "text": "GRANDMA'S OLD HOUSE\n\n"
                 "When I was a child, my favorite place was my grandmother's house in Minas Gerais.\n"
                 "It was a big old house. There were five bedrooms and a very big kitchen.\n"
                 "In the kitchen, there was an old stove, and there were always cakes on the table!\n"
                 "There wasn't a TV in the living room, but there were a lot of books and an old radio.\n"
                 "In the garden, there were many trees and some chickens.\n"
                 "My cousins and I were very happy there. Grandma's house was the best place in the world!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Where was the house? → [In Minas Gerais.]",
         "text": "1. How many bedrooms were there? → [*Five.|Three.|Two.]\n"
                 "2. Was there a TV in the living room? → [*No, there wasn't.|Yes, there was.|No, there weren't.]\n"
                 "3. What was there in the living room? → [*A lot of books and an old radio.|A TV and a sofa.|Some chickens.]\n"
                 "4. Were the cousins happy there? → [*Yes, they were.|No, they weren't.|Yes, they was.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "The house was big. → True",
         "statements": [
             {"text": "The kitchen was small.", "answer": False, "translation": "A cozinha era pequena."},
             {"text": "There were chickens in the garden.", "answer": True, "translation": "Tinha galinhas no jardim."},
             {"text": "There was an old stove in the kitchen.", "answer": True, "translation": "Tinha um fogão velho na cozinha."},
         ]},
        {"type": "fill",
         "prompt": "Complete with was, were, wasn't or weren't.",
         "translation": "Complete com was, were, wasn't ou weren't, de acordo com o texto.",
         "example": "It [was] a big old house.",
         "text": "1. There [were] five bedrooms.\n2. There [wasn't|was not] a TV in the living room.\n"
                 "3. My cousins and I [were] very happy there."},
    ],
}

AULA2_WRITING = {
    "title": "Writing — my childhood home",
    "lesson": 2,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ I was / we were… · There was a… / There were some… / There wasn't a… / There weren't any…",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Rewrite the sentences in the past.",
         "translation": "Reescreva as frases no passado.",
         "example": "I am at home. → I was at home.",
         "text": "1. They are at school. → [They were at school.]\n2. There is a lamp in the bedroom. → [There was a lamp in the bedroom.]\n"
                 "3. There are many books. → [There were many books.]\n4. She isn't tired. → [She wasn't tired.|She was not tired.]"},
        {"type": "fill",
         "prompt": "Write the questions.",
         "translation": "Escreva as perguntas em inglês.",
         "example": "Ela estava feliz? → Was she happy?",
         "text": "1. Você estava em casa ontem? → [Were you at home yesterday?]\n"
                 "2. Tinha plantas no quarto? → [Were there plants in the bedroom?|Were there any plants in the bedroom?]"},
        {"type": "free",
         "prompt": "Describe the house where you lived as a child. How was it? What was there? What wasn't there?",
         "translation": "Descreva a casa onde você morava quando era criança. Como ela era? O que tinha? O que não tinha?",
         "example": "When I was a child, my house was small. There were two bedrooms.",
         "model_answer": "When I was a child, my house was small, but it was very nice.\n"
                         "There were two bedrooms, a living room and a small kitchen.\n"
                         "There was a big tree in the garden, and there were some flowers.\n"
                         "There wasn't a computer, but there was a radio. I was very happy there.",
         "keywords": ["was", "there was", "there were"], "min_words": 30, "points": 4},
    ],
}

AULA2_VIDEO = _video(2, AULA2_TOPIC, "Video — Last summer at Grandma's",
                     "a Bia olha fotos antigas e lembra do verão na fazenda da avó: was, were, there was, there were.",
                     "aula2-video", [
    _q("Where were Bia and her brother last summer?", "Onde a Bia e o irmão estavam no verão passado?",
       "At their grandmother's farm.", "At school.", "At the beach.", "In a hotel."),
    _q("What was there in Grandma's kitchen?", "O que tinha na cozinha da avó?", "An old stove and a lot of cakes.",
       "A big TV.", "Many chickens.", "A new oven."),
    _q("Was there a dog on the farm?", "Tinha um cachorro na fazenda?", "No, there wasn't.", "Yes, there was.",
       "No, there weren't.", "Yes, there were."),
    _q("What was there in the living room?", "O que tinha na sala?", "An old record player.", "A TV.", "A computer.",
       "Some chickens."),
    _q("Which sentence is correct?", "Qual frase está correta?", "There were many chickens in the garden.",
       "There was many chickens in the garden.", "There were many chicken in the garden.",
       "It had many chickens in the garden."),
])


# ---------- Aula 03 — Prepositions of Place (https://youtu.be/kszNpewvxtc) ----------

AULA3_TOPIC = "Aula 03 — Prepositions of Place"

AULA3_PREPS = {
    "title": "Prepositions of place: where is the cat?",
    "lesson": 3,
    "description": "IN = dentro · ON = em cima / no, na (encostando) · UNDER = embaixo · BETWEEN = entre, no meio · "
                   "NEXT TO = ao lado · BEHIND = atrás · IN FRONT OF = na frente · ACROSS FROM = de frente para "
                   "(face a face, geralmente com algo no meio) · ABOVE / OVER = acima (sem encostar).\n"
                   "ON × ABOVE / OVER: com ON tem contato (My mouse is on my hand.); com ABOVE / OVER não tem contato.\n"
                   "The cat is in the box. · The cat is on the sofa. · The cat is under the chair. · "
                   "The cat is between the dogs. · The cat is next to the clock.",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the sentences to Portuguese.",
         "translation": "Ligue as frases ao português.",
         "example": "The cat is in the box. → O gato está dentro da caixa.",
         "pairs": [
             {"left": "The cat is under the chair.", "right": "O gato está embaixo da cadeira."},
             {"left": "The cat is between the dogs.", "right": "O gato está entre os cachorros."},
             {"left": "The cat is behind the wall.", "right": "O gato está atrás da parede."},
             {"left": "The cat is in front of the computer.", "right": "O gato está na frente do computador."},
             {"left": "The cat is across from the dog.", "right": "O gato está de frente para o cachorro."},
             {"left": "The cat is over the box.", "right": "O gato está acima da caixa (sem encostar)."},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the right preposition.",
         "translation": "Escolha a preposição certa (a dica em português está entre parênteses).",
         "example": "The cat is [in] the box. (dentro da)",
         "text": "1. The cat is [*on|in|under] the sofa. (em cima do)\n"
                 "2. The ball is [*next to|between|behind] the box. (ao lado da)\n"
                 "3. My shoes are [*under|on|over] the bed. (embaixo da)\n"
                 "4. The cat is [*between|next to|across from] the dogs. (no meio dos)\n"
                 "5. The car is [*in front of|across from|behind] the house. (na frente da)"},
        {"type": "dropdown",
         "prompt": "On or above / over? Is there contact?",
         "translation": "On ou above / over? Tem contato (encosta) ou não?",
         "example": "The bird is [above] the tree. (não encosta na árvore)",
         "text": "1. My mouse is [*on|over] my hand. (encosta)\n"
                 "2. The plane is [*above|on] the city. (não encosta)\n"
                 "3. The lamp is [*over|on] the table. (não encosta)\n"
                 "4. The cup is [*on|above] the table. (encosta)"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Under\" = embaixo. → True",
         "statements": [
             {"text": "We use \"on\" when there is contact.", "answer": True,
              "translation": "Usamos \"on\" quando tem contato."},
             {"text": "\"Above\" and \"over\" mean the same as \"on\".", "answer": False,
              "translation": "\"Above\" e \"over\" significam a mesma coisa que \"on\"."},
             {"text": "\"Next to\" = ao lado.", "answer": True, "translation": "\"Next to\" = ao lado."},
             {"text": "\"In front of\" and \"across from\" are the same.", "answer": False,
              "translation": "\"In front of\" e \"across from\" são a mesma coisa."},
         ]},
    ],
}

AULA3_WHERE = {
    "title": "Where is it? Where was it?",
    "lesson": 3,
    "description": "Estrutura da aula: THE + substantivo + IS / ARE + preposição + THE + substantivo.\n"
                   "Where is the dog? → The dog is on the bed. · Where is the ball? → The ball is in the box.\n"
                   "Singular → IS (It's…) · plural → ARE (They're…): The ball is between the boxes. · The keys are on the table.\n"
                   "No passado (Aula 02) → WAS / WERE: Where was the cat? → It was behind the curtains. · "
                   "Where were my keys? → They were under the bed.",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras em ordem. (A bola está entre as caixas.)",
         "example": "is / the / in / box / The / cat → The cat is in the box.",
         "tokens": ["The", "ball", "is", "between", "the", "boxes."], "alternatives": []},
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras em ordem. (Os livros estavam ao lado da TV.)",
         "example": "were / bed / under / The / the / shoes → The shoes were under the bed.",
         "tokens": ["The", "books", "were", "next", "to", "the", "TV."], "alternatives": []},
        {"type": "dropdown",
         "prompt": "Choose is, are, was or were.",
         "translation": "Escolha is, are (presente) ou was, were (passado).",
         "example": "The ball [is] in the box.",
         "text": "1. The keys [*are|is] under the bed.\n2. My phone [*is|are] on the table.\n"
                 "3. Yesterday, the children [*were|was] in the garden.\n4. Last night, my glasses [*were|was] next to the TV.\n"
                 "5. Where [*is|are] the cat?\n6. Where [*were|was] you this morning?"},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas.",
         "example": "Where is the dog? → It's on the bed.",
         "pairs": [
             {"left": "Where is the ball?", "right": "It's under the box."},
             {"left": "Where are my shoes?", "right": "They're next to the door."},
             {"left": "Where was the cat?", "right": "It was behind the curtains."},
             {"left": "Where were the books?", "right": "They were on the shelf."},
         ]},
        {"type": "choice",
         "prompt": "Which sentence is correct?",
         "translation": "Qual frase está correta?",
         "example": "The ball is next to the box. ✓",
         "options": ["The cat is in front of the computer.", "The cat is in front the computer.",
                     "The cat is front of the computer.", "The cat is in the front of computer."],
         "correct": 0},
    ],
}

AULA3_LISTENING = {
    "title": "Listening — moving day",
    "lesson": 3,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Atenção às preposições com mais de uma palavra: NEXT TO · IN FRONT OF · ACROSS FROM.",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the preposition.",
         "translation": "Ouça e escolha a preposição.",
         "example": "Você ouve: \"The cat is in the box.\" → in",
         "audio": f"{AUDIO}/aula3-preps.m4a",
         "text": "1. The keys are [*under|on|in] the bed.\n2. The cat is [*behind|next to|in front of] the door.\n"
                 "3. My phone is [*next to|in|on] the computer.\n4. The bank is [*across from|next to|behind] the supermarket.\n"
                 "5. The lamp is [*above|on|under] the table.\n6. The ball is [*between|behind|under] the boxes."},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"The dog is on the bed.\" → The dog is [on] the bed.",
         "audio": f"{AUDIO}/aula3-dictation.m4a",
         "text": "1. The cat is [in] the box.\n2. The books are [on] the shelf.\n"
                 "3. The ball is [in front of] the box.\n4. My glasses [were] under the sofa."},
        {"type": "info",
         "prompt": "Now listen: Tom helps his friend Anna in her new apartment.",
         "translation": "Agora ouça: o Tom ajuda a amiga dele, a Anna, a arrumar a sala do apartamento novo dela. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula3-moving.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Tom helps Anna in her new [apartment].",
         "text": "1. Where is the sofa? → [*In front of the TV.|Behind the TV.|Next to the window.]\n"
                 "2. Where are the plants? → [*Between the windows.|On the balcony.|Under the table.]\n"
                 "3. Where were the plants in Anna's old apartment? → [*On the balcony.|In the kitchen.|Between the windows.]\n"
                 "4. Where is the picture? → [*On the wall, above the bookcase.|Behind the door.|Over the sofa.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Anna has a new apartment. → True",
         "statements": [
             {"text": "The lamp is next to the sofa.", "answer": True, "translation": "O abajur está ao lado do sofá."},
             {"text": "The box of books is on the table.", "answer": False,
              "translation": "A caixa de livros está em cima da mesa."},
             {"text": "Tom's pizza is in the kitchen.", "answer": True, "translation": "A pizza do Tom está na cozinha."},
         ]},
    ],
}

AULA3_SPEAKING = {
    "title": "Speaking — where is the ball?",
    "lesson": 3,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica da aula: pause, repita umas três vezes e preste atenção na pronúncia de "
                   "between, behind, in front of e across from.",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula3-say-s{i}.m4a"} for i, t in enumerate(
             ["The ball is in the box.", "The ball is on the box.", "The ball is in front of the box.",
              "The ball is under the box.", "The ball is between the boxes.", "The ball is behind the box.",
              "The ball is next to the box.", "The ball is above the box."], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the questions and answers.",
         "translation": "Ouça e repita as perguntas e as respostas.",
         "example": "\"Where is the cat? It's under the chair.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula3-say-q{i}.m4a"} for i, t in enumerate(
             ["Where is the cat? It's under the chair.", "Where are my keys? They're on the table.",
              "Where was the dog? It was behind the sofa.", "Where were the children? They were in the garden."], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOU.",
         "translation": "Agora responda às perguntas sobre VOCÊ com uma frase completa.",
         "example": "\"What is on your desk or table now?\" → \"My phone and a cup of coffee are on my table.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula3-say-y{i}.m4a"} for i, t in enumerate(
             ["What is on your desk or table now?", "What is in front of your house or building?",
              "Where was your bed when you were a child?", "What was next to your bed?"], 1)]},
    ],
}

AULA3_READING = {
    "title": "Reading — where is Mimi?",
    "lesson": 3,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Paula's text.",
         "translation": "Leia e ouça o texto da Paula sobre a gata dela, a Mimi. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula3-reading.m4a",
         "text": "WHERE IS MIMI?\n\n"
                 "My name is Paula, and Mimi is my cat. She is small and white, and she loves boxes.\n"
                 "Last night, Mimi wasn't in her bed, and my family and I were very worried. Where was she?\n"
                 "She wasn't under the sofa. She wasn't behind the curtains. She wasn't in the kitchen.\n"
                 "My brother was in the garden with a flashlight, but she wasn't there.\n"
                 "Then there was a small noise in my bedroom. There was a big box next to my wardrobe.\n"
                 "And guess what? Mimi was in the box! She was asleep between two old sweaters.\n"
                 "Today, her bed is in my bedroom, next to my bed. And the box? It's on the wardrobe now, "
                 "and Mimi can't sleep in it!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Mimi is Paula's [cat].",
         "text": "1. Where was Paula's brother? → [*In the garden.|In the kitchen.|In the bedroom.]\n"
                 "2. Where was the big box? → [*Next to the wardrobe.|Under the bed.|In the kitchen.]\n"
                 "3. Where was Mimi? → [*In the box.|Behind the curtains.|Under the sofa.]\n"
                 "4. Where is Mimi's bed today? → [*Next to Paula's bed.|In the kitchen.|On the wardrobe.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Mimi is small and white. → True",
         "statements": [
             {"text": "Mimi was under the sofa.", "answer": False, "translation": "A Mimi estava embaixo do sofá."},
             {"text": "Mimi was asleep between two old sweaters.", "answer": True,
              "translation": "A Mimi estava dormindo entre dois suéteres velhos."},
             {"text": "The box is on the wardrobe now.", "answer": True,
              "translation": "A caixa está em cima do guarda-roupa agora."},
         ]},
        {"type": "fill",
         "prompt": "Complete with the preposition from the text.",
         "translation": "Complete com a preposição do texto.",
         "example": "Mimi wasn't [in] her bed.",
         "text": "1. She wasn't [behind] the curtains.\n2. There was a big box [next to] my wardrobe.\n"
                 "3. She was asleep [between] two old sweaters."},
    ],
}

AULA3_WRITING = {
    "title": "Writing — my childhood bedroom",
    "lesson": 3,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ The … is / are + preposição + the … · No passado: The … was / were … · "
                   "There was a… / There were some…",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the sentences in English.",
         "translation": "Escreva as frases em inglês.",
         "example": "A bola está dentro da caixa. → The ball is in the box.",
         "text": "1. O gato está atrás da parede. → [The cat is behind the wall.]\n"
                 "2. Os livros estão em cima da mesa. → [The books are on the table.]\n"
                 "3. O banco fica de frente para o supermercado. → [The bank is across from the supermarket.]\n"
                 "4. As minhas chaves estavam embaixo da cama. → [My keys were under the bed.]"},
        {"type": "fill",
         "prompt": "Write the questions.",
         "translation": "Escreva as perguntas em inglês.",
         "example": "Onde está a bola? → Where is the ball?",
         "text": "1. Onde está o meu celular? → [Where is my phone?|Where's my phone?|Where is my cell phone?|"
                 "Where's my cell phone?]\n"
                 "2. Onde estavam as crianças? → [Where were the children?|Where were the kids?]"},
        {"type": "free",
         "prompt": "Describe your bedroom when you were a child. What was there, and where was it? Use at least 4 prepositions.",
         "translation": "Descreva o seu quarto quando você era criança. O que tinha e onde ficava cada coisa? "
                        "Use pelo menos 4 preposições.",
         "example": "When I was a child, my bed was next to the window.",
         "model_answer": "When I was a child, my bedroom was small, but I loved it.\n"
                         "My bed was next to the window, and there was a lamp on a small table between the bed and the door.\n"
                         "There was a big picture of a cat above my bed.\n"
                         "My toys were in a box under the bed, and my books were on a shelf behind the door.",
         "keywords": ["there was", "on", "next to"], "min_words": 30, "points": 4},
    ],
}

AULA3_VIDEO = _video(3, AULA3_TOPIC, "Video — Where are the cats?",
                     "a Lily mostra vários gatos em lugares diferentes: in, on, behind, next to, in front of.",
                     "aula3-video", [
    _q("Where is the orange cat?", "Onde está o gato laranja?", "In a box.", "On a box.", "Under a box.", "Behind a box."),
    _q("Where is the little kitten?", "Onde está o gatinho?", "On the sofa.", "Under the sofa.", "Behind the sofa.",
       "Next to the sofa."),
    _q("Where is the white cat?", "Onde está o gato branco?", "Behind the window.", "In front of the TV.",
       "Under the window.", "On the bed."),
    _q("Where is the cat?", "Onde está o gato?", "Next to the dog.", "Behind the dog.", "On the dog.", "Between the dogs."),
    _q("Where is the little white kitten?", "Onde está o gatinho branco?", "In front of the big cats.",
       "Behind the big cats.", "Between the big cats.", "Under the big cats."),
    _q("Why can't Lily work today?", "Por que a Lily não consegue trabalhar hoje?", "Because the cat is on her keyboard.",
       "Because the cat is under the table.", "Because she's very tired.", "Because her computer is in a box."),
])


# ---------- Aula 04 — Past Simple: regular and irregular verbs (https://youtu.be/Ri6rnMFqH9w) ----------

AULA4_TOPIC = "Aula 04 — Past Simple (regular & irregular)"

AULA4_REGULAR = {
    "title": "Past simple: regular verbs",
    "lesson": 4,
    "description": "TIME EXPRESSIONS (passado): yesterday (ontem) · last week / last month / last Sunday (semana / mês / domingo passado) · "
                   "in 2019 · when I was a kid (quando eu era criança) · before class · a week ago (há uma semana) · "
                   "a long time ago (há muito tempo).\n"
                   "REGULAR VERBS → + ED: watch → watched · cook → cooked · work → worked.\n"
                   "Termina em E → só + D: dance → danced · explore → explored.\n"
                   "1 sílaba, consoante + vogal + consoante → dobra: stop → stopped.\n"
                   "Consoante + Y → IED: study → studied. (Vogal + Y → só ED: enjoy → enjoyed, play → played.)",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the time expressions to Portuguese.",
         "translation": "Ligue as expressões de tempo ao português.",
         "example": "yesterday → ontem",
         "pairs": [
             {"left": "last week", "right": "semana passada"},
             {"left": "last month", "right": "mês passado"},
             {"left": "a week ago", "right": "há uma semana"},
             {"left": "a long time ago", "right": "há muito tempo"},
             {"left": "when I was a kid", "right": "quando eu era criança"},
             {"left": "before class", "right": "antes da aula"},
         ]},
        {"type": "group",
         "prompt": "How do we make the past? Put each verb in the right group.",
         "translation": "Como formamos o passado? Coloque cada verbo no grupo certo.",
         "example": "cook → + ed (cooked) · dance → + d (danced)",
         "categories": ["+ ed", "+ d", "double + ed", "y → ied"],
         "words": [
             {"text": "watch", "category": "+ ed"}, {"text": "start", "category": "+ ed"},
             {"text": "enjoy", "category": "+ ed"}, {"text": "finish", "category": "+ ed"},
             {"text": "dance", "category": "+ d"}, {"text": "explore", "category": "+ d"}, {"text": "live", "category": "+ d"},
             {"text": "stop", "category": "double + ed"}, {"text": "plan", "category": "double + ed"},
             {"text": "study", "category": "y → ied"}, {"text": "cry", "category": "y → ied"},
         ]},
        {"type": "fill",
         "prompt": "Write the past of the verbs.",
         "translation": "Escreva o passado dos verbos.",
         "example": "cook → cooked",
         "text": "1. walk → [walked]\n2. work → [worked]\n3. dance → [danced]\n4. stop → [stopped]\n5. study → [studied]\n"
                 "6. play → [played]"},
        {"type": "dropdown",
         "prompt": "Complete with the past of the verb.",
         "translation": "Complete com o passado do verbo.",
         "example": "She [started] working at 9 a.m. yesterday. (start)",
         "text": "1. She [*finished|finish|finishs] work at 5 p.m. yesterday. (finish)\n"
                 "2. Last night, I [*cooked|cook|cookd] dinner and watched TV. (cook)\n"
                 "3. We [*enjoyed|enjoied|enjoy] the trip last weekend. (enjoy)\n"
                 "4. She [*studied|studyed|study] a lot last night. (study)"},
    ],
}

AULA4_IRREGULAR = {
    "title": "Past simple: irregular verbs",
    "lesson": 4,
    "description": "IRREGULAR VERBS: não terminam em ED — é preciso memorizar!\n"
                   "do → did · go → went · see → saw · eat → ate · have → had · wake up → woke up · buy → bought (\"bót\") · "
                   "read → read (escreve igual, mas no passado se fala \"réd\") · meet → met · wear → wore.\n"
                   "O verbo no passado é IGUAL para todas as pessoas: I went, you went, she went, they went. "
                   "Por isso o sujeito é obrigatório!\n"
                   "Refeições: have breakfast / lunch / dinner → had lunch (almocei).",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the verbs to their past forms.",
         "translation": "Ligue os verbos ao passado deles.",
         "example": "go → went",
         "pairs": [
             {"left": "do", "right": "did"},
             {"left": "see", "right": "saw"},
             {"left": "eat", "right": "ate"},
             {"left": "have", "right": "had"},
             {"left": "buy", "right": "bought"},
             {"left": "meet", "right": "met"},
             {"left": "wear", "right": "wore"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the right past form.",
         "translation": "Escolha a forma certa no passado.",
         "example": "Last Sunday, I [went] to the park.",
         "text": "1. Daniel [*woke up|waked up|wake up] at 7 a.m. yesterday.\n"
                 "2. He [*had|haved|has] breakfast with his wife.\n"
                 "3. I [*saw|seed|see] beautiful places in Italy.\n"
                 "4. My friends [*bought|buyed|buy] a new house.\n"
                 "5. I [*met|meeted|meet] amazing people on my last trip."},
        {"type": "fill",
         "prompt": "Translate (from the lesson).",
         "translation": "Traduza as frases da aula.",
         "example": "Eu fui à academia ontem à noite. → I went to the gym last night.",
         "text": "1. Eu comi pizza no domingo passado. → [I ate pizza last Sunday.|I had pizza last Sunday.]\n"
                 "2. Eles assistiram a um filme ontem. → [They watched a movie yesterday.]\n"
                 "3. Meus amigos compraram uma casa nova. → [My friends bought a new house.]\n"
                 "4. Minha irmã usou um vestido preto no sábado. → [My sister wore a black dress on Saturday.]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Went\" is the past of \"go\". → True",
         "statements": [
             {"text": "In the past, the verb is the same for I, you, he, she, we and they.", "answer": True,
              "translation": "No passado, o verbo é igual para I, you, he, she, we e they."},
             {"text": "In \"bought\", we say the letters G and H.", "answer": False,
              "translation": "Em \"bought\", a gente pronuncia as letras G e H."},
             {"text": "\"Read\" in the past is written the same, but the sound changes.", "answer": True,
              "translation": "\"Read\" no passado se escreve igual, mas o som muda."},
             {"text": "\"Goed\" is the past of \"go\".", "answer": False, "translation": "\"Goed\" é o passado de \"go\"."},
         ]},
    ],
}

AULA4_LISTENING = {
    "title": "Listening — Daniel's day",
    "lesson": 4,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Present or past? Listen and choose.",
         "translation": "Presente ou passado? Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"I watched TV.\" → watched",
         "audio": f"{AUDIO}/aula4-presentpast.m4a",
         "text": "1. I [*worked|work] at home.\n2. They [*go|went] to the beach.\n3. She [*cooked|cooks] dinner.\n"
                 "4. We [*had|have] lunch together.\n5. He [*buys|bought] a new car."},
        {"type": "fill",
         "prompt": "Dictation: Daniel's day. Listen and complete.",
         "translation": "Ditado da aula: o dia do Daniel. Ouça e complete com os verbos.",
         "example": "Você ouve: \"Daniel woke up at 7 a.m. yesterday.\" → Daniel [woke] up at 7 a.m. yesterday.",
         "audio": f"{AUDIO}/aula4-daniel.m4a",
         "text": "1. Daniel [woke] up at 7 a.m. yesterday.\n2. He [had] breakfast with his wife.\n"
                 "3. After that, he [went] to the gym.\n4. He [started] work at 1 p.m.\n5. He [finished] work at 7 p.m.\n"
                 "6. They had dinner together and [watched] a movie.\n7. They [went] to bed at 11 p.m."},
        {"type": "info",
         "prompt": "Now listen: Julia talks about her trip to Italy.",
         "translation": "Agora ouça: a Julia conta para um amigo como foi a viagem dela para a Itália. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula4-trip.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Julia traveled to [Italy].",
         "text": "1. Julia went to Italy [*last month|last week|in 2019].\n"
                 "2. In Rome, she visited [*the Colosseum|a museum in Paris|the beach].\n"
                 "3. She ate [*pizza and ice cream|sushi|salad] every day.\n"
                 "4. In Florence, she met [*an old friend from school|her cousin|a famous chef]."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Julia enjoyed the trip. → True",
         "statements": [
             {"text": "Julia traveled with her sister.", "answer": True, "translation": "A Julia viajou com a irmã."},
             {"text": "Julia bought a lot of shoes.", "answer": False, "translation": "A Julia comprou muitos sapatos."},
             {"text": "They walked a lot.", "answer": True, "translation": "Elas caminharam muito."},
         ]},
    ],
}

AULA4_SPEAKING = {
    "title": "Speaking — past simple",
    "lesson": 4,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: WATCHED = \"uótcht\" (o E não é falado) · BOUGHT = \"bót\" · READ (passado) = \"réd\".",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the verbs.",
         "translation": "Ouça e repita os verbos (presente → passado).",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula4-say-v{i}.m4a"} for i, t in enumerate(
             ["cook, cooked", "watch, watched", "start, started", "finish, finished", "walk, walked", "work, worked",
              "go, went", "eat, ate", "have, had", "wake up, woke up", "buy, bought", "read, read"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases.",
         "example": "\"I went to the supermarket on Saturday.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula4-say-s{i}.m4a"} for i, t in enumerate(
             ["I went to the supermarket on Saturday.", "I watched TV.", "I had lunch with my family on Sunday.",
              "Last Sunday, I went to the park and read a book.", "I saw beautiful places on my trip to Italy last month."], 1)]},
        {"type": "speak",
         "prompt": "Now talk about YOU: three things you did last weekend.",
         "translation": "Agora fale sobre VOCÊ: responda com frases completas no passado.",
         "example": "\"Tell me three things you did last weekend.\" → \"I went to the beach, I had lunch with my parents, and I watched a movie.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula4-say-y{i}.m4a"} for i, t in enumerate(
             ["Tell me three things you did last weekend.", "Tell me what you had for breakfast today.",
              "Tell me what time you woke up today."], 1)]},
    ],
}

AULA4_READING = {
    "title": "Reading — a weekend in Gramado",
    "lesson": 4,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Paula's blog post.",
         "translation": "Leia e ouça o post do blog da Paula. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula4-reading.m4a",
         "text": "A WEEKEND IN GRAMADO\n\n"
                 "Last weekend, my husband and I went to Gramado. We traveled by car on Friday night.\n"
                 "On Saturday, we woke up early and had a big breakfast at the hotel.\n"
                 "Then we walked around the city center and visited a chocolate factory. I bought a lot of chocolate for my kids!\n"
                 "In the afternoon, it rained, so we stayed at the hotel and read our books.\n"
                 "At night, we had dinner at a small Italian restaurant, and we met a very nice couple from Argentina.\n"
                 "On Sunday, we drove back home. We loved the trip!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "They went to [Gramado].",
         "text": "1. They traveled [*by car|by plane|by bus].\n"
                 "2. They visited [*a chocolate factory|a museum|a farm].\n"
                 "3. In the afternoon, they [*stayed at the hotel and read|went to the park|swam in the sea].\n"
                 "4. At the restaurant, they met [*a couple from Argentina|their kids|a chef]."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "They went to Gramado last weekend. → True",
         "statements": [
             {"text": "They had breakfast at the hotel.", "answer": True, "translation": "Eles tomaram café da manhã no hotel."},
             {"text": "Paula bought chocolate for her kids.", "answer": True,
              "translation": "A Paula comprou chocolate para os filhos."},
             {"text": "They had dinner at a Japanese restaurant.", "answer": False,
              "translation": "Eles jantaram num restaurante japonês."},
         ]},
        {"type": "fill",
         "prompt": "Find the past of the verbs in the text.",
         "translation": "Encontre no texto o passado destes verbos.",
         "example": "go → [went]",
         "text": "1. wake up → [woke up]\n2. buy → [bought]\n3. rain → [rained]\n4. meet → [met]\n5. drive → [drove]"},
    ],
}

AULA4_WRITING = {
    "title": "Writing — last weekend",
    "lesson": 4,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Sujeito + verbo no passado (regular: +ED / irregular: memorize!) + time expression.",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Rewrite the sentences in the past.",
         "translation": "Reescreva as frases no passado (use a expressão entre parênteses).",
         "example": "I go to the gym. (yesterday) → I went to the gym yesterday.",
         "text": "1. She watches TV. (last night) → [She watched TV last night.|Last night she watched TV.|Last night, she watched TV.]\n"
                 "2. We eat pizza. (last Sunday) → [We ate pizza last Sunday.|We had pizza last Sunday.]\n"
                 "3. They study English. (yesterday) → [They studied English yesterday.]"},
        {"type": "fill",
         "prompt": "Correct the mistakes.",
         "translation": "Corrija os erros.",
         "example": "I goed to school. → I went to school.",
         "text": "1. He buyed a car. → [He bought a car.]\n2. We stoped at the bakery. → [We stopped at the bakery.]\n"
                 "3. Went to the beach yesterday. (I) → [I went to the beach yesterday.]"},
        {"type": "free",
         "prompt": "Write about your last weekend: the things you did. Use at least 5 verbs in the past (regular and irregular).",
         "translation": "Escreva sobre o seu último fim de semana. O que você fez? Use pelo menos 5 verbos no passado (regulares e irregulares).",
         "example": "On Saturday, I woke up late and had breakfast with my family.",
         "model_answer": "On Saturday, I woke up late and had breakfast with my family.\n"
                         "In the afternoon, I went to the supermarket and bought some fruit.\n"
                         "At night, I cooked pasta and watched a movie with my husband.\n"
                         "On Sunday, we visited my parents, and I played with my nephew.",
         "keywords": ["went", "had", "I"], "min_words": 35, "points": 4},
    ],
}

AULA4_VIDEO = _video(4, AULA4_TOPIC, "Video — My trip to Italy",
                     "a Julia conta o que fez na viagem para a Itália: verbos regulares e irregulares no passado.",
                     "aula4-video", [
    _q("Julia went to Italy…", "A Julia foi para a Itália…", "last month.", "yesterday.", "in 2019.", "a long time ago."),
    _q("In Rome, Julia saw…", "Em Roma, a Julia viu…", "the Colosseum.", "the Eiffel Tower.", "a big beach.",
       "a chocolate factory."),
    _q("Every day, she ate…", "Todos os dias, ela comeu…", "pizza and ice cream.", "sushi.", "a sandwich.",
       "pasta and salad."),
    _q("She traveled to Venice…", "Ela foi para Veneza…", "by train.", "by car.", "by plane.", "by bike."),
    _q("Which sentence is correct?", "Qual frase está correta?", "She bought a nice bag.", "She buyed a nice bag.",
       "She buy a nice bag.", "She boughted a nice bag."),
])


# ---------- Aula 05 — -ED Pronunciation (https://youtu.be/JpdXmuXL_QY) ----------

AULA5_TOPIC = "Aula 05 — -ED Pronunciation"

AULA5_SOUNDS = {
    "title": "The three sounds of -ED",
    "lesson": 5,
    "description": "O -ED dos verbos regulares tem 3 pronúncias — e quase nunca é \"ed\"!\n"
                   "/ɪd/ (\"id\", uma sílaba a mais) → só quando o verbo termina em T ou D: wanted, visited, started, needed, ended, decided.\n"
                   "/t/ (estalinho surdo) → depois de sons que NÃO vibram (voiceless: p, k, s, sh, ch, f): "
                   "watched (\"uótcht\"), cooked (\"kukt\"), laughed, kissed, helped, danced.\n"
                   "/d/ (som que vibra) → depois de sons que VIBRAM (voiced: vogais, b, g, v, z, m, n, l, r): "
                   "played (\"plêid\"), called, loved, cleaned, used, traveled (\"trávld\").\n"
                   "Erro comum: \"cook-ED\", \"travel-ED\" ✗ — não crie uma sílaba nova!",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "Which sound? Put each verb in the right group.",
         "translation": "Qual é o som do -ED? Coloque cada verbo no grupo certo.",
         "example": "wanted → /ɪd/ (termina em T) · cooked → /t/ · played → /d/",
         "categories": ["/ɪd/", "/t/", "/d/"],
         "words": [
             {"text": "visited", "category": "/ɪd/"}, {"text": "needed", "category": "/ɪd/"},
             {"text": "decided", "category": "/ɪd/"}, {"text": "started", "category": "/ɪd/"},
             {"text": "watched", "category": "/t/"}, {"text": "kissed", "category": "/t/"},
             {"text": "helped", "category": "/t/"}, {"text": "danced", "category": "/t/"},
             {"text": "called", "category": "/d/"}, {"text": "loved", "category": "/d/"},
             {"text": "cleaned", "category": "/d/"}, {"text": "traveled", "category": "/d/"},
         ]},
        {"type": "dropdown",
         "prompt": "Does the -ED make a new syllable?",
         "translation": "O -ED cria uma sílaba a mais? (Só quando o verbo termina em T ou D.)",
         "example": "wanted → [yes] (want-ed) · cooked → [no] (\"kukt\")",
         "text": "1. ended → [*yes|no]\n2. walked → [*no|yes]\n3. collected → [*yes|no]\n4. listened → [*no|yes]\n"
                 "5. educated → [*yes|no]\n6. stayed → [*no|yes]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Started\" ends with the sound /ɪd/. → True",
         "statements": [
             {"text": "All vowel sounds vibrate (they are voiced).", "answer": True,
              "translation": "Todos os sons de vogal vibram (são vozeados)."},
             {"text": "We say \"cook-ED\", with a new syllable.", "answer": False,
              "translation": "Falamos \"cook-ED\", com uma sílaba a mais."},
             {"text": "The sounds /z/ and /s/ are the same, but /z/ vibrates.", "answer": True,
              "translation": "Os sons /z/ e /s/ são iguais na boca, mas o /z/ vibra."},
             {"text": "\"Traveled\" sounds like \"trá-ve-led\".", "answer": False,
              "translation": "\"Traveled\" soa como \"trá-ve-led\"."},
         ]},
    ],
}

AULA5_VOICED = {
    "title": "Voiced or voiceless?",
    "lesson": 5,
    "description": "VOICED (vozeado) = o som VIBRA as cordas vocais: zzz (como um celular vibrando), b, d, g, v, m, n, l, r e todas as vogais.\n"
                   "VOICELESS (desvozeado) = o ar passa e NÃO vibra: sss, p, t, k, f, sh, ch.\n"
                   "Teste: ponha a mão na garganta e fale \"zzzz\" e depois \"ssss\".\n"
                   "Regra: final do verbo NÃO vibra → -ED = /t/. Final VIBRA → -ED = /d/. Final T ou D → /ɪd/.",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "Voiced or voiceless? Look at the last SOUND of the verb.",
         "translation": "O último SOM do verbo vibra (voiced) ou não (voiceless)?",
         "example": "play (termina em vogal) → voiced · cook (k) → voiceless",
         "categories": ["voiced", "voiceless"],
         "words": [
             {"text": "play", "category": "voiced"}, {"text": "call", "category": "voiced"},
             {"text": "love", "category": "voiced"}, {"text": "clean", "category": "voiced"},
             {"text": "use", "category": "voiced"},
             {"text": "watch", "category": "voiceless"}, {"text": "laugh", "category": "voiceless"},
             {"text": "kiss", "category": "voiceless"}, {"text": "help", "category": "voiceless"},
             {"text": "dance", "category": "voiceless"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the sound of -ED.",
         "translation": "Escolha o som do -ED.",
         "example": "laughed → [/t/] (laugh termina em som de F, que não vibra)",
         "text": "1. stopped → [*/t/|/d/|/ɪd/]\n2. opened → [*/d/|/t/|/ɪd/]\n3. painted → [*/ɪd/|/t/|/d/]\n"
                 "4. washed → [*/t/|/d/|/ɪd/]\n5. lived → [*/d/|/t/|/ɪd/]\n6. added → [*/ɪd/|/d/|/t/]"},
        {"type": "match",
         "prompt": "Match the verbs to how they sound.",
         "translation": "Ligue cada verbo ao jeito como ele soa (aproximado, em português).",
         "example": "watched → \"uótcht\"",
         "pairs": [
             {"left": "cooked", "right": "\"kukt\""},
             {"left": "played", "right": "\"plêid\""},
             {"left": "wanted", "right": "\"uón-tid\""},
             {"left": "traveled", "right": "\"trávld\""},
             {"left": "danced", "right": "\"dénst\""},
         ]},
    ],
}

AULA5_LISTENING = {
    "title": "Listening — /t/, /d/ or /ɪd/?",
    "lesson": 5,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Preste atenção no FINAL de cada verbo.",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the sound of -ED.",
         "translation": "Ouça cada verbo e escolha o som do -ED.",
         "example": "Você ouve: \"cooked\" → /t/",
         "audio": f"{AUDIO}/aula5-sounds.m4a",
         "text": "1. watched → [*/t/|/d/|/ɪd/]\n2. started → [*/ɪd/|/t/|/d/]\n3. listened → [*/d/|/t/|/ɪd/]\n"
                 "4. stayed → [*/d/|/ɪd/|/t/]\n5. kissed → [*/t/|/d/|/ɪd/]\n6. needed → [*/ɪd/|/d/|/t/]"},
        {"type": "dropdown",
         "prompt": "Present or past? Listen carefully to the end of the verb.",
         "translation": "Presente ou passado? Ouça com atenção o final do verbo — às vezes é só um estalinho!",
         "example": "Você ouve: \"I cooked dinner.\" → cooked",
         "audio": f"{AUDIO}/aula5-presentpast.m4a",
         "text": "1. I [*watched|watch] TV.\n2. We [*play|played] soccer.\n3. They [*cleaned|clean] the house.\n"
                 "4. I [*love|loved] this song.\n5. She [*danced|dances] at the party."},
        {"type": "info",
         "prompt": "Now listen to Leo talking about his trip to Chile.",
         "translation": "Agora ouça o Leo contando sobre a viagem dele para o Chile. Repare na pronúncia dos verbos no passado. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula5-story.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "fill",
         "prompt": "Listen again and complete with the verbs in the past.",
         "translation": "Ouça de novo e complete com os verbos no passado.",
         "example": "Last year, I [traveled] to Chile.",
         "text": "1. I [visited] Santiago and the mountains.\n2. We [walked] a lot every day.\n"
                 "3. One day, it [rained] all afternoon.\n4. We [stayed] at the hotel and [watched] movies.\n"
                 "5. I [decided] to go back next year."},
    ],
}

AULA5_SPEAKING = {
    "title": "Speaking — say it right!",
    "lesson": 5,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Lembre: /t/ e /d/ são só um \"estalinho\" no final — nada de \"cook-ED\"!",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "/ɪd/: listen and repeat.",
         "translation": "/ɪd/ (verbos terminados em T ou D): ouça e repita.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula5-say-id{i}.m4a"} for i, t in enumerate(
             ["wanted", "visited", "started", "needed", "ended", "decided"], 1)]},
        {"type": "speak",
         "prompt": "/t/: listen and repeat.",
         "translation": "/t/ (estalinho que não vibra): ouça e repita.",
         "example": "\"watch → watched\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula5-say-t{i}.m4a"} for i, t in enumerate(
             ["watch, watched", "cook, cooked", "laugh, laughed", "kiss, kissed", "help, helped", "dance, danced"], 1)]},
        {"type": "speak",
         "prompt": "/d/: listen and repeat.",
         "translation": "/d/ (som que vibra): ouça e repita.",
         "example": "\"play → played\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula5-say-d{i}.m4a"} for i, t in enumerate(
             ["play, played", "call, called", "love, loved", "clean, cleaned", "use, used", "travel, traveled"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases.",
         "example": "\"I traveled to Chile last year.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula5-say-s{i}.m4a"} for i, t in enumerate(
             ["I traveled to Chile last year.", "She danced and laughed all night.", "We visited my grandmother on Sunday.",
              "They cleaned the house and cooked dinner."], 1)]},
    ],
}

AULA5_READING = {
    "title": "Reading — a busy Saturday",
    "lesson": 5,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto. Repare na pronúncia de cada -ED e responda às perguntas.",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Marina's text.",
         "translation": "Leia e ouça o texto da Marina. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula5-reading.m4a",
         "text": "A BUSY SATURDAY\n\n"
                 "Last Saturday was a busy day! I woke up at 7 and cleaned the whole house.\n"
                 "Then I cooked lunch for my parents. They visited me at noon, and we talked for hours.\n"
                 "In the afternoon, my sister called me. She needed help with her English homework, so I helped her.\n"
                 "At night, my friends and I danced at a party. We laughed a lot!\n"
                 "When I arrived home, I watched a movie and slept on the sofa."},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Marina woke up at [7].",
         "text": "1. In the morning, Marina [*cleaned the house|visited her parents|danced].\n"
                 "2. Her parents [*visited her at noon|called her|cooked lunch].\n"
                 "3. Her sister needed help with [*her English homework|the house|lunch].\n"
                 "4. At night, Marina [*danced at a party|stayed at home|worked]."},
        {"type": "group",
         "prompt": "Put the verbs from the text in the right group.",
         "translation": "Coloque os verbos do texto no grupo do som do -ED.",
         "example": "visited → /ɪd/",
         "categories": ["/ɪd/", "/t/", "/d/"],
         "words": [
             {"text": "visited", "category": "/ɪd/"}, {"text": "needed", "category": "/ɪd/"},
             {"text": "cooked", "category": "/t/"}, {"text": "talked", "category": "/t/"},
             {"text": "helped", "category": "/t/"}, {"text": "laughed", "category": "/t/"},
             {"text": "cleaned", "category": "/d/"}, {"text": "called", "category": "/d/"},
             {"text": "arrived", "category": "/d/"},
         ]},
    ],
}

AULA5_WRITING = {
    "title": "Writing — past verbs",
    "lesson": 5,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Escreva o passado dos verbos regulares (+ED, +D, dobra, Y→IED) e depois leia em voz alta, "
                   "com o som certo do -ED.",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the past and the sound of -ED (t, d or id).",
         "translation": "Escreva o passado e o som do -ED (escreva t, d ou id).",
         "example": "want → wanted (id)",
         "text": "1. clean → [cleaned] ([d])\n2. help → [helped] ([t])\n3. visit → [visited] ([id])\n"
                 "4. travel → [traveled|travelled] ([d])\n5. stop → [stopped] ([t])"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza (verbos regulares no passado).",
         "example": "Eu limpei a casa. → I cleaned the house.",
         "text": "1. Ela me ligou ontem. → [She called me yesterday.]\n"
                 "2. Nós viajamos para o Chile. → [We traveled to Chile.|We travelled to Chile.]\n"
                 "3. Eles dançaram e riram muito. → [They danced and laughed a lot.]"},
        {"type": "free",
         "prompt": "Write about yesterday with at least 6 regular verbs (cleaned, cooked, watched, called, visited, played…). "
                   "Then read your text aloud.",
         "translation": "Escreva sobre o seu dia de ontem com pelo menos 6 verbos regulares. Depois leia o seu texto em voz alta, "
                        "com o som certo de cada -ED.",
         "example": "Yesterday, I cooked lunch and watched a movie.",
         "model_answer": "Yesterday, I worked from 9 to 5. After work, I walked to the supermarket.\n"
                         "At home, I cooked dinner and called my mother. We talked for an hour.\n"
                         "Then I watched a movie and played video games with my brother.",
         "keywords": ["yesterday", "I"], "min_words": 30, "points": 4},
    ],
}

AULA5_VIDEO = _video(5, AULA5_TOPIC, "Video — Sounds of the past",
                     "ouça os verbos no passado em situações reais e descubra o som do -ED: /t/, /d/ ou /ɪd/.",
                     "aula5-video", [
    _q("\"She danced.\" What's the sound of -ED?", "\"She danced.\" Qual é o som do -ED?", "/t/", "/d/", "/ɪd/",
       "There's no sound."),
    _q("\"They played soccer.\" What's the sound of -ED?", "\"They played soccer.\" Qual é o som do -ED?", "/d/", "/t/",
       "/ɪd/", "/ed/"),
    _q("\"He visited his grandmother.\" What's the sound of -ED?", "\"He visited his grandmother.\" Qual é o som do -ED?",
       "/ɪd/", "/t/", "/d/", "/ed/"),
    _q("\"I cooked dinner.\" How do we say \"cooked\"?", "\"I cooked dinner.\" Como falamos \"cooked\"?", "\"kukt\"",
       "\"kúkéd\"", "\"kukid\"", "\"kúk\""),
    _q("\"We traveled to the beach.\" How do we say \"traveled\"?", "Como falamos \"traveled\"?", "\"trávld\"",
       "\"trá-ve-led\"", "\"trávid\"", "\"trávelt\""),
])


# ---------- Aula 06 — Past Simple: negative (https://youtu.be/XmT1GA9zUMA) ----------

AULA6_TOPIC = "Aula 06 — Past Simple (negative)"

AULA6_DIDNT = {
    "title": "Didn't + base form",
    "lesson": 6,
    "description": "NEGATIVE no passado: sujeito + DIDN'T (did not) + verbo na FORMA BÁSICA.\n"
                   "I didn't cook yesterday. (Eu não cozinhei ontem.) · He didn't cook. · They didn't go to the beach on Saturday.\n"
                   "O DIDN'T já mostra que é passado e negativo → o verbo NÃO vai para o passado: "
                   "didn't cook ✓ · didn't cooked ✗ · didn't go ✓ · didn't went ✗.\n"
                   "Igual para todas as pessoas: I / you / he / she / we / they didn't…\n"
                   "Como fazer: 1) ache o verbo (went) · 2) ache a forma básica (go) · 3) use didn't + go.",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta (didn't + forma básica).",
         "example": "I [didn't take] a nap last Sunday.",
         "text": "1. She [*didn't see|didn't saw|doesn't saw] her friends last weekend.\n"
                 "2. They [*didn't go|didn't went|don't went] to the beach on Saturday.\n"
                 "3. He [*didn't cook|didn't cooked|not cooked] yesterday.\n"
                 "4. We [*didn't watch|didn't watched|wasn't watch] TV last night.\n"
                 "5. I [*didn't buy|didn't bought|not bought] a new phone."},
        {"type": "match",
         "prompt": "Match the past form to the base form.",
         "translation": "Ligue o passado à forma básica do verbo (é ela que vai depois do didn't).",
         "example": "went → go",
         "pairs": [
             {"left": "did", "right": "do"},
             {"left": "saw", "right": "see"},
             {"left": "met", "right": "meet"},
             {"left": "slept", "right": "sleep"},
             {"left": "gave", "right": "give"},
             {"left": "wore", "right": "wear"},
             {"left": "took", "right": "take"},
         ]},
        {"type": "fill",
         "prompt": "Write the negative: didn't + base form.",
         "translation": "Escreva a negativa: didn't + forma básica.",
         "example": "cooked → didn't cook",
         "text": "1. watched → [didn't watch]\n2. started → [didn't start]\n3. went → [didn't go]\n4. ate → [didn't eat]\n"
                 "5. had → [didn't have]\n6. bought → [didn't buy]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Didn't\" = did not. → True",
         "statements": [
             {"text": "After \"didn't\", the verb is in the past.", "answer": False,
              "translation": "Depois de \"didn't\", o verbo fica no passado."},
             {"text": "\"Didn't\" is the same for I, you, he, she, we and they.", "answer": True,
              "translation": "\"Didn't\" é igual para I, you, he, she, we e they."},
             {"text": "\"Didn't\" is more natural than \"did not\" when we speak.", "answer": True,
              "translation": "\"Didn't\" é mais natural que \"did not\" na fala."},
             {"text": "\"She didn't went\" is correct.", "answer": False, "translation": "\"She didn't went\" está correto."},
         ]},
    ],
}

AULA6_SENTENCES = {
    "title": "Make it negative!",
    "lesson": 6,
    "description": "Transforme as frases: ache o verbo, pense na forma básica e use DIDN'T.\n"
                   "She cooked last night. → She didn't cook last night.\n"
                   "She went to the park yesterday. → She didn't go to the park yesterday.\n"
                   "Lembre: was / were NÃO usam didn't → I wasn't tired. · They weren't at home.",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Make the sentences negative (from the lesson).",
         "translation": "Passe as frases da aula para a negativa.",
         "example": "They watched TV last night. → They didn't watch TV last night.",
         "text": "1. I went to the supermarket on Saturday. → [I didn't go to the supermarket on Saturday.|I did not go to the supermarket on Saturday.]\n"
                 "2. He did his homework. → [He didn't do his homework.|He did not do his homework.]\n"
                 "3. My father saw an accident. → [My father didn't see an accident.|My father did not see an accident.]\n"
                 "4. Carla met an interesting guy. → [Carla didn't meet an interesting guy.|Carla did not meet an interesting guy.]\n"
                 "5. His girlfriend wore a red dress last night. → [His girlfriend didn't wear a red dress last night.|His girlfriend did not wear a red dress last night.]"},
        {"type": "dropdown",
         "prompt": "Didn't or wasn't / weren't?",
         "translation": "Didn't (outros verbos) ou wasn't / weren't (verb to be)?",
         "example": "I [wasn't] tired. · I [didn't] sleep.",
         "text": "1. She [*didn't|wasn't] sleep for many hours.\n2. They [*weren't|didn't] at home yesterday.\n"
                 "3. My friend [*didn't|wasn't] give me a present.\n4. The movie [*wasn't|didn't] good.\n"
                 "5. We [*didn't|weren't] eat pizza."},
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras em ordem. (Eu não tirei um cochilo no domingo passado.)",
         "example": "didn't / She / cook → She didn't cook.",
         "tokens": ["I", "didn't", "take", "a", "nap", "last", "Sunday."], "alternatives": []},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu não cozinhei ontem. → I didn't cook yesterday.",
         "text": "1. Ele não cozinhou ontem. → [He didn't cook yesterday.|He did not cook yesterday.]\n"
                 "2. Ela não viu os amigos dela no fim de semana passado. → [She didn't see her friends last weekend.|She did not see her friends last weekend.]\n"
                 "3. Nós não fomos à praia. → [We didn't go to the beach.|We did not go to the beach.]"},
    ],
}

AULA6_LISTENING = {
    "title": "Listening — what didn't they do?",
    "lesson": 6,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Affirmative or negative? Listen and choose.",
         "translation": "Afirmativa ou negativa? Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"I didn't cook.\" → didn't cook",
         "audio": f"{AUDIO}/aula6-forms.m4a",
         "text": "1. She [*didn't go|went] to work.\n2. We [*watched|didn't watch] a movie.\n3. They [*didn't eat|ate] pizza.\n"
                 "4. He [*bought|didn't buy] a car.\n5. I [*didn't sleep|slept] well."},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete com didn't + verbo.",
         "example": "Você ouve: \"I didn't cook yesterday.\" → I [didn't cook] yesterday.",
         "audio": f"{AUDIO}/aula6-dictation.m4a",
         "text": "1. She [didn't see] her friends last weekend.\n2. They [didn't go] to the beach on Saturday.\n"
                 "3. He [didn't do] his homework.\n4. We [didn't have] breakfast today."},
        {"type": "info",
         "prompt": "Now listen: Mom asks Lucas about his day.",
         "translation": "Agora ouça: a mãe pergunta para o Lucas como foi o dia dele. O Lucas diz o que ele fez e o que NÃO fez. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula6-lucas.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Lucas went to school. → True",
         "statements": [
             {"text": "Lucas ate his lunch.", "answer": False, "translation": "O Lucas comeu o almoço dele."},
             {"text": "Lucas played soccer after school.", "answer": True, "translation": "O Lucas jogou futebol depois da aula."},
             {"text": "Lucas did his homework.", "answer": False, "translation": "O Lucas fez a lição de casa."},
             {"text": "Lucas forgot his jacket at school.", "answer": True, "translation": "O Lucas esqueceu o casaco na escola."},
         ]},
        {"type": "fill",
         "prompt": "Listen again and complete Lucas's sentences.",
         "translation": "Ouça de novo e complete as frases do Lucas.",
         "example": "I [didn't eat] my lunch.",
         "text": "1. I [didn't like] the food.\n2. I [didn't have] time for my homework.\n3. I [didn't see] my jacket."},
    ],
}

AULA6_SPEAKING = {
    "title": "Speaking — didn't",
    "lesson": 6,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: DIDN'T = \"dídent\" (o T final quase some) · use sempre a forma curta na fala.",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita: afirmativa → negativa.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula6-say-v{i}.m4a"} for i, t in enumerate(
             ["cooked, didn't cook", "watched, didn't watch", "went, didn't go", "ate, didn't eat", "had, didn't have",
              "bought, didn't buy"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "\"I didn't take a nap last Sunday.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula6-say-s{i}.m4a"} for i, t in enumerate(
             ["I didn't take a nap last Sunday.", "She didn't see her friends last weekend.",
              "They didn't go to the beach on Saturday.", "She didn't go to the park yesterday.",
              "He didn't do his homework."], 1)]},
        {"type": "speak",
         "prompt": "Now talk about YOU: say two things you didn't do yesterday.",
         "translation": "Agora fale sobre VOCÊ: diga coisas que você NÃO fez ontem (e o que fez).",
         "example": "\"I didn't go to the gym yesterday. I stayed at home.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula6-say-y{i}.m4a"} for i, t in enumerate(
             ["Tell me something you didn't do yesterday.", "Tell me something you didn't eat last week.",
              "Tell me a place you didn't go last weekend."], 1)]},
    ],
}

AULA6_READING = {
    "title": "Reading — a terrible day",
    "lesson": 6,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Mark's text.",
         "translation": "Leia e ouça o texto do Mark sobre um dia terrível. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula6-reading.m4a",
         "text": "A TERRIBLE DAY\n\n"
                 "Yesterday was a terrible day! My alarm clock didn't ring, so I woke up very late.\n"
                 "I didn't take a shower, and I didn't have breakfast.\n"
                 "I ran to the bus stop, but I didn't catch the bus. I took a taxi, and it was very expensive.\n"
                 "At work, my computer didn't work all morning, and I didn't finish my report.\n"
                 "In the evening, I went to the gym, but I didn't exercise: I forgot my sneakers at home!\n"
                 "I didn't watch TV at night. I went to bed at 9 p.m. Today is a better day!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Yesterday was a [terrible] day.",
         "text": "1. Mark woke up late because [*his alarm clock didn't ring|he was sick|he went to bed late].\n"
                 "2. He went to work [*by taxi|by bus|on foot].\n"
                 "3. At work, [*his computer didn't work|he finished his report|he had a meeting].\n"
                 "4. He didn't exercise because [*he forgot his sneakers|the gym was closed|he was tired]."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Mark woke up late. → True",
         "statements": [
             {"text": "Mark had breakfast at home.", "answer": False, "translation": "O Mark tomou café da manhã em casa."},
             {"text": "The taxi was expensive.", "answer": True, "translation": "O táxi foi caro."},
             {"text": "Mark watched TV at night.", "answer": False, "translation": "O Mark assistiu TV à noite."},
         ]},
        {"type": "fill",
         "prompt": "Complete with didn't + verb, according to the text.",
         "translation": "Complete com didn't + verbo, de acordo com o texto.",
         "example": "His alarm clock [didn't ring].",
         "text": "1. He [didn't take] a shower.\n2. He [didn't catch] the bus.\n3. He [didn't finish] his report."},
    ],
}

AULA6_WRITING = {
    "title": "Writing — what I didn't do",
    "lesson": 6,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Afirmativa: verbo no passado (cooked, went). Negativa: didn't + forma básica (didn't cook, didn't go).",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Correct the mistakes.",
         "translation": "Corrija os erros.",
         "example": "She didn't went to school. → She didn't go to school.",
         "text": "1. I didn't saw the movie. → [I didn't see the movie.|I did not see the movie.]\n"
                 "2. They didn't played soccer. → [They didn't play soccer.|They did not play soccer.]\n"
                 "3. He don't cooked yesterday. → [He didn't cook yesterday.|He did not cook yesterday.]"},
        {"type": "fill",
         "prompt": "Write the negative + the affirmative.",
         "translation": "Escreva a negativa e depois a afirmativa com a informação entre parênteses.",
         "example": "She went to the park. (the beach) → She didn't go to the park. She went to the beach.",
         "text": "1. I ate pizza. (sushi) → [I didn't eat pizza. I ate sushi.]\n"
                 "2. They watched a movie. (a soccer game) → [They didn't watch a movie. They watched a soccer game.]"},
        {"type": "free",
         "prompt": "Write about last weekend: 3 things you did and 3 things you didn't do.",
         "translation": "Escreva sobre o último fim de semana: 3 coisas que você fez e 3 coisas que você NÃO fez.",
         "example": "On Saturday, I didn't wake up early. I slept until 10!",
         "model_answer": "Last weekend was very relaxing. On Saturday, I didn't wake up early: I slept until 10!\n"
                         "I didn't cook. I had lunch at a restaurant with my family.\n"
                         "On Sunday, I went to the park, but I didn't run. I walked with my dog.\n"
                         "I didn't study, and I didn't work. I watched two movies!",
         "keywords": ["didn't", "I"], "min_words": 35, "points": 4},
    ],
}

AULA6_VIDEO = _video(6, AULA6_TOPIC, "Video — Not what you think!",
                     "o que as pessoas fizeram — e o que NÃO fizeram — no fim de semana: didn't + forma básica.",
                     "aula6-video", [
    _q("Choose the true sentence about Carlos.", "Escolha a frase verdadeira sobre o Carlos.",
       "Carlos didn't go to the gym. He slept all day.", "Carlos went to the gym.", "Carlos didn't went to the gym.",
       "Carlos doesn't go to the gym."),
    _q("Choose the true sentence about the friends.", "Escolha a frase verdadeira sobre os amigos.",
       "They didn't go to the beach. They went cycling.", "They went to the beach.", "They didn't went cycling.",
       "They didn't cycling."),
    _q("Choose the true sentence about Grandma Rosa.", "Escolha a frase verdadeira sobre a vovó Rosa.",
       "She didn't buy bread. She made it at home.", "She bought bread at the bakery.", "She didn't made bread.",
       "She doesn't make bread."),
    _q("Choose the true sentence about Ana.", "Escolha a frase verdadeira sobre a Ana.",
       "She didn't watch TV. She read a book.", "She watched TV all night.", "She didn't read a book.",
       "She didn't watched TV."),
    _q("Which sentence is correct?", "Qual frase está correta?", "I didn't see my friends.", "I didn't saw my friends.",
       "I don't saw my friends.", "I not see my friends."),
])

# ---------- Aula 07 — Past Simple: interrogative (https://youtu.be/xavnVHYvcg0) ----------

AULA7_TOPIC = "Aula 07 — Past Simple (interrogative)"

AULA7_DID = {
    "title": "Did…? Yes, I did. / No, I didn't.",
    "lesson": 7,
    "description": "Na interrogativa do passado, começamos com DID + sujeito + verbo na FORMA BÁSICA.\n"
                   "She cooked last night. → She didn't cook last night. → DID she COOK last night?\n"
                   "O DID já indica passado e pergunta: nada de \"Did she cooked\" ou \"Did he went\"!\n"
                   "Respostas curtas: Yes, she did. / No, she didn't. (Resposta completa também pode, mas é menos natural: "
                   "Yes, I bought a new dress.)\n"
                   "Perguntas com DID → resposta YES ou NO.",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Make questions.",
         "translation": "Transforme as frases em perguntas.",
         "example": "She cooked last night. → Did she cook last night?",
         "text": "1. You went to the movies last weekend. → [Did you go to the movies last weekend?]\n"
                 "2. They played soccer yesterday. → [Did they play soccer yesterday?]\n"
                 "3. He bought a bike. → [Did he buy a bike?]\n"
                 "4. She woke up at 6. → [Did she wake up at 6?|Did she wake up at six?]"},
        {"type": "dropdown",
         "prompt": "Choose the right short answer.",
         "translation": "Escolha a resposta curta certa.",
         "example": "Did they play soccer yesterday? (✓) → [Yes, they did.]",
         "text": "1. Did he buy a bike? (✗) → [*No, he didn't.|No, he don't.|No, he bought.]\n"
                 "2. Did you sleep well? (✓) → [*Yes, I did.|Yes, I slept.|Yes, I do.]\n"
                 "3. Did she cook dinner last Sunday? (✓) → [*Yes, she did.|Yes, she cooked.|Yes, she does.]\n"
                 "4. Did they have a picnic in the park? (✗) → [*No, they didn't.|No, they don't.|No, they weren't.]"},
        {"type": "dropdown",
         "prompt": "Correct or incorrect?",
         "translation": "Correto ou incorreto? (Exercício da aula.)",
         "example": "Did you sleep well? → [Correct]",
         "text": "1. Did he went to the park? → [*Incorrect|Correct]\n"
                 "2. Did she watched TV? → [*Incorrect|Correct]\n"
                 "3. Did you buy a new dress? → [*Correct|Incorrect]\n"
                 "4. Did you buy a new dress? Yes, I bought. → [*Incorrect|Correct]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Did\" shows that the question is in the past. → True",
         "statements": [
             {"text": "After \"did\", we use the verb in the past.", "answer": False,
              "translation": "Depois de \"did\", usamos o verbo no passado."},
             {"text": "We answer \"Did…?\" questions with yes or no.", "answer": True,
              "translation": "Respondemos às perguntas com \"Did…?\" com sim ou não."},
             {"text": "In English, we can make a question only with intonation, like in Portuguese.", "answer": False,
              "translation": "Em inglês, podemos fazer uma pergunta só com a entonação, como em português."},
         ]},
    ],
}

AULA7_WH = {
    "title": "Wh- questions: Where did you go?",
    "lesson": 7,
    "description": "Question words (Básico 1): WHERE = onde · WHAT = o que, qual · WHEN = quando · WHY = por que · "
                   "HOW = como · HOW LONG = quanto tempo.\n"
                   "A question word tem prioridade: QUESTION WORD + DID + sujeito + verbo na forma básica + (informação extra).\n"
                   "What did you eat in the morning? · Where did she go last night?\n"
                   "Essas perguntas NÃO têm resposta yes / no: precisamos dar a informação → I ate eggs. · I went to Canada.",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Onde ela foi ontem à noite?)",
         "example": "did / eat / What / you → What did you eat?",
         "tokens": ["Where", "did", "she", "go", "last", "night?"], "alternatives": []},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Como você conheceu o seu melhor amigo?)",
         "example": "you / did / When / travel → When did you travel?",
         "tokens": ["How", "did", "you", "meet", "your", "best", "friend?"], "alternatives": []},
        {"type": "dropdown",
         "prompt": "Choose the question word.",
         "translation": "Escolha a question word certa de acordo com a resposta.",
         "example": "[Where] did you go? — I went to Rio de Janeiro.",
         "text": "1. [*When|Where|Why] did you travel? — I traveled in February.\n"
                 "2. [*Where|What|How long] did you stay? — I stayed at a hotel.\n"
                 "3. [*How long|When|Where] did you stay there? — For five days.\n"
                 "4. [*What|Where|Why] did you eat for dinner? — I ate pizza.\n"
                 "5. [*Why|When|What] did you call me? — Because I needed help."},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas.",
         "example": "Where did you go? → I went to Canada.",
         "pairs": [
             {"left": "Did you like the trip?", "right": "Yes, I did. I loved it."},
             {"left": "When did you travel?", "right": "I traveled last month."},
             {"left": "Where did you stay?", "right": "I stayed at a hotel."},
             {"left": "What did you eat in the morning?", "right": "I ate a pancake."},
             {"left": "Did you go alone?", "right": "No, I didn't."},
         ]},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Você estudou inglês? → Did you study English?",
         "text": "1. Ela acordou às 6 horas? → [Did she wake up at 6?|Did she wake up at six?|Did she wake up at 6 o'clock?|"
                 "Did she wake up at six o'clock?]\n"
                 "2. O que você comeu no jantar? → [What did you eat for dinner?]\n"
                 "3. Onde eles ficaram? → [Where did they stay?]"},
    ],
}

AULA7_LISTENING = {
    "title": "Listening — Carla's vacation",
    "lesson": 7,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Pronúncia: DID YOU soa como \"díd-iu\" ou até \"dídju\" quando falamos rápido.",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"Did you go to the park?\" → Did you go",
         "audio": f"{AUDIO}/aula7-forms.m4a",
         "text": "1. [*Did you sleep|Do you sleep|Did you slept] well?\n2. [*Did she watch|Does she watch|Did she watched] TV?\n"
                 "3. [*Yes, they did.|Yes, they do.|Yes, they didn't.]\n4. [*No, he didn't.|No, he doesn't.|No, he did.]\n"
                 "5. [*Where did you go|Where do you go|Where did you going] last night?"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"Did she cook last night?\" → [Did] she cook last night?",
         "audio": f"{AUDIO}/aula7-dictation.m4a",
         "text": "1. [Did] they play soccer yesterday?\n2. No, he [didn't|did not].\n"
                 "3. [Where] did you stay?\n4. How long did you [stay] there?"},
        {"type": "info",
         "prompt": "Now listen: Carla is back from her vacation.",
         "translation": "Agora ouça: a Carla voltou das férias, e o colega dela, o Mike, faz perguntas sobre a viagem. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula7-vacation.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Where did Carla go? → [To Salvador.]",
         "text": "1. When did Carla go? → [*In January.|In July.|In December.]\n"
                 "2. Where did they stay? → [*At a small hotel near the beach.|At a friend's house.|In an apartment.]\n"
                 "3. How long did they stay there? → [*For ten days.|For two days.|For two weeks.]\n"
                 "4. Did Carla like the acarajé? → [*Yes, she did.|No, she didn't.|Yes, she liked.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Carla traveled with her family. → True",
         "statements": [
             {"text": "It was very hot in Salvador.", "answer": True, "translation": "Estava muito quente em Salvador."},
             {"text": "Carla's brother liked the acarajé.", "answer": False,
              "translation": "O irmão da Carla gostou do acarajé."},
             {"text": "Carla took a lot of pictures.", "answer": False, "translation": "A Carla tirou muitas fotos."},
         ]},
    ],
}

AULA7_SPEAKING = {
    "title": "Speaking — did you…?",
    "lesson": 7,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: em inglês, a pergunta começa com DID; a voz sobe no final das perguntas de yes / no "
                   "(Did you sleep well? ↗) e desce nas perguntas com question word (Where did you go? ↘).",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the questions and answers.",
         "translation": "Ouça e repita as perguntas e as respostas da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula7-say-q{i}.m4a"} for i, t in enumerate(
             ["Did she cook last night? Yes, she did.", "Did you go to the movies last weekend? No, I didn't.",
              "Did they have a picnic in the park on Saturday? Yes, they did.", "Did he buy a bike? No, he didn't."], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the wh- questions.",
         "translation": "Ouça e repita as perguntas com question words.",
         "example": "\"Where did you go last night?\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula7-say-w{i}.m4a"} for i, t in enumerate(
             ["Where did you go last night?", "What did you eat for dinner?", "When did you travel?",
              "Why did you call me?", "How did you meet your best friend?"], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOUR last vacation.",
         "translation": "Agora responda às perguntas sobre as SUAS últimas férias com uma frase completa.",
         "example": "\"Where did you go?\" → \"I went to Rio de Janeiro.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula7-say-y{i}.m4a"} for i, t in enumerate(
             ["Did you travel on your last vacation?", "When did you travel?", "Where did you go?",
              "Where did you stay?", "How long did you stay there?", "Did you like the trip?"], 1)]},
    ],
}

AULA7_READING = {
    "title": "Reading — my first trip abroad",
    "lesson": 7,
    "subject": "Reading",
    "description": "Leia (e ouça) a entrevista e responda às perguntas de acordo com o texto.",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the interview with Marina.",
         "translation": "Leia e ouça a entrevista com a Marina sobre a primeira viagem dela para fora do Brasil. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula7-reading.m4a",
         "text": "MY FIRST TRIP ABROAD\n\n"
                 "Marina is 25 and lives in Curitiba. Last year, she traveled to another country for the first time. "
                 "We asked her some questions.\n\n"
                 "Where did you go? — I went to Buenos Aires, in Argentina.\n"
                 "Did you go alone? — No, I didn't. I went with my best friend, Júlia.\n"
                 "When did you travel? — We traveled in July. It was winter there, and it was very cold!\n"
                 "Where did you stay? — We stayed in a small apartment in the city center.\n"
                 "What did you do there? — We visited museums, walked a lot and watched a tango show.\n"
                 "What did you eat? — We ate a lot of meat and empanadas. Delicious!\n"
                 "Did you speak Spanish? — Yes, I did, but only a little!\n"
                 "Did you like the trip? — Yes, I did. I loved it! I want to go back next year."},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Where did Marina go? → [To Buenos Aires.]",
         "text": "1. Who did Marina travel with? → [*With her best friend.|With her family.|Alone.]\n"
                 "2. When did they travel? → [*In July.|In January.|In December.]\n"
                 "3. Where did they stay? → [*In a small apartment.|At a big hotel.|At a friend's house.]\n"
                 "4. What did they watch? → [*A tango show.|A soccer game.|A movie.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Marina lives in Curitiba. → True",
         "statements": [
             {"text": "It was hot in Buenos Aires.", "answer": False, "translation": "Estava quente em Buenos Aires."},
             {"text": "Marina spoke a little Spanish.", "answer": True, "translation": "A Marina falou um pouco de espanhol."},
             {"text": "Marina wants to go back to Buenos Aires.", "answer": True,
              "translation": "A Marina quer voltar para Buenos Aires."},
         ]},
        {"type": "fill",
         "prompt": "Complete the questions from the text.",
         "translation": "Complete as perguntas da entrevista.",
         "example": "[Where] did you go?",
         "text": "1. [Did] you go alone?\n2. What did you [eat]?\n3. Did you [like] the trip?"},
    ],
}

AULA7_WRITING = {
    "title": "Writing — my last vacation",
    "lesson": 7,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Perguntas: Did + sujeito + verbo na forma básica? · Where / When / What … did …?\n"
                   "Respostas: verbo no passado → I went… · I stayed… · I traveled… · Yes, I did. / No, I didn't.",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the questions for the answers.",
         "translation": "Escreva a pergunta para cada resposta. Use a question word entre parênteses.",
         "example": "(where) I went to Rio de Janeiro. → Where did you go?",
         "text": "1. (when) I traveled in February. → [When did you travel?]\n"
                 "2. (how long) I stayed there for five days. → [How long did you stay there?|How long did you stay?]\n"
                 "3. (what) I ate pizza for dinner. → [What did you eat for dinner?|What did you eat?]\n"
                 "4. (where) We stayed at a hotel. → [Where did you stay?]"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Ela cozinhou ontem à noite? → Did she cook last night?",
         "text": "1. Ele comprou uma bicicleta? → [Did he buy a bike?|Did he buy a bicycle?]\n"
                 "2. Vocês assistiram TV ontem? → [Did you watch TV yesterday?]"},
        {"type": "free",
         "prompt": "Write about your last vacation. Answer the questions: Did you travel? When did you travel? "
                   "Where did you go? Where did you stay? How long did you stay there? Did you like the trip?",
         "translation": "Escreva sobre as suas últimas férias respondendo às perguntas: Você viajou? Quando? Para onde? "
                        "Onde você ficou? Por quanto tempo? Você gostou da viagem?",
         "example": "Yes, I did. I traveled in February.",
         "model_answer": "Yes, I did. I traveled in February.\n"
                         "I went to Rio de Janeiro with my sister.\n"
                         "We stayed in a hotel near the beach.\n"
                         "We stayed there for five days.\n"
                         "Did I like the trip? Yes, I did. I loved it!",
         "keywords": ["went", "did"], "min_words": 30, "points": 4},
    ],
}

AULA7_VIDEO = _video(7, AULA7_TOPIC, "Video — How was your trip?",
                     "o Leo voltou do Canadá e responde a perguntas sobre a viagem: Did you…? Where did you…? What did you…?",
                     "aula7-video", [
    _q("Where did Leo go on his vacation?", "Para onde o Leo foi nas férias?", "To Canada.", "To Brazil.",
       "To the United States.", "To Argentina."),
    _q("Where did Leo stay?", "Onde o Leo ficou?", "At his cousin's house.", "At a hotel.", "In an apartment.",
       "At his friend's house."),
    _q("Did it snow?", "Nevou?", "Yes, it did.", "No, it didn't.", "Yes, it snowed it.", "No, it wasn't."),
    _q("Did Leo visit Niagara Falls?", "O Leo visitou as Cataratas do Niágara?", "Yes, he did.", "No, he didn't.",
       "Yes, he visited.", "Yes, he does."),
    _q("What did Leo eat every morning?", "O que o Leo comeu todas as manhãs?", "Pancakes with maple syrup.",
       "Eggs and coffee.", "Pizza.", "Bread and cheese."),
    _q("Did Leo go ice skating?", "O Leo foi patinar no gelo?", "No, he didn't.", "Yes, he did.", "No, he don't.",
       "No, he wasn't."),
])

# ---------- Aula 08 — Past Continuous (https://youtu.be/8pR_8NBHKu0) ----------

AULA8_TOPIC = "Aula 08 — Past Continuous"

AULA8_FORMS = {
    "title": "Past continuous: was / were + -ING",
    "lesson": 8,
    "description": "PAST CONTINUOUS = ação que ESTAVA EM PROGRESSO em um momento do passado (como o present continuous, "
                   "mas com WAS / WERE).\n"
                   "AFFIRMATIVE: sujeito + WAS / WERE + verbo-ING → She was working last Saturday. · "
                   "They were playing soccer at this time yesterday.\n"
                   "NEGATIVE: WASN'T / WEREN'T + verbo-ING → She wasn't baking a cake. · They weren't having a party.\n"
                   "-ING: a maioria só acrescenta ING (cook → cooking, study → studying) · termina em E: tira o E "
                   "(dance → dancing, give → giving) · uma sílaba com consoante + vogal + consoante: dobra a última "
                   "consoante (shop → shopping, stop → stopping).",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the -ING form.",
         "translation": "Escreva a forma com -ING. Lembre das regrinhas da aula.",
         "example": "cook → cooking",
         "text": "1. study → [studying]\n2. dance → [dancing]\n3. give → [giving]\n4. shop → [shopping]\n"
                 "5. stop → [stopping]\n6. swim → [swimming]\n7. bake → [baking]\n8. have → [having]"},
        {"type": "dropdown",
         "prompt": "Choose was or were.",
         "translation": "Escolha was ou were.",
         "example": "She [was] working last Saturday.",
         "text": "1. They [*were|was] playing soccer at this time yesterday.\n2. He [*was|were] cooking at 7 p.m.\n"
                 "3. I [*was|were] reading a book.\n4. We [*were|was] watching TV.\n5. The dog [*was|were] sleeping."},
        {"type": "fill",
         "prompt": "Look at the information and write the negative sentence.",
         "translation": "Veja a informação e escreva a frase negativa (exercício da aula).",
         "example": "She was studying English. (geography) → She wasn't studying geography.",
         "text": "1. They were playing tennis. (basketball) → [They weren't playing basketball.|They were not playing basketball.]\n"
                 "2. It was sleeping. (playing) → [It wasn't playing.|It was not playing.]\n"
                 "3. He was eating a hot dog. (pizza) → [He wasn't eating pizza.|He was not eating pizza.|"
                 "He wasn't eating a pizza.|He was not eating a pizza.]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "The past continuous uses was or were. → True",
         "statements": [
             {"text": "The past continuous shows an action in progress in the past.", "answer": True,
              "translation": "O past continuous mostra uma ação em progresso no passado."},
             {"text": "\"Shop\" + ING = \"shoping\".", "answer": False, "translation": "\"Shop\" + ING = \"shoping\"."},
             {"text": "\"Dance\" + ING = \"dancing\".", "answer": True, "translation": "\"Dance\" + ING = \"dancing\"."},
             {"text": "We say \"They was playing\".", "answer": False, "translation": "Dizemos \"They was playing\"."},
         ]},
    ],
}

AULA8_QUESTIONS = {
    "title": "Were you…? What was she doing?",
    "lesson": 8,
    "description": "INTERROGATIVE: WAS / WERE vem antes do sujeito → Was the baby crying at 2 o'clock in the morning? · "
                   "Were you having a party yesterday?\n"
                   "Short answers: Yes, I was. / No, I wasn't. · Yes, they were. / No, they weren't.\n"
                   "Com question word: What was he doing at 7 p.m. last night? → He was cooking. · "
                   "What were they eating? → They were eating sushi.",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (O bebê estava chorando às 2 horas da manhã?)",
         "example": "you / Were / a party / having → Were you having a party?",
         "tokens": ["Was", "the", "baby", "crying", "at", "2", "o'clock", "in", "the", "morning?"], "alternatives": []},
        {"type": "dropdown",
         "prompt": "Choose the right short answer.",
         "translation": "Escolha a resposta curta certa.",
         "example": "Were you having a party yesterday? (✗) → [No, I wasn't.]",
         "text": "1. Was she studying English? (✓) → [*Yes, she was.|Yes, she were.|Yes, she did.]\n"
                 "2. Were they dancing? (✗) → [*No, they weren't.|No, they wasn't.|No, they didn't.]\n"
                 "3. Was he sleeping? (✗) → [*No, he wasn't.|No, he weren't.|No, he isn't.]\n"
                 "4. Were you working at 8 p.m.? (✓) → [*Yes, I was.|Yes, I were.|Yes, I am.]"},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas (exercício da aula).",
         "example": "Were they eating cake? → No, they weren't. They were eating sushi.",
         "pairs": [
             {"left": "Was he eating pizza?", "right": "No, he wasn't. He was eating a hot dog."},
             {"left": "Was she eating salad?", "right": "No, she wasn't. She was eating pizza."},
             {"left": "What was he doing at 7 p.m. last night?", "right": "He was cooking."},
             {"left": "What was she doing?", "right": "She was reading a book."},
         ]},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza as frases da aula.",
         "example": "Minha melhor amiga estava assistindo televisão. → My best friend was watching TV.",
         "text": "1. O meu irmão estava cantando no banho. → [My brother was singing in the shower.]\n"
                 "2. Elas não estavam jogando tênis às 8:00. → [They weren't playing tennis at 8.|"
                 "They were not playing tennis at 8.|They weren't playing tennis at 8:00.|They were not playing tennis at 8:00.|"
                 "They weren't playing tennis at eight.|They were not playing tennis at eight.]\n"
                 "3. Ela estava usando salto alto na festa. → [She was wearing high heels at the party.]"},
    ],
}

AULA8_LISTENING = {
    "title": "Listening — the detective",
    "lesson": 8,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Atenção: WAS / WERE quase não aparecem na fala rápida (\"uəz\", \"uər\"), mas o -ING é bem claro.",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"They were dancing.\" → were dancing",
         "audio": f"{AUDIO}/aula8-forms.m4a",
         "text": "1. She [*was working|is working|worked] last Saturday.\n2. They [*weren't playing|aren't playing|"
                 "were playing] basketball.\n3. [*Was the baby crying|Is the baby crying|Was the baby cry]?\n"
                 "4. We [*were dancing|are dancing|danced] at the party.\n5. He [*wasn't sleeping|was sleeping|isn't sleeping]."},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"She was working last Saturday.\" → She [was working] last Saturday.",
         "audio": f"{AUDIO}/aula8-dictation.m4a",
         "text": "1. They [were playing] soccer at this time yesterday.\n2. She [wasn't|was not] baking a cake last Saturday.\n"
                 "3. [Were] you having a party yesterday?\n4. My brother was [singing] in the shower."},
        {"type": "info",
         "prompt": "Now listen: a detective asks Ms. Lane some questions.",
         "translation": "Agora ouça: alguém pegou dinheiro do escritório ontem à noite, e um detetive faz perguntas "
                        "para a Sra. Lane. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula8-detective.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Where was Ms. Lane at nine o'clock? → [At home.]",
         "text": "1. What were Ms. Lane and her husband watching? → [*A soccer game.|A movie.|The news.]\n"
                 "2. What was her husband doing at ten? → [*He was sleeping on the sofa.|He was watching TV.|"
                 "He was talking on the phone.]\n"
                 "3. Who was Ms. Lane talking to at ten thirty? → [*Her sister.|Her husband.|Mark.]\n"
                 "4. What was Mark doing? → [*He was having dinner at a restaurant.|He was working late.|"
                 "He was watching a soccer game.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Someone took money from the office. → True",
         "statements": [
             {"text": "Brazil was playing.", "answer": True, "translation": "O Brasil estava jogando."},
             {"text": "Mark was working late last night.", "answer": False,
              "translation": "O Mark estava trabalhando até tarde ontem à noite."},
             {"text": "Ms. Lane's sister lives in Portugal.", "answer": True, "translation": "A irmã da Sra. Lane mora em Portugal."},
         ]},
    ],
}

AULA8_SPEAKING = {
    "title": "Speaking — what were you doing?",
    "lesson": 8,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: no -ING, a língua toca o céu da boca lá atrás e o G quase não aparece: \"uórking\", \"plêing\".",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the verbs.",
         "translation": "Ouça e repita os verbos da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula8-say-w{i}.m4a"} for i, t in enumerate(
             ["dance", "work", "sleep", "swim", "read", "study", "play", "watch", "walk", "eat", "drive", "drink"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "\"She was working last Saturday.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula8-say-s{i}.m4a"} for i, t in enumerate(
             ["She was working last Saturday.", "They were playing soccer at this time yesterday.",
              "She wasn't baking a cake last Saturday.", "They weren't having a party yesterday.",
              "Was the baby crying at two o'clock in the morning?", "Were they dancing? No, they weren't."], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOU.",
         "translation": "Agora responda às perguntas sobre VOCÊ com uma frase completa.",
         "example": "\"What were you doing at seven p.m. last night?\" → \"I was cooking dinner.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula8-say-y{i}.m4a"} for i, t in enumerate(
             ["What were you doing at seven p.m. last night?", "What were you doing at this time yesterday?",
              "Were you studying English last Saturday?", "What was your best friend doing yesterday afternoon?"], 1)]},
    ],
}

AULA8_READING = {
    "title": "Reading — the blackout",
    "lesson": 8,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto sobre a noite em que faltou luz no prédio. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula8-reading.m4a",
         "text": "THE BLACKOUT\n\n"
                 "Yesterday at 8 p.m., all the lights in my building went out for an hour. "
                 "This is what my neighbors were doing at that time.\n"
                 "Mrs. Rosa, in apartment 101, was baking a cake. Her oven stopped, and the cake wasn't ready!\n"
                 "The Silva kids, in 102, weren't doing their homework. They were playing video games!\n"
                 "Mr. Tanaka, in 201, was taking a shower… in the dark!\n"
                 "Julia, in 202, was studying for a test, and her dog was sleeping under the table.\n"
                 "And in my apartment? I was cooking dinner. And my husband? He wasn't helping me. "
                 "He was watching a soccer game on TV.\n"
                 "After the blackout, we all were in the hall, with candles, talking and laughing. It was a fun night!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "What was Mrs. Rosa doing? → [She was baking a cake.]",
         "text": "1. What were the Silva kids doing? → [*They were playing video games.|They were doing their homework.|"
                 "They were sleeping.]\n"
                 "2. What was Mr. Tanaka doing? → [*He was taking a shower.|He was cooking dinner.|He was studying.]\n"
                 "3. Where was Julia's dog sleeping? → [*Under the table.|On the sofa.|In the hall.]\n"
                 "4. What was the writer's husband doing? → [*He was watching a soccer game.|He was helping her.|"
                 "He was baking a cake.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "The blackout was at 8 p.m. → True",
         "statements": [
             {"text": "Julia was studying for a test.", "answer": True, "translation": "A Julia estava estudando para uma prova."},
             {"text": "The writer was cooking dinner.", "answer": True, "translation": "A pessoa que escreveu estava fazendo o jantar."},
             {"text": "It was a terrible night.", "answer": False, "translation": "Foi uma noite horrível."},
         ]},
        {"type": "fill",
         "prompt": "Complete with the verbs from the text.",
         "translation": "Complete com os verbos do texto.",
         "example": "Mrs. Rosa [was baking] a cake.",
         "text": "1. The Silva kids [weren't|were not] doing their homework.\n2. Mr. Tanaka [was taking] a shower.\n"
                 "3. My husband [wasn't|was not] helping me."},
    ],
}

AULA8_WRITING = {
    "title": "Writing — at this time yesterday",
    "lesson": 8,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ I was … -ing · We were … -ing · He wasn't … -ing · Were you … -ing? · "
                   "Lembre das regras do -ING: dancing, shopping, studying.",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Make the sentences negative and then make questions.",
         "translation": "Passe as frases para a negativa e depois para a interrogativa.",
         "example": "She was studying English. → She wasn't studying English. → Was she studying English?",
         "text": "1. They were dancing. → [They weren't dancing.|They were not dancing.] → [Were they dancing?]\n"
                 "2. He was driving. → [He wasn't driving.|He was not driving.] → [Was he driving?]"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Ela estava trabalhando no sábado passado. → She was working last Saturday.",
         "text": "1. Eles estavam jogando futebol neste horário ontem. → [They were playing soccer at this time yesterday.|"
                 "They were playing football at this time yesterday.]\n"
                 "2. Você estava dormindo? → [Were you sleeping?]"},
        {"type": "free",
         "prompt": "What were you and your family doing yesterday at 8 p.m.? Write about 4 people.",
         "translation": "O que você e a sua família estavam fazendo ontem às 8 da noite? Escreva sobre 4 pessoas.",
         "example": "Yesterday at 8 p.m., I was studying English.",
         "model_answer": "Yesterday at 8 p.m., I was studying English in my bedroom.\n"
                         "My parents were in the kitchen. My mother was cooking dinner, and my father was helping her.\n"
                         "My sister wasn't studying. She was talking to her boyfriend on the phone.\n"
                         "And our cat? It was sleeping on the sofa!",
         "keywords": ["was", "were"], "min_words": 30, "points": 4},
    ],
}

AULA8_VIDEO = _video(8, AULA8_TOPIC, "Video — What were they doing?",
                     "a Julia conta o que cada pessoa da família estava fazendo no sábado às 3 da tarde: was / were + -ING.",
                     "aula8-video", [
    _q("What was Tom doing at three o'clock?", "O que o Tom estava fazendo às três horas?", "He was cooking.",
       "He was sleeping.", "He was running.", "He was watching TV."),
    _q("Was Ana studying?", "A Ana estava estudando?", "No, she wasn't. She was watching TV.",
       "Yes, she was.", "No, she didn't.", "Yes, she was studying."),
    _q("What was Grandma doing?", "O que a avó estava fazendo?", "She was washing the dishes.", "She was playing soccer.",
       "She was sleeping.", "She was watching TV."),
    _q("What were the cousins doing?", "O que os primos estavam fazendo?", "They were playing soccer.",
       "They were swimming.", "They were cooking.", "They was playing soccer."),
    _q("What was Max doing?", "O que o Max estava fazendo?", "He was sleeping.", "He was running.",
       "He was eating.", "He was playing."),
])


# ---------- Aula 09 — Past Simple × Past Continuous (https://youtu.be/ykQuOBzaufE) ----------

AULA9_TOPIC = "Aula 09 — Past Simple vs Past Continuous"

AULA9_VOCAB = {
    "title": "Superstitions: vocabulary",
    "lesson": 9,
    "description": "Vocabulário da aula: good luck = boa sorte · bad luck = azar, má sorte · broken mirror = espelho quebrado · "
                   "magic = mágica · ghost = fantasma (o H não é pronunciado: \"gôust\") · haunted = mal-assombrado · "
                   "cemetery = cemitério · lucky number = número da sorte · full moon = lua cheia · fear = medo.\n"
                   "Are you a superstitious person? → Yes, I am. / No, I'm not. · Do you believe in ghosts? → Yes, I do. / "
                   "No, I don't. · Do you have a lucky number? → Yes, I do. It's 7. / No, I don't.",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the words to Portuguese.",
         "translation": "Ligue as palavras ao português.",
         "example": "good luck → boa sorte",
         "pairs": [
             {"left": "bad luck", "right": "azar"},
             {"left": "broken mirror", "right": "espelho quebrado"},
             {"left": "ghost", "right": "fantasma"},
             {"left": "haunted", "right": "mal-assombrado"},
             {"left": "cemetery", "right": "cemitério"},
             {"left": "lucky number", "right": "número da sorte"},
             {"left": "full moon", "right": "lua cheia"},
             {"left": "fear", "right": "medo"},
         ]},
        {"type": "dropdown",
         "prompt": "Complete with the right word.",
         "translation": "Complete com a palavra certa.",
         "example": "Good [luck] on your test!",
         "text": "1. Seven is my [*lucky number|full moon|fear].\n"
                 "2. Some people say a broken mirror brings bad [*luck|magic|ghost].\n"
                 "3. Nobody lives in that old house. People say it's [*haunted|lucky|broken].\n"
                 "4. Tonight the moon is big and round. It's a [*full moon|lucky number|cemetery].\n"
                 "5. My little brother has a [*fear|ghost|luck] of the dark."},
        {"type": "dropdown",
         "prompt": "Choose the right short answer.",
         "translation": "Escolha a resposta curta certa para as perguntas da aula.",
         "example": "Are you a superstitious person? (✓) → [Yes, I am.]",
         "text": "1. Are you a superstitious person? (✗) → [*No, I'm not.|No, I don't.|No, I didn't.]\n"
                 "2. Do you believe in ghosts? (✓) → [*Yes, I do.|Yes, I am.|Yes, I believe.]\n"
                 "3. Do you have a lucky number? (✗) → [*No, I don't.|No, I'm not.|No, I haven't.]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Ghost\" = fantasma. → True",
         "statements": [
             {"text": "We pronounce the letter H in \"ghost\".", "answer": False,
              "translation": "Pronunciamos a letra H em \"ghost\"."},
             {"text": "\"Bad luck\" = azar.", "answer": True, "translation": "\"Bad luck\" = azar."},
             {"text": "A haunted house is a house with ghosts.", "answer": True,
              "translation": "Uma casa mal-assombrada é uma casa com fantasmas."},
         ]},
    ],
}

AULA9_WHEN = {
    "title": "Past continuous + when + past simple",
    "lesson": 9,
    "description": "PAST CONTINUOUS (was / were + verbo-ING) = ação EM PROGRESSO no passado.\n"
                   "PAST SIMPLE = ação COMPLETA, que INTERROMPE a outra. Ligamos as duas com WHEN (quando).\n"
                   "I was sleeping when I heard a noise in the kitchen. (Eu estava dormindo quando ouvi um barulho na cozinha.)\n"
                   "Podemos inverter a ordem, mas aí usamos VÍRGULA: When I heard a noise in the kitchen, I was sleeping.\n"
                   "Lembre: negativa do past continuous = wasn't / weren't + ING · negativa do past simple = didn't + forma básica.",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Past continuous or past simple? Choose.",
         "translation": "Past continuous (ação em progresso) ou past simple (a ação que interrompe)? Escolha.",
         "example": "I [was sleeping] when I [heard] a noise.",
         "text": "1. I [*was putting|put] on makeup when I [*broke|was breaking] the mirror.\n"
                 "2. My parents [*were cooking|cooked] when the lights [*went|were going] out.\n"
                 "3. He [*was playing|played] soccer when he [*broke|was breaking] his arm.\n"
                 "4. When I [*left|was leaving] home, my cat [*was sleeping|slept].\n"
                 "5. She [*was taking|took] a shower when the water [*got|was getting] cold."},
        {"type": "fill",
         "prompt": "Make one sentence with WHEN.",
         "translation": "Junte as duas ideias em uma frase com WHEN. Comece pela ação em progresso.",
         "example": "I / sleep — I / hear a noise → I was sleeping when I heard a noise.",
         "text": "1. She / walk in the cemetery — she / see a ghost → "
                 "[She was walking in the cemetery when she saw a ghost.]\n"
                 "2. We / watch TV — the lights / go out → [We were watching TV when the lights went out.]\n"
                 "3. I / read in bed — my phone / ring → [I was reading in bed when my phone rang.]"},
        {"type": "order",
         "prompt": "Put the words in order. Start with WHEN.",
         "translation": "Coloque as palavras em ordem, começando com WHEN. (Quando eu quebrei o espelho, eu estava me maquiando.)",
         "example": "When / heard / I / a noise, / sleeping / I / was → When I heard a noise, I was sleeping.",
         "tokens": ["When", "I", "broke", "the", "mirror,", "I", "was", "putting", "on", "makeup."], "alternatives": []},
        {"type": "choice",
         "prompt": "Which sentence is correct?",
         "translation": "Qual frase está correta?",
         "example": "I was sleeping when I heard a noise. ✓",
         "options": ["When the water got cold, he was taking a shower.", "When the water got cold he was taking a shower.",
                     "When the water was getting cold, he took a shower.", "He was take a shower when the water got cold."],
         "correct": 0},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "WHEN connects the two parts of the sentence. → True",
         "statements": [
             {"text": "The past continuous shows an action in progress.", "answer": True,
              "translation": "O past continuous mostra uma ação em progresso."},
             {"text": "The past simple shows the action that interrupts.", "answer": True,
              "translation": "O past simple mostra a ação que interrompe."},
             {"text": "When the sentence starts with WHEN, we don't use a comma.", "answer": False,
              "translation": "Quando a frase começa com WHEN, não usamos vírgula."},
         ]},
    ],
}

AULA9_LISTENING = {
    "title": "Listening — a night at Grandpa's house",
    "lesson": 9,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Preste atenção: WAS / WERE + ING (estava fazendo) × verbo no passado (fez).",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"I was reading when I heard a noise.\" → was reading",
         "audio": f"{AUDIO}/aula9-forms.m4a",
         "text": "1. I [*was sleeping|slept] when I [*heard|was hearing] a noise.\n"
                 "2. They [*were cooking|cooked] when the lights went out.\n"
                 "3. He was playing soccer when he [*broke|was breaking] his arm.\n"
                 "4. When I left home, my cat [*was sleeping|slept].\n"
                 "5. She [*was taking|took] a shower when the water got cold."},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"Good luck!\" → Good [luck]!",
         "audio": f"{AUDIO}/aula9-dictation.m4a",
         "text": "1. I was putting on makeup when I broke the [mirror].\n2. Do you believe in [ghosts]?\n"
                 "3. Seven is my lucky [number].\n4. We [were] walking in the cemetery when we saw a ghost."},
        {"type": "info",
         "prompt": "Now listen: Pedro tells Lucy about a crazy night.",
         "translation": "Agora ouça: o Pedro conta para a Lucy sobre uma noite maluca na casa velha do avô dele. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula9-story.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Pedro looks [tired].",
         "text": "1. Where was Pedro staying? → [*At his grandfather's old house.|At a hotel.|At Lucy's house.]\n"
                 "2. What was Pedro doing when he heard a noise? → [*He was reading in bed.|He was sleeping.|He was eating cake.]\n"
                 "3. What happened when he was walking to the kitchen? → [*The lights went out.|He saw a ghost.|It started to rain.]\n"
                 "4. Who was in the kitchen? → [*His grandfather.|A ghost.|Lucy.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "The house is near the cemetery. → True",
         "statements": [
             {"text": "There was a full moon.", "answer": True, "translation": "Tinha lua cheia."},
             {"text": "Pedro saw a ghost.", "answer": False, "translation": "O Pedro viu um fantasma."},
             {"text": "Pedro's grandfather was eating cake in the dark.", "answer": True,
              "translation": "O avô do Pedro estava comendo bolo no escuro."},
         ]},
    ],
}

AULA9_SPEAKING = {
    "title": "Speaking — superstitions",
    "lesson": 9,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: GHOST = \"gôust\" (sem o som do H) · HAUNTED = \"rónted\" · FEAR = \"fíar\".",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the words.",
         "translation": "Ouça e repita o vocabulário da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula9-say-w{i}.m4a"} for i, t in enumerate(
             ["good luck", "bad luck", "broken mirror", "magic", "ghost", "haunted", "cemetery", "lucky number",
              "full moon", "fear"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "\"I was sleeping when I heard a noise in the kitchen.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula9-say-s{i}.m4a"} for i, t in enumerate(
             ["I was sleeping when I heard a noise in the kitchen.", "I was putting on makeup when I broke the mirror.",
              "My parents were cooking when the lights went out.", "He was playing soccer when he broke his arm.",
              "When I left home, my cat was sleeping.", "When the water got cold, he was taking a shower."], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOU.",
         "translation": "Agora responda às perguntas sobre VOCÊ com uma frase completa.",
         "example": "\"Do you believe in ghosts?\" → \"No, I don't.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula9-say-y{i}.m4a"} for i, t in enumerate(
             ["Are you a superstitious person?", "Do you believe in ghosts?",
              "Do you have a lucky number? If you do, what number is it?",
              "What were you doing at eight o'clock last night?"], 1)]},
    ],
}

AULA9_READING = {
    "title": "Reading — the broken mirror",
    "lesson": 9,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Bruna's text.",
         "translation": "Leia e ouça o texto da Bruna sobre um espelho quebrado. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula9-reading.m4a",
         "text": "THE BROKEN MIRROR\n\n"
                 "My grandmother is very superstitious. She says a broken mirror brings seven years of bad luck.\n"
                 "Last Friday, I was getting ready for a party. I was putting on makeup in the bathroom when my cat jumped "
                 "on the sink. I dropped the mirror, and it broke!\n"
                 "My grandmother was watching TV in the living room when she heard the noise. She ran to the bathroom and "
                 "said, \"Oh, no! Seven years of bad luck!\"\n"
                 "I don't believe in superstitions, but that night, some bad things happened. I was walking to the bus stop "
                 "when it started to rain. And when I arrived at the party, I was all wet!\n"
                 "But then, I was dancing with my friends when I met a very nice boy. His name is Rafael, and today he is "
                 "my boyfriend!\n"
                 "So, was the broken mirror bad luck? I don't think so!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Who is superstitious? → [Bruna's grandmother.]",
         "text": "1. What was Bruna doing when the cat jumped on the sink? → [*She was putting on makeup.|"
                 "She was watching TV.|She was dancing.]\n"
                 "2. What was her grandmother doing? → [*She was watching TV.|She was sleeping.|She was cooking.]\n"
                 "3. What happened when Bruna was walking to the bus stop? → [*It started to rain.|She lost her phone.|"
                 "She met Rafael.]\n"
                 "4. What was Bruna doing when she met Rafael? → [*She was dancing with her friends.|"
                 "She was walking to the bus stop.|She was putting on makeup.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "The mirror broke. → True",
         "statements": [
             {"text": "Bruna believes in superstitions.", "answer": False, "translation": "A Bruna acredita em superstições."},
             {"text": "Bruna was all wet at the party.", "answer": True, "translation": "A Bruna estava toda molhada na festa."},
             {"text": "Rafael is Bruna's boyfriend today.", "answer": True, "translation": "O Rafael é namorado da Bruna hoje."},
         ]},
        {"type": "fill",
         "prompt": "Complete with the verbs from the text.",
         "translation": "Complete com os verbos do texto (past continuous ou past simple).",
         "example": "I [was getting] ready for a party.",
         "text": "1. I was putting on makeup when my cat [jumped] on the sink.\n"
                 "2. My grandmother [was watching] TV in the living room.\n"
                 "3. I [was walking] to the bus stop when it started to rain."},
    ],
}

AULA9_WRITING = {
    "title": "Writing — a strange day",
    "lesson": 9,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Ação em progresso: was / were + ING · ação que interrompe: verbo no passado.\n"
                   "I was walking home when I saw a black cat. · When I saw a black cat, I was walking home. (com vírgula!)",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Rewrite the sentences. Start with WHEN.",
         "translation": "Reescreva as frases começando com WHEN. Não esqueça a vírgula!",
         "example": "I was sleeping when I heard a noise. → When I heard a noise, I was sleeping.",
         "text": "1. My parents were cooking when the lights went out. → [When the lights went out, my parents were cooking.]\n"
                 "2. He was playing soccer when he broke his arm. → [When he broke his arm, he was playing soccer.]"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu estava dormindo quando ouvi um barulho. → I was sleeping when I heard a noise.",
         "text": "1. Ela estava andando no cemitério quando viu um fantasma. → "
                 "[She was walking in the cemetery when she saw a ghost.]\n"
                 "2. Nós estávamos assistindo TV quando o telefone tocou. → [We were watching TV when the phone rang.]"},
        {"type": "free",
         "prompt": "Write about a strange, funny or unlucky day. What were you doing? What happened? "
                   "Use the past continuous, WHEN and the past simple.",
         "translation": "Escreva sobre um dia estranho, engraçado ou de azar. O que você estava fazendo? O que aconteceu? "
                        "Use o past continuous, WHEN e o past simple.",
         "example": "Last Monday, I was walking to work when it started to rain.",
         "model_answer": "Last Monday was a very unlucky day!\n"
                         "I was walking to work when it started to rain, and I didn't have an umbrella.\n"
                         "When I arrived at the office, my boss was waiting for me.\n"
                         "Then, I was drinking coffee when I dropped the cup on my computer!\n"
                         "But in the evening, I was watching TV when my best friend called me with good news.",
         "keywords": ["when", "was"], "min_words": 30, "points": 4},
    ],
}

AULA9_VIDEO = _video(9, AULA9_TOPIC, "Video — A spooky night",
                     "a Nina conta uma noite assustadora na casa da avó: past continuous + when + past simple.",
                     "aula9-video", [
    _q("Where was Nina last Friday?", "Onde a Nina estava na sexta-feira passada?",
       "At her grandmother's old house.", "At a party.", "At the cemetery.", "At school."),
    _q("What was Nina doing when she heard a noise?", "O que a Nina estava fazendo quando ouviu um barulho?",
       "She was reading in bed.", "She was sleeping.", "She was cooking.", "She was watching TV."),
    _q("What happened when Nina was walking to the kitchen?", "O que aconteceu quando a Nina estava indo para a cozinha?",
       "The wind blew out the candle.", "She saw a ghost.", "The lights came on.", "She broke a mirror."),
    _q("What did Nina see in the dark?", "O que a Nina viu no escuro?", "Two yellow eyes.", "A ghost.",
       "Her grandmother.", "A full moon."),
    _q("What was the cat doing?", "O que o gato estava fazendo?", "He was eating Nina's cake.",
       "He was sleeping in bed.", "He was playing with a candle.", "He was walking in the cemetery."),
])

# ---------- Aula 10 — Prepositions: IN, ON, AT (https://youtu.be/74iEFBXWt6Q) ----------

AULA10_TOPIC = "Aula 10 — Prepositions: IN, ON, AT"

AULA10_TIME = {
    "title": "In, on, at: time",
    "lesson": 10,
    "description": "Pense no TRIÂNGULO da aula: em cima (parte larga) = informação GERAL · no meio = mais específica · "
                   "na ponta = MUITO específica.\n"
                   "IN → séculos, décadas, anos, meses: in the 21st century · in the 1990s · in 1990 · in May\n"
                   "ON → dias da semana e datas: on Monday · on Mondays and Wednesdays · on May 28th\n"
                   "AT → horas: at 7 p.m. · at 9 a.m. · at 6 o'clock\n"
                   "I have English class on Monday at 7 p.m. · I was born in May. · I was born on May 28th.",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "In, on or at? Put each word in the right group.",
         "translation": "In, on ou at? Coloque cada expressão de tempo no grupo certo.",
         "example": "1990 → in · Monday → on · 7 p.m. → at",
         "categories": ["in", "on", "at"],
         "words": [
             {"text": "1945", "category": "in"}, {"text": "July", "category": "in"},
             {"text": "the 1990s", "category": "in"}, {"text": "the 21st century", "category": "in"},
             {"text": "Saturday", "category": "on"}, {"text": "May 28th", "category": "on"},
             {"text": "Mondays and Wednesdays", "category": "on"},
             {"text": "9 a.m.", "category": "at"}, {"text": "6 o'clock", "category": "at"}, {"text": "7:30 p.m.", "category": "at"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose in, on or at.",
         "translation": "Escolha in, on ou at (exercício da aula).",
         "example": "I have English class [on] Monday [at] 7 p.m.",
         "text": "1. I study English [*on|in|at] Mondays and Wednesdays.\n2. My father was born [*in|on|at] 1945.\n"
                 "3. My brother's birthday is [*in|on|at] July.\n4. I start work [*at|on|in] 9 a.m.\n"
                 "5. I was born [*on|in|at] May 28th.\n6. My English class is [*at|in|on] 7 p.m."},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula (o triângulo).",
         "example": "We use IN for years. → True",
         "statements": [
             {"text": "IN is for very specific information.", "answer": False,
              "translation": "IN é para informações muito específicas."},
             {"text": "We use ON for days of the week and dates.", "answer": True,
              "translation": "Usamos ON para dias da semana e datas."},
             {"text": "We use AT for times (hours).", "answer": True, "translation": "Usamos AT para horários."},
             {"text": "We say \"I was born in May 28th\".", "answer": False,
              "translation": "Dizemos \"I was born in May 28th\"."},
         ]},
    ],
}

AULA10_PLACE = {
    "title": "In, on, at: places",
    "lesson": 10,
    "description": "O mesmo triângulo vale para LUGARES:\n"
                   "IN → país, cidade, bairro (geral): I live in Brazil. · I was born in São Paulo. · in Copacabana\n"
                   "ON → rua ou avenida, sem o número (mais específico): I live on Paulista Avenue.\n"
                   "AT → endereço completo e lugares exatos (muito específico): I live at 250 Ocean Avenue. · "
                   "I'm at home. · I'm at the hospital.",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "In, on or at? Put each place in the right group.",
         "translation": "In, on ou at? Coloque cada lugar no grupo certo.",
         "example": "Brazil → in · Paulista Avenue → on · home → at",
         "categories": ["in", "on", "at"],
         "words": [
             {"text": "São Paulo", "category": "in"}, {"text": "Italy", "category": "in"},
             {"text": "Copacabana (neighborhood)", "category": "in"},
             {"text": "Flores Street", "category": "on"}, {"text": "Ocean Avenue", "category": "on"},
             {"text": "250 Ocean Avenue", "category": "at"}, {"text": "the hospital", "category": "at"},
             {"text": "school", "category": "at"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose in, on or at.",
         "translation": "Escolha in, on ou at.",
         "example": "I live [in] Brazil.",
         "text": "1. She lives [*on|in|at] Paulista Avenue.\n2. They live [*at|on|in] 35 Flores Street.\n"
                 "3. Where are you? I'm [*at|in|on] home.\n4. I was born [*in|on|at] Brasília.\n"
                 "5. My mother is [*at|on|in] the hospital."},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas da aula às respostas.",
         "example": "Where do you live? → I live in Brasília.",
         "pairs": [
             {"left": "Where were you born?", "right": "I was born in São Paulo."},
             {"left": "When were you born?", "right": "I was born in 1990."},
             {"left": "When is your birthday?", "right": "It's on May 28th."},
             {"left": "What time do you get up?", "right": "I get up at 6 a.m."},
             {"left": "Where are you?", "right": "I'm at home."},
         ]},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu moro no Brasil. → I live in Brazil.",
         "text": "1. Eu nasci em 1990. → [I was born in 1990.]\n"
                 "2. Ela mora na Avenida Paulista. → [She lives on Paulista Avenue.]\n"
                 "3. Eu estou no hospital. → [I'm at the hospital.|I am at the hospital.]"},
    ],
}

AULA10_LISTENING = {
    "title": "Listening — at the English school",
    "lesson": 10,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: IN, ON e AT são palavras curtas e fracas na frase. Preste atenção na palavra seguinte: "
                   "ano/mês → in · dia/data → on · hora/endereço → at.",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the preposition.",
         "translation": "Ouça e escolha a preposição.",
         "example": "Você ouve: \"I live in Brazil.\" → in",
         "audio": f"{AUDIO}/aula10-preps.m4a",
         "text": "1. I was born [*in|on|at] 1990.\n2. My birthday is [*on|in|at] May 28th.\n3. I start work [*at|on|in] 9 a.m.\n"
                 "4. She lives [*on|in|at] Paulista Avenue.\n5. We live [*at|on|in] 35 Flores Street.\n6. I'm [*at|in|on] home."},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"I live in Brazil.\" → I live [in] Brazil.",
         "audio": f"{AUDIO}/aula10-dictation.m4a",
         "text": "1. I study English [on] Mondays and Wednesdays.\n2. My father was born [in] 1945.\n"
                 "3. My brother's birthday is in [July].\n4. I have English class [at] 7 p.m."},
        {"type": "info",
         "prompt": "Now listen: Laura registers at an English school.",
         "translation": "Agora ouça: a Laura faz a matrícula em uma escola de inglês e o recepcionista pede algumas "
                        "informações. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula10-school.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Laura's last name is [Costa].",
         "text": "1. Where was Laura born? → [*In Recife.|In São Paulo.|In Rio.]\n"
                 "2. When was she born? → [*On March 3rd, 1995.|On May 3rd, 1995.|On March 3rd, 1999.]\n"
                 "3. What's her address? → [*120 Augusta Street.|20 Augusta Street.|120 Paulista Avenue.]\n"
                 "4. What time is her class? → [*At 7 p.m.|At 6 p.m.|At 9 a.m.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Laura wants to study English. → True",
         "statements": [
             {"text": "Laura lives in Recife now.", "answer": False, "translation": "A Laura mora em Recife agora."},
             {"text": "Laura wants classes on Tuesdays and Thursdays.", "answer": True,
              "translation": "A Laura quer aulas às terças e quintas."},
             {"text": "Laura finishes work at 6.", "answer": True, "translation": "A Laura sai do trabalho às 6."},
         ]},
    ],
}

AULA10_SPEAKING = {
    "title": "Speaking — in, on, at",
    "lesson": 10,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: IN, ON e AT são fracas e se ligam à palavra seguinte: \"i-nnineteen ninety\", \"a-thome\".",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula10-say-s{i}.m4a"} for i, t in enumerate(
             ["I have English class on Monday at 7 p.m.", "I was born in 1990.", "I was born on May 28th.",
              "I live in Brazil.", "I live on Paulista Avenue.", "I'm at home."], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions from the lesson about YOU.",
         "translation": "Agora responda às perguntas do início da aula sobre VOCÊ, com a preposição certa.",
         "example": "\"When is your birthday?\" → \"My birthday is on May 28th.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula10-say-y{i}.m4a"} for i, t in enumerate(
             ["Where were you born?", "When were you born?", "When is your birthday?", "When do you have English class?",
              "What day is it today?", "What time do you get up?", "Where do you live?"], 1)]},
    ],
}

AULA10_READING = {
    "title": "Reading — my grandfather's story",
    "lesson": 10,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto sobre a história do avô. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula10-reading.m4a",
         "text": "MY GRANDFATHER'S STORY\n\n"
                 "My grandfather, Antônio, was born in Italy, in a small village, in 1945. "
                 "He was born on a cold winter day: on January 10th.\n"
                 "In 1960, his family moved to Brazil. They lived in São Paulo, on Liberdade Street.\n"
                 "He met my grandmother in 1968, at a party. They got married on June 15th, 1970, at a small church.\n"
                 "Today, my grandparents live at 45 Flores Street, in Campinas.\n"
                 "Every Sunday, we have lunch at their house at noon. My grandfather always says: "
                 "\"Lunch is at twelve o'clock, not at five past twelve!\""},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Where was Antônio born? → [In Italy.]",
         "text": "1. When was he born? → [*On January 10th, 1945.|In June 1970.|On June 15th, 1960.]\n"
                 "2. When did his family move to Brazil? → [*In 1960.|In 1945.|In 1968.]\n"
                 "3. Where did he meet his wife? → [*At a party.|At a church.|On Liberdade Street.]\n"
                 "4. Where do the grandparents live today? → [*At 45 Flores Street, in Campinas.|On Liberdade Street, "
                 "in São Paulo.|In a small village in Italy.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Antônio was born in a small village. → True",
         "statements": [
             {"text": "Antônio got married in 1968.", "answer": False, "translation": "O Antônio se casou em 1968."},
             {"text": "The family has lunch together on Sundays.", "answer": True,
              "translation": "A família almoça junta aos domingos."},
             {"text": "Lunch is at five past twelve.", "answer": False, "translation": "O almoço é ao meio-dia e cinco."},
         ]},
        {"type": "fill",
         "prompt": "Complete with in, on or at, according to the text.",
         "translation": "Complete com in, on ou at, de acordo com o texto.",
         "example": "He was born [in] Italy.",
         "text": "1. He was born [on] January 10th.\n2. They lived [on] Liberdade Street.\n"
                 "3. My grandparents live [at] 45 Flores Street.\n4. We have lunch [at] noon."},
    ],
}

AULA10_WRITING = {
    "title": "Writing — all about me",
    "lesson": 10,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Tempo: in + ano / mês · on + dia / data · at + hora.\n"
                   "Lugar: in + país / cidade / bairro · on + rua · at + endereço / home.",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Complete with in, on or at.",
         "translation": "Complete com in, on ou at.",
         "example": "I was born [in] 1990.",
         "text": "1. My birthday is [on] October 5th.\n2. I get up [at] 6:30.\n3. We go to the beach [in] January.\n"
                 "4. My office is [on] Paulista Avenue.\n5. I live [in] Curitiba.\n6. I'm [at] school now."},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu tenho aula de inglês na segunda às 7 da noite. → I have English class on Monday at 7 p.m.",
         "text": "1. Meu aniversário é em julho. → [My birthday is in July.]\n"
                 "2. Eu comecei a trabalhar em 2015. → [I started work in 2015.|I started working in 2015.|"
                 "I started to work in 2015.]"},
        {"type": "free",
         "prompt": "Answer the questions from the lesson about you: Where were you born? When were you born? "
                   "When is your birthday? When do you have English class? What time do you get up? Where do you live?",
         "translation": "Responda às perguntas da aula sobre você: Onde você nasceu? Quando? Quando é o seu aniversário? "
                        "Quando você tem aula de inglês? A que horas você acorda? Onde você mora?",
         "example": "I was born in Salvador, in 1995.",
         "model_answer": "I was born in Salvador, in 1995.\n"
                         "My birthday is on March 12th.\n"
                         "I have English class on Tuesdays and Thursdays at 8 p.m.\n"
                         "I get up at 6:30 on weekdays.\n"
                         "I live in Recife, on Boa Viagem Avenue.",
         "keywords": ["in", "on", "at"], "min_words": 30, "points": 4},
    ],
}

AULA10_VIDEO = _video(10, AULA10_TOPIC, "Video — All about me",
                      "a Ana fala de onde mora, quando nasceu e da rotina dela: in, on, at para lugares e tempo.",
                      "aula10-video", [
    _q("Where does Ana live?", "Onde a Ana mora?", "In Rio de Janeiro.", "On Rio de Janeiro.", "At Rio de Janeiro.",
       "In São Paulo."),
    _q("Complete: Ana lives ___ Ocean Avenue.", "Complete: a Ana mora ___ Ocean Avenue (sem o número).", "on", "in",
       "at", "to"),
    _q("When is Ana's birthday?", "Quando é o aniversário da Ana?", "On May 28th.", "In May 28th.", "At May 28th.",
       "On March 28th."),
    _q("What time does Ana get up on weekdays?", "A que horas a Ana acorda nos dias de semana?", "At six o'clock.",
       "At nine a.m.", "At seven p.m.", "On six o'clock."),
    _q("When does Ana have English class?", "Quando a Ana tem aula de inglês?", "On Mondays and Wednesdays at 7 p.m.",
       "On Saturdays at 7 a.m.", "In Mondays at 7 p.m.", "On Tuesdays at 9 a.m."),
])

# ---------- Aula 11 — Saying the Dates (https://youtu.be/ljze7DWrtJ4) ----------

AULA11_TOPIC = "Aula 11 — Saying the Dates"

AULA11_ORDINALS = {
    "title": "Ordinal numbers: first, second, third…",
    "lesson": 11,
    "description": "Em inglês, as DATAS usam sempre os números ORDINAIS (1º, 2º, 3º…), não só o dia 1º como em português.\n"
                   "Os 3 diferentes: 1st first · 2nd second · 3rd third. Os outros terminam em TH: 4th fourth · 6th sixth · 7th seventh…\n"
                   "Atenção na escrita: 5th fifth · 8th eighth · 9th ninth · 12th twelfth · 20th twentieth · 30th thirtieth\n"
                   "21 a 29: o primeiro número fica normal e só o último vira ordinal: 21st twenty-first · 22nd twenty-second · "
                   "23rd twenty-third · 24th twenty-fourth\n"
                   "O símbolo são as 2 últimas letras: first → 1ST · second → 2ND · third → 3RD · fourth → 4TH.\n"
                   "Pronúncia do TH: a língua entre os dentes, com um soprinho (não é F!).",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the numbers to the ordinal numbers.",
         "translation": "Ligue os números aos números ordinais.",
         "example": "1st → first",
         "pairs": [
             {"left": "2nd", "right": "second"},
             {"left": "3rd", "right": "third"},
             {"left": "5th", "right": "fifth"},
             {"left": "8th", "right": "eighth"},
             {"left": "9th", "right": "ninth"},
             {"left": "12th", "right": "twelfth"},
             {"left": "20th", "right": "twentieth"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the right ending.",
         "translation": "Escolha a terminação certa do símbolo (as 2 últimas letras da palavra).",
         "example": "4 → 4[th] (fourth)",
         "text": "1. 1[*st|nd|rd|th]\n2. 2[*nd|st|rd|th]\n3. 3[*rd|st|nd|th]\n4. 11[*th|st|nd|rd]\n"
                 "5. 21[*st|th|nd|rd]\n6. 22[*nd|th|st|rd]\n7. 23[*rd|th|st|nd]\n8. 31[*st|th|nd|rd]"},
        {"type": "fill",
         "prompt": "Write the ordinal numbers in words.",
         "translation": "Escreva os números ordinais por extenso.",
         "example": "7th → seventh",
         "text": "1. 4th → [fourth]\n2. 6th → [sixth]\n3. 10th → [tenth]\n4. 15th → [fifteenth]\n"
                 "5. 21st → [twenty-first|twenty first]\n6. 30th → [thirtieth]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "In English, we use ordinal numbers for dates. → True",
         "statements": [
             {"text": "In English, we only use an ordinal number for the first day of the month.", "answer": False,
              "translation": "Em inglês, só usamos número ordinal para o primeiro dia do mês."},
             {"text": "The TH sound is like the F sound.", "answer": False,
              "translation": "O som do TH é igual ao som do F."},
             {"text": "We don't pronounce the GH in \"eighth\".", "answer": True,
              "translation": "Não pronunciamos o GH em \"eighth\"."},
             {"text": "\"Twenty-second\" is the same as 22nd.", "answer": True,
              "translation": "\"Twenty-second\" é o mesmo que 22º."},
         ]},
    ],
}

AULA11_DATES = {
    "title": "Years and dates: US and UK",
    "lesson": 11,
    "description": "ANOS: dividimos em 2 partes → 1997 = nineteen ninety-seven · 1850 = eighteen fifty\n"
                   "Termina em 00 → HUNDRED: 1500 = fifteen hundred · 1800 = eighteen hundred\n"
                   "Zero no meio → \"OH\": 1705 = seventeen oh five\n"
                   "2000 = two thousand · de 2001 em diante, as duas formas: 2005 = two thousand five / twenty oh five · "
                   "2023 = twenty twenty-three / two thousand twenty-three\n"
                   "DATAS nos ESTADOS UNIDOS: mês + dia (ordinal) → July 24th = \"July twenty-fourth\" · December 25th\n"
                   "  (exceção: the Fourth of July)\n"
                   "No RESTO DO MUNDO (e no Brasil): dia + mês, com THE e OF → the 24th of July = \"the twenty-fourth of July\"\n"
                   "Cuidado: 6/8 nos EUA é June 8th; no resto do mundo é the 6th of August!",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "How do we say these years?",
         "translation": "Como falamos estes anos em inglês?",
         "example": "1997 → [nineteen ninety-seven]",
         "text": "1. 1500 → [*fifteen hundred|one thousand five hundred|fifteen zero zero]\n"
                 "2. 1850 → [*eighteen fifty|one eight five zero|eighteen hundred fifty]\n"
                 "3. 1705 → [*seventeen oh five|seventeen five|seventy five]\n"
                 "4. 2000 → [*two thousand|twenty hundred|twenty oh oh]\n"
                 "5. 1998 → [*nineteen ninety-eight|one thousand nine hundred ninety-eight|nineteen nine eight]"},
        {"type": "group",
         "prompt": "United States or the rest of the world? Put each date in the right group.",
         "translation": "Estados Unidos ou resto do mundo? Coloque cada data no grupo certo.",
         "example": "December 25th → United States · the 25th of December → rest of the world",
         "categories": ["United States", "rest of the world"],
         "words": [
             {"text": "July 24th", "category": "United States"},
             {"text": "October 25th", "category": "United States"},
             {"text": "February 21st", "category": "United States"},
             {"text": "June 8th", "category": "United States"},
             {"text": "the 24th of July", "category": "rest of the world"},
             {"text": "the 15th of April", "category": "rest of the world"},
             {"text": "the 20th of July", "category": "rest of the world"},
             {"text": "the 13th of December", "category": "rest of the world"},
         ]},
        {"type": "fill",
         "prompt": "Write the dates the American way (month + day).",
         "translation": "Escreva as datas do jeito americano (mês + dia), como no exercício da aula.",
         "example": "25/10 → It's October 25th.",
         "text": "1. 21/02 → It's February [21st].\n2. 08/06 → It's [June] 8th.\n3. 03/05 → It's May [3rd]."},
        {"type": "fill",
         "prompt": "Now write the dates the way the rest of the world says them.",
         "translation": "Agora escreva como o resto do mundo fala (com THE e OF).",
         "example": "15/04 → It's the 15th of April.",
         "text": "1. 20/07 → It's [the] 20th [of] July.\n2. 13/12 → It's the 13th of [December].\n"
                 "3. 01/01 → It's the [1st] of January."},
        {"type": "choice",
         "prompt": "In the United States, what is 6/8?",
         "translation": "Nos Estados Unidos, que data é 6/8?",
         "example": "Nos EUA, o mês vem primeiro.",
         "options": ["June 8th", "the 6th of August", "August 6th", "the 8th of June of August"],
         "correct": 0},
    ],
}

AULA11_LISTENING = {
    "title": "Listening — when is the party?",
    "lesson": 11,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: preste atenção no final das palavras: \"fourth\", \"fifth\", \"sixth\"… e no THE … OF "
                   "quando a pessoa fala o dia antes do mês.",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the number you hear.",
         "translation": "Ouça e escolha o número que você ouve.",
         "example": "Você ouve: \"first\" → 1st",
         "audio": f"{AUDIO}/aula11-ordinals.m4a",
         "text": "1. [*3rd|13th|30th]\n2. [*5th|15th|50th]\n3. [*12th|20th|2nd]\n4. [*8th|18th|80th]\n"
                 "5. [*21st|20th|1st]\n6. [*30th|13th|3rd]"},
        {"type": "fill",
         "prompt": "Dictation: listen and write the dates and years in numbers.",
         "translation": "Ditado: ouça e escreva as datas e os anos em números.",
         "example": "Você ouve: \"May twenty-eighth\" → May [28th]",
         "audio": f"{AUDIO}/aula11-dictation.m4a",
         "text": "1. It's October [25th].\n2. I was born in [1997].\n3. It's the [15th] of April.\n"
                 "4. My birthday is on March [22nd].\n5. My grandfather was born in [1950]."},
        {"type": "info",
         "prompt": "Now listen: Mike and Julia are planning a party.",
         "translation": "Agora ouça: o Mike e a Júlia estão planejando uma festa de aniversário. Depois responda às "
                        "perguntas abaixo.",
         "audio": f"{AUDIO}/aula11-party.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "The party is for [Grandma].",
         "text": "1. When is Grandma's birthday? → [*On June 12th.|On June 20th.|On July 12th.]\n"
                 "2. When was Grandma born? → [*In 1951.|In 1915.|In 1961.]\n"
                 "3. When is the party? → [*On Saturday, June 13th.|On Friday, June 12th.|On Saturday, July 4th.]\n"
                 "4. When is Mike's birthday? → [*On the 4th of July.|On June 4th.|On the 14th of July.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Mike and Julia are planning a party. → True",
         "statements": [
             {"text": "Grandma's birthday is on a Saturday this year.", "answer": False,
              "translation": "O aniversário da vovó cai num sábado este ano."},
             {"text": "Grandma is 75 this year.", "answer": True,
              "translation": "A vovó faz 75 anos este ano."},
             {"text": "Mike's birthday is on the same day as the Fourth of July.", "answer": True,
              "translation": "O aniversário do Mike é no mesmo dia do 4 de julho."},
         ]},
    ],
}

AULA11_SPEAKING = {
    "title": "Speaking — ordinal numbers and dates",
    "lesson": 11,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: no TH, coloque a língua entre os dentes e solte o ar (\"fourth\", \"fifth\"), sem exagerar.",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the ordinal numbers.",
         "translation": "Ouça e repita os números ordinais da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula11-say-o{i}.m4a"} for i, t in enumerate(
             ["first, second, third", "fourth, fifth, sixth", "seventh, eighth, ninth, tenth",
              "eleventh, twelfth, thirteenth", "twentieth, twenty-first, twenty-second", "thirtieth, thirty-first"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the dates and years.",
         "translation": "Ouça e repita as datas e os anos.",
         "example": "\"July twenty-fourth\" · \"the twenty-fourth of July\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula11-say-d{i}.m4a"} for i, t in enumerate(
             ["It's October 25th.", "It's the 15th of April.", "Christmas is on December 25th.",
              "the Fourth of July", "I was born in 1997.", "It's February 9th, 2026."], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOU.",
         "translation": "Agora responda às perguntas sobre VOCÊ, com as datas em inglês.",
         "example": "\"When is your birthday?\" → \"My birthday is on May 28th.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula11-say-y{i}.m4a"} for i, t in enumerate(
             ["When is your birthday?", "When were you born?", "What's the date today?",
              "When is your mother's birthday?"], 1)]},
    ],
}

AULA11_READING = {
    "title": "Reading — important dates in my life",
    "lesson": 11,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto da Emma, uma inglesa que fala das datas importantes da vida dela. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula11-reading.m4a",
         "text": "IMPORTANT DATES IN MY LIFE\n\n"
                 "My name is Emma. I'm British, so I say the day first: I was born on the 3rd of April, 1995, in London.\n"
                 "I started school on the 5th of September, 2000. My first teacher was Mrs. Brown. I loved her!\n"
                 "On the 12th of June, 2015, I travelled to Brazil. I met my husband, Pedro, in São Paulo. "
                 "We got married on the 21st of December, 2018.\n"
                 "Our daughter, Sofia, was born on the 2nd of February, 2021.\n"
                 "Pedro's favourite date? The 31st of December! We have a big party every year."},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Where was Emma born? → [In London.]",
         "text": "1. When was Emma born? → [*On the 3rd of April, 1995.|On the 4th of March, 1995.|On the 3rd of April, 2005.]\n"
                 "2. When did she start school? → [*In 2000.|In 1995.|In 2015.]\n"
                 "3. When did she travel to Brazil? → [*On the 12th of June, 2015.|On the 21st of December, 2018.|"
                 "On the 2nd of February, 2021.]\n"
                 "4. When is Sofia's birthday? → [*On the 2nd of February.|On the 21st of December.|On the 3rd of April.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Emma is British. → True",
         "statements": [
             {"text": "Emma met Pedro in London.", "answer": False, "translation": "A Emma conheceu o Pedro em Londres."},
             {"text": "Emma and Pedro got married in 2018.", "answer": True,
              "translation": "A Emma e o Pedro se casaram em 2018."},
             {"text": "They have a party on New Year's Eve.", "answer": True,
              "translation": "Eles fazem uma festa na véspera de Ano-Novo."},
         ]},
        {"type": "fill",
         "prompt": "Emma's dates the American way. Complete.",
         "translation": "As datas da Emma do jeito americano (mês + dia). Complete.",
         "example": "the 3rd of April → April [3rd]",
         "text": "1. the 21st of December → [December] 21st\n2. the 2nd of February → February [2nd]\n"
                 "3. the 12th of June → June [12th]"},
    ],
}

AULA11_WRITING = {
    "title": "Writing — important dates",
    "lesson": 11,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Datas: on + data (on May 28th) · in + ano ou mês (in 1990 · in May).\n"
                   "Estados Unidos: May 28th · resto do mundo: the 28th of May. Anos: 1990 = nineteen ninety.",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the years in words.",
         "translation": "Escreva os anos por extenso.",
         "example": "1997 → nineteen ninety-seven",
         "text": "1. 1980 → [nineteen eighty]\n2. 1600 → [sixteen hundred]\n3. 2000 → [two thousand]\n"
                 "4. 1905 → [nineteen oh five|nineteen o five]"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza (use o jeito americano: mês + dia).",
         "example": "O Natal é em 25 de dezembro. → Christmas is on December 25th.",
         "text": "1. Meu aniversário é em 10 de maio. → [My birthday is on May 10th.]\n"
                 "2. Eu nasci em 1995. → [I was born in 1995.]"},
        {"type": "free",
         "prompt": "Write about important dates in your life: When were you born? When is your birthday? "
                   "When did you start school or work? What's your favorite date of the year?",
         "translation": "Escreva sobre datas importantes da sua vida: quando você nasceu, quando é o seu aniversário, "
                        "quando começou a estudar ou trabalhar, qual é a sua data favorita do ano.",
         "example": "I was born on March 12th, 1995.",
         "model_answer": "I was born on March 12th, 1995, in Recife.\n"
                         "My birthday is on March 12th, so it's in the summer in Brazil.\n"
                         "I started school in 2001 and I started work in 2015.\n"
                         "My favorite date is December 25th, because my family has a big dinner.",
         "keywords": ["I was born", "on", "in"], "min_words": 30, "points": 4},
    ],
}

AULA11_VIDEO = _video(11, AULA11_TOPIC, "Video — Important dates",
                      "a Sarah fala de datas importantes do ano: Ano-Novo, o aniversário dela, o 4 de julho e o Natal.",
                      "aula11-video", [
    _q("When is New Year's Day?", "Quando é o Dia de Ano-Novo?", "On January 1st.", "On January 21st.",
       "On December 1st.", "On January 3rd."),
    _q("When is Sarah's birthday?", "Quando é o aniversário da Sarah?", "On March 22nd.", "On March 2nd.",
       "On May 22nd.", "On March 12th."),
    _q("What year was Sarah born?", "Em que ano a Sarah nasceu?", "1998 (nineteen ninety-eight)",
       "1988 (nineteen eighty-eight)", "1989 (nineteen eighty-nine)", "2008 (two thousand eight)"),
    _q("How do Americans say this holiday?", "Como os americanos falam este feriado?", "the Fourth of July",
       "July four", "the July fourth", "four of July"),
    _q("In Britain, how do people say 25/12?", "Na Grã-Bretanha, como as pessoas falam 25/12?",
       "the twenty-fifth of December", "December twenty-five", "the December twenty-fifth", "twenty-five December"),
])

# ---------- Aula 12 — Food & Drink (https://youtu.be/DssKobdytrw) ----------

AULA12_TOPIC = "Aula 12 — Food & Drink"

AULA12_MEALS = {
    "title": "Meals and food vocabulary",
    "lesson": 12,
    "description": "MEALS (refeições): breakfast (café da manhã) · lunch (almoço) · dinner (jantar) · a snack (lanche)\n"
                   "Usamos o verbo HAVE: have breakfast · have lunch · have dinner — SEM \"a\".\n"
                   "Mas: have A snack (com \"a\").  ✗ I have a breakfast  ✓ I have breakfast\n"
                   "Pronúncia: snack /snæk/ (lanche) ≠ snake /sneɪk/ (cobra)!\n"
                   "Pergunta da aula: What do you usually have for breakfast / lunch / dinner / a snack?\n"
                   "→ I usually have bread, eggs and bacon.",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the food to Portuguese.",
         "translation": "Ligue as comidas da aula ao português.",
         "example": "rice and beans → arroz e feijão",
         "pairs": [
             {"left": "roast chicken", "right": "frango assado"},
             {"left": "mashed potato", "right": "purê de batata"},
             {"left": "fried egg", "right": "ovo frito"},
             {"left": "meatballs", "right": "almôndegas"},
             {"left": "shrimp risotto", "right": "risoto de camarão"},
             {"left": "nuts", "right": "castanhas"},
             {"left": "jam", "right": "geleia"},
             {"left": "soda", "right": "refrigerante"},
         ]},
        {"type": "group",
         "prompt": "Put the food in the right group, like in the lesson.",
         "translation": "Coloque cada comida no grupo certo, como na aula.",
         "example": "coffee → breakfast · steak → lunch",
         "categories": ["breakfast", "lunch", "dinner", "snack"],
         "words": [
             {"text": "bread", "category": "breakfast"}, {"text": "eggs and bacon", "category": "breakfast"},
             {"text": "yogurt", "category": "breakfast"},
             {"text": "rice and beans", "category": "lunch"}, {"text": "steak", "category": "lunch"},
             {"text": "french fries", "category": "lunch"},
             {"text": "pasta", "category": "dinner"}, {"text": "soup", "category": "dinner"},
             {"text": "hamburger", "category": "dinner"},
             {"text": "cookies", "category": "snack"}, {"text": "ice cream", "category": "snack"},
             {"text": "smoothie", "category": "snack"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta (lembre: have breakfast, mas have A snack).",
         "example": "I [have lunch] at noon.",
         "text": "1. I [*have breakfast|have a breakfast] every day.\n"
                 "2. I usually [*have a snack|have snack] in the afternoon.\n"
                 "3. We [*have dinner|have a dinner] at 8 p.m.\n"
                 "4. She doesn't [*have lunch|have a lunch] at home."},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "Breakfast is the first meal of the day. → True",
         "statements": [
             {"text": "\"Snack\" and \"snake\" have the same pronunciation.", "answer": False,
              "translation": "\"Snack\" e \"snake\" têm a mesma pronúncia."},
             {"text": "\"Soda\" means any soft drink.", "answer": True,
              "translation": "\"Soda\" significa qualquer refrigerante."},
             {"text": "We pronounce the D in \"sandwich\".", "answer": False,
              "translation": "Pronunciamos o D em \"sandwich\"."},
             {"text": "\"Pasta\" means massa (macarrão).", "answer": True,
              "translation": "\"Pasta\" significa massa (macarrão)."},
         ]},
    ],
}

AULA12_LIKES = {
    "title": "Likes and dislikes: I love, I like, I don't like, I hate",
    "lesson": 12,
    "description": "LIKES AND DISLIKES (do que você gosta e não gosta):\n"
                   "😍 I love… (eu amo) · 🙂 I like… (eu gosto de) · 😕 I don't like… (eu não gosto de) · "
                   "😖 I hate… (eu odeio)\n"
                   "Em inglês não tem \"de\": I like pizza. (✗ I like of pizza)\n"
                   "Pergunta: Do you like hot dog? → Yes, I love hot dog! / No, I don't like hot dog.\n"
                   "Ele / ela: She likes salad. · He doesn't like fish. · Does she like soup?",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Look at the faces and choose.",
         "translation": "Olhe as carinhas e escolha a expressão certa.",
         "example": "😍 I [love] pizza.",
         "text": "1. 😍 I [*love|hate|don't like] watermelon.\n2. 🙂 I [*like|hate|don't like] beans.\n"
                 "3. 😕 I [*don't like|love|like] soup.\n4. 😖 I [*hate|like|love] mashed potato.\n"
                 "5. 🙂 She [*likes|like|liking] cookies.\n6. 😕 He [*doesn't like|don't like|not like] fish."},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (O que você geralmente come no almoço?)",
         "example": "for / have / breakfast / you / do / What / usually → What do you usually have for breakfast?",
         "tokens": ["What", "do", "you", "usually", "have", "for", "lunch?"], "alternatives": []},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas.",
         "example": "What's your favorite meal? → My favorite meal is breakfast.",
         "pairs": [
             {"left": "What do you usually have for breakfast?", "right": "I usually have bread, eggs and bacon."},
             {"left": "What do you usually have for a snack?", "right": "I usually have a sandwich."},
             {"left": "Do you like hot dog?", "right": "Yes, I love hot dog!"},
             {"left": "Does your brother like fish?", "right": "No, he doesn't. He hates fish."},
             {"left": "What's your favorite meal?", "right": "Dinner! I love pasta."},
         ]},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu amo sorvete. → I love ice cream.",
         "text": "1. Eu gosto de salada. → [I like salad.]\n"
                 "2. Eu não gosto de refrigerante. → [I don't like soda.|I do not like soda.]\n"
                 "3. Ela odeia peixe. → [She hates fish.]"},
    ],
}

AULA12_LISTENING = {
    "title": "Listening — what do you usually have?",
    "lesson": 12,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: preste atenção em LOVE / LIKE / DON'T LIKE / HATE. O \"don't\" é rápido: \"I don' like\".",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the word you hear.",
         "translation": "Ouça e escolha a palavra que você ouve.",
         "example": "Você ouve: \"snack\" → snack",
         "audio": f"{AUDIO}/aula12-words.m4a",
         "text": "1. [*snack|snake]\n2. [*steak|cake]\n3. [*meatballs|nuts]\n4. [*jam|ham]\n5. [*soup|soda]\n"
                 "6. [*chips|cheese]"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"I love pizza.\" → I [love] pizza.",
         "audio": f"{AUDIO}/aula12-dictation.m4a",
         "text": "1. I usually have [bread] and coffee for breakfast.\n2. I [hate] mashed potato.\n"
                 "3. She has a [snack] in the afternoon.\n4. We [don't] like soda."},
        {"type": "info",
         "prompt": "Now listen: Tom and Lucy talk about food.",
         "translation": "Agora ouça: o Tom e a Lucy conversam sobre o que eles comem e do que gostam. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula12-friends.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Tom and Lucy are [friends].",
         "text": "1. What's Lucy's favorite meal? → [*Breakfast.|Lunch.|Dinner.]\n"
                 "2. What does Tom usually have for lunch? → [*Rice, beans and steak.|Pasta and soup.|A sandwich.]\n"
                 "3. What does Lucy have for a snack? → [*A smoothie.|Cookies.|Ice cream.]\n"
                 "4. What does Tom hate? → [*Fish.|Salad.|Meatballs.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Lucy loves breakfast. → True",
         "statements": [
             {"text": "Lucy has eggs and bacon for breakfast.", "answer": False,
              "translation": "A Lucy come ovos e bacon no café da manhã."},
             {"text": "Tom doesn't have a snack in the afternoon.", "answer": True,
              "translation": "O Tom não faz lanche à tarde."},
             {"text": "They decide to have pizza for dinner.", "answer": True,
              "translation": "Eles decidem comer pizza no jantar."},
         ]},
    ],
}

AULA12_SPEAKING = {
    "title": "Speaking — food and drink",
    "lesson": 12,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: \"sandwich\" sem o D (\"sanuích\") · snack ≠ snake.",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the food vocabulary.",
         "translation": "Ouça e repita o vocabulário da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula12-say-w{i}.m4a"} for i, t in enumerate(
             ["breakfast, lunch, dinner", "a snack, a snake", "eggs and bacon", "rice and beans", "roast chicken",
              "mashed potato", "shrimp risotto", "sandwich", "yogurt", "smoothie"], 1)]},
        {"type": "speak",
         "prompt": "Answer the questions about YOU.",
         "translation": "Responda às perguntas sobre VOCÊ.",
         "example": "\"What do you usually have for breakfast?\" → \"I usually have coffee and bread.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula12-say-y{i}.m4a"} for i, t in enumerate(
             ["What's your favorite meal?", "What do you usually have for breakfast?",
              "What do you usually have for lunch?", "What do you usually have for a snack?",
              "Do you like hot dog?", "Do you like watermelon?"], 1)]},
    ],
}

AULA12_READING = {
    "title": "Reading — a day of food",
    "lesson": 12,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto da Camila sobre o que ela come em um dia normal. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula12-reading.m4a",
         "text": "A DAY OF FOOD\n\n"
                 "Hi! I'm Camila, and I love food! My favorite meal is lunch.\n"
                 "For breakfast, I usually have coffee with milk, bread and cheese. I don't like eggs.\n"
                 "For lunch, I have rice and beans, salad and roast chicken. On Sundays, my mother makes meatballs "
                 "with mashed potato. Delicious!\n"
                 "In the afternoon, I have a snack at work: fruit, nuts or yogurt. I hate chips!\n"
                 "For dinner, I usually have soup. My husband doesn't like soup, so he has a sandwich.\n"
                 "And on Fridays? Pizza and soda, of course!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "What's Camila's favorite meal? → [Lunch.]",
         "text": "1. What does Camila have for breakfast? → [*Coffee with milk, bread and cheese.|Eggs and bacon.|"
                 "Yogurt and fruit.]\n"
                 "2. What does her mother make on Sundays? → [*Meatballs with mashed potato.|Shrimp risotto.|"
                 "Roast chicken.]\n"
                 "3. What does her husband have for dinner? → [*A sandwich.|Soup.|Pizza.]\n"
                 "4. When do they have pizza? → [*On Fridays.|On Sundays.|Every day.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Camila loves food. → True",
         "statements": [
             {"text": "Camila likes eggs.", "answer": False, "translation": "A Camila gosta de ovos."},
             {"text": "She has a snack at work.", "answer": True, "translation": "Ela faz um lanche no trabalho."},
             {"text": "Camila loves chips.", "answer": False, "translation": "A Camila ama salgadinho."},
         ]},
        {"type": "fill",
         "prompt": "Complete according to the text.",
         "translation": "Complete de acordo com o texto.",
         "example": "Camila's favorite meal is [lunch].",
         "text": "1. She [doesn't] like eggs.\n2. For dinner, she usually has [soup].\n"
                 "3. Her husband [doesn't] like soup."},
    ],
}

AULA12_WRITING = {
    "title": "Writing — my meals",
    "lesson": 12,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ I usually have … for breakfast / lunch / dinner / a snack.\n"
                   "I love… · I like… · I don't like… · I hate… (sem \"a\" antes de breakfast, lunch e dinner).",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Is this sentence correct?",
         "translation": "Esta frase está correta? (exercício do final da aula)",
         "example": "I have lunch at noon. → [Correct]",
         "text": "1. I have a breakfast every day. → [*Incorrect|Correct]\n"
                 "2. I usually have a snack in the afternoon. → [*Correct|Incorrect]\n"
                 "3. She likes of pizza. → [*Incorrect|Correct]\n"
                 "4. We have dinner at 7 p.m. → [*Correct|Incorrect]"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu geralmente como pão no café da manhã. → I usually have bread for breakfast.",
         "text": "1. Minha refeição favorita é o jantar. → [My favorite meal is dinner.]\n"
                 "2. Eu geralmente como arroz e feijão no almoço. → [I usually have rice and beans for lunch.]"},
        {"type": "free",
         "prompt": "Write about your meals: What do you usually have for breakfast, lunch and dinner? "
                   "What do you have for a snack? What do you love, like, not like and hate?",
         "translation": "Escreva sobre as suas refeições: o que você costuma comer no café, almoço e jantar, "
                        "o que come no lanche e do que você ama, gosta, não gosta e odeia.",
         "example": "For breakfast, I usually have coffee and bread.",
         "model_answer": "My favorite meal is breakfast.\n"
                         "For breakfast, I usually have coffee, bread and cheese.\n"
                         "For lunch, I have rice, beans, steak and salad.\n"
                         "In the afternoon, I have a snack: fruit or a smoothie.\n"
                         "For dinner, I usually have soup or pasta.\n"
                         "I love ice cream, but I don't like soda. I hate fish!",
         "keywords": ["breakfast", "lunch", "dinner", "like"], "min_words": 30, "points": 4},
    ],
}

AULA12_VIDEO = _video(12, AULA12_TOPIC, "Video — My favorite meals",
                      "o Paul mostra o que ele come no café da manhã, no almoço, no lanche e no jantar — e do que gosta "
                      "e não gosta.",
                      "aula12-video", [
    _q("What does Paul usually have for breakfast?", "O que o Paul geralmente come no café da manhã?",
       "Coffee, bread and cheese.", "Eggs and bacon.", "Yogurt and fruit.", "Rice and beans."),
    _q("What doesn't Paul like?", "Do que o Paul não gosta?", "Fish.", "Chicken.", "Rice.", "French fries."),
    _q("What does Paul have for a snack?", "O que o Paul come no lanche?", "A smoothie.", "A cake.", "Chips.",
       "Cookies."),
    _q("What's Paul's favorite meal?", "Qual é a refeição favorita do Paul?", "Dinner.", "Breakfast.", "Lunch.",
       "A snack."),
])

# ---------- Aula 13 — Countable & Uncountable Nouns (https://youtu.be/pBZnLjBJ0QA) ----------

AULA13_TOPIC = "Aula 13 — Countable & Uncountable Nouns"

AULA13_VOCAB = {
    "title": "Fruit and vegetables",
    "lesson": 13,
    "description": "FRUIT: orange · apple · pineapple (abacaxi) · watermelon (melancia) · grape (uva) · banana · papaya (mamão) · "
                   "coconut (coco) · strawberry (morango) · melon (melão)\n"
                   "VEGETABLES: potato · carrot (cenoura) · tomato · onion (cebola) · peas (ervilhas) · corn (milho) · "
                   "broccoli · lettuce (alface) · cabbage (repolho) · cucumber (pepino)\n"
                   "What's your favorite fruit? → My favorite fruit is watermelon.",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the words to Portuguese.",
         "translation": "Ligue as palavras ao português.",
         "example": "strawberry → morango",
         "pairs": [
             {"left": "pineapple", "right": "abacaxi"},
             {"left": "watermelon", "right": "melancia"},
             {"left": "grape", "right": "uva"},
             {"left": "papaya", "right": "mamão"},
             {"left": "onion", "right": "cebola"},
             {"left": "lettuce", "right": "alface"},
             {"left": "cabbage", "right": "repolho"},
             {"left": "cucumber", "right": "pepino"},
         ]},
        {"type": "group",
         "prompt": "Fruit or vegetable? Put each word in the right group.",
         "translation": "Fruta ou legume/verdura? Coloque cada palavra no grupo certo.",
         "example": "apple → fruit · carrot → vegetable",
         "categories": ["fruit", "vegetable"],
         "words": [
             {"text": "orange", "category": "fruit"}, {"text": "coconut", "category": "fruit"},
             {"text": "strawberry", "category": "fruit"}, {"text": "melon", "category": "fruit"},
             {"text": "banana", "category": "fruit"},
             {"text": "potato", "category": "vegetable"}, {"text": "peas", "category": "vegetable"},
             {"text": "corn", "category": "vegetable"}, {"text": "broccoli", "category": "vegetable"},
             {"text": "onion", "category": "vegetable"},
         ]},
        {"type": "fill",
         "prompt": "Write the English word.",
         "translation": "Escreva a palavra em inglês.",
         "example": "maçã → apple",
         "text": "1. laranja → [orange]\n2. cenoura → [carrot]\n3. morango → [strawberry]\n4. milho → [corn]\n"
                 "5. batata → [potato]"},
    ],
}

AULA13_COUNT = {
    "title": "Countable or uncountable?",
    "lesson": 13,
    "description": "COUNTABLE (contáveis): dá para contar e TEM PLURAL → a banana, two bananas · an apple, three apples · "
                   "a burger, two hot dogs, three candies\n"
                   "  Use a / an / one (singular) e números ou SOME (plural): some bananas.\n"
                   "  Verbo no singular ou plural: The banana is fresh. · The bananas are fresh.\n"
                   "UNCOUNTABLE (incontáveis): NÃO tem plural, NÃO usa a / an / número, verbo sempre no SINGULAR.\n"
                   "  ✗ a milk, two breads, rices  ✓ milk · bread · rice  → Bacon is salty.\n"
                   "  Para contar, conte o recipiente ou a parte: a cup of coffee · a loaf of bread · a slice of bread\n"
                   "INCONTÁVEIS COMUNS: líquidos e gases (water, milk, coffee, juice, soup, smoke, rain) · "
                   "grãos e pós (rice, sugar, salt, flour, sand) · algumas comidas (bread, cheese, meat, bacon, butter, "
                   "chocolate) · ideias (love, music, help, luck) · materiais (paper, wood, glass, gold)\n"
                   "PEGADINHAS: money · furniture · information · luggage · work → sempre singular!",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "Countable or uncountable? Put each word in the right group.",
         "translation": "Contável ou incontável? Coloque cada palavra no grupo certo (como no exercício da aula).",
         "example": "banana → countable · coffee → uncountable",
         "categories": ["countable", "uncountable"],
         "words": [
             {"text": "burger", "category": "countable"}, {"text": "hot dog", "category": "countable"},
             {"text": "candy", "category": "countable"}, {"text": "apple", "category": "countable"},
             {"text": "carrot", "category": "countable"}, {"text": "song", "category": "countable"},
             {"text": "bread", "category": "uncountable"}, {"text": "rice", "category": "uncountable"},
             {"text": "meat", "category": "uncountable"}, {"text": "milk", "category": "uncountable"},
             {"text": "money", "category": "uncountable"}, {"text": "music", "category": "uncountable"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta.",
         "example": "I want [a banana]. · I want [some bananas].",
         "text": "1. I have [*two bananas|two banana|a bananas].\n2. She wants [*an apple|a apple|some apple].\n"
                 "3. We need [*bread|a bread|two breads].\n4. There are [*three candies|three candys|three candy].\n"
                 "5. I need [*some information|an information|two informations].\n"
                 "6. The bananas [*are|is] fresh.\n7. Bacon [*is|are] salty.\n8. Rice [*is|are] cheap in Brazil."},
        {"type": "match",
         "prompt": "Match the uncountable nouns to their type.",
         "translation": "Ligue cada palavra incontável ao seu tipo (a tabela da aula).",
         "example": "water → liquid",
         "pairs": [
             {"left": "milk, juice, soup", "right": "liquids"},
             {"left": "sugar, salt, flour", "right": "small parts (powder, grains)"},
             {"left": "cheese, butter, ham", "right": "some food"},
             {"left": "love, luck, peace", "right": "abstract ideas"},
             {"left": "paper, wood, gold", "right": "materials"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Coffee\" is uncountable. → True",
         "statements": [
             {"text": "We can say \"two breads\".", "answer": False, "translation": "Podemos dizer \"two breads\"."},
             {"text": "We use A and AN only with singular countable nouns.", "answer": True,
              "translation": "Usamos A e AN só com substantivos contáveis no singular."},
             {"text": "\"Song\" is countable, but \"music\" is uncountable.", "answer": True,
              "translation": "\"Song\" é contável, mas \"music\" é incontável."},
             {"text": "\"Money\" is countable: one money, two moneys.", "answer": False,
              "translation": "\"Money\" é contável: one money, two moneys."},
         ]},
    ],
}

AULA13_LISTENING = {
    "title": "Listening — at the street market",
    "lesson": 13,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: preste atenção no S do plural (\"apples\", \"carrots\") e no A / AN antes das palavras.",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"an apple\" → an apple",
         "audio": f"{AUDIO}/aula13-words.m4a",
         "text": "1. [*an orange|oranges]\n2. [*two carrots|a carrot]\n3. [*some bananas|a banana]\n4. [*a pineapple|pineapples]\n"
                 "5. [*three tomatoes|three potatoes]\n6. [*a cup of coffee|a cup of tea]"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"The banana is fresh.\" → The banana [is] fresh.",
         "audio": f"{AUDIO}/aula13-dictation.m4a",
         "text": "1. The bananas [are] fresh.\n2. I need some [carrots].\n3. Milk [is] good for you.\n"
                 "4. My favorite fruit is [watermelon]."},
        {"type": "info",
         "prompt": "Now listen: Anna buys fruit and vegetables at the street market.",
         "translation": "Agora ouça: a Anna compra frutas e legumes na feira. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula13-market.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Anna is at the [street market].",
         "text": "1. How many bananas does Anna want? → [*Six.|Two.|Ten.]\n"
                 "2. What fruit does she buy for her son? → [*A watermelon.|A pineapple.|Some grapes.]\n"
                 "3. What vegetables does she buy? → [*Carrots and an onion.|Potatoes and corn.|Lettuce and cabbage.]\n"
                 "4. What does the man sell? → [*Fruit and vegetables.|Bread and milk.|Meat and fish.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Anna wants some bananas. → True",
         "statements": [
             {"text": "The man sells bread.", "answer": False, "translation": "O homem vende pão."},
             {"text": "The strawberries are very fresh today.", "answer": True,
              "translation": "Os morangos estão bem fresquinhos hoje."},
             {"text": "Anna buys some strawberries.", "answer": False, "translation": "A Anna compra morangos."},
         ]},
    ],
}

AULA13_SPEAKING = {
    "title": "Speaking — fruit, vegetables and plurals",
    "lesson": 13,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: \"vegetable\" tem 3 sílabas (\"VÉDJ-ta-bou\") · \"money\" se fala \"mâni\".",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the fruit and vegetables.",
         "translation": "Ouça e repita as frutas e os legumes da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula13-say-w{i}.m4a"} for i, t in enumerate(
             ["orange, apple, pineapple", "watermelon, grape, banana", "papaya, coconut, strawberry, melon",
              "potato, carrot, tomato, onion", "peas, corn, broccoli", "lettuce, cabbage, cucumber"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases (contáveis e incontáveis).",
         "example": "\"The banana is fresh. The bananas are fresh.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula13-say-s{i}.m4a"} for i, t in enumerate(
             ["The banana is fresh.", "The bananas are fresh.", "Bacon is salty.", "I want a cup of coffee.",
              "Two loaves of bread, please.", "My favorite fruit is watermelon."], 1)]},
        {"type": "speak",
         "prompt": "Answer the questions about YOU.",
         "translation": "Responda às perguntas sobre VOCÊ.",
         "example": "\"What's your favorite fruit?\" → \"My favorite fruit is mango.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula13-say-y{i}.m4a"} for i, t in enumerate(
             ["What's your favorite fruit?", "What's your favorite vegetable?", "Do you like broccoli?"], 1)]},
    ],
}

AULA13_READING = {
    "title": "Reading — Saturday at the street market",
    "lesson": 13,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto do Roberto sobre os sábados na feira. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula13-reading.m4a",
         "text": "SATURDAY AT THE STREET MARKET\n\n"
                 "Every Saturday morning, I go to the street market with my daughter, Lia.\n"
                 "First we buy fruit: some bananas, two pineapples and a big watermelon. Lia loves strawberries, "
                 "so we buy some strawberries for her too.\n"
                 "Then we buy vegetables: carrots, tomatoes, onions and a lettuce for the salad. I don't buy broccoli. "
                 "Lia hates broccoli!\n"
                 "After the market, we go to the bakery. Bread is uncountable, so I say: \"Two loaves of bread, please.\"\n"
                 "At home, I have a cup of coffee and Lia has a glass of milk. Saturday is my favorite day!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "When does Roberto go to the street market? → [On Saturday mornings.]",
         "text": "1. Who goes to the market with him? → [*His daughter.|His wife.|His son.]\n"
                 "2. How many pineapples do they buy? → [*Two.|One.|Some.]\n"
                 "3. What does Lia hate? → [*Broccoli.|Strawberries.|Lettuce.]\n"
                 "4. What does Roberto say at the bakery? → [*Two loaves of bread, please.|Two breads, please.|"
                 "A bread, please.]"},
        {"type": "group",
         "prompt": "Find in the text: countable or uncountable?",
         "translation": "Encontre no texto: contável ou incontável?",
         "example": "bananas → countable · bread → uncountable",
         "categories": ["countable", "uncountable"],
         "words": [
             {"text": "pineapple", "category": "countable"}, {"text": "strawberry", "category": "countable"},
             {"text": "onion", "category": "countable"}, {"text": "loaf", "category": "countable"},
             {"text": "fruit", "category": "uncountable"}, {"text": "bread", "category": "uncountable"},
             {"text": "coffee", "category": "uncountable"}, {"text": "milk", "category": "uncountable"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Lia loves strawberries. → True",
         "statements": [
             {"text": "They buy broccoli for the salad.", "answer": False,
              "translation": "Eles compram brócolis para a salada."},
             {"text": "Lia has a glass of milk at home.", "answer": True, "translation": "A Lia toma um copo de leite em casa."},
         ]},
    ],
}

AULA13_WRITING = {
    "title": "Writing — fruit and vegetables I like",
    "lesson": 13,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Contáveis: a / an + singular · número ou some + plural (an apple, some apples).\n"
                   "Incontáveis: sem a / an e sem plural (milk, bread, rice) · para contar: a cup of coffee, a loaf of bread.",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the plural. If the word is uncountable, write it again (no plural).",
         "translation": "Escreva o plural. Se a palavra for incontável, escreva ela de novo (não tem plural).",
         "example": "banana → bananas · rice → rice",
         "text": "1. apple → [apples]\n2. candy → [candies]\n3. tomato → [tomatoes]\n4. bread → [bread]\n"
                 "5. milk → [milk]\n6. strawberry → [strawberries]"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu quero uma xícara de café. → I want a cup of coffee.",
         "text": "1. Eu tenho duas laranjas. → [I have two oranges.]\n"
                 "2. O pão está fresco. → [The bread is fresh.]"},
        {"type": "free",
         "prompt": "Write about the fruit and vegetables you like and don't like. What's your favorite fruit? "
                   "What's your favorite vegetable? What do you usually buy at the supermarket or street market?",
         "translation": "Escreva sobre as frutas e os legumes de que você gosta e não gosta, a sua fruta e o seu legume "
                        "favoritos e o que você costuma comprar no mercado ou na feira.",
         "example": "My favorite fruit is pineapple.",
         "model_answer": "My favorite fruit is pineapple, and my favorite vegetable is corn.\n"
                         "I love strawberries and grapes, but I don't like papaya.\n"
                         "At the street market, I usually buy some bananas, an avocado and some tomatoes.\n"
                         "I don't buy cabbage. I hate cabbage!",
         "keywords": ["favorite fruit", "vegetable", "some"], "min_words": 30, "points": 4},
    ],
}

AULA13_VIDEO = _video(13, AULA13_TOPIC, "Video — At the street market",
                      "a Sarah vai à feira e à padaria e mostra o que é contável e incontável.",
                      "aula13-video", [
    _q("Is \"banana\" countable or uncountable?", "\"Banana\" é contável ou incontável?", "Countable: one banana, two bananas.",
       "Uncountable: no plural.", "Countable, but no plural.", "Uncountable: a banana."),
    _q("Complete: Sarah buys ___ apple for her.", "Complete: a Sarah compra ___ maçã para ela.", "an", "a", "some", "two"),
    _q("Which is correct?", "Qual está correto?", "a loaf of bread", "a bread", "two breads", "some breads"),
    _q("Why are milk and coffee uncountable?", "Por que milk e coffee são incontáveis?", "They're liquids.",
       "They're expensive.", "They're fruit.", "They're vegetables."),
])

# ---------- Aula 14 — Countable & Uncountable Nouns: a, an, some, any (https://youtu.be/bsdjLfTCq34) ----------

AULA14_TOPIC = "Aula 14 — Countable & Uncountable Nouns (a, an, some, any)"

AULA14_QUANT = {
    "title": "A, an, some, any",
    "lesson": 14,
    "description": "A / AN → singular CONTÁVEL, em frases afirmativas, negativas e perguntas.\n"
                   "  A antes de som de consoante (a pineapple) · AN antes de som de vogal (an orange, an egg, an apple)\n"
                   "  I need an orange. · I don't need an orange. · Do you need an orange?\n"
                   "SOME (alguns, algumas, um pouco de) → plural contável OU incontável, só em frases AFIRMATIVAS.\n"
                   "  We need some oranges. · She wants some orange juice.\n"
                   "ANY → plural contável OU incontável, em frases NEGATIVAS e PERGUNTAS.\n"
                   "  We don't need any oranges. · We don't need any rice. · Do we need any oranges? · Do we need any rice?\n"
                   "Pronúncia: dessert /dɪˈzɜːrt/ (sobremesa) ≠ desert /ˈdezərt/ (deserto)!",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "A, an or some? Put each word in the right group.",
         "translation": "A, an ou some? Coloque cada palavra no grupo certo (exercício das figuras da aula).",
         "example": "burger → a · bread → some",
         "categories": ["a", "an", "some"],
         "words": [
             {"text": "burger", "category": "a"}, {"text": "banana", "category": "a"},
             {"text": "sandwich", "category": "a"}, {"text": "pineapple", "category": "a"},
             {"text": "apple", "category": "an"}, {"text": "egg", "category": "an"}, {"text": "orange", "category": "an"},
             {"text": "bread", "category": "some"}, {"text": "rice", "category": "some"},
             {"text": "coffee", "category": "some"}, {"text": "milk", "category": "some"},
             {"text": "hot dogs", "category": "some"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose a, an, some or any.",
         "translation": "Escolha a, an, some ou any.",
         "example": "We need [some] oranges.",
         "text": "1. I need [*an|a|some] orange.\n2. She wants [*some|any|a] orange juice.\n"
                 "3. We don't need [*any|some|a] rice.\n4. Do we need [*any|some|an] oranges?\n"
                 "5. She doesn't want [*a|any|some] pineapple.\n6. They want [*some|any|an] candies."},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "We use AN before a vowel sound. → True",
         "statements": [
             {"text": "We use SOME in negative sentences.", "answer": False,
              "translation": "Usamos SOME em frases negativas."},
             {"text": "We use ANY in questions and negative sentences.", "answer": True,
              "translation": "Usamos ANY em perguntas e frases negativas."},
             {"text": "We can use A and AN with uncountable nouns.", "answer": False,
              "translation": "Podemos usar A e AN com substantivos incontáveis."},
             {"text": "\"Dessert\" means sobremesa, and \"desert\" means deserto.", "answer": True,
              "translation": "\"Dessert\" significa sobremesa e \"desert\" significa deserto."},
         ]},
    ],
}

AULA14_THERE = {
    "title": "There is / there are + a, an, some, any",
    "lesson": 14,
    "description": "THERE IS (singular ou incontável) · THERE ARE (plural)\n"
                   "AFFIRMATIVE: There is an apple. · There is some coffee. · There are some oranges.\n"
                   "NEGATIVE: There isn't an apple. · There isn't any milk. · There aren't any apples.\n"
                   "QUESTION: Is there an apple? · Is there any milk? · Are there any apples in the fridge?\n"
                   "Exemplos da aula: There is some butter. · There is a green apple. · There are two slices of bread. · "
                   "There are three sausages.",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta.",
         "example": "There [is] some coffee.",
         "text": "1. There [*is|are] some butter.\n2. There [*are|is] some oranges.\n"
                 "3. There [*aren't any|isn't some|aren't some] apples.\n4. [*Is there any|Are there any|Is there some] milk?\n"
                 "5. [*Are there any|Is there any|Are there some] eggs in the fridge?\n6. There [*isn't an|aren't an|isn't some] egg."},
        {"type": "fill",
         "prompt": "Complete with a, an or some.",
         "translation": "Complete com a, an ou some (exercício do final da aula).",
         "example": "I need [some] money.",
         "text": "1. I need some money to buy [a] sandwich.\n2. She had [an] apple and [some] bread for breakfast.\n"
                 "3. I always have [an] egg in the morning.\n4. There are [some] tomatoes in the fridge.\n"
                 "5. There is [some] rice, too."},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Tem maçãs na geladeira?)",
         "example": "there / milk / any / Is → Is there any milk?",
         "tokens": ["Are", "there", "any", "apples", "in", "the", "fridge?"], "alternatives": []},
        {"type": "choice",
         "prompt": "Which sentence is correct?",
         "translation": "Qual frase está correta?",
         "example": "There is some coffee. ✓",
         "options": ["There isn't any milk in the fridge.", "There isn't some milk in the fridge.",
                     "There aren't any milk in the fridge.", "There isn't a milk in the fridge."],
         "correct": 0},
    ],
}

AULA14_LISTENING = {
    "title": "Listening — let's make a cake!",
    "lesson": 14,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: SOME e ANY são fracas na frase (\"səm\", \"éni\"). Preste atenção também em IS / ARE.",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"There is an apple.\" → an apple",
         "audio": f"{AUDIO}/aula14-words.m4a",
         "text": "1. There is [*an|some] egg.\n2. There [*are some|aren't any] oranges.\n3. We don't need [*any|some] rice.\n"
                 "4. [*Is there|Are there] any milk?\n5. My favorite [*dessert|desert] is ice cream."},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"I need an orange.\" → I need [an] orange.",
         "audio": f"{AUDIO}/aula14-dictation.m4a",
         "text": "1. There is [some] coffee.\n2. There aren't [any] tomatoes.\n3. Do you need [an] egg?\n"
                 "4. She wants [some] orange juice."},
        {"type": "info",
         "prompt": "Now listen: Bia and her dad want to make a chocolate cake.",
         "translation": "Agora ouça: a Bia e o pai dela querem fazer um bolo de chocolate e olham o que tem na cozinha. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula14-cake.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "They want to make a [chocolate cake].",
         "text": "1. How many eggs are there? → [*Three.|Two.|There aren't any eggs.]\n"
                 "2. Is there any milk? → [*Yes, there is some milk.|No, there isn't any milk.|There is a milk.]\n"
                 "3. What do they need from the supermarket? → [*Some chocolate.|Some eggs.|Some flour.]\n"
                 "4. Is there any sugar? → [*Yes, there's some sugar.|No, there isn't any sugar.|There are some sugars.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Bia wants a chocolate cake. → True",
         "statements": [
             {"text": "There isn't any flour.", "answer": False, "translation": "Não tem farinha."},
             {"text": "There isn't any chocolate.", "answer": True, "translation": "Não tem chocolate."},
             {"text": "Bia's dad goes to the supermarket.", "answer": True, "translation": "O pai da Bia vai ao supermercado."},
         ]},
    ],
}

AULA14_SPEAKING = {
    "title": "Speaking — there is, there are",
    "lesson": 14,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: \"there is an apple\" se liga: \"therizanapple\" · \"some\" é curtinho: \"səm\".",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula14-say-s{i}.m4a"} for i, t in enumerate(
             ["I need an orange.", "We need some oranges.", "We don't need any rice.", "Do we need any oranges?",
              "There is some butter.", "There are two slices of bread.", "There aren't any apples.",
              "Are there any apples in the fridge?", "dessert, desert"], 1)]},
        {"type": "speak",
         "prompt": "Now answer about YOUR kitchen.",
         "translation": "Agora responda sobre a SUA cozinha, com some ou any.",
         "example": "\"Is there any milk in your fridge?\" → \"Yes, there is some milk.\" / \"No, there isn't any milk.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula14-say-y{i}.m4a"} for i, t in enumerate(
             ["What's your favorite dessert?", "Is there any milk in your fridge?", "Are there any eggs in your kitchen?",
              "Are there any apples in your kitchen?", "Is there any chocolate in your house?"], 1)]},
    ],
}

AULA14_READING = {
    "title": "Reading — the empty fridge",
    "lesson": 14,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto do Lucas, um estudante que mora sozinho. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula14-reading.m4a",
         "text": "THE EMPTY FRIDGE\n\n"
                 "I'm Lucas. I'm a student, and I live alone. It's Sunday night and I'm very hungry!\n"
                 "I open the fridge. Hmm… There isn't any meat, and there aren't any vegetables. "
                 "There is some butter and there is an egg. Only one egg!\n"
                 "I look in the kitchen cupboard. There is some rice, but there isn't any bread. "
                 "There are some cookies, but they're my roommate's cookies.\n"
                 "So, what's for dinner? Rice with a fried egg! And for dessert? An apple.\n"
                 "Tomorrow I need to go to the supermarket. I need some bread, some milk, some fruit and some eggs."},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "What day is it? → [Sunday.]",
         "text": "1. How many eggs are there? → [*One.|Two.|There aren't any eggs.]\n"
                 "2. Is there any bread? → [*No, there isn't.|Yes, there is.|Yes, there are some.]\n"
                 "3. Whose cookies are they? → [*His roommate's.|Lucas's.|His mother's.]\n"
                 "4. What does Lucas have for dinner? → [*Rice with a fried egg.|Meat and vegetables.|Bread and butter.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Lucas is hungry. → True",
         "statements": [
             {"text": "There are some vegetables in the fridge.", "answer": False,
              "translation": "Tem legumes na geladeira."},
             {"text": "There is some butter in the fridge.", "answer": True, "translation": "Tem manteiga na geladeira."},
             {"text": "Lucas has an apple for dessert.", "answer": True, "translation": "O Lucas come uma maçã de sobremesa."},
         ]},
        {"type": "fill",
         "prompt": "Complete according to the text with a, an, some or any.",
         "translation": "Complete de acordo com o texto com a, an, some ou any.",
         "example": "There is [an] egg.",
         "text": "1. There isn't [any] meat.\n2. There is [some] rice.\n3. For dessert, he has [an] apple.\n"
                 "4. He needs [some] milk."},
    ],
}

AULA14_WRITING = {
    "title": "Writing — what's in your kitchen?",
    "lesson": 14,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ There is a / an / some (singular ou incontável) · There are some (plural)\n"
                   "Negativa e pergunta com ANY: There isn't any milk. · There aren't any apples. · Is there any juice?",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Complete with a, an, some or any.",
         "translation": "Complete com a, an, some ou any.",
         "example": "Do we need [any] bread?",
         "text": "1. There are [some] grapes on the table.\n2. Is there [any] cheese?\n3. I want [an] orange.\n"
                 "4. We don't have [any] potatoes.\n5. She has [a] banana every day."},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Tem um pouco de café. → There is some coffee.",
         "text": "1. Tem algumas laranjas na geladeira. → [There are some oranges in the fridge.]\n"
                 "2. Não tem leite. → [There isn't any milk.|There is not any milk.|There's no milk.]"},
        {"type": "free",
         "prompt": "Look in your kitchen and fridge (or imagine). Write what there is and what there isn't. "
                   "What do you need from the supermarket?",
         "translation": "Olhe a sua cozinha e a geladeira (ou imagine). Escreva o que tem e o que não tem. "
                        "O que você precisa comprar no supermercado?",
         "example": "There is some milk in my fridge.",
         "model_answer": "There is some milk and some cheese in my fridge.\n"
                         "There are some eggs and there is an orange.\n"
                         "There isn't any butter, and there aren't any tomatoes.\n"
                         "I need some bread, some apples and a pineapple from the supermarket.",
         "keywords": ["There is", "There are", "some", "any"], "min_words": 30, "points": 4},
    ],
}

AULA14_VIDEO = _video(14, AULA14_TOPIC, "Video — What's in the fridge?",
                      "a Sarah quer fazer uma omelete e olha o que tem (e o que não tem) na geladeira.",
                      "aula14-video", [
    _q("Are there any tomatoes?", "Tem tomates?", "No, there aren't any tomatoes.", "Yes, there are some tomatoes.",
       "Yes, there is a tomato.", "No, there isn't some tomatoes."),
    _q("Complete: There are ___ eggs.", "Complete: Tem ___ ovos.", "some", "any", "an", "a"),
    _q("Complete: I can make ___ orange juice.", "Complete: Eu posso fazer ___ suco de laranja.", "some", "an", "a", "any"),
    _q("What does Sarah have for breakfast?", "O que a Sarah come no café da manhã?",
       "A fried egg and some juice.", "An omelet and some milk.", "Some tomatoes and bread.", "Some apples and coffee."),
])

# ---------- Aula 15 — Countable & Uncountable Nouns: Containers (https://youtu.be/TyfgtkibUfc) ----------

AULA15_TOPIC = "Aula 15 — Countable & Uncountable Nouns (Containers)"

AULA15_CONTAINERS = {
    "title": "Containers: a bottle of, a can of, a loaf of…",
    "lesson": 15,
    "description": "Para CONTAR um incontável, contamos o RECIPIENTE (container) ou a parte. O recipiente vai para o plural; "
                   "a comida, não!\n"
                   "a bottle of water (garrafa) · a box of chocolate / cereal (caixa, para sólidos) · "
                   "a can of soda (lata de BEBIDA) · a carton of milk / juice (caixa de LÍQUIDO) · a jar of honey (pote) · "
                   "a packet of pasta / rice / crisps (pacote — ou a bag of) · a tin of tuna (lata de COMIDA)\n"
                   "Sem recipiente: a loaf of bread (um pão inteiro) → two LOAVES of bread · a slice of cheese (fatia) · "
                   "a cup of tea / coffee (xícara) · a scoop of ice cream (bola) · a bar of chocolate (barra) · "
                   "a glass of water (copo)\n"
                   "✗ two breads · two waters  ✓ two loaves of bread · two glasses of water",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the containers to Portuguese.",
         "translation": "Ligue os recipientes ao português.",
         "example": "a bottle → uma garrafa",
         "pairs": [
             {"left": "a jar", "right": "um pote"},
             {"left": "a packet", "right": "um pacote"},
             {"left": "a can (of soda)", "right": "uma lata (de bebida)"},
             {"left": "a tin (of tuna)", "right": "uma lata (de comida)"},
             {"left": "a carton (of milk)", "right": "uma caixa (de líquido)"},
             {"left": "a slice", "right": "uma fatia"},
             {"left": "a scoop", "right": "uma bola (de sorvete)"},
             {"left": "a loaf", "right": "um pão inteiro"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the right container.",
         "translation": "Escolha o recipiente certo (exercício da aula).",
         "example": "a [packet] of rice",
         "text": "1. a [*jar|can|slice] of honey\n2. a [*tin|carton|scoop] of tuna\n3. a [*carton|tin|loaf] of juice\n"
                 "4. a [*packet|glass|scoop] of crisps\n5. a [*can|jar|loaf] of soda\n6. a [*box|carton|cup] of cereal\n"
                 "7. a [*bar|glass|slice] of chocolate\n8. a [*cup|loaf|tin] of coffee"},
        {"type": "fill",
         "prompt": "Complete with the plural.",
         "translation": "Complete com o plural (o recipiente vai para o plural, a comida não).",
         "example": "a cup of tea → two [cups] of tea",
         "text": "1. a loaf of bread → two [loaves] of bread\n2. a slice of cheese → three [slices] of cheese\n"
                 "3. a scoop of ice cream → two [scoops] of ice cream\n4. a glass of water → two [glasses] of water\n"
                 "5. a box of chocolate → two [boxes] of chocolate\n6. a tin of tuna → three [tins] of tuna"},
        {"type": "choice",
         "prompt": "You are at the bakery. What do you say?",
         "translation": "Você está na padaria e quer dois pães. O que você fala?",
         "example": "Três fatias de queijo → three slices of cheese",
         "options": ["Two loaves of bread, please.", "Two breads, please.", "Two loafs of breads, please.",
                     "Two bread, please."],
         "correct": 0},
    ],
}

AULA15_QUANT = {
    "title": "A lot of, many, much, a few, a little",
    "lesson": 15,
    "description": "GRANDES QUANTIDADES:\n"
                   "A LOT OF → plural e incontável, em afirmativas, negativas e perguntas: There are a lot of tomatoes. · "
                   "There's a lot of milk. (pronúncia ligada: \"a lódov\")\n"
                   "MANY → só PLURAL contável: There are many apples. · There aren't many apples. · Are there many apples?\n"
                   "MUCH → só INCONTÁVEL, em negativas e perguntas: I don't eat much chocolate. · Do you eat much chocolate?\n"
                   "PEQUENAS QUANTIDADES:\n"
                   "A FEW → plural contável: I have a few oranges left. · A LITTLE → incontável: I have a little money left.\n"
                   "PERGUNTAS: HOW MANY + plural → How many cups of coffee do you drink in a day?\n"
                   "HOW MUCH + incontável → How much water do you drink in a day?",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "Countable or uncountable? Put the quantifiers in the right group.",
         "translation": "Coloque cada palavra no grupo certo: usamos com plural contável, com incontável ou com os dois?",
         "example": "many → countable (plural) · much → uncountable",
         "categories": ["countable (plural)", "uncountable", "both"],
         "words": [
             {"text": "many", "category": "countable (plural)"}, {"text": "a few", "category": "countable (plural)"},
             {"text": "How many", "category": "countable (plural)"},
             {"text": "much", "category": "uncountable"}, {"text": "a little", "category": "uncountable"},
             {"text": "How much", "category": "uncountable"},
             {"text": "a lot of", "category": "both"}, {"text": "some", "category": "both"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta (exercício do final da aula).",
         "example": "She has [many] friends at school.",
         "text": "1. I don't have [*much|many|a few] time today.\n2. She has [*a lot of|much|a little] friends at school.\n"
                 "3. There is [*a little|a few|many] milk in the fridge.\n4. We don't eat [*much|many|a few] fast food.\n"
                 "5. She has [*a little|a lot of|many] money, but it's enough for lunch.\n"
                 "6. There are [*a few|a little|much] apples on the table."},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas.",
         "example": "How many apples are there? → There are a few apples.",
         "pairs": [
             {"left": "How many cups of coffee do you drink in a day?", "right": "I drink three cups of coffee."},
             {"left": "How much water do you drink in a day?", "right": "I drink a lot of water. Two liters!"},
             {"left": "How many brothers do you have?", "right": "I don't have many. Only one."},
             {"left": "How much money do you have?", "right": "A little. Only ten reais."},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "We use MANY with plural countable nouns. → True",
         "statements": [
             {"text": "We can use A LOT OF with countable and uncountable nouns.", "answer": True,
              "translation": "Podemos usar A LOT OF com contáveis e incontáveis."},
             {"text": "\"I eat much chocolate\" is natural in English.", "answer": False,
              "translation": "\"I eat much chocolate\" é natural em inglês."},
             {"text": "We say \"How much water…?\" and \"How many apples…?\".", "answer": True,
              "translation": "Dizemos \"How much water…?\" e \"How many apples…?\"."},
             {"text": "We use A FEW with uncountable nouns.", "answer": False,
              "translation": "Usamos A FEW com substantivos incontáveis."},
         ]},
    ],
}

AULA15_LISTENING = {
    "title": "Listening — the shopping list",
    "lesson": 15,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: o OF fica fraco e ligado: \"a bóttleov water\", \"a lódov\". Preste atenção no número e no recipiente.",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"a cup of tea\" → a cup of tea",
         "audio": f"{AUDIO}/aula15-words.m4a",
         "text": "1. a [*jar|can] of honey\n2. two [*cans|tins] of soda\n3. a [*carton|bottle] of milk\n"
                 "4. two [*loaves|slices] of bread\n5. three [*scoops|cups] of ice cream\n6. a [*packet|box] of pasta"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"I drink a lot of water.\" → I drink [a lot of] water.",
         "audio": f"{AUDIO}/aula15-dictation.m4a",
         "text": "1. There are [a lot of] tomatoes in the fridge.\n2. I don't eat [much] chocolate.\n"
                 "3. How [many] cups of coffee do you drink?\n4. I have a [little] money left."},
        {"type": "info",
         "prompt": "Now listen: Paulo and Marta make a shopping list for a picnic.",
         "translation": "Agora ouça: o Paulo e a Marta fazem a lista de compras para um piquenique. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula15-list.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "They are planning a [picnic].",
         "text": "1. How many people are at the picnic? → [*Six.|Four.|Ten.]\n"
                 "2. How much bread do they need? → [*Two loaves.|Three loaves.|One slice.]\n"
                 "3. How much water do they need? → [*Four bottles.|Two bottles.|Six glasses.]\n"
                 "4. What do they buy for dessert? → [*A box of chocolate.|A tin of tuna.|A jar of honey.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Paulo and Marta are planning a picnic. → True",
         "statements": [
             {"text": "There is a lot of cheese at home.", "answer": False, "translation": "Tem muito queijo em casa."},
             {"text": "They buy some cans of soda.", "answer": True, "translation": "Eles compram algumas latas de refrigerante."},
             {"text": "Marta doesn't eat much chocolate.", "answer": False,
              "translation": "A Marta não come muito chocolate."},
         ]},
    ],
}

AULA15_SPEAKING = {
    "title": "Speaking — containers and quantities",
    "lesson": 15,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: OF tem som de V (\"ov\") e se liga à palavra anterior: \"a cup of\" = \"a cúpov\".",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as expressões da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula15-say-s{i}.m4a"} for i, t in enumerate(
             ["a bottle of water", "a can of soda", "a carton of milk", "a jar of honey", "a packet of pasta",
              "two loaves of bread", "three slices of cheese", "two scoops of ice cream", "a bar of chocolate",
              "There are a lot of tomatoes in the fridge.", "I don't eat much chocolate.",
              "I have a few oranges left."], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOU.",
         "translation": "Agora responda às perguntas sobre VOCÊ.",
         "example": "\"How much water do you drink in a day?\" → \"I drink a lot of water. Two bottles!\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula15-say-y{i}.m4a"} for i, t in enumerate(
             ["How many cups of coffee do you drink in a day?", "How much water do you drink in a day?",
              "Do you eat much chocolate?", "How many scoops of ice cream do you usually have?"], 1)]},
    ],
}

AULA15_READING = {
    "title": "Reading — Grandma's kitchen",
    "lesson": 15,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto da Júlia sobre a cozinha da avó dela. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula15-reading.m4a",
         "text": "GRANDMA'S KITCHEN\n\n"
                 "My grandma loves cooking, and her kitchen is always full of food!\n"
                 "In her cupboard, there are a lot of packets of pasta and rice, and there are many tins of tuna. "
                 "There are three jars of honey, too. Grandma has a little honey in her tea every morning.\n"
                 "In her fridge, there are two cartons of milk, a few eggs and a lot of cheese. "
                 "But there isn't much juice. Grandma doesn't drink much juice. She prefers water.\n"
                 "Every Sunday, she buys two loaves of bread at the bakery. And on my birthday? A big cake and three "
                 "scoops of ice cream for me!\n"
                 "How much sugar does Grandma eat? Not much. But how many cookies does she make? A lot!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Who loves cooking? → [Grandma.]",
         "text": "1. How many jars of honey are there? → [*Three.|Two.|A few.]\n"
                 "2. How much milk is in the fridge? → [*Two cartons.|Two bottles.|A little.]\n"
                 "3. What does Grandma buy on Sundays? → [*Two loaves of bread.|Two cartons of juice.|Three tins of tuna.]\n"
                 "4. What does Grandma drink? → [*Water, and tea in the morning.|A lot of juice.|A lot of soda.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Grandma's kitchen is full of food. → True",
         "statements": [
             {"text": "There is a lot of juice in the fridge.", "answer": False,
              "translation": "Tem muito suco na geladeira."},
             {"text": "Grandma has a little honey in her tea.", "answer": True,
              "translation": "A avó coloca um pouco de mel no chá."},
             {"text": "Grandma makes a lot of cookies.", "answer": True, "translation": "A avó faz muitos biscoitos."},
         ]},
        {"type": "fill",
         "prompt": "Complete according to the text.",
         "translation": "Complete de acordo com o texto.",
         "example": "There are many [tins] of tuna.",
         "text": "1. There are a lot of [packets] of pasta and rice.\n2. There are a [few] eggs.\n"
                 "3. Grandma doesn't drink [much] juice."},
    ],
}

AULA15_WRITING = {
    "title": "Writing — how much? how many?",
    "lesson": 15,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ How many + plural · How much + incontável.\n"
                   "a lot of (tudo) · many (plural) · much (incontável, negativa/pergunta) · a few (plural) · a little (incontável).",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Complete with How many or How much.",
         "translation": "Complete com How many ou How much.",
         "example": "[How many] apples do you want?",
         "text": "1. [How much] milk do you drink?\n2. [How many] bottles of water do we need?\n"
                 "3. [How much] money do you have?\n4. [How many] slices of cheese do you want?"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu quero uma xícara de chá. → I want a cup of tea.",
         "text": "1. Eu quero duas latas de refrigerante. → [I want two cans of soda.]\n"
                 "2. Eu não como muito chocolate. → [I don't eat much chocolate.|I do not eat much chocolate.|"
                 "I don't eat a lot of chocolate.]"},
        {"type": "free",
         "prompt": "Answer: How many cups of coffee do you drink in a day? How much water do you drink? "
                   "Do you eat much chocolate? Then write your shopping list for this week with containers.",
         "translation": "Responda: quantas xícaras de café você toma por dia? Quanta água você bebe? Você come muito "
                        "chocolate? Depois escreva a sua lista de compras da semana usando os recipientes.",
         "example": "I drink two cups of coffee in a day.",
         "model_answer": "I drink two cups of coffee in a day.\n"
                         "I drink a lot of water: about two bottles.\n"
                         "I don't eat much chocolate, only a little on Sundays.\n"
                         "My shopping list: two loaves of bread, a carton of milk, a jar of honey, "
                         "a packet of rice and a few bananas.",
         "keywords": ["cups of", "a lot of", "a carton of", "a few"], "min_words": 30, "points": 4},
    ],
}

AULA15_VIDEO = _video(15, AULA15_TOPIC, "Video — A picnic shopping trip",
                      "a Sarah compra comida para um piquenique e conta tudo com os recipientes: bottle, loaf, scoop…",
                      "aula15-video", [
    _q("Complete: a ___ of milk", "Complete: uma ___ de leite (no vídeo, ela coloca leite no copo)", "glass", "loaf",
       "slice", "scoop"),
    _q("What's the plural of \"loaf\"?", "Qual é o plural de \"loaf\"?", "loaves", "loafs", "loaf", "loafes"),
    _q("Complete: six ___ of water", "Complete: seis ___ de água", "bottles", "loaves", "scoops", "slices"),
    _q("Complete: two ___ of ice cream", "Complete: duas ___ de sorvete", "scoops", "balls", "slices", "loaves"),
])

# ---------- Aula 16 — Comparatives (https://youtu.be/daR67-eZHFc) ----------

AULA16_TOPIC = "Aula 16 — Comparatives"

AULA16_NUMBERS = {
    "title": "Large numbers: hundreds and thousands",
    "lesson": 16,
    "description": "100 = a hundred / one hundred · 1,000 = a thousand / one thousand (TH: língua entre os dentes!)\n"
                   "AND entre a centena e a dezena/unidade: 105 = a hundred AND five · 155 = a hundred and fifty-five\n"
                   "HÍFEN entre dezena e unidade: twenty-one, fifty-five, eighty-six\n"
                   "Do milhar para a centena NÃO tem and (só uma vírgula): 1,255 = a thousand, two hundred and fifty-five · "
                   "10,300 = ten thousand, three hundred\n"
                   "Do milhar direto para dezena/unidade, tem and: 1,005 = a thousand and five · 10,086 = ten thousand and eighty-six\n"
                   "10,000 = ten thousand · 20,000 = twenty thousand · 100,000 = a hundred thousand (thousand não vai para o plural!)",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "How do we say these numbers?",
         "translation": "Como falamos estes números em inglês?",
         "example": "150 → [a hundred and fifty]",
         "text": "1. 105 → [*a hundred and five|a hundred five|one hundreds and five]\n"
                 "2. 1,055 → [*a thousand and fifty-five|a thousand fifty and five|one thousands fifty-five]\n"
                 "3. 1,255 → [*a thousand, two hundred and fifty-five|a thousand and two hundred and fifty-five|"
                 "twelve thousand fifty-five]\n"
                 "4. 10,300 → [*ten thousand, three hundred|ten thousand and three hundreds|ten thousands three hundred]\n"
                 "5. 100,000 → [*a hundred thousand|a hundred thousands|ten thousand]"},
        {"type": "match",
         "prompt": "Match the numbers to the words.",
         "translation": "Ligue os números às palavras.",
         "example": "155 → a hundred and fifty-five",
         "pairs": [
             {"left": "1,005", "right": "a thousand and five"},
             {"left": "10,086", "right": "ten thousand and eighty-six"},
             {"left": "10,309", "right": "ten thousand, three hundred and nine"},
             {"left": "20,000", "right": "twenty thousand"},
             {"left": "300,000", "right": "three hundred thousand"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "We can say \"a hundred\" or \"one hundred\". → True",
         "statements": [
             {"text": "We say \"two thousands\" for 2,000.", "answer": False,
              "translation": "Dizemos \"two thousands\" para 2.000."},
             {"text": "We use a hyphen in \"fifty-five\".", "answer": True, "translation": "Usamos hífen em \"fifty-five\"."},
             {"text": "We use AND between thousands and hundreds: \"a thousand and two hundred\".", "answer": False,
              "translation": "Usamos AND entre milhar e centena: \"a thousand and two hundred\"."},
         ]},
    ],
}

AULA16_COMPARATIVES = {
    "title": "Comparatives: taller than, more beautiful than",
    "lesson": 16,
    "description": "O COMPARATIVO compara DUAS coisas, pessoas ou lugares. Na frase usamos THAN (do que / que).\n"
                   "1. Maioria: + ER → tall → taller · short → shorter · cold → colder: My brother is taller than me.\n"
                   "2. Curto com consoante-vogal-consoante: DOBRA + ER → big → bigger · hot → hotter\n"
                   "3. Consoante + Y: tira o Y + IER → easy → easier · happy → happier · healthy → healthier\n"
                   "4. Adjetivos LONGOS (2, 3, 4 sílabas): MORE + adjetivo → more beautiful · more dangerous · more expensive\n"
                   "5. Só 3 irregulares: good → better · bad → worse · far → further\n"
                   "Ex.: Brasília is hotter than Curitiba. · A car is more expensive than a bike.",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "Put the adjectives in the right group, by the comparative rule.",
         "translation": "Coloque os adjetivos no grupo certo, de acordo com a regra do comparativo.",
         "example": "tall → + er · big → double + er",
         "categories": ["+ er", "double + er", "y → ier", "more", "irregular"],
         "words": [
             {"text": "tall", "category": "+ er"}, {"text": "cold", "category": "+ er"}, {"text": "cheap", "category": "+ er"},
             {"text": "big", "category": "double + er"}, {"text": "hot", "category": "double + er"},
             {"text": "easy", "category": "y → ier"}, {"text": "healthy", "category": "y → ier"},
             {"text": "beautiful", "category": "more"}, {"text": "expensive", "category": "more"},
             {"text": "delicious", "category": "more"},
             {"text": "good", "category": "irregular"}, {"text": "bad", "category": "irregular"},
         ]},
        {"type": "fill",
         "prompt": "Write the comparative form.",
         "translation": "Escreva a forma comparativa.",
         "example": "short → shorter",
         "text": "1. small → [smaller]\n2. hot → [hotter]\n3. happy → [happier]\n4. dangerous → [more dangerous]\n"
                 "5. good → [better]\n6. bad → [worse]\n7. far → [further|farther]"},
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta (exemplos da aula).",
         "example": "The boy is [taller than] the girl.",
         "text": "1. The cat is [*smaller than|smaller that|more small than] the dog.\n"
                 "2. Canada is [*colder than|more cold than|colder] Brazil.\n"
                 "3. A car is [*more expensive than|expensiver than|more expensiver than] a bike.\n"
                 "4. A bike is [*cheaper than|more cheap than|cheapper than] a car.\n"
                 "5. Salad is [*healthier than|more healthy than|healthyer than] pizza.\n"
                 "6. Pizza is [*more delicious than|deliciouser than|more delicious that] salad."},
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras em ordem. (Curitiba é mais fria do que o Rio de Janeiro.)",
         "example": "is / taller / me / than / brother / My → My brother is taller than me.",
         "tokens": ["Curitiba", "is", "colder", "than", "Rio de Janeiro."], "alternatives": []},
    ],
}

AULA16_LISTENING = {
    "title": "Listening — which apartment?",
    "lesson": 16,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: o THAN é fraco e rápido (\"dhən\"). Nos números, preste atenção no AND e em THOUSAND.",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the number you hear.",
         "translation": "Ouça e escolha o número que você ouve.",
         "example": "Você ouve: \"a hundred and five\" → 105",
         "audio": f"{AUDIO}/aula16-numbers.m4a",
         "text": "1. [*150|115|1,500]\n2. [*1,005|1,500|1,050]\n3. [*10,086|10,860|1,086]\n"
                 "4. [*1,255|1,225|12,055]\n5. [*100,000|10,000|1,000]"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"My brother is taller than me.\" → My brother is [taller] than me.",
         "audio": f"{AUDIO}/aula16-dictation.m4a",
         "text": "1. Brasília is [hotter] than Curitiba.\n2. English is [easier] than Chinese.\n"
                 "3. A car is [more] expensive than a bike.\n4. My English is [better] now."},
        {"type": "info",
         "prompt": "Now listen: Bruno and Carla want to rent an apartment.",
         "translation": "Agora ouça: o Bruno e a Carla querem alugar um apartamento e comparam duas opções. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula16-apartments.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "They want to rent an [apartment].",
         "text": "1. How much is the apartment on Flores Street? → [*R$2,500|R$1,800|R$25,000]\n"
                 "2. Which apartment is bigger? → [*The apartment on Flores Street.|The apartment on Ocean Avenue.|"
                 "They are the same.]\n"
                 "3. Which apartment is closer to the beach? → [*The apartment on Ocean Avenue.|"
                 "The apartment on Flores Street.|Neither.]\n"
                 "4. Which apartment do they choose? → [*The apartment on Ocean Avenue.|"
                 "The apartment on Flores Street.|They don't choose.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Bruno and Carla want an apartment. → True",
         "statements": [
             {"text": "The apartment on Ocean Avenue is more expensive.", "answer": False,
              "translation": "O apartamento na Ocean Avenue é mais caro."},
             {"text": "The apartment on Flores Street is further from Carla's work.", "answer": True,
              "translation": "O apartamento na Flores Street é mais longe do trabalho da Carla."},
             {"text": "Bruno thinks the beach is better than a big kitchen.", "answer": True,
              "translation": "O Bruno acha que a praia é melhor do que uma cozinha grande."},
         ]},
    ],
}

AULA16_SPEAKING = {
    "title": "Speaking — numbers and comparisons",
    "lesson": 16,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: \"thousand\" com TH (não é \"fousand\") · o -ER final é curtinho: \"táler\", \"bíguer\".",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the numbers.",
         "translation": "Ouça e repita os números.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula16-say-n{i}.m4a"} for i, t in enumerate(
             ["105 — a hundred and five", "155 — a hundred and fifty-five", "1,000 — a thousand",
              "1,255 — a thousand, two hundred and fifty-five", "10,086 — ten thousand and eighty-six",
              "100,000 — a hundred thousand"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "\"The boy is taller than the girl.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula16-say-s{i}.m4a"} for i, t in enumerate(
             ["The boy is taller than the girl.", "The cat is smaller than the dog.", "Canada is colder than Brazil.",
              "A car is more expensive than a bike.", "Salad is healthier than pizza.",
              "Pizza is more delicious than salad."], 1)]},
        {"type": "speak",
         "prompt": "Now compare! Answer the questions.",
         "translation": "Agora compare! Responda às perguntas com o comparativo.",
         "example": "\"Who is taller, you or your mother?\" → \"I'm taller than my mother.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula16-say-y{i}.m4a"} for i, t in enumerate(
             ["Who is taller, you or your best friend?", "Which is colder, Curitiba or Rio de Janeiro?",
              "Which is more expensive, a car or a bike?", "Which is healthier, salad or pizza?"], 1)]},
    ],
}

AULA16_READING = {
    "title": "Reading — two sisters",
    "lesson": 16,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto da Paula sobre ela e a irmã. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula16-reading.m4a",
         "text": "TWO SISTERS\n\n"
                 "My name is Paula, and I have a sister, Renata. We are very different!\n"
                 "Renata is older than me. She's 30 and I'm 25. But I'm taller than her: I'm 1.70 m and she's 1.62 m.\n"
                 "Renata lives in Curitiba, and I live in Salvador. Curitiba is colder than Salvador, of course! "
                 "Salvador is about 2,400 kilometers from Curitiba. That's far!\n"
                 "Renata is a doctor. She works more than me, but her salary is bigger: she makes about "
                 "fifteen thousand reais a month.\n"
                 "I'm a teacher. My job is easier, and I think I'm happier. I have more free time, and the beach is near my house!\n"
                 "But Renata is a better cook than me. Her lasagna is more delicious than my lasagna!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Who is older? → [Renata.]",
         "text": "1. Who is taller? → [*Paula.|Renata.|They are the same.]\n"
                 "2. Which city is colder? → [*Curitiba.|Salvador.|The text doesn't say.]\n"
                 "3. How far is Salvador from Curitiba? → [*About 2,400 km.|About 240 km.|About 24,000 km.]\n"
                 "4. Who is a better cook? → [*Renata.|Paula.|Their mother.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Paula is a teacher. → True",
         "statements": [
             {"text": "Paula's salary is bigger than Renata's salary.", "answer": False,
              "translation": "O salário da Paula é maior do que o da Renata."},
             {"text": "Paula thinks she is happier than her sister.", "answer": True,
              "translation": "A Paula acha que é mais feliz do que a irmã."},
             {"text": "Renata works more than Paula.", "answer": True, "translation": "A Renata trabalha mais do que a Paula."},
         ]},
        {"type": "fill",
         "prompt": "Complete according to the text.",
         "translation": "Complete de acordo com o texto.",
         "example": "Renata is [older] than Paula.",
         "text": "1. Paula is [taller] than Renata.\n2. Paula's job is [easier].\n"
                 "3. Renata's lasagna is [more] delicious."},
    ],
}

AULA16_WRITING = {
    "title": "Writing — let's compare!",
    "lesson": 16,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ adjetivo + ER + THAN (taller than) · MORE + adjetivo longo + THAN (more beautiful than)\n"
                   "Irregulares: good → better · bad → worse · far → further.",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Complete with the comparative.",
         "translation": "Complete com o comparativo do adjetivo entre parênteses.",
         "example": "My brother is [taller] than me. (tall)",
         "text": "1. Rio de Janeiro is [hotter] than Curitiba. (hot)\n2. My bedroom is [bigger] than your bedroom. (big)\n"
                 "3. Math is [more difficult] than English. (difficult)\n4. This pizza is [better] than that pizza. (good)\n"
                 "5. I'm [happier] today than yesterday. (happy)"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "O gato é menor do que o cachorro. → The cat is smaller than the dog.",
         "text": "1. Minha mãe é mais baixa do que meu pai. → [My mother is shorter than my father.]\n"
                 "2. Um carro é mais caro do que uma bicicleta. → [A car is more expensive than a bike.|"
                 "A car is more expensive than a bicycle.]"},
        {"type": "free",
         "prompt": "Compare two people in your family (or two cities you know). Use at least four comparatives: "
                   "taller, older, more…, better…",
         "translation": "Compare duas pessoas da sua família (ou duas cidades que você conhece). Use pelo menos quatro "
                        "comparativos.",
         "example": "My father is older than my mother.",
         "model_answer": "My father is older than my mother. He's 60 and she's 56.\n"
                         "My mother is shorter than my father, but she is more organized than him.\n"
                         "My father is a better cook than my mother.\n"
                         "My mother is happier in the morning, and my father is happier at night!",
         "keywords": ["than", "more", "older"], "min_words": 30, "points": 4},
    ],
}

AULA16_VIDEO = _video(16, AULA16_TOPIC, "Video — Bigger, faster, colder",
                      "a Sarah compara animais, países, carro e bicicleta, salada e pizza.",
                      "aula16-video", [
    _q("Which is bigger?", "Qual é maior?", "The elephant is bigger than the mouse.",
       "The mouse is bigger than the elephant.", "The elephant is more big than the mouse.",
       "The elephant is biger than the mouse."),
    _q("Complete: The turtle is ___ than the cheetah.", "Complete: A tartaruga é ___ do que o guepardo.", "slower",
       "faster", "more slow", "slowier"),
    _q("Which country is colder?", "Qual país é mais frio?", "Canada.", "Brazil.", "They are the same.", "Rio de Janeiro."),
    _q("Complete: A bike is ___ than a car.", "Complete: Uma bicicleta é ___ do que um carro.", "cheaper",
       "more expensive", "more cheap", "cheapper"),
    _q("What does Sarah say about pizza?", "O que a Sarah diz sobre a pizza?", "It's more delicious than salad.",
       "It's healthier than salad.", "It's deliciouser than salad.", "It's cheaper than salad."),
])

# ---------- Aula 17 — Superlatives (https://youtu.be/ody8AaThA1c) ----------

AULA17_TOPIC = "Aula 17 — Superlatives"

AULA17_PLACES = {
    "title": "Places in town",
    "lesson": 17,
    "description": "PLACES IN TOWN: drugstore / pharmacy (farmácia) · church (igreja) · hospital · street market (feira) · park · "
                   "police station (delegacia) · post office (correio) · mall (shopping) · supermarket · "
                   "town hall / city hall (prefeitura) · museum · theater · zoo · bus station (rodoviária) · "
                   "railway station (estação de trem) · square (praça) · bank · cinema / movie theater · "
                   "bookstore (livraria) · gym (academia) · school · bakery (padaria) · restaurant · pet shop\n"
                   "Atenção: \"shopping\" é o ato de fazer compras! Let's go shopping. (vamos às compras) · "
                   "Let's go to the mall. (vamos ao shopping)\n"
                   "Where can you see animals? → At the zoo.",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the places to Portuguese.",
         "translation": "Ligue os lugares ao português.",
         "example": "bakery → padaria",
         "pairs": [
             {"left": "drugstore", "right": "farmácia"},
             {"left": "street market", "right": "feira"},
             {"left": "post office", "right": "correio"},
             {"left": "town hall", "right": "prefeitura"},
             {"left": "square", "right": "praça"},
             {"left": "bookstore", "right": "livraria"},
             {"left": "gym", "right": "academia"},
             {"left": "mall", "right": "shopping center"},
         ]},
        {"type": "dropdown",
         "prompt": "Answer the questions from the lesson.",
         "translation": "Responda às perguntas da aula (sempre AT THE + lugar).",
         "example": "Where can you see animals? → [At the zoo.]",
         "text": "1. Where can you do exercise? → [*At the gym.|At the church.|At the bakery.]\n"
                 "2. Where can you buy bread? → [*At the bakery.|At the bank.|At the post office.]\n"
                 "3. Where can you pray? → [*At the church.|At the zoo.|At the gym.]\n"
                 "4. Where can you go for a walk? → [*At the park.|At the bank.|At the drugstore.]\n"
                 "5. Where can you buy medicine? → [*At the drugstore.|At the bookstore.|At the theater.]\n"
                 "6. Where can you catch a bus to another city? → [*At the bus station.|At the town hall.|At the square.]"},
        {"type": "choice",
         "prompt": "You want to go to the shopping center with a friend. What do you say?",
         "translation": "Você quer ir ao shopping center com um amigo. O que você fala?",
         "example": "Let's go shopping. = Vamos fazer compras.",
         "options": ["Let's go to the mall.", "Let's go to the shopping.", "Let's go to shopping center the.",
                     "Let's go in the shopping."],
         "correct": 0},
    ],
}

AULA17_SUPERLATIVES = {
    "title": "Superlatives: the tallest, the most beautiful",
    "lesson": 17,
    "description": "COMPARATIVE → compara DUAS coisas: Mike is taller than Ana.\n"
                   "SUPERLATIVE → UM em relação ao GRUPO todo: Josh is the tallest (in the family).\n"
                   "Regras (com THE na frase):\n"
                   "1. Maioria: + EST → tall → the tallest · short → the shortest\n"
                   "2. Consoante-vogal-consoante: DOBRA + EST → big → the biggest · hot → the hottest\n"
                   "3. Consoante + Y: tira o Y + IEST → easy → the easiest · happy → the happiest · healthy → the healthiest\n"
                   "4. Adjetivos LONGOS: THE MOST + adjetivo → the most beautiful · the most dangerous · the most comfortable\n"
                   "5. Irregulares: good → the best · bad → the worst · far → the furthest\n"
                   "Com possessivo, sem THE: My best friend is Ana. (✗ my the best friend)",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the superlative form.",
         "translation": "Escreva a forma superlativa (com THE).",
         "example": "tall → the tallest",
         "text": "1. short → [the shortest]\n2. big → [the biggest]\n3. easy → [the easiest]\n"
                 "4. beautiful → [the most beautiful]\n5. good → [the best]\n6. bad → [the worst]\n"
                 "7. far → [the furthest|the farthest]"},
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta (exemplos da aula).",
         "example": "Josh is [the tallest] in the family.",
         "text": "1. Orange juice is [*the healthiest|the most healthy|healthiest] of the four drinks.\n"
                 "2. Sneakers are [*the most comfortable|the comfortablest|the more comfortable] of the four shoes.\n"
                 "3. Soccer is [*the most popular|the popularest|the more popular] sport in Brazil.\n"
                 "4. Gisele is [*the prettiest|the most pretty|the prettyest] woman in the world.\n"
                 "5. Salad is [*the healthiest|the healthier|the most healthiest] food in my diet.\n"
                 "6. McDonald's has [*the most delicious|the deliciousest|the more delicious] burger."},
        {"type": "dropdown",
         "prompt": "Comparative or superlative? Choose.",
         "translation": "Comparativo (2 coisas) ou superlativo (1 do grupo)? Escolha.",
         "example": "Mike is [taller than] Ana.",
         "text": "1. My brother is [*taller than|the tallest] me.\n"
                 "2. My brother is [*the tallest|taller than] person in my family.\n"
                 "3. Curitiba is [*colder than|the coldest] Salvador.\n"
                 "4. This is [*the best|better than] restaurant in my city.\n"
                 "5. [*My best friend|My the best friend] is Ana."},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "We use the superlative for one person in a group. → True",
         "statements": [
             {"text": "We use the comparative to compare one thing with a whole group.", "answer": False,
              "translation": "Usamos o comparativo para comparar uma coisa com um grupo inteiro."},
             {"text": "The superlative of \"good\" is \"the best\".", "answer": True,
              "translation": "O superlativo de \"good\" é \"the best\"."},
             {"text": "We say \"the most tall\".", "answer": False, "translation": "Dizemos \"the most tall\"."},
         ]},
    ],
}

AULA17_LISTENING = {
    "title": "Listening — a tour of the town",
    "lesson": 17,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: o THE antes do superlativo é fraco (\"dhə\"). Preste atenção no final -EST e no MOST.",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the place you hear.",
         "translation": "Ouça e escolha o lugar que você ouve.",
         "example": "Você ouve: \"bakery\" → bakery",
         "audio": f"{AUDIO}/aula17-places.m4a",
         "text": "1. [*drugstore|bookstore]\n2. [*post office|police station]\n3. [*museum|mall]\n4. [*theater|town hall]\n"
                 "5. [*railway station|bus station]\n6. [*square|school]"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"Josh is the tallest.\" → Josh is the [tallest].",
         "audio": f"{AUDIO}/aula17-dictation.m4a",
         "text": "1. This is the [biggest] park in the city.\n2. Soccer is the most [popular] sport in Brazil.\n"
                 "3. It's the [best] bakery in town.\n4. August is the [coldest] month here."},
        {"type": "info",
         "prompt": "Now listen: a guide shows the town to a tourist.",
         "translation": "Agora ouça: um guia mostra a cidade de Pinewood para uma turista. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula17-tour.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "The town is [Pinewood].",
         "text": "1. What is the oldest building in town? → [*The church.|The museum.|The town hall.]\n"
                 "2. What's the most popular place on weekends? → [*The park.|The mall.|The zoo.]\n"
                 "3. Where is the best coffee in town? → [*At Rosa's Bakery.|At the museum café.|At the mall.]\n"
                 "4. What's the most interesting thing at the museum? → [*An old train.|A dinosaur.|A big painting.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "The man is a tour guide. → True",
         "statements": [
             {"text": "The church is 100 years old.", "answer": False, "translation": "A igreja tem 100 anos."},
             {"text": "The museum is free on Sundays.", "answer": True, "translation": "O museu é de graça aos domingos."},
             {"text": "The tourist wants to go to the bakery first.", "answer": True,
              "translation": "A turista quer ir à padaria primeiro."},
         ]},
    ],
}

AULA17_SPEAKING = {
    "title": "Speaking — places and superlatives",
    "lesson": 17,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: police = \"pəLÍS\" (sem o E no final) · museum = \"miuZÍəm\" (feche os lábios no M) · "
                   "post office = \"pôustófis\".",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the places.",
         "translation": "Ouça e repita os lugares da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula17-say-p{i}.m4a"} for i, t in enumerate(
             ["drugstore, church, hospital", "street market, park, police station", "post office, mall, supermarket",
              "town hall, museum, theater", "zoo, bus station, railway station", "square, bank, cinema",
              "bookstore, gym, school", "bakery, restaurant, pet shop"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases com superlativos.",
         "example": "\"Josh is the tallest in the family.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula17-say-s{i}.m4a"} for i, t in enumerate(
             ["Josh is the tallest in the family.", "Orange juice is the healthiest of the four drinks.",
              "Soccer is the most popular sport in Brazil.", "My best friend is Ana."], 1)]},
        {"type": "speak",
         "prompt": "Now answer the homework questions from the lesson.",
         "translation": "Agora responda às perguntas da tarefa de casa da aula, com respostas completas.",
         "example": "\"Who is the tallest person in your family?\" → \"My brother is the tallest person in my family.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula17-say-y{i}.m4a"} for i, t in enumerate(
             ["Who is the tallest person in your family?", "What is the best restaurant in your city?",
              "What is the most beautiful city in Brazil?", "What is the most delicious food you can cook?"], 1)]},
    ],
}

AULA17_READING = {
    "title": "Reading — the best town in the world",
    "lesson": 17,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto do Diego sobre a cidade dele, no interior de Minas Gerais. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula17-reading.m4a",
         "text": "THE BEST TOWN IN THE WORLD\n\n"
                 "I live in Santa Luz, a small town in Minas Gerais. For me, it's the best town in the world!\n"
                 "The most important place is the main square. On Sundays, there is a street market there, "
                 "and all the families go.\n"
                 "Next to the square, there is São José Church. It's the oldest building in town: it's 250 years old.\n"
                 "The best bakery is Dona Maria's Bakery. Her cheese bread is the most delicious in Minas!\n"
                 "We don't have a mall or a zoo, but we have a beautiful park and a small museum.\n"
                 "July is the coldest month, and January is the hottest. The happiest time of the year? "
                 "The town party in June!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Where is Santa Luz? → [In Minas Gerais.]",
         "text": "1. What's the most important place? → [*The main square.|The church.|The park.]\n"
                 "2. What's the oldest building? → [*São José Church.|The museum.|Dona Maria's Bakery.]\n"
                 "3. What's the coldest month? → [*July.|January.|June.]\n"
                 "4. What's the happiest time of the year? → [*The town party in June.|Christmas.|The street market.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Diego loves his town. → True",
         "statements": [
             {"text": "Santa Luz has a big mall.", "answer": False, "translation": "Santa Luz tem um shopping grande."},
             {"text": "The street market is on Sundays.", "answer": True, "translation": "A feira é aos domingos."},
             {"text": "Dona Maria's cheese bread is the most delicious in Minas.", "answer": True,
              "translation": "O pão de queijo da Dona Maria é o mais gostoso de Minas."},
         ]},
        {"type": "fill",
         "prompt": "Complete according to the text.",
         "translation": "Complete de acordo com o texto.",
         "example": "It's the [best] town in the world.",
         "text": "1. The church is the [oldest] building in town.\n2. January is the [hottest] month.\n"
                 "3. The [most] important place is the main square."},
    ],
}

AULA17_WRITING = {
    "title": "Writing — the best of my city",
    "lesson": 17,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ THE + adjetivo + EST (the tallest, the biggest, the easiest) · "
                   "THE MOST + adjetivo longo (the most beautiful) · the best · the worst · the furthest.",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Complete with the superlative.",
         "translation": "Complete com o superlativo do adjetivo entre parênteses.",
         "example": "Josh is [the tallest] in the family. (tall)",
         "text": "1. This is [the biggest] park in my city. (big)\n2. It's [the most expensive] restaurant in town. (expensive)\n"
                 "3. Friday is [the happiest] day of the week. (happy)\n4. That was [the worst] movie of the year. (bad)"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Ele é o mais alto da família. → He is the tallest in the family.",
         "text": "1. Esta é a melhor padaria da cidade. → [This is the best bakery in the city.|"
                 "This is the best bakery in town.]\n"
                 "2. O futebol é o esporte mais popular do Brasil. → [Soccer is the most popular sport in Brazil.|"
                 "Football is the most popular sport in Brazil.]"},
        {"type": "free",
         "prompt": "Answer the homework questions with complete answers: Who is the tallest person in your family? "
                   "What is the best restaurant in your city? What is the most beautiful city in Brazil? "
                   "What is the most delicious food you can cook?",
         "translation": "Responda às perguntas da tarefa de casa da aula com respostas completas.",
         "example": "My brother is the tallest person in my family.",
         "model_answer": "My brother is the tallest person in my family.\n"
                         "The best restaurant in my city is Casa Verde.\n"
                         "The most beautiful city in Brazil is Florianópolis.\n"
                         "The most delicious food I can cook is lasagna.",
         "keywords": ["the tallest", "the best", "the most"], "min_words": 30, "points": 4},
    ],
}

AULA17_VIDEO = _video(17, AULA17_TOPIC, "Video — The best places in my town",
                      "o Paul mostra os melhores lugares da cidade dele: o maior parque, a igreja mais antiga, "
                      "a melhor padaria…",
                      "aula17-video", [
    _q("What's this park?", "O que é este parque?", "The biggest park in town.", "The smallest park in town.",
       "The most big park in town.", "The bigger park in town."),
    _q("How old is the church?", "Quantos anos tem a igreja?", "300 years old. It's the oldest church.",
       "30 years old. It's the newest church.", "100 years old. It's the oldest church.",
       "300 years old. It's the older church."),
    _q("Complete: This is the ___ bakery in town.", "Complete: Esta é a ___ padaria da cidade.", "best", "goodest",
       "most good", "better"),
    _q("What's the most popular place on weekends?", "Qual é o lugar mais popular nos fins de semana?", "The mall.",
       "The church.", "The bakery.", "The zoo."),
    _q("What's the tallest animal at the zoo?", "Qual é o animal mais alto do zoológico?", "The giraffe.",
       "The elephant.", "The horse.", "The lion."),
])

# ---------- Aula 18 — Directions (https://youtu.be/2ZsKCVaBAGU) ----------

AULA18_TOPIC = "Aula 18 — Directions"

AULA18_VOCAB = {
    "title": "Directions: turn right, go straight on…",
    "lesson": 18,
    "description": "➡️ turn right (vire à direita) · ⬅️ turn left (vire à esquerda) · ⬆️ go straight on (siga reto)\n"
                   "↩️ turn around / take the U-turn (faça o retorno)\n"
                   "at the corner (na esquina) · at the traffic light (no semáforo) · at the intersection (no cruzamento) · "
                   "at the roundabout (na rotatória / no balão)\n"
                   "walk one block / two blocks (ande uma / duas quadras) · go past the church (passe pela igreja) · "
                   "go over the bridge (atravesse a ponte)\n"
                   "on your left / on your right (à sua esquerda / direita) · next to (ao lado de)\n"
                   "Pronúncia: straight = \"strêit\" (sem o GH) · straight on = \"strêiron\".",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the directions to Portuguese.",
         "translation": "Ligue as direções ao português.",
         "example": "turn right → vire à direita",
         "pairs": [
             {"left": "turn left", "right": "vire à esquerda"},
             {"left": "go straight on", "right": "siga reto"},
             {"left": "take the U-turn", "right": "faça o retorno"},
             {"left": "at the corner", "right": "na esquina"},
             {"left": "at the traffic light", "right": "no semáforo"},
             {"left": "at the intersection", "right": "no cruzamento"},
             {"left": "at the roundabout", "right": "na rotatória"},
             {"left": "go past the church", "right": "passe pela igreja"},
         ]},
        {"type": "dropdown",
         "prompt": "Look at the signs and choose.",
         "translation": "Olhe os sinais e escolha a direção certa.",
         "example": "➡️ → [Turn right.]",
         "text": "1. ⬅️ → [*Turn left.|Turn right.|Go straight on.]\n2. ⬆️ → [*Go straight on.|Turn around.|Turn left.]\n"
                 "3. ↩️ → [*Take the U-turn.|Go past the school.|Turn right.]\n"
                 "4. 🚦 → [*at the traffic light|at the roundabout|at the corner]\n"
                 "5. 🌉 → [*Go over the bridge.|Walk one block.|Turn around.]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Turn right\" means vire à direita. → True",
         "statements": [
             {"text": "We pronounce the GH in \"straight\".", "answer": False,
              "translation": "Pronunciamos o GH em \"straight\"."},
             {"text": "A roundabout is a rotatória (balão).", "answer": True, "translation": "Roundabout é uma rotatória (balão)."},
             {"text": "\"Go past the church\" means turn at the church.", "answer": False,
              "translation": "\"Go past the church\" significa virar na igreja."},
             {"text": "A U-turn has the shape of the letter U.", "answer": True, "translation": "O retorno tem o formato da letra U."},
         ]},
    ],
}

AULA18_ASKING = {
    "title": "Asking for and giving directions",
    "lesson": 18,
    "description": "PEDIR DIREÇÕES (troque o lugar pelo que você procura):\n"
                   "Is there a mall near here? (Tem um shopping aqui perto?)\n"
                   "Where can I find a drugstore? (Onde eu encontro uma farmácia?)\n"
                   "How far is the hospital from here? (Qual é a distância do hospital até aqui?)\n"
                   "Excuse me, I'm looking for the city hall. Can you help me? (mais educado)\n"
                   "DAR DIREÇÕES (exemplo do mapa da aula, do posto ao museu):\n"
                   "Go straight on Elm Street. Go past the park. Turn right on Park Avenue. Then, turn left on Oak Street. "
                   "The museum is next to the church.",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the questions to Portuguese.",
         "translation": "Ligue as perguntas ao português.",
         "example": "Is there a mall near here? → Tem um shopping aqui perto?",
         "pairs": [
             {"left": "Where can I find a drugstore?", "right": "Onde eu encontro uma farmácia?"},
             {"left": "How far is the hospital from here?", "right": "Qual é a distância do hospital até aqui?"},
             {"left": "I'm looking for the city hall.", "right": "Estou procurando a prefeitura."},
             {"left": "Can you help me?", "right": "Você pode me ajudar?"},
         ]},
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras em ordem. (Com licença, estou procurando o banco.)",
         "example": "near / a / here / Is / mall / there → Is there a mall near here?",
         "tokens": ["Excuse", "me,", "I'm", "looking", "for", "the", "bank."], "alternatives": []},
        {"type": "fill",
         "prompt": "Complete the directions with go, turn, past, over or on.",
         "translation": "Complete as direções da aula (Sally vai até o restaurante) com go, turn, past, over ou on.",
         "example": "[Go] straight on Main Street.",
         "text": "1. Go straight [on] Main Street.\n2. [Turn] right on Pine Street.\n3. Go [over] the bridge.\n"
                 "4. Go [past] River Street.\n5. The diner is at the [corner] on the right."},
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta.",
         "example": "The bank is [on your left], next to the pet shop.",
         "text": "1. [*Turn right|Turn to right|Right turn] at the traffic light.\n"
                 "2. Walk two [*blocks|block|blockes] and turn left.\n"
                 "3. The museum is [*next to|next|near of] the church.\n"
                 "4. [*How far|How much far|How long far] is the hospital from here?"},
    ],
}

AULA18_LISTENING = {
    "title": "Listening — how do I get to the bus station?",
    "lesson": 18,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: anote as direções na ordem: primeiro, depois, no final. Preste atenção em LEFT e RIGHT!",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"turn left\" → turn left",
         "audio": f"{AUDIO}/aula18-words.m4a",
         "text": "1. [*turn right|turn left]\n2. [*go straight on|go past]\n3. [*at the roundabout|at the corner]\n"
                 "4. [*walk two blocks|walk one block]\n5. [*at the intersection|at the traffic light]\n6. [*take the U-turn|turn around]"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"Turn left at the corner.\" → Turn [left] at the corner.",
         "audio": f"{AUDIO}/aula18-dictation.m4a",
         "text": "1. Go straight on and turn [right] at the traffic light.\n2. Go [past] the school.\n"
                 "3. Is there a [drugstore] near here?\n4. The bank is [next] to the post office."},
        {"type": "info",
         "prompt": "Now listen: a tourist asks for directions.",
         "translation": "Agora ouça: um turista pede informação para chegar à rodoviária. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula18-tourist.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "The man is looking for the [bus station].",
         "text": "1. Where does he turn left? → [*At the traffic light.|At the roundabout.|At the corner.]\n"
                 "2. What does he go past? → [*The hospital.|The church.|The school.]\n"
                 "3. How many blocks does he walk? → [*Two.|One.|Three.]\n"
                 "4. Where is the bus station? → [*At the corner, on the right.|Next to the hospital.|On the left, next to the bank.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "The man is a tourist. → True",
         "statements": [
             {"text": "The bus station is very far.", "answer": False, "translation": "A rodoviária é muito longe."},
             {"text": "It's a ten-minute walk.", "answer": True, "translation": "É uma caminhada de dez minutos."},
             {"text": "The man goes over a bridge.", "answer": False, "translation": "O homem atravessa uma ponte."},
         ]},
    ],
}

AULA18_SPEAKING = {
    "title": "Speaking — asking and giving directions",
    "lesson": 18,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: \"straight on\" se liga: \"strêiron\" · \"turn left\" = \"târn léft\".",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the directions.",
         "translation": "Ouça e repita as direções da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula18-say-d{i}.m4a"} for i, t in enumerate(
             ["Turn right.", "Turn left.", "Go straight on.", "Turn around.", "Take the U-turn.", "at the corner",
              "at the traffic light", "at the intersection", "at the roundabout", "Walk one block.",
              "Go past the church."], 1)]},
        {"type": "speak",
         "prompt": "Now ask for directions.",
         "translation": "Agora peça informações (as perguntas da aula).",
         "example": "\"Excuse me, I'm looking for the city hall. Can you help me?\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula18-say-q{i}.m4a"} for i, t in enumerate(
             ["Is there a mall near here?", "Where can I find a drugstore?", "How far is the hospital from here?",
              "Excuse me, I'm looking for the city hall. Can you help me?"], 1)]},
    ],
}

AULA18_READING = {
    "title": "Reading — directions to the party",
    "lesson": 18,
    "subject": "Reading",
    "description": "Leia (e ouça) a mensagem e responda às perguntas de acordo com o texto.",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the message.",
         "translation": "Leia e ouça a mensagem que a Bianca mandou para os amigos com o caminho até a festa dela. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula18-reading.m4a",
         "text": "HOW TO GET TO MY PARTY 🎉\n\n"
                 "Hi, everyone! My birthday party is on Saturday at 8 p.m. Here are the directions from the subway station.\n"
                 "Leave the station and go straight on Rio Branco Avenue. Go past the big supermarket and the post office.\n"
                 "At the traffic light, turn right on Flores Street. Walk two blocks.\n"
                 "At the roundabout, turn left. You can see a small square with a fountain.\n"
                 "My building is at the corner, next to the bakery. It's number 45. "
                 "The bakery has the best cake in town, so I have a big cake for you!\n"
                 "It's a fifteen-minute walk. See you there!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "When is the party? → [On Saturday at 8 p.m.]",
         "text": "1. Where do the directions start? → [*At the subway station.|At the bus station.|At the square.]\n"
                 "2. What do you go past on Rio Branco Avenue? → [*A supermarket and the post office.|"
                 "A bakery and a bank.|A church and a school.]\n"
                 "3. Where do you turn right? → [*At the traffic light.|At the roundabout.|At the corner.]\n"
                 "4. Where is Bianca's building? → [*At the corner, next to the bakery.|Next to the post office.|"
                 "On Rio Branco Avenue.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "It's Bianca's birthday party. → True",
         "statements": [
             {"text": "You turn left at the roundabout.", "answer": True, "translation": "Você vira à esquerda na rotatória."},
             {"text": "You walk three blocks on Flores Street.", "answer": False,
              "translation": "Você anda três quadras na Flores Street."},
             {"text": "It's a five-minute walk.", "answer": False, "translation": "É uma caminhada de cinco minutos."},
         ]},
        {"type": "fill",
         "prompt": "Complete the directions according to the text.",
         "translation": "Complete as direções de acordo com o texto.",
         "example": "Go [straight] on Rio Branco Avenue.",
         "text": "1. Go [past] the big supermarket.\n2. At the traffic light, turn [right].\n3. Walk two [blocks].\n"
                 "4. My building is next [to] the bakery."},
    ],
}

AULA18_WRITING = {
    "title": "Writing — how to get to my house",
    "lesson": 18,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Go straight on… · Turn right / left on… · at the traffic light / corner / roundabout · "
                   "Walk two blocks · Go past the… · Go over the bridge · It's next to the… / on your left.",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate the directions.",
         "translation": "Traduza as direções.",
         "example": "Vire à direita. → Turn right.",
         "text": "1. Siga reto. → [Go straight on.|Go straight.]\n2. Vire à esquerda no semáforo. → "
                 "[Turn left at the traffic light.]\n3. Passe pela escola. → [Go past the school.]\n"
                 "4. Fica na esquina. → [It's at the corner.|It is at the corner.]"},
        {"type": "fill",
         "prompt": "Ask for directions in English.",
         "translation": "Peça informações em inglês.",
         "example": "Tem um shopping aqui perto? → Is there a mall near here?",
         "text": "1. Tem uma farmácia aqui perto? → [Is there a drugstore near here?|Is there a pharmacy near here?]\n"
                 "2. Onde eu encontro um banco? → [Where can I find a bank?]"},
        {"type": "free",
         "prompt": "A friend is at the nearest bus stop (or subway station). Write the directions to your house. "
                   "Use at least four steps.",
         "translation": "Um amigo está no ponto de ônibus (ou estação de metrô) mais perto. Escreva o caminho até a sua "
                        "casa, com pelo menos quatro passos.",
         "example": "Go straight on Paulista Avenue.",
         "model_answer": "Go straight on Paulista Avenue and go past the bank.\n"
                         "Turn left at the traffic light, on Augusta Street.\n"
                         "Walk two blocks and turn right at the corner.\n"
                         "My house is on your left, next to the bakery. It's number 120.",
         "keywords": ["Go straight on", "Turn", "at the"], "min_words": 30, "points": 4},
    ],
}

AULA18_VIDEO = _video(18, AULA18_TOPIC, "Video — Excuse me, where is the museum?",
                      "um turista pede informação na rua e a Sarah explica o caminho até o museu.",
                      "aula18-video", [
    _q("What is the man looking for?", "O que o homem está procurando?", "The museum.", "The bus station.",
       "The bank.", "The church."),
    _q("Where does he turn left?", "Onde ele vira à esquerda?", "At the traffic light.", "At the roundabout.",
       "At the corner.", "At the bridge."),
    _q("How many blocks does he walk?", "Quantas quadras ele anda?", "Two blocks.", "One block.", "Three blocks.",
       "Ten blocks."),
    _q("What does he do at the roundabout?", "O que ele faz na rotatória?", "He turns right.", "He turns left.",
       "He takes the U-turn.", "He goes straight on."),
    _q("Where is the museum?", "Onde fica o museu?", "At the corner, next to the church.", "Next to the bank.",
       "Over the bridge, on the left.", "At the traffic light."),
])

# ---------- Aula 19 — A, An, The (https://youtu.be/nmqFvvbporM) ----------

AULA19_TOPIC = "Aula 19 — A, An, The"

AULA19_JOBS = {
    "title": "Jobs with -ER and -OR",
    "lesson": 19,
    "description": "Verbo + ER / OR = a pessoa que faz a ação (o \"agente\", muitas vezes a profissão):\n"
                   "teach → teacher · sing → singer · paint → painter · write → writer · manage → manager · "
                   "design → designer · compose → composer · program → programmer (dobra o M!)\n"
                   "invent → inventor · act → actor · direct → director · conduct → conductor (maestro) · "
                   "edit → editor\n"
                   "ER e OR têm o MESMO SOM no final (\"ər\"). Para saber qual usar, é prática e leitura!\n"
                   "Atenção: edit (Édit) → editor (Éditər) · direct no sentido de dirigir um filme (dirigir carro = drive → driver).",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the person who does the action.",
         "translation": "Escreva a pessoa que faz a ação, com -ER ou -OR (exercício da aula).",
         "example": "teach → teacher · invent → inventor",
         "text": "1. sing → [singer]\n2. act → [actor]\n3. manage → [manager]\n4. program → [programmer]\n"
                 "5. direct → [director]\n6. paint → [painter]\n7. write → [writer]\n8. edit → [editor]"},
        {"type": "group",
         "prompt": "-ER or -OR? Put each job in the right group.",
         "translation": "-ER ou -OR? Coloque cada profissão no grupo certo.",
         "example": "teacher → -er · actor → -or",
         "categories": ["-er", "-or"],
         "words": [
             {"text": "teach…", "category": "-er"}, {"text": "sing…", "category": "-er"},
             {"text": "design…", "category": "-er"}, {"text": "compose…", "category": "-er"},
             {"text": "invent…", "category": "-or"}, {"text": "act…", "category": "-or"},
             {"text": "conduct…", "category": "-or"}, {"text": "direct…", "category": "-or"},
         ]},
        {"type": "match",
         "prompt": "Match the jobs to Portuguese.",
         "translation": "Ligue as profissões ao português.",
         "example": "teacher → professor(a)",
         "pairs": [
             {"left": "writer", "right": "escritor(a)"},
             {"left": "painter", "right": "pintor(a)"},
             {"left": "manager", "right": "gerente"},
             {"left": "conductor", "right": "maestro / maestrina"},
             {"left": "composer", "right": "compositor(a)"},
             {"left": "programmer", "right": "programador(a)"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "A singer sings. → True",
         "statements": [
             {"text": "-ER and -OR have different sounds.", "answer": False,
              "translation": "-ER e -OR têm sons diferentes."},
             {"text": "In \"programmer\", we double the M.", "answer": True,
              "translation": "Em \"programmer\", dobramos o M."},
             {"text": "A conductor drives a car.", "answer": False, "translation": "Um conductor dirige um carro."},
         ]},
    ],
}

AULA19_ARTICLES = {
    "title": "A, an, the or no article?",
    "lesson": 19,
    "description": "A / AN (artigos indefinidos):\n"
                   "  • para dizer o que algo é: What is this? It's a photo of my daughter.\n"
                   "  • para PROFISSÕES no singular: He is a doctor. · She is an architect. (plural: They are doctors.)\n"
                   "  • em frequência: three times a week · once a month · twice a year\n"
                   "  • 1ª vez que falamos de algo: I have a cat and a dog.\n"
                   "THE (artigo definido):\n"
                   "  • os dois sabem do que se fala: Can you close the window, please?\n"
                   "  • algo ÚNICO: the moon · the sun\n"
                   "  • antes do SUPERLATIVO: It's the best restaurant I know.\n"
                   "  • 2ª vez que falamos de algo: The cat is very old, but the dog is just a puppy.\n"
                   "SEM ARTIGO: generalizando (Men are more interested in sports than women. · I love cats.) · "
                   "antes de possessivo com 's (She is my mother's cousin.) · refeições (have breakfast / lunch / dinner) · "
                   "cidades e países (Brazil is a big country.) · by + transporte (by car, by bus).",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose a, an, the or — (no article).",
         "translation": "Escolha a, an, the ou — (sem artigo). Exercício do final da aula.",
         "example": "I saw [a] movie last night.",
         "text": "1. What does your sister do? She is [*an|a|the] architect.\n"
                 "2. I go to the gym twice [*a|the|—] week.\n"
                 "3. This is [*the|a|—] most interesting movie I've ever seen.\n"
                 "4. I saw a movie last night. [*The|A|—] movie was very interesting.\n"
                 "5. We usually have [*—|a|the] lunch at noon.\n"
                 "6. I love [*—|the|a] cats.\n"
                 "7. [*The|A|—] sun rises early in the summer."},
        {"type": "match",
         "prompt": "Match the sentences to the rules.",
         "translation": "Ligue cada frase à regra da aula.",
         "example": "He is a doctor. → job",
         "pairs": [
             {"left": "He is a doctor.", "right": "A / AN: job"},
             {"left": "three times a week", "right": "A / AN: frequency"},
             {"left": "The moon is beautiful today.", "right": "THE: only one (unique)"},
             {"left": "It's the best restaurant I know.", "right": "THE: superlative"},
             {"left": "Brazil is a big country.", "right": "no article: countries"},
             {"left": "I go to work by bus.", "right": "no article: by + transport"},
         ]},
        {"type": "choice",
         "prompt": "Which sentence is correct?",
         "translation": "Qual frase está correta?",
         "example": "She is my mother's cousin. ✓",
         "options": ["I live in Brazil, and I go to work by car.", "I live in the Brazil, and I go to work by the car.",
                     "I live in Brazil, and I go to the work by a car.", "I live in a Brazil, and I go to work by car."],
         "correct": 0},
        {"type": "fill",
         "prompt": "Complete with a or the.",
         "translation": "Complete com a ou the (1ª vez que se fala = a · 2ª vez = the).",
         "example": "I have [a] cat. [The] cat is old.",
         "text": "1. I have [a] cat and [a] dog. [The] cat is very old, but [the] dog is just a puppy.\n"
                 "2. Can you close [the] window, please?\n3. My father is [a] teacher."},
    ],
}

AULA19_LISTENING = {
    "title": "Listening — what do you do?",
    "lesson": 19,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: A, AN e THE são fracos na frase (\"ə\", \"ən\", \"dhə\"). Ouça a palavra seguinte para ajudar.",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the job you hear.",
         "translation": "Ouça e escolha a profissão que você ouve.",
         "example": "Você ouve: \"teacher\" → teacher",
         "audio": f"{AUDIO}/aula19-jobs.m4a",
         "text": "1. [*painter|printer]\n2. [*actor|doctor]\n3. [*writer|waiter]\n4. [*designer|director]\n"
                 "5. [*programmer|composer]\n6. [*manager|singer]"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete with a, an or the.",
         "translation": "Ditado: ouça e complete com a, an ou the.",
         "example": "Você ouve: \"He is a doctor.\" → He is [a] doctor.",
         "audio": f"{AUDIO}/aula19-dictation.m4a",
         "text": "1. She is [an] actor.\n2. I have English class twice [a] week.\n3. [The] moon is beautiful tonight.\n"
                 "4. It's [the] best pizza in town."},
        {"type": "info",
         "prompt": "Now listen: Rita and Sam meet at a party.",
         "translation": "Agora ouça: a Rita e o Sam se conhecem em uma festa e falam sobre o trabalho e a família. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula19-party.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Rita and Sam are at a [party].",
         "text": "1. What does Sam do? → [*He's a programmer.|He's a designer.|He's an actor.]\n"
                 "2. What does Rita do? → [*She's a designer.|She's a writer.|She's a singer.]\n"
                 "3. How often does Rita's band play? → [*Twice a month.|Twice a week.|Once a year.]\n"
                 "4. What does Rita's brother do? → [*He's an actor.|He's a teacher.|He's a manager.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Sam works with computers. → True",
         "statements": [
             {"text": "Sam works at home.", "answer": True, "translation": "O Sam trabalha em casa."},
             {"text": "Rita is a singer in a band.", "answer": True, "translation": "A Rita é cantora em uma banda."},
             {"text": "Rita's brother is in a movie now.", "answer": False,
              "translation": "O irmão da Rita está em um filme agora."},
         ]},
    ],
}

AULA19_SPEAKING = {
    "title": "Speaking — jobs and articles",
    "lesson": 19,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: -ER e -OR têm o mesmo som curtinho no final: \"TÍtchər\", \"ÉKtər\".",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the jobs.",
         "translation": "Ouça e repita as profissões da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula19-say-j{i}.m4a"} for i, t in enumerate(
             ["teacher, inventor, singer, actor", "manager, programmer, director", "painter, writer, composer",
              "conductor, editor, designer"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "\"She is an architect.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula19-say-s{i}.m4a"} for i, t in enumerate(
             ["It's a photo of my daughter.", "He is a doctor.", "She is an architect.",
              "They have classes three times a week.", "Can you close the window, please?",
              "I have a cat and a dog. The cat is very old, but the dog is just a puppy."], 1)]},
        {"type": "speak",
         "prompt": "Now answer about YOU.",
         "translation": "Agora responda sobre VOCÊ.",
         "example": "\"What do you do?\" → \"I'm a nurse.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula19-say-y{i}.m4a"} for i, t in enumerate(
             ["What do you do?", "What does your mother do?", "How often do you study English?",
              "Do you have a pet?"], 1)]},
    ],
}

AULA19_READING = {
    "title": "Reading — an artistic family",
    "lesson": 19,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto do Gabriel sobre a família dele, cheia de artistas. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula19-reading.m4a",
         "text": "AN ARTISTIC FAMILY\n\n"
                 "My family is very artistic! My mother is a painter. She paints every day, and she has an exhibition "
                 "twice a year. My father is a writer. He writes books for children.\n"
                 "My sister is an actor. She's in a play at the Municipal Theater. The play is about the moon and "
                 "the sun — it's beautiful!\n"
                 "And me? I'm not an artist. I'm a programmer. I work at home three days a week.\n"
                 "We live in Belo Horizonte, in a big old house. We have a dog and a parrot. The dog is quiet, "
                 "but the parrot sings all day. Maybe the parrot is the real singer in my family!\n"
                 "We have dinner together every night. It's the best part of my day."},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "What does Gabriel's mother do? → [She's a painter.]",
         "text": "1. What does his father do? → [*He's a writer.|He's an actor.|He's a programmer.]\n"
                 "2. How often does his mother have an exhibition? → [*Twice a year.|Twice a week.|Once a month.]\n"
                 "3. What is the play about? → [*The moon and the sun.|A big old house.|A parrot.]\n"
                 "4. Which pet sings all day? → [*The parrot.|The dog.|The cat.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Gabriel is a programmer. → True",
         "statements": [
             {"text": "Gabriel is an artist.", "answer": False, "translation": "O Gabriel é artista."},
             {"text": "The family lives in Belo Horizonte.", "answer": True, "translation": "A família mora em Belo Horizonte."},
             {"text": "For Gabriel, dinner is the best part of the day.", "answer": True,
              "translation": "Para o Gabriel, o jantar é a melhor parte do dia."},
         ]},
        {"type": "fill",
         "prompt": "Complete with a, an or the, according to the text.",
         "translation": "Complete com a, an ou the, de acordo com o texto.",
         "example": "My mother is [a] painter.",
         "text": "1. My sister is [an] actor.\n2. We have [a] dog and [a] parrot.\n3. [The] dog is quiet.\n"
                 "4. It's [the] best part of my day."},
    ],
}

AULA19_WRITING = {
    "title": "Writing — my family's jobs",
    "lesson": 19,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Profissão no singular com A / AN: She is a teacher. · He is an engineer.\n"
                   "THE na 2ª vez, para coisas únicas e com superlativo · sem artigo para refeições, cidades, países e "
                   "by + transporte.",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose a, an, the or — (no article).",
         "translation": "Escolha a, an, the ou — (sem artigo).",
         "example": "I go to work by [—] bus.",
         "text": "1. My uncle is [*an|a|the|—] engineer.\n2. I have [*—|a|the|an] breakfast at 7 a.m.\n"
                 "3. [*—|The|A] Brazil is a big country.\n4. Look at [*the|a|—] moon!\n"
                 "5. I study English three times [*a|the|—] week."},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Ele é médico. → He is a doctor.",
         "text": "1. Minha irmã é professora. → [My sister is a teacher.]\n"
                 "2. Ela é a prima da minha mãe. → [She is my mother's cousin.|She's my mother's cousin.]"},
        {"type": "free",
         "prompt": "Write about your family: What do they do? How often do they work or study? Do you have pets? "
                   "Use a, an and the.",
         "translation": "Escreva sobre a sua família: o que fazem, com que frequência trabalham ou estudam, se vocês têm "
                        "bichos de estimação. Use a, an e the.",
         "example": "My father is an engineer.",
         "model_answer": "My father is an engineer, and my mother is a teacher.\n"
                         "She teaches five days a week.\n"
                         "My brother is a programmer. He works at home.\n"
                         "We have a cat and a dog. The cat is lazy, but the dog is very happy.\n"
                         "We have dinner together on Sundays.",
         "keywords": ["is a", "is an", "The"], "min_words": 30, "points": 4},
    ],
}

AULA19_VIDEO = _video(19, AULA19_TOPIC, "Video — Meet my family",
                      "a Sarah apresenta a família: as profissões (com a / an), a frequência e os bichos (a cat… the cat).",
                      "aula19-video", [
    _q("What does Sarah's mother do?", "O que a mãe da Sarah faz?", "She's a teacher.", "She's teacher.",
       "She's an teacher.", "She's the teacher."),
    _q("How often does her brother sing in restaurants?", "Com que frequência o irmão dela canta em restaurantes?",
       "Three times a week.", "Three times the week.", "Three times week.", "Once a month."),
    _q("Complete: She works at ___ best hospital in the city.", "Complete: Ela trabalha no melhor hospital da cidade.",
       "the", "a", "an", "— (no article)"),
    _q("Which pet is very old?", "Qual bicho é bem velho?", "The cat.", "The dog.", "The puppy.", "The parrot."),
])

# ---------- Aula 20 — Adverbs of Manner (https://youtu.be/PPtyfyYRmTo) ----------

AULA20_TOPIC = "Aula 20 — Adverbs of Manner"

AULA20_PETS = {
    "title": "Animals and pets: vocabulary",
    "lesson": 20,
    "description": "ANIMALS: donkey (burro) · deer (cervo) · cat · chameleon (camaleão) · owl (coruja) · dog · "
                   "hedgehog (ouriço) · hamster · fish · alligator (jacaré) — \"See you later, alligator!\"\n"
                   "PET CARE (cuidar do pet): play (brincar) · clean up (limpar) · walk the dog (passear com o cachorro — "
                   "SEM \"with\": walk my dog) · pet (fazer carinho, passar a mão) · feed (alimentar) · train (treinar) · "
                   "groom (tosar, arrumar) · bathe (dar banho) · cuddle (aconchegar, fazer carinho)\n"
                   "Pronúncia: bathe (verbo, \"bêidh\") ≠ bath (banho, \"béth\") · cuddle = \"cârou\".\n"
                   "puppy = filhote de cachorro.",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the animals to Portuguese.",
         "translation": "Ligue os animais ao português.",
         "example": "owl → coruja",
         "pairs": [
             {"left": "donkey", "right": "burro"},
             {"left": "deer", "right": "cervo"},
             {"left": "chameleon", "right": "camaleão"},
             {"left": "hedgehog", "right": "ouriço"},
             {"left": "alligator", "right": "jacaré"},
             {"left": "puppy", "right": "filhote de cachorro"},
         ]},
        {"type": "match",
         "prompt": "Match the pet care verbs to Portuguese.",
         "translation": "Ligue os verbos de cuidados com o pet ao português.",
         "example": "feed → alimentar",
         "pairs": [
             {"left": "walk the dog", "right": "passear com o cachorro"},
             {"left": "groom", "right": "tosar, arrumar"},
             {"left": "bathe", "right": "dar banho"},
             {"left": "train", "right": "treinar"},
             {"left": "cuddle", "right": "aconchegar"},
             {"left": "clean up", "right": "limpar"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta.",
         "example": "Every morning, I [feed] my cat.",
         "text": "1. I [*walk my dog|walk with my dog] in the park every day.\n"
                 "2. I [*bathe|bath] my dog on Saturdays.\n"
                 "3. My cat loves it when I [*pet|feed] her head.\n"
                 "4. Every morning, I [*feed|groom] my fish. They're always hungry!"},
    ],
}

AULA20_ADVERBS = {
    "title": "Adverbs of manner: quickly, happily, well",
    "lesson": 20,
    "description": "ADVERBS OF MANNER (advérbios de modo) dizem COMO uma ação acontece — em português, muitos terminam em "
                   "\"-mente\": rapidamente, alegremente.\n"
                   "Regra geral: adjetivo + LY → quick → quickly · brave → bravely · slow → slowly · beautiful → beautifully\n"
                   "Termina em Y: tira o Y + ILY → happy → happily · easy → easily\n"
                   "Consoante + LE: tira o E + Y → gentle → gently · comfortable → comfortably\n"
                   "IRREGULARES: good → WELL · fast → FAST · hard → HARD (study hard, work hard)\n"
                   "Adjetivo descreve o SUBSTANTIVO: She has a beautiful voice.\n"
                   "Advérbio descreve o VERBO: She sings beautifully. (✗ She sings beautiful)\n"
                   "Cuidado: FRIENDLY (amigável) termina em LY, mas é ADJETIVO: friendly pets.",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the adverb.",
         "translation": "Escreva o advérbio de modo.",
         "example": "quick → quickly",
         "text": "1. slow → [slowly]\n2. brave → [bravely]\n3. happy → [happily]\n4. easy → [easily]\n"
                 "5. gentle → [gently]\n6. comfortable → [comfortably]\n7. good → [well]\n8. fast → [fast]"},
        {"type": "dropdown",
         "prompt": "Adjective or adverb? Choose.",
         "translation": "Adjetivo ou advérbio? Escolha (adjetivo → substantivo · advérbio → verbo).",
         "example": "She has a [beautiful] voice. · She sings [beautifully].",
         "text": "1. She sings [*beautifully|beautiful].\n2. She has a [*beautiful|beautifully] voice.\n"
                 "3. He drives very [*carefully|careful].\n4. He plays the guitar [*well|good].\n"
                 "5. My dog runs [*fast|fastly].\n6. We have [*friendly|friendlily] pets."},
        {"type": "dropdown",
         "prompt": "Is this sentence correct?",
         "translation": "Esta frase está correta? (exercício da aula)",
         "example": "He drives very carefully. → [Correct]",
         "text": "1. She sings beautiful. → [*Incorrect|Correct]\n2. They speak English fluently. → [*Correct|Incorrect]\n"
                 "3. He plays the guitar good. → [*Incorrect|Correct]\n4. Study hard! → [*Correct|Incorrect]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "Quickly is an adverb. → True",
         "statements": [
             {"text": "\"Friendly\" is an adverb.", "answer": False, "translation": "\"Friendly\" é um advérbio."},
             {"text": "The adverb of \"good\" is \"well\".", "answer": True, "translation": "O advérbio de \"good\" é \"well\"."},
             {"text": "We say \"fastly\".", "answer": False, "translation": "Dizemos \"fastly\"."},
             {"text": "Adverbs of manner say how we do an action.", "answer": True,
              "translation": "Os advérbios de modo dizem como fazemos uma ação."},
         ]},
    ],
}

AULA20_LISTENING = {
    "title": "Listening — at the pet shop",
    "lesson": 20,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: o -LY no final é curtinho (\"li\"): quickly = \"KUÍK-li\". Preste atenção no final das palavras!",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the word you hear.",
         "translation": "Ouça e escolha a palavra que você ouve.",
         "example": "Você ouve: \"quickly\" → quickly",
         "audio": f"{AUDIO}/aula20-words.m4a",
         "text": "1. [*happily|happy]\n2. [*bathe|bath]\n3. [*gently|gentle]\n4. [*well|good]\n5. [*owl|all]\n6. [*slowly|slow]"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"My puppy eats very well.\" → My puppy eats very [well].",
         "audio": f"{AUDIO}/aula20-dictation.m4a",
         "text": "1. It runs and plays [happily].\n2. I [gently] groom my puppy.\n3. It learns [quickly].\n"
                 "4. She speaks English [fluently]."},
        {"type": "info",
         "prompt": "Now listen: Leo talks to a woman at the pet shop.",
         "translation": "Agora ouça: o Leo conversa com a atendente de um pet shop sobre o filhote dele. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula20-petshop.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Leo has a new [puppy].",
         "text": "1. What's the puppy's name? → [*Toby.|Max.|Bob.]\n"
                 "2. How does Toby eat? → [*Very quickly.|Very slowly.|Very badly.]\n"
                 "3. What does Leo want today? → [*A bath for Toby.|A new dog.|Some cat food.]\n"
                 "4. When can Leo pick Toby up? → [*At 4 p.m.|At 2 p.m.|Tomorrow.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Toby is a puppy. → True",
         "statements": [
             {"text": "Toby doesn't like water.", "answer": True, "translation": "O Toby não gosta de água."},
             {"text": "The woman bathes the dogs quickly and roughly.", "answer": False,
              "translation": "A moça dá banho nos cachorros rápido e de forma bruta."},
             {"text": "Toby learns quickly.", "answer": True, "translation": "O Toby aprende rápido."},
         ]},
    ],
}

AULA20_SPEAKING = {
    "title": "Speaking — pets and adverbs",
    "lesson": 20,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: owl = \"áuol\" · bathe = \"bêidh\" · cuddle = \"cârou\".",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the vocabulary.",
         "translation": "Ouça e repita o vocabulário da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula20-say-w{i}.m4a"} for i, t in enumerate(
             ["donkey, deer, cat, chameleon", "owl, dog, hedgehog", "hamster, fish, alligator",
              "play, clean up, walk, pet", "feed, train, groom", "bathe, cuddle"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "\"She sings beautifully.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula20-say-s{i}.m4a"} for i, t in enumerate(
             ["My puppy eats very well.", "It runs and plays happily.", "I gently groom my puppy.",
              "It learns quickly.", "She sings beautifully.", "He drives very carefully."], 1)]},
        {"type": "speak",
         "prompt": "Now answer about YOU.",
         "translation": "Agora responda sobre VOCÊ, com advérbios.",
         "example": "\"How do you drive?\" → \"I drive carefully.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula20-say-y{i}.m4a"} for i, t in enumerate(
             ["Do you have a pet?", "How do you speak English?", "How do you drive?", "Who sings well in your family?"], 1)]},
    ],
}

AULA20_READING = {
    "title": "Reading — my new puppy",
    "lesson": 20,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto do exercício da aula e responda às perguntas de acordo com o texto.",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto sobre um filhote novo (o texto do exercício 2 da aula). "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula20-reading.m4a",
         "text": "MY NEW PUPPY\n\n"
                 "I have a new puppy. Every morning, I feed it. My puppy eats very well.\n"
                 "Then, I walk my puppy in the park. It runs and plays happily. It runs fast to catch the ball.\n"
                 "In the afternoon, I gently groom my puppy. It likes being brushed.\n"
                 "I also train my puppy with simple commands. It learns quickly.\n"
                 "Taking care of a puppy is fun and rewarding."},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "When do I feed my puppy? → [Every morning.]",
         "text": "1. How does the puppy eat? → [*Very well.|Very slowly.|Very badly.]\n"
                 "2. Where does the puppy play? → [*In the park.|At home.|At the pet shop.]\n"
                 "3. When do I groom the puppy? → [*In the afternoon.|In the morning.|At night.]\n"
                 "4. How does the puppy learn? → [*Quickly.|Slowly.|Badly.]"},
        {"type": "fill",
         "prompt": "Complete with the adverbs from the text.",
         "translation": "Complete com os advérbios do texto (exercício da aula).",
         "example": "My puppy eats very [well].",
         "text": "1. It runs and plays [happily].\n2. It runs [fast] to catch the ball.\n3. I [gently] groom my puppy.\n"
                 "4. It learns [quickly]."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "The puppy is new. → True",
         "statements": [
             {"text": "The puppy doesn't like being brushed.", "answer": False,
              "translation": "O filhote não gosta de ser escovado."},
             {"text": "Taking care of a puppy is fun.", "answer": True, "translation": "Cuidar de um filhote é divertido."},
         ]},
    ],
}

AULA20_WRITING = {
    "title": "Writing — how do they do it?",
    "lesson": 20,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ verbo + advérbio: She sings beautifully. · It learns quickly. · He plays well.\n"
                   "Irregulares: good → well · fast → fast · hard → hard.",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza (frases da revisão da aula).",
         "example": "Ele dirige muito cuidadosamente. → He drives very carefully.",
         "text": "1. Eles falam inglês fluentemente. → [They speak English fluently.]\n"
                 "2. Ela terminou o dever de casa rapidamente. → [She quickly finished her homework.|"
                 "She finished her homework quickly.]\n"
                 "3. Ele toca violão bem. → [He plays the guitar well.|He plays guitar well.]"},
        {"type": "fill",
         "prompt": "Complete with the adverb of the word in parentheses.",
         "translation": "Complete com o advérbio da palavra entre parênteses.",
         "example": "My cat sleeps [comfortably] on the sofa. (comfortable)",
         "text": "1. The chameleon moves [slowly]. (slow)\n2. My grandmother cooks very [well]. (good)\n"
                 "3. The children play [happily] in the park. (happy)\n4. You work [hard]! (hard)"},
        {"type": "free",
         "prompt": "Write about a pet (yours, a friend's or your dream pet). How does it eat, run, play, sleep and learn? "
                   "What do you do to take care of it?",
         "translation": "Escreva sobre um bicho de estimação (o seu, de um amigo ou o dos seus sonhos). Como ele come, "
                        "corre, brinca, dorme e aprende? O que você faz para cuidar dele?",
         "example": "My cat sleeps comfortably on my bed.",
         "model_answer": "I have a cat. Her name is Luna.\n"
                         "Luna eats very well, and she sleeps comfortably on my bed.\n"
                         "She doesn't run fast, but she plays happily with her ball.\n"
                         "Every morning, I feed her, and on Sundays I gently groom her.\n"
                         "She learns quickly!",
         "keywords": ["well", "happily", "quickly"], "min_words": 30, "points": 4},
    ],
}

AULA20_VIDEO = _video(20, AULA20_TOPIC, "Video — Max, my new puppy",
                      "a Sarah mostra como é o dia do Max, o filhote dela: como ele come, corre, brinca e aprende.",
                      "aula20-video", [
    _q("How does Max eat?", "Como o Max come?", "Very well.", "Very good.", "Very slowly.", "Very badly."),
    _q("How does Max run?", "Como o Max corre?", "Fast.", "Fastly.", "Slowly.", "Badly."),
    _q("How does Sarah pet Max?", "Como a Sarah faz carinho no Max?", "Gently.", "Gentle.", "Quickly.", "Badly."),
    _q("How does Max learn?", "Como o Max aprende?", "Quickly.", "Quick.", "Slowly.", "Hardly."),
    _q("How does the chameleon move?", "Como o camaleão se move?", "Very slowly.", "Very slow.", "Very fast.",
       "Very happily."),
])


SPECS = (AULA1_FORMS, AULA1_QUESTIONS, AULA1_LISTENING, AULA1_SPEAKING, AULA1_READING, AULA1_WRITING, AULA1_VIDEO,
         AULA2_WASWERE, AULA2_THEREWAS, AULA2_LISTENING, AULA2_SPEAKING, AULA2_READING, AULA2_WRITING, AULA2_VIDEO,
         AULA3_PREPS, AULA3_WHERE, AULA3_LISTENING, AULA3_SPEAKING, AULA3_READING, AULA3_WRITING, AULA3_VIDEO,
         AULA4_REGULAR, AULA4_IRREGULAR, AULA4_LISTENING, AULA4_SPEAKING, AULA4_READING, AULA4_WRITING, AULA4_VIDEO,
         AULA5_SOUNDS, AULA5_VOICED, AULA5_LISTENING, AULA5_SPEAKING, AULA5_READING, AULA5_WRITING, AULA5_VIDEO,
         AULA6_DIDNT, AULA6_SENTENCES, AULA6_LISTENING, AULA6_SPEAKING, AULA6_READING, AULA6_WRITING, AULA6_VIDEO,
         AULA7_DID, AULA7_WH, AULA7_LISTENING, AULA7_SPEAKING, AULA7_READING, AULA7_WRITING, AULA7_VIDEO,
         AULA8_FORMS, AULA8_QUESTIONS, AULA8_LISTENING, AULA8_SPEAKING, AULA8_READING, AULA8_WRITING, AULA8_VIDEO,
         AULA9_VOCAB, AULA9_WHEN, AULA9_LISTENING, AULA9_SPEAKING, AULA9_READING, AULA9_WRITING, AULA9_VIDEO,
         AULA10_TIME, AULA10_PLACE, AULA10_LISTENING, AULA10_SPEAKING, AULA10_READING, AULA10_WRITING, AULA10_VIDEO,
         AULA11_ORDINALS, AULA11_DATES, AULA11_LISTENING, AULA11_SPEAKING, AULA11_READING, AULA11_WRITING, AULA11_VIDEO,
         AULA12_MEALS, AULA12_LIKES, AULA12_LISTENING, AULA12_SPEAKING, AULA12_READING, AULA12_WRITING, AULA12_VIDEO,
         AULA13_VOCAB, AULA13_COUNT, AULA13_LISTENING, AULA13_SPEAKING, AULA13_READING, AULA13_WRITING, AULA13_VIDEO,
         AULA14_QUANT, AULA14_THERE, AULA14_LISTENING, AULA14_SPEAKING, AULA14_READING, AULA14_WRITING, AULA14_VIDEO,
         AULA15_CONTAINERS, AULA15_QUANT, AULA15_LISTENING, AULA15_SPEAKING, AULA15_READING, AULA15_WRITING, AULA15_VIDEO,
         AULA16_NUMBERS, AULA16_COMPARATIVES, AULA16_LISTENING, AULA16_SPEAKING, AULA16_READING, AULA16_WRITING, AULA16_VIDEO,
         AULA17_PLACES, AULA17_SUPERLATIVES, AULA17_LISTENING, AULA17_SPEAKING, AULA17_READING, AULA17_WRITING, AULA17_VIDEO,
         AULA18_VOCAB, AULA18_ASKING, AULA18_LISTENING, AULA18_SPEAKING, AULA18_READING, AULA18_WRITING, AULA18_VIDEO,
         AULA19_JOBS, AULA19_ARTICLES, AULA19_LISTENING, AULA19_SPEAKING, AULA19_READING, AULA19_WRITING, AULA19_VIDEO,
         AULA20_PETS, AULA20_ADVERBS, AULA20_LISTENING, AULA20_SPEAKING, AULA20_READING, AULA20_WRITING, AULA20_VIDEO)


def main():
    publish(SLUG, "A2", SPECS)


if __name__ == "__main__":
    main()
