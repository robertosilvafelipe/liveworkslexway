"""Básico 3 public course page (/curso/basico-3): 6 activities per lesson + an interactive video extra.

Run on the server: python -m app.seed_basico_3  (creates or updates; ids and past attempts are kept).
Audios: app/static/audio/basico-3 (deploy/make_audio.py, scripts named b3-…); videos: app/static/video/basico-3.
Voices (same as Básico 2): Sarah (female) and Jerry B. (male).
"""
import json
import os

from .public_seed import publish

SLUG = "basico-3"
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


# ---------- Aula 01 — Past Simple: regular & irregular (https://youtu.be/Ri6rnMFqH9w) ----------

AULA1_TOPIC = "Aula 01 — Past Simple (regular & irregular)"

AULA1_REGULAR = {
    "title": "Regular verbs: the -ED spelling rules",
    "lesson": 1,
    "description": "VERBOS REGULARES no passado terminam em -ED. Regras de escrita:\n"
                   "1. Maioria: + ED → watch → watched · cook → cooked · start → started\n"
                   "2. Termina em E: só + D → dance → danced · explore → explored · live → lived\n"
                   "3. Curto (1 sílaba) com consoante-vogal-consoante: DOBRA + ED → stop → stopped · plan → planned\n"
                   "4. Consoante + Y: tira o Y + IED → study → studied · cry → cried\n"
                   "   Mas VOGAL + Y: só + ED → enjoy → enjoyed · play → played · stay → stayed\n"
                   "O verbo no passado é IGUAL para todos: I watched, you watched, she watched… por isso o SUJEITO é "
                   "obrigatório em inglês!",
    "topic": AULA1_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "How do we write the past? Put each verb in the right group.",
         "translation": "Como escrevemos o passado? Coloque cada verbo no grupo da regra certa.",
         "example": "watch → + ed · dance → + d",
         "categories": ["+ ed", "+ d", "double + ed", "y → ied"],
         "words": [
             {"text": "visit", "category": "+ ed"}, {"text": "finish", "category": "+ ed"},
             {"text": "enjoy", "category": "+ ed"}, {"text": "play", "category": "+ ed"},
             {"text": "explore", "category": "+ d"}, {"text": "live", "category": "+ d"},
             {"text": "love", "category": "+ d"},
             {"text": "stop", "category": "double + ed"}, {"text": "plan", "category": "double + ed"},
             {"text": "chat", "category": "double + ed"},
             {"text": "study", "category": "y → ied"}, {"text": "cry", "category": "y → ied"},
             {"text": "try", "category": "y → ied"},
         ]},
        {"type": "fill",
         "prompt": "Write the past of the verbs.",
         "translation": "Escreva o passado dos verbos.",
         "example": "walk → walked",
         "text": "1. visit → [visited]\n2. explore → [explored]\n3. plan → [planned]\n4. cry → [cried]\n"
                 "5. stay → [stayed]\n6. like → [liked]\n7. chat → [chatted]\n8. carry → [carried]"},
        {"type": "match",
         "prompt": "Match the time expressions to Portuguese.",
         "translation": "Ligue as expressões de tempo ao português.",
         "example": "yesterday → ontem",
         "pairs": [
             {"left": "a week ago", "right": "há uma semana"},
             {"left": "a month ago", "right": "há um mês"},
             {"left": "last month", "right": "no mês passado"},
             {"left": "when I was a kid", "right": "quando eu era criança"},
             {"left": "before class", "right": "antes da aula"},
             {"left": "a long time ago", "right": "há muito tempo"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta (verbos regulares).",
         "example": "We [enjoyed] the trip last weekend.",
         "text": "1. I [*explored|exploreed|explore] the city center yesterday.\n"
                 "2. She [*studied|studyed|studies] a lot last night.\n"
                 "3. We [*enjoyed|enjoied|enjoy] the trip last weekend.\n"
                 "4. The bus [*stopped|stoped|stops] in front of my house a week ago.\n"
                 "5. They [*lived|liveed|live] in Recife when I was a kid."},
    ],
}

AULA1_IRREGULAR = {
    "title": "Irregular verbs: went, ate, saw, met…",
    "lesson": 1,
    "description": "VERBOS IRREGULARES não terminam em -ED: mudam de forma e precisamos MEMORIZAR (anote, cole post-its pela casa!).\n"
                   "do → did · go → went · see → saw · eat → ate · have → had · wake up → woke up · buy → bought (\"bót\") · "
                   "read → read (escrita igual, pronúncia \"réd\") · meet → met · wear → wore\n"
                   "Estrutura: SUJEITO + VERBO NO PASSADO (+ complemento + expressão de tempo)\n"
                   "I saw beautiful places on my trip to Italy last month. · I met amazing people on my last trip.\n"
                   "Refeições: have lunch → I had lunch with my family on Sunday. (\"comer\" também pode ser have: I had pizza.)",
    "topic": AULA1_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the verbs to their past forms.",
         "translation": "Ligue os verbos às formas do passado.",
         "example": "go → went",
         "pairs": [
             {"left": "do", "right": "did"},
             {"left": "see", "right": "saw"},
             {"left": "eat", "right": "ate"},
             {"left": "buy", "right": "bought"},
             {"left": "meet", "right": "met"},
             {"left": "wear", "right": "wore"},
             {"left": "wake up", "right": "woke up"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the right past form.",
         "translation": "Escolha a forma certa do passado.",
         "example": "I [saw] beautiful places on my trip.",
         "text": "1. I [*met|meeted|meet] amazing people on my last trip.\n"
                 "2. My sister [*wore|weared|wear] a black dress on Saturday.\n"
                 "3. My friends [*bought|buyed|boughted] a new house.\n"
                 "4. We [*had|haved|has] lunch with my family on Sunday.\n"
                 "5. He [*read|readed|reads] a book last night."},
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras em ordem. (Eu vi lugares lindos na minha viagem para a Itália.)",
         "example": "went / I / the park / to / last Sunday → I went to the park last Sunday.",
         "tokens": ["I", "saw", "beautiful", "places", "on", "my", "trip", "to", "Italy."], "alternatives": []},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Went\" is the past of \"go\". → True",
         "statements": [
             {"text": "In the past, the verb changes for each person: I went, she wents.", "answer": False,
              "translation": "No passado, o verbo muda para cada pessoa: I went, she wents."},
             {"text": "In English, we always need the subject: \"I went\", not only \"went\".", "answer": True,
              "translation": "Em inglês sempre precisamos do sujeito: \"I went\", não só \"went\"."},
             {"text": "The past of \"read\" has the same spelling but a different sound.", "answer": True,
              "translation": "O passado de \"read\" tem a mesma escrita, mas outro som."},
             {"text": "We pronounce the GH in \"bought\".", "answer": False,
              "translation": "Pronunciamos o GH em \"bought\"."},
         ]},
    ],
}

AULA1_LISTENING = {
    "title": "Listening — Monday morning at the office",
    "lesson": 1,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: o -ED é curtinho (\"wɑtʃt\", \"plεɪd\"). Preste atenção no final dos verbos para saber se é passado.",
    "topic": AULA1_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the verb you hear.",
         "translation": "Ouça e escolha o verbo que você ouve.",
         "example": "Você ouve: \"I watched a movie.\" → watched",
         "audio": f"{AUDIO}/aula1-verbs.m4a",
         "text": "1. I [*visited|visit] my grandma.\n2. She [*bought|brought] a new phone.\n3. We [*met|meet] at the mall.\n"
                 "4. They [*played|play] soccer.\n5. He [*wore|were] a blue jacket.\n6. I [*stayed|stay] at home."},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"I went to the gym last night.\" → I [went] to the gym last night.",
         "audio": f"{AUDIO}/aula1-dictation.m4a",
         "text": "1. They [watched] a movie yesterday.\n2. I [ate] pizza last Sunday.\n"
                 "3. My friends [bought] a new house.\n4. We [studied] English a week ago."},
        {"type": "info",
         "prompt": "Now listen: Ana and Leo talk about their weekend.",
         "translation": "Agora ouça: a Ana e o Leo chegam ao escritório na segunda-feira e contam o que fizeram no fim de "
                        "semana. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula1-office.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "It's [Monday] morning.",
         "text": "1. On Saturday, Ana went [*to the beach.|to the mall.|to her mother's house.]\n"
                 "2. At the restaurant, Ana ate [*fish and rice.|pizza.|hamburgers.]\n"
                 "3. On Saturday, Leo [*painted his bedroom.|played soccer.|visited his parents.]\n"
                 "4. On Sunday, Leo met [*an old friend from school.|his sister.|Ana.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Ana and Leo work together. → True",
         "statements": [
             {"text": "The weather was bad on Saturday.", "answer": False, "translation": "O tempo estava ruim no sábado."},
             {"text": "Leo was tired on Sunday.", "answer": True, "translation": "O Leo estava cansado no domingo."},
             {"text": "Leo and his friend watched a movie.", "answer": True,
              "translation": "O Leo e o amigo assistiram a um filme."},
         ]},
    ],
}

AULA1_SPEAKING = {
    "title": "Speaking — what I did",
    "lesson": 1,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: bought = \"bót\" · read (passado) = \"réd\" · watched = \"wótʃt\" (o E não é pronunciado).",
    "topic": AULA1_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the verbs.",
         "translation": "Ouça e repita os verbos (presente → passado).",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula1-say-v{i}.m4a"} for i, t in enumerate(
             ["cook, cooked", "watch, watched", "start, started", "finish, finished", "do, did", "go, went",
              "see, saw", "eat, ate", "buy, bought", "read, read", "meet, met", "wear, wore"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "\"I explored the city center yesterday.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula1-say-s{i}.m4a"} for i, t in enumerate(
             ["I explored the city center yesterday.", "We enjoyed the trip last weekend.", "She studied a lot last night.",
              "I saw beautiful places on my trip to Italy last month.", "I met amazing people on my last trip.",
              "I had lunch with my family on Sunday."], 1)]},
        {"type": "speak",
         "prompt": "Now talk about YOU: say three things you did last weekend.",
         "translation": "Agora fale sobre VOCÊ: diga três coisas que você fez no fim de semana passado.",
         "example": "\"I went to the supermarket on Saturday, I watched TV and I had lunch with my family.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula1-say-y{i}.m4a"} for i, t in enumerate(
             ["Tell me three things you did last weekend.", "Tell me what you did yesterday morning.",
              "Tell me about something you did when you were a kid."], 1)]},
    ],
}

AULA1_READING = {
    "title": "Reading — when my grandma was a kid",
    "lesson": 1,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA1_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto da Laura sobre a infância da avó dela. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula1-reading.m4a",
         "text": "WHEN MY GRANDMA WAS A KID\n\n"
                 "A long time ago, in 1955, my grandma Rosa lived on a small farm in Minas Gerais.\n"
                 "Every morning, she woke up at five o'clock. She helped her mother in the kitchen and carried water "
                 "from the river.\n"
                 "She walked to school with her brothers. The school was very far, and they arrived tired!\n"
                 "There was no TV, so in the evenings the family played cards and listened to the radio.\n"
                 "When she was eighteen, she moved to Belo Horizonte. There, she met my grandpa at a party. "
                 "They danced all night!\n"
                 "Last week, she showed me some old photos and told me these stories. I loved them!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Rosa lived [on a farm].",
         "text": "1. Rosa woke up [*at five o'clock.|at seven o'clock.|at noon.]\n"
                 "2. She went to school [*on foot, with her brothers.|by bus.|by car.]\n"
                 "3. In the evenings, the family [*played cards and listened to the radio.|"
                 "watched TV.|went to parties.]\n"
                 "4. She met the grandpa [*at a party.|at school.|on the farm.]"},
        {"type": "fill",
         "prompt": "Find the past of these verbs in the text.",
         "translation": "Encontre no texto o passado destes verbos.",
         "example": "live → [lived]",
         "text": "1. carry → [carried]\n2. arrive → [arrived]\n3. meet → [met]\n4. tell → [told]\n5. show → [showed]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Rosa lived on a farm. → True",
         "statements": [
             {"text": "The school was near the farm.", "answer": False, "translation": "A escola era perto da fazenda."},
             {"text": "Rosa moved to Belo Horizonte when she was eighteen.", "answer": True,
              "translation": "A Rosa se mudou para Belo Horizonte aos dezoito anos."},
         ]},
    ],
}

AULA1_WRITING = {
    "title": "Writing — yesterday",
    "lesson": 1,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ SUJEITO + VERBO NO PASSADO (+ expressão de tempo).\n"
                   "Regulares: + ed / + d / dobra + ed / y → ied · Irregulares: went, ate, had, saw, bought, met, woke up…",
    "topic": AULA1_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate (from the lesson).",
         "translation": "Traduza (exercício de tradução da aula).",
         "example": "Eu fui à academia ontem à noite. → I went to the gym last night.",
         "text": "1. Eles assistiram a um filme ontem. → [They watched a movie yesterday.]\n"
                 "2. Meus amigos compraram uma casa nova. → [My friends bought a new house.]\n"
                 "3. Minha irmã usou um vestido preto no sábado. → [My sister wore a black dress on Saturday.]"},
        {"type": "fill",
         "prompt": "Complete with the past of the verb.",
         "translation": "Complete com o passado do verbo entre parênteses.",
         "example": "I [woke] up at 7 a.m. (wake)",
         "text": "1. We [planned] a trip to Bahia. (plan)\n2. She [cried] at the end of the movie. (cry)\n"
                 "3. I [saw] my teacher at the supermarket. (see)\n4. They [played] video games all night. (play)"},
        {"type": "free",
         "prompt": "Write about yesterday: the time you woke up, the things you ate, the places you went to and "
                   "the things you did in the evening. Use regular and irregular verbs.",
         "translation": "Escreva sobre o seu dia de ontem: a que horas acordou, o que comeu, aonde foi, o que fez à noite. "
                        "Use verbos regulares e irregulares.",
         "example": "Yesterday, I woke up at 6:30.",
         "model_answer": "Yesterday, I woke up at 6:30 and had coffee with my husband.\n"
                         "I went to work by bus and finished work at 5 p.m.\n"
                         "In the evening, I cooked pasta, watched a series and studied English.\n"
                         "I went to bed at 11 p.m.",
         "keywords": ["woke up", "went", "watched", "had"], "min_words": 30, "points": 4},
    ],
}

AULA1_VIDEO = _video(1, AULA1_TOPIC, "Video — My Saturday",
                     "o Daniel conta o que fez no sábado: acordou tarde, surfou, almoçou, leu e encontrou os amigos.",
                     "aula1-video", [
    _q("Complete: Daniel ___ up at ten o'clock.", "Complete: o Daniel ___ às dez horas.", "woke", "waked", "wake", "wakes"),
    _q("Complete: Then Daniel ___ to the beach.", "Complete: depois o Daniel ___ à praia.", "went", "goed", "go",
       "gone"),
    _q("Complete: Daniel ___ paella for lunch.", "Complete: o Daniel ___ paella no almoço.", "ate", "eated", "eat", "had eat"),
    _q("How do we say \"read\" in the past?", "Como falamos \"read\" no passado?", "\"red\" — same spelling, new sound",
       "\"readed\"", "\"reed\" — the same sound", "\"rode\""),
])

# ---------- Aula 02 — -ED Pronunciation (https://youtu.be/JpdXmuXL_QY) ----------

AULA2_TOPIC = "Aula 02 — -ED Pronunciation"

AULA2_SOUNDS = {
    "title": "-ED: /ɪd/, /t/ or /d/?",
    "lesson": 2,
    "description": "O -ED tem TRÊS sons possíveis — e quase nunca é lido \"éd\"!\n"
                   "/ɪd/ (nova sílaba) → só quando o verbo termina em T ou D: want → wanted · visit → visited · "
                   "need → needed · end → ended · decide → decided · educate → educated · divide → divided\n"
                   "/t/ (estalinho sem vibração) → depois de sons que NÃO vibram (voiceless): watch → watched · cook → cooked · "
                   "laugh → laughed · kiss → kissed · help → helped · dance → danced\n"
                   "/d/ (som que vibra) → depois de sons que vibram (voiced) e de vogais: play → played · call → called · "
                   "love → loved · clean → cleaned · use → used · travel → traveled · listen → listened\n"
                   "Erro comum: \"cook-ed\", \"travel-ed\" → não crie uma sílaba nova! Diga \"cookt\", \"travld\".",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "Which sound? Put each verb in the right group.",
         "translation": "Qual é o som do -ED? Coloque cada verbo no grupo certo.",
         "example": "wanted → /ɪd/ · cooked → /t/ · played → /d/",
         "categories": ["/ɪd/", "/t/", "/d/"],
         "words": [
             {"text": "needed", "category": "/ɪd/"}, {"text": "decided", "category": "/ɪd/"},
             {"text": "educated", "category": "/ɪd/"}, {"text": "divided", "category": "/ɪd/"},
             {"text": "laughed", "category": "/t/"}, {"text": "kissed", "category": "/t/"},
             {"text": "helped", "category": "/t/"}, {"text": "danced", "category": "/t/"},
             {"text": "loved", "category": "/d/"}, {"text": "used", "category": "/d/"},
             {"text": "traveled", "category": "/d/"}, {"text": "called", "category": "/d/"},
         ]},
        {"type": "dropdown",
         "prompt": "How many syllables?",
         "translation": "Quantas sílabas tem o verbo no passado? (o -ED só cria sílaba nova depois de T ou D)",
         "example": "wanted → [2] (wan-ted) · cooked → [1]",
         "text": "1. watched → [*1|2]\n2. started → [*2|1]\n3. traveled → [*2|3]\n4. kissed → [*1|2]\n"
                 "5. ended → [*2|1]\n6. cleaned → [*1|2]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "Vowel sounds always vibrate. → True",
         "statements": [
             {"text": "We always read -ED as \"ed\", like in Portuguese.", "answer": False,
              "translation": "Sempre lemos o -ED como \"éd\", como em português."},
             {"text": "The /ɪd/ sound comes after verbs ending in T or D.", "answer": True,
              "translation": "O som /ɪd/ vem depois de verbos terminados em T ou D."},
             {"text": "The S sound vibrates, and the Z sound doesn't vibrate.", "answer": False,
              "translation": "O som de S vibra e o som de Z não vibra."},
             {"text": "All vowel sounds vibrate our vocal cords.", "answer": True,
              "translation": "Todos os sons de vogais vibram as nossas cordas vocais."},
         ]},
    ],
}

AULA2_VOICED = {
    "title": "Voiced or voiceless?",
    "lesson": 2,
    "description": "VOICED (vozeado) = o som VIBRA as cordas vocais. Ponha a mão na garganta e diga \"zzzz\": vibra!\n"
                   "VOICELESS (desvozeado) = o ar passa e NÃO vibra: diga \"ssss\" — a boca fica igual, mas não vibra.\n"
                   "Pares: /z/ vibra × /s/ não vibra · /d/ vibra × /t/ não vibra · /v/ vibra × /f/ não vibra\n"
                   "Regra: se o ÚLTIMO SOM do verbo não vibra, o -ED também não vibra → /t/. "
                   "Se vibra, o -ED vibra → /d/.\n"
                   "Atenção ao SOM, não à letra: laugh termina com som de F (não vibra) → laughed /t/ · "
                   "dance termina com som de S → danced /t/ · use termina com som de Z → used /d/.",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Voiced or voiceless? Look at the last SOUND of the verb.",
         "translation": "O último SOM do verbo vibra (voiced) ou não vibra (voiceless)?",
         "example": "kiss (som de S) → [voiceless]",
         "text": "1. laugh (som de F) → [*voiceless|voiced]\n2. love (som de V) → [*voiced|voiceless]\n"
                 "3. help (som de P) → [*voiceless|voiced]\n4. clean (som de N) → [*voiced|voiceless]\n"
                 "5. play (som de vogal) → [*voiced|voiceless]\n6. dance (som de S) → [*voiceless|voiced]"},
        {"type": "dropdown",
         "prompt": "Choose the sound of -ED.",
         "translation": "Escolha o som do -ED.",
         "example": "helped → [/t/]",
         "text": "1. claimed → [*/d/|/t/|/ɪd/]\n2. collected → [*/ɪd/|/t/|/d/]\n3. laughed → [*/t/|/d/|/ɪd/]\n"
                 "4. traveled → [*/d/|/ɪd/|/t/]\n5. needed → [*/ɪd/|/d/|/t/]\n6. kissed → [*/t/|/ɪd/|/d/]"},
        {"type": "match",
         "prompt": "Match the verbs to how they sound.",
         "translation": "Ligue cada verbo ao jeito como ele soa.",
         "example": "cooked → \"cookt\"",
         "pairs": [
             {"left": "watched", "right": "\"wótʃt\" (1 sílaba)"},
             {"left": "traveled", "right": "\"TRÉ-vəld\" (2 sílabas)"},
             {"left": "decided", "right": "\"di-SAI-did\" (3 sílabas)"},
             {"left": "used", "right": "\"iuzd\" (1 sílaba)"},
             {"left": "danced", "right": "\"dænst\" (1 sílaba)"},
         ]},
    ],
}

AULA2_LISTENING = {
    "title": "Listening — hear the -ED",
    "lesson": 2,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: o -ED é só um \"estalinho\" no final. Se você esperar ouvir \"éd\", vai se perder!",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the sound of -ED.",
         "translation": "Ouça e escolha o som do -ED.",
         "example": "Você ouve: \"wanted\" → /ɪd/",
         "audio": f"{AUDIO}/aula2-sounds.m4a",
         "text": "1. laughed → [*/t/|/d/|/ɪd/]\n2. decided → [*/ɪd/|/t/|/d/]\n3. used → [*/d/|/t/|/ɪd/]\n"
                 "4. helped → [*/t/|/d/|/ɪd/]\n5. educated → [*/ɪd/|/d/|/t/]\n6. loved → [*/d/|/ɪd/|/t/]"},
        {"type": "dropdown",
         "prompt": "Present or past? Listen carefully to the end of the verb.",
         "translation": "Presente ou passado? Ouça com atenção o final do verbo.",
         "example": "Você ouve: \"We cooked pasta.\" → cooked",
         "audio": f"{AUDIO}/aula2-tense.m4a",
         "text": "1. They [*traveled|travel] a lot.\n2. I [*help|helped] my mom.\n3. We [*kissed|kiss] the baby.\n"
                 "4. You [*use|used] my computer.\n5. She [*laughed|laughs] a lot."},
        {"type": "info",
         "prompt": "Now listen: Bruna talks about her trip to Portugal.",
         "translation": "Agora ouça: a Bruna conta sobre a viagem dela para Portugal. Preste atenção nos verbos no passado. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula2-portugal.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "fill",
         "prompt": "Listen again and complete with the verbs in the past.",
         "translation": "Ouça de novo e complete com os verbos no passado.",
         "example": "Last year, I [traveled] to Portugal.",
         "text": "1. My husband and I [decided] to visit Lisbon.\n2. We [walked] a lot every day.\n"
                 "3. I [loved] the old trams.\n4. We [listened] to fado at a small bar.\n5. My husband [laughed] all the time."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the audio.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o áudio.",
         "example": "Bruna traveled to Portugal. → True",
         "statements": [
             {"text": "Bruna traveled alone.", "answer": False, "translation": "A Bruna viajou sozinha."},
             {"text": "They visited Porto, too.", "answer": True, "translation": "Eles visitaram o Porto também."},
             {"text": "Bruna wanted to stay in Portugal.", "answer": True, "translation": "A Bruna queria ficar em Portugal."},
         ]},
    ],
}

AULA2_SPEAKING = {
    "title": "Speaking — say the -ED right!",
    "lesson": 2,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: diga o verbo e coloque só um estalinho no final: watch → watcht · play → playd. "
                   "Só faça a sílaba \"id\" depois de T ou D.",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "/ɪd/: listen and repeat.",
         "translation": "/ɪd/: ouça e repita (verbos terminados em T ou D).",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula2-say-i{i}.m4a"} for i, t in enumerate(
             ["want, wanted", "need, needed", "decide, decided", "educate, educated", "collect, collected",
              "divide, divided"], 1)]},
        {"type": "speak",
         "prompt": "/t/ and /d/: listen and repeat.",
         "translation": "/t/ e /d/: ouça e repita (sem criar sílaba nova!).",
         "example": "\"cook, cooked\" · \"play, played\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula2-say-t{i}.m4a"} for i, t in enumerate(
             ["cook, cooked", "laugh, laughed", "kiss, kissed", "help, helped", "play, played", "love, loved",
              "use, used", "travel, traveled"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases.",
         "example": "\"I traveled to Chile last year.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula2-say-s{i}.m4a"} for i, t in enumerate(
             ["I traveled to Chile last year.", "We laughed and danced all night.", "She decided to study English.",
              "They cleaned the house and cooked dinner.", "He helped me and I thanked him."], 1)]},
    ],
}

AULA2_READING = {
    "title": "Reading — the surprise party",
    "lesson": 2,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto. Depois, preste atenção no som de cada -ED.",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto do Rafael sobre a festa surpresa para a mãe dele. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula2-reading.m4a",
         "text": "THE SURPRISE PARTY\n\n"
                 "Last Saturday was my mom's 60th birthday. My sister and I planned a surprise party for her.\n"
                 "In the morning, my dad invited her to the mall. While they were out, we cleaned the house, "
                 "cooked lots of food and decorated the living room with balloons.\n"
                 "At six o'clock, all our relatives arrived. We turned off the lights and waited in silence.\n"
                 "When my mom opened the door, we shouted \"SURPRISE!\" She screamed, then laughed and cried at the same time.\n"
                 "We danced, talked and played old songs until midnight. My mom hugged everybody. She loved it!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "The party was for [Rafael's mom].",
         "text": "1. Rafael and his sister [*planned the party.|bought a car.|went to the mall.]\n"
                 "2. The dad took the mom [*to the mall.|to a restaurant.|to the beach.]\n"
                 "3. The relatives arrived [*at six o'clock.|at noon.|at midnight.]\n"
                 "4. When she opened the door, the mom [*screamed, laughed and cried.|went home.|was angry.]"},
        {"type": "group",
         "prompt": "Verbs from the text: which sound is the -ED?",
         "translation": "Verbos do texto: qual é o som do -ED?",
         "example": "planned → /d/",
         "categories": ["/ɪd/", "/t/", "/d/"],
         "words": [
             {"text": "invited", "category": "/ɪd/"}, {"text": "decorated", "category": "/ɪd/"},
             {"text": "waited", "category": "/ɪd/"}, {"text": "shouted", "category": "/ɪd/"},
             {"text": "cooked", "category": "/t/"}, {"text": "laughed", "category": "/t/"},
             {"text": "danced", "category": "/t/"}, {"text": "talked", "category": "/t/"},
             {"text": "cleaned", "category": "/d/"}, {"text": "arrived", "category": "/d/"},
             {"text": "opened", "category": "/d/"}, {"text": "loved", "category": "/d/"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "It was the mom's 60th birthday. → True",
         "statements": [
             {"text": "The mom knew about the party.", "answer": False, "translation": "A mãe sabia da festa."},
             {"text": "The party finished at midnight.", "answer": True, "translation": "A festa terminou à meia-noite."},
         ]},
    ],
}

AULA2_WRITING = {
    "title": "Writing — regular verbs in the past",
    "lesson": 2,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Escreva o passado com -ED e pense no som: /ɪd/ (depois de T ou D) · "
                   "/t/ (sons que não vibram) · /d/ (sons que vibram).",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the past and the sound of -ED (t, d or id).",
         "translation": "Escreva o passado e o som do -ED (escreva t, d ou id).",
         "example": "want → wanted (id)",
         "text": "1. laugh → [laughed] ([t])\n2. travel → [traveled|travelled] ([d])\n3. decide → [decided] ([id])\n"
                 "4. kiss → [kissed] ([t])\n5. use → [used] ([d])"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu viajei para o Chile. → I traveled to Chile.",
         "text": "1. Nós rimos muito. → [We laughed a lot.]\n"
                 "2. Ela decidiu estudar inglês. → [She decided to study English.]\n"
                 "3. Eles me ajudaram ontem. → [They helped me yesterday.]"},
        {"type": "free",
         "prompt": "Write about a special day (a party, a trip, a birthday) with at least 6 regular verbs: "
                   "traveled, visited, danced, laughed, decided, loved, helped…",
         "translation": "Escreva sobre um dia especial (uma festa, uma viagem, um aniversário) com pelo menos 6 verbos "
                        "regulares no passado. Depois leia em voz alta cuidando do som do -ED!",
         "example": "Last year, I traveled to Salvador with my friends.",
         "model_answer": "Last year, I traveled to Salvador with my friends.\n"
                         "We visited the old city and walked a lot.\n"
                         "At night, we danced and laughed in a small bar.\n"
                         "I loved the food, and I decided to go back next year.",
         "keywords": ["visited", "danced", "loved"], "min_words": 30, "points": 4},
    ],
}

AULA2_VIDEO = _video(2, AULA2_TOPIC, "Video — My trip to New York",
                     "a Sarah conta a viagem dela para Nova York — preste atenção no som de cada -ED.",
                     "aula2-video", [
    _q("What's the sound of -ED in \"arrived\"?", "Qual é o som do -ED em \"arrived\"?", "/d/", "/t/", "/ɪd/", "/ed/"),
    _q("What's the sound of -ED in \"walked\"?", "Qual é o som do -ED em \"walked\"?", "/t/", "/d/", "/ɪd/", "/ed/"),
    _q("Why do we say /ɪd/ in \"visited\" and \"wanted\"?", "Por que falamos /ɪd/ em \"visited\" e \"wanted\"?",
       "Because the verbs end in T.", "Because they are irregular.", "Because they end in a vowel.",
       "Because they are long verbs."),
    _q("What's the sound of -ED in \"danced\"?", "Qual é o som do -ED em \"danced\"?", "/t/", "/d/", "/ɪd/", "/ed/"),
])

# ---------- Aula 03 — Past Simple: negative (https://youtu.be/XmT1GA9zUMA) ----------

AULA3_TOPIC = "Aula 03 — Past Simple (negative)"

AULA3_DIDNT = {
    "title": "Didn't + base form",
    "lesson": 3,
    "description": "NEGATIVA no passado: SUJEITO + DIDN'T + VERBO NA FORMA BÁSICA\n"
                   "didn't = did not (a contração é mais natural)\n"
                   "O DIDN'T já mostra que é PASSADO e NEGATIVO → o verbo volta para a forma básica (sem -ED, sem forma irregular):\n"
                   "cooked → didn't cook · watched → didn't watch · went → didn't go · ate → didn't eat · bought → didn't buy\n"
                   "I didn't take a nap last Sunday. · She didn't see her friends last weekend. · "
                   "They didn't go to the beach on Saturday.\n"
                   "✗ I didn't went · ✗ She didn't cooked  →  ✓ I didn't go · ✓ She didn't cook\n"
                   "Igual para todos: I / you / he / she / we / they didn't…",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the past form to the base form.",
         "translation": "Ligue o verbo no passado à forma básica (exercício da aula: identifique o verbo!).",
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
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta.",
         "example": "I [didn't take] a nap last Sunday.",
         "text": "1. He [*didn't do|didn't did|doesn't did] his homework.\n"
                 "2. My father [*didn't see|didn't saw|not saw] an accident.\n"
                 "3. Carla [*didn't meet|didn't met|didn't meeted] an interesting guy.\n"
                 "4. She [*didn't sleep|didn't slept|wasn't sleep] for many hours.\n"
                 "5. My friend [*didn't give|didn't gave|don't gave] me a beautiful shirt."},
        {"type": "fill",
         "prompt": "Write the negative: didn't + base form.",
         "translation": "Escreva a negativa: didn't + forma básica.",
         "example": "cooked → didn't cook",
         "text": "1. walked → [didn't walk|did not walk]\n2. worked → [didn't work|did not work]\n"
                 "3. woke up → [didn't wake up|did not wake up]\n4. had → [didn't have|did not have]\n"
                 "5. read → [didn't read|did not read]\n6. wore → [didn't wear|did not wear]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Didn't\" means \"did not\". → True",
         "statements": [
             {"text": "After DIDN'T, the verb stays in the past: \"I didn't went\".", "answer": False,
              "translation": "Depois de DIDN'T, o verbo fica no passado: \"I didn't went\"."},
             {"text": "\"Didn't\" is more natural than \"did not\" in conversation.", "answer": True,
              "translation": "\"Didn't\" é mais natural do que \"did not\" na conversa."},
             {"text": "We use \"didn't\" for regular and irregular verbs.", "answer": True,
              "translation": "Usamos \"didn't\" com verbos regulares e irregulares."},
         ]},
    ],
}

AULA3_SENTENCES = {
    "title": "Make it negative!",
    "lesson": 3,
    "description": "Como transformar uma frase em NEGATIVA:\n"
                   "1. Identifique o verbo: She WENT to the park yesterday.\n"
                   "2. Ache a forma básica: went → GO\n"
                   "3. Use DIDN'T + forma básica: She DIDN'T GO to the park yesterday.\n"
                   "Exemplos da aula: They watched TV last night. → They didn't watch TV last night. · "
                   "His girlfriend wore a red dress. → His girlfriend didn't wear a red dress.\n"
                   "Atenção: com WAS / WERE não usamos didn't → I wasn't at home. · They weren't tired.",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Make the sentences negative.",
         "translation": "Passe as frases para a negativa.",
         "example": "She cooked last night. → She didn't cook last night.",
         "text": "1. His girlfriend wore a red dress last night. → [His girlfriend didn't wear a red dress last night.|"
                 "His girlfriend did not wear a red dress last night.]\n"
                 "2. We bought a new car. → [We didn't buy a new car.|We did not buy a new car.]\n"
                 "3. I took a nap after lunch. → [I didn't take a nap after lunch.|I did not take a nap after lunch.]"},
        {"type": "dropdown",
         "prompt": "Didn't or wasn't / weren't?",
         "translation": "Didn't ou wasn't / weren't? (verbo normal → didn't · verbo to be → wasn't / weren't)",
         "example": "I [wasn't] at home. · I [didn't] go out.",
         "text": "1. My friends [*weren't|didn't] at the party.\n2. I [*didn't|wasn't] like the movie.\n"
                 "3. The food [*wasn't|didn't] good.\n4. We [*didn't|weren't] eat at home.\n"
                 "5. She [*wasn't|didn't] happy yesterday."},
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras em ordem. (Eles não foram à praia no sábado.)",
         "example": "didn't / I / a nap / take → I didn't take a nap.",
         "tokens": ["They", "didn't", "go", "to", "the", "beach", "on", "Saturday."], "alternatives": []},
        {"type": "choice",
         "prompt": "Which sentence is correct?",
         "translation": "Qual frase está correta?",
         "example": "I didn't cook yesterday. ✓",
         "options": ["She didn't see her friends last weekend.", "She didn't saw her friends last weekend.",
                     "She doesn't saw her friends last weekend.", "She not saw her friends last weekend."],
         "correct": 0},
    ],
}

AULA3_LISTENING = {
    "title": "Listening — the worst vacation",
    "lesson": 3,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: o T de DIDN'T quase some na fala: \"dĭdn' go\". Preste atenção: é afirmativa ou negativa?",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Affirmative or negative? Listen and choose.",
         "translation": "Afirmativa ou negativa? Ouça e escolha.",
         "example": "Você ouve: \"I didn't sleep.\" → didn't sleep",
         "audio": f"{AUDIO}/aula3-forms.m4a",
         "text": "1. He [*didn't call|called] me.\n2. We [*met|didn't meet] at school.\n3. She [*didn't wear|wore] a dress.\n"
                 "4. They [*slept|didn't sleep] well.\n5. I [*didn't take|took] a nap."},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"I didn't cook yesterday.\" → I [didn't cook] yesterday.",
         "audio": f"{AUDIO}/aula3-dictation.m4a",
         "text": "1. She [didn't sleep] for many hours.\n2. We [didn't watch] TV last night.\n"
                 "3. My friend [didn't give] me a present.\n4. They [didn't do] their homework."},
        {"type": "info",
         "prompt": "Now listen: Tiago talks about his vacation in the mountains.",
         "translation": "Agora ouça: o Tiago conta para a Júlia como foram as férias dele nas montanhas. Nada deu certo! "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula3-vacation.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Tiago went to the mountains. → True",
         "statements": [
             {"text": "It was sunny every day.", "answer": False, "translation": "Fez sol todos os dias."},
             {"text": "Tiago didn't see the waterfall.", "answer": True, "translation": "O Tiago não viu a cachoeira."},
             {"text": "The hotel restaurant was open.", "answer": False, "translation": "O restaurante do hotel estava aberto."},
             {"text": "Tiago read three books.", "answer": True, "translation": "O Tiago leu três livros."},
         ]},
        {"type": "fill",
         "prompt": "Listen again and complete Tiago's sentences.",
         "translation": "Ouça de novo e complete as frases do Tiago.",
         "example": "It [didn't stop] raining.",
         "text": "1. We [didn't go] hiking.\n2. I [didn't take] any good photos.\n3. My wife [didn't like] the hotel."},
    ],
}

AULA3_SPEAKING = {
    "title": "Speaking — I didn't…",
    "lesson": 3,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: didn't = \"DÍd-nt\" — o T final é bem fraquinho.",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat: affirmative → negative.",
         "translation": "Ouça e repita: afirmativa → negativa.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula3-say-v{i}.m4a"} for i, t in enumerate(
             ["cooked, didn't cook", "watched, didn't watch", "went, didn't go", "ate, didn't eat",
              "saw, didn't see", "slept, didn't sleep", "gave, didn't give", "wore, didn't wear"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "\"I didn't take a nap last Sunday.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula3-say-s{i}.m4a"} for i, t in enumerate(
             ["I didn't take a nap last Sunday.", "She didn't see her friends last weekend.",
              "They didn't go to the beach on Saturday.", "He didn't do his homework.",
              "My father didn't see an accident.", "His girlfriend didn't wear a red dress last night."], 1)]},
        {"type": "speak",
         "prompt": "Now talk about YOU.",
         "translation": "Agora fale sobre VOCÊ: complete as frases com algo que você NÃO fez.",
         "example": "\"Yesterday, I didn't…\" → \"Yesterday, I didn't go to the gym.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula3-say-y{i}.m4a"} for i, t in enumerate(
             ["Yesterday, I didn't…", "Last weekend, I didn't…", "When I was a kid, I didn't…",
              "This morning, I didn't…"], 1)]},
    ],
}

AULA3_READING = {
    "title": "Reading — a week without my phone",
    "lesson": 3,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto da Bianca, que passou uma semana sem celular. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula3-reading.m4a",
         "text": "A WEEK WITHOUT MY PHONE\n\n"
                 "Last month, I tried an experiment: one week without my phone!\n"
                 "On the first day, it was difficult. I didn't know the time, because I don't have a watch. "
                 "I didn't check my messages, and I didn't watch videos before bed.\n"
                 "But then, things changed. I didn't spend hours on social media, so I had more time. "
                 "I read two books and I cooked new recipes.\n"
                 "I didn't take photos of my food — I ate it! I talked to my neighbors and I walked in the park every day.\n"
                 "There was one problem: my mom called me ten times and I didn't answer. She wasn't happy!\n"
                 "I didn't stop using my phone forever, but now I use it less."},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Bianca's experiment was [one week without her phone].",
         "text": "1. On the first day, Bianca [*didn't know the time.|was very happy.|bought a watch.]\n"
                 "2. With more time, she [*read two books.|watched videos.|took photos of her food.]\n"
                 "3. Her mom [*called ten times.|visited her.|sent a letter.]\n"
                 "4. Today, Bianca [*uses her phone less.|doesn't use a phone.|uses her phone more.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "The experiment was last month. → True",
         "statements": [
             {"text": "Bianca checked her messages every day.", "answer": False,
              "translation": "A Bianca olhou as mensagens todos os dias."},
             {"text": "Her mom wasn't happy.", "answer": True, "translation": "A mãe dela não ficou feliz."},
             {"text": "She talked to her neighbors.", "answer": True, "translation": "Ela conversou com os vizinhos."},
         ]},
        {"type": "fill",
         "prompt": "Complete with didn't + verb, according to the text.",
         "translation": "Complete com didn't + verbo, de acordo com o texto.",
         "example": "She [didn't check] her messages.",
         "text": "1. She [didn't watch] videos before bed.\n2. She [didn't spend] hours on social media.\n"
                 "3. She [didn't answer] her mom's calls."},
    ],
}

AULA3_WRITING = {
    "title": "Writing — what I didn't do",
    "lesson": 3,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ SUJEITO + DIDN'T + VERBO NA FORMA BÁSICA (didn't go, didn't eat, didn't buy).\n"
                   "Com was / were: wasn't / weren't.",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Correct the mistakes.",
         "translation": "Corrija os erros.",
         "example": "I didn't went to school. → I didn't go to school.",
         "text": "1. She didn't bought the shoes. → [She didn't buy the shoes.|She did not buy the shoes.]\n"
                 "2. We didn't slept well. → [We didn't sleep well.|We did not sleep well.]\n"
                 "3. They didn't was at home. → [They weren't at home.|They were not at home.]"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu não cozinhei ontem. → I didn't cook yesterday.",
         "text": "1. Ela não dormiu bem. → [She didn't sleep well.|She did not sleep well.]\n"
                 "2. Nós não vimos o acidente. → [We didn't see the accident.|We did not see the accident.]"},
        {"type": "free",
         "prompt": "Write about a day when things went wrong (or a lazy day!). What didn't you do? "
                   "Write at least 4 sentences with didn't and 2 with the affirmative.",
         "translation": "Escreva sobre um dia em que deu tudo errado (ou um dia de preguiça!). O que você NÃO fez? "
                        "Escreva pelo menos 4 frases com didn't e 2 na afirmativa.",
         "example": "Last Sunday, I didn't wake up early.",
         "model_answer": "Last Sunday was a lazy day. I didn't wake up early.\n"
                         "I didn't make breakfast, and I didn't go to the gym.\n"
                         "I didn't clean the house and I didn't answer my messages.\n"
                         "I watched three movies and I ate pizza on the sofa. It was perfect!",
         "keywords": ["didn't", "didn't go", "watched"], "min_words": 30, "points": 4},
    ],
}

AULA3_VIDEO = _video(3, AULA3_TOPIC, "Video — A terrible Monday",
                     "o Mark conta tudo o que deu errado na segunda-feira: o que ele NÃO fez.",
                     "aula3-video", [
    _q("What happened in the morning?", "O que aconteceu de manhã?", "His alarm clock didn't ring.",
       "His alarm clock didn't rang.", "His alarm clock rang at six.", "He didn't woke up."),
    _q("Complete: He ___ the bus.", "Complete: ele ___ o ônibus.", "didn't catch", "didn't caught", "doesn't catch",
       "not caught"),
    _q("Complete: He ___ his umbrella.", "Complete: ele ___ o guarda-chuva.", "didn't have", "didn't had", "hadn't",
       "wasn't have"),
    _q("Why was his boss unhappy?", "Por que o chefe dele não ficou feliz?", "He didn't finish his report.",
       "He didn't finished his report.", "He didn't go to work.", "He didn't drink coffee."),
])

# ---------- Aula 04 — Past Simple: interrogative (https://youtu.be/xavnVHYvcg0) ----------

AULA4_TOPIC = "Aula 04 — Past Simple (interrogative)"

AULA4_DID = {
    "title": "Did…? Yes, I did. / No, I didn't.",
    "lesson": 4,
    "description": "PERGUNTA no passado: DID + SUJEITO + VERBO NA FORMA BÁSICA (+ complemento)?\n"
                   "She cooked last night. → She didn't cook last night. → DID she COOK last night?\n"
                   "Did you go to the movies last weekend? · Did she cook dinner last Sunday? · "
                   "Did they have a picnic at the park last Saturday?\n"
                   "Igual para todos: Did I / you / he / she / it / we / they go to the park?\n"
                   "Pergunta com DID → resposta YES ou NO, com respostas curtas:\n"
                   "Yes, I did. · No, I didn't. · Yes, they did. · No, he didn't.\n"
                   "Resposta completa também é possível, mas com complemento: Yes, I bought a new dress. (✗ Yes, I bought.)\n"
                   "Em português, só a entonação muda (\"Você estudou inglês?\"). Em inglês precisamos do DID: Did you study English?",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Make questions with Did.",
         "translation": "Transforme em perguntas com Did.",
         "example": "She cooked last night. → Did she cook last night?",
         "text": "1. You studied English. → [Did you study English?]\n"
                 "2. She woke up at 6. → [Did she wake up at 6?|Did she wake up at six?]\n"
                 "3. They had a picnic at the park. → [Did they have a picnic at the park?]\n"
                 "4. He bought a bike. → [Did he buy a bike?]"},
        {"type": "dropdown",
         "prompt": "Choose the right short answer.",
         "translation": "Escolha a resposta curta certa.",
         "example": "Did they play soccer yesterday? (✓) → [Yes, they did.]",
         "text": "1. Did you go to the park? (✓) → [*Yes, I did.|Yes, I went.|Yes, I do.]\n"
                 "2. Did she cook dinner? (✗) → [*No, she didn't.|No, she don't.|No, she didn't cooked.]\n"
                 "3. Did you buy a new dress? (✓) → [*Yes, I did.|Yes, I bought.|Yes, I buy.]\n"
                 "4. Did they like the trip? (✗) → [*No, they didn't.|No, they not.|No, they doesn't.]"},
        {"type": "dropdown",
         "prompt": "Correct or incorrect?",
         "translation": "Correta ou incorreta? (exercício da aula)",
         "example": "Did you sleep well? → [Correct]",
         "text": "1. Did he went to the park? → [*Incorrect|Correct]\n2. Did she watch TV? → [*Correct|Incorrect]\n"
                 "3. Did you slept well? → [*Incorrect|Correct]\n4. Did they have a picnic? → [*Correct|Incorrect]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "Questions with DID have yes / no answers. → True",
         "statements": [
             {"text": "After DID, we use the verb in the past.", "answer": False,
              "translation": "Depois de DID, usamos o verbo no passado."},
             {"text": "\"Yes, I did\" is a short answer.", "answer": True, "translation": "\"Yes, I did\" é uma resposta curta."},
             {"text": "In English, we can make a question only with intonation: \"You studied English?\"", "answer": False,
              "translation": "Em inglês, podemos fazer pergunta só com a entonação: \"You studied English?\""},
         ]},
    ],
}

AULA4_WH = {
    "title": "Wh- questions: what, where, when, why, how",
    "lesson": 4,
    "description": "WH- QUESTION + DID + SUJEITO + VERBO NA FORMA BÁSICA + (informação extra)?\n"
                   "A question word tem PRIORIDADE: vem primeiro, depois o did.\n"
                   "What did you eat in the morning? · Where did she go last night? · When did you travel to Canada? · "
                   "Why did you call me? · How did you meet your best friend? · How long did you stay there?\n"
                   "Essas perguntas pedem INFORMAÇÃO, não yes/no:\n"
                   "What did you eat? → I ate eggs and coffee. (✗ Yes, I did.)\n"
                   "where = onde · what = o que / qual · when = quando · why = por que · how = como · "
                   "how long = quanto tempo",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas.",
         "example": "Where did you go last night? → I went to a party.",
         "pairs": [
             {"left": "What did you eat for dinner?", "right": "I ate soup."},
             {"left": "When did you travel to Canada?", "right": "Last month."},
             {"left": "Why did you call me?", "right": "Because I needed help."},
             {"left": "How did you meet your best friend?", "right": "At school, when we were kids."},
             {"left": "How long did you stay there?", "right": "For two weeks."},
             {"left": "Where did you stay?", "right": "At a hotel."},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the question word.",
         "translation": "Escolha a palavra interrogativa.",
         "example": "[Where] did she go last night? — To the cinema.",
         "text": "1. [*What|Where|When] did you eat in the morning? — Eggs and coffee.\n"
                 "2. [*How long|How|Why] did you stay in Rio? — Five days.\n"
                 "3. [*Why|What|Where] did you leave early? — Because I was tired.\n"
                 "4. [*How|When|What] did you go to work? — By bus.\n"
                 "5. [*When|Where|Why] did they arrive? — Yesterday."},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Onde ela foi ontem à noite?)",
         "example": "did / eat / you / What → What did you eat?",
         "tokens": ["Where", "did", "she", "go", "last", "night?"], "alternatives": []},
        {"type": "choice",
         "prompt": "Which question is correct?",
         "translation": "Qual pergunta está correta?",
         "example": "What did you eat? ✓",
         "options": ["How did you meet your best friend?", "How you met your best friend?",
                     "How did you met your best friend?", "Did how you meet your best friend?"],
         "correct": 0},
    ],
}

AULA4_LISTENING = {
    "title": "Listening — the marathon interview",
    "lesson": 4,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: o DID é fraco e se liga ao sujeito: \"didju\" (did you), \"didshi\" (did she).",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the question you hear.",
         "translation": "Ouça e escolha a pergunta que você ouve.",
         "example": "Você ouve: \"Did you sleep well?\" → Did you",
         "audio": f"{AUDIO}/aula4-questions.m4a",
         "text": "1. [*Did you|Do you] like it?\n2. [*Where did|Where do] they live?\n3. [*Did she|Does she] work there?\n"
                 "4. [*What did|What do] you eat?\n5. [*How long did|How long do] you stay?"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete the questions.",
         "translation": "Ditado: ouça e complete as perguntas.",
         "example": "Você ouve: \"Did you go to the movies?\" → [Did] you go to the movies?",
         "audio": f"{AUDIO}/aula4-dictation.m4a",
         "text": "1. [Why] did you call me?\n2. [How] did you meet your best friend?\n3. Did they [have] a picnic?\n"
                 "4. Where did you [stay]?"},
        {"type": "info",
         "prompt": "Now listen: a reporter interviews the winner of a marathon.",
         "translation": "Agora ouça: um repórter entrevista a vencedora de uma maratona. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula4-marathon.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "The winner's name is [Sofia].",
         "text": "1. How long did Sofia run? → [*Two hours and thirty minutes.|Three hours.|Two hours.]\n"
                 "2. When did she start running? → [*When she was twelve.|Last year.|When she was twenty.]\n"
                 "3. What did she eat before the race? → [*Bread with banana.|Pasta.|Nothing.]\n"
                 "4. Who did she call after the race? → [*Her grandmother.|Her coach.|Her husband.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the interview.",
         "translation": "Verdadeiro ou falso? Responda de acordo com a entrevista.",
         "example": "Sofia won the marathon. → True",
         "statements": [
             {"text": "Sofia slept well before the race.", "answer": False,
              "translation": "A Sofia dormiu bem antes da corrida."},
             {"text": "Her grandmother watched the race on TV.", "answer": True,
              "translation": "A avó dela assistiu à corrida na TV."},
         ]},
    ],
}

AULA4_SPEAKING = {
    "title": "Speaking — ask and answer",
    "lesson": 4,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: did you = \"didju\" · what did you = \"wódidju\". A entonação desce nas wh- questions e sobe nas "
                   "perguntas de yes/no.",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the questions and answers.",
         "translation": "Ouça e repita as perguntas e respostas.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula4-say-s{i}.m4a"} for i, t in enumerate(
             ["Did you go to the park? Yes, I did.", "Did she cook dinner? No, she didn't.",
              "Did they play soccer yesterday? Yes, they did.", "Did he buy a bike? No, he didn't.",
              "What did you eat in the morning?", "Where did she go last night?", "Why did you call me?",
              "How did you meet your best friend?"], 1)]},
        {"type": "speak",
         "prompt": "Now answer about YOUR last vacation.",
         "translation": "Agora responda sobre as SUAS últimas férias (exercício da aula).",
         "example": "\"Where did you go?\" → \"I went to Rio de Janeiro.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula4-say-y{i}.m4a"} for i, t in enumerate(
             ["Did you travel on your last vacation?", "When did you travel?", "Where did you go?",
              "Where did you stay?", "How long did you stay there?", "Did you like the trip?"], 1)]},
    ],
}

AULA4_READING = {
    "title": "Reading — an interview with my grandpa",
    "lesson": 4,
    "subject": "Reading",
    "description": "Leia (e ouça) a entrevista e responda às perguntas de acordo com o texto.",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the interview.",
         "translation": "Leia e ouça a entrevista que a Lívia fez com o avô dela para um trabalho da escola. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula4-reading.m4a",
         "text": "AN INTERVIEW WITH MY GRANDPA\n\n"
                 "Lívia: Where did you grow up, Grandpa?\n"
                 "Grandpa: I grew up in a small town in Paraná.\n"
                 "Lívia: Did you like school?\n"
                 "Grandpa: No, I didn't! I liked soccer. I played every afternoon.\n"
                 "Lívia: What was your first job?\n"
                 "Grandpa: I worked at a bakery. I started at four in the morning!\n"
                 "Lívia: How did you meet Grandma?\n"
                 "Grandpa: She bought bread at the bakery every day. One day, I gave her a cake for free.\n"
                 "Lívia: Did she like the cake?\n"
                 "Grandpa: Yes, she did. And she liked me, too! We got married two years later."},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Who did Lívia interview? → [Her grandpa.]",
         "text": "1. Where did Grandpa grow up? → [*In a small town in Paraná.|In São Paulo.|On a farm in Minas.]\n"
                 "2. What did he do every afternoon? → [*He played soccer.|He studied.|He worked.]\n"
                 "3. Where did he work? → [*At a bakery.|At a school.|At a bank.]\n"
                 "4. How did he meet Grandma? → [*She bought bread at the bakery.|At a party.|At school.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Grandpa worked at a bakery. → True",
         "statements": [
             {"text": "Grandpa liked school.", "answer": False, "translation": "O avô gostava da escola."},
             {"text": "He started work very early.", "answer": True, "translation": "Ele começava a trabalhar muito cedo."},
             {"text": "They got married two years later.", "answer": True, "translation": "Eles se casaram dois anos depois."},
         ]},
        {"type": "fill",
         "prompt": "Complete the questions from the interview.",
         "translation": "Complete as perguntas da entrevista.",
         "example": "Where did you [grow] up?",
         "text": "1. [Did] you like school?\n2. [How] did you meet Grandma?\n3. Did she [like] the cake?"},
    ],
}

AULA4_WRITING = {
    "title": "Writing — questions about the past",
    "lesson": 4,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ DID + sujeito + verbo na forma básica? → Yes, I did. / No, I didn't.\n"
                   "WH- + DID + sujeito + verbo? → resposta com informação (What did you eat? → I ate pizza.)",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the question for the answer.",
         "translation": "Escreva a pergunta para a resposta (use a palavra entre parênteses).",
         "example": "(where) I went to Canada. → Where did you go?",
         "text": "1. (what) I ate pancakes. → [What did you eat?]\n"
                 "2. (when) I traveled in February. → [When did you travel?]\n"
                 "3. (how long) I stayed for five days. → [How long did you stay?|How long did you stay there?]"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Você estudou inglês? → Did you study English?",
         "text": "1. Por que você me ligou? → [Why did you call me?]\n"
                 "2. Eles gostaram da viagem? → [Did they like the trip?]"},
        {"type": "free",
         "prompt": "Answer the questions about your last vacation, like in the lesson: Did you travel? When did you travel? "
                   "Where did you go? Where did you stay? How long did you stay there? Did you like the trip?",
         "translation": "Responda às perguntas sobre as suas últimas férias, como no exercício da aula. "
                        "Use frases completas no passado.",
         "example": "Yes, I did. I traveled in February.",
         "model_answer": "Yes, I did. I traveled in February.\n"
                         "I went to Rio de Janeiro with my family.\n"
                         "We stayed in a hotel near the beach.\n"
                         "We stayed there for five days.\n"
                         "Yes, I did. I loved it!",
         "keywords": ["I did", "I went", "stayed"], "min_words": 30, "points": 4},
    ],
}

AULA4_VIDEO = _video(4, AULA4_TOPIC, "Video — How was Japan?",
                     "a Sarah faz perguntas no passado para o Leo sobre a viagem dele ao Japão.",
                     "aula4-video", [
    _q("Where did Leo go?", "Aonde o Leo foi?", "He went to Japan.", "He goes to Japan.", "He did go to China.",
       "He went to Korea."),
    _q("When did he travel?", "Quando ele viajou?", "In April.", "In August.", "In December.", "Last week."),
    _q("Did he eat sushi?", "Ele comeu sushi?", "Yes, he did.", "Yes, he ate.", "No, he didn't.", "Yes, he does."),
    _q("Complete: ___ you visit temples?", "Complete: ___ você visitou templos?", "Did", "Do", "Were", "Does"),
    _q("Did he see Mount Fuji?", "Ele viu o Monte Fuji?", "No, he didn't.", "No, he didn't saw.", "Yes, he did.",
       "No, he doesn't."),
])

# ---------- Aula 05 — Possessive 's (https://youtu.be/tb-B06CgpFo) ----------

AULA5_TOPIC = "Aula 05 — Possessive 's"

AULA5_APOSTROPHE = {
    "title": "Possessive 's: Peter's car, my parents' house",
    "lesson": 5,
    "description": "O 'S (apóstrofo + S) mostra POSSE: algo pertence a alguém. Em português: \"o carro DO Peter\" → "
                   "Peter's car (o dono vem PRIMEIRO, depois a coisa).\n"
                   "Marcas: Hershey's, Levi's, Ben & Jerry's, Kellogg's = o negócio do Hershey, do Levi…\n"
                   "Também para FAMÍLIA e relações: Madonna's brother · Mary's mother\n"
                   "REGRAS:\n"
                   "• Nome ou substantivo no singular → 'S: Peter's car · my mom's restaurant\n"
                   "• Nome terminado em S → 'S ou só ': Marcus's dog / Marcus' dog\n"
                   "• Plural terminado em S → só ': my parents' house · my friends' baby\n"
                   "• Plural irregular (sem S) → 'S: the children's toys\n"
                   "• Dois nomes, MESMA coisa (posse compartilhada) → 'S só no último: Kim and Kyle's mom\n"
                   "• Dois nomes, coisas DIFERENTES → 'S em cada um: Lisa's and Mel's mothers are friends.",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta.",
         "example": "It's [Peter's] car.",
         "text": "1. That is [*Emma's|Emmas|Emma] cat.\n2. That is my [*parents'|parent's|parents's] garden.\n"
                 "3. Ben is [*James's|James|Jame's] brother.\n4. That is my [*cousins'|cousin|cousins's] dog. (I have two cousins.)\n"
                 "5. These are the [*children's|childrens'|childrens] toys.\n6. It's my [*mom's|moms|moms'] restaurant."},
        {"type": "fill",
         "prompt": "Rewrite the sentences using 's or '.",
         "translation": "Reescreva as frases usando 's ou ' (exercício da aula).",
         "example": "Emma has a cat. → That is Emma's cat.",
         "text": "1. Daniel has a laptop. → That is [Daniel's] laptop.\n"
                 "2. Paul has two children, Lucas and Sophie. → Paul is Lucas and [Sophie's] father.\n"
                 "3. My parents have a garden. → That is my [parents'] garden.\n"
                 "4. My sister has a new bike. → That is my [sister's] new bike."},
        {"type": "choice",
         "prompt": "Kim and Kyle are brother and sister. They have the same mom. What do you say?",
         "translation": "A Kim e o Kyle são irmãos e têm a mesma mãe. O que você fala?",
         "example": "Posse compartilhada → 's só no último nome.",
         "options": ["Kim and Kyle's mom", "Kim's and Kyle's mom", "Kim and Kyle mom's", "Kims and Kyles mom"],
         "correct": 0},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "The 's shows possession. → True",
         "statements": [
             {"text": "In \"Levi's\", the 's means the business belongs to Levi Strauss.", "answer": True,
              "translation": "Em \"Levi's\", o 's significa que o negócio pertence ao Levi Strauss."},
             {"text": "For plural nouns ending in S, we add 's: my parents's house.", "answer": False,
              "translation": "Para plurais terminados em S, colocamos 's: my parents's house."},
             {"text": "\"Children\" doesn't end in S, so we say \"the children's toys\".", "answer": True,
              "translation": "\"Children\" não termina em S, então dizemos \"the children's toys\"."},
             {"text": "In English, the owner comes after the object: \"the car Peter's\".", "answer": False,
              "translation": "Em inglês, o dono vem depois do objeto: \"the car Peter's\"."},
         ]},
    ],
}

AULA5_WHOSE = {
    "title": "Whose…? and Who's…?",
    "lesson": 5,
    "description": "WHOSE = de quem? (pergunta sobre o DONO)\n"
                   "Whose hat is it? → It's Justin's hat. · Whose watch is this? → It's Neymar's watch. · "
                   "Whose dress is it? → It's Shakira's dress. · Whose guitar is it? → It's Madonna's guitar.\n"
                   "WHO'S = who is (quem é / quem está) — a pronúncia é IGUAL a whose!\n"
                   "Who's at the door? (Quem está na porta?) · Who's your best friend? (Quem é o seu melhor amigo?) · "
                   "Who's cooking today? (Quem está cozinhando hoje?)\n"
                   "Vocabulário da aula: hat (touca/chapéu) · glasses (óculos) · watch (relógio) · dress (vestido) · "
                   "jacket (jaqueta) · guitar (violão/guitarra) · suit (terno)",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Whose or who's?",
         "translation": "Whose (de quem) ou who's (quem é / quem está)? Exercício da aula.",
         "example": "[Whose] car is that?",
         "text": "1. I don't know [*whose|who's] keys these are.\n2. [*Who's|Whose] at the door?\n"
                 "3. [*Who's|Whose] cooking today?\n4. [*Who's|Whose] your best friend?\n5. [*Whose|Who's] car is that?"},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas (os artistas da aula).",
         "example": "Whose hat is it? → It's Justin's hat.",
         "pairs": [
             {"left": "Whose watch is this?", "right": "It's Neymar's watch."},
             {"left": "Whose dress is it?", "right": "It's Shakira's dress."},
             {"left": "Whose guitar is it?", "right": "It's Madonna's guitar."},
             {"left": "Who's Madonna's brother?", "right": "His name is Christopher."},
             {"left": "Who's at the door?", "right": "It's the mailman."},
         ]},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (De quem é esta jaqueta?)",
         "example": "is / Whose / watch / this → Whose watch is this?",
         "tokens": ["Whose", "jacket", "is", "this?"], "alternatives": []},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "É o relógio do Neymar. → It's Neymar's watch.",
         "text": "1. É o vestido da Shakira. → [It's Shakira's dress.|It is Shakira's dress.]\n"
                 "2. Esta é a casa dos meus pais. → [This is my parents' house.]\n"
                 "3. Quem é o seu melhor amigo? → [Who's your best friend?|Who is your best friend?]"},
    ],
}

AULA5_LISTENING = {
    "title": "Listening — the lost and found box",
    "lesson": 5,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: o 'S soa como /s/ ou /z/ e se liga ao nome: \"Peter's\" = \"pí-terz\". "
                   "Whose e who's soam igual — preste atenção no resto da frase!",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"It's Anna's bag.\" → Anna's bag",
         "audio": f"{AUDIO}/aula5-words.m4a",
         "text": "1. It's [*Peter's car.|Peter car.]\n2. That's my [*brother's|brothers] room.\n"
                 "3. These are the [*children's toys.|children toys.]\n4. [*Whose|Who's] bag is this?\n"
                 "5. [*Who's|Whose] your teacher?"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"It's Justin's hat.\" → It's [Justin's] hat.",
         "audio": f"{AUDIO}/aula5-dictation.m4a",
         "text": "1. That's my [mom's] restaurant.\n2. We went to my [parents'] house.\n"
                 "3. [Whose] watch is this?\n4. Kim and [Kyle's] mom is a doctor."},
        {"type": "info",
         "prompt": "Now listen: a teacher finds things in the classroom.",
         "translation": "Agora ouça: depois da aula, a professora encontra várias coisas esquecidas na sala e pergunta "
                        "de quem são. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula5-lost.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "match",
         "prompt": "Listen again. Whose is it?",
         "translation": "Ouça de novo. De quem é cada coisa?",
         "example": "the umbrella → Carol's",
         "pairs": [
             {"left": "the blue jacket", "right": "Tom's"},
             {"left": "the glasses", "right": "the teacher's"},
             {"left": "the notebook", "right": "Ana and Leo's (they share it)"},
             {"left": "the water bottle", "right": "Mr. Silva's"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the audio.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o áudio.",
         "example": "The teacher found things in the classroom. → True",
         "statements": [
             {"text": "The blue jacket is Ana's.", "answer": False, "translation": "A jaqueta azul é da Ana."},
             {"text": "The teacher forgot her glasses.", "answer": True, "translation": "A professora esqueceu os óculos dela."},
         ]},
    ],
}

AULA5_SPEAKING = {
    "title": "Speaking — whose is it?",
    "lesson": 5,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: whose = \"rûz\" (igual a who's) · o 'S se cola no nome: \"Neymar's\" = \"nei-márz\".",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula5-say-s{i}.m4a"} for i, t in enumerate(
             ["Whose hat is it? It's Justin's hat.", "Whose watch is this? It's Neymar's watch.",
              "Whose dress is it? It's Shakira's dress.", "Whose guitar is it? It's Madonna's guitar.",
              "It's Peter's car.", "That is my parents' garden.", "These are the children's toys.",
              "Kim and Kyle's mom is a doctor."], 1)]},
        {"type": "speak",
         "prompt": "Now answer about YOUR family.",
         "translation": "Agora responda sobre a SUA família, usando 's.",
         "example": "\"What's your mother's name?\" → \"My mother's name is Rosa.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula5-say-y{i}.m4a"} for i, t in enumerate(
             ["What's your mother's name?", "What's your best friend's name?", "Who's your favorite singer?",
              "Where is your parents' house?"], 1)]},
    ],
}

AULA5_READING = {
    "title": "Reading — my family's restaurant",
    "lesson": 5,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto da Giovana sobre o restaurante da família dela. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula5-reading.m4a",
         "text": "MY FAMILY'S RESTAURANT\n\n"
                 "My grandparents started a small restaurant in 1980. Its name is \"Nonna Lucia's\". "
                 "Lucia is my grandmother's name!\n"
                 "Today, it's my mom's restaurant. My dad is the chef, and my aunt is the manager.\n"
                 "The most famous dish is my grandma's lasagna. People come from other cities to try it!\n"
                 "On weekends, I help at the restaurant. My cousins help too, and the children's corner is their idea: "
                 "there are toys and books for the kids.\n"
                 "My brother Marcus doesn't work there. Marcus's dream is different: he wants to open a bakery. "
                 "Maybe one day we can say: \"Let's buy bread at Marcus's!\""},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Who started the restaurant? → [Giovana's grandparents.]",
         "text": "1. Whose name is Lucia? → [*Her grandmother's.|Her mom's.|Her aunt's.]\n"
                 "2. Whose restaurant is it today? → [*Her mom's.|Her brother's.|Her aunt's.]\n"
                 "3. What is the most famous dish? → [*Her grandma's lasagna.|Her dad's pizza.|Marcus's bread.]\n"
                 "4. Whose idea was the children's corner? → [*Her cousins'.|Her mom's.|Marcus's.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Giovana's dad is the chef. → True",
         "statements": [
             {"text": "Marcus works at the restaurant.", "answer": False, "translation": "O Marcus trabalha no restaurante."},
             {"text": "Marcus's dream is to open a bakery.", "answer": True,
              "translation": "O sonho do Marcus é abrir uma padaria."},
         ]},
        {"type": "fill",
         "prompt": "Complete with 's or ', according to the text.",
         "translation": "Complete com 's ou ', de acordo com o texto.",
         "example": "It's my [mom's] restaurant.",
         "text": "1. The famous dish is my [grandma's] lasagna.\n2. There are toys in the [children's] corner.\n"
                 "3. The corner was my [cousins'] idea."},
    ],
}

AULA5_WRITING = {
    "title": "Writing — whose is it?",
    "lesson": 5,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ dono + 'S + coisa: Peter's car · plural com S → só ': my parents' house · "
                   "children's · Kim and Kyle's mom (mesma mãe).",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the phrase with 's or '.",
         "translation": "Escreva a expressão com 's ou '.",
         "example": "o carro do Peter → Peter's car",
         "text": "1. o celular da minha irmã → [my sister's phone|my sister's cell phone|my sister's cellphone]\n"
                 "2. o quarto dos meus filhos (2 filhos) → [my sons' bedroom|my sons' room|my children's bedroom|"
                 "my children's room|my kids' bedroom|my kids' room]\n"
                 "3. o cachorro do James → [James's dog|James' dog]"},
        {"type": "fill",
         "prompt": "Answer with 's.",
         "translation": "Responda com 's.",
         "example": "Whose hat is it? (Justin) → It's Justin's hat.",
         "text": "1. Whose bag is it? (Maria) → [It's Maria's bag.|It is Maria's bag.]\n"
                 "2. Whose shoes are these? (my brother) → [They're my brother's shoes.|They are my brother's shoes.|"
                 "These are my brother's shoes.]"},
        {"type": "free",
         "prompt": "Write about your family and things that belong to them. Use 's at least four times: "
                   "my mother's name, my brother's car, my parents' house…",
         "translation": "Escreva sobre a sua família e as coisas deles. Use 's pelo menos quatro vezes.",
         "example": "My mother's name is Rosa.",
         "model_answer": "My mother's name is Rosa and my father's name is João.\n"
                         "My parents' house is in Campinas. It's big and it has a garden.\n"
                         "My brother's car is red, and my sister's dog is very small.\n"
                         "My grandma's cake is the best cake in the world!",
         "keywords": ["mother's", "brother's", "sister's"], "min_words": 30, "points": 4},
    ],
}

AULA5_VIDEO = _video(5, AULA5_TOPIC, "Video — Whose is it?",
                     "a Sarah mostra as coisas da família dela: o carro do irmão, a casa dos pais, o cachorro da irmã…",
                     "aula5-video", [
    _q("Whose car is it?", "De quem é o carro?", "It's her brother's car.", "It's her brothers car.",
       "It's the car of her brother's.", "It's her brother car."),
    _q("How do we write \"a casa dos pais dela\"?", "Como escrevemos \"a casa dos pais dela\"?", "her parents' house",
       "her parent's house", "her parents's house", "her house parents"),
    _q("Whose dog is Toby?", "De quem é o Toby?", "Her sister's.", "Her sisters.", "Her sister.", "Sister's her."),
    _q("Which is correct?", "Qual está correto?", "my children's puppy", "my childrens' puppy", "my childrens puppy",
       "my children puppy"),
])

# ---------- Aula 06 — Possessive Adjectives & Possessive Pronouns (https://youtu.be/Xo0A1FzyA94) ----------

AULA6_TOPIC = "Aula 06 — Possessive Adjectives & Possessive Pronouns"

AULA6_FORMS = {
    "title": "My / mine, your / yours, her / hers…",
    "lesson": 6,
    "description": "TRÊS formas de falar de posse:\n"
                   "It's MY castle. (possessive ADJECTIVE) · It's MINE. (possessive PRONOUN) · It's Glinda's castle. ('s)\n"
                   "POSSESSIVE ADJECTIVE → SEMPRE com um substantivo depois: my car · your car · his house · her hair\n"
                   "  my · your · his · her · its · our · your · their\n"
                   "POSSESSIVE PRONOUN → NUNCA com substantivo depois; ele SUBSTITUI o substantivo (evita repetição):\n"
                   "  mine · yours · his · hers · its · ours · yours · theirs\n"
                   "This is my computer. → This computer is mine. (✗ This computer is my.)\n"
                   "Is this your laptop or mine? ✓",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the possessive adjectives to the possessive pronouns.",
         "translation": "Ligue cada possessive adjective ao possessive pronoun.",
         "example": "my → mine",
         "pairs": [
             {"left": "your", "right": "yours"},
             {"left": "his", "right": "his"},
             {"left": "her", "right": "hers"},
             {"left": "our", "right": "ours"},
             {"left": "their", "right": "theirs"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta (adjective + substantivo · pronoun sozinho).",
         "example": "This is [my] computer. · This computer is [mine].",
         "text": "1. This book is [*hers|her]. \n2. It's [*their|theirs] backpack.\n3. Is this your laptop or [*mine|my]?\n"
                 "4. [*Our|Ours] house is near the beach.\n5. These keys aren't [*yours|your].\n6. That's [*his|he] car."},
        {"type": "group",
         "prompt": "Adjective or pronoun? Put each word in the right group.",
         "translation": "Possessive adjective (precisa de substantivo) ou possessive pronoun (fica sozinho)?",
         "example": "my → adjective · mine → pronoun",
         "categories": ["possessive adjective", "possessive pronoun"],
         "words": [
             {"text": "your", "category": "possessive adjective"}, {"text": "her", "category": "possessive adjective"},
             {"text": "our", "category": "possessive adjective"}, {"text": "their", "category": "possessive adjective"},
             {"text": "yours", "category": "possessive pronoun"}, {"text": "hers", "category": "possessive pronoun"},
             {"text": "ours", "category": "possessive pronoun"}, {"text": "theirs", "category": "possessive pronoun"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Mine\" never comes before a noun. → True",
         "statements": [
             {"text": "We can say \"It's mine car\".", "answer": False, "translation": "Podemos dizer \"It's mine car\"."},
             {"text": "Possessive pronouns help us avoid repeating the noun.", "answer": True,
              "translation": "Os possessive pronouns nos ajudam a evitar repetir o substantivo."},
             {"text": "\"His\" is the same as adjective and as pronoun.", "answer": True,
              "translation": "\"His\" é igual como adjective e como pronoun."},
         ]},
    ],
}

AULA6_ANSWERS = {
    "title": "Four ways to answer \"Whose…?\"",
    "lesson": 6,
    "description": "Whose jacket is this? (é do Josh) → 4 respostas possíveis:\n"
                   "It's Josh's jacket. · It's Josh's. · It's his jacket. · It's his.\n"
                   "Whose t-shirt is this? (é da Sarah) → It's Sarah's t-shirt. · It's Sarah's. · It's her t-shirt. · It's hers.\n"
                   "PLURAL: Whose glasses are these? (são do Mike) → They're Mike's glasses. · They're Mike's. · "
                   "They're his glasses. · They're his.\n"
                   "(glasses é sempre plural → they're, não it's)",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Whose t-shirt is this? It belongs to Sarah. Complete the four answers.",
         "translation": "De quem é esta camiseta? É da Sarah. Complete as quatro respostas.",
         "example": "It's Sarah's t-shirt.",
         "text": "1. It's [Sarah's].\n2. It's [her] t-shirt.\n3. It's [hers]."},
        {"type": "dropdown",
         "prompt": "Whose glasses are these? They belong to Mike. Choose.",
         "translation": "De quem são estes óculos? São do Mike. Escolha (atenção ao plural!).",
         "example": "[They're] Mike's glasses.",
         "text": "1. [*They're|It's] Mike's glasses.\n2. They're [*Mike's|Mike].\n3. They're [*his|her] glasses.\n"
                 "4. They're [*his|him]."},
        {"type": "dropdown",
         "prompt": "Is this sentence correct?",
         "translation": "Esta frase está correta? (exercício da aula)",
         "example": "Those are John's keys. → [Correct]",
         "text": "1. This book is her. → [*Incorrect|Correct]\n2. Those are John's keys. → [*Correct|Incorrect]\n"
                 "3. It's theirs backpack. → [*Incorrect|Correct]\n4. Is this your laptop or mine? → [*Correct|Incorrect]\n"
                 "5. She is Sarahs' sister. → [*Incorrect|Correct]"},
        {"type": "fill",
         "prompt": "Replace the words in brackets with a possessive pronoun.",
         "translation": "Troque as palavras entre parênteses por um possessive pronoun.",
         "example": "This computer is (my computer). → This computer is mine.",
         "text": "1. That house is (our house). → That house is [ours].\n"
                 "2. These books are (her books). → These books are [hers].\n"
                 "3. The red car is (their car). → The red car is [theirs].\n"
                 "4. Is this phone (your phone)? → Is this phone [yours]?"},
    ],
}

AULA6_LISTENING = {
    "title": "Listening — after the party",
    "lesson": 6,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: her / hers e your / yours são parecidos — escute o S no final!",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"It's mine.\" → mine",
         "audio": f"{AUDIO}/aula6-words.m4a",
         "text": "1. It's [*hers|her].\n2. Is this [*yours|your]?\n3. That's [*our|ours] car.\n4. They're [*theirs|their].\n"
                 "5. It's [*his|he's] phone."},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"This book is hers.\" → This book is [hers].",
         "audio": f"{AUDIO}/aula6-dictation.m4a",
         "text": "1. Is this your laptop or [mine]?\n2. These keys are [ours].\n3. That isn't [their] house.\n"
                 "4. Whose jacket is this? It's [his]."},
        {"type": "info",
         "prompt": "Now listen: Paula and Rick clean up after a party.",
         "translation": "Agora ouça: a Paula e o Rick arrumam a casa depois de uma festa e encontram coisas dos convidados. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula6-party.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "They found things after the [party].",
         "text": "1. Whose sunglasses are they? → [*Julia's.|Paula's.|Rick's.]\n"
                 "2. Whose phone is it? → [*Rick's. It's his.|Marco's.|Paula's. It's hers.]\n"
                 "3. Whose scarf is it? → [*Paula's mother's.|Julia's.|The neighbors'.]\n"
                 "4. Whose dog is in the garden? → [*The neighbors'. It's theirs.|Marco's.|Rick's.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "There was a party at Paula and Rick's house. → True",
         "statements": [
             {"text": "Rick looked for his phone all morning.", "answer": True,
              "translation": "O Rick procurou o celular dele a manhã toda."},
             {"text": "The dog is Paula and Rick's dog.", "answer": False,
              "translation": "O cachorro é da Paula e do Rick."},
         ]},
    ],
}

AULA6_SPEAKING = {
    "title": "Speaking — mine, yours, hers…",
    "lesson": 6,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: their = \"dhér\" (com TH vozeado, língua entre os dentes) · theirs = \"dhérz\".",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita os possessivos da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula6-say-w{i}.m4a"} for i, t in enumerate(
             ["my, your, his, her", "its, our, your, their", "mine, yours, his, hers", "its, ours, yours, theirs"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases.",
         "example": "\"It's my castle. It's mine.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula6-say-s{i}.m4a"} for i, t in enumerate(
             ["It's my castle. It's mine.", "It's Josh's jacket. It's his jacket. It's his.",
              "It's Sarah's t-shirt. It's her t-shirt. It's hers.", "They're Mike's glasses. They're his.",
              "This book is hers.", "Is this your laptop or mine?"], 1)]},
    ],
}

AULA6_READING = {
    "title": "Reading — sharing a house",
    "lesson": 6,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto do Caio, que divide a casa com outros estudantes. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula6-reading.m4a",
         "text": "SHARING A HOUSE\n\n"
                 "I live with three friends in a big old house near our university.\n"
                 "My bedroom is small, but it's mine and I love it. Lara's bedroom is the biggest. Hers has a balcony!\n"
                 "Pedro and Davi share a bedroom. Theirs is always messy — clothes everywhere!\n"
                 "We share the kitchen. There's one rule: our food is on the shelves, and each person has a shelf. "
                 "The top shelf is mine, the second is Lara's…\n"
                 "Last week, someone ate my yogurt. I asked: \"Whose spoon is this?\" Pedro said: \"It's not mine!\" "
                 "But the spoon was his. Ha!\n"
                 "It's not always easy, but this house is ours, and we're like a family."},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "How many people live in the house? → [Four.]",
         "text": "1. Whose bedroom has a balcony? → [*Lara's.|Caio's.|Pedro's.]\n"
                 "2. Whose bedroom is always messy? → [*Pedro and Davi's.|Lara's.|Caio's.]\n"
                 "3. Whose shelf is the top shelf? → [*Caio's. It's his.|Lara's. It's hers.|Davi's.]\n"
                 "4. Whose spoon was it? → [*Pedro's.|Caio's.|Lara's.]"},
        {"type": "fill",
         "prompt": "Complete with a possessive pronoun, according to the text.",
         "translation": "Complete com um possessive pronoun, de acordo com o texto.",
         "example": "My bedroom is small, but it's [mine].",
         "text": "1. Lara's bedroom is the biggest. [Hers] has a balcony.\n"
                 "2. Pedro and Davi's bedroom is messy. [Theirs] is always messy.\n"
                 "3. This house is [ours]."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "They live near their university. → True",
         "statements": [
             {"text": "Pedro ate Caio's yogurt.", "answer": True, "translation": "O Pedro comeu o iogurte do Caio."},
             {"text": "Each person has a kitchen.", "answer": False, "translation": "Cada pessoa tem uma cozinha."},
         ]},
    ],
}

AULA6_WRITING = {
    "title": "Writing — it's mine!",
    "lesson": 6,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Adjective + substantivo: my bag, her phone, their house.\n"
                   "Pronoun sozinho: mine, yours, his, hers, ours, theirs (This bag is mine).",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Correct the mistakes.",
         "translation": "Corrija os erros.",
         "example": "This book is her. → This book is hers.",
         "text": "1. It's theirs backpack. → [It's their backpack.|It is their backpack.]\n"
                 "2. This phone is my. → [This phone is mine.]\n"
                 "3. Is this pen your? → [Is this pen yours?|Is this your pen?]"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Este computador é meu. → This computer is mine.",
         "text": "1. Esta bolsa é dela. → [This bag is hers.|This purse is hers.]\n"
                 "2. A casa deles é grande. → [Their house is big.]\n"
                 "3. Este carro é seu ou meu? → [Is this car yours or mine?|Is this your car or mine?]"},
        {"type": "free",
         "prompt": "Think about your house or your family. Write about things that are yours, your family's, and your "
                   "friends'. Use possessive adjectives AND possessive pronouns.",
         "translation": "Pense na sua casa ou família. Escreva sobre coisas que são suas, da sua família e dos seus amigos. "
                        "Use possessive adjectives e possessive pronouns.",
         "example": "My bedroom is small, but it's mine.",
         "model_answer": "My bedroom is small, but it's mine and I love it.\n"
                         "My sister's bedroom is bigger. Hers has a big window.\n"
                         "Our car is old. My neighbors' car is new; theirs is red.\n"
                         "My dog sleeps on my bed, and the cat sleeps on its own pillow.",
         "keywords": ["my", "mine", "hers", "our"], "min_words": 30, "points": 4},
    ],
}

AULA6_VIDEO = _video(6, AULA6_TOPIC, "Video — Moving day!",
                     "é dia de mudança! A Sarah diz de quem é cada coisa: ours, his, mine, hers.",
                     "aula6-video", [
    _q("Whose boxes are they?", "De quem são as caixas?", "They're ours.", "They're our.", "They're us.", "They're mine's."),
    _q("Complete: The books are her husband's. They're ___.", "Complete: os livros são do marido dela. São ___.", "his",
       "him", "he's", "hers"),
    _q("Whose lamp is it now?", "De quem é a luminária agora?", "It's Sarah's. It's hers.", "It's her daughter's.",
       "It's her husband's.", "It's the cat's."),
    _q("Complete: It's my daughter's cat. It's ___.", "Complete: é o gato da minha filha. É ___.", "hers", "her",
       "his", "she's"),
])

# ---------- Aula 07 — Object Pronouns (https://youtu.be/3qb8LySBxzA) ----------

AULA7_TOPIC = "Aula 07 — Object Pronouns"

AULA7_SUBJECT = {
    "title": "Subject pronouns: who does the action",
    "lesson": 7,
    "description": "SUBJECT PRONOUNS: I · you · he · she · it · we · you · they\n"
                   "Substituem pessoas, animais, objetos, lugares e situações e PRATICAM a ação → vêm ANTES do verbo.\n"
                   "The dog is sleeping. → IT is sleeping. · Mike and Jenny are friends. → THEY are friends.\n"
                   "Atenção 1: THEY é o plural de he, she E de IT → The books are on the table. → THEY are on the table.\n"
                   "Atenção 2: se o I está no grupo, é WE → Anna and I study English. → WE study English.\n"
                   "Atenção 3: you + outra pessoa = YOU (vocês) → You and Mark are in the same class. → YOU are in the same class.",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Replace the words in bold with a subject pronoun.",
         "translation": "Troque as palavras em destaque pelo subject pronoun certo (exercício da aula).",
         "example": "THE DOG is sleeping. → [It] is sleeping.",
         "text": "1. MIKE AND JENNY are friends. → [*They|We|He] are friends.\n"
                 "2. MY FATHER drives a truck. → [*He|It|She] drives a truck.\n"
                 "3. THE BOOKS are on the table. → [*They|It|We] are on the table.\n"
                 "4. ANNA AND I study English every day. → [*We|They|She] study English every day.\n"
                 "5. YOU AND MARK are in the same class. → [*You|They|We] are in the same class.\n"
                 "6. MY PHONE is new. → [*It|He|She] is new."},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "Subject pronouns come before the verb. → True",
         "statements": [
             {"text": "We use THEY only for people.", "answer": False, "translation": "Usamos THEY só para pessoas."},
             {"text": "\"My sister and I\" = we.", "answer": True, "translation": "\"My sister and I\" = we."},
             {"text": "Subject pronouns practice the action.", "answer": True,
              "translation": "Os subject pronouns praticam a ação."},
         ]},
    ],
}

AULA7_OBJECT = {
    "title": "Object pronouns: me, him, her, us, them",
    "lesson": 7,
    "description": "OBJECT PRONOUNS (pronomes oblíquos): me · you · him · her · it · us · you · them\n"
                   "Também substituem pessoas e coisas, mas NÃO praticam a ação: RECEBEM a ação → vêm DEPOIS do verbo "
                   "(ou depois de preposição: with them, for me, to her).\n"
                   "I → me · you → you · he → him · she → her · it → it · we → us · they → them\n"
                   "Sarah calls JOHN every day. → Sarah calls HIM every day.\n"
                   "My parents love MY BROTHER AND ME. → My parents love US.\n"
                   "Em inglês, não muda para masculino/feminino ou plural como \"o, a, os, as\": é bem mais fácil!\n"
                   "Usamos para não repetir: Do you have a favorite book? How often do you read IT?",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the subject pronouns to the object pronouns.",
         "translation": "Ligue cada subject pronoun ao object pronoun.",
         "example": "I → me",
         "pairs": [
             {"left": "he", "right": "him"},
             {"left": "she", "right": "her"},
             {"left": "we", "right": "us"},
             {"left": "they", "right": "them"},
             {"left": "it", "right": "it"},
         ]},
        {"type": "dropdown",
         "prompt": "Complete with the correct object pronoun.",
         "translation": "Complete com o object pronoun certo (exercício da aula).",
         "example": "Sarah calls JOHN every day. → Sarah calls [him] every day.",
         "text": "1. My parents love MY BROTHER AND ME. → My parents love [*us|we|them].\n"
                 "2. I can see THE CAT in the garden. → I can see [*it|him|them] in the garden.\n"
                 "3. Emily visits HER GRANDPARENTS on weekends. → Emily visits [*them|they|her] on weekends.\n"
                 "4. I don't know PETER. → I don't know [*him|he|his].\n"
                 "5. My sister always texts MY MOTHER. → My sister always texts [*her|she|hers]."},
        {"type": "dropdown",
         "prompt": "Subject or object pronoun?",
         "translation": "Subject pronoun (antes do verbo) ou object pronoun (depois do verbo)?",
         "example": "[She] loves [him].",
         "text": "1. [*He|Him] works with [*me|I].\n2. Can you help [*us|we]?\n3. [*They|Them] invited [*her|she] to the party.\n"
                 "4. I play soccer with [*them|they] on Sundays."},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu conheço ela. → I know her.",
         "text": "1. Ela liga para ele todos os dias. → [She calls him every day.]\n"
                 "2. Meus pais nos amam. → [My parents love us.]\n"
                 "3. Eu visito eles nos fins de semana. → [I visit them on weekends.|I visit them on the weekends.]"},
    ],
}

AULA7_LISTENING = {
    "title": "Listening — the new neighbor",
    "lesson": 7,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: os object pronouns são fracos e se ligam ao verbo: \"call him\" = \"cólim\", "
                   "\"love them\" = \"lâvdəm\".",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the pronoun you hear.",
         "translation": "Ouça e escolha o pronome que você ouve.",
         "example": "Você ouve: \"I love them.\" → them",
         "audio": f"{AUDIO}/aula7-words.m4a",
         "text": "1. Call [*him|her] later.\n2. Can you help [*us|them]?\n3. I don't know [*her|him].\n"
                 "4. We visit [*them|him] every Sunday.\n5. She texts [*me|him] every day."},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"Sarah calls him every day.\" → Sarah calls [him] every day.",
         "audio": f"{AUDIO}/aula7-dictation.m4a",
         "text": "1. My parents love [us].\n2. I can see [it] in the garden.\n3. Emily visits [them] on weekends.\n"
                 "4. I always play with [them]."},
        {"type": "info",
         "prompt": "Now listen: Clara tells her husband about the new neighbor.",
         "translation": "Agora ouça: a Clara conta para o marido sobre a nova vizinha. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula7-neighbor.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "The new neighbor's name is [Helen].",
         "text": "1. Where did Clara meet Helen? → [*At the elevator.|At the supermarket.|At the park.]\n"
                 "2. What does Helen have? → [*Two cats.|A dog.|Three children.]\n"
                 "3. What did Helen give Clara? → [*A cake.|Some flowers.|A book.]\n"
                 "4. When can they visit Helen? → [*On Saturday.|Tonight.|On Monday.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Helen is the new neighbor. → True",
         "statements": [
             {"text": "Clara's husband knows Helen.", "answer": False, "translation": "O marido da Clara conhece a Helen."},
             {"text": "Helen invited them to her apartment.", "answer": True,
              "translation": "A Helen convidou eles para o apartamento dela."},
         ]},
    ],
}

AULA7_SPEAKING = {
    "title": "Speaking — speaking time!",
    "lesson": 7,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: him, her e them perdem o H e o TH na fala rápida: \"call him\" = \"cólim\".",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita os object pronouns e as frases.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula7-say-s{i}.m4a"} for i, t in enumerate(
             ["me, you, him, her, it, us, you, them", "Sarah calls him every day.", "My parents love us.",
              "I can see it in the garden.", "Emily visits them on weekends.", "Yes, I do. I read it twice a year.",
              "Yes, I do. I always play with them."], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions from the lesson.",
         "translation": "Agora responda às perguntas do \"speaking time\" da aula, usando object pronouns.",
         "example": "\"Do you have a favorite book? How often do you read it?\" → \"Yes, I do. I read it once a year.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula7-say-y{i}.m4a"} for i, t in enumerate(
             ["Do you have a favorite book? How often do you read it?",
              "Do you have any pets? How often do you play with them?",
              "Do you have a car? Do you drive it very often?",
              "Do you call your parents? How often do you call them?"], 1)]},
    ],
}

AULA7_READING = {
    "title": "Reading — my best friend",
    "lesson": 7,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto do Lucas sobre o melhor amigo dele. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula7-reading.m4a",
         "text": "MY BEST FRIEND\n\n"
                 "My best friend is Felipe. I met him at school when we were seven.\n"
                 "Felipe has a big family: two sisters and a little brother. I love them! His mother makes amazing cakes, "
                 "and she always gives me a piece.\n"
                 "Now Felipe lives in Portugal. I miss him, but we talk every week. I call him on Sundays, or he calls me.\n"
                 "Last year, I visited him in Lisbon. He showed me the city, and his girlfriend, Inês, cooked for us. "
                 "I liked her a lot!\n"
                 "Felipe has an old guitar. He plays it every night. And me? I sing with him… badly!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Who is Lucas's best friend? → [Felipe.]",
         "text": "1. When did Lucas meet Felipe? → [*When they were seven.|Last year.|In Portugal.]\n"
                 "2. When does Lucas call Felipe? → [*On Sundays.|Every day.|On Fridays.]\n"
                 "3. Who cooked for them in Lisbon? → [*Inês.|Felipe's mother.|Felipe.]\n"
                 "4. What does Felipe play every night? → [*His old guitar.|Soccer.|Video games.]"},
        {"type": "dropdown",
         "prompt": "What does the pronoun mean in the text?",
         "translation": "A quem ou a que o pronome se refere no texto?",
         "example": "\"I met HIM at school.\" → [Felipe]",
         "text": "1. \"I love THEM!\" → [*Felipe's family|Felipe's cakes|the guitars]\n"
                 "2. \"…she always gives ME a piece.\" → [*Lucas|Felipe|Inês]\n"
                 "3. \"I liked HER a lot!\" → [*Inês|Felipe's mother|Felipe's sister]\n"
                 "4. \"He plays IT every night.\" → [*the guitar|the city|the cake]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Felipe lives in Portugal. → True",
         "statements": [
             {"text": "Lucas never talks to Felipe now.", "answer": False, "translation": "O Lucas nunca conversa com o Felipe agora."},
             {"text": "Lucas doesn't sing very well.", "answer": True, "translation": "O Lucas não canta muito bem."},
         ]},
    ],
}

AULA7_WRITING = {
    "title": "Writing — don't repeat, replace!",
    "lesson": 7,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Antes do verbo (sujeito): I, you, he, she, it, we, they.\n"
                   "Depois do verbo ou preposição (objeto): me, you, him, her, it, us, them.",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Rewrite the sentences. Replace the words in CAPITALS with a pronoun.",
         "translation": "Reescreva as frases trocando as palavras em MAIÚSCULAS por um pronome.",
         "example": "I don't know PETER. → I don't know him.",
         "text": "1. I visit MY GRANDMOTHER on Sundays. → [I visit her on Sundays.]\n"
                 "2. MY BROTHER AND I love pizza. → [We love pizza.]\n"
                 "3. She plays with THE DOGS every day. → [She plays with them every day.]"},
        {"type": "fill",
         "prompt": "Correct the mistakes.",
         "translation": "Corrija os erros.",
         "example": "I love she. → I love her.",
         "text": "1. Him is my teacher. → [He is my teacher.|He's my teacher.]\n"
                 "2. Can you help I? → [Can you help me?]\n"
                 "3. My friends invited we to the party. → [My friends invited us to the party.]"},
        {"type": "free",
         "prompt": "Write about a person you love (a friend or a family member). When did you meet him/her? "
                   "What do you do together? How often do you see or call him/her? Use object pronouns.",
         "translation": "Escreva sobre uma pessoa que você ama (amigo ou familiar): quando a conheceu, o que fazem juntos, "
                        "com que frequência se veem ou se falam. Use object pronouns.",
         "example": "My best friend is Carla. I met her at work.",
         "model_answer": "My best friend is Carla. I met her at work in 2019.\n"
                         "She is funny and kind. I call her every Friday, and she always helps me.\n"
                         "Carla has two dogs. I love them, and I walk with them in the park.\n"
                         "Her husband is nice too. We have dinner with him on Saturdays.",
         "keywords": ["her", "them", "him", "me"], "min_words": 30, "points": 4},
    ],
}


AULA7_VIDEO = _video(7, AULA7_TOPIC, "Video — People I love",
                      "a Sarah apresenta as pessoas (e o gatinho) que ela ama — com object pronouns.",
                      "aula7-video", [
    _q("Complete: I visit ___ every Sunday. (my grandparents)", "Complete: eu visito ___ todo domingo. (os avós)", "them", "they", "their", "him"),
    _q("Complete: I call ___ every day. (my brother)", "Complete: eu ligo para ___ todo dia. (o irmão)", "him", "he", "his", "her"),
    _q("Complete: I play with ___ every morning. (my kitten)", "Complete: eu brinco com ___ toda manhã. (o gatinho)", "it", "its", "them", "him"),
    _q("Complete: She always helps ___. (Sarah)", "Complete: ela sempre ajuda ___. (a Sarah)", "me", "I", "my", "mine"),
])

# ---------- Aula 08 — Be Going To for Plans (https://youtu.be/rHVfzHliuqk) ----------

AULA8_TOPIC = "Aula 08 — Be Going To for Plans"

AULA8_FORMS = {
    "title": "Be going to: plans and intentions",
    "lesson": 8,
    "description": "BE GOING TO = planos, intenções e decisões que você JÁ TINHA TOMADO antes de falar.\n"
                   "AFFIRMATIVE: sujeito + AM / IS / ARE + GOING TO + verbo na forma básica\n"
                   "  I'm going to relax a lot this weekend. · My sister is going to binge-watch series this Sunday. · "
                   "My friends are going to go to the beach on Saturday.\n"
                   "NEGATIVE: só o verbo to be na negativa → I'm not going to… · She isn't going to… · They aren't going to…\n"
                   "QUESTION: AM / IS / ARE + sujeito + going to + verbo? → Is your brother going to go to the beach? "
                   "Yes, he is. / No, he isn't.\n"
                   "Com question word: What are you going to do next weekend? → I'm going to go to the movies.\n"
                   "Atenção: My friends and I = we → My friends and I ARE going to play…",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the weekend plans to Portuguese.",
         "translation": "Ligue os planos de fim de semana da aula ao português.",
         "example": "go to the movies → ir ao cinema",
         "pairs": [
             {"left": "relax", "right": "descansar, relaxar"},
             {"left": "hang out with friends", "right": "sair com os amigos"},
             {"left": "binge-watch series", "right": "maratonar séries"},
             {"left": "walk in the park", "right": "caminhar no parque"},
             {"left": "visit my grandparents", "right": "visitar meus avós"},
             {"left": "have lunch with the family", "right": "almoçar em família"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose am, is or are.",
         "translation": "Escolha am, is ou are.",
         "example": "I [am] going to relax this weekend.",
         "text": "1. My sister [*is|are|am] going to binge-watch series this Sunday.\n"
                 "2. My friends [*are|is|am] going to go to the beach on Saturday.\n"
                 "3. I [*am|is|are] going to visit my grandparents.\n"
                 "4. My friends and I [*are|am|is] going to play soccer.\n"
                 "5. It [*is|are|am] going to be a very fun weekend."},
        {"type": "fill",
         "prompt": "Make the sentences negative.",
         "translation": "Passe para a negativa (só o verbo to be muda).",
         "example": "I'm going to relax this weekend. → I'm not going to relax this weekend.",
         "text": "1. My sister is going to study on Saturday. → [My sister isn't going to study on Saturday.|"
                 "My sister is not going to study on Saturday.]\n"
                 "2. My friends are going to travel to New York next month. → [My friends aren't going to travel to New York "
                 "next month.|My friends are not going to travel to New York next month.]"},
        {"type": "dropdown",
         "prompt": "Choose the right short answer.",
         "translation": "Escolha a resposta curta certa.",
         "example": "Are you going to study? (✓) → [Yes, I am.]",
         "text": "1. Is your brother going to go to the beach? (✓) → [*Yes, he is.|Yes, he does.|Yes, he goes.]\n"
                 "2. Are your friends going to travel? (✗) → [*No, they aren't.|No, they don't.|No, they not.]\n"
                 "3. Am I going to study a lot this weekend? (✓) → [*Yes, you are.|Yes, I do.|Yes, you going.]"},
    ],
}

AULA8_GONNA = {
    "title": "Questions and \"gonna\"",
    "lesson": 8,
    "description": "PERGUNTAS: (question word) + AM / IS / ARE + sujeito + GOING TO + verbo?\n"
                   "What are you going to do on Saturday? → On Saturday, I'm going to go to the movies.\n"
                   "What are you not going to do this weekend? → I'm not going to go to the beach, because it's very cold.\n"
                   "PRONÚNCIA: na fala, GOING TO vira GONNA → I'm gonna call you later. · She's gonna study tonight.\n"
                   "We SAY gonna (inglês falado natural) · We DON'T WRITE gonna (texto formal, e-mail, redação) → "
                   "escreva going to.",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (O que você vai fazer no próximo fim de semana?)",
         "example": "going / you / Are / to / study → Are you going to study?",
         "tokens": ["What", "are", "you", "going", "to", "do", "next", "weekend?"], "alternatives": []},
        {"type": "fill",
         "prompt": "Make questions with be going to.",
         "translation": "Faça perguntas com be going to.",
         "example": "your brother / go to the beach → Is your brother going to go to the beach?",
         "text": "1. you / visit your grandparents → [Are you going to visit your grandparents?]\n"
                 "2. she / study tonight → [Is she going to study tonight?]\n"
                 "3. what / they / do on Sunday → [What are they going to do on Sunday?]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Gonna\" is common in spoken English. → True",
         "statements": [
             {"text": "We use BE GOING TO for plans we made before the moment of speaking.", "answer": True,
              "translation": "Usamos BE GOING TO para planos feitos antes do momento da fala."},
             {"text": "We write \"gonna\" in a formal e-mail.", "answer": False,
              "translation": "Escrevemos \"gonna\" em um e-mail formal."},
             {"text": "\"I'm going to call you later\" is wrong; we must say \"gonna\".", "answer": False,
              "translation": "\"I'm going to call you later\" está errado; precisamos dizer \"gonna\"."},
             {"text": "After GOING TO, the verb is in the base form.", "answer": True,
              "translation": "Depois de GOING TO, o verbo fica na forma básica."},
         ]},
        {"type": "choice",
         "prompt": "Which sentence is correct?",
         "translation": "Qual frase está correta?",
         "example": "She's going to study tonight. ✓",
         "options": ["We're going to watch a movie tonight.", "We going to watch a movie tonight.",
                     "We're going to watching a movie tonight.", "We're go to watch a movie tonight."],
         "correct": 0},
    ],
}

AULA8_LISTENING = {
    "title": "Listening — Rachel's weekend plans",
    "lesson": 8,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: preste atenção nas contrações (I'm, we're) e no GONNA!",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"I'm gonna call you later.\" → I'm going to",
         "audio": f"{AUDIO}/aula8-words.m4a",
         "text": "1. [*I'm going to|I went to] travel.\n2. She [*isn't|is] going to study.\n3. [*We're|Were] going to relax.\n"
                 "4. [*Are|Is] they going to come?\n5. He's [*going to|going] cook."},
        {"type": "info",
         "prompt": "Listen to Rachel talking about her weekend plans.",
         "translation": "Ouça a Rachel falando dos planos dela para o fim de semana (o listening da aula). "
                        "Depois complete o texto abaixo.",
         "audio": f"{AUDIO}/aula8-rachel.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois complete o texto abaixo."},
        {"type": "fill",
         "prompt": "Listen again and complete Rachel's paragraph.",
         "translation": "Ouça de novo e complete o parágrafo da Rachel com going to + verbo.",
         "example": "On Saturday morning, I'm [going to visit] my grandparents.",
         "text": "This weekend, I have a lot of plans. On Saturday morning, I'm [going to visit] my grandparents. "
                 "We're [going to have] lunch together. In the afternoon, my friends and I are [going to play] volleyball "
                 "at the beach, and then we're [going to eat] açaí. On Sunday, I'm [going to clean] my apartment. "
                 "At night, my family and I are [going to watch] a movie. It's going to be a very fun weekend!"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the audio.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o áudio.",
         "example": "Rachel has a lot of plans. → True",
         "statements": [
             {"text": "Rachel is going to visit her grandparents on Sunday.", "answer": False,
              "translation": "A Rachel vai visitar os avós no domingo."},
             {"text": "She's going to play volleyball with her friends.", "answer": True,
              "translation": "Ela vai jogar vôlei com os amigos."},
             {"text": "She isn't going to clean her apartment.", "answer": False,
              "translation": "Ela não vai limpar o apartamento."},
         ]},
    ],
}

AULA8_SPEAKING = {
    "title": "Speaking — my weekend plans",
    "lesson": 8,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: tente falar \"gonna\": I'm gonna = \"aim gâna\".",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat (with \"gonna\").",
         "translation": "Ouça e repita (com \"gonna\", como na aula).",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula8-say-s{i}.m4a"} for i, t in enumerate(
             ["going to, gonna", "I'm going to call you later.", "She's going to study tonight.",
              "We are going to watch a movie.", "I'm going to relax a lot this weekend.",
              "My friends are going to go to the beach on Saturday."], 1)]},
        {"type": "speak",
         "prompt": "Speaking time: answer the questions from the lesson.",
         "translation": "Speaking time: responda às perguntas da aula sobre os SEUS planos.",
         "example": "\"What are you going to do on Saturday?\" → \"On Saturday, I'm going to go to the movies.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula8-say-y{i}.m4a"} for i, t in enumerate(
             ["What are you not going to do this weekend?", "What are you going to do on Saturday?",
              "What are you going to do on Sunday?", "Are you going to study English this week?"], 1)]},
    ],
}

AULA8_READING = {
    "title": "Reading — our big trip",
    "lesson": 8,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto do Rodrigo sobre a viagem que a família dele já planejou. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula8-reading.m4a",
         "text": "OUR BIG TRIP\n\n"
                 "We have big plans for July! My wife, my two kids and I are going to travel to Chile.\n"
                 "We bought the tickets last month. We're going to fly to Santiago on July 10th.\n"
                 "In Santiago, we're going to stay at a small hotel downtown. My wife is going to visit the museums — "
                 "she loves art. The kids are going to see snow for the first time in the mountains!\n"
                 "I'm going to try the famous Chilean food. And we aren't going to rent a car: "
                 "we're going to use the subway.\n"
                 "We aren't going to stay long — only eight days — but it's going to be amazing!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Where are they going to travel? → [To Chile.]",
         "text": "1. When are they going to fly? → [*On July 10th.|In June.|Next week.]\n"
                 "2. Where are they going to stay? → [*At a small hotel downtown.|At a friend's house.|In the mountains.]\n"
                 "3. What are the kids going to do? → [*See snow in the mountains.|Visit museums.|Rent a car.]\n"
                 "4. How long are they going to stay? → [*Eight days.|Two weeks.|One month.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "They bought the tickets last month. → True",
         "statements": [
             {"text": "They are going to rent a car.", "answer": False, "translation": "Eles vão alugar um carro."},
             {"text": "Rodrigo's wife is going to visit museums.", "answer": True,
              "translation": "A esposa do Rodrigo vai visitar museus."},
         ]},
        {"type": "fill",
         "prompt": "Complete according to the text.",
         "translation": "Complete de acordo com o texto.",
         "example": "We're going to [fly] to Santiago.",
         "text": "1. My wife [is] going to visit the museums.\n2. We [aren't] going to rent a car.\n"
                 "3. I'm going to [try] the famous Chilean food."},
    ],
}

AULA8_WRITING = {
    "title": "Writing — my plans for the weekend",
    "lesson": 8,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ am / is / are + going to + verbo (na escrita, sempre GOING TO — não \"gonna\").\n"
                   "Use o parágrafo da Rachel como modelo, como a professora sugeriu.",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu vou relaxar muito. → I'm going to relax a lot.",
         "text": "1. Minha irmã vai maratonar séries no domingo. → [My sister is going to binge-watch series on Sunday.|"
                 "My sister's going to binge-watch series on Sunday.|My sister is going to binge watch series on Sunday.]\n"
                 "2. Nós não vamos estudar no sábado. → [We aren't going to study on Saturday.|"
                 "We are not going to study on Saturday.|We're not going to study on Saturday.]"},
        {"type": "fill",
         "prompt": "Write \"gonna\" sentences in the formal way.",
         "translation": "Reescreva as frases faladas com \"gonna\" do jeito formal (escrito).",
         "example": "I'm gonna call you. → I'm going to call you.",
         "text": "1. She's gonna study tonight. → [She's going to study tonight.|She is going to study tonight.]\n"
                 "2. We're gonna watch a movie. → [We're going to watch a movie.|We are going to watch a movie.]"},
        {"type": "free",
         "prompt": "What are you going to do on the weekend? Write a paragraph about your plans, like Rachel's paragraph. "
                   "Include one thing you aren't going to do.",
         "translation": "O que você vai fazer no fim de semana? Escreva um parágrafo sobre os seus planos, como o da Rachel. "
                        "Inclua uma coisa que você NÃO vai fazer.",
         "example": "This weekend, I have a lot of plans.",
         "model_answer": "This weekend, I have a lot of plans.\n"
                         "On Saturday morning, I'm going to walk in the park with my dog.\n"
                         "In the afternoon, I'm going to hang out with my friends.\n"
                         "On Sunday, my family and I are going to have lunch together.\n"
                         "I'm not going to study, because I need to relax!",
         "keywords": ["going to", "I'm going to", "not going to"], "min_words": 30, "points": 4},
    ],
}


AULA8_VIDEO = _video(8, AULA8_TOPIC, "Video — My weekend plans",
                      "o Bruno conta os planos dele para o fim de semana com be going to.",
                      "aula8-video", [
    _q("What's Bruno going to do on Saturday morning?", "O que o Bruno vai fazer no sábado de manhã?", "He's going to walk in the park.", "He's going to go to the beach.", "He's going to study.", "He's going to sleep."),
    _q("Complete: My friends and I ___ going to go to the beach.", "Complete: meus amigos e eu ___ going to ir à praia.", "are", "am", "is", "be"),
    _q("Who are they going to have lunch with on Sunday?", "Com quem eles vão almoçar no domingo?", "With his grandparents.", "With his friends.", "With his boss.", "Alone."),
    _q("What's his sister going to do?", "O que a irmã dele vai fazer?", "Binge-watch series and eat chocolate.", "Go to the beach.", "Walk in the park.", "Cook lasagna."),
])

# ---------- Aula 09 — Be Going To for Predictions (https://youtu.be/_BLchqyoorU) ----------

AULA9_TOPIC = "Aula 09 — Be Going To for Predictions"

AULA9_EVIDENCE = {
    "title": "Look! It's going to rain!",
    "lesson": 9,
    "description": "BE GOING TO também serve para PREVISÕES baseadas em EVIDÊNCIAS: você VÊ algo agora e prevê o que vai acontecer.\n"
                   "Look at the sky! It's going to rain. · Look at the cars! They're going to crash. · "
                   "Look at her! She's going to sleep.\n"
                   "Estrutura: sujeito + am / is / are + going to + verbo (forma básica) · na fala: gonna → He's gonna fall.\n"
                   "Os 3 usos do going to:\n"
                   "1. PLANOS: I'm going to study English next year.\n"
                   "2. PREVISÃO com evidência: Look at the clouds. It's going to rain.\n"
                   "3. Algo PRESTES a acontecer: Let's have a break. Lunch is going to be ready in five minutes.",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Look at the evidence. Match it to the prediction.",
         "translation": "Ligue a evidência (o que você vê) à previsão.",
         "example": "Look at the sky! → It's going to rain.",
         "pairs": [
             {"left": "The cars are very fast and very close!", "right": "They're going to crash."},
             {"left": "She's reading, and her eyes are closing.", "right": "She's going to sleep."},
             {"left": "He's on the edge of the roof.", "right": "He's going to fall."},
             {"left": "He's driving and looking at his phone.", "right": "He's going to have an accident."},
             {"left": "They have rings and a big cake.", "right": "They're going to get married."},
         ]},
        {"type": "group",
         "prompt": "Plan, prediction or about to happen? Put each sentence in the right group.",
         "translation": "Plano, previsão com evidência ou algo prestes a acontecer? Coloque cada frase no grupo certo.",
         "example": "I'm going to study English next year. → plan",
         "categories": ["plan", "prediction (evidence)", "about to happen"],
         "words": [
             {"text": "I'm going to study English next year.", "category": "plan"},
             {"text": "We're going to visit Grandma on Sunday.", "category": "plan"},
             {"text": "Look at the clouds. It's going to rain.", "category": "prediction (evidence)"},
             {"text": "Be careful! You're going to fall!", "category": "prediction (evidence)"},
             {"text": "Lunch is going to be ready in five minutes.", "category": "about to happen"},
             {"text": "Hurry! The train is going to leave!", "category": "about to happen"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta.",
         "example": "Look at the sky! It's [going to rain].",
         "text": "1. Look at the cars! They're going to [*crash|crashing|crashed].\n"
                 "2. Look at him! He [*'s going to fall|going to fall|are going to fall].\n"
                 "3. The lions are near the zebra. It [*'s going to die|is going die|going to dying].\n"
                 "4. Look at that man! He [*isn't going to jump|not going to jump|doesn't going to jump]. He's too scared!"},
    ],
}

AULA9_FUTURE = {
    "title": "Predictions: the world in 20 years",
    "lesson": 9,
    "description": "Para fazer previsões e dar opinião sobre o futuro: I think + going to.\n"
                   "I think we're going to travel to the moon very often. · I don't think people are going to use cash.\n"
                   "Negativa: isn't / aren't going to · Pergunta: Is it going to rain? → Yes, it is. / No, it isn't.\n"
                   "Na fala: gonna → It's gonna rain. · They're gonna get married.\n"
                   "Vocabulário: crash (bater, colidir) · fall (cair) · jump (pular) · get married (casar-se) · "
                   "have an accident (sofrer um acidente) · be ready (ficar pronto)",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Make predictions with be going to.",
         "translation": "Faça previsões com be going to, usando o verbo entre parênteses.",
         "example": "Look at the clouds. (rain) → It's going to rain.",
         "text": "1. He's driving very fast. (have an accident) → He's [going to have] an accident.\n"
                 "2. They have rings! (get married) → They're [going to get] married.\n"
                 "3. She's very tired. (sleep) → She's [going to sleep].\n"
                 "4. Look! The glass is on the edge of the table. (fall) → It's [going to fall]."},
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras em ordem. (Eu acho que nós vamos viajar para a lua com frequência.)",
         "example": "rain / to / It's / going → It's going to rain.",
         "tokens": ["I", "think", "we're", "going", "to", "travel", "to", "the", "moon", "very", "often."],
         "alternatives": []},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "We can use BE GOING TO for predictions. → True",
         "statements": [
             {"text": "We use BE GOING TO for predictions based on evidence in the present.", "answer": True,
              "translation": "Usamos BE GOING TO para previsões baseadas em evidências do presente."},
             {"text": "\"Crash\" means \"cair\".", "answer": False, "translation": "\"Crash\" significa \"cair\"."},
             {"text": "\"Lunch is going to be ready in five minutes\" talks about something that is about to happen.",
              "answer": True, "translation": "\"Lunch is going to be ready in five minutes\" fala de algo prestes a acontecer."},
         ]},
        {"type": "choice",
         "prompt": "You see dark clouds and hear thunder. What do you say?",
         "translation": "Você vê nuvens escuras e ouve trovões. O que você fala?",
         "example": "Evidência no presente → be going to",
         "options": ["Look at the sky! It's going to rain.", "Look at the sky! It going to rain.",
                     "Look at the sky! It's going rain.", "Look at the sky! It's going to rains."],
         "correct": 0},
    ],
}

AULA9_LISTENING = {
    "title": "Listening — what's going to happen?",
    "lesson": 9,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: na fala rápida, going to = \"gonna\": It's gonna rain.",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the prediction.",
         "translation": "Ouça a situação e escolha a previsão que você ouve.",
         "example": "Você ouve: \"Look at the sky! It's going to rain.\" → rain",
         "audio": f"{AUDIO}/aula9-predictions.m4a",
         "text": "1. It's going to [*rain|snow].\n2. They're going to [*crash|stop].\n3. She's going to [*fall|jump].\n"
                 "4. He's going to [*be late|be early].\n5. The baby is going to [*cry|sleep]."},
        {"type": "info",
         "prompt": "Now listen: Bia and her dad are at the beach.",
         "translation": "Agora ouça: a Bia e o pai estão na praia, e muita coisa está prestes a acontecer! "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula9-beach.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Bia and her dad are at the [beach].",
         "text": "1. Why is it going to rain? → [*There are dark clouds.|The radio said so.|It's winter.]\n"
                 "2. What's the dog going to do? → [*Eat their sandwiches.|Swim.|Sleep.]\n"
                 "3. Why is Dad going to get a sunburn? → [*He has no sunscreen.|He's swimming.|He's sleeping.]\n"
                 "4. What are they going to do now? → [*Go home.|Have lunch at the beach.|Swim.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "They are at the beach. → True",
         "statements": [
             {"text": "The sky is blue and sunny.", "answer": False, "translation": "O céu está azul e ensolarado."},
             {"text": "The dog belongs to Bia.", "answer": False, "translation": "O cachorro é da Bia."},
             {"text": "Dad's back is very red.", "answer": True, "translation": "As costas do pai estão bem vermelhas."},
         ]},
    ],
}

AULA9_SPEAKING = {
    "title": "Speaking — make predictions",
    "lesson": 9,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: It's gonna = \"itsgâna\" · He's gonna = \"hizgâna\".",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the predictions.",
         "translation": "Ouça e repita as previsões da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula9-say-s{i}.m4a"} for i, t in enumerate(
             ["Look at the sky! It's going to rain.", "Look at the cars! They're going to crash.",
              "Look at her! She's going to sleep.", "He's gonna fall.", "They're gonna get married.",
              "Lunch is going to be ready in five minutes."], 1)]},
        {"type": "speak",
         "prompt": "Speaking time: the world in 20 years.",
         "translation": "Speaking time: o que você acha que vai acontecer no mundo daqui a 20 anos? Responda com going to.",
         "example": "\"I think we're going to travel to the moon very often.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula9-say-y{i}.m4a"} for i, t in enumerate(
             ["What's going to happen with cars in 20 years?", "Are people going to work at home?",
              "Are we going to travel to the moon?", "What's going to happen with your city?"], 1)]},
    ],
}

AULA9_READING = {
    "title": "Reading — the soccer final",
    "lesson": 9,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto do Marcos, que está assistindo à final do campeonato na TV com a família. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula9-reading.m4a",
         "text": "THE SOCCER FINAL\n\n"
                 "It's Sunday, and we're watching the final on TV. It's 1 to 1, and there are only two minutes left!\n"
                 "Look! Our best player has the ball. He's running very fast… He's going to score!\n"
                 "Oh, no! The goalkeeper is going to catch the ball… No! It's a goal! We're going to win!\n"
                 "My dad is standing on the sofa. He's going to fall! My mom is looking at him. She's going to be angry.\n"
                 "And my little brother has a big glass of juice in his hand, and he's jumping. "
                 "He's going to drop it on the carpet!\n"
                 "It's a crazy day. But tonight, the whole city is going to celebrate!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "What are they watching? → [The soccer final.]",
         "text": "1. What's the score at the beginning? → [*1 to 1.|2 to 1.|0 to 0.]\n"
                 "2. Why is Dad going to fall? → [*He's standing on the sofa.|He's running.|He's tired.]\n"
                 "3. Why is Mom going to be angry? → [*Dad is standing on the sofa.|They lost the game.|The TV broke.]\n"
                 "4. What's the brother going to drop? → [*His glass of juice.|The ball.|His phone.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "It's Sunday. → True",
         "statements": [
             {"text": "Their team scored a goal.", "answer": True, "translation": "O time deles fez um gol."},
             {"text": "The city isn't going to celebrate.", "answer": False, "translation": "A cidade não vai comemorar."},
         ]},
        {"type": "fill",
         "prompt": "Complete the predictions from the text.",
         "translation": "Complete as previsões do texto.",
         "example": "He's going to [score]!",
         "text": "1. We're going to [win]!\n2. My dad is going to [fall].\n3. The whole city is going to [celebrate]."},
    ],
}

AULA9_WRITING = {
    "title": "Writing — the world in 20 years",
    "lesson": 9,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Previsão: (I think) + sujeito + am / is / are + going to + verbo.\n"
                   "Negativa: isn't / aren't going to · I don't think… going to…",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Vai chover. → It's going to rain.",
         "text": "1. Olha os carros! Eles vão bater. → [Look at the cars! They're going to crash.|"
                 "Look at the cars! They are going to crash.]\n"
                 "2. Eles vão se casar. → [They're going to get married.|They are going to get married.]\n"
                 "3. Ele não vai pular. → [He isn't going to jump.|He's not going to jump.|He is not going to jump.]"},
        {"type": "free",
         "prompt": "Try to guess what is going to happen in the world in 20 years. Write at least five predictions "
                   "with be going to (affirmative and negative).",
         "translation": "Tente adivinhar o que vai acontecer no mundo daqui a 20 anos. Escreva pelo menos cinco previsões "
                        "com be going to (afirmativas e negativas). Exercício da aula!",
         "example": "I think we're going to travel to the moon very often.",
         "model_answer": "I think we're going to travel to the moon very often.\n"
                         "Cars are going to drive without people.\n"
                         "People aren't going to use cash; they're going to pay with their phones.\n"
                         "Robots are going to clean our houses.\n"
                         "I think the summers are going to be very hot.",
         "keywords": ["going to", "aren't going to", "I think"], "min_words": 30, "points": 4},
    ],
}


AULA9_VIDEO = _video(9, AULA9_TOPIC, "Video — What's going to happen?",
                      "a Sarah olha as cenas e faz previsões com base no que está vendo.",
                      "aula9-video", [
    _q("What's going to happen?", "O que vai acontecer?", "It's going to rain.", "It's going to snow.", "It's sunny.", "It's going rain."),
    _q("What are they going to do?", "O que eles vão fazer?", "They're going to get married.", "They're going to crash.", "They're going to sleep.", "They going to marry."),
    _q("Is the boy going to fall?", "O menino vai cair?", "No, he isn't. His dad is helping him.", "Yes, he is.", "No, he doesn't.", "Yes, he going."),
    _q("What's the dog going to do?", "O que o cachorro vai fazer?", "He's going to eat everything.", "He's going to sleep.", "He's going to run.", "He's going to swim."),
])

# ---------- Aula 10 — Will for Predictions (https://youtu.be/L_ecO_pey4o) ----------

AULA10_TOPIC = "Aula 10 — Will for Predictions"

AULA10_WILL = {
    "title": "Will: forms and contractions",
    "lesson": 10,
    "description": "WILL também fala do futuro. Para PREVISÕES, usamos will mais para dar a nossa OPINIÃO (sem evidência).\n"
                   "(No dia a dia, as pessoas misturam will e going to — os dois indicam futuro e você será entendido!)\n"
                   "AFFIRMATIVE: sujeito + WILL + verbo na forma básica (igual para todos): You will pass the exam.\n"
                   "  Contração só com subject pronoun: I'll · you'll · he'll · she'll · it'll · we'll · they'll → It'll rain tomorrow.\n"
                   "  Com nome não contrai na escrita: Lisa will travel tomorrow.\n"
                   "NEGATIVE: WILL NOT = WON'T (mais comum): It won't rain tomorrow. · You won't pass the exam.\n"
                   "QUESTION: WILL + sujeito + verbo? (sem contração) → Will she pass the exam? Yes, she will. / No, she won't.\n"
                   "Pronúncia: o 'LL tem som de L (ponta da língua atrás dos dentes): I'll = \"ául\".",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta.",
         "example": "It [will rain] tomorrow.",
         "text": "1. You [*will pass|will passed|will to pass] the exam because you studied a lot.\n"
                 "2. It [*won't|willn't|doesn't will] rain tomorrow.\n"
                 "3. [*Will she|She will|Will she to] pass the exam?\n"
                 "4. Yes, she [*will|'ll|does].\n"
                 "5. They [*'ll|will to|wills] pass the exam."},
        {"type": "dropdown",
         "prompt": "Can we use a contraction? Choose.",
         "translation": "Podemos usar contração? Escolha a forma certa (exercício da aula).",
         "example": "I think they [’ll] lose the match.",
         "text": "1. I think [*they'll|they will'] lose the match.\n"
                 "2. [*Will the meeting|'ll the meeting|The meeting'll] be long?\n"
                 "3. She [*won't|will'nt|willn't] get the job. She's not qualified.\n"
                 "4. [*Will you|You'll] see him at home later?\n"
                 "5. [*You'll|Will you'll] find a good job, I'm sure."},
        {"type": "fill",
         "prompt": "Write the contraction.",
         "translation": "Escreva a contração.",
         "example": "I will → I'll",
         "text": "1. you will → [you'll]\n2. she will → [she'll]\n3. it will → [it'll]\n4. we will → [we'll]\n"
                 "5. will not → [won't]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Won't\" means \"will not\". → True",
         "statements": [
             {"text": "We can contract WILL in questions: \"'ll it rain?\"", "answer": False,
              "translation": "Podemos contrair WILL em perguntas: \"'ll it rain?\""},
             {"text": "WILL is the same for all subjects.", "answer": True, "translation": "WILL é igual para todos os sujeitos."},
             {"text": "In everyday English, people often use will and going to with the same meaning.", "answer": True,
              "translation": "No inglês do dia a dia, as pessoas usam will e going to com o mesmo sentido muitas vezes."},
         ]},
    ],
}

AULA10_MURPHY = {
    "title": "Murphy's law: what will happen?",
    "lesson": 10,
    "description": "Optimist (otimista) × pessimist (pessimista): I'm an optimist. / I'm a pessimist.\n"
                   "MURPHY'S LAW (lei de Murphy): \"If something can go wrong, it will go wrong.\" — se algo pode dar errado, "
                   "vai dar errado!\n"
                   "If you change lines, the old line will start moving and the new one will stop.\n"
                   "If you leave your umbrella at home, it will start raining.\n"
                   "Previsões de opinião: I think you'll have a nice weekend. · Do you think you'll live to be a hundred?",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Murphy's law: what will happen?",
         "translation": "Lei de Murphy: o que vai acontecer? (as situações da aula)",
         "example": "If you leave the umbrella at home… → [it will start raining.]",
         "text": "1. You change to another line at the supermarket… → [*the old line will start moving and the new one "
                 "will stop.|the new line will move fast.]\n"
                 "2. A car is far away and the light is green. When it gets to the traffic light… → "
                 "[*the light will turn red.|the light will stay green.]\n"
                 "3. She leaves the umbrella at home and there are dark clouds… → [*it will start raining.|it will stay sunny.]\n"
                 "4. He drops the bread with butter… → [*it will fall with the butter side down.|"
                 "it will fall with the butter side up.]"},
        {"type": "match",
         "prompt": "Match the sentences from the lesson.",
         "translation": "Ligue as partes das frases da aula de pronúncia.",
         "example": "I'll be late → for work.",
         "pairs": [
             {"left": "You'll break", "right": "your leg."},
             {"left": "He'll win", "right": "the match."},
             {"left": "She'll miss", "right": "the train."},
             {"left": "We'll go", "right": "on holiday."},
             {"left": "They'll pass", "right": "the exam."},
         ]},
        {"type": "fill",
         "prompt": "Write sentences with will or won't. Use contractions where you can.",
         "translation": "Escreva frases com will ou won't. Use contrações quando possível.",
         "example": "(+) I think / they / lose the match → I think they'll lose the match.",
         "text": "1. (–) you / like that book → [You won't like that book.|You will not like that book.]\n"
                 "2. (–) it / be easy to pass → [It won't be easy to pass.|It will not be easy to pass.]\n"
                 "3. (?) the meeting / be long → [Will the meeting be long?]"},
        {"type": "choice",
         "prompt": "Which sentence is correct?",
         "translation": "Qual frase está correta?",
         "example": "It'll rain tomorrow. ✓",
         "options": ["Will it rain tomorrow?", "'ll it rain tomorrow?", "Will it rains tomorrow?", "It will rain tomorrow?"],
         "correct": 0},
    ],
}

AULA10_LISTENING = {
    "title": "Listening — the fortune teller",
    "lesson": 10,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: o 'LL é só um L no final do pronome: \"you'll\" = \"iúl\". Won't = \"wôunt\" (não confunda com want!).",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"I'll be late.\" → I'll",
         "audio": f"{AUDIO}/aula10-words.m4a",
         "text": "1. [*I'll|I] be late for work.\n2. You [*won't|want] like it.\n3. [*She'll|She] miss the train.\n"
                 "4. [*It'll|It] rain tomorrow.\n5. [*We'll|We] go on holiday."},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"You'll pass the exam.\" → [You'll] pass the exam.",
         "audio": f"{AUDIO}/aula10-dictation.m4a",
         "text": "1. [You'll] break your leg.\n2. He'll [win] the match.\n3. She [won't] get the job.\n"
                 "4. [Will] the meeting be long?"},
        {"type": "info",
         "prompt": "Now listen: Paulo visits a fortune teller.",
         "translation": "Agora ouça: o Paulo visita uma cartomante que faz previsões sobre o futuro dele. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula10-fortune.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Paulo visits a [fortune teller].",
         "text": "1. Where will Paulo travel? → [*To Italy.|To Japan.|To Canada.]\n"
                 "2. Who will he meet there? → [*A beautiful woman.|An old friend.|His boss.]\n"
                 "3. Will he be rich? → [*No, he won't.|Yes, he will.|She doesn't know.]\n"
                 "4. What will happen tomorrow? → [*He'll lose his wallet.|He'll find money.|He'll get a new job.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Paulo is an optimist. → True",
         "statements": [
             {"text": "Paulo will get a new job next month.", "answer": True,
              "translation": "O Paulo vai conseguir um emprego novo no mês que vem."},
             {"text": "Paulo is happy at the end.", "answer": False, "translation": "O Paulo fica feliz no final."},
         ]},
    ],
}

AULA10_SPEAKING = {
    "title": "Speaking — I'll, you'll, he'll…",
    "lesson": 10,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: no 'LL, a ponta da língua toca atrás dos dentes de cima: \"ául\", \"iúl\", \"híul\".",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat (pronunciation practice from the lesson).",
         "translation": "Ouça e repita (o exercício de pronúncia da aula).",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula10-say-s{i}.m4a"} for i, t in enumerate(
             ["I'll. I'll be late. I'll be late for work.", "You'll. You'll break. You'll break your leg.",
              "He'll. He'll win. He'll win the match.", "She'll. She'll miss. She'll miss the train.",
              "It'll. It'll rain. It'll rain tomorrow.", "We'll. We'll go. We'll go on holiday.",
              "They'll. They'll pass. They'll pass the exam."], 1)]},
        {"type": "speak",
         "prompt": "Are you a positive thinker? Answer the questions.",
         "translation": "Você é uma pessoa positiva? Responda às perguntas da aula com will / won't.",
         "example": "\"Do you think you'll have a nice weekend?\" → \"Yes, I do. I think I'll have a nice weekend.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula10-say-y{i}.m4a"} for i, t in enumerate(
             ["Do you think you'll have a nice weekend?", "Do you think you'll have a better job in the future?",
              "Do you think you'll make some new friends this year?", "Do you think you'll live to be a hundred?",
              "Do you think you'll read more than one book this year?"], 1)]},
    ],
}

AULA10_READING = {
    "title": "Reading — life in 2050",
    "lesson": 10,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça as opiniões de três pessoas sobre como será a vida em 2050. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula10-reading.m4a",
         "text": "LIFE IN 2050: WHAT DO YOU THINK?\n\n"
                 "CARLA (optimist): \"I think life will be better. People will live to be 120, and doctors will cure many "
                 "diseases. We'll work only four days a week!\"\n"
                 "JOSÉ (pessimist): \"I don't think it'll be better. The summers will be very hot, and there won't be "
                 "enough water. Robots will do our jobs, so a lot of people won't have work.\"\n"
                 "AMANDA: \"I'm not sure. Maybe cars will fly, and we'll travel to Mars on vacation. But I think people "
                 "will still love pizza and soccer. Some things will never change!\""},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Who is the optimist? → [Carla.]",
         "text": "1. How long will people live, according to Carla? → [*To 120.|To 100.|To 80.]\n"
                 "2. What does José think about water? → [*There won't be enough.|There will be a lot.|It will be free.]\n"
                 "3. Who thinks cars will fly? → [*Amanda.|José.|Carla.]\n"
                 "4. What will never change, for Amanda? → [*People will love pizza and soccer.|The weather.|Our jobs.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "José is a pessimist. → True",
         "statements": [
             {"text": "Carla thinks we'll work only four days a week.", "answer": True,
              "translation": "A Carla acha que vamos trabalhar só quatro dias por semana."},
             {"text": "José thinks robots will create more jobs.", "answer": False,
              "translation": "O José acha que os robôs vão criar mais empregos."},
         ]},
        {"type": "fill",
         "prompt": "Complete with will or won't, according to the text.",
         "translation": "Complete com will ou won't, de acordo com o texto.",
         "example": "Life [will] be better. (Carla)",
         "text": "1. Doctors [will] cure many diseases. (Carla)\n2. There [won't] be enough water. (José)\n"
                 "3. A lot of people [won't] have work. (José)"},
    ],
}

AULA10_WRITING = {
    "title": "Writing — are you a positive thinker?",
    "lesson": 10,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ I think + sujeito + will ('ll) + verbo · I don't think + … will…\n"
                   "Negativa: won't · Pergunta: Will you…? → Yes, I will. / No, I won't.",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Vai chover amanhã. → It'll rain tomorrow.",
         "text": "1. Você vai passar na prova. → [You'll pass the exam.|You will pass the exam.|You'll pass the test.|"
                 "You will pass the test.]\n"
                 "2. Não vai ser fácil. → [It won't be easy.|It will not be easy.]\n"
                 "3. Ela vai conseguir o emprego? → [Will she get the job?]"},
        {"type": "free",
         "prompt": "Answer the questions from the lesson with complete sentences: Do you think you'll have a nice "
                   "weekend? A better job in the future? New friends this year? Will you live to be a hundred? "
                   "Are you an optimist or a pessimist?",
         "translation": "Responda às perguntas da aula com frases completas, usando will e won't.",
         "example": "Yes, I do. I think I'll have a nice weekend.",
         "model_answer": "I'm an optimist!\n"
                         "I think I'll have a nice weekend, because I'm going to visit my parents.\n"
                         "I think I'll have a better job in the future.\n"
                         "I'll make some new friends this year at my English course.\n"
                         "But I don't think I'll live to be a hundred. I won't exercise enough!",
         "keywords": ["I'll", "I think", "won't"], "min_words": 30, "points": 4},
    ],
}


AULA10_VIDEO = _video(10, AULA10_TOPIC, "Video — Life in 2050",
                      "a Sarah, otimista, faz previsões com will sobre a vida em 2050.",
                      "aula10-video", [
    _q("What will robots do, for Sarah?", "O que os robôs vão fazer, para a Sarah?", "They'll do a lot of our jobs.", "They won't work.", "They'll travel to Mars.", "They'll cook pizza."),
    _q("Complete: Cities ___ be so polluted.", "Complete: as cidades ___ tão poluídas.", "won't", "willn't", "don't will", "not will"),
    _q("Will it be expensive to travel to Mars?", "Vai ser caro viajar para Marte?", "Yes, it will.", "Yes, it'll.", "No, it won't.", "Yes, it does."),
    _q("How long will people live?", "Até que idade as pessoas vão viver?", "To 120.", "To 100.", "To 80.", "To 200."),
])

# ---------- Aula 11 — Will for Offers, Promises and Decisions (https://youtu.be/RPfRuqFlV6k) ----------

AULA11_TOPIC = "Aula 11 — Will for Offers, Promises and Decisions"

AULA11_USES = {
    "title": "Will: promises, offers and instant decisions",
    "lesson": 11,
    "description": "Além de previsões, usamos WILL para:\n"
                   "PROMISES (promessas): I'll love you forever. · I'll change, I promise.\n"
                   "OFFERS (oferecer ajuda): I'll help you with your homework. · I'll help you when I finish.\n"
                   "INSTANT DECISIONS (decisões tomadas NA HORA, no momento da fala): I'll have a diet coke, please. · "
                   "I'll go home, I'm tired.\n"
                   "Diferença: decisão na hora → WILL (I'll have the chicken) · plano decidido ANTES → GOING TO.\n"
                   "Estrutura: sujeito + will ('ll) + verbo na forma básica.\n"
                   "Não se preocupe demais: no dia a dia, will e going to são entendidos como futuro!",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the situations from the lesson to the uses of will.",
         "translation": "Ligue as situações da aula aos usos do will.",
         "example": "\"I'll change, I promise.\" (the frog) → promise to do something",
         "pairs": [
             {"left": "\"Yes, I'll have a diet coke, please.\"", "right": "decide to have something"},
             {"left": "\"I'll help you when I finish.\"", "right": "offer to do something"},
             {"left": "\"I'll love you forever.\"", "right": "promise"},
             {"left": "\"I'll go home. I'm tired.\"", "right": "instant decision"},
         ]},
        {"type": "group",
         "prompt": "Promise, offer or instant decision?",
         "translation": "Promessa, oferta de ajuda ou decisão na hora? Coloque cada frase no grupo certo.",
         "example": "I'll call you every day, I promise. → promise",
         "categories": ["promise", "offer", "instant decision"],
         "words": [
             {"text": "I won't be late again, I promise.", "category": "promise"},
             {"text": "I'll never forget you.", "category": "promise"},
             {"text": "Your bags are heavy. I'll carry one.", "category": "offer"},
             {"text": "I'll lend you some money.", "category": "offer"},
             {"text": "Hmm… I'll have the fish, please.", "category": "instant decision"},
             {"text": "It's late. I'll take a taxi.", "category": "instant decision"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta.",
         "example": "I'm thirsty. — [I'll get] you a glass of water.",
         "text": "1. Your order is two burgers. Anything else? — Yes, [*I'll have|I have had|I'm going to having] a soda.\n"
                 "2. I left my wallet at home. — Don't worry. [*I'll lend|I lend|I lent] you some money.\n"
                 "3. I'll do my homework every day, I [*promise|promised|offer].\n"
                 "4. We haven't got any milk. — [*I'll buy|I bought|I'm buy] some on my way home."},
    ],
}

AULA11_SHALL = {
    "title": "Offers as questions: Shall I…? Shall we…?",
    "lesson": 11,
    "description": "Quando a OFERTA é uma PERGUNTA, usamos SHALL I / SHALL WE (não \"will I\"):\n"
                   "Shall I help you open the window? (Quer que eu te ajude a abrir a janela?)\n"
                   "Shall we do the washing up? (Quer que a gente lave a louça?)\n"
                   "Shall I + verbo na forma básica: Shall I open the window? · Shall I make you a sandwich? · "
                   "Shall I carry one for you? · Shall I turn off the music?",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the sentences (exercise from the lesson).",
         "translation": "Ligue as frases (exercício da aula).",
         "example": "It's hot in here. → Shall I open the window?",
         "pairs": [
             {"left": "I'm thirsty.", "right": "I'll get you a glass of water."},
             {"left": "I have a headache.", "right": "Shall I turn off the music?"},
             {"left": "This exercise is hard.", "right": "I'll help you to do it."},
             {"left": "I'm hungry.", "right": "Shall I make you a sandwich?"},
             {"left": "These bags are heavy.", "right": "Shall I carry one for you?"},
             {"left": "I left my wallet at home.", "right": "I'll lend you some money."},
             {"left": "We haven't got any milk.", "right": "I'll buy some on my way home."},
         ]},
        {"type": "dropdown",
         "prompt": "Choose will or shall.",
         "translation": "Escolha will ('ll) ou shall.",
         "example": "[Shall] I help you?",
         "text": "1. [*Shall|Will] I open the window?\n2. I[*'ll|shall] help you with your homework.\n"
                 "3. [*Shall|Will] we do the washing up?\n4. I[*'ll|shall] love you forever."},
        {"type": "order",
         "prompt": "Put the words in order to make an offer.",
         "translation": "Coloque as palavras em ordem para fazer uma oferta. (Quer que eu carregue uma para você?)",
         "example": "I / Shall / the window / open → Shall I open the window?",
         "tokens": ["Shall", "I", "carry", "one", "for", "you?"], "alternatives": []},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Shall I…?\" is an offer. → True",
         "statements": [
             {"text": "We use WILL for decisions made at the moment of speaking.", "answer": True,
              "translation": "Usamos WILL para decisões tomadas no momento da fala."},
             {"text": "For offers in questions, we say \"Will I help you?\".", "answer": False,
              "translation": "Para ofertas em perguntas, dizemos \"Will I help you?\"."},
             {"text": "\"I'll change, I promise\" is a promise.", "answer": True,
              "translation": "\"I'll change, I promise\" é uma promessa."},
         ]},
    ],
}

AULA11_LISTENING = {
    "title": "Listening — at the café",
    "lesson": 11,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: o 'LL quase some: \"I'll have\" = \"ál hév\". Preste atenção no SHALL das ofertas.",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"I'll help you.\" → I'll",
         "audio": f"{AUDIO}/aula11-words.m4a",
         "text": "1. [*I'll|I] have the chicken.\n2. [*Shall|Will] I open the window?\n3. I [*won't|want] forget.\n"
                 "4. [*We'll|We] call you later.\n5. [*Shall we|Should we] go?"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"I'll get you some water.\" → [I'll] get you some water.",
         "audio": f"{AUDIO}/aula11-dictation.m4a",
         "text": "1. [Shall] I make you a sandwich?\n2. I'll [lend] you some money.\n3. I'll [love] you forever.\n"
                 "4. I'll [help] you when I finish."},
        {"type": "info",
         "prompt": "Now listen: Lucas and Nina are at a café.",
         "translation": "Agora ouça: o Lucas e a Nina estão em um café. Eles fazem pedidos, ofertas e promessas! "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula11-cafe.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Lucas and Nina are at a [café].",
         "text": "1. What does Nina order? → [*A cappuccino and a piece of chocolate cake.|A coffee and a sandwich.|Orange juice.]\n"
                 "2. What does Lucas order? → [*An espresso.|A cappuccino.|A soda.]\n"
                 "3. What problem does Nina have? → [*She left her wallet at home.|She's very tired.|She has a headache.]\n"
                 "4. What does Nina promise? → [*She'll pay next time.|She'll arrive early.|She'll make a cake.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Lucas pays today. → True",
         "statements": [
             {"text": "Lucas offers to close the window.", "answer": True,
              "translation": "O Lucas se oferece para fechar a janela."},
             {"text": "Lucas decides to eat a sandwich.", "answer": False,
              "translation": "O Lucas decide comer um sanduíche."},
         ]},
    ],
}

AULA11_SPEAKING = {
    "title": "Speaking — I'll help you!",
    "lesson": 11,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: shall = \"shél\" (curtinho) · I'll = \"ául\".",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula11-say-s{i}.m4a"} for i, t in enumerate(
             ["Yes, I'll have a diet coke, please.", "I'll help you when I finish.", "I'll change, I promise.",
              "I'll love you forever.", "Shall I help you open the window?", "Shall we do the washing up?"], 1)]},
        {"type": "speak",
         "prompt": "Now respond with an offer.",
         "translation": "Agora responda com uma oferta (I'll… ou Shall I…?).",
         "example": "\"It's hot in here.\" → \"Shall I open the window?\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula11-say-y{i}.m4a"} for i, t in enumerate(
             ["It's hot in here.", "I'm thirsty.", "I have a headache.", "These bags are heavy.", "I'm hungry."], 1)]},
    ],
}

AULA11_READING = {
    "title": "Reading — New Year's promises",
    "lesson": 11,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça as promessas de Ano-Novo da família Souza. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula11-reading.m4a",
         "text": "NEW YEAR'S PROMISES\n\n"
                 "Every December 31st, my family writes promises for the new year. Here are this year's promises:\n"
                 "DAD: \"I'll stop eating so much junk food, and I'll walk to work.\"\n"
                 "MOM: \"I won't work on weekends. I'll spend more time with my family.\"\n"
                 "MY SISTER, CLARA: \"I'll study harder, and I won't use my phone at dinner.\"\n"
                 "ME: \"I'll learn English! I'll practice every day with my English course.\"\n"
                 "GRANDMA: \"I'll teach my grandchildren how to make my famous chocolate cake.\"\n"
                 "Last year, we didn't keep all our promises… but this year will be different!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "When does the family write promises? → [On December 31st.]",
         "text": "1. How will Dad go to work? → [*He'll walk.|He'll drive.|He'll take the bus.]\n"
                 "2. What won't Mom do? → [*She won't work on weekends.|She won't cook.|She won't study.]\n"
                 "3. What won't Clara do at dinner? → [*Use her phone.|Eat junk food.|Talk.]\n"
                 "4. What will Grandma teach? → [*How to make her chocolate cake.|English.|How to walk.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "The writer wants to learn English. → True",
         "statements": [
             {"text": "Last year, they kept all their promises.", "answer": False,
              "translation": "No ano passado, eles cumpriram todas as promessas."},
             {"text": "Mom will spend more time with the family.", "answer": True,
              "translation": "A mãe vai passar mais tempo com a família."},
         ]},
        {"type": "fill",
         "prompt": "Complete with will ('ll) or won't, according to the text.",
         "translation": "Complete com 'll ou won't, de acordo com o texto.",
         "example": "Dad: \"I[’ll] walk to work.\"",
         "text": "1. Mom: \"I [won't] work on weekends.\"\n2. Clara: \"I [won't] use my phone at dinner.\"\n"
                 "3. This year [will] be different!"},
    ],
}

AULA11_WRITING = {
    "title": "Writing — my promises",
    "lesson": 11,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Promises: I'll… / I won't… · Offers: I'll… / Shall I…? · Decisions: I'll have…",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu vou te ajudar com o dever de casa. → I'll help you with your homework.",
         "text": "1. Quer que eu abra a janela? → [Shall I open the window?]\n"
                 "2. Eu vou querer o frango, por favor. → [I'll have the chicken, please.]\n"
                 "3. Eu prometo que não vou me atrasar. → [I promise I won't be late.|I won't be late, I promise.|"
                 "I promise I will not be late.]"},
        {"type": "free",
         "prompt": "Write your promises for this year (at least 3 with I'll and 2 with I won't). "
                   "Then write one offer to help a friend.",
         "translation": "Escreva as suas promessas para este ano (pelo menos 3 com I'll e 2 com I won't). "
                        "Depois escreva uma oferta de ajuda para um amigo.",
         "example": "I'll study English every day.",
         "model_answer": "This year, I'll study English every day.\n"
                         "I'll drink more water and I'll go to bed early.\n"
                         "I won't eat so much chocolate, and I won't spend hours on my phone.\n"
                         "And to my friend Bia: your English test is next week. I'll help you study!",
         "keywords": ["I'll", "I won't"], "min_words": 30, "points": 4},
    ],
}


AULA11_VIDEO = _video(11, AULA11_TOPIC, "Video — I'll help you!",
                      "a Sarah e o Leo vão a um café: pedidos, ofertas e promessas com will e shall.",
                      "aula11-video", [
    _q("What will Leo have?", "O que o Leo vai pedir?", "A cappuccino.", "A juice.", "A tea.", "An espresso."),
    _q("What does Sarah promise?", "O que a Sarah promete?", "She'll pay next time.", "She'll buy an umbrella.", "She'll call a taxi.", "She'll go home."),
    _q("Complete: ___ I call a taxi for you?", "Complete: ___ eu chamar um táxi para você?", "Shall", "Will", "Do", "Am"),
    _q("\"I'll always help you\" is…", "\"I'll always help you\" é…", "a promise.", "a plan.", "a prediction with evidence.", "a question."),
])

# ---------- Aula 12 — Will vs Be Going To (https://youtu.be/TR9RpzZpa94) ----------

AULA12_TOPIC = "Aula 12 — Will vs Be Going To"

AULA12_CONTRAST = {
    "title": "Will or going to?",
    "lesson": 12,
    "description": "WILL + verbo:\n"
                   "• decisões NA HORA: I'm ready to order. I'll have the chicken, please.\n"
                   "• previsões de OPINIÃO: I think Brazil will win the next World Cup.\n"
                   "• ofertas, promessas: I will help you with your homework tonight.\n"
                   "BE GOING TO + verbo:\n"
                   "• planos decididos ANTES: I'm going to visit my parents next weekend.\n"
                   "• previsões com EVIDÊNCIA: I see clouds. It's going to rain.\n"
                   "• algo PRESTES a acontecer: Look! The bomb is going to explode!\n"
                   "Lembre: na comunicação real, os dois expressam futuro e você será entendido — não se desespere com as regras!",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "Will or going to? Put each use in the right group.",
         "translation": "Will ou going to? Coloque cada uso no grupo certo.",
         "example": "instant decision → will · plan → going to",
         "categories": ["will", "going to"],
         "words": [
             {"text": "decision at the moment of speaking", "category": "will"},
             {"text": "prediction from personal opinion", "category": "will"},
             {"text": "offers and promises", "category": "will"},
             {"text": "plans decided before", "category": "going to"},
             {"text": "prediction from evidence", "category": "going to"},
             {"text": "something about to happen", "category": "going to"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct option (exercise from the lesson).",
         "translation": "Escolha a opção correta (exercício da aula).",
         "example": "I promise I [will water] the plants.",
         "text": "1. Do you have any plans for tomorrow? — Yes, [*I'm going to have|I'll have] a picnic.\n"
                 "2. Why is she learning Spanish? — She [*'s going to travel|'ll travel] to Spain.\n"
                 "3. We're thirsty. — Wait here. [*I'll get|I'm going to get] you some water.\n"
                 "4. Meat or fish? — [*I'll have|I'm going to have] some fish, please.\n"
                 "5. Why are you turning on the TV? — [*I'm going to watch|I'll watch] the football match at 4 p.m.\n"
                 "6. Why do you want so many eggs? — [*I'm going to make|I'll make] a big cake this weekend.\n"
                 "7. Why are you taking an umbrella? — I think [*it's going to rain|it rains]."},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"I'll have the chicken\" is an instant decision. → True",
         "statements": [
             {"text": "\"I'm going to visit my parents next weekend\" is a plan.", "answer": True,
              "translation": "\"I'm going to visit my parents next weekend\" é um plano."},
             {"text": "\"I see clouds, it's going to rain\" is a prediction from opinion.", "answer": False,
              "translation": "\"I see clouds, it's going to rain\" é uma previsão de opinião."},
             {"text": "In real conversations, people understand you with will or going to.", "answer": True,
              "translation": "Em conversas reais, as pessoas te entendem com will ou going to."},
         ]},
    ],
}

AULA12_QUESTIONS = {
    "title": "Talking about the future",
    "lesson": 12,
    "description": "Perguntas da aula e como responder:\n"
                   "Will it be cold tomorrow where you live? → Yes, it will. / No, it won't.\n"
                   "What are your plans for next Christmas? → I'm going to stay home with my family.\n"
                   "Which country do you think will win the next World Cup? → I think Brazil will win.\n"
                   "What do you promise you will do better this year? → I promise I will do more exercise.",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas da aula às respostas.",
         "example": "Will it be cold tomorrow? → No, it won't.",
         "pairs": [
             {"left": "What are your plans for next Christmas?", "right": "I'm going to stay home with my family."},
             {"left": "Which country do you think will win the next World Cup?", "right": "I think Brazil will win."},
             {"left": "What do you promise you will do better this year?", "right": "I promise I will do more exercise."},
             {"left": "Will it be cold tomorrow where you live?", "right": "Yes, it will."},
         ]},
        {"type": "fill",
         "prompt": "Complete with will ('ll) or going to + verb.",
         "translation": "Complete com 'll ou going to + o verbo entre parênteses.",
         "example": "Look at the sky! It's [going to rain]. (rain)",
         "text": "1. The phone is ringing. — I[’ll answer|'ll answer] it! (answer)\n"
                 "2. We bought the tickets. We're [going to travel] to Bahia in July. (travel)\n"
                 "3. Be careful! You're [going to fall]! (fall)\n"
                 "4. I think robots [will do] our housework one day. (do)"},
        {"type": "choice",
         "prompt": "Your friend says: \"I forgot my lunch!\" What do you say?",
         "translation": "Seu amigo diz: \"Esqueci meu almoço!\" O que você responde? (decisão / oferta na hora)",
         "example": "Oferta na hora → will",
         "options": ["Don't worry, I'll share my sandwich with you.", "Don't worry, I'm going to share my sandwich two weeks ago.",
                     "Don't worry, I share my sandwich yesterday.", "Don't worry, I going to share my sandwich."],
         "correct": 0},
    ],
}

AULA12_LISTENING = {
    "title": "Listening — planning a birthday",
    "lesson": 12,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: preste atenção: é um plano (going to) ou uma decisão na hora (I'll)?",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"I'll have the fish.\" → I'll have",
         "audio": f"{AUDIO}/aula12-words.m4a",
         "text": "1. [*I'm going to|I'll] visit my parents.\n2. [*I'll|I'm going to] have the chicken.\n"
                 "3. It's [*going to|going] rain.\n4. [*I think|I thought] Brazil will win.\n5. [*I promise|I'm promising] I'll call you."},
        {"type": "info",
         "prompt": "Now listen: Leo and Carol plan their mother's birthday.",
         "translation": "Agora ouça: o Leo e a Carol planejam o aniversário da mãe deles. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula12-birthday.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "It's their [mother's] birthday.",
         "text": "1. What's Carol's plan? → [*She's going to make a cake.|She's going to buy flowers.|She's going to cook lunch.]\n"
                 "2. What does Leo decide at the moment? → [*He'll buy the flowers.|He'll make the cake.|He'll call Grandma.]\n"
                 "3. What does Carol think about the weather? → [*It's going to rain.|It will be sunny.|It will snow.]\n"
                 "4. So, where will they have the party? → [*At home.|At the park.|At a restaurant.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Carol bought the ingredients. → True",
         "statements": [
             {"text": "Leo promises he won't be late.", "answer": True, "translation": "O Leo promete que não vai se atrasar."},
             {"text": "Their mother knows about the party.", "answer": False, "translation": "A mãe deles sabe da festa."},
         ]},
    ],
}

AULA12_SPEAKING = {
    "title": "Speaking — will or going to?",
    "lesson": 12,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: na fala, use I'll e gonna: \"ául\" · \"aim gâna\".",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula12-say-s{i}.m4a"} for i, t in enumerate(
             ["I'll have the chicken, please.", "I'm going to visit my parents next weekend.",
              "I think Brazil will win the next World Cup.", "I see clouds. It's going to rain.",
              "I will help you with your homework tonight.", "Look! The bomb is going to explode!"], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions from the lesson.",
         "translation": "Agora responda às perguntas do início da aula sobre VOCÊ.",
         "example": "\"What are your plans for next Christmas?\" → \"I'm going to stay home with my family.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula12-say-y{i}.m4a"} for i, t in enumerate(
             ["Will it be cold tomorrow where you live?", "What are your plans for next Christmas?",
              "Which country do you think will win the next World Cup?",
              "What do you promise you will do better this year?"], 1)]},
    ],
}

AULA12_READING = {
    "title": "Reading — messages about Saturday",
    "lesson": 12,
    "subject": "Reading",
    "description": "Leia (e ouça) as mensagens e responda às perguntas de acordo com o texto.",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the messages.",
         "translation": "Leia e ouça as mensagens de um grupo de amigos sobre o sábado. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula12-reading.m4a",
         "text": "SATURDAY 🏖️\n\n"
                 "MARI: Hi, guys! We're going to go to the beach on Saturday. We decided last week. Who wants to come?\n"
                 "TOM: Me! I'll bring the volleyball.\n"
                 "JULIA: Hmm, I checked the weather app. There are a lot of clouds. I think it's going to rain.\n"
                 "MARI: Oh no! OK, new plan: I'll check the weather again on Friday.\n"
                 "TOM: If it rains, we can watch a movie at my place. I'll make popcorn!\n"
                 "JULIA: Great idea. I'll bring the drinks. I promise I won't be late this time 😅\n"
                 "MARI: Ha ha. I don't believe you, Julia!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "What's the plan for Saturday? → [Go to the beach.]",
         "text": "1. When did they decide to go to the beach? → [*Last week.|Today.|On Friday.]\n"
                 "2. What will Tom bring? → [*The volleyball.|The drinks.|The popcorn and drinks.]\n"
                 "3. Why does Julia think it's going to rain? → [*There are a lot of clouds in the weather app.|"
                 "It rained last week.|She doesn't like the beach.]\n"
                 "4. What does Julia promise? → [*She won't be late.|She'll make popcorn.|She'll go to the beach.]"},
        {"type": "group",
         "prompt": "Find in the text: will or going to? Why?",
         "translation": "Encontre no texto: cada frase é um plano/evidência (going to) ou decisão/oferta/promessa (will)?",
         "example": "We're going to go to the beach. → plan / evidence",
         "categories": ["plan / evidence (going to)", "decision / offer / promise (will)"],
         "words": [
             {"text": "We're going to go to the beach.", "category": "plan / evidence (going to)"},
             {"text": "I think it's going to rain.", "category": "plan / evidence (going to)"},
             {"text": "I'll bring the volleyball.", "category": "decision / offer / promise (will)"},
             {"text": "I'll make popcorn!", "category": "decision / offer / promise (will)"},
             {"text": "I promise I won't be late.", "category": "decision / offer / promise (will)"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Mari wrote the first message. → True",
         "statements": [
             {"text": "Mari believes Julia's promise.", "answer": False, "translation": "A Mari acredita na promessa da Julia."},
             {"text": "If it rains, they can watch a movie at Tom's place.", "answer": True,
              "translation": "Se chover, eles podem ver um filme na casa do Tom."},
         ]},
    ],
}

AULA12_WRITING = {
    "title": "Writing — my future",
    "lesson": 12,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Planos e evidências → going to · decisões na hora, opiniões, ofertas e promessas → will.",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu vou visitar meus pais no próximo fim de semana. → I'm going to visit my parents next weekend.",
         "text": "1. Eu acho que o Brasil vai ganhar a próxima Copa. → [I think Brazil will win the next World Cup.]\n"
                 "2. Ela vai viajar para a Espanha (já comprou a passagem). → [She's going to travel to Spain.|"
                 "She is going to travel to Spain.]"},
        {"type": "free",
         "prompt": "Answer the questions from the lesson: What are your plans for next Christmas? Which country do you "
                   "think will win the next World Cup? What do you promise you will do better this year? "
                   "Will it be cold tomorrow where you live?",
         "translation": "Responda às perguntas da aula com frases completas, usando will e going to.",
         "example": "Next Christmas, I'm going to stay home with my family.",
         "model_answer": "Next Christmas, I'm going to stay home with my family. My mom is going to cook a big dinner.\n"
                         "I think Brazil will win the next World Cup!\n"
                         "I promise I will do more exercise and I will read more books.\n"
                         "No, it won't be cold tomorrow. It's summer here.",
         "keywords": ["going to", "will", "won't"], "min_words": 30, "points": 4},
    ],
}


AULA12_VIDEO = _video(12, AULA12_TOPIC, "Video — Plans change!",
                      "o plano de sábado muda: veja quando a Sarah usa going to e quando usa will.",
                      "aula12-video", [
    _q("\"We're going to play volleyball\" is…", "\"We're going to play volleyball\" é…", "a plan.", "an instant decision.", "a promise.", "an offer."),
    _q("Why does Sarah say \"It's going to rain\"?", "Por que a Sarah diz \"It's going to rain\"?", "She can see dark clouds.", "She heard it on TV.", "It's her opinion.", "It's a promise."),
    _q("\"I'll call our friends\" is…", "\"I'll call our friends\" é…", "an instant decision.", "a plan from last week.", "a prediction.", "a rule."),
    _q("Complete: I ___ make some popcorn.", "Complete: eu ___ fazer pipoca.", "'ll", "'m going", "will to", "going"),
])

# ---------- Aula 13 — Present Continuous for Future Arrangements (https://youtu.be/VeTJOnPTodQ) ----------

AULA13_TOPIC = "Aula 13 — Present Continuous for Future Arrangements"

AULA13_ARRANGEMENTS = {
    "title": "Future arrangements: I'm meeting a friend tonight",
    "lesson": 13,
    "description": "FUTURE ARRANGEMENTS = planos já COMBINADOS, com data, hora ou lugar marcados (passagem comprada, hotel "
                   "reservado, consulta no dentista, casamento com convite, reunião agendada).\n"
                   "Usamos o PRESENT CONTINUOUS: sujeito + am / is / are + verbo-ING + EXPRESSÃO DE FUTURO\n"
                   "I'm watching a movie tonight. · I'm going to a party on Saturday night. · "
                   "I'm running in the park on Sunday morning. · I'm seeing an old friend tonight. · "
                   "She isn't leaving until Friday.\n"
                   "Pergunta: What are you doing tonight / this weekend / on Sunday? (= O que você VAI fazer…?)\n"
                   "Expressões de futuro: tonight · tomorrow · this weekend · on Sunday · next month\n"
                   "Going to e will também funcionam, mas o present continuous deixa claro que já está TUDO COMBINADO.",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "Now or future? Read the sentences.",
         "translation": "Agora (now) ou futuro (future)? Leia as frases (exercício da aula). Procure a expressão de futuro!",
         "example": "I'm talking to my dad on the phone. → now",
         "categories": ["now", "future"],
         "words": [
             {"text": "I'm living in a big house with my parents.", "category": "now"},
             {"text": "I'm working on a school project.", "category": "now"},
             {"text": "I'm reading a very good book about history.", "category": "now"},
             {"text": "I'm studying for my science test.", "category": "now"},
             {"text": "They're meeting their friends this weekend.", "category": "future"},
             {"text": "My parents are visiting us next month.", "category": "future"},
             {"text": "We're having lunch with our clients tomorrow.", "category": "future"},
             {"text": "Are you watching the game tonight?", "category": "future"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta.",
         "example": "I'm [watching] a movie tonight.",
         "text": "1. I'm [*going|go|goes] to a party on Saturday night.\n"
                 "2. She [*isn't leaving|doesn't leaving|not leaving] until Friday.\n"
                 "3. What [*are you doing|do you doing|you are doing] this weekend?\n"
                 "4. We [*are having|having|have having] lunch with our clients tomorrow.\n"
                 "5. I'm [*running|runing|run] in the park on Sunday morning."},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "A dentist appointment is a future arrangement. → True",
         "statements": [
             {"text": "A future arrangement has a fixed time or place.", "answer": True,
              "translation": "Um future arrangement tem hora ou lugar marcados."},
             {"text": "\"What are you doing tonight?\" can be a question about the future.", "answer": True,
              "translation": "\"What are you doing tonight?\" pode ser uma pergunta sobre o futuro."},
             {"text": "It's wrong to use going to for future arrangements.", "answer": False,
              "translation": "É errado usar going to para future arrangements."},
         ]},
    ],
}

AULA13_DIARY = {
    "title": "My diary for next week",
    "lesson": 13,
    "description": "Agenda (diary / calendar): use o present continuous para os compromissos marcados.\n"
                   "On Monday, I'm meeting my boss at 9 a.m. · On Tuesday, I'm having lunch with Ana. · "
                   "I'm flying to Recife on Friday.\n"
                   "Perguntas: Who are you meeting on Monday? · Where are you going on Sunday? · "
                   "What time is your train leaving?\n"
                   "Negativa: I'm not working on Saturday. · They aren't coming tonight.",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Complete with the present continuous.",
         "translation": "Complete com o present continuous do verbo entre parênteses.",
         "example": "I'm [seeing] an old friend tonight. (see)",
         "text": "1. My parents [are visiting] us next month. (visit)\n2. We [are flying] to Salvador on Friday. (fly)\n"
                 "3. She [is having] dinner with her old professor tomorrow. (have)\n"
                 "4. I [am not working] on Saturday. (not / work)"},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas.",
         "example": "What are you doing tonight? → I'm watching a movie.",
         "pairs": [
             {"left": "Who are you meeting on Monday?", "right": "My new boss."},
             {"left": "Where are you going on Sunday?", "right": "To my grandma's house."},
             {"left": "What time is your train leaving?", "right": "At 6:15 p.m."},
             {"left": "Are you coming to the party?", "right": "Yes, I am. I'm bringing a cake."},
         ]},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (O que você vai fazer no sábado à noite?)",
         "example": "you / tonight / are / doing / What → What are you doing tonight?",
         "tokens": ["What", "are", "you", "doing", "on", "Saturday", "night?"], "alternatives": []},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza usando o present continuous.",
         "example": "Eu vou a uma festa no sábado. → I'm going to a party on Saturday.",
         "text": "1. Eu vou encontrar um velho amigo hoje à noite. → [I'm seeing an old friend tonight.|"
                 "I'm meeting an old friend tonight.|I am seeing an old friend tonight.|I am meeting an old friend tonight.]\n"
                 "2. Ela só vai embora na sexta. → [She isn't leaving until Friday.|She's not leaving until Friday.|"
                 "She is not leaving until Friday.]"},
    ],
}

AULA13_LISTENING = {
    "title": "Listening — when are they meeting?",
    "lesson": 13,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: anote os dias e horários. Primeiro ouça sem ler nada; depois confira.",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose: now or future?",
         "translation": "Ouça e escolha: agora (now) ou futuro (future)?",
         "example": "Você ouve: \"I'm having lunch tomorrow.\" → future",
         "audio": f"{AUDIO}/aula13-nowfuture.m4a",
         "text": "1. [*future|now]\n2. [*now|future]\n3. [*future|now]\n4. [*now|future]\n5. [*future|now]"},
        {"type": "info",
         "prompt": "Now listen: Daniel calls his old friend Laura. They want to meet.",
         "translation": "Agora ouça: o Daniel liga para a velha amiga Laura. Eles querem se encontrar, mas a agenda dele está "
                        "cheia! Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula13-call.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Daniel arrived in [Lisbon] last night.",
         "text": "1. When are they meeting? → [*On Thursday at 10:30 a.m.|On Wednesday at 1 p.m.|On Thursday at 7 p.m.]\n"
                 "2. What is Daniel doing on Wednesday? → [*He's visiting a factory.|He's flying home.|He's having dinner with Laura.]\n"
                 "3. Who is he having dinner with on Thursday? → [*His old teacher.|His boss.|Laura.]\n"
                 "4. Where are they meeting? → [*At a café near the river.|At the hotel.|At the airport.]"},
        {"type": "match",
         "prompt": "Listen again. Complete Daniel's diary for Thursday.",
         "translation": "Ouça de novo. Ligue os horários aos compromissos de quinta-feira do Daniel.",
         "example": "10:30 → coffee with Laura",
         "pairs": [
             {"left": "8:00", "right": "breakfast meeting with clients"},
             {"left": "2:00", "right": "presentation"},
             {"left": "7:30", "right": "dinner with his old teacher"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Daniel is in Lisbon. → True",
         "statements": [
             {"text": "Daniel is free on Thursday evening.", "answer": False,
              "translation": "O Daniel está livre na quinta à noite."},
             {"text": "Daniel is flying home on Friday.", "answer": True, "translation": "O Daniel volta para casa de avião na sexta."},
         ]},
    ],
}

AULA13_SPEAKING = {
    "title": "Speaking — what are you doing this weekend?",
    "lesson": 13,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: grave a sua voz respondendo, depois se escute — é uma ótima forma de treinar sozinho!",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula13-say-s{i}.m4a"} for i, t in enumerate(
             ["I'm watching a movie tonight.", "I'm going to a party on Saturday night.",
              "I'm running in the park on Sunday morning.", "I'm seeing an old friend tonight.",
              "She isn't leaving until Friday.", "What are you doing this weekend?"], 1)]},
        {"type": "speak",
         "prompt": "Speaking practice: answer about YOUR arrangements.",
         "translation": "Prática de speaking: responda sobre os SEUS compromissos.",
         "example": "\"What are you doing tonight?\" → \"I'm having dinner with my sister.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula13-say-y{i}.m4a"} for i, t in enumerate(
             ["What are you doing tonight?", "Who are you meeting on Monday?", "Where are you going on Sunday?",
              "What are you doing on Saturday night?", "Are you traveling next month?"], 1)]},
    ],
}

AULA13_READING = {
    "title": "Reading — the wedding weekend",
    "lesson": 13,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the e-mail.",
         "translation": "Leia e ouça o e-mail da Ana para a prima Júlia sobre o casamento do irmão. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula13-reading.m4a",
         "text": "Hi, Júlia!\n\n"
                 "Everything is ready for my brother's wedding! Here's the plan for the weekend:\n"
                 "On Friday, we're picking up Grandma at the airport at 6 p.m. She's flying from Recife.\n"
                 "On Saturday morning, my mom and I are going to the hairdresser at 9. The ceremony is starting at 4 p.m. "
                 "at Santa Rita Church, and the party is at the Blue Garden restaurant.\n"
                 "On Sunday, we're having a family lunch at my parents' house. And on Monday, the couple is flying to Chile "
                 "for their honeymoon!\n"
                 "Are you coming on Friday or Saturday? Tell me!\n\n"
                 "Love,\nAna"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Whose wedding is it? → [Ana's brother's.]",
         "text": "1. When are they picking up Grandma? → [*On Friday at 6 p.m.|On Saturday at 9 a.m.|On Sunday.]\n"
                 "2. Where is the ceremony? → [*At Santa Rita Church.|At the Blue Garden restaurant.|At the parents' house.]\n"
                 "3. What are they doing on Sunday? → [*Having a family lunch.|Going to the airport.|Going to the hairdresser.]\n"
                 "4. Where is the couple flying on Monday? → [*To Chile.|To Recife.|To Portugal.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Grandma is flying from Recife. → True",
         "statements": [
             {"text": "The ceremony is starting in the morning.", "answer": False,
              "translation": "A cerimônia começa de manhã."},
             {"text": "Ana and her mom are going to the hairdresser.", "answer": True,
              "translation": "A Ana e a mãe vão ao cabeleireiro."},
         ]},
        {"type": "fill",
         "prompt": "Complete according to the text.",
         "translation": "Complete de acordo com o texto.",
         "example": "Grandma is [flying] from Recife.",
         "text": "1. We're [picking] up Grandma at the airport.\n2. The ceremony [is] starting at 4 p.m.\n"
                 "3. On Sunday, we're [having] a family lunch."},
    ],
}

AULA13_WRITING = {
    "title": "Writing — my arrangements",
    "lesson": 13,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ am / is / are + verbo-ING + expressão de futuro (tonight, tomorrow, on Sunday…).",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write N (now) or F (future).",
         "translation": "Escreva N (agora) ou F (futuro).",
         "example": "I'm studying for my test. → N",
         "text": "1. They're meeting their friends this weekend. → [F]\n2. I'm talking to my dad on the phone. → [N]\n"
                 "3. My parents are visiting us next month. → [F]\n4. I'm reading a good book. → [N]"},
        {"type": "free",
         "prompt": "Write about your arrangements for next week. What are you doing on each day? "
                   "Who are you meeting? Where are you going? Use the present continuous and time expressions.",
         "translation": "Escreva sobre os seus compromissos da próxima semana: o que você vai fazer em cada dia, com quem vai "
                        "se encontrar e aonde vai. Use o present continuous e expressões de tempo.",
         "example": "On Monday, I'm meeting my boss at 9 a.m.",
         "model_answer": "On Monday, I'm meeting my boss at 9 a.m.\n"
                         "On Tuesday evening, I'm having dinner with my sister at an Italian restaurant.\n"
                         "On Thursday, I'm going to the dentist at 3 p.m.\n"
                         "On Saturday, I'm flying to Porto Alegre for my friend's wedding.\n"
                         "I'm not working on Friday!",
         "keywords": ["I'm meeting", "I'm having", "On"], "min_words": 30, "points": 4},
    ],
}


AULA13_VIDEO = _video(13, AULA13_TOPIC, "Video — My week",
                      "a Sarah mostra a agenda da semana: compromissos marcados com o present continuous.",
                      "aula13-video", [
    _q("What's Sarah doing on Monday at nine?", "O que a Sarah vai fazer na segunda às nove?", "She's seeing the dentist.", "She's flying to Rio.", "She's meeting her boss.", "She's taking a yoga class."),
    _q("Who is she meeting on Tuesday?", "Com quem ela vai se encontrar na terça?", "Her new boss.", "Her sister.", "Her best friend.", "The dentist."),
    _q("What's she doing on Wednesday evening?", "O que ela vai fazer na quarta à noite?", "Taking a yoga class.", "Flying to Rio.", "Getting married.", "Seeing the dentist."),
    _q("When is she flying to Rio?", "Quando ela vai voar para o Rio?", "On Friday.", "On Monday.", "On Saturday.", "Next month."),
    _q("What's happening on Saturday?", "O que vai acontecer no sábado?", "Her best friend is getting married.", "She's working.", "She's going to the dentist.", "Nothing."),
])

# ---------- Aula 14 — -ED or -ING Adjectives (https://youtu.be/dbhPuv0v1h0) ----------

AULA14_TOPIC = "Aula 14 — -ED or -ING Adjectives"

AULA14_CONTRAST = {
    "title": "Bored or boring? Interested or interesting?",
    "lesson": 14,
    "description": "-ED → como a PESSOA SE SENTE: I was really interested in the movie. · She has nothing to do. She is bored.\n"
                   "-ING → descreve a SITUAÇÃO, a COISA ou a PESSOA que causa o sentimento: "
                   "The movie was so interesting that I watched it twice. · The movie was so boring that I fell asleep.\n"
                   "excited × exciting (animado × empolgante) · interested × interesting · surprised × surprising · "
                   "bored × boring (entediado × chato) · confused × confusing (confuso nos dois em português!) · "
                   "frightened × frightening (com medo × assustador) · embarrassed × embarrassing (envergonhado × "
                   "constrangedor) · tired × tiring (cansado × cansativo) · frustrated × frustrating\n"
                   "EXCEÇÕES: scared × SCARY (assustado × assustador) · stressed × STRESSFUL (estressado × estressante)",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose -ed or -ing (exercises from the lesson).",
         "translation": "Escolha -ed ou -ing (exercícios da aula).",
         "example": "The trip is going to be [exciting]. She is very [excited].",
         "text": "1. The trip is going to be [*exciting|excited].\n2. She is very [*excited|exciting].\n"
                 "3. Her job is very [*frustrating|frustrated].\n4. She is really [*frustrated|frustrating].\n"
                 "5. The competition was very [*tiring|tired].\n6. The athlete was very [*tired|tiring]."},
        {"type": "match",
         "prompt": "Match the adjectives to Portuguese.",
         "translation": "Ligue os adjetivos ao português.",
         "example": "bored → entediado(a)",
         "pairs": [
             {"left": "boring", "right": "chato, entediante"},
             {"left": "embarrassed", "right": "envergonhado(a)"},
             {"left": "embarrassing", "right": "constrangedor"},
             {"left": "frightened", "right": "com medo"},
             {"left": "frightening", "right": "assustador"},
             {"left": "tiring", "right": "cansativo"},
             {"left": "surprised", "right": "surpreso(a)"},
         ]},
        {"type": "group",
         "prompt": "Feeling (person) or situation (cause)?",
         "translation": "Sentimento da pessoa ou descrição da situação? Coloque cada palavra no grupo certo.",
         "example": "confused → feeling · confusing → situation",
         "categories": ["feeling (how a person feels)", "situation (what causes it)"],
         "words": [
             {"text": "confused", "category": "feeling (how a person feels)"},
             {"text": "scared", "category": "feeling (how a person feels)"},
             {"text": "stressed", "category": "feeling (how a person feels)"},
             {"text": "interested", "category": "feeling (how a person feels)"},
             {"text": "confusing", "category": "situation (what causes it)"},
             {"text": "scary", "category": "situation (what causes it)"},
             {"text": "stressful", "category": "situation (what causes it)"},
             {"text": "interesting", "category": "situation (what causes it)"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "-ED adjectives describe feelings. → True",
         "statements": [
             {"text": "\"The movie was very bored\" is correct.", "answer": False,
              "translation": "\"The movie was very bored\" está correto."},
             {"text": "The opposite of \"scared\" is \"scary\", not \"scaring\".", "answer": True,
              "translation": "O par de \"scared\" é \"scary\", não \"scaring\"."},
             {"text": "We say \"stressing\" for a routine that causes stress.", "answer": False,
              "translation": "Dizemos \"stressing\" para uma rotina que causa estresse."},
         ]},
    ],
}

AULA14_SOUNDS = {
    "title": "Pronunciation: -ED and -ING",
    "lesson": 14,
    "description": "O -ED dos adjetivos segue a MESMA regra de pronúncia dos verbos no passado:\n"
                   "/ɪd/ depois de T ou D: excited · interested · crowded (lotado) · open-minded (de mente aberta)\n"
                   "/t/: shocked (chocado) · stressed · relaxed — ✗ \"stress-ed\"\n"
                   "/d/: skilled (habilidoso) · concerned (preocupado) · bored · damaged (danificado) · loved · disturbed\n"
                   "HOMÓFONOS: bored (entediado) = board (quadro) → mesmo som, escrita diferente!\n"
                   "-ING: não pronunciamos o G forte; é um \"in\" alongado e suave: boring = \"bórin\" · interesting = \"íntrestin\".",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose the sound of -ED.",
         "translation": "Escolha o som do -ED.",
         "example": "excited → [/ɪd/]",
         "text": "1. crowded → [*/ɪd/|/t/|/d/]\n2. shocked → [*/t/|/d/|/ɪd/]\n3. bored → [*/d/|/ɪd/|/t/]\n"
                 "4. stressed → [*/t/|/ɪd/|/d/]\n5. interested → [*/ɪd/|/d/|/t/]\n6. concerned → [*/d/|/t/|/ɪd/]"},
        {"type": "fill",
         "prompt": "Complete with the right adjective.",
         "translation": "Complete com o adjetivo certo (-ed, -ing ou as exceções).",
         "example": "The beach was [crowded] on Sunday. (lotada)",
         "text": "1. He couldn't finish the movie because he was so [scared]. The story was very [scary].\n"
                 "2. She's so [stressed]. Her routine is very [stressful].\n"
                 "3. This exercise is [confusing]. I'm [confused]."},
        {"type": "choice",
         "prompt": "Which word sounds the same as \"bored\"?",
         "translation": "Qual palavra tem o MESMO som de \"bored\"?",
         "example": "Homófonos: escrita diferente, mesmo som.",
         "options": ["board", "bird", "bread", "boarding"],
         "correct": 0},
    ],
}

AULA14_LISTENING = {
    "title": "Listening — the horror movie",
    "lesson": 14,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: o final faz toda a diferença: -ED (\"t\", \"d\", \"id\") ou -ING (\"in\")?",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the word you hear.",
         "translation": "Ouça e escolha a palavra que você ouve.",
         "example": "Você ouve: \"boring\" → boring",
         "audio": f"{AUDIO}/aula14-words.m4a",
         "text": "1. [*bored|boring]\n2. [*interesting|interested]\n3. [*tired|tiring]\n4. [*embarrassing|embarrassed]\n"
                 "5. [*scary|scared]\n6. [*relaxed|relaxing]"},
        {"type": "info",
         "prompt": "Now listen: Fernanda and Gabriel talk about a movie.",
         "translation": "Agora ouça: a Fernanda e o Gabriel conversam sobre o filme de terror a que assistiram ontem. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula14-movie.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "They watched a [horror] movie.",
         "text": "1. How did Fernanda feel? → [*Very scared.|Bored.|Relaxed.]\n"
                 "2. What did Gabriel think of the movie? → [*It was boring.|It was frightening.|It was confusing.]\n"
                 "3. Why was Fernanda embarrassed? → [*She screamed in the cinema.|She fell asleep.|She lost her phone.]\n"
                 "4. What are they watching next time? → [*A comedy.|Another horror movie.|A documentary.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "They watched the movie yesterday. → True",
         "statements": [
             {"text": "Gabriel fell asleep during the movie.", "answer": True, "translation": "O Gabriel dormiu durante o filme."},
             {"text": "Fernanda thinks the end was surprising.", "answer": True, "translation": "A Fernanda acha que o final foi surpreendente."},
             {"text": "The cinema was empty.", "answer": False, "translation": "O cinema estava vazio."},
         ]},
    ],
}

AULA14_SPEAKING = {
    "title": "Speaking — how do you feel?",
    "lesson": 14,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: stressed = \"strést\" (sem \"ed\") · bored = \"bórd\" · boring = \"bórin\".",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat: -ed and -ing.",
         "translation": "Ouça e repita os pares -ed / -ing da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula14-say-w{i}.m4a"} for i, t in enumerate(
             ["excited, exciting", "interested, interesting", "surprised, surprising", "bored, boring",
              "confused, confusing", "frightened, frightening", "embarrassed, embarrassing", "tired, tiring",
              "scared, scary", "stressed, stressful"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases.",
         "example": "\"The movie was so boring that I fell asleep.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula14-say-s{i}.m4a"} for i, t in enumerate(
             ["The movie was so interesting that I watched it twice.", "She has nothing to do. She is bored.",
              "The movie was so boring that I fell asleep.", "The beach was crowded on Sunday.",
              "She's so stressed. Her routine is very stressful."], 1)]},
        {"type": "speak",
         "prompt": "Now answer about YOU.",
         "translation": "Agora responda sobre VOCÊ.",
         "example": "\"What's a boring thing for you?\" → \"Cleaning the house is boring.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula14-say-y{i}.m4a"} for i, t in enumerate(
             ["What's something boring for you?", "When do you feel tired?", "What's the most interesting movie you know?",
              "What makes you stressed?"], 1)]},
    ],
}

AULA14_READING = {
    "title": "Reading — my first day at work",
    "lesson": 14,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto da Patrícia sobre o primeiro dia dela num emprego novo. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula14-reading.m4a",
         "text": "MY FIRST DAY AT WORK\n\n"
                 "Last Monday was my first day at a new company. I was so excited, but I was also a little frightened.\n"
                 "The morning was very interesting. My boss showed me the office, and I met a lot of people. "
                 "Then I had a training session about the computer system. It was really confusing, and I was confused all "
                 "afternoon!\n"
                 "At lunch, something embarrassing happened: I dropped my coffee on my new boss's shoes. "
                 "I was so embarrassed!\n"
                 "But my boss laughed and said, \"Don't worry!\" That was surprising.\n"
                 "At the end of the day, I was tired, but happy. It was a tiring day, but a good one."},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "How did Patrícia feel in the morning? → [Excited and a little frightened.]",
         "text": "1. How was the training session? → [*Confusing.|Boring.|Exciting.]\n"
                 "2. What embarrassing thing happened? → [*She dropped coffee on her boss's shoes.|She arrived late.|"
                 "She forgot her boss's name.]\n"
                 "3. Why was it surprising? → [*Her boss laughed.|Her boss was angry.|Her boss cried.]\n"
                 "4. How did she feel at the end of the day? → [*Tired, but happy.|Bored.|Stressed and sad.]"},
        {"type": "fill",
         "prompt": "Complete with -ed or -ing, according to the text.",
         "translation": "Complete com a palavra -ed ou -ing, de acordo com o texto.",
         "example": "I was so [excited].",
         "text": "1. The morning was very [interesting].\n2. I was [confused] all afternoon.\n"
                 "3. Something [embarrassing] happened.\n4. It was a [tiring] day."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "It was Patrícia's first day. → True",
         "statements": [
             {"text": "The computer system was easy.", "answer": False, "translation": "O sistema do computador era fácil."},
             {"text": "Her boss wasn't angry.", "answer": True, "translation": "O chefe dela não ficou bravo."},
         ]},
    ],
}

AULA14_WRITING = {
    "title": "Writing — feelings and situations",
    "lesson": 14,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ -ED: como a pessoa se sente (I was bored) · -ING: a situação (the class was boring).\n"
                   "Exceções: scared / scary · stressed / stressful.",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "O filme foi chato. → The movie was boring.",
         "text": "1. Eu estou muito cansado. → [I'm very tired.|I am very tired.]\n"
                 "2. O livro é interessante. → [The book is interesting.]\n"
                 "3. Ela ficou envergonhada. → [She was embarrassed.|She felt embarrassed.]"},
        {"type": "free",
         "prompt": "Write about a day you remember: a trip, a party, a test, a first day… How was the situation? "
                   "How did you feel? Use at least four -ed / -ing adjectives.",
         "translation": "Escreva sobre um dia de que você se lembra (uma viagem, festa, prova, primeiro dia…). Como foi a "
                        "situação? Como você se sentiu? Use pelo menos quatro adjetivos -ed / -ing.",
         "example": "My first English test was very stressful.",
         "model_answer": "My first English test was very stressful. I was so stressed the night before!\n"
                         "The first part was confusing, and I was confused.\n"
                         "But the reading was interesting, about a trip to Peru.\n"
                         "When I got my grade, I was surprised: 9.5! I was tired, but very excited.",
         "keywords": ["stressed", "confused", "interesting", "surprised"], "min_words": 30, "points": 4},
    ],
}


AULA14_VIDEO = _video(14, AULA14_TOPIC, "Video — A day at the amusement park",
                      "a Sarah conta o dia no parque de diversões com adjetivos -ed e -ing.",
                      "aula14-video", [
    _q("Complete: The roller coaster was so ___.", "Complete: a montanha-russa foi tão ___.", "exciting", "excited", "excite", "excitement"),
    _q("Complete: My brother was really ___.", "Complete: meu irmão ficou muito ___ (com medo).", "scared", "scary", "scaring", "scare"),
    _q("How did Sarah feel in the line?", "Como a Sarah se sentiu na fila?", "Bored.", "Boring.", "Excited.", "Scary."),
    _q("Complete: It was a ___ day.", "Complete: foi um dia ___ (cansativo).", "tiring", "tired", "tire", "tiredness"),
])

# ---------- Aula 15 — Parts of the Body (https://youtu.be/UBKOVhbIyvU) ----------

AULA15_TOPIC = "Aula 15 — Parts of the Body"

AULA15_VOCAB = {
    "title": "Parts of the body",
    "lesson": 15,
    "description": "head (cabeça — H aspirado!) · face (rosto) · eyes (olhos — \"áiz\") · ears (orelhas) · nose (nariz) · "
                   "mouth (boca) · lips (lábios) · teeth (dentes) · tongue (língua) · neck (pescoço) · shoulders (ombros) · "
                   "back (costas — backpack = mochila) · belly (barriga) · arms (braços — armchair = poltrona) · "
                   "hand (mão) · fingers (dedos das MÃOS) · legs (pernas) · knees (joelhos) · foot (pé) · "
                   "toes (dedos dos PÉS)\n"
                   "Música infantil: Head, shoulders, knees and toes! (cabeça, ombro, joelho e pé)",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the parts of the body to Portuguese.",
         "translation": "Ligue as partes do corpo ao português.",
         "example": "head → cabeça",
         "pairs": [
             {"left": "neck", "right": "pescoço"},
             {"left": "shoulders", "right": "ombros"},
             {"left": "back", "right": "costas"},
             {"left": "belly", "right": "barriga"},
             {"left": "knees", "right": "joelhos"},
             {"left": "tongue", "right": "língua"},
             {"left": "lips", "right": "lábios"},
             {"left": "toes", "right": "dedos dos pés"},
         ]},
        {"type": "group",
         "prompt": "Head or body? Put each word in the right group.",
         "translation": "Cabeça (head) ou resto do corpo (body)? Coloque cada palavra no grupo certo.",
         "example": "nose → head · knees → body",
         "categories": ["head", "body"],
         "words": [
             {"text": "mouth", "category": "head"}, {"text": "eyes", "category": "head"}, {"text": "ears", "category": "head"},
             {"text": "teeth", "category": "head"}, {"text": "face", "category": "head"},
             {"text": "arms", "category": "body"}, {"text": "hand", "category": "body"}, {"text": "legs", "category": "body"},
             {"text": "fingers", "category": "body"}, {"text": "foot", "category": "body"},
         ]},
        {"type": "fill",
         "prompt": "Write the English word.",
         "translation": "Escreva a palavra em inglês.",
         "example": "nariz → nose",
         "text": "1. boca → [mouth]\n2. mão → [hand]\n3. orelhas → [ears]\n4. pernas → [legs]\n5. braços → [arms]\n"
                 "6. rosto → [face]"},
    ],
}

AULA15_DETAILS = {
    "title": "Tricky words: feet, teeth, knees…",
    "lesson": 15,
    "description": "PLURAIS IRREGULARES (sem S!): one foot → two FEET · one tooth → my TEETH\n"
                   "FINGERS × TOES: fingers = dedos das mãos · toes = dedos dos pés (\"tôuz\")\n"
                   "LETRA MUDA: knees → o K não é pronunciado (\"níiz\") — KN no começo: know, knife, knee\n"
                   "PRONÚNCIA: eyes = \"áiz\" · head = \"réd\" com H soprado · tongue = \"tâng\"\n"
                   "Exercício da aula: I can see with my eyes. · I can hear with my ears. · I can write with my hand. · "
                   "When I was a baby, I couldn't walk on my feet. · I can smell with my nose. · "
                   "When I was younger, I could touch my toes with my fingers.",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Complete the sentences with the parts of the body.",
         "translation": "Complete as frases com as partes do corpo (exercício da aula).",
         "example": "I can see with my [eyes].",
         "text": "1. I can hear with my [*ears|eyes|teeth].\n2. I can write with my [*hand|foot|knees].\n"
                 "3. When I was a baby, I couldn't walk on my [*feet|foots|hands].\n4. I can smell with my [*nose|mouth|ears].\n"
                 "5. When I was younger, I could touch my [*toes|fingers|ears] with my [*fingers|toes|lips]."},
        {"type": "fill",
         "prompt": "Singular or plural? Complete.",
         "translation": "Singular ou plural? Complete (atenção aos plurais irregulares!).",
         "example": "one hand → two [hands]",
         "text": "1. one foot → two [feet]\n2. one tooth → many [teeth]\n3. one knee → two [knees]\n4. one finger → ten [fingers]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Toes\" are on your feet. → True",
         "statements": [
             {"text": "We pronounce the K in \"knees\".", "answer": False, "translation": "Pronunciamos o K em \"knees\"."},
             {"text": "\"Fingers\" are on our hands.", "answer": True, "translation": "\"Fingers\" ficam nas mãos."},
             {"text": "The plural of \"foot\" is \"foots\".", "answer": False, "translation": "O plural de \"foot\" é \"foots\"."},
             {"text": "A backpack is a bag you carry on your back.", "answer": True,
              "translation": "Backpack é uma bolsa que você carrega nas costas."},
         ]},
    ],
}

AULA15_LISTENING = {
    "title": "Listening — the yoga class",
    "lesson": 15,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: ouça com atenção os plurais: foot / feet · tooth / teeth.",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the word you hear.",
         "translation": "Ouça e escolha a palavra que você ouve.",
         "example": "Você ouve: \"head\" → head",
         "audio": f"{AUDIO}/aula15-words.m4a",
         "text": "1. [*knees|nose]\n2. [*teeth|tooth]\n3. [*toes|toast]\n4. [*mouth|month]\n5. [*feet|foot]\n6. [*back|bag]"},
        {"type": "info",
         "prompt": "Now listen to a yoga teacher.",
         "translation": "Agora ouça uma professora de yoga dando instruções para os alunos. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula15-yoga.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "This is a [yoga] class.",
         "text": "1. First, the students close their [*eyes.|mouths.|hands.]\n"
                 "2. They put their hands on their [*belly.|head.|knees.]\n"
                 "3. Then they move their [*shoulders and neck.|legs and feet.|arms and fingers.]\n"
                 "4. At the end, they try to touch their [*toes with their fingers.|nose with their tongue.|ears.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the audio.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o áudio.",
         "example": "The teacher is calm. → True",
         "statements": [
             {"text": "The students breathe through their nose.", "answer": True,
              "translation": "Os alunos respiram pelo nariz."},
             {"text": "The teacher says: \"Bend your knees a lot.\"", "answer": False,
              "translation": "A professora diz: \"Dobrem bastante os joelhos.\""},
         ]},
    ],
}

AULA15_SPEAKING = {
    "title": "Speaking — head, shoulders, knees and toes",
    "lesson": 15,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: aula de vocabulário = muita repetição! Toque na parte do corpo enquanto fala.",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the 20 words of the lesson.",
         "translation": "Ouça e repita as 20 palavras da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula15-say-w{i}.m4a"} for i, t in enumerate(
             ["mouth, head, toes, neck", "hand, arms, foot, back", "face, belly, teeth, shoulders",
              "eyes, fingers, tongue, ears", "legs, nose, knees, lips"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "\"I can see with my eyes.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula15-say-s{i}.m4a"} for i, t in enumerate(
             ["Head, shoulders, knees and toes.", "I can see with my eyes.", "I can hear with my ears.",
              "I can smell with my nose.", "When I was a baby, I couldn't walk on my feet.",
              "When I was younger, I could touch my toes with my fingers."], 1)]},
    ],
}

AULA15_READING = {
    "title": "Reading — the soccer player's body",
    "lesson": 15,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto sobre um jogador de futebol e as partes do corpo que ele mais usa. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula15-reading.m4a",
         "text": "THE SOCCER PLAYER'S BODY\n\n"
                 "Rafael is a professional soccer player. His most important tools are his legs and feet. "
                 "He kicks the ball with his right foot, but he can use his left foot, too.\n"
                 "He also uses his head a lot to score goals. Goalkeepers are different: they use their hands and arms.\n"
                 "Rafael takes care of his body. Every morning, he stretches his back, his shoulders and his neck. "
                 "He has a strong belly from a lot of exercise.\n"
                 "Last year, he had a problem with his left knee. He couldn't play for three months! "
                 "Now his knee is fine, and he can run again.\n"
                 "And his smile? He has perfect white teeth — he goes to the dentist every six months!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "What does Rafael do? → [He's a soccer player.]",
         "text": "1. What are his most important tools? → [*His legs and feet.|His hands and arms.|His eyes.]\n"
                 "2. Who uses their hands and arms? → [*Goalkeepers.|Rafael.|Dentists.]\n"
                 "3. What problem did he have last year? → [*A problem with his left knee.|A problem with his teeth.|"
                 "A problem with his back.]\n"
                 "4. How often does he go to the dentist? → [*Every six months.|Every month.|Every year.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Rafael stretches every morning. → True",
         "statements": [
             {"text": "Rafael can only kick with his right foot.", "answer": False,
              "translation": "O Rafael só consegue chutar com o pé direito."},
             {"text": "He couldn't play for three months.", "answer": True, "translation": "Ele não pôde jogar por três meses."},
         ]},
        {"type": "fill",
         "prompt": "Find the parts of the body in the text.",
         "translation": "Encontre no texto as partes do corpo.",
         "example": "pés → [feet]",
         "text": "1. joelho → [knee]\n2. dentes → [teeth]\n3. costas → [back]\n4. pescoço → [neck]"},
    ],
}

AULA15_WRITING = {
    "title": "Writing — my body and me",
    "lesson": 15,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Crie frases com o vocabulário: I can… with my… · When I was a child, I could / couldn't…",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Complete the sentences.",
         "translation": "Complete as frases com a parte do corpo certa.",
         "example": "I can see with my [eyes].",
         "text": "1. I can taste food with my [tongue].\n2. I carry my backpack on my [back].\n"
                 "3. I brush my [teeth] three times a day.\n4. I wear a ring on my [finger]."},
        {"type": "free",
         "prompt": "Write about you and your body: What can you do with your hands, feet, eyes…? "
                   "What could you do when you were a child? Use at least 6 parts of the body.",
         "translation": "Escreva sobre você e o seu corpo: o que você consegue fazer com as mãos, pés, olhos…? "
                        "O que você conseguia fazer quando era criança? Use pelo menos 6 partes do corpo.",
         "example": "I can play the guitar with my fingers.",
         "model_answer": "I can play the guitar with my fingers, and I can dance with my feet.\n"
                         "I wear glasses, because I can't see very well with my eyes.\n"
                         "When I was a child, I could touch my toes with my fingers.\n"
                         "Now my back and my knees hurt when I run!",
         "keywords": ["fingers", "feet", "eyes", "back"], "min_words": 30, "points": 4},
    ],
}


AULA15_VIDEO = _video(15, AULA15_TOPIC, "Video — Let's stretch!",
                      "a Sarah conduz uma aula de alongamento: siga as instruções com as partes do corpo.",
                      "aula15-video", [
    _q("What do you put up first?", "O que você levanta primeiro?", "Your arms.", "Your legs.", "Your toes.", "Your head."),
    _q("What do you move slowly?", "O que você move devagar?", "Your shoulders and your neck.", "Your knees and feet.", "Your eyes.", "Your tongue."),
    _q("What do you move when you look at your feet?", "O que você mexe olhando para os pés?", "Your toes.", "Your fingers.", "Your ears.", "Your lips."),
    _q("What do you bend a little?", "O que você dobra um pouco?", "Your knees.", "Your nose.", "Your teeth.", "Your back."),
])

# ---------- Aula 16 — Can & Could (https://youtu.be/l33Kbd1FAVc) ----------

AULA16_TOPIC = "Aula 16 — Can & Could"

AULA16_FORMS = {
    "title": "Can (present) and could (past)",
    "lesson": 16,
    "description": "CAN e COULD são MODAL VERBS: iguais para todos os sujeitos (sem S), sem do / does / did.\n"
                   "CAN → presente: habilidade, possibilidade, permissão, pedido: She can drive. · It can rain today. · "
                   "Can I use your phone?\n"
                   "COULD → passado (habilidade no passado) e pedidos EDUCADOS: I could swim when I was younger. · "
                   "Could you help me? (Você poderia me ajudar?)\n"
                   "NEGATIVE: can't (cannot) · couldn't (could not): He can't sing. · I couldn't swim when I was five.\n"
                   "QUESTION: inverta a ordem → Can I…? · Could you…? → Yes, I can. / No, I couldn't.\n"
                   "Pronúncia: could = \"kud\" — o L é MUDO e o OU é curtinho.\n"
                   "Can não tem futuro (para o futuro usamos outra estrutura, nas próximas aulas).",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose the correct option (exercise from the lesson).",
         "translation": "Escolha a opção correta (exercício da aula).",
         "example": "When I lived by the sea, I [could] swim every morning.",
         "text": "1. When I lived by the sea, I [*could|can] swim every morning.\n"
                 "2. [*Could|Can] you read before you started school?\n"
                 "3. He's only seven months old, so he [*can't|couldn't] walk yet.\n"
                 "4. They ran as fast as they [*could|can].\n"
                 "5. The room is too noisy, so I [*can't|couldn't] concentrate."},
        {"type": "fill",
         "prompt": "Complete the dialogue with can, can't, could or couldn't.",
         "translation": "Complete o diálogo da aula com can, can't, could ou couldn't.",
         "example": "[Could] you lift this weight before?",
         "text": "A: Hey, you look stronger. [Could] you lift this weight before?\n"
                 "B: No, I [couldn't]. But now I [can] lift it easily.\n"
                 "A: That's great. I [can't] do that yet.\n"
                 "B: Don't worry. You [can] with more practice!"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "Could is the past of can. → True",
         "statements": [
             {"text": "We pronounce the L in \"could\".", "answer": False, "translation": "Pronunciamos o L em \"could\"."},
             {"text": "\"She cans drive\" is correct.", "answer": False, "translation": "\"She cans drive\" está correto."},
             {"text": "\"Could you help me?\" is more polite than \"Can you help me?\".", "answer": True,
              "translation": "\"Could you help me?\" é mais educado do que \"Can you help me?\"."},
             {"text": "We don't use DO or DID with can and could.", "answer": True,
              "translation": "Não usamos DO ou DID com can e could."},
         ]},
    ],
}

AULA16_USES = {
    "title": "Ability, permission and polite requests",
    "lesson": 16,
    "description": "Usos de CAN: ability (habilidade): He can swim. · possibility: It can rain today. · "
                   "permission: Can I go to the bathroom? · request: Can you open the door?\n"
                   "Usos de COULD: past ability: When I was a child, I could swim. · permission no passado: "
                   "When I was a child, I couldn't stay up late. (não podia) · polite request: Could I go to the bathroom? "
                   "(mais educado)",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "Ability, permission or polite request?",
         "translation": "Habilidade, permissão ou pedido educado? Coloque cada frase no grupo certo.",
         "example": "He can swim. → ability",
         "categories": ["ability", "permission", "polite request"],
         "words": [
             {"text": "She can drive very well.", "category": "ability"},
             {"text": "I could swim when I was five.", "category": "ability"},
             {"text": "Can I use your phone?", "category": "permission"},
             {"text": "When I was a child, I couldn't stay up late.", "category": "permission"},
             {"text": "Could you help me, please?", "category": "polite request"},
             {"text": "Could you open the window, please?", "category": "polite request"},
         ]},
        {"type": "order",
         "prompt": "Put the words in order to make a polite question.",
         "translation": "Coloque as palavras em ordem para fazer um pedido educado. (Eu poderia ir ao banheiro?)",
         "example": "you / Could / me / help → Could you help me?",
         "tokens": ["Could", "I", "go", "to", "the", "bathroom?"], "alternatives": []},
        {"type": "fill",
         "prompt": "Complete with can, can't, could or couldn't to make the sentences true for you.",
         "translation": "Complete com can, can't, could ou couldn't para as frases serem verdadeiras para você "
                        "(exercício da aula). Qualquer resposta coerente vale!",
         "example": "I [can] speak English very well now.",
         "text": "1. When I was a child, I [could|couldn't] swim.\n2. I [can|can't] cook very well.\n"
                 "3. When I was a child, I [could|couldn't] stay up late.\n4. I [can|can't] drive."},
        {"type": "choice",
         "prompt": "You are at a restaurant. What's the most polite way to ask?",
         "translation": "Você está num restaurante. Qual é o jeito mais educado de pedir?",
         "example": "could → mais educado",
         "options": ["Could I have the menu, please?", "Give me the menu.", "I can the menu?", "Do you could give me the menu?"],
         "correct": 0},
    ],
}

AULA16_LISTENING = {
    "title": "Listening — when you were a child",
    "lesson": 16,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: can (\"kən\", fraco) × can't (\"kænt\", forte e longo). O T de can't às vezes quase some — "
                   "ouça a vogal!",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"I can swim.\" → can",
         "audio": f"{AUDIO}/aula16-words.m4a",
         "text": "1. She [*can|can't] drive.\n2. He [*can't|can] sing.\n3. I [*could|couldn't] swim.\n4. They [*couldn't|could] come.\n"
                 "5. [*Could|Can] you help me?"},
        {"type": "info",
         "prompt": "Now listen: two friends talk about swimming.",
         "translation": "Agora ouça: dois amigos conversam sobre nadar, antes e agora (o segundo diálogo da aula). "
                        "Depois complete abaixo.",
         "audio": f"{AUDIO}/aula16-swim.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois complete abaixo."},
        {"type": "fill",
         "prompt": "Listen again and complete the dialogue.",
         "translation": "Ouça de novo e complete o diálogo com can, can't, could ou couldn't.",
         "example": "When you were a child, [could] you swim?",
         "text": "A: When you were a child, [could] you swim?\nB: No, I [couldn't]. I was afraid of water.\n"
                 "A: Really? I [could] swim when I was five.\nB: Wow. I [couldn't] even go into the pool!\n"
                 "A: And now, [can] you swim?\nB: Yes, now I [can] swim very well!"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Person B was afraid of water. → True",
         "statements": [
             {"text": "Person A could swim at five.", "answer": True, "translation": "A pessoa A sabia nadar aos cinco anos."},
             {"text": "Person B can't swim now.", "answer": False, "translation": "A pessoa B não sabe nadar agora."},
         ]},
    ],
}

AULA16_SPEAKING = {
    "title": "Speaking — I can, I couldn't",
    "lesson": 16,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: could = \"kud\" (sem L!) · can't = \"kænt\" (vogal aberta).",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula16-say-s{i}.m4a"} for i, t in enumerate(
             ["could, couldn't", "can, can't", "She can drive.", "I could swim when I was younger.",
              "He can't sing.", "I couldn't swim when I was five.", "Can I use your phone?", "Could you help me?"], 1)]},
        {"type": "speak",
         "prompt": "Now answer about YOU.",
         "translation": "Agora responda sobre VOCÊ.",
         "example": "\"Could you swim when you were a child?\" → \"Yes, I could.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula16-say-y{i}.m4a"} for i, t in enumerate(
             ["Could you swim when you were a child?", "Could you read before you started school?",
              "Can you cook very well?", "Can you drive?", "What can you do now that you couldn't do as a child?"], 1)]},
    ],
}

AULA16_READING = {
    "title": "Reading — my grandmother, then and now",
    "lesson": 16,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto do Pedro sobre a avó dele, antes e agora. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula16-reading.m4a",
         "text": "MY GRANDMOTHER, THEN AND NOW\n\n"
                 "My grandmother Helena is 82, and she's amazing!\n"
                 "When she was young, she lived on a farm. She could ride a horse, and she could cook for twenty people. "
                 "But she couldn't go to school after the age of ten, so she couldn't read very well.\n"
                 "At sixty, she decided to study. Now she can read books and newspapers, and she can write long letters to me!\n"
                 "Two years ago, she bought a smartphone. At first, she couldn't use it. Now she can send messages, "
                 "make video calls and watch cooking videos.\n"
                 "There's one thing she can't do: she can't stay awake after nine o'clock!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "How old is Helena? → [82.]",
         "text": "1. What could she do when she was young? → [*Ride a horse and cook for twenty people.|Read very well.|"
                 "Use a smartphone.]\n"
                 "2. Why couldn't she read very well? → [*She stopped school at ten.|She didn't like books.|She lived in a city.]\n"
                 "3. When did she decide to study? → [*At sixty.|At ten.|Two years ago.]\n"
                 "4. What can't she do? → [*Stay awake after nine.|Send messages.|Read newspapers.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Helena lived on a farm. → True",
         "statements": [
             {"text": "She could use the smartphone on the first day.", "answer": False,
              "translation": "Ela conseguiu usar o smartphone no primeiro dia."},
             {"text": "Now she can make video calls.", "answer": True, "translation": "Agora ela consegue fazer chamadas de vídeo."},
         ]},
        {"type": "fill",
         "prompt": "Complete with can, can't, could or couldn't, according to the text.",
         "translation": "Complete com can, can't, could ou couldn't, de acordo com o texto.",
         "example": "She [could] ride a horse.",
         "text": "1. She [couldn't] go to school after the age of ten.\n2. Now she [can] read books.\n"
                 "3. At first, she [couldn't] use the smartphone."},
    ],
}

AULA16_WRITING = {
    "title": "Writing — then and now",
    "lesson": 16,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ When I was a child, I could / couldn't… · Now I can / can't…\n"
                   "Pedidos educados: Could you…? · Could I…?",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Ela sabe dirigir. → She can drive.",
         "text": "1. Eu não sabia nadar quando tinha cinco anos. → [I couldn't swim when I was five.|"
                 "I could not swim when I was five.]\n"
                 "2. Você poderia me ajudar? → [Could you help me?]\n"
                 "3. Ele não sabe cantar. → [He can't sing.|He cannot sing.|He can not sing.]"},
        {"type": "free",
         "prompt": "Write about you: things you could and couldn't do when you were a child, and things you can and "
                   "can't do now.",
         "translation": "Escreva sobre você: coisas que você conseguia ou não fazer quando era criança e coisas que consegue "
                        "ou não fazer agora.",
         "example": "When I was a child, I could ride a bike.",
         "model_answer": "When I was a child, I could ride a bike, but I couldn't swim.\n"
                         "I couldn't stay up late, and I couldn't eat a lot of candy.\n"
                         "Now I can swim very well, and I can speak a little English.\n"
                         "But I can't cook very well, and I can't touch my toes anymore!",
         "keywords": ["could", "couldn't", "can", "can't"], "min_words": 30, "points": 4},
    ],
}


AULA16_VIDEO = _video(16, AULA16_TOPIC, "Video — Then and now",
                      "a Sarah compara o que ela conseguia fazer quando criança com o que consegue fazer agora.",
                      "aula16-video", [
    _q("Could Sarah swim when she was a child?", "A Sarah sabia nadar quando era criança?", "No, she couldn't.", "Yes, she could.", "No, she can't.", "Yes, she can."),
    _q("What could she do very well?", "O que ela conseguia fazer muito bem?", "Climb trees and rocks.", "Swim.", "Drive.", "Tell stories."),
    _q("Complete: Now I ___ swim very well.", "Complete: agora eu ___ nadar muito bem.", "can", "could", "can't", "couldn't"),
    _q("What can't her grandmother do?", "O que a avó dela não consegue fazer?", "Walk very fast.", "Tell stories.", "Talk.", "Read."),
])

# ---------- Aula 17 — Be Able To (https://youtu.be/8PSSuxXP98g) ----------

AULA17_TOPIC = "Aula 17 — Be Able To"

AULA17_FORMS = {
    "title": "Be able to: present, past and future",
    "lesson": 17,
    "description": "BE ABLE TO = ser capaz de / conseguir (habilidade e possibilidade). Parecido com CAN, mas funciona em "
                   "TODOS os tempos verbais — CAN só tem presente (can) e passado (could)!\n"
                   "PRESENT: She is able to dance salsa. · She isn't able to… · Is she able to…? Yes, she is. / No, she isn't.\n"
                   "PAST: He was able to speak Japanese. · He wasn't able to… · Was he able to…? Yes, he was. / No, he wasn't.\n"
                   "FUTURE (só com be able to!): They will be able to scuba dive. · She won't be able to… · "
                   "They're going to be able to… · Will she be able to…?\n"
                   "Be able to soa um pouco mais FORMAL; no dia a dia, can / could são mais comuns no presente e passado.\n"
                   "Pronúncia: able = \"êibəl\" (como table) · able to = \"êibəl tə\" (o TO é fraquinho).",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta.",
         "example": "She [is able to] dance salsa.",
         "text": "1. He [*was able to|were able to|is able] speak Japanese when he lived in Tokyo.\n"
                 "2. They [*will be able to|will able to|will can] scuba dive next summer.\n"
                 "3. [*Is she able to|Does she able to|Is she able] ride a horse? — Yes, she is.\n"
                 "4. I'm sorry, I [*won't be able to|won't can|not will be able to] come to your party.\n"
                 "5. [*Was he able to|Did he able to|Was he able] finish the race? — No, he wasn't."},
        {"type": "dropdown",
         "prompt": "Choose the correct option. If both are possible, choose \"both\".",
         "translation": "Escolha a opção correta. Se as duas forem possíveis, escolha \"both\" (exercício da aula).",
         "example": "I [both: can't / am not able to] hear you very well.",
         "text": "1. I can't / am not able to hear you very well. The connection is terrible. → [*both|only can't|only am not able to]\n"
                 "2. She's much better after her operation. She ___ walk again in a few months. → "
                 "[*will be able to|will can|both]\n"
                 "3. Our team can / is able to answer clients much faster now. → [*both|only can|only is able to]\n"
                 "4. We ___ go on holiday this year. We need to spend money on the house. → "
                 "[*won't be able to|can't will|both]"},
        {"type": "fill",
         "prompt": "Rewrite with be able to.",
         "translation": "Reescreva com be able to.",
         "example": "She can dance salsa. → She is able to dance salsa.",
         "text": "1. She can't dance salsa. → [She isn't able to dance salsa.|She is not able to dance salsa.|"
                 "She's not able to dance salsa.]\n"
                 "2. He could speak Japanese. → [He was able to speak Japanese.]\n"
                 "3. Could he speak Japanese? → [Was he able to speak Japanese?]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "We can use be able to in the future. → True",
         "statements": [
             {"text": "We can say \"I will can swim\".", "answer": False, "translation": "Podemos dizer \"I will can swim\"."},
             {"text": "\"Be able to\" sounds a little more formal than \"can\".", "answer": True,
              "translation": "\"Be able to\" soa um pouco mais formal do que \"can\"."},
             {"text": "In \"able to\", the TO is strong and long.", "answer": False,
              "translation": "Em \"able to\", o TO é forte e longo."},
         ]},
    ],
}

AULA17_COULD = {
    "title": "Could or was able to?",
    "lesson": 17,
    "description": "No PASSADO, em frases AFIRMATIVAS:\n"
                   "COULD → habilidade GERAL no passado: I could swim well when I was a child. · I could climb trees quickly.\n"
                   "WAS / WERE ABLE TO → algo que você CONSEGUIU numa situação ESPECÍFICA (uma conquista):\n"
                   "  I was able to buy the car cheaply. · I was able to win the gold medal. · "
                   "The exit was blocked, but we were able to escape. · After three attempts, I was able to unlock the door.\n"
                   "Exceção: com verbos dos SENTIDOS (feel, hear, see, smell), could serve para situações específicas: "
                   "I could hear my father's voice cheering me on.\n"
                   "Na NEGATIVA, tanto faz: I wasn't able to swim well. = I couldn't swim well.",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Could or was / were able to?",
         "translation": "Could (habilidade geral) ou was / were able to (conquista específica)?",
         "example": "I [could] climb trees quickly when I was a kid.",
         "text": "1. I [*could|was able to] swim well when I was a child.\n"
                 "2. The firefighters [*were able to|could] rescue everyone before the building collapsed.\n"
                 "3. She [*was able to|could] catch the last train by running to the platform.\n"
                 "4. He [*was able to|could] pass the exam after months of studying.\n"
                 "5. I [*could|was able to] feel the water all around me. (verbo de sentido)"},
        {"type": "match",
         "prompt": "Match the sentences to Portuguese.",
         "translation": "Ligue as frases ao português.",
         "example": "I was able to win the gold medal. → Eu consegui ganhar a medalha de ouro.",
         "pairs": [
             {"left": "I was able to buy the car cheaply.", "right": "Eu consegui comprar o carro barato."},
             {"left": "We were able to escape.", "right": "Nós conseguimos escapar."},
             {"left": "I could hear my father's voice.", "right": "Eu conseguia ouvir a voz do meu pai."},
             {"left": "I wasn't able to swim well.", "right": "Eu não conseguia nadar bem."},
         ]},
        {"type": "choice",
         "prompt": "You lost your keys, but after one hour you found them. What do you say?",
         "translation": "Você perdeu as chaves, mas depois de uma hora encontrou. O que você fala? (conquista específica)",
         "example": "Situação específica → was able to",
         "options": ["After an hour, I was able to find my keys.", "After an hour, I can find my keys.",
                     "After an hour, I will able to find my keys.", "After an hour, I am able find my keys."],
         "correct": 0},
    ],
}

AULA17_LISTENING = {
    "title": "Listening — things I wasn't able to learn",
    "lesson": 17,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: \"able to\" soa \"êibəltə\". Preste atenção no tempo: is / was / will be able to.",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose: present, past or future?",
         "translation": "Ouça e escolha: presente, passado ou futuro?",
         "example": "Você ouve: \"I'll be able to help you.\" → future",
         "audio": f"{AUDIO}/aula17-tenses.m4a",
         "text": "1. [*past|present|future]\n2. [*future|past|present]\n3. [*present|future|past]\n4. [*future|present|past]\n"
                 "5. [*past|present|future]"},
        {"type": "info",
         "prompt": "Now listen: Marcos talks about something he wasn't able to learn.",
         "translation": "Agora ouça: o Marcos responde à pergunta da aula: \"Is there anything you tried to learn but you "
                        "weren't able to?\". Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula17-guitar.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Marcos tried to learn the [guitar].",
         "text": "1. Why did he want to learn? → [*He loved a famous rock band.|His father was a musician.|For his job.]\n"
                 "2. What wasn't he able to do? → [*Move his fingers fast enough.|Read music.|Buy a guitar.]\n"
                 "3. What was he able to play after a year? → [*Three easy songs.|A whole concert.|Nothing.]\n"
                 "4. What is he going to try now? → [*The drums.|The piano.|Singing.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the audio.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o áudio.",
         "example": "Marcos took guitar classes. → True",
         "statements": [
             {"text": "Marcos thinks he will be able to play in a band one day.", "answer": False,
              "translation": "O Marcos acha que vai conseguir tocar numa banda um dia."},
             {"text": "His teacher was very patient.", "answer": True, "translation": "O professor dele era muito paciente."},
         ]},
    ],
}

AULA17_SPEAKING = {
    "title": "Speaking — I wasn't able to…",
    "lesson": 17,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: able to = \"êibəl tə\" — treine os dois juntos, bem ligados.",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula17-say-s{i}.m4a"} for i, t in enumerate(
             ["able, able to", "She is able to dance salsa.", "I'm not able to ride a horse.",
              "He was able to speak Japanese.", "They will be able to scuba dive.",
              "She won't be able to scuba dive.", "I was able to win the gold medal."], 1)]},
        {"type": "speak",
         "prompt": "Now answer about YOU.",
         "translation": "Agora responda sobre VOCÊ.",
         "example": "\"Is there anything you tried to learn, but you weren't able to?\" → \"Yes. I wasn't able to learn to skate.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula17-say-y{i}.m4a"} for i, t in enumerate(
             ["Is there anything you tried to learn, but you weren't able to?", "Are you able to ride a horse?",
              "What will you be able to do after this English course?", "What were you able to do last year?"], 1)]},
    ],
}

AULA17_READING = {
    "title": "Reading — the marathon",
    "lesson": 17,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto da Cláudia sobre a primeira maratona dela. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula17-reading.m4a",
         "text": "MY FIRST MARATHON\n\n"
                 "Three years ago, I wasn't able to run for five minutes. I was always tired!\n"
                 "Then a friend invited me to a running group. In the beginning, it was very hard. "
                 "After two months, I was able to run five kilometers without stopping.\n"
                 "Last year, I decided to try a marathon: 42 kilometers! On the day of the race, it was very hot. "
                 "At kilometer 30, my legs hurt a lot, but I could hear my family cheering for me.\n"
                 "After four hours and fifty minutes, I was able to finish the race. I cried!\n"
                 "Now I'm training for a marathon in Chile. I hope I'll be able to finish it in less than four and a half hours."},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Three years ago, Cláudia [wasn't able to run for five minutes].",
         "text": "1. After two months, she [*was able to run 5 km without stopping.|was able to run a marathon.|stopped running.]\n"
                 "2. At kilometer 30, she [*could hear her family.|stopped the race.|was able to run faster.]\n"
                 "3. How long did the marathon take? → [*4 hours and 50 minutes.|4 and a half hours.|3 hours.]\n"
                 "4. What does she hope? → [*She'll be able to finish in less than 4.5 hours.|She'll win the race.|"
                 "She won't run again.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "It was very hot on the day of the race. → True",
         "statements": [
             {"text": "Cláudia wasn't able to finish the marathon.", "answer": False,
              "translation": "A Cláudia não conseguiu terminar a maratona."},
             {"text": "Her next marathon is in Chile.", "answer": True, "translation": "A próxima maratona dela é no Chile."},
         ]},
        {"type": "fill",
         "prompt": "Complete with the forms of be able to from the text.",
         "translation": "Complete com as formas de be able to do texto.",
         "example": "Three years ago, I [wasn't] able to run for five minutes.",
         "text": "1. After two months, I [was] able to run five kilometers.\n"
                 "2. I hope I'll [be] able to finish it in less than four and a half hours."},
    ],
}

AULA17_WRITING = {
    "title": "Writing — what I wasn't able to learn",
    "lesson": 17,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ am / is / are able to · was / were able to · will be able to / going to be able to.\n"
                   "Conquista específica no passado → was able to.",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Ela vai conseguir andar de novo. → She'll be able to walk again.",
         "text": "1. Eu consegui destrancar a porta. → [I was able to unlock the door.]\n"
                 "2. Nós não vamos conseguir ir. → [We won't be able to go.|We will not be able to go.|"
                 "We aren't going to be able to go.|We're not going to be able to go.]"},
        {"type": "free",
         "prompt": "Is there anything you tried to learn but you weren't able to? What was it? What happened? "
                   "And what do you think you will be able to do in the future?",
         "translation": "Tem alguma coisa que você tentou aprender, mas não conseguiu? O que foi? O que aconteceu? "
                        "E o que você acha que vai conseguir fazer no futuro?",
         "example": "I tried to learn to swim, but I wasn't able to.",
         "model_answer": "I tried to learn to play the piano when I was fifteen, but I wasn't able to.\n"
                         "My fingers were very slow, and I wasn't able to read music.\n"
                         "After six months, I was able to play one song, and then I stopped.\n"
                         "But I think I'll be able to speak English very well in the future!",
         "keywords": ["wasn't able to", "was able to", "be able to"], "min_words": 30, "points": 4},
    ],
}


AULA17_VIDEO = _video(17, AULA17_TOPIC, "Video — My first surf lesson",
                      "a Sarah conta a primeira aula de surfe com be able to no passado e no futuro.",
                      "aula17-video", [
    _q("In the first hour, Sarah…", "Na primeira hora, a Sarah…", "wasn't able to stand on the board.", "was able to surf big waves.", "won't be able to swim.", "didn't fall."),
    _q("Complete: After two hours, I ___ able to stand up.", "Complete: depois de duas horas, eu ___ able to ficar de pé.", "was", "were", "am", "will"),
    _q("How did she feel?", "Como ela se sentiu?", "Very happy.", "Bored.", "Angry.", "Tired and sad."),
    _q("Complete: Next summer, I'll ___ able to surf bigger waves.", "Complete: no próximo verão, eu vou ___ able to surfar ondas maiores.", "be", "is", "can", "being"),
])

# ---------- Aula 18 — May & Might (https://youtu.be/cTTzvNZSfkw) ----------

AULA18_TOPIC = "Aula 18 — May & Might"

AULA18_USES = {
    "title": "May and might: permission, possibility, wish…",
    "lesson": 18,
    "description": "MAY e MIGHT são MODAL VERBS: iguais para todos, sem TO depois (✗ may to go), sem do/does/did.\n"
                   "MAY →\n"
                   "• PERMISSION (permissão, mais educado e formal que can): May I drink some water, please? · "
                   "You may leave now. · You may go to the restroom.\n"
                   "• REQUEST (pedido educado): May I borrow your eraser? · May I have your attention, please? · "
                   "May I speak with the manager?\n"
                   "• WISH (desejo): May all your dreams come true. · May the force be with you. · "
                   "May this year bring you success.\n"
                   "• POSSIBILITY: It may rain today.\n"
                   "MIGHT →\n"
                   "• POSSIBILITY (sem certeza, \"talvez\"): It might rain later. · We might be late because of the traffic. · "
                   "She might come to the party tonight.\n"
                   "• SUGGESTION: You might try calling her. · You might want to check your email.\n"
                   "Pronúncia: may rima com day, say, play · might rima com night, right, light.",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "What does the sentence express?",
         "translation": "O que a frase expressa? (exercício da aula)",
         "example": "May I drink some water, please? → [permission]",
         "text": "1. It might rain later. → [*possibility|permission|wish]\n"
                 "2. You might try calling her. → [*suggestion|wish|request]\n"
                 "3. May all your dreams come true. → [*wish|possibility|suggestion]\n"
                 "4. May I borrow your eraser? → [*request|wish|suggestion]\n"
                 "5. You may leave now. → [*permission|wish|possibility]"},
        {"type": "group",
         "prompt": "May, might or both? (exercise from the lesson)",
         "translation": "May, might ou os dois? Coloque cada frase no grupo certo (exercício da aula).",
         "example": "It ___ snow tonight. → both",
         "categories": ["may", "might", "both"],
         "words": [
             {"text": "___ I use your phone for a minute?", "category": "may"},
             {"text": "You ___ leave the classroom early today.", "category": "may"},
             {"text": "___ all your dreams come true.", "category": "may"},
             {"text": "You ___ want to talk to your teacher after class.", "category": "might"},
             {"text": "It ___ snow tonight.", "category": "both"},
             {"text": "He ___ be late.", "category": "both"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"May I…?\" is more formal than \"Can I…?\". → True",
         "statements": [
             {"text": "We say \"She might to come\".", "answer": False, "translation": "Dizemos \"She might to come\"."},
             {"text": "\"Might\" expresses a possibility, not a certainty.", "answer": True,
              "translation": "\"Might\" expressa uma possibilidade, não uma certeza."},
             {"text": "\"Might\" rhymes with \"night\".", "answer": True, "translation": "\"Might\" rima com \"night\"."},
             {"text": "We say \"She mays come\" for he / she / it.", "answer": False,
              "translation": "Dizemos \"She mays come\" para he / she / it."},
         ]},
    ],
}

AULA18_PRACTICE = {
    "title": "Maybe… it might happen!",
    "lesson": 18,
    "description": "MIGHT / MAY + verbo = talvez aconteça: She might come. = Maybe she will come.\n"
                   "Negativa: might not / may not → I might not go to the party. (Talvez eu não vá.)\n"
                   "Pedidos e permissão começam com MAY: May I…? → Yes, of course. / Sure.",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Rewrite with might.",
         "translation": "Reescreva com might (troque o maybe).",
         "example": "Maybe it will rain later. → It might rain later.",
         "text": "1. Maybe she will come to the party tonight. → [She might come to the party tonight.]\n"
                 "2. Maybe we will be late because of the traffic. → [We might be late because of the traffic.]\n"
                 "3. Maybe I won't go to the beach. → [I might not go to the beach.|I may not go to the beach.]"},
        {"type": "match",
         "prompt": "Match the situations to what you say.",
         "translation": "Ligue cada situação ao que você fala.",
         "example": "You want water in class. → May I drink some water, please?",
         "pairs": [
             {"left": "You want to talk to the boss of a store.", "right": "May I speak with the manager?"},
             {"left": "Your friend's birthday.", "right": "May this year bring you success!"},
             {"left": "Dark clouds, but you're not sure.", "right": "It might rain later."},
             {"left": "Your friend is worried about an e-mail.", "right": "You might want to check your inbox."},
             {"left": "A teacher starts the class.", "right": "May I have your attention, please?"},
         ]},
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras em ordem. (Posso abrir a janela?)",
         "example": "I / May / your eraser / borrow → May I borrow your eraser?",
         "tokens": ["May", "I", "open", "the", "window?"], "alternatives": []},
    ],
}

AULA18_LISTENING = {
    "title": "Listening — weekend plans… maybe!",
    "lesson": 18,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: might = \"máit\" (o T final é curtinho). May = \"mêi\".",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"It might rain.\" → might",
         "audio": f"{AUDIO}/aula18-words.m4a",
         "text": "1. [*May|Can] I come in?\n2. It [*might|will] snow tonight.\n3. You [*may|must] leave now.\n"
                 "4. She [*might not|might] come.\n5. [*May|Might] the force be with you."},
        {"type": "info",
         "prompt": "Now listen: Bruno and Tati make plans for the weekend.",
         "translation": "Agora ouça: o Bruno e a Tati falam do fim de semana, mas nada está certo ainda! "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula18-weekend.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "They're talking about the [weekend].",
         "text": "1. Why might they not go to the beach? → [*It might rain.|The car is broken.|They're tired.]\n"
                 "2. What might they do instead? → [*Go to the cinema.|Go to a restaurant.|Visit Grandma.]\n"
                 "3. Who might come too? → [*Tati's sister.|Bruno's brother.|Their neighbors.]\n"
                 "4. What does Tati suggest? → [*Checking the weather app on Saturday morning.|Staying home.|Buying an umbrella.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Their plans aren't certain. → True",
         "statements": [
             {"text": "Bruno is sure it's going to rain.", "answer": False, "translation": "O Bruno tem certeza de que vai chover."},
             {"text": "Tati's sister might bring her kids.", "answer": True, "translation": "A irmã da Tati talvez traga os filhos."},
         ]},
    ],
}

AULA18_SPEAKING = {
    "title": "Speaking — may I…? It might…",
    "lesson": 18,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: may = \"mêi\" (como day) · might = \"máit\" (como night).",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula18-say-s{i}.m4a"} for i, t in enumerate(
             ["may, day, say, play", "might, night, right, light", "May I drink some water, please?",
              "It might rain later.", "You might try calling her.", "May all your dreams come true.",
              "May the force be with you.", "May I speak with the manager?"], 1)]},
        {"type": "speak",
         "prompt": "Now answer about YOU, with might.",
         "translation": "Agora responda sobre VOCÊ, usando might (talvez).",
         "example": "\"What might you do this weekend?\" → \"I might go to the beach.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula18-say-y{i}.m4a"} for i, t in enumerate(
             ["What might you do this weekend?", "Where might you travel next year?",
              "What might you have for dinner tonight?", "Who might you call today?"], 1)]},
    ],
}

AULA18_READING = {
    "title": "Reading — a note from the teacher",
    "lesson": 18,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the note.",
         "translation": "Leia e ouça o recado da professora para os alunos sobre a excursão da escola. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula18-reading.m4a",
         "text": "SCHOOL TRIP TO THE SCIENCE MUSEUM\n\n"
                 "Dear students,\n"
                 "On Friday, we are visiting the Science Museum. Please read this information.\n"
                 "We are leaving at 8 a.m. The traffic might be bad, so we might arrive a little late.\n"
                 "You may bring your phone, but you may not use it during the guided tour.\n"
                 "The museum café might be crowded, so you might want to bring a snack and a bottle of water.\n"
                 "It might rain in the afternoon. Bring a jacket!\n"
                 "If you have questions, you may send me an e-mail.\n"
                 "May you all have a wonderful day of learning!\n"
                 "Ms. Carter"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Where are they going? → [To the Science Museum.]",
         "text": "1. Why might they arrive late? → [*The traffic might be bad.|The bus is old.|It might snow.]\n"
                 "2. When can't they use their phones? → [*During the guided tour.|On the bus.|At the café.]\n"
                 "3. Why might they want to bring a snack? → [*The café might be crowded.|The museum has no café.|It's free.]\n"
                 "4. Why do they need a jacket? → [*It might rain in the afternoon.|It's winter.|The museum is cold.]"},
        {"type": "group",
         "prompt": "Find in the text: what does each sentence express?",
         "translation": "Encontre no texto: o que cada frase expressa?",
         "example": "You may bring your phone. → permission",
         "categories": ["permission", "possibility", "suggestion", "wish"],
         "words": [
             {"text": "You may bring your phone.", "category": "permission"},
             {"text": "You may send me an e-mail.", "category": "permission"},
             {"text": "The traffic might be bad.", "category": "possibility"},
             {"text": "It might rain in the afternoon.", "category": "possibility"},
             {"text": "You might want to bring a snack.", "category": "suggestion"},
             {"text": "May you all have a wonderful day!", "category": "wish"},
         ]},
    ],
}

AULA18_WRITING = {
    "title": "Writing — maybe…",
    "lesson": 18,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ may / might + verbo (sem TO): I might travel. · May I…? · May you…!\n"
                   "Negativa: might not / may not.",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Pode chover mais tarde. → It might rain later.",
         "text": "1. Posso usar seu telefone? → [May I use your phone?|Can I use your phone?|Could I use your phone?]\n"
                 "2. Talvez ela venha à festa. → [She might come to the party.|She may come to the party.]\n"
                 "3. Que todos os seus sonhos se realizem. → [May all your dreams come true.]"},
        {"type": "free",
         "prompt": "Write about your next weekend or next vacation. You aren't sure yet! Use might / may (not) for "
                   "possibilities, and write one wish with may.",
         "translation": "Escreva sobre o seu próximo fim de semana ou as próximas férias. Você ainda não tem certeza! "
                        "Use might / may (not) para possibilidades e escreva um desejo com may.",
         "example": "Next weekend, I might go to the beach.",
         "model_answer": "Next weekend, I might go to the beach with my friends, but it might rain.\n"
                         "If it rains, we may go to the cinema or have a pizza at home.\n"
                         "My brother might come too, but he might not have time.\n"
                         "And to all my friends: may you have a wonderful weekend!",
         "keywords": ["might", "may"], "min_words": 30, "points": 4},
    ],
}


AULA18_VIDEO = _video(18, AULA18_TOPIC, "Video — Maybe…",
                      "a Sarah ainda não tem certeza dos planos — e deseja feliz aniversário à irmã.",
                      "aula18-video", [
    _q("Complete: It ___ rain later.", "Complete: ___ chover mais tarde.", "might", "must", "should", "mights"),
    _q("If it doesn't rain, they might…", "Se não chover, eles talvez…", "go hiking in the mountains.", "go to the cinema.", "stay home.", "go to the beach."),
    _q("Is Sarah sure about the picnic?", "A Sarah tem certeza do piquenique?", "No, she isn't.", "Yes, she is.", "Yes, she must.", "No, she mustn't."),
    _q("\"May all your dreams come true\" is…", "\"May all your dreams come true\" é…", "a wish.", "a permission.", "a possibility.", "a rule."),
])

# ---------- Aula 19 — Should & Shouldn't (https://youtu.be/MdIL9gnFHFs) ----------

AULA19_TOPIC = "Aula 19 — Should & Shouldn't"

AULA19_ADVICE = {
    "title": "Should and shouldn't: advice",
    "lesson": 19,
    "description": "SHOULD = deveria / deve → CONSELHOS (advice), sugestões e recomendações.\n"
                   "She's very tired. She should go to bed early. · It's very hot today. You should drink more water. · "
                   "If you feel sick, you should see a doctor.\n"
                   "NEGATIVE: SHOULDN'T (should not): You shouldn't smoke. It's bad for your health.\n"
                   "QUESTION (pedir conselho): inverta → Should I call him? · Should I tell him the truth? · Should we leave now?\n"
                   "Modal verb: igual para todos (he should, she should) e SEM TO: ✗ I should to study → ✓ I should study more.\n"
                   "✗ You don't should worry → ✓ You shouldn't worry.\n"
                   "Pronúncia: should = \"shud\" (curtinho, L mudo) · should I = \"shudai\" → Should I stay or should I go?",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Complete with should or shouldn't (exercise from the lesson).",
         "translation": "Complete com should ou shouldn't (exercício da aula).",
         "example": "You [shouldn't] eat too much junk food.",
         "text": "1. He [*should|shouldn't] listen to his parents' advice.\n"
                 "2. She [*shouldn't|should] stay up so late on school nights.\n"
                 "3. You [*should|shouldn't] bring an umbrella today. It's going to rain.\n"
                 "4. I [*shouldn't|should] forget to do my homework.\n"
                 "5. People [*should|shouldn't] recycle more to help the planet.\n"
                 "6. We [*should|shouldn't] practice English every day."},
        {"type": "dropdown",
         "prompt": "Is this sentence correct?",
         "translation": "Esta frase está correta? (exercício da aula)",
         "example": "Should we leave now? → [Correct]",
         "text": "1. She should to do exercise. → [*Incorrect|Correct]\n2. You don't should worry. → [*Incorrect|Correct]\n"
                 "3. Should we leave now? → [*Correct|Incorrect]\n4. He shoulds study more. → [*Incorrect|Correct]"},
        {"type": "match",
         "prompt": "Match the problems to the advice.",
         "translation": "Ligue os problemas aos conselhos.",
         "example": "She's very tired. → She should go to bed early.",
         "pairs": [
             {"left": "It's very hot today.", "right": "You should drink more water."},
             {"left": "I feel sick.", "right": "You should see a doctor."},
             {"left": "He smokes a lot.", "right": "He shouldn't smoke. It's bad for his health."},
             {"left": "My English test is tomorrow.", "right": "You should study tonight."},
             {"left": "I'm always late for work.", "right": "You shouldn't stay up so late."},
         ]},
        {"type": "fill",
         "prompt": "Make questions to ask for advice.",
         "translation": "Faça perguntas para pedir conselho (should + sujeito + verbo).",
         "example": "I / call him → Should I call him?",
         "text": "1. I / tell him the truth → [Should I tell him the truth?]\n2. we / leave now → [Should we leave now?]\n"
                 "3. I / buy this jacket → [Should I buy this jacket?]"},
    ],
}

AULA19_DIGITAL = {
    "title": "Digital life: screen time and advice",
    "lesson": 19,
    "description": "DIGITAL VOCABULARY: screen time (tempo de tela) · notifications (notificações) · "
                   "digital detox (pausa de todas as telas) · scrolling (rolar a tela) · binge-watch (maratonar) · "
                   "blue light (luz azul, atrapalha o sono) · eye strain (vista cansada) · social media (redes sociais) · "
                   "do not disturb (modo não perturbe)\n"
                   "Conselhos: You should set a screen time limit. · She should try a digital detox. · "
                   "You shouldn't scroll for hours. · He shouldn't binge-watch at night.\n"
                   "Dica da aula: coloque o celular em inglês!",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the digital words to their meanings.",
         "translation": "Ligue as palavras às definições.",
         "example": "screen time → total time spent on screens",
         "pairs": [
             {"left": "notifications", "right": "alerts from apps and messages"},
             {"left": "digital detox", "right": "taking a break from all screens"},
             {"left": "scrolling", "right": "sliding up and down through content"},
             {"left": "binge-watch", "right": "watch many episodes in one sitting"},
             {"left": "eye strain", "right": "tired eyes from too much screen use"},
             {"left": "do not disturb", "right": "mode that silences all notifications"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct option for each digital life tip.",
         "translation": "Escolha a opção certa para cada dica de vida digital (exercício da aula).",
         "example": "You [shouldn't] use your phone in bed right before sleeping.",
         "text": "1. You [*should|shouldn't] turn off notifications while studying or working.\n"
                 "2. You [*should|shouldn't] take a screen break every 45 minutes.\n"
                 "3. You [*shouldn't|should] scroll social media for hours without any purpose.\n"
                 "4. You [*should|shouldn't] set a daily screen time limit on your apps."},
        {"type": "choice",
         "prompt": "Your friend gets anxious when he can't check his phone for 30 minutes. What's good advice?",
         "translation": "Seu amigo fica ansioso quando não pode olhar o celular por 30 minutos. Qual é um bom conselho?",
         "example": "He should turn off notifications.",
         "options": ["He shouldn't spend so much time on his phone.", "He should to turn off notifications.",
                     "He don't should use his phone.", "He should scrolls less."],
         "correct": 0},
    ],
}

AULA19_LISTENING = {
    "title": "Listening — too much screen time",
    "lesson": 19,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: should = \"shud\" · shouldn't = \"shudnt\" (o T final quase some).",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"You should rest.\" → should",
         "audio": f"{AUDIO}/aula19-words.m4a",
         "text": "1. You [*should|shouldn't] sleep more.\n2. He [*shouldn't|should] drive fast.\n3. [*Should I|Shall I] call her?\n"
                 "4. We [*should|could] go now.\n5. You [*shouldn't|should] worry."},
        {"type": "info",
         "prompt": "Now listen: Paulo talks to his friend Lia. She looks tired.",
         "translation": "Agora ouça: o Paulo conversa com a amiga Lia, que parece cansada. Depois complete abaixo.",
         "audio": f"{AUDIO}/aula19-tired.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois complete abaixo."},
        {"type": "fill",
         "prompt": "Listen again and fill in the blanks with the digital vocabulary.",
         "translation": "Ouça de novo e complete com o vocabulário digital (como no exercício da aula).",
         "example": "I was checking my [notifications] all night.",
         "text": "1. I was checking my [notifications] all night.\n2. The [blue light] affects your sleep.\n"
                 "3. I couldn't stop [scrolling].\n4. My [screen time] was nine hours yesterday!\n"
                 "5. Then I [binge-watched|binge watched] a series until midnight.\n6. You should try a [digital detox]."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Lia is tired. → True",
         "statements": [
             {"text": "Lia slept very well.", "answer": False, "translation": "A Lia dormiu muito bem."},
             {"text": "Paulo says she shouldn't use her phone in bed.", "answer": True,
              "translation": "O Paulo diz que ela não deveria usar o celular na cama."},
         ]},
    ],
}

AULA19_SPEAKING = {
    "title": "Speaking — give advice",
    "lesson": 19,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: should I = \"shudai\" (o D fica leve, quase um R).",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula19-say-s{i}.m4a"} for i, t in enumerate(
             ["should, shouldn't", "She should go to bed early.", "You should drink more water.",
              "You shouldn't smoke. It's bad for your health.", "Should I call him?", "Should I stay or should I go?",
              "You should set a screen time limit.", "You shouldn't scroll for hours."], 1)]},
        {"type": "speak",
         "prompt": "Now give advice for each situation.",
         "translation": "Agora dê um conselho para cada situação (com should ou shouldn't).",
         "example": "\"I'm always tired.\" → \"You should go to bed early.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula19-say-y{i}.m4a"} for i, t in enumerate(
             ["I'm always tired.", "I want to speak English better.", "I spend six hours a day on social media.",
              "I have a headache.", "My friend gets anxious without his phone."], 1)]},
    ],
}

AULA19_READING = {
    "title": "Reading — Ask Anna",
    "lesson": 19,
    "subject": "Reading",
    "description": "Leia (e ouça) a coluna de conselhos e responda às perguntas de acordo com o texto.",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the advice column.",
         "translation": "Leia e ouça a coluna de conselhos de uma revista. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula19-reading.m4a",
         "text": "ASK ANNA 💬\n\n"
                 "Dear Anna,\nMy 14-year-old son spends all his time on his phone. He plays games until 2 a.m., and in the "
                 "morning he can't wake up for school. His grades are bad now. What should I do? — Worried Mom\n\n"
                 "Dear Worried Mom,\nYou should talk to your son calmly. He shouldn't feel that you are angry. "
                 "Together, you should set a screen time limit — maybe two hours a day. "
                 "He shouldn't take his phone to bed: the blue light affects sleep. "
                 "You should also find activities for the family without screens: a walk in the park, a board game, cooking. "
                 "And you shouldn't use your phone at dinner either! Children copy what we do. — Anna"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Who wrote to Anna? → [A worried mom.]",
         "text": "1. What's the son's problem? → [*He spends all his time on his phone.|He doesn't like school.|He's sick.]\n"
                 "2. How many hours a day does Anna suggest? → [*Maybe two hours.|Six hours.|No hours.]\n"
                 "3. Why shouldn't he take his phone to bed? → [*The blue light affects sleep.|He might break it.|It's expensive.]\n"
                 "4. What shouldn't the mom do at dinner? → [*Use her phone.|Talk.|Cook.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "The son is 14. → True",
         "statements": [
             {"text": "Anna says the mom should be angry with her son.", "answer": False,
              "translation": "A Anna diz que a mãe deveria ficar brava com o filho."},
             {"text": "Anna suggests family activities without screens.", "answer": True,
              "translation": "A Anna sugere atividades em família sem telas."},
         ]},
        {"type": "group",
         "prompt": "Anna's advice: should or shouldn't?",
         "translation": "Os conselhos da Anna: should ou shouldn't?",
         "example": "talk to your son calmly → should",
         "categories": ["should", "shouldn't"],
         "words": [
             {"text": "talk to your son calmly", "category": "should"},
             {"text": "set a screen time limit", "category": "should"},
             {"text": "find activities without screens", "category": "should"},
             {"text": "take his phone to bed", "category": "shouldn't"},
             {"text": "use your phone at dinner", "category": "shouldn't"},
         ]},
    ],
}

AULA19_WRITING = {
    "title": "Writing — my advice",
    "lesson": 19,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ should / shouldn't + verbo (sem TO) · Should I…? para pedir conselho.",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Você deveria beber mais água. → You should drink more water.",
         "text": "1. Eu deveria estudar mais. → [I should study more.]\n"
                 "2. Você não deveria se preocupar. → [You shouldn't worry.|You should not worry.]\n"
                 "3. Eu devo contar a verdade para ele? → [Should I tell him the truth?]"},
        {"type": "free",
         "prompt": "Read the situation and give advice: \"My friend gets anxious when he can't check his phone for 30 "
                   "minutes. He sleeps very little and he's always tired.\" Write at least 3 sentences with should and "
                   "2 with shouldn't.",
         "translation": "Leia a situação e dê conselhos: \"Meu amigo fica ansioso quando não pode olhar o celular por 30 "
                        "minutos. Ele dorme pouco e está sempre cansado.\" Escreva pelo menos 3 frases com should e 2 com "
                        "shouldn't.",
         "example": "He should turn off notifications.",
         "model_answer": "He should turn off notifications when he is working.\n"
                         "He should set a screen time limit on his apps.\n"
                         "He should try a digital detox on the weekend.\n"
                         "He shouldn't use his phone in bed, and he shouldn't scroll social media for hours.",
         "keywords": ["should", "shouldn't"], "min_words": 30, "points": 4},
    ],
}


AULA19_VIDEO = _video(19, AULA19_TOPIC, "Video — Advice for Lia",
                      "o Bruno dá conselhos com should e shouldn't para a amiga que vive cansada.",
                      "aula19-video", [
    _q("What should Lia do?", "O que a Lia deveria fazer?", "Go to bed early.", "Go to bed at 2 a.m.", "Drink more coffee.", "Scroll more."),
    _q("Complete: She ___ use her phone in bed.", "Complete: ela ___ usar o celular na cama.", "shouldn't", "should", "don't should", "should to"),
    _q("What should she drink more?", "O que ela deveria beber mais?", "Water.", "Coffee.", "Soda.", "Juice."),
    _q("Complete: She should ___.", "Complete: ela deveria ___.", "exercise", "to exercise", "exercises", "exercising"),
])

# ---------- Aula 20 — Health Problems (https://youtu.be/lKBTJNpHuvI) ----------

AULA20_TOPIC = "Aula 20 — Health Problems"

AULA20_ACHES = {
    "title": "Health problems: headache, sore throat…",
    "lesson": 20,
    "description": "ACHE = dor (pronúncia \"êik\"!) → headache (dor de cabeça) · stomachache (dor de estômago) · "
                   "toothache (dor de dente) · backache (dor nas costas) · earache (dor de ouvido)\n"
                   "Outros problemas: a rash (vermelhidão, alergia na pele) · sunburn (queimadura de sol) · "
                   "vomiting / throwing up (vomitando) · a cough (tosse — \"kóf\", ≠ coffee!) · bleeding (sangrando) · "
                   "sneezing (espirrando) · swollen (inchado) · the flu (gripe) · a fever / a temperature (febre) · "
                   "a sore throat (garganta inflamada) · a blister (bolha)\n"
                   "Estruturas: She HAS a headache. · He HAS sunburn. · She IS sneezing. · His finger IS bleeding. · "
                   "Her ankle IS swollen.",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the health problems to Portuguese.",
         "translation": "Ligue os problemas de saúde ao português.",
         "example": "headache → dor de cabeça",
         "pairs": [
             {"left": "stomachache", "right": "dor de estômago"},
             {"left": "toothache", "right": "dor de dente"},
             {"left": "backache", "right": "dor nas costas"},
             {"left": "earache", "right": "dor de ouvido"},
             {"left": "a sore throat", "right": "garganta inflamada"},
             {"left": "a cough", "right": "tosse"},
             {"left": "a fever", "right": "febre"},
             {"left": "a blister", "right": "bolha"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose has or is.",
         "translation": "Escolha has (tem) ou is (está).",
         "example": "She [has] a headache. · She [is] sneezing.",
         "text": "1. He [*has|is] a cough.\n2. She [*is|has] vomiting.\n3. His finger [*is|has] bleeding.\n"
                 "4. She [*has|is] a sore throat.\n5. Her ankle [*is|has] swollen.\n6. He [*has|is] the flu."},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Ache\" means dor. → True",
         "statements": [
             {"text": "We pronounce \"ache\" like \"atchy\".", "answer": False,
              "translation": "Pronunciamos \"ache\" como \"átchi\"."},
             {"text": "\"Cough\" and \"coffee\" have the same sound.", "answer": False,
              "translation": "\"Cough\" e \"coffee\" têm o mesmo som."},
             {"text": "\"Throwing up\" means the same as \"vomiting\".", "answer": True,
              "translation": "\"Throwing up\" significa o mesmo que \"vomiting\"."},
             {"text": "\"Temperature\" can mean fever.", "answer": True, "translation": "\"Temperature\" pode significar febre."},
         ]},
    ],
}

AULA20_DOCTOR = {
    "title": "At the doctor's: what's the matter?",
    "lesson": 20,
    "description": "No médico: What's the matter? / What's wrong? (O que você tem?) → I have a terrible sore throat. · "
                   "My whole body aches. (meu corpo todo dói — ache também é verbo: doer)\n"
                   "Conselhos (should, da aula passada): You should stay at home. · You should rest your voice. · "
                   "You shouldn't drink cold water. · You shouldn't take strong medicine without seeing a doctor.\n"
                   "Na aula seguinte você vai ver MUST / MUSTN'T, que o médico também usa: You must stay at home.",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "Which body part? Put each problem in the right group.",
         "translation": "Qual parte do corpo? Coloque cada problema no grupo certo.",
         "example": "headache → head",
         "categories": ["head", "mouth / throat", "body / skin"],
         "words": [
             {"text": "headache", "category": "head"}, {"text": "earache", "category": "head"},
             {"text": "toothache", "category": "mouth / throat"}, {"text": "sore throat", "category": "mouth / throat"},
             {"text": "cough", "category": "mouth / throat"},
             {"text": "rash", "category": "body / skin"}, {"text": "sunburn", "category": "body / skin"},
             {"text": "blister", "category": "body / skin"}, {"text": "backache", "category": "body / skin"},
         ]},
        {"type": "match",
         "prompt": "Match the problems to the advice.",
         "translation": "Ligue cada problema a um conselho.",
         "example": "I have a toothache. → You should see a dentist.",
         "pairs": [
             {"left": "I have a high temperature and my whole body aches.", "right": "You should stay at home and rest."},
             {"left": "I have a terrible sore throat.", "right": "You shouldn't drink cold water."},
             {"left": "I have sunburn.", "right": "You should use sunscreen next time."},
             {"left": "My finger is bleeding.", "right": "You should wash it and use a bandage."},
             {"left": "I have a blister on my foot.", "right": "You shouldn't wear those new shoes."},
         ]},
        {"type": "fill",
         "prompt": "Write the health problem.",
         "translation": "Escreva o problema de saúde em inglês.",
         "example": "dor de cabeça → headache",
         "text": "1. dor de dente → [toothache|a toothache]\n2. dor nas costas → [backache|a backache]\n"
                 "3. gripe → [flu|the flu|a flu]\n4. febre → [fever|a fever|temperature|a temperature]\n"
                 "5. queimadura de sol → [sunburn]"},
    ],
}

AULA20_LISTENING = {
    "title": "Listening — at the doctor's",
    "lesson": 20,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: -ACHE no final = \"êik\": headache = \"HÉDêik\".",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the problem you hear.",
         "translation": "Ouça e escolha o problema que você ouve.",
         "example": "Você ouve: \"She has a headache.\" → headache",
         "audio": f"{AUDIO}/aula20-problems.m4a",
         "text": "1. [*stomachache|toothache]\n2. [*a cough|coffee]\n3. [*sneezing|sleeping]\n4. [*a sore throat|a sore toe]\n"
                 "5. [*a rash|a rush]\n6. [*the flu|the floor]"},
        {"type": "info",
         "prompt": "Now listen: Mrs. Lopes visits the doctor.",
         "translation": "Agora ouça: a Sra. Lopes vai ao médico. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula20-doctor.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Mrs. Lopes is at the [doctor's].",
         "text": "1. What are her problems? → [*A sore throat, a cough and a fever.|A stomachache and a rash.|A backache.]\n"
                 "2. When did it start? → [*On Monday.|Two weeks ago.|Yesterday.]\n"
                 "3. What does she have? → [*The flu.|A cold.|Sunburn.]\n"
                 "4. What does the doctor say about work? → [*She shouldn't go to work this week.|She should go to work.|"
                 "She should work from the beach.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Mrs. Lopes feels sick. → True",
         "statements": [
             {"text": "The doctor says she should drink a lot of water and tea.", "answer": True,
              "translation": "O médico diz que ela deveria beber muita água e chá."},
             {"text": "Her temperature is normal.", "answer": False, "translation": "A temperatura dela está normal."},
         ]},
    ],
}

AULA20_SPEAKING = {
    "title": "Speaking — what's the matter?",
    "lesson": 20,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: cough = \"kóf\" · sore throat = \"sór thrôut\" (TH com a língua entre os dentes).",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita o vocabulário da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula20-say-w{i}.m4a"} for i, t in enumerate(
             ["ache", "She has a stomachache.", "She has a toothache.", "He has a backache.", "She has an earache.",
              "She has a headache.", "He has sunburn.", "She is throwing up.", "He has a cough.",
              "She is sneezing.", "Her ankle is swollen.", "She has a sore throat."], 1)]},
        {"type": "speak",
         "prompt": "Now tell the doctor what's wrong.",
         "translation": "Agora diga ao médico o que você tem (invente!) e dê um conselho.",
         "example": "\"What's the matter?\" → \"I have a terrible headache.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula20-say-y{i}.m4a"} for i, t in enumerate(
             ["What's the matter?", "Do you have a fever?", "What should I do for a sore throat?",
              "What should I do for sunburn?"], 1)]},
    ],
}

AULA20_READING = {
    "title": "Reading — a terrible trip",
    "lesson": 20,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto do Rafael sobre uma viagem em família cheia de problemas de saúde. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula20-reading.m4a",
         "text": "A TERRIBLE TRIP\n\n"
                 "Last summer, my family went to Bahia for a week. It was a disaster!\n"
                 "On the first day, my dad slept on the beach without sunscreen. He had terrible sunburn!\n"
                 "On the second day, my sister ate shrimp at a beach kiosk. That night, she had a stomachache and "
                 "she was throwing up.\n"
                 "My mom walked a lot in new sandals, and she had blisters on both feet.\n"
                 "And me? I swam in the cold sea for hours, and I got a sore throat and a cough. "
                 "On the last day, I had a fever, too.\n"
                 "The only person who was fine was my little brother. He was sneezing a bit, but he said he was \"great\"!\n"
                 "Next year, we should stay at home. Or we should take a doctor with us!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Where did the family go? → [To Bahia.]",
         "text": "1. Why did the dad have sunburn? → [*He slept on the beach without sunscreen.|He swam all day.|He worked outside.]\n"
                 "2. What was the sister's problem? → [*A stomachache and vomiting.|A sore throat.|Blisters.]\n"
                 "3. Why did the mom have blisters? → [*She walked in new sandals.|She ran a marathon.|She had sunburn.]\n"
                 "4. Who was fine? → [*The little brother.|The dad.|Rafael.]"},
        {"type": "match",
         "prompt": "Match each person to the health problem.",
         "translation": "Ligue cada pessoa ao problema de saúde.",
         "example": "the dad → sunburn",
         "pairs": [
             {"left": "the sister", "right": "a stomachache"},
             {"left": "the mom", "right": "blisters"},
             {"left": "Rafael", "right": "a sore throat, a cough and a fever"},
             {"left": "the little brother", "right": "sneezing a bit"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "The trip was a disaster. → True",
         "statements": [
             {"text": "The sister ate shrimp at a beach kiosk.", "answer": True,
              "translation": "A irmã comeu camarão num quiosque de praia."},
             {"text": "Rafael didn't have a fever.", "answer": False, "translation": "O Rafael não teve febre."},
         ]},
    ],
}

AULA20_WRITING = {
    "title": "Writing — I'm sick!",
    "lesson": 20,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ I have a + problema (a headache, a cough, a fever) · I'm sneezing / throwing up · "
                   "My ankle is swollen · Conselhos: You should… / You shouldn't…",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu estou com dor de cabeça. → I have a headache.",
         "text": "1. Ela está com dor de garganta. → [She has a sore throat.|She's got a sore throat.]\n"
                 "2. Meu dedo está sangrando. → [My finger is bleeding.|My finger's bleeding.]\n"
                 "3. Ele está com gripe. → [He has the flu.|He has flu.|He has a flu.|He's got the flu.]"},
        {"type": "free",
         "prompt": "Write a message to your boss or teacher: you are sick today. Describe your health problems "
                   "(at least three) and say what the doctor told you (you should… / you shouldn't…).",
         "translation": "Escreva uma mensagem para o seu chefe ou professor: você está doente hoje. Descreva seus "
                        "problemas de saúde (pelo menos três) e diga o que o médico falou (should / shouldn't).",
         "example": "Hi, Ms. Silva. I'm sorry, but I'm sick today.",
         "model_answer": "Hi, Ms. Silva. I'm sorry, but I'm sick today.\n"
                         "I have a sore throat, a terrible headache and a fever.\n"
                         "I went to the doctor this morning. He said I have the flu.\n"
                         "He said I should stay at home and drink a lot of water, and I shouldn't go to work this week.",
         "keywords": ["I have", "headache", "should"], "min_words": 30, "points": 4},
    ],
}


AULA20_VIDEO = _video(20, AULA20_TOPIC, "Video — A terrible week",
                      "a Sarah conta os problemas de saúde da família numa semana difícil.",
                      "aula20-video", [
    _q("What did Sarah have on Monday?", "O que a Sarah teve na segunda?", "A headache.", "A toothache.", "A backache.", "Sunburn."),
    _q("What was she doing on Tuesday?", "O que ela estava fazendo na terça?", "Sneezing.", "Vomiting.", "Bleeding.", "Coughing."),
    _q("What did her husband have?", "O que o marido dela teve?", "A bad cough.", "A rash.", "A blister.", "An earache."),
    _q("What did the doctor say?", "O que o médico disse?", "It's the flu.", "It's sunburn.", "It's a toothache.", "It's nothing."),
])

# ---------- Aula 21 — Must & Mustn't (https://youtu.be/RTobtsTsvYY) ----------

AULA21_TOPIC = "Aula 21 — Must & Mustn't"

AULA21_MUST = {
    "title": "Must: obligation and strong advice",
    "lesson": 21,
    "description": "MUST = tenho que / preciso (obrigação que VEM DE VOCÊ, ou conselho muito forte). I must do something = "
                   "I need to do it.\n"
                   "I must talk to my boss about the new project. · I'm very hungry. I must eat something. · "
                   "I must study hard. · I must tidy my room.\n"
                   "Conselho forte / recomendação: It's a fantastic movie. You must watch it! · That new restaurant is amazing. "
                   "You must go there! (também: you have to…, próxima aula)\n"
                   "Modal verb: SEM TO e SEM S: ✗ She must to study · ✗ He musts come → ✓ She must study. · He must come.",
    "topic": AULA21_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Is this sentence correct? (from the lesson)",
         "translation": "Esta frase está correta? (exercício da aula)",
         "example": "I must study hard. → [Correct]",
         "text": "1. She must to study for the test. → [*Incorrect|Correct]\n2. You don't must touch the pictures. → [*Incorrect|Correct]\n"
                 "3. He musts come with us. → [*Incorrect|Correct]\n4. I must talk to my boss. → [*Correct|Incorrect]"},
        {"type": "match",
         "prompt": "Match the situations to the sentences with must.",
         "translation": "Ligue as situações às frases com must.",
         "example": "I'm very hungry. → I must eat something.",
         "pairs": [
             {"left": "My room is a mess.", "right": "I must tidy my room."},
             {"left": "My test is tomorrow.", "right": "I must study hard tonight."},
             {"left": "It's a fantastic movie!", "right": "You must watch it!"},
             {"left": "There's a problem with the new project.", "right": "I must talk to my boss."},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "MUST is a modal verb. → True",
         "statements": [
             {"text": "With MUST, the obligation usually comes from the speaker.", "answer": True,
              "translation": "Com MUST, a obrigação geralmente vem de quem fala."},
             {"text": "\"You must watch it!\" can be a strong recommendation.", "answer": True,
              "translation": "\"You must watch it!\" pode ser uma recomendação forte."},
             {"text": "The negative of must is \"don't must\".", "answer": False,
              "translation": "A negativa de must é \"don't must\"."},
         ]},
    ],
}

AULA21_MUSTNT = {
    "title": "Mustn't: prohibition",
    "lesson": 21,
    "description": "MUSTN'T (must not) = PROIBIÇÃO, não pode de jeito nenhum.\n"
                   "You must not touch the animals at the zoo. · You mustn't touch the pictures. · You mustn't skip the medicine. · "
                   "She mustn't eat heavy food now.\n"
                   "Pronúncia: o primeiro T de mustn't é MUDO → \"mâsnt\".\n"
                   "Exercício da aula (saúde): You must take this medicine. · You mustn't touch the wound with dirty hands. · "
                   "You mustn't drive after taking this medicine, because it makes you sleepy. · "
                   "Diabetics must check their blood sugar regularly. · She must rest for a few days after the surgery.",
    "topic": AULA21_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Must or mustn't? (exercise from the lesson)",
         "translation": "Must ou mustn't? (exercício da aula)",
         "example": "You [must] take this medicine.",
         "text": "1. You [*mustn't|must] touch the wound with dirty hands.\n"
                 "2. You [*mustn't|must] drive after taking this medicine. It makes you sleepy.\n"
                 "3. Diabetics [*must|mustn't] check their blood sugar regularly.\n"
                 "4. She [*must|mustn't] rest for a few days after the surgery.\n"
                 "5. You [*mustn't|must] touch the animals at the zoo.\n"
                 "6. She [*mustn't|must] eat heavy food now."},
        {"type": "group",
         "prompt": "Museum rules: must or mustn't?",
         "translation": "Regras do museu: must (obrigatório) ou mustn't (proibido)?",
         "example": "touch the pictures → mustn't",
         "categories": ["must", "mustn't"],
         "words": [
             {"text": "buy a ticket", "category": "must"}, {"text": "leave big bags at the entrance", "category": "must"},
             {"text": "speak quietly", "category": "must"},
             {"text": "touch the pictures", "category": "mustn't"}, {"text": "eat in the rooms", "category": "mustn't"},
             {"text": "take photos with flash", "category": "mustn't"},
         ]},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Você não pode tocar nos quadros. → You mustn't touch the pictures.",
         "text": "1. Eu tenho que estudar muito. → [I must study hard.|I must study a lot.]\n"
                 "2. Você não pode pular o remédio. → [You mustn't skip the medicine.|You must not skip the medicine.]\n"
                 "3. Ela tem que descansar. → [She must rest.]"},
    ],
}

AULA21_LISTENING = {
    "title": "Listening — the doctor's instructions",
    "lesson": 21,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: must = \"mâst\" · mustn't = \"mâsnt\" (sem o primeiro T) — ouça o N!",
    "topic": AULA21_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose must or mustn't.",
         "translation": "Ouça e escolha must ou mustn't.",
         "example": "Você ouve: \"You mustn't smoke.\" → mustn't",
         "audio": f"{AUDIO}/aula21-words.m4a",
         "text": "1. You [*must|mustn't] rest.\n2. You [*mustn't|must] run.\n3. She [*must|mustn't] drink water.\n"
                 "4. They [*mustn't|must] be late.\n5. I [*must|mustn't] call my mom."},
        {"type": "info",
         "prompt": "Now listen: a doctor talks to Pedro after his surgery.",
         "translation": "Agora ouça: a médica explica ao Pedro o que ele deve e não pode fazer depois da cirurgia no joelho. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula21-surgery.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "group",
         "prompt": "Listen again. What must Pedro do, and what mustn't he do?",
         "translation": "Ouça de novo. O que o Pedro deve fazer e o que ele não pode fazer?",
         "example": "rest for a week → must",
         "categories": ["must", "mustn't"],
         "words": [
             {"text": "rest for a week", "category": "must"},
             {"text": "take the medicine every eight hours", "category": "must"},
             {"text": "come back in two weeks", "category": "must"},
             {"text": "play soccer for two months", "category": "mustn't"},
             {"text": "drive this week", "category": "mustn't"},
             {"text": "get the bandage wet", "category": "mustn't"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Pedro had surgery on his knee. → True",
         "statements": [
             {"text": "Pedro can play soccer next week.", "answer": False, "translation": "O Pedro pode jogar futebol semana que vem."},
             {"text": "The medicine makes Pedro sleepy.", "answer": True, "translation": "O remédio dá sono no Pedro."},
         ]},
    ],
}

AULA21_SPEAKING = {
    "title": "Speaking — rules and obligations",
    "lesson": 21,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: mustn't = \"mâsnt\" — não pronuncie o primeiro T!",
    "topic": AULA21_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula21-say-s{i}.m4a"} for i, t in enumerate(
             ["must, mustn't", "I must talk to my boss about the new project.", "It's a fantastic movie. You must watch it.",
              "I'm very hungry. I must eat something.", "You must not touch the animals at the zoo.",
              "You mustn't touch the pictures.", "You must take this medicine."], 1)]},
        {"type": "speak",
         "prompt": "Now answer about YOU.",
         "translation": "Agora responda sobre VOCÊ.",
         "example": "\"What must you do this week?\" → \"I must finish my report.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula21-say-y{i}.m4a"} for i, t in enumerate(
             ["What must you do this week?", "Tell me a movie that people must watch.",
              "What mustn't you do at work or at school?", "What must you do to speak English well?"], 1)]},
    ],
}

AULA21_READING = {
    "title": "Reading — swimming pool rules",
    "lesson": 21,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA21_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the rules.",
         "translation": "Leia e ouça as regras da piscina do clube. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula21-reading.m4a",
         "text": "SUNNY CLUB — SWIMMING POOL RULES 🏊\n\n"
                 "• You must take a shower before you enter the pool.\n"
                 "• You must wear a swimming cap.\n"
                 "• Children under 10 must be with an adult.\n"
                 "• You mustn't run around the pool. The floor is wet!\n"
                 "• You mustn't eat or drink in the water.\n"
                 "• You mustn't dive in the shallow area.\n"
                 "• You mustn't use glass bottles near the pool.\n"
                 "• The pool is open from 7 a.m. to 8 p.m. You must leave the water at 7:45.\n"
                 "Have fun and be safe!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "What must you wear? → [A swimming cap.]",
         "text": "1. What must you do before entering the pool? → [*Take a shower.|Eat something.|Run.]\n"
                 "2. Who must be with an adult? → [*Children under 10.|Everybody.|Teenagers.]\n"
                 "3. Why mustn't you run? → [*The floor is wet.|It's too hot.|The pool is closed.]\n"
                 "4. When must you leave the water? → [*At 7:45 p.m.|At 8 p.m.|At 7 a.m.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "The pool opens at 7 a.m. → True",
         "statements": [
             {"text": "You can drink a soda in the water.", "answer": False, "translation": "Você pode tomar refrigerante na água."},
             {"text": "You mustn't use glass bottles near the pool.", "answer": True,
              "translation": "Você não pode usar garrafas de vidro perto da piscina."},
         ]},
        {"type": "fill",
         "prompt": "Complete with must or mustn't, according to the text.",
         "translation": "Complete com must ou mustn't, de acordo com o texto.",
         "example": "You [must] wear a swimming cap.",
         "text": "1. You [mustn't] dive in the shallow area.\n2. You [must] take a shower first.\n"
                 "3. You [mustn't] eat in the water."},
    ],
}

AULA21_WRITING = {
    "title": "Writing — the rules of my house",
    "lesson": 21,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ must + verbo (obrigação / conselho forte) · mustn't + verbo (proibição). Sem TO!",
    "topic": AULA21_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Correct the mistakes.",
         "translation": "Corrija os erros.",
         "example": "She must to study. → She must study.",
         "text": "1. You don't must smoke here. → [You mustn't smoke here.|You must not smoke here.]\n"
                 "2. He musts finish the report. → [He must finish the report.]\n"
                 "3. We must to leave now. → [We must leave now.]"},
        {"type": "free",
         "prompt": "Write the rules of your house (or your office / school): at least 3 things people must do "
                   "and 3 things they mustn't do.",
         "translation": "Escreva as regras da sua casa (ou trabalho / escola): pelo menos 3 coisas que as pessoas devem fazer "
                        "e 3 que não podem fazer.",
         "example": "You must take off your shoes at the door.",
         "model_answer": "In my house, you must take off your shoes at the door.\n"
                         "You must wash your dishes after dinner, and you must turn off the lights.\n"
                         "You mustn't play loud music after 10 p.m.\n"
                         "You mustn't feed the cat chocolate, and you mustn't use my coffee mug!",
         "keywords": ["must", "mustn't"], "min_words": 30, "points": 4},
    ],
}


AULA21_VIDEO = _video(21, AULA21_TOPIC, "Video — Rules, rules, rules!",
                      "o Bruno mostra regras do zoológico, do museu, da bicicleta e do hospital com must e mustn't.",
                      "aula21-video", [
    _q("Complete: At the zoo, you ___ feed the animals.", "Complete: no zoológico, você ___ alimentar os animais.", "mustn't", "must", "don't must", "must to"),
    _q("What must you do at the museum?", "O que você tem que fazer no museu?", "Buy a ticket.", "Touch the paintings.", "Smoke.", "Feed the animals."),
    _q("When must you wear a helmet?", "Quando você tem que usar capacete?", "When you ride a bike.", "At the museum.", "At the zoo.", "In hospitals."),
    _q("Where mustn't you smoke?", "Onde é proibido fumar?", "In hospitals and schools.", "On a bike.", "At home.", "Everywhere is OK."),
])

# ---------- Aula 22 — Phone Etiquette (https://youtu.be/s8C5aqJLSEQ) ----------

AULA22_TOPIC = "Aula 22 — Phone Etiquette"

AULA22_LANGUAGE = {
    "title": "Phone language",
    "lesson": 22,
    "description": "PHONE LANGUAGE:\n"
                   "dial a number (discar) · text / message a friend (mandar mensagem) · hang up (desligar — passado: hung up) · "
                   "ringtone (toque do celular) · call back (ligar de volta) · voicemail (correio de voz) · "
                   "the line's engaged / busy (a linha está ocupada) · swipe through photos (passar as fotos) · "
                   "go off (tocar de repente / disparar) · put someone on hold (colocar na espera) · "
                   "be cut off (a ligação cair) · silent mode (modo silencioso) · loudspeaker (viva-voz) · "
                   "helpline (central de atendimento)\n"
                   "Please hold. (Aguarde, por favor.) · I missed his call, so I'll call him back later.",
    "topic": AULA22_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the phone words to their meanings.",
         "translation": "Ligue as palavras às definições (como na aula).",
         "example": "voicemail → a recorded message when you miss a call",
         "pairs": [
             {"left": "call back", "right": "to return someone's missed call"},
             {"left": "silent mode", "right": "phone setting that stops all sound"},
             {"left": "hold", "right": "to ask someone to wait on the phone"},
             {"left": "hang up", "right": "to end a phone call"},
             {"left": "loudspeaker", "right": "audio mode for hands-free calls"},
             {"left": "ringtone", "right": "the sound or song when the phone rings"},
         ]},
        {"type": "dropdown",
         "prompt": "Complete the sentences (exercise from the lesson).",
         "translation": "Complete as frases (exercício da aula).",
         "example": "Please [hold]. I'll be back in two minutes.",
         "text": "1. I missed his call, so I'll [*call him back|hang him up|hold him] later.\n"
                 "2. She left a [*voicemail|ringtone|loudspeaker] explaining the meeting time.\n"
                 "3. He put his phone on [*silent mode|voicemail|hold] during class.\n"
                 "4. Don't forget to [*hang up|call back|dial] after the conversation ends.\n"
                 "5. She used the [*loudspeaker|ringtone|helpline] so everyone in the room could hear."},
        {"type": "match",
         "prompt": "Match the sentences to Portuguese.",
         "translation": "Ligue as frases ao português.",
         "example": "He's dialing a number. → Ele está discando um número.",
         "pairs": [
             {"left": "He hung up.", "right": "Ele desligou."},
             {"left": "The line's busy.", "right": "A linha está ocupada."},
             {"left": "They put her on hold.", "right": "Colocaram ela na espera."},
             {"left": "He was cut off.", "right": "A ligação dele caiu."},
             {"left": "She's swiping through photos.", "right": "Ela está passando as fotos."},
         ]},
    ],
}

AULA22_ETIQUETTE = {
    "title": "Phone etiquette: rules for good manners",
    "lesson": 22,
    "description": "ETIQUETTE = boas maneiras. Revise should / must / mustn't com dicas de etiqueta no telefone:\n"
                   "You should put your phone on silent mode in meetings and at the cinema.\n"
                   "You shouldn't use the loudspeaker in public places.\n"
                   "You should call back when you miss a call.\n"
                   "You mustn't text while you're driving!\n"
                   "His phone went off in the middle of a meeting. → Que vergonha!",
    "topic": AULA22_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "Good or bad phone etiquette?",
         "translation": "Boa ou má etiqueta no telefone? Coloque cada atitude no grupo certo.",
         "example": "put your phone on silent mode at the cinema → good",
         "categories": ["good etiquette", "bad etiquette"],
         "words": [
             {"text": "put your phone on silent mode at the cinema", "category": "good etiquette"},
             {"text": "call back when you miss a call", "category": "good etiquette"},
             {"text": "leave a short voicemail", "category": "good etiquette"},
             {"text": "use the loudspeaker on the bus", "category": "bad etiquette"},
             {"text": "text while you're driving", "category": "bad etiquette"},
             {"text": "hang up without saying goodbye", "category": "bad etiquette"},
         ]},
        {"type": "dropdown",
         "prompt": "Should, shouldn't or mustn't?",
         "translation": "Should, shouldn't ou mustn't?",
         "example": "You [mustn't] text while you're driving.",
         "text": "1. You [*should|shouldn't] put your phone on silent mode in meetings.\n"
                 "2. You [*shouldn't|should] use the loudspeaker in a restaurant.\n"
                 "3. You [*mustn't|should] use your phone when you're driving.\n"
                 "4. You [*should|shouldn't] call back when you miss an important call."},
        {"type": "fill",
         "prompt": "Write the phone word.",
         "translation": "Escreva a palavra do vocabulário de telefone.",
         "example": "correio de voz → voicemail",
         "text": "1. desligar (o telefone) → [hang up]\n2. viva-voz → [loudspeaker|loud speaker]\n"
                 "3. toque do celular → [ringtone]\n4. modo silencioso → [silent mode]"},
    ],
}

AULA22_LISTENING = {
    "title": "Listening — phone situations",
    "lesson": 22,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: preste atenção nos sons de fundo e nas palavras-chave (hold, busy, voicemail, cut off).",
    "topic": AULA22_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Listen to five short phone situations.",
         "translation": "Ouça cinco situações curtas ao telefone. Depois ligue cada uma ao que está acontecendo.",
         "audio": f"{AUDIO}/aula22-situations.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda abaixo."},
        {"type": "dropdown",
         "prompt": "What is happening in each situation?",
         "translation": "O que está acontecendo em cada situação?",
         "example": "Situation 1 → [The line's busy.]",
         "text": "Situation 1 → [*The line's busy.|She's texting a friend.|He hung up.]\n"
                 "Situation 2 → [*She left a message on his voicemail.|She's choosing a ringtone.|She was cut off.]\n"
                 "Situation 3 → [*They put him on hold.|He's dialing a number.|His phone went off.]\n"
                 "Situation 4 → [*He was cut off in the middle of the conversation.|He called back.|He's swiping through photos.]\n"
                 "Situation 5 → [*His phone went off in the middle of a meeting.|He's on hold.|The line's busy.]"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"Please hold.\" → Please [hold].",
         "audio": f"{AUDIO}/aula22-dictation.m4a",
         "text": "1. I'll [call] you back later.\n2. Don't forget to [hang] up.\n3. Put your phone on [silent] mode.\n"
                 "4. She left a message on his [voicemail]."},
    ],
}

AULA22_SPEAKING = {
    "title": "Speaking — on the phone",
    "lesson": 22,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: hung up = \"hângâp\" (tudo ligado) · voicemail = \"vóismêil\".",
    "topic": AULA22_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula22-say-s{i}.m4a"} for i, t in enumerate(
             ["He's dialing a number.", "She's texting a friend.", "He hung up.", "He's calling back.",
              "She left a message on his voicemail.", "The line's busy.", "They put her on hold.",
              "He was cut off in the middle of a conversation.", "Please hold. I'll be back in two minutes."], 1)]},
        {"type": "speak",
         "prompt": "Now answer about YOU.",
         "translation": "Agora responda sobre VOCÊ.",
         "example": "\"What's your ringtone?\" → \"It's a song by my favorite band.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula22-say-y{i}.m4a"} for i, t in enumerate(
             ["What's your ringtone?", "Do you prefer calling or texting?", "Do you listen to your voicemail?",
              "When do you put your phone on silent mode?"], 1)]},
    ],
}

AULA22_READING = {
    "title": "Reading — the phone call disaster",
    "lesson": 22,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA22_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto da Carla sobre um dia em que tudo deu errado ao telefone. "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula22-reading.m4a",
         "text": "THE PHONE CALL DISASTER\n\n"
                 "Yesterday, I needed to talk to my bank about a problem with my card. I dialed the helpline number, "
                 "and a recorded voice said: \"Please hold.\" They put me on hold for 25 minutes!\n"
                 "Finally, a woman answered. But in the middle of the conversation, I was cut off. I called back, "
                 "but the line was busy.\n"
                 "Then, at 3 p.m., I had an important meeting with my boss. I forgot to put my phone on silent mode, "
                 "and it went off in the middle of the meeting. My ringtone is a very loud rock song. How embarrassing!\n"
                 "It was the bank. I couldn't answer, so they left a message on my voicemail.\n"
                 "In the evening, I texted my best friend: \"Worst phone day ever!\""},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Why did Carla call the bank? → [A problem with her card.]",
         "text": "1. How long was she on hold? → [*25 minutes.|5 minutes.|An hour.]\n"
                 "2. What happened in the middle of the conversation? → [*She was cut off.|She hung up.|The woman laughed.]\n"
                 "3. When did her phone go off? → [*In the middle of a meeting with her boss.|At the bank.|In the evening.]\n"
                 "4. Who left a voicemail? → [*The bank.|Her boss.|Her best friend.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Carla's ringtone is a rock song. → True",
         "statements": [
             {"text": "Carla's phone was on silent mode in the meeting.", "answer": False,
              "translation": "O celular da Carla estava no modo silencioso na reunião."},
             {"text": "When she called back, the line was busy.", "answer": True,
              "translation": "Quando ela ligou de volta, a linha estava ocupada."},
         ]},
        {"type": "fill",
         "prompt": "Find the phone words in the text.",
         "translation": "Encontre as palavras de telefone no texto.",
         "example": "central de atendimento → [helpline]",
         "text": "1. discou → [dialed|dialled]\n2. ligou de volta → [called back]\n3. mandou mensagem → [texted]"},
    ],
}

AULA22_WRITING = {
    "title": "Writing — my phone rules",
    "lesson": 22,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Use o vocabulário de telefone + should / shouldn't / must / mustn't.",
    "topic": AULA22_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Aguarde, por favor. → Please hold.",
         "text": "1. Eu perdi a ligação dele, então vou ligar de volta mais tarde. → [I missed his call, so I'll call him back "
                 "later.|I missed his call, so I will call him back later.]\n"
                 "2. A linha está ocupada. → [The line's busy.|The line is busy.|The line's engaged.|The line is engaged.]"},
        {"type": "free",
         "prompt": "Write your phone etiquette rules: at least 5 tips using the vocabulary of the lesson "
                   "(silent mode, call back, voicemail, loudspeaker, hang up, texting…).",
         "translation": "Escreva as suas regras de etiqueta no telefone: pelo menos 5 dicas usando o vocabulário da aula.",
         "example": "You should put your phone on silent mode at the cinema.",
         "model_answer": "You should put your phone on silent mode at the cinema and in meetings.\n"
                         "You shouldn't use the loudspeaker on the bus.\n"
                         "If you miss a call, you should call back.\n"
                         "You should leave a short message on the voicemail.\n"
                         "You mustn't text while you're driving!",
         "keywords": ["silent mode", "call back", "should"], "min_words": 30, "points": 4},
    ],
}


AULA22_VIDEO = _video(22, AULA22_TOPIC, "Video — On the phone",
                      "o Bruno apresenta situações de telefone e uma dica de etiqueta.",
                      "aula22-video", [
    _q("What is the man doing?", "O que o homem está fazendo?", "He's dialing a number.", "He's texting.", "He hung up.", "He's on hold."),
    _q("What is she doing?", "O que ela está fazendo?", "She's texting a friend.", "She's dialing a number.", "She's calling back.", "She's on hold."),
    _q("At the cinema, you should…", "No cinema, você deveria…", "put your phone on silent mode.", "use the loudspeaker.", "call your friends.", "choose a new ringtone."),
    _q("What happened to the call?", "O que aconteceu com a ligação?", "It was cut off.", "It was on hold.", "It went to voicemail.", "The line was busy."),
])

# ---------- Aula 23 — Have To & Don't Have To (https://youtu.be/gWwQJnochaE) ----------

AULA23_TOPIC = "Aula 23 — Have To & Don't Have To"

AULA23_FORMS = {
    "title": "Have to: obligation (rules and laws)",
    "lesson": 23,
    "description": "HAVE TO = ter que (obrigação EXTERNA, que não depende da sua vontade: regras, leis, horários).\n"
                   "You have to wear a mask. · I start work at 8. I have to be punctual. · They have to wear a uniform. · "
                   "You have to wear a seat belt in the car.\n"
                   "HAVE TO é um verbo NORMAL (não é modal): muda com he / she / it → She HAS to wear glasses.\n"
                   "PASSADO: HAD TO para todos → I had to wear a uniform at school. (pronúncia: \"hédtə\" ligado)\n"
                   "PERGUNTAS com do / does / did: Do you have to cook tonight? · Does she have to wake up early? · "
                   "Did you have to clean the house yesterday? → Yes, I do / she does / I did. · No, I don't / she doesn't / I didn't.",
    "topic": AULA23_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose have to, has to or had to.",
         "translation": "Escolha have to, has to ou had to.",
         "example": "She [has to] wear glasses.",
         "text": "1. They [*have to|has to] travel on business.\n2. She always [*has to|have to] travel on business.\n"
                 "3. He [*had to|has to] go to the doctor last week.\n4. I [*had to|have to] wear a uniform in school when I was a kid.\n"
                 "5. We [*have to|has to] buy food for dinner."},
        {"type": "dropdown",
         "prompt": "Is the sentence correct? (from the lesson)",
         "translation": "A frase está correta? (exercício da aula)",
         "example": "He had to travel on business last month. → [Correct]",
         "text": "1. She always have to travel on business. → [*Incorrect|Correct]\n"
                 "2. They have wear a uniform. → [*Incorrect|Correct]\n"
                 "3. He had to go to the doctor last week. → [*Correct|Incorrect]\n"
                 "4. Does she has to wake up early? → [*Incorrect|Correct]"},
        {"type": "fill",
         "prompt": "Make questions.",
         "translation": "Faça as perguntas.",
         "example": "you / cook tonight → Do you have to cook tonight?",
         "text": "1. she / wake up early → [Does she have to wake up early?]\n"
                 "2. you / clean the house yesterday → [Did you have to clean the house yesterday?]\n"
                 "3. what time / you / arrive at work → [What time do you have to arrive at work?]"},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas curtas.",
         "example": "Do you have to cook tonight? → Yes, I do.",
         "pairs": [
             {"left": "Does he have to wear glasses?", "right": "Yes, he does."},
             {"left": "Did you have to pay for the tickets?", "right": "No, I didn't. They were free."},
             {"left": "What time do you have to get up tomorrow?", "right": "I have to get up at 6 a.m."},
             {"left": "Do they have to wear a uniform?", "right": "No, they don't."},
         ]},
    ],
}

AULA23_CONTRAST = {
    "title": "Don't have to or mustn't?",
    "lesson": 23,
    "description": "AFIRMATIVA — parecidos: have to e must = obrigação.\n"
                   "  HAVE TO → obrigação externa, geral (regras, leis): I have to wear a shirt and tie at work. It's the rule.\n"
                   "  MUST → obrigação pessoal, decisão sua: I must buy a new shirt. This one is too old.\n"
                   "NEGATIVA — COMPLETAMENTE DIFERENTES!\n"
                   "  DON'T HAVE TO = não é necessário (você pode, se quiser): You don't have to pay. This museum is free. · "
                   "You don't have to drive. We can get a train.\n"
                   "  MUSTN'T = é PROIBIDO: You mustn't drive along this street. It's against the law.\n"
                   "You are invited → I don't have to go. (opcional) · No entry → I mustn't go. (proibido)",
    "topic": AULA23_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose the correct option (exercise from the lesson).",
         "translation": "Escolha a opção correta (exercício da aula).",
         "example": "I [have to] turn off my phone before the flight. It's the rule.",
         "text": "1. Employees [*have to|mustn't] answer the phone in English at this office.\n"
                 "2. You [*don't have to|mustn't] leave a voicemail. You can just call back later.\n"
                 "3. I [*must|don't have to] remember to call her back. It's really important.\n"
                 "4. You [*mustn't|don't have to] hang up without saying goodbye. That's rude.\n"
                 "5. She [*doesn't have to|mustn't] wear a uniform. Casual clothes are fine at the office."},
        {"type": "group",
         "prompt": "Not necessary or prohibited?",
         "translation": "Não é necessário (don't have to) ou é proibido (mustn't)?",
         "example": "You ___ pay. The museum is free. → don't have to",
         "categories": ["don't have to (not necessary)", "mustn't (prohibited)"],
         "words": [
             {"text": "You ___ pay. The museum is free.", "category": "don't have to (not necessary)"},
             {"text": "You ___ go to the party if you don't want to.", "category": "don't have to (not necessary)"},
             {"text": "We ___ drive. We can get a train.", "category": "don't have to (not necessary)"},
             {"text": "You ___ smoke in the hospital.", "category": "mustn't (prohibited)"},
             {"text": "You ___ drive along this street. It's against the law.", "category": "mustn't (prohibited)"},
             {"text": "You ___ use your phone during the test.", "category": "mustn't (prohibited)"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "Have to exists in all tenses. → True",
         "statements": [
             {"text": "\"Don't have to\" and \"mustn't\" have the same meaning.", "answer": False,
              "translation": "\"Don't have to\" e \"mustn't\" têm o mesmo significado."},
             {"text": "\"Have to\" is common for rules and laws.", "answer": True,
              "translation": "\"Have to\" é comum para regras e leis."},
             {"text": "MUST has a past form: \"musted\".", "answer": False,
              "translation": "MUST tem forma no passado: \"musted\"."},
         ]},
    ],
}

AULA23_LISTENING = {
    "title": "Listening — the first day at a new job",
    "lesson": 23,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: have to = \"héftə\" · has to = \"héstə\" · had to = \"hédtə\" (tudo ligado).",
    "topic": AULA23_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"I have to go.\" → have to",
         "audio": f"{AUDIO}/aula23-words.m4a",
         "text": "1. She [*has to|have to] work today.\n2. I [*had to|have to] wear a uniform.\n3. You [*don't have to|mustn't] pay.\n"
                 "4. [*Do you have to|Did you have to] cook tonight?\n5. You [*mustn't|don't have to] smoke here."},
        {"type": "info",
         "prompt": "Now listen: the manager explains the rules to Lucas, a new employee.",
         "translation": "Agora ouça: a gerente explica as regras da loja para o Lucas, funcionário novo. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula23-job.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "group",
         "prompt": "Listen again. Have to, don't have to or mustn't?",
         "translation": "Ouça de novo. Cada regra é have to, don't have to ou mustn't?",
         "example": "arrive at 8:45 → have to",
         "categories": ["has to", "doesn't have to", "mustn't"],
         "words": [
             {"text": "arrive at 8:45", "category": "has to"},
             {"text": "wear the store T-shirt", "category": "has to"},
             {"text": "wear a tie", "category": "doesn't have to"},
             {"text": "work on Sundays", "category": "doesn't have to"},
             {"text": "use his phone in front of customers", "category": "mustn't"},
             {"text": "eat in the store", "category": "mustn't"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Lucas is a new employee. → True",
         "statements": [
             {"text": "Lucas has to bring his lunch.", "answer": False, "translation": "O Lucas tem que trazer o almoço."},
             {"text": "At his old job, Lucas had to work on weekends.", "answer": True,
              "translation": "No emprego antigo, o Lucas tinha que trabalhar nos fins de semana."},
         ]},
    ],
}

AULA23_SPEAKING = {
    "title": "Speaking — have to: ask and answer",
    "lesson": 23,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: had to = \"hédtə\" — não pronuncie os dois sons, junte!",
    "topic": AULA23_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula23-say-s{i}.m4a"} for i, t in enumerate(
             ["You have to wear a mask.", "She has to wear glasses.", "I had to wear a uniform at school.",
              "Do you have to cook tonight?", "You don't have to pay. This museum is free.",
              "You mustn't drive along this street.", "I have to be punctual."], 1)]},
        {"type": "speak",
         "prompt": "Ask and answer: answer the questions about YOU.",
         "translation": "Ask and answer: responda às perguntas da aula sobre VOCÊ.",
         "example": "\"What time do you have to get up tomorrow?\" → \"I have to get up at 6 a.m.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula23-say-y{i}.m4a"} for i, t in enumerate(
             ["What time do you have to get up tomorrow?", "Did you have to cook lunch yesterday?",
              "What time do you have to arrive at work?", "Did you have to wear a uniform at school?",
              "What don't you have to do on weekends?"], 1)]},
    ],
}

AULA23_READING = {
    "title": "Reading — social media manners",
    "lesson": 23,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA23_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça um artigo com regras de boas maneiras nas redes sociais. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula23-reading.m4a",
         "text": "SOCIAL MEDIA MANNERS 📱\n\n"
                 "Good manners are important online, too! Here are some tips.\n"
                 "You have to be careful with personal information. Your address and your phone number are private.\n"
                 "You mustn't post a private message or conversation without permission. That's very rude!\n"
                 "You don't have to answer every comment. It's OK to ignore some people.\n"
                 "You don't have to post all the details of your breakup with a partner. Some things are better offline.\n"
                 "And you must think before you post. Remember: the internet never forgets!"},
        {"type": "group",
         "prompt": "According to the text: have to / must, don't have to or mustn't?",
         "translation": "De acordo com o texto: obrigação, não é necessário ou proibido?",
         "example": "be careful with personal information → obligation",
         "categories": ["obligation (have to / must)", "not necessary (don't have to)", "prohibited (mustn't)"],
         "words": [
             {"text": "be careful with personal information", "category": "obligation (have to / must)"},
             {"text": "think before you post", "category": "obligation (have to / must)"},
             {"text": "answer every comment", "category": "not necessary (don't have to)"},
             {"text": "post all the details of your breakup", "category": "not necessary (don't have to)"},
             {"text": "post a private conversation without permission", "category": "prohibited (mustn't)"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Good manners are important online. → True",
         "statements": [
             {"text": "You have to answer every comment.", "answer": False,
              "translation": "Você tem que responder todos os comentários."},
             {"text": "Your address is private information.", "answer": True,
              "translation": "O seu endereço é uma informação privada."},
         ]},
        {"type": "fill",
         "prompt": "Complete according to the text.",
         "translation": "Complete de acordo com o texto.",
         "example": "You [have] to be careful with personal information.",
         "text": "1. You [mustn't] post a private message without permission.\n"
                 "2. You don't have to [answer] every comment.\n3. You [must] think before you post."},
    ],
}

AULA23_WRITING = {
    "title": "Writing — rules at work or school",
    "lesson": 23,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ have / has to (obrigação) · had to (passado) · don't / doesn't have to (não é necessário) · "
                   "mustn't (proibido).",
    "topic": AULA23_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Você não precisa pagar. → You don't have to pay.",
         "text": "1. Ela tem que usar óculos. → [She has to wear glasses.]\n"
                 "2. Eu tive que pagar pelos ingressos. → [I had to pay for the tickets.]\n"
                 "3. Você não precisa ir à festa. → [You don't have to go to the party.|You do not have to go to the party.]"},
        {"type": "free",
         "prompt": "Write about the rules at your work or school (now and in the past): things you have to do, "
                   "things you don't have to do and things you mustn't do. Use had to for the past.",
         "translation": "Escreva sobre as regras do seu trabalho ou escola (agora e no passado): o que você tem que fazer, "
                        "o que não precisa fazer e o que é proibido. Use had to para o passado.",
         "example": "At my work, I have to arrive at 8 a.m.",
         "model_answer": "At my work, I have to arrive at 8 a.m. and I have to answer the phone in English.\n"
                         "I don't have to wear a uniform, and I don't have to work on weekends.\n"
                         "We mustn't use our phones in meetings.\n"
                         "When I was at school, I had to wear a uniform every day.",
         "keywords": ["have to", "don't have to", "had to"], "min_words": 30, "points": 4},
    ],
}


AULA23_VIDEO = _video(23, AULA23_TOPIC, "Video — Our jobs",
                      "a Sarah fala das obrigações no trabalho dela e dos irmãos com have to e don't have to.",
                      "aula23-video", [
    _q("Complete: My sister ___ wear a uniform.", "Complete: minha irmã ___ usar uniforme.", "has to", "have to", "has", "must to"),
    _q("What time does the sister have to wake up?", "A que horas a irmã tem que acordar?", "At 5:30.", "At 6:30.", "At 8:00.", "At 4:30."),
    _q("What does her brother have to do?", "O que o irmão dela tem que fazer?", "Travel a lot.", "Wear a nurse uniform.", "Work at home.", "Wake up at noon."),
    _q("Complete: I ___ wear a uniform.", "Complete: eu ___ usar uniforme (não é necessário).", "don't have to", "mustn't", "haven't to", "doesn't have to"),
])

# ---------- Aula 24 — Bucket List (https://youtu.be/cqR6134vy_c) ----------

AULA24_TOPIC = "Aula 24 — Bucket List"

AULA24_VOCAB = {
    "title": "What's a bucket list?",
    "lesson": 24,
    "description": "BUCKET = balde · KICK THE BUCKET = morrer (expressão MUITO informal, como \"bater as botas\" — "
                   "não é o mesmo que \"chutar o balde\" em português!)\n"
                   "BUCKET LIST = a list of the things that a person would like to do or achieve before they die "
                   "(lista de coisas para fazer antes de morrer). I have so many things on my bucket list yet to do!\n"
                   "Ideias populares: get a tattoo · visit Paris · run a marathon · go on a hot-air balloon · "
                   "learn new languages · go bungee jumping\n"
                   "Expressões com verbos: make a list · go on holiday · ride a horse · learn a language · go for a walk · "
                   "make a dream come true · cook a recipe · get in a taxi",
    "topic": AULA24_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose the verb to complete the phrases (exercise from the lesson).",
         "translation": "Escolha o verbo que completa as expressões (exercício da aula).",
         "example": "[make] a list",
         "text": "1. [*go|make|ride] on holiday\n2. [*ride|cook|get] a horse\n3. [*learn|go|make] a language\n"
                 "4. [*go|make|cook] for a walk\n5. [*make|go|ride] a dream come true\n6. [*cook|ride|go] a recipe\n"
                 "7. [*get|make|learn] in a taxi"},
        {"type": "match",
         "prompt": "Match the bucket list ideas to Portuguese.",
         "translation": "Ligue as ideias de bucket list ao português.",
         "example": "get a tattoo → fazer uma tatuagem",
         "pairs": [
             {"left": "run a marathon", "right": "correr uma maratona"},
             {"left": "go on a hot-air balloon", "right": "andar de balão"},
             {"left": "go bungee jumping", "right": "pular de bungee jump"},
             {"left": "ride a horse", "right": "andar a cavalo"},
             {"left": "make a dream come true", "right": "realizar um sonho"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Bucket\" means balde. → True",
         "statements": [
             {"text": "\"Kick the bucket\" means \"die\" (very informal).", "answer": True,
              "translation": "\"Kick the bucket\" significa \"morrer\" (bem informal)."},
             {"text": "\"Kick the bucket\" is good for a serious conversation.", "answer": False,
              "translation": "\"Kick the bucket\" é bom para uma conversa séria."},
             {"text": "A bucket list is a list of things to buy at the supermarket.", "answer": False,
              "translation": "Bucket list é uma lista de compras do supermercado."},
         ]},
    ],
}

AULA24_WOULD = {
    "title": "Would you like to…? I'd like to…",
    "lesson": 24,
    "description": "WOULD LIKE TO = gostaria de (desejos, sonhos):\n"
                   "Which would you like to do? → I would like to visit Paris. · I'd like to learn Italian.\n"
                   "Contrações: I'd · you'd · he'd · she'd · it'd · we'd · they'd\n"
                   "Negativa: would not = WOULDN'T → I wouldn't like to go on a cruise.\n"
                   "Pergunta: Would you like to visit Antarctica? → Yes, I would. / No, I wouldn't.\n"
                   "Pronúncia: would = \"wud\" — lábios arredondados no W e o L é MUDO.\n"
                   "Frases úteis: I would really like to go bungee jumping. · One of my dreams is to…",
    "topic": AULA24_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta.",
         "example": "I [would like to] visit Paris.",
         "text": "1. [*Would you like to|Do you would like to|Would you like] visit Antarctica?\n"
                 "2. Would you like to fly first class? — Yes, I [*would|like|do].\n"
                 "3. I [*wouldn't like to|don't would like to|wouldn't like] go on a cruise.\n"
                 "4. She[*'d like to|'d like|like to would] learn Japanese.\n"
                 "5. Would you like to climb Mount Everest? — No, I [*wouldn't|don't like|not would]."},
        {"type": "fill",
         "prompt": "Write the contraction.",
         "translation": "Escreva a contração.",
         "example": "I would → I'd",
         "text": "1. you would → [you'd]\n2. she would → [she'd]\n3. we would → [we'd]\n4. they would → [they'd]\n"
                 "5. would not → [wouldn't]"},
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras em ordem. (Eu gostaria muito de pular de bungee jump.)",
         "example": "like / I'd / to / Paris / visit → I'd like to visit Paris.",
         "tokens": ["I", "would", "really", "like", "to", "go", "bungee", "jumping."], "alternatives": []},
    ],
}

AULA24_LISTENING = {
    "title": "Listening — two bucket lists",
    "lesson": 24,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: I'd like to = \"áid láik tə\" — tudo ligado e rápido.",
    "topic": AULA24_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"I'd like to visit Paris.\" → I'd like to",
         "audio": f"{AUDIO}/aula24-words.m4a",
         "text": "1. [*I'd like to|I like to] ride a horse.\n2. [*Would you|Do you] like to go surfing?\n"
                 "3. She [*wouldn't|would] like to get a tattoo.\n4. [*We'd|We] like to learn Spanish.\n5. Yes, I [*would|do]."},
        {"type": "info",
         "prompt": "Now listen: Bia and Rafa talk about their bucket lists.",
         "translation": "Agora ouça: a Bia e o Rafa conversam sobre as bucket lists deles. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula24-lists.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "They're talking about their [bucket lists].",
         "text": "1. What would Bia like to see in Japan? → [*The cherry blossoms.|Mount Fuji.|The temples.]\n"
                 "2. What would Rafa like to do in New York? → [*Get in a yellow taxi, like in the movies.|Run a marathon.|"
                 "Visit museums.]\n"
                 "3. What wouldn't Bia like to do? → [*Go bungee jumping.|Ride a horse.|Learn Japanese.]\n"
                 "4. What would Rafa like to cook? → [*A traditional recipe from every country he visits.|Japanese food.|Pizza.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Bia would like to go to Japan. → True",
         "statements": [
             {"text": "Rafa is afraid of heights.", "answer": False, "translation": "O Rafa tem medo de altura."},
             {"text": "Bia would like to learn to ride a horse.", "answer": True,
              "translation": "A Bia gostaria de aprender a andar a cavalo."},
         ]},
    ],
}

AULA24_SPEAKING = {
    "title": "Speaking — my bucket list",
    "lesson": 24,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: would = \"wud\" (sem L!) · I'd = \"áid\".",
    "topic": AULA24_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula24-say-s{i}.m4a"} for i, t in enumerate(
             ["would, wouldn't", "I'd, you'd, he'd, she'd, it'd, we'd, they'd",
              "I have so many things on my bucket list yet to do.", "I would really like to go bungee jumping.",
              "I wouldn't like to go on a cruise.", "One of my dreams is to visit Paris."], 1)]},
        {"type": "speak",
         "prompt": "Would you like to…? Answer about YOU.",
         "translation": "Would you like to…? Responda sobre VOCÊ (perguntas da aula).",
         "example": "\"Would you like to visit Antarctica?\" → \"No, I wouldn't. It's too cold!\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula24-say-y{i}.m4a"} for i, t in enumerate(
             ["Would you like to visit Antarctica?", "Would you like to climb Mount Everest?",
              "Would you like to fly first class?", "Would you like to go surfing?", "Would you like to become famous?"], 1)]},
    ],
}

AULA24_READING = {
    "title": "Reading — Grandpa's bucket list",
    "lesson": 24,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA24_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto da Lara sobre a bucket list do avô dela. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula24-reading.m4a",
         "text": "GRANDPA'S BUCKET LIST\n\n"
                 "My grandpa Jorge is 75, and last year he made a bucket list. He says, \"I'm not going to kick the bucket "
                 "before I do all these things!\"\n"
                 "The first thing on his list was \"go on a hot-air balloon\". In March, we went together. "
                 "He loved it — I was a little scared!\n"
                 "Now he would like to learn a new language. He chose Italian, because his parents were from Italy. "
                 "He'd also like to visit their village there.\n"
                 "He wouldn't like to go bungee jumping (\"I'm old, not crazy!\"), but he'd really like to run a "
                 "5 km race. He walks every morning to practice.\n"
                 "The last item on his list? \"Make a dream come true for my granddaughter.\" I think I'd like to "
                 "go to Italy with him!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "How old is Grandpa Jorge? → [75.]",
         "text": "1. What was the first thing on his list? → [*Go on a hot-air balloon.|Learn Italian.|Run a marathon.]\n"
                 "2. Why would he like to learn Italian? → [*His parents were from Italy.|He has an Italian friend.|"
                 "For his job.]\n"
                 "3. What wouldn't he like to do? → [*Go bungee jumping.|Run a 5 km race.|Visit Italy.]\n"
                 "4. What does he do every morning? → [*He walks.|He studies Italian.|He swims.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Grandpa made a bucket list. → True",
         "statements": [
             {"text": "Lara was a little scared in the balloon.", "answer": True,
              "translation": "A Lara ficou com um pouco de medo no balão."},
             {"text": "Grandpa would like to run a marathon.", "answer": False,
              "translation": "O avô gostaria de correr uma maratona."},
         ]},
        {"type": "fill",
         "prompt": "Complete according to the text.",
         "translation": "Complete de acordo com o texto.",
         "example": "He would like to [learn] a new language.",
         "text": "1. He'd also like to [visit] their village.\n2. He [wouldn't] like to go bungee jumping.\n"
                 "3. I think I'd like to [go] to Italy with him!"},
    ],
}

AULA24_WRITING = {
    "title": "Writing — my mini bucket list",
    "lesson": 24,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ I'd like to… · I'd also like to… · I'd really love to… · I wouldn't like to… · "
                   "One of my dreams is to…\n"
                   "Verbos úteis: make, go, ride, learn, cook, get, visit, try.",
    "topic": AULA24_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu gostaria de visitar Paris. → I'd like to visit Paris.",
         "text": "1. Eu gostaria de aprender italiano. → [I'd like to learn Italian.|I would like to learn Italian.]\n"
                 "2. Você gostaria de ficar famoso? → [Would you like to become famous?|Would you like to be famous?]"},
        {"type": "free",
         "prompt": "Just like in the lesson, make your own mini bucket list: write three things you would like to do "
                   "before you are 40 (or 60, or…), and one thing you wouldn't like to do. Explain why.",
         "translation": "Como na aula, faça a sua mini bucket list: três coisas que você gostaria de fazer antes dos 40 "
                        "(ou 60…) e uma que você não gostaria. Explique por quê.",
         "example": "I'd like to visit Canada, because I love snow.",
         "model_answer": "Before I'm 40, I'd like to visit Canada, because I love snow.\n"
                         "I'd also like to learn Italian and cook a traditional recipe from every country I visit.\n"
                         "One of my dreams is to ride a horse on the beach.\n"
                         "But I wouldn't like to go bungee jumping. I'm afraid of heights!",
         "keywords": ["I'd like to", "wouldn't like to"], "min_words": 30, "points": 4},
    ],
}


AULA24_VIDEO = _video(24, AULA24_TOPIC, "Video — My bucket list",
                      "a Sarah mostra a bucket list dela com I'd like to e I wouldn't like to.",
                      "aula24-video", [
    _q("Where would Sarah like to go on a hot-air balloon?", "Onde a Sarah gostaria de andar de balão?", "In Turkey.", "In Brazil.", "In Japan.", "In Paris."),
    _q("What would she like to get?", "O que ela gostaria de fazer?", "A small tattoo.", "A new car.", "A big house.", "A dog."),
    _q("Complete: I'd really like to ___ a marathon.", "Complete: eu gostaria muito de ___ uma maratona.", "run", "to run", "running", "runs"),
    _q("What would she like to learn?", "O que ela gostaria de aprender?", "To ride a horse.", "To surf.", "To cook.", "To fly a plane."),
])

# ---------- Aula 25 — Would Like To & Want (https://youtu.be/FqrkKg7jNAU) ----------

AULA25_TOPIC = "Aula 25 — Would Like To & Want"

AULA25_WOULD = {
    "title": "Would like to: wishes and polite requests",
    "lesson": 25,
    "description": "WOULD LIKE TO → desejos, vontades e pedidos educados.\n"
                   "AFFIRMATIVE: I would like to visit Japan. = I'd like to visit Japan.\n"
                   "NEGATIVE: I would not like to climb Everest. = I wouldn't like to climb Everest.\n"
                   "QUESTION: Would + sujeito + like to…? → What would she like to do next year? · Would you like to go surfing?\n"
                   "Igual para todos (sem S para he / she / it), como os modal verbs.\n"
                   "Contração só quando possível: ✓ They'd like to… · ✗ My brother'd (com nome, escreva would) · "
                   "✗ Would no início da pergunta não contrai.\n"
                   "SHORT ANSWERS: Yes, I would. / No, I wouldn't. (✗ Yes, I'd. — resposta curta precisa de 3 palavras!)",
    "topic": AULA25_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Complete with would like to or wouldn't like to (exercise from the lesson).",
         "translation": "Complete com would like to ou wouldn't like to, usando contração quando possível "
                        "(exercício da aula).",
         "example": "I['d like to] travel to New Zealand. It looks incredible.",
         "text": "1. She [*wouldn't like to|'d like to] eat insects. She says it's disgusting.\n"
                 "2. [*Would you like to|You'd like to] visit the Amazon rainforest one day?\n"
                 "3. My brother [*would like to|'d like to] learn to play the guitar.\n"
                 "4. We [*wouldn't like to|'d like to] sleep in a tent. We prefer a comfortable hotel.\n"
                 "5. What [*would you like to|you would like to] do if you had one free year?\n"
                 "6. They[*'d like to|wouldn't like to] see the pyramids in Egypt.\n"
                 "7. He [*wouldn't like to|'d like to] go bungee jumping. He's afraid of heights."},
        {"type": "dropdown",
         "prompt": "Choose the right short answer.",
         "translation": "Escolha a resposta curta certa.",
         "example": "Would you like to surf? → [Yes, I would.]",
         "text": "1. Would you like to visit Paris? (✓) → [*Yes, I would.|Yes, I'd.|Yes, I like.]\n"
                 "2. Would she like to go surfing? (✗) → [*No, she wouldn't.|No, she doesn't.|No, she'd not.]\n"
                 "3. Would they like to come? (✓) → [*Yes, they would.|Yes, they'd.|Yes, they want.]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Would like to\" doesn't change for he / she / it. → True",
         "statements": [
             {"text": "\"Yes, I'd.\" is a correct short answer.", "answer": False,
              "translation": "\"Yes, I'd.\" é uma resposta curta correta."},
             {"text": "We say \"She would likes to travel\".", "answer": False,
              "translation": "Dizemos \"She would likes to travel\"."},
             {"text": "\"I'd like to\" is the contraction of \"I would like to\".", "answer": True,
              "translation": "\"I'd like to\" é a contração de \"I would like to\"."},
         ]},
    ],
}

AULA25_WANT = {
    "title": "Would like or want?",
    "lesson": 25,
    "description": "WOULD LIKE TO × WANT TO: o sentido é muito parecido!\n"
                   "Would like to → mais educado e formal: I'd like to visit Paris. · Would you like to dance?\n"
                   "Want to → mais direto e informal: I want to visit Paris. · Do you want to dance?\n"
                   "ATENÇÃO — PEDIDOS em restaurantes, hotéis, lojas: em português \"eu quero uma água\" é normal; "
                   "em inglês, \"I want…\" soa INDELICADO. Use WOULD LIKE + coisa:\n"
                   "Would you like anything to drink? → I'd like a glass of wine, please. · I'd like some water, please.\n"
                   "(✗ I want some water.)",
    "topic": AULA25_TOPIC,
    "items": [
        {"type": "choice",
         "prompt": "You are at a restaurant. The waiter asks: \"Would you like anything to drink?\" What do you say?",
         "translation": "Você está num restaurante. O garçom pergunta: \"Would you like anything to drink?\" O que você responde?",
         "example": "Pedido educado → I'd like…",
         "options": ["I'd like some water, please.", "I want water.", "Give me water.", "I would like to water, please."],
         "correct": 0},
        {"type": "group",
         "prompt": "More polite or more direct?",
         "translation": "Mais educado / formal ou mais direto / informal? Coloque cada frase no grupo certo.",
         "example": "Would you like to dance? → more polite",
         "categories": ["more polite / formal", "more direct / informal"],
         "words": [
             {"text": "Would you like to dance?", "category": "more polite / formal"},
             {"text": "I'd like to visit Paris.", "category": "more polite / formal"},
             {"text": "I'd like a glass of wine, please.", "category": "more polite / formal"},
             {"text": "Do you want to dance?", "category": "more direct / informal"},
             {"text": "I want to visit Paris.", "category": "more direct / informal"},
             {"text": "I want a soda.", "category": "more direct / informal"},
         ]},
        {"type": "fill",
         "prompt": "Make these requests polite.",
         "translation": "Deixe os pedidos educados (use I'd like… please).",
         "example": "I want a coffee. → I'd like a coffee, please.",
         "text": "1. I want a glass of water. → [I'd like a glass of water, please.|I would like a glass of water, please.]\n"
                 "2. I want the chicken. → [I'd like the chicken, please.|I would like the chicken, please.]"},
    ],
}

AULA25_LISTENING = {
    "title": "Listening — at the hotel",
    "lesson": 25,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: I'd like = \"áid láik\" (o D quase some) · would you = \"wúdju\".",
    "topic": AULA25_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"I'd like a coffee.\" → I'd like",
         "audio": f"{AUDIO}/aula25-words.m4a",
         "text": "1. [*I'd like|I like] a room, please.\n2. [*Would you like|Do you like] some tea?\n"
                 "3. [*I want to|I wanted to] go home.\n4. She [*wouldn't like|would like] to sleep in a tent.\n"
                 "5. [*They'd like|They like] to see the pyramids."},
        {"type": "info",
         "prompt": "Now listen: Mr. and Mrs. Alves arrive at a hotel.",
         "translation": "Agora ouça: o casal Alves chega a um hotel e conversa com a recepcionista. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula25-hotel.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "They are at a [hotel].",
         "text": "1. What kind of room would they like? → [*A room with a sea view.|A room near the pool.|A small room.]\n"
                 "2. How many nights would they like to stay? → [*Three.|Two.|Seven.]\n"
                 "3. What would Mrs. Alves like to drink? → [*A glass of orange juice.|A coffee.|Some water.]\n"
                 "4. What would they like to do tomorrow? → [*Go on a boat tour.|Go bungee jumping.|Sleep all day.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "The receptionist is polite. → True",
         "statements": [
             {"text": "Mr. Alves would like a coffee.", "answer": True, "translation": "O Sr. Alves gostaria de um café."},
             {"text": "They would like breakfast in their room.", "answer": False,
              "translation": "Eles gostariam de tomar café da manhã no quarto."},
         ]},
    ],
}

AULA25_SPEAKING = {
    "title": "Speaking — I'd like…, please",
    "lesson": 25,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: arredonde os lábios no W de would · o L é mudo.",
    "topic": AULA25_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula25-say-s{i}.m4a"} for i, t in enumerate(
             ["I would like to visit Japan.", "I'd like to travel to New Zealand. It looks incredible.",
              "I wouldn't like to go bungee jumping.", "What would she like to do next year?",
              "Would you like to dance?", "Would you like anything to drink?", "I'd like a glass of wine, please.",
              "I'd like some water, please."], 1)]},
        {"type": "speak",
         "prompt": "Ask and answer about YOU.",
         "translation": "Ask and answer: responda sobre VOCÊ.",
         "example": "\"Would you like to surf?\" → \"Yes, I would.\" / \"No, I wouldn't.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula25-say-y{i}.m4a"} for i, t in enumerate(
             ["Would you like to surf?", "Would you like to visit Paris?", "Would you like to eat insects?",
              "What would you like to do if you had one free year?", "Would you like anything to drink?"], 1)]},
    ],
}

AULA25_READING = {
    "title": "Reading — a gap year",
    "lesson": 25,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA25_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text.",
         "translation": "Leia e ouça o texto da Júlia, que vai tirar um ano sabático (gap year). "
                        "As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula25-reading.m4a",
         "text": "MY GAP YEAR\n\n"
                 "Next year, I'm taking a gap year: one free year before university! So, what would I like to do?\n"
                 "First, I'd like to travel to New Zealand. It looks incredible! I'd also like to see the pyramids in Egypt.\n"
                 "My best friend, Duda, would like to come with me, but she wouldn't like to go to Egypt. "
                 "She says it's too hot!\n"
                 "I'd really like to learn to surf, and I want to improve my English, so I'd like to work in a café in Australia.\n"
                 "My parents asked: \"Would you like to stay with your aunt in Sydney?\" Yes, I would! It's cheaper than a hotel.\n"
                 "One thing I wouldn't like to do: sleep in a tent. I prefer a comfortable bed!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "What's Júlia taking next year? → [A gap year.]",
         "text": "1. Where would she like to travel first? → [*To New Zealand.|To Egypt.|To Australia.]\n"
                 "2. Why wouldn't Duda like to go to Egypt? → [*It's too hot.|It's too expensive.|It's too far.]\n"
                 "3. Why would she like to work in a café in Australia? → [*To improve her English.|To learn to cook.|"
                 "To meet her aunt.]\n"
                 "4. What wouldn't Júlia like to do? → [*Sleep in a tent.|Learn to surf.|Stay with her aunt.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Júlia would like to learn to surf. → True",
         "statements": [
             {"text": "Júlia would like to stay in a hotel in Sydney.", "answer": False,
              "translation": "A Júlia gostaria de ficar num hotel em Sydney."},
             {"text": "Duda would like to travel with Júlia.", "answer": True,
              "translation": "A Duda gostaria de viajar com a Júlia."},
         ]},
        {"type": "fill",
         "prompt": "Complete according to the text.",
         "translation": "Complete de acordo com o texto.",
         "example": "I'd like to [travel] to New Zealand.",
         "text": "1. Duda [would] like to come with me.\n2. She [wouldn't] like to go to Egypt.\n"
                 "3. Would you like to stay with your aunt? — Yes, I [would]."},
    ],
}

AULA25_WRITING = {
    "title": "Writing — my free year",
    "lesson": 25,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ I'd like to… · I wouldn't like to… · I'd really like to… · "
                   "Pedidos educados: I'd like a…, please.",
    "topic": AULA25_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu gostaria de visitar o Japão. → I'd like to visit Japan.",
         "text": "1. Ela não gostaria de dormir numa barraca. → [She wouldn't like to sleep in a tent.|"
                 "She would not like to sleep in a tent.]\n"
                 "2. Você gostaria de dançar? → [Would you like to dance?]\n"
                 "3. Eu gostaria de um café, por favor. → [I'd like a coffee, please.|I would like a coffee, please.|"
                 "I'd like a cup of coffee, please.]"},
        {"type": "free",
         "prompt": "What would you like to do if you had one free year? Write about at least four things you'd like to do "
                   "and one thing you wouldn't like to do.",
         "translation": "O que você gostaria de fazer se tivesse um ano livre? Escreva pelo menos quatro coisas que você "
                        "gostaria de fazer e uma que você não gostaria.",
         "example": "If I had one free year, I'd like to travel around Europe.",
         "model_answer": "If I had one free year, I'd like to travel around Europe by train.\n"
                         "I'd like to visit Italy and learn to cook real pasta.\n"
                         "I'd also like to learn French and run a marathon in Paris.\n"
                         "I'd really like to spend more time with my family.\n"
                         "But I wouldn't like to work in an office!",
         "keywords": ["I'd like to", "wouldn't like to"], "min_words": 30, "points": 4},
    ],
}


AULA25_VIDEO = _video(25, AULA25_TOPIC, "Video — My dream trip",
                      "a Sarah fala da viagem dos sonhos e faz um pedido educado no café.",
                      "aula25-video", [
    _q("Where would Sarah like to travel one day?", "Para onde a Sarah gostaria de viajar um dia?", "To New Zealand.", "To Canada.", "To Japan.", "To Chile."),
    _q("What would she also like to see?", "O que ela também gostaria de ver?", "The pyramids in Egypt.", "The Eiffel Tower.", "Mount Fuji.", "The Amazon."),
    _q("Would she like to surf in Australia?", "Ela gostaria de surfar na Austrália?", "Yes, she would.", "Yes, she'd.", "No, she wouldn't.", "Yes, she does."),
    _q("What's the polite way to order?", "Qual é o jeito educado de pedir?", "I'd like a cappuccino, please.", "I want a cappuccino.", "Give me a cappuccino.", "Cappuccino. Now."),
])


SPECS = (AULA1_REGULAR, AULA1_IRREGULAR, AULA1_LISTENING, AULA1_SPEAKING, AULA1_READING, AULA1_WRITING, AULA1_VIDEO,
         AULA2_SOUNDS, AULA2_VOICED, AULA2_LISTENING, AULA2_SPEAKING, AULA2_READING, AULA2_WRITING, AULA2_VIDEO,
         AULA3_DIDNT, AULA3_SENTENCES, AULA3_LISTENING, AULA3_SPEAKING, AULA3_READING, AULA3_WRITING, AULA3_VIDEO,
         AULA4_DID, AULA4_WH, AULA4_LISTENING, AULA4_SPEAKING, AULA4_READING, AULA4_WRITING, AULA4_VIDEO,
         AULA5_APOSTROPHE, AULA5_WHOSE, AULA5_LISTENING, AULA5_SPEAKING, AULA5_READING, AULA5_WRITING, AULA5_VIDEO,
         AULA6_FORMS, AULA6_ANSWERS, AULA6_LISTENING, AULA6_SPEAKING, AULA6_READING, AULA6_WRITING, AULA6_VIDEO,
         AULA7_SUBJECT, AULA7_OBJECT, AULA7_LISTENING, AULA7_SPEAKING, AULA7_READING, AULA7_WRITING, AULA7_VIDEO,
         AULA8_FORMS, AULA8_GONNA, AULA8_LISTENING, AULA8_SPEAKING, AULA8_READING, AULA8_WRITING, AULA8_VIDEO,
         AULA9_EVIDENCE, AULA9_FUTURE, AULA9_LISTENING, AULA9_SPEAKING, AULA9_READING, AULA9_WRITING, AULA9_VIDEO,
         AULA10_WILL, AULA10_MURPHY, AULA10_LISTENING, AULA10_SPEAKING, AULA10_READING, AULA10_WRITING, AULA10_VIDEO,
         AULA11_USES, AULA11_SHALL, AULA11_LISTENING, AULA11_SPEAKING, AULA11_READING, AULA11_WRITING, AULA11_VIDEO,
         AULA12_CONTRAST, AULA12_QUESTIONS, AULA12_LISTENING, AULA12_SPEAKING, AULA12_READING, AULA12_WRITING, AULA12_VIDEO,
         AULA13_ARRANGEMENTS, AULA13_DIARY, AULA13_LISTENING, AULA13_SPEAKING, AULA13_READING, AULA13_WRITING, AULA13_VIDEO,
         AULA14_CONTRAST, AULA14_SOUNDS, AULA14_LISTENING, AULA14_SPEAKING, AULA14_READING, AULA14_WRITING, AULA14_VIDEO,
         AULA15_VOCAB, AULA15_DETAILS, AULA15_LISTENING, AULA15_SPEAKING, AULA15_READING, AULA15_WRITING, AULA15_VIDEO,
         AULA16_FORMS, AULA16_USES, AULA16_LISTENING, AULA16_SPEAKING, AULA16_READING, AULA16_WRITING, AULA16_VIDEO,
         AULA17_FORMS, AULA17_COULD, AULA17_LISTENING, AULA17_SPEAKING, AULA17_READING, AULA17_WRITING, AULA17_VIDEO,
         AULA18_USES, AULA18_PRACTICE, AULA18_LISTENING, AULA18_SPEAKING, AULA18_READING, AULA18_WRITING, AULA18_VIDEO,
         AULA19_ADVICE, AULA19_DIGITAL, AULA19_LISTENING, AULA19_SPEAKING, AULA19_READING, AULA19_WRITING, AULA19_VIDEO,
         AULA20_ACHES, AULA20_DOCTOR, AULA20_LISTENING, AULA20_SPEAKING, AULA20_READING, AULA20_WRITING, AULA20_VIDEO,
         AULA21_MUST, AULA21_MUSTNT, AULA21_LISTENING, AULA21_SPEAKING, AULA21_READING, AULA21_WRITING, AULA21_VIDEO,
         AULA22_LANGUAGE, AULA22_ETIQUETTE, AULA22_LISTENING, AULA22_SPEAKING, AULA22_READING, AULA22_WRITING, AULA22_VIDEO,
         AULA23_FORMS, AULA23_CONTRAST, AULA23_LISTENING, AULA23_SPEAKING, AULA23_READING, AULA23_WRITING, AULA23_VIDEO,
         AULA24_VOCAB, AULA24_WOULD, AULA24_LISTENING, AULA24_SPEAKING, AULA24_READING, AULA24_WRITING, AULA24_VIDEO,
         AULA25_WOULD, AULA25_WANT, AULA25_LISTENING, AULA25_SPEAKING, AULA25_READING, AULA25_WRITING, AULA25_VIDEO)


def main():
    publish(SLUG, "A2", SPECS)


if __name__ == "__main__":
    main()
