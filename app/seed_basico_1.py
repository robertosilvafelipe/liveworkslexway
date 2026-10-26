"""Exercises for the public page of the course "Básico 1" (/curso/basico-1); "lesson" = lesson number in app/curriculum.py.

Usage: python -m app.seed_basico_1
Safe to run again: exercises are matched by title and updated in place.
Listening/speaking audios live in app/static/audio/basico-1/ (made with deploy/make_audio.py on a Mac).

House style for every lesson: commands in English with the Portuguese translation below ("translation"),
an example to follow ("example"), and a mix of written, matching, drag-and-drop, listening, dictation,
speaking (record your voice) and reading-comprehension activities.
Six activities per lesson, one per day ("Dia 1–6" on the page, in id order); the last one is always Writing.
Some lessons also have an extra interactive video (subject "Video", shown as "🎬 Extra"; made with deploy/make_video.py).
"""
import json
import os

from .public_seed import publish

SLUG = "basico-1"
AUDIO = f"/static/audio/{SLUG}"
VIDEO = f"/static/video/{SLUG}"


def video_item(name, prompt, translation, questions):
    """Interactive video item: question k pauses the video where scene k (with "stop") ends, per <name>.json."""
    meta = json.load(open(os.path.join(os.path.dirname(__file__), "static", "video", SLUG, name + ".json")))
    assert len(meta["stops"]) == len(questions), name
    return {"type": "video", "prompt": prompt, "translation": translation,
            "video": f"{VIDEO}/{name}.mp4", "subtitles": f"{VIDEO}/{name}.vtt", "poster": f"{VIDEO}/{name}.jpg",
            "stops": [dict(q, at=at) for q, at in zip(questions, meta["stops"])]}

# ---------- Aula 01 — Alphabet (https://youtu.be/ZZJUIJe4Wp8) ----------

AULA1_SOUNDS = {
    "title": "Letters & sounds",
    "lesson": 1,
    "description": "Revise o alfabeto da aula: as vogais (vowels), as letras que mais confundem e as dicas para lembrar de cada uma.",
    "topic": "Aula 01 — Alphabet",
    "items": [
        {"type": "group",
         "prompt": "Group the letters by sound. Each letter rhymes with the vowel of its group.",
         "translation": "Agrupe as letras pelo som. Cada letra rima com a vogal do seu grupo.",
         "example": "B rhymes with E (bi – i) → coloque B no grupo \"rhymes with E\".",
         "categories": ["rhymes with A", "rhymes with E", "rhymes with I", "rhymes with U"],
         "words": [
             {"text": "H", "category": "rhymes with A"}, {"text": "J", "category": "rhymes with A"},
             {"text": "K", "category": "rhymes with A"},
             {"text": "B", "category": "rhymes with E"}, {"text": "D", "category": "rhymes with E"},
             {"text": "G", "category": "rhymes with E"}, {"text": "P", "category": "rhymes with E"},
             {"text": "T", "category": "rhymes with E"},
             {"text": "Y", "category": "rhymes with I"},
             {"text": "Q", "category": "rhymes with U"}, {"text": "W", "category": "rhymes with U"},
         ]},
        {"type": "match",
         "prompt": "Match each letter to the tip from the lesson.",
         "translation": "Ligue cada letra à dica da aula que ajuda a lembrar o som dela.",
         "example": "K → OK (o K tem o mesmo som do \"K\" de OK).",
         "pairs": [
             {"left": "J", "right": "DJ"},
             {"left": "K", "right": "OK"},
             {"left": "X", "right": "X-Men"},
             {"left": "Y", "right": "why?"},
             {"left": "W", "right": "double U"},
             {"left": "I", "right": "I (o pronome \"eu\")"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Think about the sounds from the lesson.",
         "translation": "Verdadeiro (True) ou falso (False)? Pense nos sons da aula.",
         "example": "\"The letter I sounds like the pronoun I.\" → True",
         "statements": [
             {"text": "The letters T, C, V, D and B end in the same sound.", "answer": True, "translation": "As letras T, C, V, D e B terminam com o mesmo som."},
             {"text": "The letter H and the number 8 (eight) have exactly the same sound.", "answer": False, "translation": "A letra H e o número 8 (eight) têm exatamente o mesmo som."},
             {"text": "\"Alphabet\" is written with PH, but PH has the sound of F.", "answer": True, "translation": "\"Alphabet\" é escrito com PH, mas o PH tem som de F."},
             {"text": "The letter A in English sounds like the Portuguese \"a\".", "answer": False, "translation": "A letra A em inglês soa como o \"a\" do português."},
             {"text": "W is called \"double U\".", "answer": True, "translation": "O W se chama \"double U\" (U duplo)."},
         ]},
    ],
}

AULA1_SPELLING = {
    "title": "How do you spell…?",
    "lesson": 1,
    "description": "Pratique as perguntas da aula: What's your name? / How do you spell your name? / What's your last name?\n"
                   "Lembre: letras repetidas → double (book = B, double O, K).",
    "topic": "Aula 01 — Alphabet",
    "items": [
        {"type": "fill",
         "prompt": "Look at the pictures. What are they? Write the words.",
         "translation": "Olhe as figuras. O que são? Escreva o nome de cada uma em inglês.",
         "image": "https://64-181-168-113.sslip.io/static/img/basico-1/aula1-objects.jpg?v=ddf96a7e",
         "text": "1. [bus]\n2. [car]\n3. [pen]\n4. [book]\n5. [notebook]"},
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta.",
         "text": "1. [*How|What|Who] do you spell your name?\n"
                 "2. What's your [*last name|last spell|name last]?\n"
                 "3. In the word \"book\", we say B, [*double O|two O|O], K.\n"
                 "4. In the name \"Vanessa\", we say V, A, N, E, [*double S|two S], A."},
        {"type": "order",
         "prompt": "Put the words in the correct order to make a question.",
         "translation": "Coloque as palavras na ordem certa para formar uma pergunta. Clique ou arraste os blocos.",
         "tokens": ["What's", "your", "name?"], "alternatives": []},
        {"type": "order",
         "prompt": "Put the words in the correct order to make a question.",
         "translation": "Coloque as palavras na ordem certa para formar uma pergunta. Clique ou arraste os blocos.",
         "tokens": ["How", "do", "you", "spell", "your", "last", "name?"], "alternatives": []},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas.",
         "example": "What's your name? → My name is Sarah.",
         "pairs": [
             {"left": "What's your name?", "right": "My name is Vanessa."},
             {"left": "How do you spell your name?", "right": "V, A, N, E, double S, A."},
             {"left": "What's your last name?", "right": "Vieira."},
             {"left": "How do you spell your last name?", "right": "V, I, E, I, R, A."},
             {"left": "Do you know this word in English?", "right": "Yes! It's \"bus\"."},
         ]},
        {"type": "free",
         "prompt": "Now it's your turn! Answer the questions about YOU:\nWhat's your name? How do you spell it?\n"
                   "What's your last name? How do you spell it?",
         "translation": "Agora é a sua vez! Responda sobre VOCÊ: seu nome e como se soletra, seu sobrenome e como se soletra.",
         "example": "My name is Vanessa. V, A, N, E, double S, A.\nMy last name is Vieira. V, I, E, I, R, A.",
         "model_answer": "My name is Vanessa. V, A, N, E, double S, A.\nMy last name is Vieira. V, I, E, I, R, A.",
         "keywords": ["my name is"], "points": 2},
    ],
}

AULA1_LISTENING = {
    "title": "Listening — letters & spelling",
    "lesson": 1,
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧",
    "topic": "Aula 01 — Alphabet",
    "subject": "Listening",
    "items": [
        {"type": "fill",
         "prompt": "Listen and write the letters you hear.",
         "translation": "Ouça e escreva as letras que você escutar. (Ditado)",
         "example": "Você ouve: \"Number one… B.\" → escreva: B",
         "audio": f"{AUDIO}/aula1-letters.m4a",
         "text": "1. [G]   2. [Y]   3. [V]   4. [M]   5. [E]\n6. [J]   7. [W|double u|double-u]   8. [L]   9. [F]   10. [X]"},
        {"type": "fill",
         "prompt": "Listen to the spelling and write the words.",
         "translation": "Ouça as palavras sendo soletradas e escreva cada palavra.",
         "example": "Você ouve: \"C, A, T\" → escreva: cat",
         "audio": f"{AUDIO}/aula1-words.m4a",
         "text": "1. [bus]\n2. [car]\n3. [pen]\n4. [book]\n5. [desk]\n6. [notebook]"},
        {"type": "fill",
         "prompt": "Listen to the conversation and complete the names.",
         "translation": "Ouça a conversa e complete os nomes e sobrenomes.",
         "example": "Você ouve: \"My name is Ana. A, N, A.\" → First name: Ana",
         "audio": f"{AUDIO}/aula1-names.m4a",
         "text": "Person 1 — First name: [Daniel]   Last name: [Mitchell]\n"
                 "Person 2 — First name: [Kelly]   Last name: [Gibbs]"},
    ],
}

AULA1_SPEAKING = {
    "title": "Speaking — say the letters",
    "lesson": 1,
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando o som e depois ouça a sua gravação para comparar.\n"
                   "Na primeira vez, o navegador vai pedir permissão para usar o microfone: clique em \"Permitir\".",
    "topic": "Aula 01 — Alphabet",
    "subject": "Speaking",
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the vowels. Record your voice.",
         "translation": "Ouça e repita as vogais. Grave a sua voz.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": v, "audio": f"{AUDIO}/aula1-say-{v.lower()}.m4a"} for v in "AEIOU"]},
        {"type": "speak",
         "prompt": "These letters are easy to confuse. Listen and repeat.",
         "translation": "Estas letras costumam confundir. Ouça e repita, prestando atenção ao som.",
         "example": "G = \"dji\" (como em \"bom dia\")  ·  J = \"djei\" (como em DJ)",
         "phrases": [{"text": v, "audio": f"{AUDIO}/aula1-say-{v.lower()}.m4a"} for v in "GJKQWYH"]},
        {"type": "speak",
         "prompt": "Listen and repeat the questions and answers.",
         "translation": "Ouça e repita as perguntas e respostas da aula.",
         "example": "\"How do you spell your name?\" — fale a frase inteira, com calma.",
         "phrases": [
             {"text": "What's your name?", "audio": f"{AUDIO}/aula1-say-s1.m4a"},
             {"text": "How do you spell your name?", "audio": f"{AUDIO}/aula1-say-s2.m4a"},
             {"text": "What's your last name?", "audio": f"{AUDIO}/aula1-say-s3.m4a"},
             {"text": "How do you spell bus?", "audio": f"{AUDIO}/aula1-say-s4.m4a"},
         ]},
    ],
}

AULA1_READING = {
    "title": "Reading — at the hotel",
    "lesson": 1,
    "description": "Leia (e ouça) o diálogo e responda às perguntas de acordo com o texto.",
    "topic": "Aula 01 — Alphabet",
    "subject": "Reading",
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the dialogue.",
         "translation": "Leia e ouça o diálogo. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula1-hotel.m4a",
         "text": "AT THE HOTEL\n\n"
                 "Receptionist: Good evening! Welcome to the Sunset Hotel. What's your name, please?\n"
                 "Guest: Hi! My name is Bruno Teixeira.\n"
                 "Receptionist: How do you spell your last name?\n"
                 "Guest: T, E, I, X, E, I, R, A.\n"
                 "Receptionist: Thank you, Mr. Teixeira. And what's your first name? Is it B, R, U, N, O?\n"
                 "Guest: Yes, that's right.\n"
                 "Receptionist: Perfect. Your room is number 12. Here's your key!\n"
                 "Guest: Thank you very much!"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "\"The guest is at a hotel.\" → True",
         "statements": [
             {"text": "The guest's first name is Bruno.", "answer": True, "translation": "O primeiro nome do hóspede é Bruno."},
             {"text": "His last name is Sunset.", "answer": False, "translation": "O sobrenome dele é Sunset."},
             {"text": "His last name starts with the letter T.", "answer": True, "translation": "O sobrenome dele começa com a letra T."},
             {"text": "His room is number 20.", "answer": False, "translation": "O quarto dele é o número 20."},
         ]},
        {"type": "choice",
         "prompt": "What is the first question the receptionist asks?",
         "translation": "Qual é a primeira pergunta que a recepcionista faz?",
         "options": ["What's your name, please?", "How old are you?", "Where are you from?"], "correct": 0},
        {"type": "fill",
         "prompt": "Complete the sentences according to the text.",
         "translation": "Complete as frases de acordo com o texto.",
         "example": "The guest's first name is [Bruno].",
         "text": "1. The name of the hotel is the [Sunset] Hotel.\n"
                 "2. The guest spells his last name: T, E, I, [X], E, I, R, A.\n"
                 "3. His room is number [12|twelve]."},
    ],
}

AULA1_WRITING = {
    "title": "Writing — introduce yourself",
    "lesson": 1,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Escreva as perguntas da aula e depois um pequeno texto sobre você.\n"
                   "Dica: escreva com calma e confira a pontuação (o ponto de interrogação ? no fim das perguntas).",
    "topic": "Aula 01 — Alphabet",
    "items": [
        {"type": "fill",
         "prompt": "Read the answers. Write the questions.",
         "translation": "Leia as respostas. Escreva a pergunta completa para cada uma.",
         "example": "Answer: \"Bus. B, U, S.\" → Question: How do you spell bus?",
         "text": "1. Answer: \"My name is Ana.\" → [What's your name?|What is your name?]\n"
                 "2. Answer: \"A, N, A.\" → [How do you spell your name?|How do you spell it?|How do you spell Ana?]\n"
                 "3. Answer: \"Silva.\" → [What's your last name?|What is your last name?|What's your surname?|What is your surname?]\n"
                 "4. Answer: \"S, I, L, V, A.\" → [How do you spell your last name?|How do you spell it?|"
                 "How do you spell Silva?|How do you spell your surname?]"},
        {"type": "free",
         "prompt": "Write about you (3 to 5 sentences): your name and how to spell it, your last name and how to spell it.",
         "translation": "Escreva sobre você (3 a 5 frases): seu nome e como se soletra, seu sobrenome e como se soletra.",
         "example": "My name is Vanessa. It's V, A, N, E, double S, A.\nMy last name is Vieira. It's V, I, E, I, R, A.",
         "model_answer": "Hi! My name is Vanessa. It's V, A, N, E, double S, A.\n"
                         "My last name is Vieira. It's V, I, E, I, R, A.",
         "keywords": ["name", "last name"], "min_words": 12, "points": 4},
    ],
}

# ---------- Aula 02 — Classroom Language (https://youtu.be/AHkMCc3PhtY) ----------

AULA2_TOPIC = "Aula 02 — Classroom Language"

AULA2_QUESTIONS = {
    "title": "How do I say…? What does … mean?",
    "lesson": 2,
    "description": "As três perguntas da aula para não precisar usar português na sala de aula:\n"
                   "• How do I say ___ in English? → a palavra está em PORTUGUÊS (como se diz… em inglês?)\n"
                   "• What does ___ mean? → a palavra está em INGLÊS (o que significa…?)\n"
                   "• How do you spell ___? → para pedir as letras (como se soletra…?)",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match each question to its meaning in Portuguese.",
         "translation": "Ligue cada pergunta ao seu significado em português.",
         "example": "How do you spell table? → Como se soletra \"table\"?",
         "pairs": [
             {"left": "How do I say \"livro\" in English?", "right": "Como se diz \"livro\" em inglês?"},
             {"left": "What does \"spoon\" mean?", "right": "O que significa \"spoon\"?"},
             {"left": "How do you spell \"apple\"?", "right": "Como se soletra \"apple\"?"},
         ]},
        {"type": "group",
         "prompt": "Which question do you use? Is the word in Portuguese or in English?",
         "translation": "Qual pergunta você usa? Veja se a palavra está em português ou em inglês e arraste para o grupo certo.",
         "example": "Você quer saber \"mesa\" em inglês → \"How do I say ___ in English?\" (mesa está em português)",
         "categories": ["How do I say ___ in English?", "What does ___ mean?"],
         "words": [
             {"text": "mesa", "category": "How do I say ___ in English?"},
             {"text": "copo", "category": "How do I say ___ in English?"},
             {"text": "colher", "category": "How do I say ___ in English?"},
             {"text": "caderno", "category": "How do I say ___ in English?"},
             {"text": "spoon", "category": "What does ___ mean?"},
             {"text": "book", "category": "What does ___ mean?"},
             {"text": "table", "category": "What does ___ mean?"},
             {"text": "glass", "category": "What does ___ mean?"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct word to complete the questions.",
         "translation": "Escolha a palavra correta para completar as perguntas.",
         "example": "How do I [say] \"mesa\" in English?",
         "text": "1. How do I [*say|mean|spell] \"copo\" in English?\n"
                 "2. What does \"book\" [*mean|say|spell]?\n"
                 "3. How do you [*spell|mean|say] \"table\"? — T, A, B, L, E.\n"
                 "4. [*What|How|Who] does \"spoon\" mean?\n"
                 "5. How do I say \"livro\" [*in English|in Portuguese|of English]?"},
        {"type": "order",
         "prompt": "Put the words in order to make the question.",
         "translation": "Coloque as palavras na ordem certa para formar a pergunta. Clique ou arraste os blocos.",
         "example": "you / spell / How / do / table? → How do you spell table?",
         "tokens": ["How", "do", "I", "say", "\"caneta\"", "in", "English?"], "alternatives": []},
        {"type": "order",
         "prompt": "Put the words in order to make the question.",
         "translation": "Coloque as palavras na ordem certa para formar a pergunta.",
         "example": "mean? / What / \"book\" / does → What does \"book\" mean?",
         "tokens": ["What", "does", "\"notebook\"", "mean?"], "alternatives": []},
        {"type": "fill",
         "prompt": "Complete the mini-dialogues with the right question.",
         "translation": "Complete os minidiálogos com a palavra que falta na pergunta.",
         "example": "A: How do I [say] \"livro\" in English?  B: Book.",
         "text": "1. A: What does \"spoon\" [mean]?  B: Colher.\n"
                 "2. A: How do I [say] \"copo\" in English?  B: Glass.\n"
                 "3. A: How do you [spell] \"apple\"?  B: A, double P, L, E.\n"
                 "4. A: How do I say \"mesa\" in [English]?  B: Table."},
    ],
}

AULA2_ONLINE = {
    "title": "Online class phrases",
    "lesson": 2,
    "description": "Frases úteis para as aulas online e expressões para usar em qualquer aula.\n"
                   "Lembre: HEAR = o som está chegando (ouvir). LISTEN = escutar com atenção.",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the phrases to their meaning.",
         "translation": "Ligue as frases ao seu significado.",
         "example": "Can you hear me? → Você está me ouvindo?",
         "pairs": [
             {"left": "Can you hear me?", "right": "Você está me ouvindo?"},
             {"left": "You're breaking up.", "right": "Seu áudio está falhando."},
             {"left": "My internet connection is slow today.", "right": "Minha internet está lenta hoje."},
             {"left": "You're frozen.", "right": "Sua imagem está congelada."},
             {"left": "You're muted.", "right": "Você está no mudo."},
         ]},
        {"type": "match",
         "prompt": "Match the useful expressions to their meaning.",
         "translation": "Ligue as expressões úteis ao seu significado.",
         "example": "Thank you. → Obrigado / Obrigada.",
         "pairs": [
             {"left": "I don't know.", "right": "Eu não sei."},
             {"left": "I have a question.", "right": "Tenho uma pergunta / uma dúvida."},
             {"left": "Can you repeat, please?", "right": "Pode repetir, por favor?"},
             {"left": "Thank you.", "right": "Obrigado / Obrigada."},
             {"left": "See you next class.", "right": "Até a próxima aula."},
         ]},
        {"type": "choice",
         "prompt": "You join the online class and want to test your microphone. What do you say?",
         "translation": "Você entra na aula online e quer testar o seu microfone. O que você diz?",
         "options": ["Can you hear me?", "Can you listen me?", "You're frozen.", "See you next class."], "correct": 0},
        {"type": "dropdown",
         "prompt": "What do you say in each situation? Choose the best phrase.",
         "translation": "O que você diz em cada situação? Escolha a melhor frase.",
         "example": "A imagem da professora parou e não se mexe. → [You're frozen.]",
         "text": "1. O áudio da professora está cortando. → [*You're breaking up.|You're muted.|I don't know.]\n"
                 "2. Seu colega está falando, mas não sai som nenhum. → [*You're muted.|You're frozen.|Thank you.]\n"
                 "3. Você não entendeu e quer ouvir de novo. → [*Can you repeat, please?|I have a question.|Can you hear me?]\n"
                 "4. Você quer fazer uma pergunta. → [*I have a question.|I don't know.|You're breaking up.]\n"
                 "5. A professora perguntou algo e você não sabe a resposta. → [*I don't know.|Thank you.|You're muted.]\n"
                 "6. A aula terminou. → [*Bye! See you next class.|Can you hear me?|My internet connection is slow today.]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Thank you\" means \"obrigado / obrigada\". → True",
         "statements": [
             {"text": "To test the audio, we say \"Can you hear me?\" (not \"listen\").", "answer": True, "translation": "Para testar o áudio, dizemos \"Can you hear me?\" (e não \"listen\")."},
             {"text": "\"Listen\" means to pay attention to what someone says.", "answer": True, "translation": "\"Listen\" significa prestar atenção no que alguém diz."},
             {"text": "\"You're frozen\" means the person's audio is muted.", "answer": False, "translation": "\"You're frozen\" significa que o áudio da pessoa está no mudo."},
             {"text": "\"My internet connection is slow today\" explains a technical problem.", "answer": True, "translation": "\"My internet connection is slow today\" explica um problema técnico."},
             {"text": "In class, it's better to speak Portuguese when you don't know a word.", "answer": False, "translation": "Na aula, é melhor falar português quando você não sabe uma palavra."},
         ]},
        {"type": "fill",
         "prompt": "Complete the phrases with the missing word.",
         "translation": "Complete as frases com a palavra que falta.",
         "example": "Can you [hear] me?",
         "text": "1. You're breaking [up].\n"
                 "2. My internet [connection] is slow today.\n"
                 "3. You're [muted|mute]. Turn on your microphone!\n"
                 "4. I have a [question].\n"
                 "5. Can you [repeat], please?\n"
                 "6. I don't [know]."},
    ],
}

AULA2_LISTENING = {
    "title": "Listening — in the online class",
    "lesson": 2,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Dictation: listen and write the missing words. Each sentence is said twice.",
         "translation": "Ditado: ouça e escreva as palavras que faltam. Cada frase é dita duas vezes.",
         "example": "Você ouve: \"Can you hear me?\" → Can you [hear] me?",
         "audio": f"{AUDIO}/aula2-dictation.m4a",
         "text": "1. I have a [question].\n"
                 "2. Can you [repeat], please?\n"
                 "3. You're [frozen].\n"
                 "4. My internet connection is [slow] today.\n"
                 "5. What does \"[spoon]\" mean?\n"
                 "6. How do I [say] \"copo\" in English?"},
        {"type": "info",
         "prompt": "Now listen to the conversation in an online class.",
         "translation": "Agora ouça a conversa numa aula online. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula2-class.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the conversation.",
         "translation": "Verdadeiro ou falso? Responda de acordo com a conversa.",
         "example": "\"The student says: Sorry, I was muted.\" → True",
         "statements": [
             {"text": "At first, the teacher can't hear the student.", "answer": True, "translation": "No começo, a professora não consegue ouvir o aluno."},
             {"text": "The student's internet connection is slow today.", "answer": True, "translation": "A internet do aluno está lenta hoje."},
             {"text": "The teacher asks: \"What does table mean?\"", "answer": False, "translation": "A professora pergunta: \"O que significa table?\""},
             {"text": "The student asks how to say \"caderno\" in English.", "answer": True, "translation": "O aluno pergunta como se diz \"caderno\" em inglês."},
         ]},
        {"type": "fill",
         "prompt": "Listen again and complete.",
         "translation": "Ouça de novo e complete.",
         "example": "The teacher says: \"Good morning! Can you [hear] me?\"",
         "text": "1. \"Caderno\" in English is [notebook|a notebook].\n"
                 "2. The teacher spells it: N, O, T, E, B, double [O], K.\n"
                 "3. At the end, the teacher says: \"Bye! See you next [class].\""},
    ],
}

AULA2_SPEAKING = {
    "title": "Speaking — classroom phrases",
    "lesson": 2,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando a frase e depois ouça a sua gravação para comparar.\n"
                   "Na primeira vez, o navegador vai pedir permissão para usar o microfone: clique em \"Permitir\".",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the questions.",
         "translation": "Ouça e repita as perguntas.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [
             {"text": "How do I say \"livro\" in English?", "audio": f"{AUDIO}/aula2-say-q1.m4a"},
             {"text": "What does \"spoon\" mean?", "audio": f"{AUDIO}/aula2-say-q2.m4a"},
             {"text": "How do you spell \"table\"?", "audio": f"{AUDIO}/aula2-say-q3.m4a"},
         ]},
        {"type": "speak",
         "prompt": "Listen and repeat the online class phrases.",
         "translation": "Ouça e repita as frases para aulas online.",
         "example": "\"Can you hear me?\" — o \"hear\" soa parecido com \"rír\".",
         "phrases": [
             {"text": "Can you hear me?", "audio": f"{AUDIO}/aula2-say-o1.m4a"},
             {"text": "You're breaking up.", "audio": f"{AUDIO}/aula2-say-o2.m4a"},
             {"text": "My internet connection is slow today.", "audio": f"{AUDIO}/aula2-say-o3.m4a"},
             {"text": "You're frozen.", "audio": f"{AUDIO}/aula2-say-o4.m4a"},
             {"text": "You're muted.", "audio": f"{AUDIO}/aula2-say-o5.m4a"},
         ]},
        {"type": "speak",
         "prompt": "Listen and repeat the useful expressions.",
         "translation": "Ouça e repita as expressões úteis.",
         "example": "\"Can you repeat, please?\" — fale a frase inteira, com calma.",
         "phrases": [
             {"text": "I don't know.", "audio": f"{AUDIO}/aula2-say-e1.m4a"},
             {"text": "I have a question.", "audio": f"{AUDIO}/aula2-say-e2.m4a"},
             {"text": "Can you repeat, please?", "audio": f"{AUDIO}/aula2-say-e3.m4a"},
             {"text": "Thank you.", "audio": f"{AUDIO}/aula2-say-e4.m4a"},
             {"text": "Bye! See you next class.", "audio": f"{AUDIO}/aula2-say-e5.m4a"},
         ]},
    ],
}

AULA2_READING = {
    "title": "Reading — the class chat",
    "lesson": 2,
    "subject": "Reading",
    "description": "Leia o chat de uma aula online e responda às perguntas de acordo com o texto.",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read the chat from an online English class.",
         "translation": "Leia o chat de uma aula de inglês online. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula2-chat.m4a",
         "text": "💬 ENGLISH CLASS — CHAT\n\n"
                 "Teacher Anna: Good morning, everybody! Can you hear me?\n"
                 "Pedro: Yes, I can hear you, teacher!\n"
                 "Julia: Teacher, you're breaking up. My internet connection is slow today. 😕\n"
                 "Teacher Anna: No problem, Julia. Lucas, you're muted! Turn on your microphone, please.\n"
                 "Lucas: Sorry! I have a question. How do I say \"cadeira\" in English?\n"
                 "Teacher Anna: Chair. C, H, A, I, R.\n"
                 "Julia: What does \"desk\" mean?\n"
                 "Teacher Anna: \"Desk\" means \"carteira\" or \"mesa de escritório\".\n"
                 "Pedro: Can you repeat, please?\n"
                 "Teacher Anna: Of course! Desk: D, E, S, K.\n"
                 "Pedro: Thank you!\n"
                 "Teacher Anna: Bye, everybody! See you next class!"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "\"The teacher's name is Anna.\" → True",
         "statements": [
             {"text": "Pedro can hear the teacher.", "answer": True, "translation": "O Pedro consegue ouvir a professora."},
             {"text": "Julia's internet connection is fast today.", "answer": False, "translation": "A internet da Julia está rápida hoje."},
             {"text": "Lucas is muted at first.", "answer": True, "translation": "No começo, o Lucas está no mudo."},
             {"text": "Julia wants to know how to say \"cadeira\" in English.", "answer": False, "translation": "A Julia quer saber como se diz \"cadeira\" em inglês."},
         ]},
        {"type": "choice",
         "prompt": "Who has a problem with the internet?",
         "translation": "Quem tem um problema com a internet?",
         "options": ["Julia", "Pedro", "Lucas", "Teacher Anna"], "correct": 0},
        {"type": "choice",
         "prompt": "Why does Pedro say \"Can you repeat, please?\"",
         "translation": "Por que o Pedro diz \"Can you repeat, please?\"",
         "options": ["He wants to hear the explanation again.", "He is muted.", "He doesn't have a question.",
                     "He wants to say goodbye."], "correct": 0},
        {"type": "fill",
         "prompt": "Complete the sentences according to the text.",
         "translation": "Complete as frases de acordo com o texto.",
         "example": "The teacher's name is [Anna].",
         "text": "1. \"Cadeira\" in English is [chair].\n"
                 "2. Julia asks: \"What does [desk] mean?\"\n"
                 "3. Lucas says: \"I have a [question].\"\n"
                 "4. At the end, the teacher says: \"See you next [class]!\""},
    ],
}

AULA2_WRITING = {
    "title": "Writing — ask in English",
    "lesson": 2,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Escreva as frases da aula em inglês e depois uma mensagem curta para o professor.\n"
                   "Dica: não precisa usar aspas nas palavras, por exemplo: How do I say mesa in English?",
    "topic": AULA2_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "What do you say in English? Write the complete sentence.",
         "translation": "O que você diz em inglês? Escreva a frase completa.",
         "example": "Você quer saber como se diz \"mesa\" em inglês. → How do I say mesa in English?",
         "text": "1. Você quer saber como se diz \"cadeira\" em inglês. → "
                 "[How do I say cadeira in English?|How do I say \"cadeira\" in English?|How do I say “cadeira” in English?]\n"
                 "2. Você quer saber o que \"window\" significa. → "
                 "[What does window mean?|What does \"window\" mean?|What does “window” mean?]\n"
                 "3. Você quer saber como se soletra \"chair\". → "
                 "[How do you spell chair?|How do you spell \"chair\"?|How do you spell “chair”?]\n"
                 "4. Você não entendeu e quer ouvir de novo. → [Can you repeat, please?|Can you repeat please?|Can you repeat?]\n"
                 "5. Você quer testar se o professor está te ouvindo. → [Can you hear me?]\n"
                 "6. Você quer dizer que tem uma pergunta. → [I have a question.]"},
        {"type": "free",
         "prompt": "Write a short message to your teacher in the class chat (3 or 4 sentences): say hi, "
                   "talk about a problem in the online class and ask a question.",
         "translation": "Escreva uma mensagem curta para o professor no chat da aula (3 ou 4 frases): cumprimente, "
                        "fale de um problema na aula online e faça uma pergunta.",
         "example": "Hi, teacher! My internet connection is slow today. I have a question. What does desk mean?",
         "model_answer": "Hi, teacher! Sorry, my internet connection is slow today and you're breaking up.\n"
                         "I have a question. How do I say caneta in English?\nThank you!",
         "keywords": ["teacher", "question"], "min_words": 12, "points": 4},
    ],
}

# ---------- Aula 03 — Greetings (https://youtu.be/kN9vRp1Dq_Q) ----------

AULA3_TOPIC = "Aula 03 — Greetings"

AULA3_HELLO = {
    "title": "Hello! How are you?",
    "lesson": 3,
    "description": "Cumprimentar, perguntar o nome e responder \"How are you?\".\n"
                   "Lembre: a resposta para \"How are you?\" é curtinha, como o nosso \"tudo bem\". Depois, devolva a pergunta: \"And you?\"",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "Hello or goodbye? Put each expression in the right group.",
         "translation": "Olá ou tchau? Arraste cada expressão para o grupo certo.",
         "example": "Hi → \"Hello (olá)\"   ·   Take care → \"Goodbye (tchau)\"",
         "categories": ["Hello (olá)", "Goodbye (tchau)"],
         "words": [
             {"text": "Hello", "category": "Hello (olá)"}, {"text": "Hey", "category": "Hello (olá)"},
             {"text": "Good morning", "category": "Hello (olá)"}, {"text": "Good evening", "category": "Hello (olá)"},
             {"text": "Bye", "category": "Goodbye (tchau)"}, {"text": "See you", "category": "Goodbye (tchau)"},
             {"text": "See you next class", "category": "Goodbye (tchau)"},
             {"text": "Good night", "category": "Goodbye (tchau)"},
         ]},
        {"type": "match",
         "prompt": "Match the English expressions to their meaning.",
         "translation": "Ligue as expressões em inglês ao seu significado.",
         "example": "Take care. → Se cuida.",
         "pairs": [
             {"left": "How are you?", "right": "Como vai você? / Tudo bem?"},
             {"left": "I'm great.", "right": "Estou ótimo / ótima."},
             {"left": "All good.", "right": "Tudo certo."},
             {"left": "I'm fine, thank you.", "right": "Estou bem, obrigado / obrigada."},
             {"left": "See you!", "right": "Te vejo! / Até mais!"},
             {"left": "Take care.", "right": "Se cuida."},
         ]},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas.",
         "example": "Hi! → Hello!",
         "pairs": [
             {"left": "What's your name?", "right": "I'm Vanessa."},
             {"left": "How are you?", "right": "I'm fine, thank you. And you?"},
             {"left": "How are you doing?", "right": "All good!"},
             {"left": "Bye! See you next class.", "right": "Bye! Take care."},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct option to complete the dialogue.",
         "translation": "Escolha a opção correta para completar o diálogo.",
         "example": "A: Hi! [What's] your name?  B: I'm Ana.",
         "text": "A: Hello! What's your [*name|names|is]?\n"
                 "B: [*My name's|My name|Name is] Carla. And you?\n"
                 "A: [*I'm|I|I is] Paulo. How [*are|is|do] you, Carla?\n"
                 "B: I'm fine, thank you. [*And you?|You and?|How you?]\n"
                 "A: I'm [*great|bye|morning], thanks!"},
        {"type": "order",
         "prompt": "Put the words in order to make the question.",
         "translation": "Coloque as palavras na ordem certa para formar a pergunta. Clique ou arraste os blocos.",
         "example": "you? / How / are → How are you?",
         "tokens": ["How", "are", "you", "doing?"], "alternatives": []},
        {"type": "order",
         "prompt": "Put the words in order to make the answer.",
         "translation": "Coloque as palavras na ordem certa para formar a resposta.",
         "example": "name / My / Ana. / is → My name is Ana.",
         "tokens": ["I'm", "fine,", "thank", "you."], "alternatives": []},
        {"type": "free",
         "prompt": "Your turn! Write a short dialogue: say hello, ask the name, ask \"How are you?\", answer and say goodbye.",
         "translation": "Sua vez! Escreva um diálogo curto: cumprimente, pergunte o nome, pergunte \"How are you?\", responda e se despeça.",
         "example": "A: Hi! What's your name?\nB: I'm Lucas. And you?\nA: My name is Bia. How are you?\nB: I'm great, thanks! And you?\nA: All good. Bye! Take care!",
         "model_answer": "A: Hi! What's your name?\nB: I'm Lucas. And you?\nA: My name is Bia. How are you?\nB: I'm great, thanks! And you?\nA: All good. Bye! Take care!",
         "keywords": ["name", "how are you"], "points": 2},
    ],
}

AULA3_TIMES = {
    "title": "Good morning, good evening or good night?",
    "lesson": 3,
    "description": "Morning = manhã · Afternoon = tarde · Evening/Night = noite.\n"
                   "Atenção: GOOD EVENING é para CHEGAR (= hello). GOOD NIGHT é para SAIR ou ir dormir (= goodbye).",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the words to their meaning.",
         "translation": "Ligue as palavras ao seu significado.",
         "example": "morning → manhã",
         "pairs": [
             {"left": "morning", "right": "manhã"},
             {"left": "afternoon", "right": "tarde"},
             {"left": "night", "right": "noite"},
             {"left": "Good afternoon!", "right": "Boa tarde!"},
         ]},
        {"type": "dropdown",
         "prompt": "What do you say? Look at the time and the situation.",
         "translation": "O que você diz? Observe o horário e a situação.",
         "example": "9:00 — você chega no trabalho. → [Good morning!]",
         "text": "1. 8:00 — você chega na escola. → [*Good morning!|Good afternoon!|Good night!]\n"
                 "2. 3:00 p.m. (15h) — você entra numa reunião. → [*Good afternoon!|Good morning!|Good night!]\n"
                 "3. 7:30 p.m. (19h30) — você entra na aula de inglês da noite. → [*Good evening!|Good night!|Good morning!]\n"
                 "4. 9:30 p.m. (21h30) — a aula terminou e você vai embora. → [*Good night!|Good evening!|Good afternoon!]\n"
                 "5. 11:00 p.m. (23h) — você vai dormir. → [*Good night!|Good evening!|Hello!]"},
        {"type": "truefalse",
         "prompt": "True or false?",
         "translation": "Verdadeiro ou falso?",
         "example": "\"Good morning\" means \"bom dia\". → True",
         "statements": [
             {"text": "We say \"Good evening\" when we arrive somewhere at night.", "answer": True, "translation": "Dizemos \"Good evening\" quando chegamos em algum lugar à noite."},
             {"text": "We say \"Good night\" to say hello at night.", "answer": False, "translation": "Dizemos \"Good night\" para dizer olá à noite."},
             {"text": "\"Good night\" is related to goodbye.", "answer": True, "translation": "\"Good night\" está ligado a dizer tchau."},
             {"text": "\"Bye bye\" sounds a bit more childish or affectionate (carinhoso).", "answer": True, "translation": "\"Bye bye\" soa um pouco mais infantil ou carinhoso."},
             {"text": "When someone asks \"How are you?\", you usually give a long answer with many details.", "answer": False, "translation": "Quando alguém pergunta \"How are you?\", normalmente você dá uma resposta longa, cheia de detalhes."},
         ]},
        {"type": "choice",
         "prompt": "It's 8 p.m. You start your online English class. What do you say to your teacher?",
         "translation": "São 20h. Sua aula online de inglês está começando. O que você diz para o seu professor?",
         "options": ["Good evening, teacher!", "Good night, teacher!", "Good morning, teacher!", "Take care, teacher!"],
         "correct": 0},
        {"type": "fill",
         "prompt": "Complete with morning, afternoon, evening or night.",
         "translation": "Complete com morning, afternoon, evening ou night.",
         "example": "Bom dia! → Good [morning]!",
         "text": "1. Boa tarde! → Good [afternoon]!\n"
                 "2. Boa noite! (chegando numa festa) → Good [evening]!\n"
                 "3. Boa noite! (indo dormir) → Good [night]!\n"
                 "4. Bom dia! → Good [morning]!"},
    ],
}

AULA3_LISTENING = {
    "title": "Listening — greetings",
    "lesson": 3,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Lembre da aula: na fala real os sons se juntam (What is → What's) e o \"your\" fica bem fraquinho.",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Dictation: listen and complete. Each sentence is said twice: slowly, then at natural speed.",
         "translation": "Ditado: ouça e complete. Cada frase é dita duas vezes: devagar e depois na velocidade natural.",
         "example": "Você ouve: \"Good morning!\" → Good [morning]!",
         "audio": f"{AUDIO}/aula3-dictation.m4a",
         "text": "1. What's your [name]?\n"
                 "2. My [name's|name is] Vanessa.\n"
                 "3. How are you [doing]?\n"
                 "4. I'm [fine], thank you.\n"
                 "5. Good [afternoon]!\n"
                 "6. Take [care]!"},
        {"type": "fill",
         "prompt": "Listen to four short situations. Write the greeting you hear.",
         "translation": "Ouça quatro situações curtas. Escreva o cumprimento que você ouvir.",
         "example": "Você ouve: \"Good morning, everybody!\" → Good [morning]",
         "audio": f"{AUDIO}/aula3-situations.m4a",
         "text": "1. Good [evening]\n2. Good [night]\n3. Good [afternoon]\n4. Good [morning]"},
        {"type": "info",
         "prompt": "Now listen to the conversation on the first day of class.",
         "translation": "Agora ouça a conversa no primeiro dia de aula. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula3-dialogue.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the conversation.",
         "translation": "Verdadeiro ou falso? Responda de acordo com a conversa.",
         "example": "\"The two people are at school.\" → True",
         "statements": [
             {"text": "The woman's name is Sarah.", "answer": True, "translation": "O nome da mulher é Sarah."},
             {"text": "The man's name is Michael.", "answer": False, "translation": "O nome do homem é Michael."},
             {"text": "Sarah says she is great.", "answer": True, "translation": "A Sarah diz que está ótima."},
             {"text": "The conversation happens in the morning.", "answer": False, "translation": "A conversa acontece de manhã."},
         ]},
        {"type": "choice",
         "prompt": "How does the man say goodbye?",
         "translation": "Como o homem se despede?",
         "options": ["Bye! Take care!", "Good night!", "Bye bye!", "See you next class!"], "correct": 0},
    ],
}

AULA3_SPEAKING = {
    "title": "Speaking — greetings",
    "lesson": 3,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando a frase e depois ouça a sua gravação para comparar.\n"
                   "Tente falar de forma natural, juntando os sons, como na aula.",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the greetings.",
         "translation": "Ouça e repita os cumprimentos.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula3-say-g{i}.m4a"} for i, t in enumerate(
             ["Hello!", "Hi!", "Hey!", "Good morning!", "Good afternoon!", "Good evening!"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the questions and answers. Join the sounds, like in the lesson.",
         "translation": "Ouça e repita as perguntas e respostas. Junte os sons, como na aula.",
         "example": "What is your name? → \"What's your name?\" (o \"your\" fica bem fraquinho; o mais forte é NAME)",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula3-say-q{i}.m4a"} for i, t in enumerate(
             ["What's your name?", "My name's Vanessa.", "I'm Vanessa.", "How are you?", "How are you doing?",
              "I'm fine, thank you. And you?", "All good!"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the goodbyes.",
         "translation": "Ouça e repita as despedidas.",
         "example": "\"Take care!\" = Se cuida!",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula3-say-b{i}.m4a"} for i, t in enumerate(
             ["Goodbye!", "Bye bye!", "See you!", "See you next class!", "Take care!", "Good night!"], 1)]},
    ],
}

AULA3_READING = {
    "title": "Reading — first day of class",
    "lesson": 3,
    "subject": "Reading",
    "description": "Leia (e ouça) o diálogo e responda às perguntas de acordo com o texto.",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the dialogue.",
         "translation": "Leia e ouça o diálogo. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula3-reading.m4a",
         "text": "FIRST DAY OF CLASS — 7 p.m.\n\n"
                 "Teacher: Good evening, everybody! Welcome to the English class!\n"
                 "Students: Good evening, teacher!\n"
                 "Teacher: My name's Laura. What's your name?\n"
                 "Rafael: Hi, Laura! I'm Rafael.\n"
                 "Teacher: Nice to meet you, Rafael. How are you doing?\n"
                 "Rafael: I'm great, thanks! And you?\n"
                 "Teacher: I'm fine, thank you.\n"
                 "Bia: Hey! My name is Beatriz, but you can call me Bia.\n"
                 "Teacher: Hello, Bia! How are you?\n"
                 "Bia: All good!\n\n"
                 "— 9 p.m. —\n\n"
                 "Teacher: OK, everybody. Good night! See you next class!\n"
                 "Rafael: Bye, teacher! Take care!\n"
                 "Bia: Good night!"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "\"The class starts at 7 p.m.\" → True",
         "statements": [
             {"text": "The teacher's name is Laura.", "answer": True, "translation": "O nome da professora é Laura."},
             {"text": "Rafael is fine, but not great.", "answer": False, "translation": "O Rafael está bem, mas não ótimo."},
             {"text": "Bia's full name is Beatriz.", "answer": True, "translation": "O nome completo da Bia é Beatriz."},
             {"text": "The class finishes at 10 p.m.", "answer": False, "translation": "A aula termina às 22h (10 p.m.)."},
         ]},
        {"type": "choice",
         "prompt": "Why does the teacher say \"Good evening\" at the beginning and \"Good night\" at the end?",
         "translation": "Por que a professora diz \"Good evening\" no começo e \"Good night\" no final?",
         "options": ["\"Good evening\" is for arriving and \"Good night\" is for leaving.",
                     "\"Good evening\" is for the morning.",
                     "They mean \"bom dia\" and \"boa tarde\".",
                     "There is no difference."], "correct": 0},
        {"type": "fill",
         "prompt": "Complete the sentences according to the text.",
         "translation": "Complete as frases de acordo com o texto.",
         "example": "The teacher says: \"Welcome to the [English] class!\"",
         "text": "1. Rafael answers: \"I'm [great], thanks! And you?\"\n"
                 "2. Bia answers: \"All [good]!\"\n"
                 "3. Rafael says goodbye: \"Bye, teacher! Take [care]!\""},
    ],
}

AULA3_WRITING = {
    "title": "Writing — greetings in my day",
    "lesson": 3,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Corrija as frases com erro e depois escreva um pequeno texto sobre os cumprimentos do seu dia.",
    "topic": AULA3_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Each sentence has ONE mistake. Rewrite the sentence correctly.",
         "translation": "Cada frase tem UM erro. Reescreva a frase do jeito certo.",
         "example": "\"How you are?\" → How are you?",
         "text": "1. \"What your name?\" → [What's your name?|What is your name?]\n"
                 "2. \"I fine, thank you.\" → [I'm fine, thank you.|I am fine, thank you.|I'm fine thank you.|I am fine thank you.]\n"
                 "3. \"My name Carla.\" → [My name is Carla.|My name's Carla.]\n"
                 "4. Você chega numa festa às 21h: \"Good night! Welcome to the party!\" → "
                 "[Good evening! Welcome to the party!|Good evening. Welcome to the party!|Good evening, welcome to the party!]\n"
                 "5. \"See you next classes!\" → [See you next class!]"},
        {"type": "free",
         "prompt": "Write a short text (4 to 6 sentences): what do you say to people during your day? "
                   "Use good morning, good afternoon, good evening and good night.",
         "translation": "Escreva um texto curto (4 a 6 frases): o que você diz para as pessoas durante o seu dia? "
                        "Use good morning, good afternoon, good evening e good night.",
         "example": "In the morning, I say \"Good morning!\" to my family.",
         "model_answer": "In the morning, I say \"Good morning!\" to my family.\n"
                         "In the afternoon, I say \"Good afternoon!\" to my friends at work.\n"
                         "In the evening, I arrive at my English class and I say \"Good evening, teacher!\"\n"
                         "At the end of the class, I say \"Bye! See you next class!\"\n"
                         "At 11 p.m., I say \"Good night!\" and I go to bed.",
         "keywords": ["good morning", "good afternoon", "good evening", "good night"], "min_words": 20, "points": 4},
    ],
}

# ---------- Aula 04 — Daily Routine (https://youtu.be/cox3ODLCkx4) ----------

AULA4_TOPIC = "Aula 04 — Daily Routine"

AULA4_VERBS = {
    "title": "Daily routine verbs",
    "lesson": 4,
    "description": "Os verbos da rotina diária da aula: wake up, have breakfast, brush my teeth, take a shower, get dressed, "
                   "have coffee, start work, have lunch, study English, go to the gym, finish work, read a book, watch TV, go to bed.\n"
                   "Lembre: lunch = almoço (lanche = snack). Have também é usado com refeições: have breakfast, have lunch, have dinner.",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the routine verbs to the pictures.",
         "translation": "Ligue os verbos da rotina às figuras.",
         "example": "wake up → a figura de alguém acordando",
         # pictures from Pixabay (free for commercial use); "right" stays as the hidden answer key and the image alt text
         "pairs": [
             {"left": "have breakfast", "right": "tomar café da manhã", "image": f"/static/img/{SLUG}/aula4-have-breakfast.png"},
             {"left": "brush my teeth", "right": "escovar os dentes", "image": f"/static/img/{SLUG}/aula4-brush-teeth.png"},
             {"left": "take a shower", "right": "tomar banho", "image": f"/static/img/{SLUG}/aula4-take-shower.png"},
             {"left": "get dressed", "right": "se vestir / se arrumar", "image": f"/static/img/{SLUG}/aula4-get-dressed.png"},
             {"left": "start work", "right": "começar a trabalhar", "image": f"/static/img/{SLUG}/aula4-start-work.png"},
             {"left": "have lunch", "right": "almoçar", "image": f"/static/img/{SLUG}/aula4-have-lunch.jpg"},
             {"left": "go to the gym", "right": "ir para a academia", "image": f"/static/img/{SLUG}/aula4-go-gym.png"},
             {"left": "go to bed", "right": "ir para a cama / ir dormir", "image": f"/static/img/{SLUG}/aula4-go-bed.png"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct verb.",
         "translation": "Escolha o verbo correto.",
         "example": "I [take] a shower.",
         "text": "1. I [*wake|get|go] up at 6 a.m.\n"
                 "2. I [*brush|take|have] my teeth.\n"
                 "3. I [*get|take|have] dressed.\n"
                 "4. I [*have|take|go] lunch at 12:30.\n"
                 "5. I [*go|have|watch] to the gym.\n"
                 "6. I [*watch|read|go] TV.\n"
                 "7. I [*read|watch|study] a book.\n"
                 "8. I [*finish|go|wake] work at 6 p.m."},
        {"type": "group",
         "prompt": "Which verb goes with each word? Put the words in the right group.",
         "translation": "Qual verbo combina com cada palavra? Arraste as palavras para o grupo certo.",
         "example": "breakfast → \"have ___\" (have breakfast)",
         "categories": ["have ___", "go to ___", "start / finish ___"],
         "words": [
             {"text": "breakfast", "category": "have ___"}, {"text": "lunch", "category": "have ___"},
             {"text": "coffee", "category": "have ___"}, {"text": "dinner", "category": "have ___"},
             {"text": "the gym", "category": "go to ___"}, {"text": "bed", "category": "go to ___"},
             {"text": "work", "category": "start / finish ___"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Have lunch\" means \"almoçar\". → True",
         "statements": [
             {"text": "\"Lunch\" means \"lanche\".", "answer": False, "translation": "\"Lunch\" significa \"lanche\"."},
             {"text": "In \"get dressed\", the letters ED sound like /t/.", "answer": True, "translation": "Em \"get dressed\", as letras ED têm som de /t/."},
             {"text": "In English we say \"brush MY teeth\" (escovar MEUS dentes).", "answer": True, "translation": "Em inglês dizemos \"brush MY teeth\" (escovar MEUS dentes)."},
             {"text": "\"Go to bed\" is used to say the time you go to bed in your routine.", "answer": True, "translation": "\"Go to bed\" é usado para dizer a hora em que você vai dormir na sua rotina."},
             {"text": "In English, the letter H is always silent, like in Portuguese.", "answer": False, "translation": "Em inglês, a letra H é sempre muda, como em português."},
         ]},
        {"type": "order",
         "prompt": "Put the words in order to make a sentence about your routine.",
         "translation": "Coloque as palavras na ordem certa para formar uma frase sobre a rotina.",
         "example": "a / I / shower / take → I take a shower.",
         "tokens": ["I", "have", "breakfast", "at", "7", "a.m."], "alternatives": []},
    ],
}

AULA4_SEQUENCE = {
    "title": "First, then, after that, finally",
    "lesson": 4,
    "description": "Palavras para contar a rotina em ordem:\n"
                   "FIRST (primeiro) → THEN / NEXT / AFTER THAT (depois, em seguida) → FINALLY (finalmente).\n"
                   "Atenção: use AFTER THAT, e não \"after\" sozinho. E não esqueça o pronome: I take a shower.",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the sequence words to their meaning.",
         "translation": "Ligue as palavras de sequência ao seu significado.",
         "example": "first → primeiro",
         "pairs": [
             {"left": "first", "right": "primeiro"},
             {"left": "then", "right": "então / depois"},
             {"left": "after that", "right": "depois disso"},
             {"left": "finally", "right": "finalmente / por último"},
         ]},
        {"type": "dropdown",
         "prompt": "Complete the paragraph with the sequence words.",
         "translation": "Complete o parágrafo com as palavras de sequência.",
         "example": "[First], I wake up at 6 a.m.",
         "text": "My morning: [*First|Finally|After that], I take a shower. [*Then|First|Finally] I have breakfast. "
                 "[*After that|After|First], I brush my teeth. Next, I read a book. "
                 "And [*finally|first|after], I start work at 9 a.m."},
        {"type": "choice",
         "prompt": "Which sentence is correct?",
         "translation": "Qual frase está correta?",
         "options": ["After that, I get dressed.", "After, I get dressed.", "After that, get dressed I.", "After that, dressed I get."],
         "correct": 0},
        {"type": "choice",
         "prompt": "Why do we always use \"I\" in the sentences (I take a shower, I have breakfast…)?",
         "translation": "Por que usamos sempre o \"I\" nas frases (I take a shower, I have breakfast…)?",
         "options": ["Because the verb doesn't show who is doing the action, so we need the pronoun.",
                     "Because \"I\" means \"then\".",
                     "We don't need it. \"Take a shower\" is a complete sentence about me."],
         "correct": 0},
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras na ordem certa.",
         "example": "I / Then / breakfast / have → Then I have breakfast.",
         "tokens": ["After", "that,", "I", "brush", "my", "teeth."], "alternatives": []},
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras na ordem certa.",
         "example": "up / First, / wake / I → First, I wake up.",
         "tokens": ["Finally,", "I", "go", "to", "bed", "at", "11", "p.m."], "alternatives": []},
    ],
}

AULA4_LISTENING = {
    "title": "Listening — routines and H or R?",
    "lesson": 4,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Lembre: o H do inglês normalmente TEM som (have, house). O R do inglês não é igual ao do português (read, red).",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "H or R? Listen and choose the word you hear.",
         "translation": "H ou R? Ouça e escolha a palavra que você escutar.",
         "example": "Você ouve: \"hat\" (chapéu) → escolha hat, e não rat (rato).",
         "audio": f"{AUDIO}/aula4-hr.m4a",
         "text": "1. [*rat|hat]   2. [*hope|rope]   3. [*red|head]   4. [*hat|rat]   5. [*ride|hide]   6. [*have|read]"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete the routine sentences. Each sentence is said twice.",
         "translation": "Ditado: ouça e complete as frases da rotina. Cada frase é dita duas vezes.",
         "example": "Você ouve: \"I wake up at six.\" → I [wake] up at six.",
         "audio": f"{AUDIO}/aula4-dictation.m4a",
         "text": "1. I take a [shower].\n"
                 "2. I brush my [teeth].\n"
                 "3. I get [dressed].\n"
                 "4. I have [lunch] at one o'clock.\n"
                 "5. I go to the [gym].\n"
                 "6. I go to [bed] at eleven."},
        {"type": "info",
         "prompt": "Now listen to Kevin. He describes his morning.",
         "translation": "Agora ouça o Kevin. Ele descreve a manhã dele. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula4-kevin.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "fill",
         "prompt": "Listen to Kevin again and complete.",
         "translation": "Ouça o Kevin de novo e complete.",
         "example": "Kevin: \"I wake up at [six thirty].\"",
         "text": "1. Kevin: \"First, I take a [shower].\"\n"
                 "2. Kevin: \"Then I have [coffee].\"\n"
                 "3. Kevin: \"After that, I go to the [gym].\"\n"
                 "4. Kevin: \"Finally, I start work at [9|nine|9 a.m.|nine a.m.].\""},
        {"type": "truefalse",
         "prompt": "Does Kevin say this? True or false?",
         "translation": "O Kevin diz isto? Verdadeiro ou falso? Responda de acordo com o áudio.",
         "example": "Kevin: \"I wake up at six thirty.\" → True",
         "statements": [
             {"text": "Kevin: \"I have breakfast at home.\"", "answer": False, "translation": "Kevin: \"Eu tomo café da manhã em casa.\""},
             {"text": "Kevin: \"I go to the gym in the morning.\"", "answer": True, "translation": "Kevin: \"Eu vou para a academia de manhã.\""},
             {"text": "Kevin: \"I read a book before work.\"", "answer": False, "translation": "Kevin: \"Eu leio um livro antes do trabalho.\""},
         ]},
    ],
}

AULA4_SPEAKING = {
    "title": "Speaking — my routine",
    "lesson": 4,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando a frase e depois ouça a sua gravação para comparar.\n"
                   "Na aula: TEETH (ponta da língua entre os dentes + um soprinho), GET DRESSED (o ED soa como /t/), WAKE UP (tudo junto).",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the routine verbs.",
         "translation": "Ouça e repita os verbos da rotina.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula4-say-v{i}.m4a"} for i, t in enumerate(
             ["wake up", "have breakfast", "brush my teeth", "take a shower", "get dressed", "start work",
              "have lunch", "go to the gym", "watch TV", "go to bed"], 1)]},
        {"type": "speak",
         "prompt": "H or R? Listen and repeat. The H has a sound in English!",
         "translation": "H ou R? Ouça e repita. O H tem som em inglês! (exceção: honest, em que o H é mudo)",
         "example": "hat (chapéu) ≠ rat (rato) — trocar o som pode mudar a palavra!",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula4-say-h{i}.m4a"} for i, t in enumerate(
             ["have", "house", "hospital", "helicopter", "hat", "read", "red", "rat"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences about a morning routine.",
         "translation": "Ouça e repita as frases sobre a rotina da manhã.",
         "example": "\"First, I take a shower.\" — fale a frase inteira, com calma.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula4-say-s{i}.m4a"} for i, t in enumerate(
             ["What do you do in the morning?", "First, I take a shower.", "Then I have breakfast.",
              "After that, I brush my teeth.", "Finally, I start work at 9 a.m."], 1)]},
    ],
}

AULA4_READING = {
    "title": "Reading — Carol's day",
    "lesson": 4,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Carol's text about her day.",
         "translation": "Leia e ouça o texto da Carol sobre o dia dela. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula4-carol.m4a",
         "text": "MY DAY — by Carol\n\n"
                 "Hi! I'm Carol and I'm a nurse. My day is very busy!\n"
                 "First, I wake up at 5:30 a.m. Then I take a shower and I get dressed. "
                 "After that, I have breakfast with my family: bread and coffee. Next, I brush my teeth "
                 "and I go to the hospital. I start work at 7 a.m.\n"
                 "I have lunch at 12:00 at the hospital. I finish work at 3 p.m. "
                 "Then I go to the gym. In the evening, I study English and I read a book.\n"
                 "I don't watch TV. Finally, I go to bed at 10 p.m."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Carol: \"I'm a nurse.\" → True",
         "statements": [
             {"text": "Carol: \"I wake up at 5:30 a.m.\"", "answer": True, "translation": "Carol: \"Eu acordo às 5h30.\""},
             {"text": "Carol: \"I have breakfast alone.\"", "answer": False, "translation": "Carol: \"Eu tomo café da manhã sozinha.\""},
             {"text": "Carol: \"I start work at 7 a.m.\"", "answer": True, "translation": "Carol: \"Eu começo a trabalhar às 7h.\""},
             {"text": "Carol: \"I watch TV in the evening.\"", "answer": False, "translation": "Carol: \"Eu assisto TV à noite.\""},
         ]},
        {"type": "choice",
         "prompt": "What does Carol do after work?",
         "translation": "O que a Carol faz depois do trabalho?",
         "options": ["\"I go to the gym.\"", "\"I have breakfast.\"", "\"I take a shower.\"", "\"I go to bed.\""], "correct": 0},
        {"type": "order",
         "prompt": "Put Carol's morning in order (click or drag the blocks).",
         "translation": "Coloque a manhã da Carol na ordem certa (clique ou arraste os blocos).",
         "example": "1º wake up → 2º …",
         "tokens": ["wake up →", "take a shower →", "get dressed →", "have breakfast →", "brush my teeth →", "start work"],
         "alternatives": []},
        {"type": "fill",
         "prompt": "Complete the sentences according to the text.",
         "translation": "Complete as frases de acordo com o texto.",
         "example": "Carol: \"I go to the [hospital].\"",
         "text": "1. Carol: \"I have breakfast with my family: bread and [coffee].\"\n"
                 "2. Carol: \"I have lunch at [12:00|12|twelve|noon].\"\n"
                 "3. Carol: \"I finish work at [3 p.m.|3|three|3 pm|three p.m.].\"\n"
                 "4. Carol: \"Finally, I go to bed at [10 p.m.|10|ten|10 pm|ten p.m.].\""},
    ],
}

AULA4_WRITING = {
    "title": "Writing — my morning routine",
    "lesson": 4,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Primeiro, monte frases da rotina. Depois, escreva um parágrafo sobre a SUA manhã, "
                   "usando First, Then, Next, After that e Finally.\nNão esqueça o pronome I em cada frase!",
    "topic": AULA4_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Look at the Portuguese sentence and write it in English.",
         "translation": "Leia a frase em português e escreva-a em inglês.",
         "example": "Eu acordo às 6h. → I wake up at 6 a.m.",
         "text": "1. Eu tomo banho. → [I take a shower.]\n"
                 "2. Eu escovo os dentes. → [I brush my teeth.]\n"
                 "3. Eu almoço. → [I have lunch.]\n"
                 "4. Eu vou para a academia. → [I go to the gym.]\n"
                 "5. Eu vou dormir. → [I go to bed.|I go to sleep.|I sleep.]"},
        {"type": "free",
         "prompt": "What do you do in the morning? Write a paragraph (5 or 6 sentences) about YOUR morning. "
                   "Use First, Then, After that, Next and Finally.",
         "translation": "O que você faz pela manhã? Escreva um parágrafo (5 ou 6 frases) sobre a SUA manhã. "
                        "Use First, Then, After that, Next e Finally.",
         "example": "First, I wake up at 6 a.m. Then I take a shower. After that, I …",
         "model_answer": "First, I wake up at 6 a.m. Then I take a shower and I get dressed. "
                         "After that, I have breakfast. Next, I brush my teeth. "
                         "Finally, I start work at 8 a.m.",
         "keywords": ["first", "then", "after that", "finally"], "min_words": 25, "points": 4},
    ],
}

# ---------- Aula 05 — Numbers (https://youtu.be/viInOHOnHYY) ----------

AULA5_TOPIC = "Aula 05 — Numbers"

AULA5_NUMBERS = {
    "title": "Numbers 0 to 1,000",
    "lesson": 5,
    "description": "Os números da aula. Lembre:\n"
                   "• 13 a 19 (thirTEEN) → a força fica no final. 30, 40, 50… (THIRty) → a força fica no começo.\n"
                   "• Números compostos levam hífen: 21 = twenty-one, 59 = fifty-nine.\n"
                   "• 100 = one hundred (ou a hundred) · 1,000 = one thousand (ou a thousand).",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the numbers to the words.",
         "translation": "Ligue os números às palavras.",
         "example": "3 → three",
         "pairs": [
             {"left": "8", "right": "eight"},
             {"left": "12", "right": "twelve"},
             {"left": "13", "right": "thirteen"},
             {"left": "30", "right": "thirty"},
             {"left": "15", "right": "fifteen"},
             {"left": "50", "right": "fifty"},
             {"left": "20", "right": "twenty"},
             {"left": "100", "right": "one hundred"},
         ]},
        {"type": "fill",
         "prompt": "Write the numbers in words.",
         "translation": "Escreva os números por extenso (em palavras).",
         "example": "4 → four   ·   21 → twenty-one (com hífen!)",
         "text": "1. 7 → [seven]\n"
                 "2. 11 → [eleven]\n"
                 "3. 14 → [fourteen]\n"
                 "4. 40 → [forty]\n"
                 "5. 45 → [forty-five]\n"
                 "6. 67 → [sixty-seven]\n"
                 "7. 99 → [ninety-nine]\n"
                 "8. 2,000 → [two thousand]"},
        {"type": "group",
         "prompt": "Where is the strong part of the word? Put the numbers in the right group.",
         "translation": "Onde fica a parte forte da palavra? Arraste os números para o grupo certo.",
         "example": "thirTEEN (13) → força no FINAL   ·   THIRty (30) → força no COMEÇO",
         "categories": ["força no FINAL (-TEEN)", "força no COMEÇO (-ty)"],
         "words": [
             {"text": "13 thirteen", "category": "força no FINAL (-TEEN)"},
             {"text": "14 fourteen", "category": "força no FINAL (-TEEN)"},
             {"text": "16 sixteen", "category": "força no FINAL (-TEEN)"},
             {"text": "19 nineteen", "category": "força no FINAL (-TEEN)"},
             {"text": "30 thirty", "category": "força no COMEÇO (-ty)"},
             {"text": "40 forty", "category": "força no COMEÇO (-ty)"},
             {"text": "60 sixty", "category": "força no COMEÇO (-ty)"},
             {"text": "90 ninety", "category": "força no COMEÇO (-ty)"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct spelling.",
         "translation": "Escolha a escrita correta.",
         "example": "5 → [five]",
         "text": "1. 21 → [*twenty-one|twenty one|twentyone]\n"
                 "2. 3 → [*three|tree|thre]\n"
                 "3. 40 → [*forty|fourty|fourteen]\n"
                 "4. 15 → [*fifteen|fiveteen|fifty]\n"
                 "5. 1,000 → [*one thousand|one hundred|one thousands]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Twenty-one\" is written with a hyphen (-). → True",
         "statements": [
             {"text": "The word \"one\" starts with a W sound.", "answer": True,
              "translation": "A palavra \"one\" começa com som de W."},
             {"text": "In \"five\" and in \"fifteen\", the letter I has the same sound.", "answer": False,
              "translation": "Em \"five\" e em \"fifteen\", a letra I tem o mesmo som."},
             {"text": "\"A hundred\" and \"one hundred\" mean the same: 100.", "answer": True,
              "translation": "\"A hundred\" e \"one hundred\" significam a mesma coisa: 100."},
             {"text": "If you don't understand a number, it's polite to say \"What?\".", "answer": False,
              "translation": "Se você não entender um número, é educado dizer \"What?\"."},
             {"text": "\"Sorry?\" and \"Can you repeat, please?\" are good ways to ask someone to repeat.", "answer": True,
              "translation": "\"Sorry?\" e \"Can you repeat, please?\" são boas formas de pedir para alguém repetir."},
         ]},
    ],
}

AULA5_PHONE_AGE_TIME = {
    "title": "Phone numbers, age and time",
    "lesson": 5,
    "description": "• Telefone: o 0 é falado como \"oh\" e números repetidos usam DOUBLE (66 = double six).\n"
                   "• Idade: I'm 36 years old (ou só I'm 36). Nunca \"I have 36 years\".\n"
                   "• Horas: It's ten o'clock. · It's two twenty-five (2:25). · a.m. = manhã · p.m. = depois do meio-dia.\n"
                   "• Horário de um compromisso: I wake up AT six o'clock.",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the phone numbers to the way we say them.",
         "translation": "Ligue os números de telefone ao jeito como falamos.",
         "example": "102 → one oh two",
         "pairs": [
             {"left": "233-4870", "right": "two double three, four eight seven oh"},
             {"left": "916-0055", "right": "nine one six, double oh, double five"},
             {"left": "704-2618", "right": "seven oh four, two six one eight"},
             {"left": "566-1209", "right": "five double six, one two oh nine"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct option.",
         "translation": "Escolha a opção correta.",
         "example": "How [old] are you?",
         "text": "1. How old [*are|is|have] you?\n"
                 "2. I [*am|have|has] 25 years old.\n"
                 "3. I'm 30 [*years old|years|old years].\n"
                 "4. What's your phone [*number|numbers|name]?\n"
                 "5. It's ten [*o'clock|hours|clock].\n"
                 "6. I wake up [*at|in|on] 6 a.m."},
        {"type": "choice",
         "prompt": "Which sentence is correct?",
         "translation": "Qual frase está correta?",
         "options": ["I'm 20 years old.", "I have 20 years.", "I'm 20 years.", "I have 20 years old."], "correct": 0},
        {"type": "match",
         "prompt": "Match the times to the way we say them.",
         "translation": "Ligue os horários ao jeito como falamos.",
         "example": "9:00 → It's nine o'clock.",
         "pairs": [
             {"left": "10:00", "right": "It's ten o'clock."},
             {"left": "2:25", "right": "It's two twenty-five."},
             {"left": "4:15", "right": "It's four fifteen."},
             {"left": "10:40", "right": "It's ten forty."},
             {"left": "5:45", "right": "It's five forty-five."},
         ]},
        {"type": "dropdown",
         "prompt": "a.m. or p.m.?",
         "translation": "a.m. (da meia-noite ao meio-dia) ou p.m. (do meio-dia à meia-noite)?",
         "example": "Eu acordo às 6 da manhã. → I wake up at 6 [a.m.].",
         "text": "1. Eu almoço à 1 da tarde. → I have lunch at 1 [*p.m.|a.m.].\n"
                 "2. Eu tomo café da manhã às 7. → I have breakfast at 7 [*a.m.|p.m.].\n"
                 "3. Eu vou dormir às 11 da noite. → I go to bed at 11 [*p.m.|a.m.].\n"
                 "4. Eu começo a trabalhar às 9 da manhã. → I start work at 9 [*a.m.|p.m.]."},
        {"type": "order",
         "prompt": "Put the words in order to make the question.",
         "translation": "Coloque as palavras na ordem certa para formar a pergunta.",
         "example": "old / How / you? / are → How old are you?",
         "tokens": ["What", "time", "do", "you", "wake", "up?"], "alternatives": []},
    ],
}

AULA5_LISTENING = {
    "title": "Listening — numbers, phones and times",
    "lesson": 5,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Dica: 13 (thirTEEN) tem a força no final; 30 (THIRty) tem a força no começo.",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "-TEEN or -TY? Listen and choose the number you hear.",
         "translation": "-TEEN ou -TY? Ouça e escolha o número que você escutar.",
         "example": "Você ouve: \"fourteen\" → escolha 14 (e não 40).",
         "audio": f"{AUDIO}/aula5-teens.m4a",
         "text": "1. [*13|30]   2. [*50|15]   3. [*16|60]   4. [*70|17]   5. [*18|80]   6. [*90|19]"},
        {"type": "fill",
         "prompt": "Dictation: listen and write the numbers (use digits).",
         "translation": "Ditado: ouça e escreva os números (use algarismos).",
         "example": "Você ouve: \"twenty-one\" → 21",
         "audio": f"{AUDIO}/aula5-dictation.m4a",
         "text": "1. [12]   2. [20]   3. [45]   4. [67]   5. [100]   6. [3,000|3000|3.000]"},
        {"type": "fill",
         "prompt": "Listen to three people. Write their phone numbers.",
         "translation": "Ouça três pessoas. Escreva o número de telefone de cada uma.",
         "example": "Você ouve: \"five five five, oh one three two\" → 555-0132",
         "audio": f"{AUDIO}/aula5-phones.m4a",
         "text": "1. Anna: [233-4870|2334870|233 4870]\n"
                 "2. Tom: [916-0055|9160055|916 0055]\n"
                 "3. Lucy: [704-2618|7042618|704 2618]"},
        {"type": "fill",
         "prompt": "Listen. What time is it? Write the time with numbers.",
         "translation": "Ouça. Que horas são? Escreva o horário com números.",
         "example": "Você ouve: \"It's nine o'clock.\" → 9:00",
         "audio": f"{AUDIO}/aula5-times.m4a",
         "text": "1. [10:00|10|10h] \n2. [2:25|2h25] \n3. [4:15|4h15] \n4. [10:40|10h40] \n5. [5:45|5h45]"},
    ],
}

AULA5_SPEAKING = {
    "title": "Speaking — say the numbers",
    "lesson": 5,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "THREE: ponta da língua entre os dentes + o som do R. Não se preocupe se não sair perfeito: é treino!",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the numbers.",
         "translation": "Ouça e repita os números.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula5-say-n{i}.m4a"} for i, t in enumerate(
             ["one", "two", "three", "eight", "twelve", "twenty", "a hundred", "a thousand"], 1)]},
        {"type": "speak",
         "prompt": "-TEEN or -TY? Listen and repeat. Pay attention to the strong part.",
         "translation": "-TEEN ou -TY? Ouça e repita. Preste atenção na parte forte da palavra.",
         "example": "thirTEEN (13) — THIRty (30)",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula5-say-t{i}.m4a"} for i, t in enumerate(
             ["thirteen, thirty", "fourteen, forty", "fifteen, fifty", "sixteen, sixty"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the questions and answers.",
         "translation": "Ouça e repita as perguntas e respostas.",
         "example": "\"How old are you?\" — \"I'm thirty-six years old.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula5-say-q{i}.m4a"} for i, t in enumerate(
             ["What's your phone number?", "My phone number is nine one six, double oh, double five.",
              "How old are you?", "I'm thirty-six years old.",
              "What time do you wake up?", "I wake up at six o'clock."], 1)]},
    ],
}

AULA5_READING = {
    "title": "Reading — new student",
    "lesson": 5,
    "subject": "Reading",
    "description": "Leia (e ouça) o diálogo na escola de inglês e responda às perguntas de acordo com o texto.",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen. Marcos is a new student at an English school.",
         "translation": "Leia e ouça. O Marcos é um aluno novo numa escola de inglês. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula5-reading.m4a",
         "text": "AT THE ENGLISH SCHOOL\n\n"
                 "Receptionist: Good afternoon! What's your name, please?\n"
                 "Marcos: Hi! My name's Marcos Oliveira.\n"
                 "Receptionist: How old are you, Marcos?\n"
                 "Marcos: I'm twenty-seven years old.\n"
                 "Receptionist: And what's your phone number?\n"
                 "Marcos: It's nine one six, double oh, double five.\n"
                 "Receptionist: Sorry? Can you repeat, please?\n"
                 "Marcos: Sure! Nine one six, double oh, double five.\n"
                 "Receptionist: Thank you. Your class is on Mondays at 7 p.m., in room one oh two.\n"
                 "Marcos: Great! What time is it now?\n"
                 "Receptionist: It's four fifteen.\n"
                 "Marcos: OK. Thank you! See you!"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "\"Marcos is a new student.\" → True",
         "statements": [
             {"text": "Marcos is 27 years old.", "answer": True, "translation": "O Marcos tem 27 anos."},
             {"text": "His phone number is 916-0055.", "answer": True, "translation": "O telefone dele é 916-0055."},
             {"text": "His class is at 7 a.m.", "answer": False, "translation": "A aula dele é às 7 da manhã."},
             {"text": "His class is in room 120.", "answer": False, "translation": "A aula dele é na sala 120."},
         ]},
        {"type": "choice",
         "prompt": "Why does the receptionist say \"Sorry? Can you repeat, please?\"",
         "translation": "Por que a recepcionista diz \"Sorry? Can you repeat, please?\"",
         "options": ["She doesn't understand the phone number.", "She is angry.", "She wants to know his age.",
                     "She wants to say goodbye."], "correct": 0},
        {"type": "fill",
         "prompt": "Complete according to the text. Use numbers.",
         "translation": "Complete de acordo com o texto. Use algarismos.",
         "example": "Marcos's age: [27]",
         "text": "1. Room number: [102]\n"
                 "2. Time of the class: [7 p.m.|7|7pm|7 pm|19:00|19h]\n"
                 "3. Time now: [4:15|4h15]"},
    ],
}

AULA5_WRITING = {
    "title": "Writing — numbers about me",
    "lesson": 5,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Corrija as frases e depois escreva um pequeno texto sobre você com números: "
                   "idade, telefone e horários.",
    "topic": AULA5_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Each sentence has a mistake. Rewrite the sentence correctly.",
         "translation": "Cada frase tem um erro. Reescreva a frase do jeito certo.",
         "example": "\"I have 18 years.\" → I'm 18 years old.",
         "text": "1. \"I have 25 years.\" → [I'm 25 years old.|I am 25 years old.|I'm twenty-five years old.|I am twenty-five years old.]\n"
                 "2. \"I'm 40 years.\" → [I'm 40 years old.|I am 40 years old.|I'm forty years old.|I am forty years old.|I'm 40.|I am 40.]\n"
                 "3. \"It's ten o'clocks.\" → [It's ten o'clock.|It is ten o'clock.]\n"
                 "4. \"I wake up in 7 a.m.\" → [I wake up at 7 a.m.|I wake up at 7am.|I wake up at 7 am.|I wake up at seven a.m.]\n"
                 "5. \"Twenty one\" (21) → [twenty-one]"},
        {"type": "free",
         "prompt": "Write about you (4 to 6 sentences): How old are you? What's your phone number? "
                   "What time do you wake up, start work (or study) and go to bed?",
         "translation": "Escreva sobre você (4 a 6 frases): Quantos anos você tem? Qual é o seu telefone? "
                        "Que horas você acorda, começa a trabalhar (ou estudar) e vai dormir? "
                        "(Se preferir, invente um número de telefone.)",
         "example": "I'm 32 years old. My phone number is 555-0132. I wake up at 6 a.m. …",
         "model_answer": "My name is Paula. I'm 32 years old. My phone number is 555-0132.\n"
                         "I wake up at 6 a.m. I start work at 8 a.m. I have lunch at 12:30.\n"
                         "I go to bed at 11 p.m.",
         "keywords": ["years old", "phone number", "at"], "min_words": 20, "points": 4},
    ],
}

# ---------- Aula 06 — Days of the Week, Seasons, Months (https://youtu.be/ClUHjyidPh0) ----------

AULA6_TOPIC = "Aula 06 — Days of the Week, Seasons, Months"

AULA6_DAYS = {
    "title": "Days of the week",
    "lesson": 6,
    "description": "Os dias da semana da aula. Lembre:\n"
                   "• Em inglês, os dias da semana SEMPRE começam com letra maiúscula (capital letter): Monday, Friday…\n"
                   "• TUesday (som do number two) ≠ THursday (som do TH).\n"
                   "• Wednesday tem letras mudas: fala-se \"WENZ-day\".",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the days of the week to Portuguese.",
         "translation": "Ligue os dias da semana ao português.",
         "example": "Monday → segunda-feira",
         "pairs": [
             {"left": "Tuesday", "right": "terça-feira"},
             {"left": "Wednesday", "right": "quarta-feira"},
             {"left": "Thursday", "right": "quinta-feira"},
             {"left": "Friday", "right": "sexta-feira"},
             {"left": "Saturday", "right": "sábado"},
             {"left": "Sunday", "right": "domingo"},
         ]},
        {"type": "order",
         "prompt": "Put the days of the week in order, starting with Monday.",
         "translation": "Coloque os dias da semana em ordem, começando pela segunda-feira (Monday).",
         "example": "Monday → Tuesday → …",
         "tokens": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "alternatives": []},
        {"type": "fill",
         "prompt": "Complete with the correct day.",
         "translation": "Complete com o dia correto.",
         "example": "The day after Monday is [Tuesday]. (O dia depois de segunda é terça.)",
         "text": "1. The day after Tuesday is [Wednesday].\n"
                 "2. The day after Wednesday is [Thursday].\n"
                 "3. The day before Saturday is [Friday].\n"
                 "4. The day after Saturday is [Sunday]."},
        {"type": "choice",
         "prompt": "Which sentence is written correctly?",
         "translation": "Qual frase está escrita corretamente?",
         "options": ["My English class is on Monday.", "My English class is on monday.", "my English class is on monday.",
                     "My english class is on MONDAY."], "correct": 0},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Sunday\" means \"domingo\". → True",
         "statements": [
             {"text": "In English, the days of the week start with a capital letter.", "answer": True,
              "translation": "Em inglês, os dias da semana começam com letra maiúscula."},
             {"text": "\"Tuesday\" starts with the same sound as the number two.", "answer": True,
              "translation": "\"Tuesday\" começa com o mesmo som do número two (2)."},
             {"text": "\"Thursday\" means \"terça-feira\".", "answer": False,
              "translation": "\"Thursday\" significa \"terça-feira\"."},
             {"text": "In \"Wednesday\", we pronounce all the letters.", "answer": False,
              "translation": "Em \"Wednesday\", pronunciamos todas as letras."},
         ]},
    ],
}

AULA6_MONTHS = {
    "title": "Months and seasons",
    "lesson": 6,
    "description": "Os meses do ano (months) e as estações (seasons).\n"
                   "• Os meses também começam SEMPRE com letra maiúscula: January, July…\n"
                   "• Outono tem duas palavras: autumn ou fall (fall = cair, como as folhas).\n"
                   "• Pergunta com WHY (por quê?) → resposta com BECAUSE (porque).",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the seasons to Portuguese.",
         "translation": "Ligue as estações do ano ao português.",
         "example": "summer → verão",
         "pairs": [
             {"left": "winter", "right": "inverno"},
             {"left": "spring", "right": "primavera"},
             {"left": "summer", "right": "verão"},
             {"left": "autumn / fall", "right": "outono"},
         ]},
        {"type": "match",
         "prompt": "Match the months to Portuguese.",
         "translation": "Ligue os meses ao português.",
         "example": "January → janeiro",
         "pairs": [
             {"left": "February", "right": "fevereiro"},
             {"left": "April", "right": "abril"},
             {"left": "May", "right": "maio"},
             {"left": "June", "right": "junho"},
             {"left": "July", "right": "julho"},
             {"left": "August", "right": "agosto"},
             {"left": "September", "right": "setembro"},
             {"left": "December", "right": "dezembro"},
         ]},
        {"type": "fill",
         "prompt": "Complete the list of months.",
         "translation": "Complete a lista dos meses do ano.",
         "example": "January, [February], March…",
         "text": "January, February, [March], April, [May], June, [July], August, [September], [October], November, [December]"},
        {"type": "dropdown",
         "prompt": "Choose the correct word.",
         "translation": "Escolha a palavra correta.",
         "example": "What's your favorite [season]? — Summer.",
         "text": "1. What's your favorite [*month|season|day]? — December.\n"
                 "2. What's your favorite [*season|month|day]? — Winter.\n"
                 "3. What's your favorite day of the [*week|year|month]? — Friday.\n"
                 "4. [*Why|What|How]? — Because I love Christmas.\n"
                 "5. My favorite season is summer [*because|why|what] I can go to the beach."},
        {"type": "choice",
         "prompt": "Which sentence is written correctly?",
         "translation": "Qual frase está escrita corretamente?",
         "options": ["My favorite month is October.", "My favorite month is october.", "my favorite month is october.",
                     "My Favorite Month is october."], "correct": 0},
        {"type": "truefalse",
         "prompt": "True or false?",
         "translation": "Verdadeiro ou falso?",
         "example": "\"Spring\" means \"primavera\". → True",
         "statements": [
             {"text": "\"Fall\" and \"autumn\" mean the same season.", "answer": True,
              "translation": "\"Fall\" e \"autumn\" são a mesma estação."},
             {"text": "There are five seasons in the year.", "answer": False,
              "translation": "Há cinco estações no ano."},
             {"text": "We use \"why\" in the question and \"because\" in the answer.", "answer": True,
              "translation": "Usamos \"why\" na pergunta e \"because\" na resposta."},
             {"text": "In English, the months start with a small letter (letra minúscula).", "answer": False,
              "translation": "Em inglês, os meses começam com letra minúscula."},
         ]},
    ],
}

AULA6_LISTENING = {
    "title": "Listening — days, months and favorites",
    "lesson": 6,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Atenção: TUesday ≠ THursday!",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Tuesday or Thursday? Listen and choose.",
         "translation": "Tuesday (terça) ou Thursday (quinta)? Ouça e escolha.",
         "example": "Você ouve: \"Tuesday\" (som do two) → escolha Tuesday.",
         "audio": f"{AUDIO}/aula6-tt.m4a",
         "text": "1. [*Thursday|Tuesday]   2. [*Tuesday|Thursday]   3. [*Tuesday|Thursday]   4. [*Thursday|Tuesday]"},
        {"type": "fill",
         "prompt": "Dictation: listen and write the days and months.",
         "translation": "Ditado: ouça e escreva os dias e os meses. Lembre da letra maiúscula!",
         "example": "Você ouve: \"Monday\" → Monday",
         "audio": f"{AUDIO}/aula6-dictation.m4a",
         "text": "1. [Wednesday]   2. [Saturday]   3. [February]   4. [August]   5. [Friday]   6. [June]"},
        {"type": "info",
         "prompt": "Now listen to Ben and Clara talking about their favorite day, season and month.",
         "translation": "Agora ouça o Ben e a Clara falando sobre o dia, a estação e o mês favoritos deles. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula6-dialogue.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "fill",
         "prompt": "Listen again and complete the table.",
         "translation": "Ouça de novo e complete a tabela.",
         "example": "Ben — favorite day: [Sunday]",
         "text": "Clara — favorite day: [Friday]\n"
                 "Ben — favorite season: [winter]\n"
                 "Clara — favorite season: [spring]\n"
                 "Clara — favorite month: [July]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the conversation.",
         "translation": "Verdadeiro ou falso? Responda de acordo com a conversa.",
         "example": "Ben: \"My favorite day is Sunday.\" → True",
         "statements": [
             {"text": "Ben: \"I love hot chocolate.\"", "answer": True,
              "translation": "Ben: \"Eu amo chocolate quente.\""},
             {"text": "Clara: \"My favorite month is December.\"", "answer": False,
              "translation": "Clara: \"Meu mês favorito é dezembro.\""},
             {"text": "Clara: \"My birthday is in July.\"", "answer": True,
              "translation": "Clara: \"Meu aniversário é em julho.\""},
         ]},
    ],
}

AULA6_SPEAKING = {
    "title": "Speaking — days, months and seasons",
    "lesson": 6,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: WEDNESDAY = \"WENZ-day\" · FEBRUARY = \"FEB-ru-ary\" (sem forçar o R) · AUGUST e AUTUMN: AU soa como \"ó\".",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the days of the week.",
         "translation": "Ouça e repita os dias da semana.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula6-say-d{i}.m4a"} for i, t in enumerate(
             ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the seasons and the difficult months.",
         "translation": "Ouça e repita as estações e os meses mais difíceis.",
         "example": "February — August — autumn",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula6-say-m{i}.m4a"} for i, t in enumerate(
             ["winter", "spring", "summer", "autumn", "fall", "January", "February", "August", "October"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the questions and answers.",
         "translation": "Ouça e repita as perguntas e respostas.",
         "example": "\"What's your favorite season?\" — \"My favorite season is summer.\" — \"Why?\" — \"Because I can go to the beach.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula6-say-q{i}.m4a"} for i, t in enumerate(
             ["What's your favorite day of the week?", "My favorite day of the week is Saturday because I relax.",
              "What's your favorite season?", "My favorite season is summer because I can go to the beach.",
              "What's your favorite month?", "My favorite month is December because I love Christmas."], 1)]},
    ],
}

AULA6_READING = {
    "title": "Reading — Lucas's favorites",
    "lesson": 6,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Lucas's text.",
         "translation": "Leia e ouça o texto do Lucas. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula6-reading.m4a",
         "text": "MY FAVORITES — by Lucas\n\n"
                 "Hi! I'm Lucas and I'm from Brazil. I'm 19 years old.\n"
                 "My favorite day of the week is Friday because I go to the gym with my friends. "
                 "I don't like Monday because I start work at 7 a.m.!\n"
                 "My favorite season is summer because I love the beach. "
                 "I don't like winter because I don't like cold weather.\n"
                 "My favorite month is April because my birthday is on April 10th. "
                 "And you? What's your favorite month? Why?"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Lucas: \"I'm from Brazil.\" → True",
         "statements": [
             {"text": "Lucas: \"My favorite day is Monday.\"", "answer": False,
              "translation": "Lucas: \"Meu dia favorito é segunda-feira.\""},
             {"text": "Lucas: \"I love the beach.\"", "answer": True,
              "translation": "Lucas: \"Eu amo a praia.\""},
             {"text": "Lucas: \"I like cold weather.\"", "answer": False,
              "translation": "Lucas: \"Eu gosto de tempo frio.\""},
             {"text": "Lucas: \"My birthday is in April.\"", "answer": True,
              "translation": "Lucas: \"Meu aniversário é em abril.\""},
         ]},
        {"type": "choice",
         "prompt": "Why is Friday Lucas's favorite day?",
         "translation": "Por que sexta-feira é o dia favorito do Lucas?",
         "options": ["\"Because I go to the gym with my friends.\"", "\"Because I start work at 7 a.m.\"",
                     "\"Because I love the beach.\"", "\"Because of my birthday.\""], "correct": 0},
        {"type": "fill",
         "prompt": "Complete according to the text.",
         "translation": "Complete de acordo com o texto.",
         "example": "Lucas's age: [19]",
         "text": "1. Favorite season: [summer]\n"
                 "2. The season he doesn't like: [winter]\n"
                 "3. Favorite month: [April]\n"
                 "4. The day he doesn't like: [Monday]"},
    ],
}

AULA6_WRITING = {
    "title": "Writing — my favorites",
    "lesson": 6,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Escreva frases com WHY e BECAUSE e depois um pequeno texto sobre os seus favoritos.\n"
                   "Não esqueça: dias da semana e meses com letra maiúscula!",
    "topic": AULA6_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the questions in English.",
         "translation": "Escreva as perguntas em inglês.",
         "example": "Qual é o seu mês favorito? → What's your favorite month?",
         "text": "1. Qual é a sua estação favorita? → [What's your favorite season?|What is your favorite season?|"
                 "What's your favourite season?|What is your favourite season?]\n"
                 "2. Qual é o seu dia da semana favorito? → [What's your favorite day of the week?|What is your favorite day of the week?|"
                 "What's your favourite day of the week?|What is your favourite day of the week?|What's your favorite day?|What is your favorite day?]\n"
                 "3. Por quê? → [Why?]"},
        {"type": "fill",
         "prompt": "Complete the answers with \"because\" and the reason in parentheses.",
         "translation": "Complete as respostas com \"because\" e o motivo entre parênteses.",
         "example": "My favorite day is Saturday ___ (eu relaxo). → because I relax",
         "text": "1. My favorite month is December [because I love Christmas] (eu amo o Natal).\n"
                 "2. My favorite season is summer [because I go to the beach|because I can go to the beach] (eu vou à praia).\n"
                 "3. My favorite day is Friday [because I go to the gym] (eu vou para a academia)."},
        {"type": "free",
         "prompt": "Write about YOUR favorites (4 to 6 sentences): your favorite day of the week, season and month. "
                   "Say why, using because.",
         "translation": "Escreva sobre os SEUS favoritos (4 a 6 frases): seu dia da semana, estação e mês favoritos. "
                        "Diga por quê, usando because.",
         "example": "My favorite day of the week is Saturday because I relax.",
         "model_answer": "My favorite day of the week is Saturday because I relax and I watch TV.\n"
                         "My favorite season is spring because I love flowers.\n"
                         "My favorite month is December because I love Christmas.",
         "keywords": ["favorite", "because", "season", "month"], "min_words": 20, "points": 4},
    ],
}

# ---------- Aula 07 — Subject Pronouns (https://youtu.be/19tnfU4tYoE) ----------

AULA7_TOPIC = "Aula 07 — Subject Pronouns"

AULA7_PRONOUNS = {
    "title": "Subject pronouns",
    "lesson": 7,
    "description": "Os pronomes sujeitos (subject pronouns) da aula:\n"
                   "• Singular: I (eu) · you (você) · he (ele) · she (ela) · it (ele/ela para animais, objetos e lugares)\n"
                   "• Plural: we (nós) · you (vocês) · they (eles/elas)\n"
                   "• YOU é igual no singular e no plural: você ou vocês.",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the subject pronouns to Portuguese.",
         "translation": "Ligue os pronomes sujeitos ao português.",
         "example": "I → eu",
         "pairs": [
             {"left": "you", "right": "você / vocês"},
             {"left": "he", "right": "ele (um homem ou menino)"},
             {"left": "she", "right": "ela (uma mulher ou menina)"},
             {"left": "it", "right": "ele / ela (animal, objeto, lugar)"},
             {"left": "we", "right": "nós"},
             {"left": "they", "right": "eles / elas"},
         ]},
        {"type": "group",
         "prompt": "Singular or plural? Put each pronoun in the correct group.",
         "translation": "Singular (uma pessoa ou coisa) ou plural (mais de uma)? Coloque cada pronome no grupo certo.",
         "example": "I (eu) → singular",
         "categories": ["singular", "plural"],
         "words": [
             {"text": "I", "category": "singular"}, {"text": "he", "category": "singular"},
             {"text": "she", "category": "singular"}, {"text": "it", "category": "singular"},
             {"text": "you (você)", "category": "singular"},
             {"text": "we", "category": "plural"}, {"text": "they", "category": "plural"},
             {"text": "you (vocês)", "category": "plural"},
         ]},
        {"type": "order",
         "prompt": "Put the pronouns in the order of the lesson (like in Portuguese: eu, tu/você, ele, ela…).",
         "translation": "Coloque os pronomes na ordem da aula (como no português: eu, você, ele, ela…).",
         "example": "I → you → …",
         "tokens": ["I", "you", "he", "she", "it", "we", "you", "they"], "alternatives": []},
        {"type": "dropdown",
         "prompt": "Choose the correct pronoun for the Portuguese word.",
         "translation": "Escolha o pronome correto para a palavra em português.",
         "example": "ela → [she]",
         "text": "1. nós → [*we|they|you]\n"
                 "2. eles → [*they|he|we]\n"
                 "3. ele (o menino) → [*he|she|it]\n"
                 "4. ele (o computador) → [*it|he|they]\n"
                 "5. vocês → [*you|we|they]\n"
                 "6. eu → [*I|it|you]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"She\" means \"ela\". → True",
         "statements": [
             {"text": "We use \"it\" for animals, objects and places.", "answer": True,
              "translation": "Usamos \"it\" para animais, objetos e lugares."},
             {"text": "\"You\" can mean \"você\" or \"vocês\".", "answer": True,
              "translation": "\"You\" pode significar \"você\" ou \"vocês\"."},
             {"text": "We use \"it\" for five dogs.", "answer": False,
              "translation": "Usamos \"it\" para cinco cachorros."},
             {"text": "\"They\" means \"eles\" or \"elas\".", "answer": True,
              "translation": "\"They\" significa \"eles\" ou \"elas\"."},
             {"text": "We use \"he\" for a table (mesa).", "answer": False,
              "translation": "Usamos \"he\" para uma mesa."},
         ]},
    ],
}

AULA7_REPLACE = {
    "title": "Names → pronouns",
    "lesson": 7,
    "description": "O pronome substitui o nome na frase:\n"
                   "Daniel → he · Sarah → she · my dog → it · my dogs → they · my friend and I → we · the boy and the girl → they\n"
                   "Lembre: IT só no singular (1 coisa ou animal). No plural é sempre THEY.",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Which pronoun replaces the words?",
         "translation": "Qual pronome substitui as palavras?",
         "example": "Daniel → [he]",
         "text": "1. Sarah → [*she|he|it]\n"
                 "2. my dog → [*it|he|they]\n"
                 "3. my dogs → [*they|it|we]\n"
                 "4. my friend and I → [*we|they|you]\n"
                 "5. the boy and the girl → [*they|we|he]\n"
                 "6. my mother → [*she|he|it]\n"
                 "7. the house → [*it|she|they]\n"
                 "8. Paul and you → [*you|they|we]"},
        {"type": "group",
         "prompt": "Put the words in the correct pronoun group.",
         "translation": "Coloque as palavras no grupo do pronome correto.",
         "example": "my father (meu pai) → he",
         "categories": ["he", "she", "it", "we", "they"],
         "words": [
             {"text": "John", "category": "he"}, {"text": "the boy", "category": "he"},
             {"text": "Maria", "category": "she"}, {"text": "my sister", "category": "she"},
             {"text": "the cat", "category": "it"}, {"text": "the pencil", "category": "it"},
             {"text": "London", "category": "it"},
             {"text": "my family and I", "category": "we"}, {"text": "Ana and I", "category": "we"},
             {"text": "the cats", "category": "they"}, {"text": "Tom and Lisa", "category": "they"},
         ]},
        {"type": "fill",
         "prompt": "Singular or plural? Complete with IT or THEY.",
         "translation": "Singular ou plural? Complete com IT (1 coisa/animal) ou THEY (mais de 1).",
         "example": "[It] is a cat. → [They] are cats.",
         "text": "1. Look at the dog. [It] is cute.\n"
                 "2. Look at the dogs. [They] are cute.\n"
                 "3. This is my pencil. [It] is blue.\n"
                 "4. These are my pencils. [They] are colorful.\n"
                 "5. I love Rio. [It] is beautiful."},
        {"type": "choice",
         "prompt": "\"My friend and I\" = ?",
         "translation": "\"Meu amigo e eu\" = ? (Dica: eu estou incluído no grupo.)",
         "options": ["we", "they", "you", "he"], "correct": 0},
        {"type": "choice",
         "prompt": "Which sentence is correct?",
         "translation": "Qual frase está correta?",
         "options": ["They are cats.", "It are cats.", "It is cats.", "He is cats."], "correct": 0},
    ],
}

AULA7_LISTENING = {
    "title": "Listening — he, she, it, we, they",
    "lesson": 7,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Atenção: HE (ri) ≠ SHE (shi) · THEY (dêi, com a língua entre os dentes).",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "He or she? Listen and choose.",
         "translation": "He (ele) ou she (ela)? Ouça e escolha.",
         "example": "Você ouve: \"she\" → escolha she.",
         "audio": f"{AUDIO}/aula7-heshe.m4a",
         "text": "1. [*she|he]   2. [*he|she]   3. [*he|she]   4. [*she|he]   5. [*she|he]"},
        {"type": "fill",
         "prompt": "Dictation: listen and write the pronoun you hear.",
         "translation": "Ditado: ouça e escreva o pronome que você ouvir.",
         "example": "Você ouve: \"It is a cat.\" → [It] is a cat.",
         "audio": f"{AUDIO}/aula7-dictation.m4a",
         "text": "1. [They] are cats.\n"
                 "2. [We] are friends.\n"
                 "3. [She] is my sister.\n"
                 "4. [It] is blue.\n"
                 "5. [You] are students.\n"
                 "6. [He] is my teacher."},
        {"type": "info",
         "prompt": "Now listen to Emma showing her photos.",
         "translation": "Agora ouça a Emma mostrando as fotos dela. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula7-photos.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again. Which pronoun does Emma use?",
         "translation": "Ouça de novo. Qual pronome a Emma usa para cada foto?",
         "example": "Emma — \"This is me. I am from Canada.\" → me = [I]",
         "text": "1. my brother, Jack → [*he|she|it]\n"
                 "2. my dog, Bob → [*it|he|they]\n"
                 "3. my friends, Mia and Kate → [*they|we|she]\n"
                 "4. my mother → [*she|he|they]\n"
                 "5. my brother and I → [*we|they|you]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the audio.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o áudio.",
         "example": "Emma: \"I am from Canada.\" → True",
         "statements": [
             {"text": "Emma: \"My dog is big.\"", "answer": False,
              "translation": "Emma: \"Meu cachorro é grande.\""},
             {"text": "Emma: \"My friends are from Brazil.\"", "answer": True,
              "translation": "Emma: \"Minhas amigas são do Brasil.\""},
             {"text": "Emma: \"My brother and I are students.\"", "answer": True,
              "translation": "Emma: \"Meu irmão e eu somos estudantes.\""},
         ]},
    ],
}

AULA7_SPEAKING = {
    "title": "Speaking — subject pronouns",
    "lesson": 7,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas: HE soa como \"ri\" (H aspirado) · SHE soa como \"shi\" · THEY: ponha a ponta da língua entre os dentes — \"dêi\", não \"dei\".",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the subject pronouns.",
         "translation": "Ouça e repita os pronomes sujeitos.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula7-say-p{i}.m4a"} for i, t in enumerate(
             ["I", "you", "he", "she", "it", "we", "they"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat: singular (it) and plural (they).",
         "translation": "Ouça e repita: singular (it) e plural (they).",
         "example": "\"It is a cat.\" — \"They are cats.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula7-say-s{i}.m4a"} for i, t in enumerate(
             ["It is a cat.", "They are cats.", "It is cute.", "They are cute.", "It is blue.", "They are colorful."], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases.",
         "example": "\"He is my friend.\" (Ele é meu amigo.)",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula7-say-f{i}.m4a"} for i, t in enumerate(
             ["He is my friend.", "She is my teacher.", "We are students.", "You are my friends.", "They are from Brazil."], 1)]},
    ],
}

AULA7_READING = {
    "title": "Reading — Julia's family",
    "lesson": 7,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto. Preste atenção nos pronomes!",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Julia's text.",
         "translation": "Leia e ouça o texto da Julia. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula7-reading.m4a",
         "text": "MY FAMILY — by Julia\n\n"
                 "Hi! I'm Julia. I'm 20 years old and I'm from Brazil.\n"
                 "This is my mother, Ana. She is a teacher. "
                 "This is my father, Carlos. He is a doctor.\n"
                 "My brother Leo and I are students. We study English on Saturdays.\n"
                 "This is my cat, Mimi. It is small and white. It is very cute!\n"
                 "My grandparents have two dogs, Rex and Bolt. They are big and brown."},
        {"type": "dropdown",
         "prompt": "Who or what is it? Read the text and choose.",
         "translation": "Quem ou o que é? Leia o texto e escolha a quem o pronome se refere.",
         "example": "\"She is a teacher.\" → She = [Ana]",
         "text": "1. \"He is a doctor.\" → He = [*Carlos|Leo|Mimi]\n"
                 "2. \"We study English.\" → We = [*Julia and Leo|Ana and Carlos|Rex and Bolt]\n"
                 "3. \"It is small and white.\" → It = [*Mimi|Rex|Leo]\n"
                 "4. \"They are big and brown.\" → They = [*Rex and Bolt|Julia and Leo|Ana and Carlos]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Julia: \"I'm from Brazil.\" → True",
         "statements": [
             {"text": "Julia: \"My mother is a doctor.\"", "answer": False,
              "translation": "Julia: \"Minha mãe é médica.\""},
             {"text": "Julia: \"My brother and I are students.\"", "answer": True,
              "translation": "Julia: \"Meu irmão e eu somos estudantes.\""},
             {"text": "Julia: \"My cat is big.\"", "answer": False,
              "translation": "Julia: \"Minha gata é grande.\""},
             {"text": "Julia: \"We study English on Saturdays.\"", "answer": True,
              "translation": "Julia: \"Nós estudamos inglês aos sábados.\""},
         ]},
        {"type": "fill",
         "prompt": "Complete with the pronoun from the text.",
         "translation": "Complete com o pronome usado no texto.",
         "example": "Ana → [she]",
         "text": "1. Carlos → [he]\n"
                 "2. Mimi → [it]\n"
                 "3. Rex and Bolt → [they]\n"
                 "4. my brother Leo and I (Julia) → [we]"},
    ],
}

AULA7_WRITING = {
    "title": "Writing — people and things in my life",
    "lesson": 7,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Troque os nomes por pronomes e depois escreva um pequeno texto apresentando pessoas, animais e coisas da sua vida.\n"
                   "Escreva He is / She is / It is / They are por extenso (sem abreviar).",
    "topic": AULA7_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Rewrite the sentences. Replace the words in CAPITAL LETTERS with a pronoun.",
         "translation": "Reescreva as frases trocando as palavras em MAIÚSCULAS por um pronome.",
         "example": "DANIEL is my friend. → He is my friend.",
         "text": "1. SARAH is my teacher. → [She is my teacher.|She's my teacher.]\n"
                 "2. MY DOG is cute. → [It is cute.|It's cute.]\n"
                 "3. MY DOGS are cute. → [They are cute.|They're cute.]\n"
                 "4. MY FRIEND AND I are students. → [We are students.|We're students.]\n"
                 "5. PAUL is from Canada. → [He is from Canada.|He's from Canada.]"},
        {"type": "fill",
         "prompt": "Write the sentences in English.",
         "translation": "Escreva as frases em inglês.",
         "example": "Ele é meu amigo. → He is my friend.",
         "text": "1. Ela é minha mãe. → [She is my mother.|She's my mother.|She is my mom.|She's my mom.]\n"
                 "2. Nós somos amigos. → [We are friends.|We're friends.]\n"
                 "3. Eles são fofos. → [They are cute.|They're cute.]"},
        {"type": "free",
         "prompt": "Write about 3 or 4 people, animals or things in your life (4 to 6 sentences). "
                   "Use \"This is my…\" and then a pronoun: he, she, it, we or they.",
         "translation": "Escreva sobre 3 ou 4 pessoas, animais ou coisas da sua vida (4 a 6 frases). "
                        "Use \"This is my…\" e depois um pronome: he, she, it, we ou they.",
         "example": "This is my sister, Paula. She is 25 years old.",
         "model_answer": "This is my sister, Paula. She is 25 years old.\n"
                         "This is my friend, Marcos. He is from Recife.\n"
                         "This is my cat, Luna. It is black and very cute.\n"
                         "My friends and I love music. We are in a band.",
         "keywords": ["this is my", "he", "she", "it", "we"], "min_words": 20, "points": 4},
    ],
}

# ---------- Aula 08 — Present Simple (affirmative) (https://youtu.be/5y_qrzgDTHA) ----------

AULA8_TOPIC = "Aula 08 — Present Simple (affirmative)"

AULA8_RULES = {
    "title": "He, she, it + S",
    "lesson": 8,
    "description": "Present simple = rotina (o que você faz todo dia ou com frequência).\n"
                   "• I, you, we, they → o verbo NÃO muda: I wake up · they watch TV\n"
                   "• HE, SHE, IT → o verbo ganha S: he wakes up · she takes a shower\n"
                   "• Verbo terminado em S, SH, CH, TCH, X ou O → ES: watches, finishes, fixes, passes, goes, does\n"
                   "• Consoante + Y → IES: study → studies, cry → cries\n"
                   "• HAVE → HAS: she has breakfast\n"
                   "Esse S NÃO é plural — é a conjugação do verbo!",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "How do we write the verb with he, she, it? Put each verb in the correct group.",
         "translation": "Como escrevemos o verbo com he, she, it? Coloque cada verbo no grupo certo.",
         "example": "watch → watches → grupo \"+ ES\"",
         "categories": ["+ S", "+ ES", "Y → IES", "have → has"],
         "words": [
             {"text": "wake up", "category": "+ S"}, {"text": "take", "category": "+ S"},
             {"text": "work", "category": "+ S"}, {"text": "play", "category": "+ S"},
             {"text": "finish", "category": "+ ES"}, {"text": "fix", "category": "+ ES"},
             {"text": "go", "category": "+ ES"}, {"text": "do", "category": "+ ES"},
             {"text": "brush", "category": "+ ES"},
             {"text": "study", "category": "Y → IES"}, {"text": "cry", "category": "Y → IES"},
             {"text": "fly", "category": "Y → IES"},
             {"text": "have", "category": "have → has"},
         ]},
        {"type": "fill",
         "prompt": "Write the verb with HE / SHE / IT.",
         "translation": "Escreva o verbo como fica com HE / SHE / IT (terceira pessoa do singular).",
         "example": "wake up → she [wakes up]",
         "text": "1. take → she [takes]\n"
                 "2. watch → he [watches]\n"
                 "3. go → she [goes]\n"
                 "4. study → he [studies]\n"
                 "5. have → she [has]\n"
                 "6. finish → he [finishes]\n"
                 "7. do → she [does]\n"
                 "8. fix → he [fixes]"},
        {"type": "match",
         "prompt": "Match the verbs to Portuguese.",
         "translation": "Ligue os verbos da aula ao português.",
         "example": "study → estudar",
         "pairs": [
             {"left": "finish", "right": "terminar"},
             {"left": "fix", "right": "consertar"},
             {"left": "pass", "right": "passar"},
             {"left": "fly", "right": "voar"},
             {"left": "cry", "right": "chorar"},
             {"left": "copy", "right": "copiar"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"He watches TV.\" has ES because of \"he\". → True",
         "statements": [
             {"text": "We use the present simple to talk about our routine.", "answer": True,
              "translation": "Usamos o present simple para falar sobre a nossa rotina."},
             {"text": "With \"they\", the verb gets an S: they watches.", "answer": False,
              "translation": "Com \"they\", o verbo ganha S: they watches."},
             {"text": "The S in \"she works\" is the plural.", "answer": False,
              "translation": "O S em \"she works\" é o plural."},
             {"text": "\"Have\" with \"he\" or \"she\" is \"has\".", "answer": True,
              "translation": "\"Have\" com \"he\" ou \"she\" vira \"has\"."},
             {"text": "\"Study\" with \"she\" is \"studies\".", "answer": True,
              "translation": "\"Study\" com \"she\" vira \"studies\"."},
         ]},
    ],
}

AULA8_SENTENCES = {
    "title": "My routine and their routine",
    "lesson": 8,
    "description": "Agora com frases completas! Olhe sempre o pronome (ou o nome) antes do verbo:\n"
                   "I / you / we / they → wake up · He / she / it (e nomes como Maria, my father) → wakes up.\n"
                   "Para contar a sequência da rotina: first (primeiro) → then / next (então / em seguida) → after that (depois disso) → finally (finalmente).",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose the correct form of the verb.",
         "translation": "Escolha a forma correta do verbo.",
         "example": "She [wakes up] at 6 a.m.",
         "text": "1. I [*wake up|wakes up] at 5:30.\n"
                 "2. He [*takes|take] a shower every day.\n"
                 "3. They [*watch|watches] TV every day.\n"
                 "4. My mother [*goes|go] to bed at 11 p.m.\n"
                 "5. We [*study|studies] English twice a week.\n"
                 "6. Paul [*has|have] breakfast at 7 a.m.\n"
                 "7. You [*go|goes] to the gym every day."},
        {"type": "fill",
         "prompt": "Complete with the verb in parentheses.",
         "translation": "Complete com o verbo entre parênteses. Atenção ao pronome!",
         "example": "She ___ (wake up) at 7. → She [wakes up] at 7.",
         "text": "1. She [finishes] work at 6 p.m. (finish)\n"
                 "2. I [have] lunch at noon. (have)\n"
                 "3. He [fixes] computers. (fix)\n"
                 "4. She [studies] French. (study)\n"
                 "5. We [go] to bed at 10 p.m. (go)\n"
                 "6. He [does] his homework every day. (do)"},
        {"type": "choice",
         "prompt": "Is this sentence correct? \"They watches TV every day.\"",
         "translation": "Esta frase está correta? \"They watches TV every day.\"",
         "options": ["No. → They watch TV every day.", "Yes, it is correct.",
                     "No. → They watchs TV every day.", "No. → They watcheses TV every day."], "correct": 0},
        {"type": "order",
         "prompt": "Put the words in order to make a sentence.",
         "translation": "Coloque as palavras em ordem para formar a frase. (Ela vai dormir às 11 da noite.)",
         "example": "He / at 7 / wakes up → He wakes up at 7.",
         "tokens": ["She", "goes", "to", "bed", "at", "11 p.m."], "alternatives": []},
        {"type": "dropdown",
         "prompt": "Complete Maria's routine with the sequence words.",
         "translation": "Complete a rotina da Maria com as palavras de sequência.",
         "example": "[First], she wakes up at 6.",
         "text": "[*First|Finally], Maria wakes up at 6 a.m. [*Then|First] she takes a shower. "
                 "[*After that|First], she has breakfast. [*Finally|First], she goes to work."},
    ],
}

AULA8_LISTENING = {
    "title": "Listening — Mark's day",
    "lesson": 8,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Preste atenção no S no final do verbo: wake ≠ wakeS · watch ≠ watchES.",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "With S or without S? Listen and choose.",
         "translation": "Com S ou sem S? Ouça e escolha o que você ouvir.",
         "example": "Você ouve: \"watches\" → escolha watches.",
         "audio": f"{AUDIO}/aula8-s.m4a",
         "text": "1. [*watches|watch]   2. [*go|goes]   3. [*studies|study]   4. [*have|has]   5. [*finishes|finish]   6. [*take|takes]"},
        {"type": "fill",
         "prompt": "Dictation: listen and write the verb.",
         "translation": "Ditado: ouça e escreva o verbo que falta.",
         "example": "Você ouve: \"He wakes up at seven.\" → He [wakes up] at 7.",
         "audio": f"{AUDIO}/aula8-dictation.m4a",
         "text": "1. She [takes] a shower every day.\n"
                 "2. They [watch] TV at night.\n"
                 "3. He [goes] to the gym every day.\n"
                 "4. She [has] breakfast at 8 a.m.\n"
                 "5. I [study] English twice a week."},
        {"type": "info",
         "prompt": "Now listen to Amy talking about her brother Mark's routine.",
         "translation": "Agora ouça a Amy falando sobre a rotina do irmão dela, o Mark. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula8-mark.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "fill",
         "prompt": "Listen again and write the times.",
         "translation": "Ouça de novo e escreva os horários (use números, como 6:30).",
         "example": "Mark wakes up at [6:30].",
         "text": "1. He has breakfast at [7:00|7|7 a.m.|7:00 a.m.].\n"
                 "2. He starts work at [8:00|8|8 a.m.|8:00 a.m.].\n"
                 "3. He finishes work at [5:00|5|5 p.m.|5:00 p.m.].\n"
                 "4. He goes to bed at [11:00|11|11 p.m.|11:00 p.m.]."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the audio.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o áudio.",
         "example": "Mark wakes up at 6:30. → True",
         "statements": [
             {"text": "Mark takes a shower in the morning.", "answer": True,
              "translation": "O Mark toma banho de manhã."},
             {"text": "Mark goes to the gym in the morning.", "answer": False,
              "translation": "O Mark vai à academia de manhã."},
             {"text": "Mark fixes computers.", "answer": True,
              "translation": "O Mark conserta computadores."},
             {"text": "Mark watches TV with his wife.", "answer": False,
              "translation": "O Mark assiste TV com a esposa dele."},
         ]},
    ],
}

AULA8_SPEAKING = {
    "title": "Speaking — wake up, wakes up",
    "lesson": 8,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: GOES = \"gôuz\" (junte tudo, não fale \"go-es\") · WATCHES = \"wó-tchiz\" · DOES = \"dâz\" · HAS = \"rréz\".",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat: I / he.",
         "translation": "Ouça e repita os pares: I (sem S) / he, she (com S).",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula8-say-v{i}.m4a"} for i, t in enumerate(
             ["wake up — wakes up", "watch — watches", "go — goes", "do — does", "study — studies", "have — has",
              "finish — finishes"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences from the lesson.",
         "translation": "Ouça e repita as frases da aula.",
         "example": "\"He wakes up at 7.\" (Ele acorda às 7.)",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula8-say-s{i}.m4a"} for i, t in enumerate(
             ["He wakes up at seven.", "She takes a shower every day.", "He watches TV at night.",
              "She goes to bed at 11 p.m.", "She studies English twice a week.", "She has breakfast at 8 a.m.",
              "He goes to the gym every day.", "She always does her homework."], 1)]},
        {"type": "speak",
         "prompt": "Answer the questions about YOUR routine. Listen to the question, then record your answer.",
         "translation": "Responda às perguntas sobre a SUA rotina. Ouça a pergunta e grave a sua resposta.",
         "example": "What time do you wake up? → \"I wake up at 6:30.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula8-say-q{i}.m4a"} for i, t in enumerate(
             ["What time do you wake up?", "What time do you go to bed?", "What do you do in the afternoon?"], 1)]},
    ],
}

AULA8_READING = {
    "title": "Reading — Laura's day",
    "lesson": 8,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto. Repare no S dos verbos!",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text about Laura.",
         "translation": "Leia e ouça o texto sobre a Laura. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula8-reading.m4a",
         "text": "LAURA'S DAY\n\n"
                 "This is Laura. She is a nurse and she works at a hospital in São Paulo.\n"
                 "First, she wakes up at 5:30 a.m. and takes a shower. Then she has breakfast with her husband, Pedro. "
                 "She starts work at 7 a.m.\n"
                 "After that, she has lunch at the hospital at noon. She finishes work at 3 p.m.\n"
                 "In the afternoon, she studies English. She goes to the gym at 6 p.m.\n"
                 "Finally, she watches TV with Pedro and goes to bed at 10 p.m.\n"
                 "Pedro fixes cars. He wakes up at 7 a.m. and goes to bed at midnight!"},
        {"type": "order",
         "prompt": "Put Laura's day in order.",
         "translation": "Coloque o dia da Laura em ordem.",
         "example": "wakes up → takes a shower → …",
         "tokens": ["wakes up", "has breakfast", "starts work", "has lunch", "studies English", "goes to the gym",
                    "goes to bed"], "alternatives": []},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Laura is a nurse. → True",
         "statements": [
             {"text": "Laura has breakfast with Pedro.", "answer": True,
              "translation": "A Laura toma café da manhã com o Pedro."},
             {"text": "Laura finishes work at 5 p.m.", "answer": False,
              "translation": "A Laura termina o trabalho às 5 da tarde."},
             {"text": "Laura studies English in the afternoon.", "answer": True,
              "translation": "A Laura estuda inglês à tarde."},
             {"text": "Pedro fixes computers.", "answer": False,
              "translation": "O Pedro conserta computadores."},
         ]},
        {"type": "fill",
         "prompt": "Complete with information from the text.",
         "translation": "Complete com as informações do texto.",
         "example": "Laura wakes up at [5:30].",
         "text": "1. Laura starts work at [7|7 a.m.|7:00|7:00 a.m.].\n"
                 "2. She goes to the gym at [6|6 p.m.|6:00|6:00 p.m.].\n"
                 "3. Pedro wakes up at [7|7 a.m.|7:00|7:00 a.m.].\n"
                 "4. Pedro goes to bed at [midnight|12|12 a.m.|12:00]."},
    ],
}

AULA8_WRITING = {
    "title": "Writing — someone's routine",
    "lesson": 8,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Primeiro passe frases de I para HE/SHE e depois escreva sobre a rotina de outra pessoa.\n"
                   "Lembre: he/she + verbo com S (wakes up, goes, has, studies, watches).",
    "topic": AULA8_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Rewrite the sentences with SHE.",
         "translation": "Reescreva as frases com SHE (ela).",
         "example": "I wake up at 6. → She wakes up at 6.",
         "text": "1. I take a shower at 7. → [She takes a shower at 7.]\n"
                 "2. I go to bed at 11 p.m. → [She goes to bed at 11 p.m.|She goes to bed at 11pm.]\n"
                 "3. I have lunch at noon. → [She has lunch at noon.]\n"
                 "4. I watch TV at night. → [She watches TV at night.|She watches TV at night]\n"
                 "5. I study English every day. → [She studies English every day.|She studies English everyday.]"},
        {"type": "fill",
         "prompt": "Write the sentences in English.",
         "translation": "Escreva as frases em inglês.",
         "example": "Ele acorda às 7. → He wakes up at 7.",
         "text": "1. Ele vai à academia todo dia. → [He goes to the gym every day.|He goes to the gym everyday.]\n"
                 "2. Ela toma café da manhã às 8. → [She has breakfast at 8.|She has breakfast at 8 a.m.|She has breakfast at eight.]\n"
                 "3. Eles assistem TV todo dia. → [They watch TV every day.|They watch TV everyday.]"},
        {"type": "free",
         "prompt": "Write about the routine of a person in your family or a friend (5 to 7 sentences). "
                   "Use he or she, times (at…) and first, then, after that, finally.",
         "translation": "Escreva sobre a rotina de uma pessoa da sua família ou de um amigo (5 a 7 frases). "
                        "Use he ou she, horários (at…) e first, then, after that, finally.",
         "example": "This is my father, Carlos. First, he wakes up at 6 a.m.",
         "model_answer": "This is my mother, Rosa. First, she wakes up at 6 a.m. Then she takes a shower and has breakfast.\n"
                         "After that, she goes to work at 7:30. She has lunch at noon and finishes work at 5 p.m.\n"
                         "At night, she watches TV. Finally, she goes to bed at 10 p.m.",
         "keywords": ["wakes up", "has", "goes", "then", "finally"], "min_words": 25, "points": 4},
    ],
}

# ---------- Aula 09 — Jobs (https://youtu.be/6yjyY3IGGYQ) ----------

AULA9_TOPIC = "Aula 09 — Jobs"

AULA9_JOBS = {
    "title": "Jobs",
    "lesson": 9,
    "description": "As profissões (jobs / professions) da aula. A maioria serve para homem e mulher (teacher = professor ou professora).\n"
                   "Exceções: waiter (garçom) → waitress (garçonete) · actor (ator) → actress (atriz).",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the jobs to Portuguese.",
         "translation": "Ligue as profissões ao português.",
         "example": "doctor → médico(a)",
         "pairs": [
             {"left": "nurse", "right": "enfermeiro(a)"},
             {"left": "lawyer", "right": "advogado(a)"},
             {"left": "engineer", "right": "engenheiro(a)"},
             {"left": "accountant", "right": "contador(a)"},
             {"left": "cleaner", "right": "faxineiro(a)"},
             {"left": "police officer", "right": "policial"},
             {"left": "firefighter", "right": "bombeiro(a)"},
             {"left": "flight attendant", "right": "comissário(a) de bordo"},
         ]},
        {"type": "match",
         "prompt": "Match more jobs to Portuguese.",
         "translation": "Ligue mais profissões ao português.",
         "example": "teacher → professor(a)",
         "pairs": [
             {"left": "vet", "right": "veterinário(a)"},
             {"left": "hairdresser", "right": "cabeleireiro(a)"},
             {"left": "salesperson", "right": "vendedor(a)"},
             {"left": "singer", "right": "cantor(a)"},
             {"left": "musician", "right": "músico(a)"},
             {"left": "taxi driver", "right": "taxista"},
             {"left": "chef", "right": "chefe de cozinha"},
             {"left": "journalist", "right": "jornalista"},
         ]},
        {"type": "dropdown",
         "prompt": "Who is it? Choose the job.",
         "translation": "Quem é? Escolha a profissão de acordo com a descrição.",
         "example": "She flies planes. → [pilot]",
         "text": "1. She works in a hospital and helps the doctors. → [*nurse|chef|lawyer]\n"
                 "2. He cooks in a restaurant. → [*chef|waiter|dentist]\n"
                 "3. She takes care of animals. → [*vet|model|singer]\n"
                 "4. He drives a taxi. → [*taxi driver|pilot|cleaner]\n"
                 "5. She cuts hair. → [*hairdresser|accountant|receptionist]\n"
                 "6. He works at the reception of a hotel. → [*receptionist|firefighter|journalist]"},
        {"type": "choice",
         "prompt": "The woman who serves food in a restaurant is a…",
         "translation": "A mulher que serve a comida no restaurante é uma… (garçonete)",
         "options": ["waitress", "waiter", "actress", "chef"], "correct": 0},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Teacher\" is for men and women. → True",
         "statements": [
             {"text": "\"Doctor\" is for men and women.", "answer": True,
              "translation": "\"Doctor\" serve para homens e mulheres."},
             {"text": "\"Actress\" is the word for a man.", "answer": False,
              "translation": "\"Actress\" é a palavra para um homem."},
             {"text": "In \"police officer\", the strong part of \"police\" is \"LICE\": po-LICE.", "answer": True,
              "translation": "Em \"police officer\", a parte forte de \"police\" é \"LICE\": po-LICE (como em polícia)."},
             {"text": "A \"cleaner\" works in a hospital as a doctor.", "answer": False,
              "translation": "Um \"cleaner\" trabalha num hospital como médico."},
         ]},
    ],
}

AULA9_WHAT_DO_YOU_DO = {
    "title": "What do you do? — a / an",
    "lesson": 9,
    "description": "Para perguntar a profissão: WHAT DO YOU DO? (O que você faz?)\n"
                   "Resposta: I'm A teacher. · I'm AN engineer.\n"
                   "• Em inglês SEMPRE usamos a / an antes da profissão (\"eu sou UMA professora\").\n"
                   "• AN antes de som de vogal: an engineer, an architect, an accountant, an actor.\n"
                   "Revisão do present simple: he/she + S → works, goes, fixes, studies, plays, stays, has.",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "A or AN?",
         "translation": "A ou AN? (AN antes de som de vogal: a, e, i, o, u)",
         "example": "I'm [an] engineer. · I'm [a] teacher.",
         "text": "1. I'm [*a|an] doctor.\n"
                 "2. She's [*an|a] accountant.\n"
                 "3. He's [*an|a] actor.\n"
                 "4. I'm [*a|an] nurse.\n"
                 "5. He's [*an|a] architect.\n"
                 "6. She's [*a|an] lawyer."},
        {"type": "fill",
         "prompt": "What do you do? Answer with I'm a / I'm an + the job.",
         "translation": "O que você faz? Responda com I'm a / I'm an + a profissão.",
         "example": "(professora) → I'm a teacher.",
         "text": "1. (engenheiro) → [I'm an engineer.|I am an engineer.]\n"
                 "2. (piloto) → [I'm a pilot.|I am a pilot.]\n"
                 "3. (dentista) → [I'm a dentist.|I am a dentist.]\n"
                 "4. (contadora) → [I'm an accountant.|I am an accountant.]\n"
                 "5. (cantor) → [I'm a singer.|I am a singer.]"},
        {"type": "group",
         "prompt": "How do we write the verb with he / she? Put the verbs in the correct group.",
         "translation": "Revisão: como fica o verbo com he / she? Coloque os verbos no grupo certo.",
         "example": "play → plays (vogal + Y: só acrescenta S) → \"+ S\"",
         "categories": ["+ S", "+ ES", "Y → IES", "have → has"],
         "words": [
             {"text": "work", "category": "+ S"}, {"text": "like", "category": "+ S"},
             {"text": "play", "category": "+ S"}, {"text": "stay", "category": "+ S"},
             {"text": "wash", "category": "+ ES"}, {"text": "kiss", "category": "+ ES"},
             {"text": "go", "category": "+ ES"}, {"text": "fix", "category": "+ ES"},
             {"text": "fly", "category": "Y → IES"}, {"text": "study", "category": "Y → IES"},
             {"text": "have", "category": "have → has"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the correct form of the verb.",
         "translation": "Escolha a forma correta do verbo.",
         "example": "She [works] as a teacher.",
         "text": "1. She [*works|work] as a teacher in a school near here.\n"
                 "2. He [*goes|go] to work by car.\n"
                 "3. She [*has|haves] special qualifications.\n"
                 "4. I [*work|works] for a big company.\n"
                 "5. They [*wear|wears] a uniform at work.\n"
                 "6. He [*plays|plaies] soccer on Saturdays.\n"
                 "7. She [*stays|staies] home on the weekends."},
        {"type": "truefalse",
         "prompt": "True or false?",
         "translation": "Verdadeiro ou falso?",
         "example": "\"What do you do?\" asks about your job. → True",
         "statements": [
             {"text": "\"What do you do?\" asks about your job.", "answer": True,
              "translation": "\"What do you do?\" pergunta sobre a sua profissão."},
             {"text": "\"I'm teacher.\" is correct.", "answer": False,
              "translation": "\"I'm teacher.\" está correto."},
             {"text": "We say \"an engineer\" because \"engineer\" starts with a vowel sound.", "answer": True,
              "translation": "Dizemos \"an engineer\" porque \"engineer\" começa com som de vogal."},
             {"text": "We use the present simple for routines and facts: \"I like chocolate.\"", "answer": True,
              "translation": "Usamos o present simple para rotinas e fatos: \"Eu gosto de chocolate.\""},
         ]},
    ],
}

AULA9_LISTENING = {
    "title": "Listening — what do they do?",
    "lesson": 9,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the job you hear.",
         "translation": "Ouça e escolha a profissão que você ouvir.",
         "example": "Você ouve: \"nurse\" → escolha nurse.",
         "audio": f"{AUDIO}/aula9-jobs.m4a",
         "text": "1. [*lawyer|engineer|singer]   2. [*musician|accountant|journalist]   3. [*waitress|waiter|actress]\n"
                 "4. [*firefighter|flight attendant|hairdresser]   5. [*vet|chef|dentist]   6. [*actress|actor|waitress]"},
        {"type": "fill",
         "prompt": "Dictation: listen and write the job.",
         "translation": "Ditado: ouça e escreva a profissão.",
         "example": "Você ouve: \"I'm a doctor.\" → I'm a [doctor].",
         "audio": f"{AUDIO}/aula9-dictation.m4a",
         "text": "1. I'm a [teacher].\n"
                 "2. She's a [nurse].\n"
                 "3. He's a [pilot].\n"
                 "4. I'm a [dentist].\n"
                 "5. She's a [singer]."},
        {"type": "info",
         "prompt": "Now listen to Tom at a party. He meets three people.",
         "translation": "Agora ouça o Tom numa festa. Ele conhece três pessoas. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula9-party.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again. What do they do?",
         "translation": "Ouça de novo. Qual é a profissão de cada um?",
         "example": "Tom → [engineer]",
         "text": "1. Sophie → [*flight attendant|nurse|teacher]\n"
                 "2. Ryan → [*chef|waiter|police officer]\n"
                 "3. Grace → [*lawyer|accountant|journalist]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the audio.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o áudio.",
         "example": "Tom is an engineer. → True",
         "statements": [
             {"text": "Sophie flies to London every week.", "answer": True,
              "translation": "A Sophie voa para Londres toda semana."},
             {"text": "Ryan works in a hospital.", "answer": False,
              "translation": "O Ryan trabalha num hospital."},
             {"text": "Grace works from home.", "answer": True,
              "translation": "A Grace trabalha de casa."},
         ]},
    ],
}

AULA9_SPEAKING = {
    "title": "Speaking — jobs",
    "lesson": 9,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar. "
                   "A aula sugere repetir cada palavra 3 vezes!\n"
                   "Dicas da aula: POLICE = \"po-LÍCE\" (forte no final, como em polícia) · MUSICIAN = \"miu-ZI-shan\" · "
                   "AN ENGINEER: junte o N com a vogal — \"a-nen-dji-NIR\".",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the jobs.",
         "translation": "Ouça e repita as profissões.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula9-say-j{i}.m4a"} for i, t in enumerate(
             ["doctor", "teacher", "nurse", "lawyer", "engineer", "accountant", "police officer", "musician",
              "firefighter", "flight attendant", "hairdresser", "receptionist"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the question and the answers.",
         "translation": "Ouça e repita a pergunta e as respostas.",
         "example": "\"What do you do?\" — \"I'm a teacher.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula9-say-q{i}.m4a"} for i, t in enumerate(
             ["What do you do?", "I'm a teacher.", "I'm an engineer.", "I'm an accountant.",
              "She works as a teacher in a school near here.", "He goes to work by car.", "I work for a big company.",
              "They wear a uniform at work."], 1)]},
        {"type": "speak",
         "prompt": "Now answer about YOU: What do you do?",
         "translation": "Agora responda sobre VOCÊ: o que você faz? Ouça a pergunta e grave a sua resposta "
                        "(se precisar, procure a sua profissão no dicionário).",
         "example": "\"I'm a salesperson. I work for a big company. I go to work by bus.\"",
         "phrases": [{"text": "What do you do?", "audio": f"{AUDIO}/aula9-say-q1.m4a"},
                     {"text": "How do you go to work?", "audio": f"{AUDIO}/aula9-say-q9.m4a"}]},
    ],
}

AULA9_READING = {
    "title": "Reading — my neighbors",
    "lesson": 9,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Bruno's text about his neighbors.",
         "translation": "Leia e ouça o texto do Bruno sobre os vizinhos dele. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula9-reading.m4a",
         "text": "MY NEIGHBORS — by Bruno\n\n"
                 "I'm Bruno and I'm a musician. I play the guitar in a band and I work at night.\n"
                 "My neighbor Helen is a pilot. She flies to Europe every month and she has a big house.\n"
                 "Mr. Costa is a police officer. He wears a uniform at work and he goes to work by bus.\n"
                 "Daniel and Paula are vets. They have a small clinic near here. Daniel fixes old cars on the weekends.\n"
                 "And Mrs. Lima? She is a teacher, but now she stays home and studies Italian!"},
        {"type": "match",
         "prompt": "Match the people to their jobs.",
         "translation": "Ligue as pessoas às profissões delas.",
         "example": "Bruno → musician",
         "pairs": [
             {"left": "Helen", "right": "pilot"},
             {"left": "Mr. Costa", "right": "police officer"},
             {"left": "Daniel and Paula", "right": "vets"},
             {"left": "Mrs. Lima", "right": "teacher"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Bruno plays the guitar. → True",
         "statements": [
             {"text": "Bruno works in the morning.", "answer": False,
              "translation": "O Bruno trabalha de manhã."},
             {"text": "Helen flies to Europe every month.", "answer": True,
              "translation": "A Helen voa para a Europa todo mês."},
             {"text": "Mr. Costa goes to work by car.", "answer": False,
              "translation": "O Sr. Costa vai para o trabalho de carro."},
             {"text": "Mrs. Lima studies Italian.", "answer": True,
              "translation": "A Sra. Lima estuda italiano."},
         ]},
        {"type": "fill",
         "prompt": "Complete with the verbs from the text.",
         "translation": "Complete com os verbos do texto (atenção ao S!).",
         "example": "Bruno: \"I [play] the guitar.\"",
         "text": "1. Helen [has] a big house.\n"
                 "2. Mr. Costa [wears] a uniform at work.\n"
                 "3. Daniel [fixes] old cars on the weekends.\n"
                 "4. Mrs. Lima [stays] home."},
    ],
}

AULA9_WRITING = {
    "title": "Writing — my job",
    "lesson": 9,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Traduza as frases e depois escreva sobre o seu trabalho e o de alguém que você conhece.\n"
                   "Lembre: I'm A teacher / I'm AN engineer · he/she + verbo com S.",
    "topic": AULA9_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the sentences in English.",
         "translation": "Escreva as frases em inglês.",
         "example": "Ela é enfermeira. → She's a nurse.",
         "text": "1. O que você faz? → [What do you do?]\n"
                 "2. Eu sou advogado. → [I'm a lawyer.|I am a lawyer.]\n"
                 "3. Ele é engenheiro. → [He's an engineer.|He is an engineer.]\n"
                 "4. Ela trabalha para uma empresa grande. → [She works for a big company.]\n"
                 "5. Eu vou para o trabalho de ônibus. → [I go to work by bus.]"},
        {"type": "fill",
         "prompt": "Rewrite the sentences with HE.",
         "translation": "Reescreva as frases com HE (ele).",
         "example": "I work at a hospital. → He works at a hospital.",
         "text": "1. I fix computers. → [He fixes computers.]\n"
                 "2. I play the guitar. → [He plays the guitar.]\n"
                 "3. I have a car. → [He has a car.]"},
        {"type": "free",
         "prompt": "What do you do? Write about your job (or your studies) and the job of a person in your family (5 to 7 sentences).",
         "translation": "O que você faz? Escreva sobre o seu trabalho (ou os seus estudos) e a profissão de alguém da sua família (5 a 7 frases).",
         "example": "I'm a salesperson. I work for a big company. My sister is a nurse. She works at a hospital.",
         "model_answer": "I'm a salesperson. I work for a big company in São Paulo. I go to work by bus.\n"
                         "My sister is a nurse. She works at a hospital near here. She goes to work by car.\n"
                         "She wears a uniform at work.",
         "keywords": ["I'm", "work", "works", "goes"], "min_words": 25, "points": 4},
    ],
}

# ---------- Aula 10 — Present Simple (negative) (https://youtu.be/LazzJ2Xmfwk) ----------

AULA10_TOPIC = "Aula 10 — Present Simple (negative)"

AULA10_VOCAB = {
    "title": "Food, drinks and verb phrases",
    "lesson": 10,
    "description": "O vocabulário da aula: comidas e bebidas (food & drinks) e expressões com verbos (verb phrases).\n"
                   "Dica da aula: memorize em blocos! say sorry (pedir desculpas) · have a picnic (fazer um piquenique) · "
                   "wear glasses (usar óculos — WEAR é para o que vai no corpo) · listen TO music · go to the movies (ir ao cinema).\n"
                   "housework (tarefas de limpeza da casa) ≠ homework (dever de casa).",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the food and drinks to Portuguese.",
         "translation": "Ligue as comidas e bebidas ao português.",
         "example": "cake → bolo",
         "pairs": [
             {"left": "cheese", "right": "queijo"},
             {"left": "ice cream", "right": "sorvete"},
             {"left": "soup", "right": "sopa"},
             {"left": "salad", "right": "salada"},
             {"left": "tea", "right": "chá"},
             {"left": "milk", "right": "leite"},
             {"left": "juice", "right": "suco"},
             {"left": "hot dog", "right": "cachorro-quente"},
         ]},
        {"type": "group",
         "prompt": "Which verb goes with each word? Put the words in the correct group.",
         "translation": "Qual verbo combina com cada palavra? Coloque as palavras no grupo certo.",
         "example": "the guitar → play (play the guitar = tocar violão)",
         "categories": ["do", "play", "have", "drink"],
         "words": [
             {"text": "housework", "category": "do"}, {"text": "homework", "category": "do"},
             {"text": "exercise", "category": "do"},
             {"text": "tennis", "category": "play"}, {"text": "the guitar", "category": "play"},
             {"text": "a picnic", "category": "have"}, {"text": "a pet", "category": "have"},
             {"text": "water", "category": "drink"}, {"text": "a coffee", "category": "drink"},
         ]},
        {"type": "dropdown",
         "prompt": "Complete the verb phrases.",
         "translation": "Complete as expressões com o verbo correto.",
         "example": "[read] a book (ler um livro)",
         "text": "1. [*live|work|meet] in a flat (morar num apartamento)\n"
                 "2. [*listen|watch|say] to music (ouvir música)\n"
                 "3. [*go|play|do] to the movies (ir ao cinema)\n"
                 "4. [*say|speak|meet] sorry (pedir desculpas)\n"
                 "5. [*wear|use|play] glasses (usar óculos)\n"
                 "6. [*meet|need|speak] friends (encontrar amigos)\n"
                 "7. [*cook|eat|drive] dinner (fazer o jantar)\n"
                 "8. [*need|drive|wear] a new phone (precisar de um celular novo)"},
        {"type": "match",
         "prompt": "Match the verb phrases to Portuguese.",
         "translation": "Ligue as expressões ao português.",
         "example": "study math → estudar matemática",
         "pairs": [
             {"left": "work in an office", "right": "trabalhar num escritório"},
             {"left": "speak English", "right": "falar inglês"},
             {"left": "eat vegetables", "right": "comer legumes e verduras"},
             {"left": "drive a car", "right": "dirigir um carro"},
             {"left": "do housework", "right": "fazer as tarefas de casa (limpeza)"},
             {"left": "do homework", "right": "fazer o dever de casa"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Think about the pronunciation tips from the lesson.",
         "translation": "Verdadeiro ou falso? Pense nas dicas de pronúncia da aula.",
         "example": "In \"cake\", the final E is silent. → True",
         "statements": [
             {"text": "\"Chocolate\" sounds like two syllables: \"CHOC-lit\".", "answer": True,
              "translation": "\"Chocolate\" soa como duas sílabas: \"CHÓC-lit\"."},
             {"text": "We say \"milky\", with an \"i\" sound at the end.", "answer": False,
              "translation": "Falamos \"milki\", com som de \"i\" no final."},
             {"text": "In \"juice\", the letter I is silent.", "answer": True,
              "translation": "Em \"juice\", a letra I é muda."},
             {"text": "In \"listen\", we pronounce the letter T.", "answer": False,
              "translation": "Em \"listen\", pronunciamos a letra T."},
             {"text": "To say \"usar óculos\" in English, we use the verb \"wear\".", "answer": True,
              "translation": "Para dizer \"usar óculos\" em inglês, usamos o verbo \"wear\"."},
         ]},
    ],
}

AULA10_NEGATIVE = {
    "title": "Don't and doesn't",
    "lesson": 10,
    "description": "Para negar no present simple usamos o verbo auxiliar DO / DOES + NOT:\n"
                   "• I, you, we, they → DON'T (do not): I don't like soup.\n"
                   "• He, she, it → DOESN'T (does not): She doesn't like salad.\n"
                   "• O S aparece UMA vez só: no doesn't. O verbo volta para a forma básica: "
                   "she likes → she doesn't like (NÃO \"doesn't likes\").\n"
                   "• Não dá para usar só not: \"I not like pizza\" está errado → I don't like pizza.",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Don't or doesn't?",
         "translation": "Don't ou doesn't? Olhe o sujeito da frase!",
         "example": "She [doesn't] like salad.",
         "text": "1. I [*don't|doesn't] like soup.\n"
                 "2. He [*doesn't|don't] live in a flat.\n"
                 "3. We [*don't|doesn't] have a pet.\n"
                 "4. Alice and John [*don't|doesn't] eat vegetables.\n"
                 "5. Your dog [*doesn't|don't] drink much water.\n"
                 "6. They [*don't|doesn't] go to bed early.\n"
                 "7. My mother [*doesn't|don't] work in an office."},
        {"type": "fill",
         "prompt": "Write the sentences in the negative.",
         "translation": "Escreva as frases no negativo.",
         "example": "I like juice. → I don't like juice.",
         "text": "1. They like pizza. → [They don't like pizza.|They do not like pizza.]\n"
                 "2. He likes cheese. → [He doesn't like cheese.|He does not like cheese.]\n"
                 "3. I wake up at 10 a.m. → [I don't wake up at 10 a.m.|I do not wake up at 10 a.m.|I don't wake up at 10am.|I don't wake up at 10.]\n"
                 "4. She studies English. → [She doesn't study English.|She does not study English.]\n"
                 "5. We watch TV. → [We don't watch TV.|We do not watch TV.]"},
        {"type": "fill",
         "prompt": "Complete with ONE word: do, does, don't, doesn't or not.",
         "translation": "Complete com UMA palavra só: do, does, don't, doesn't ou not.",
         "example": "She does [not] have breakfast.",
         "text": "1. She [does] not have breakfast.\n"
                 "2. She [doesn't] go to bed early.\n"
                 "3. I [don't] study French. I study English.\n"
                 "4. I do [not] like pizza.\n"
                 "5. He [doesn't] play the guitar."},
        {"type": "truefalse",
         "prompt": "Is this sentence correct? Choose True (correct) or False (incorrect).",
         "translation": "Esta frase está correta? Escolha True (correta) ou False (errada).",
         "example": "\"I don't like pizza.\" → True",
         "statements": [
             {"text": "I not like pizza.", "answer": False,
              "translation": "Eu não gosto de pizza."},
             {"text": "She like ice cream.", "answer": False,
              "translation": "Ela gosta de sorvete."},
             {"text": "He doesn't like sushi.", "answer": True,
              "translation": "Ele não gosta de sushi."},
             {"text": "She doesn't likes coffee.", "answer": False,
              "translation": "Ela não gosta de café."},
             {"text": "We don't drink milk.", "answer": True,
              "translation": "Nós não bebemos leite."},
         ]},
        {"type": "choice",
         "prompt": "What is the correct form of \"She doesn't likes coffee\"?",
         "translation": "Qual é a forma correta de \"She doesn't likes coffee\"?",
         "options": ["She doesn't like coffee.", "She don't like coffee.", "She not likes coffee.", "She doesn't likes coffees."],
         "correct": 0},
    ],
}

AULA10_LISTENING = {
    "title": "Listening — likes and dislikes",
    "lesson": 10,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Atenção: DON'T (dônt) ≠ DOESN'T (dâzunt).",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen. Do they like it or not? Choose.",
         "translation": "Ouça. Gosta ou não gosta? Escolha o que você ouvir.",
         "example": "Você ouve: \"I don't like soup.\" → don't like",
         "audio": f"{AUDIO}/aula10-likes.m4a",
         "text": "1. I [*like|don't like] sushi.\n"
                 "2. He [*doesn't like|likes] bacon.\n"
                 "3. We [*don't like|like] coffee.\n"
                 "4. She [*likes|doesn't like] cake.\n"
                 "5. They [*don't like|like] tea."},
        {"type": "fill",
         "prompt": "Dictation: listen and write the food or drink.",
         "translation": "Ditado: ouça e escreva a comida ou bebida.",
         "example": "Você ouve: \"cake\" → cake",
         "audio": f"{AUDIO}/aula10-dictation.m4a",
         "text": "1. [cheese]   2. [juice]   3. [milk]   4. [soup]   5. [coffee]   6. [salad]"},
        {"type": "info",
         "prompt": "Now listen to Kate and Leo. They plan a picnic.",
         "translation": "Agora ouça a Kate e o Leo. Eles estão planejando um piquenique. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula10-picnic.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and complete.",
         "translation": "Ouça de novo e complete.",
         "example": "Leo [likes] sandwiches.",
         "text": "1. Kate [*doesn't like|likes] cheese.\n"
                 "2. Leo [*doesn't drink|drinks] coffee.\n"
                 "3. Kate [*likes|doesn't like] juice.\n"
                 "4. Leo [*doesn't eat|eats] chocolate."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the audio.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o áudio.",
         "example": "Kate and Leo plan a picnic. → True",
         "statements": [
             {"text": "Leo drinks tea.", "answer": True,
              "translation": "O Leo bebe chá."},
             {"text": "Kate doesn't like cake.", "answer": False,
              "translation": "A Kate não gosta de bolo."},
             {"text": "Leo wears glasses.", "answer": False,
              "translation": "O Leo usa óculos."},
         ]},
    ],
}

AULA10_SPEAKING = {
    "title": "Speaking — I don't like…",
    "lesson": 10,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: termine no som da consoante, sem colocar \"i\" no final — CAKE (não \"keiki\"), MILK (não \"milki\") · "
                   "CHOCOLATE = \"CHÓC-lit\" · JUICE = \"djuuss\" · LISTEN = \"LÍS-sen\" (T mudo) · VEGETABLES = \"VÉDJ-ta-buls\".",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the food and drinks.",
         "translation": "Ouça e repita as comidas e bebidas.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula10-say-f{i}.m4a"} for i, t in enumerate(
             ["chocolate", "cake", "cheese", "ice cream", "soup", "tea", "coffee", "milk", "juice", "vegetables"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases.",
         "example": "\"I like sushi. I don't like soup.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula10-say-s{i}.m4a"} for i, t in enumerate(
             ["I like sushi. I don't like soup.", "He likes pizza. He doesn't like salad.",
              "She likes hot dog. She doesn't like salad.", "I don't go to the movies on Monday.", "We don't have a pet.",
              "He doesn't live in a flat.", "She doesn't work in an office.", "I listen to music every day."], 1)]},
        {"type": "speak",
         "prompt": "Now talk about YOU: say what you like and what you don't like.",
         "translation": "Agora fale sobre VOCÊ: diga do que você gosta e do que não gosta. Faça frases verdadeiras!",
         "example": "\"I like tea and milk. I don't like coffee.\"",
         "phrases": [{"text": "Say the food you like and the food you don't like.", "audio": f"{AUDIO}/aula10-say-q1.m4a"},
                     {"text": "Make true sentences: live in an apartment · cook dinner every day · play the guitar",
                      "audio": f"{AUDIO}/aula10-say-q2.m4a"}]},
    ],
}

AULA10_READING = {
    "title": "Reading — two roommates",
    "lesson": 10,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Bia's text about her roommate.",
         "translation": "Leia e ouça o texto da Bia sobre a colega de apartamento dela. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula10-reading.m4a",
         "text": "MY ROOMMATE AND I — by Bia\n\n"
                 "I live in a flat in Curitiba with my friend Nina. We are very different!\n"
                 "I work in an office and I drive a car. Nina doesn't drive. She goes to work by bus.\n"
                 "I love coffee, but Nina doesn't drink coffee. She drinks tea and juice.\n"
                 "Nina cooks dinner every day. I don't cook — I do the housework!\n"
                 "She eats vegetables and salad. I don't like salad, I like pizza and hot dogs.\n"
                 "We don't have a pet, but we have a picnic in the park every Sunday."},
        {"type": "group",
         "prompt": "Who does it? Put each phrase in the correct group.",
         "translation": "Quem faz isso? Coloque cada expressão no grupo certo: Bia, Nina ou as duas (both).",
         "example": "drives a car → Bia",
         "categories": ["Bia", "Nina", "both"],
         "words": [
             {"text": "works in an office", "category": "Bia"}, {"text": "drinks coffee", "category": "Bia"},
             {"text": "does the housework", "category": "Bia"},
             {"text": "goes to work by bus", "category": "Nina"}, {"text": "cooks dinner", "category": "Nina"},
             {"text": "eats salad", "category": "Nina"},
             {"text": "live in a flat", "category": "both"}, {"text": "have a picnic on Sundays", "category": "both"},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Bia drives a car. → True",
         "statements": [
             {"text": "Nina drinks coffee.", "answer": False,
              "translation": "A Nina bebe café."},
             {"text": "Bia doesn't cook.", "answer": True,
              "translation": "A Bia não cozinha."},
             {"text": "Bia doesn't like pizza.", "answer": False,
              "translation": "A Bia não gosta de pizza."},
             {"text": "They don't have a pet.", "answer": True,
              "translation": "Elas não têm um animal de estimação."},
         ]},
        {"type": "dropdown",
         "prompt": "Complete according to the text.",
         "translation": "Complete de acordo com o texto.",
         "example": "Nina [doesn't drive].",
         "text": "1. Nina [*doesn't drink|drinks] coffee.\n"
                 "2. Bia [*doesn't like|likes] salad.\n"
                 "3. Nina [*cooks|doesn't cook] dinner every day.\n"
                 "4. Bia [*works|doesn't work] in an office."},
    ],
}

AULA10_WRITING = {
    "title": "Writing — true for me",
    "lesson": 10,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Como a aula sugere: faça frases que sejam VERDADEIRAS para você, no afirmativo ou no negativo.\n"
                   "Lembre: I / you / we / they → don't · he / she / it → doesn't + verbo SEM S.",
    "topic": AULA10_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the sentences in English.",
         "translation": "Escreva as frases em inglês.",
         "example": "Eu não gosto de sopa. → I don't like soup.",
         "text": "1. Eu não bebo café. → [I don't drink coffee.|I do not drink coffee.]\n"
                 "2. Ela não gosta de queijo. → [She doesn't like cheese.|She does not like cheese.]\n"
                 "3. Nós não temos um pet. → [We don't have a pet.|We do not have a pet.]\n"
                 "4. Ele não usa óculos. → [He doesn't wear glasses.|He does not wear glasses.]\n"
                 "5. Eles não comem legumes. → [They don't eat vegetables.|They do not eat vegetables.]"},
        {"type": "fill",
         "prompt": "Correct the sentences.",
         "translation": "Corrija as frases (todas têm um erro).",
         "example": "I not like pizza. → I don't like pizza.",
         "text": "1. She doesn't likes coffee. → [She doesn't like coffee.|She does not like coffee.]\n"
                 "2. He don't play tennis. → [He doesn't play tennis.|He does not play tennis.]\n"
                 "3. I no speak French. → [I don't speak French.|I do not speak French.]"},
        {"type": "free",
         "prompt": "Write 6 to 8 TRUE sentences about you and a person you know: food and drinks you like and don't like, "
                   "and things you do and don't do (live in an apartment, cook dinner, play the guitar, wear glasses…).",
         "translation": "Escreva de 6 a 8 frases VERDADEIRAS sobre você e uma pessoa que você conhece: comidas e bebidas de que gostam "
                        "e não gostam, e coisas que fazem e não fazem (morar em apartamento, cozinhar, tocar violão, usar óculos…).",
         "example": "I like tea. I don't like coffee. My brother doesn't wear glasses.",
         "model_answer": "I like chocolate and ice cream, but I don't like soup.\n"
                         "I live in an apartment. I don't cook dinner every day.\n"
                         "My husband likes coffee. He doesn't drink tea.\n"
                         "He plays the guitar, but he doesn't speak English.",
         "keywords": ["like", "don't", "doesn't"], "min_words": 30, "points": 4},
    ],
}

# ---------- Aula 09 — extra: interactive video ----------

AULA9_VIDEO = {
    "title": "Video — Ana's family",
    "lesson": 9,
    "subject": "Video",
    "description": "🎬 Atividade extra: assista ao vídeo da Ana apresentando a família e o que cada um faz. O vídeo pausa sozinho e faz uma pergunta; "
                   "responda e continue assistindo. Tente primeiro sem legenda!",
    "topic": AULA9_TOPIC,
    "items": [
        video_item("aula9-video", "Watch the video. Answer the questions when it stops.",
                   "Assista ao vídeo. Responda às perguntas quando ele pausar.", [
            {"question": "Ana is an…", "translation": "A Ana é…",
             "options": ["accountant", "engineer", "actress", "architect"], "correct": 0},
            {"question": "Paulo works at…", "translation": "O Paulo trabalha em…",
             "options": ["a big hospital", "a hotel", "a school", "an office"], "correct": 0},
            {"question": "Rosa goes to work…", "translation": "A Rosa vai para o trabalho…",
             "options": ["by bus", "by car", "by taxi", "by plane"], "correct": 0},
            {"question": "Bia is a pilot. She flies to…", "translation": "A Bia é piloto. Ela voa para…",
             "options": ["Europe", "Rio", "Canada", "Japan"], "correct": 0},
            {"question": "Leo plays…", "translation": "O Leo toca…",
             "options": ["the guitar", "the piano", "tennis", "soccer"], "correct": 0},
        ]),
    ],
}

# ---------- extra: one interactive video per lesson (deploy/videos.py + deploy/make_video.py) ----------

def _video(n, topic, title, description, name, questions):
    return {"title": title, "lesson": n, "subject": "Video", "topic": topic,
            "description": "🎬 Atividade extra: " + description + " O vídeo pausa sozinho e faz uma pergunta; responda e continue "
                           "assistindo. Tente primeiro sem legenda!",
            "items": [video_item(name, "Watch the video. Answer the questions when it stops.",
                                 "Assista ao vídeo. Responda às perguntas quando ele pausar.", questions)]}


def _q(question, translation, *options):
    """First option is the right one (the seed shuffles them)."""
    return {"question": question, "translation": translation, "options": list(options), "correct": 0}


AULA1_VIDEO = _video(1, "Aula 01 — Alphabet", "Video — At the coffee shop",
                     "na cafeteria, os clientes soletram o nome para o barista.", "aula1-video", [
    _q("Choose Kate's name.", "Escolha o nome que a Kate soletrou.", "KATE", "CATE", "KAIT", "KATTE"),
    _q("Choose Jeff's name.", "Escolha o nome que o Jeff soletrou.", "JEFF", "GEFF", "JEF", "GEF"),
    _q("Choose Grace's name.", "Escolha o nome que a Grace soletrou.", "GRACE", "JRACE", "GRASE", "GREICE"),
    _q("Grace: a coffee or a latte?", "A Grace pediu um café ou um latte?", "a latte", "a coffee", "a tea", "a juice"),
])
AULA2_VIDEO = _video(2, "Aula 02 — Classroom Language", "Video — My online English class",
                     "a aula online do Lucas, com as frases de sala de aula.", "aula2-video", [
    _q("What's the problem? The teacher says: \"Lucas, …\"", "Qual é o problema? A professora diz: \"Lucas, …\"",
       "you're muted.", "you're frozen.", "you're breaking up.", "I don't know."),
    _q("What does \"spoon\" mean?", "O que significa \"spoon\"?", "colher", "copo", "mesa", "caderno"),
    _q("How do you spell \"spoon\"?", "Como se soletra \"spoon\"?", "S-P-O-O-N", "S-P-O-N", "S-P-U-N", "E-S-P-O-O-N"),
    _q("Lucas: \"My internet connection is…\"", "Lucas: \"Minha conexão de internet está…\"",
       "slow today.", "fast today.", "good today.", "new today."),
])
AULA3_VIDEO = _video(3, "Aula 03 — Greetings", "Video — Hello from morning to night",
                     "cumprimentos de manhã, de tarde, à noite e na hora de dormir.", "aula3-video", [
    _q("It's 7 a.m. They say…", "São 7 da manhã. Eles dizem…", "Good morning!", "Good afternoon!", "Good evening!", "Good night!"),
    _q("\"Nice to meet you\" means…", "\"Nice to meet you\" significa…", "Prazer em te conhecer.", "Boa tarde.", "Até logo.",
       "Tudo bem?"),
    _q("8 p.m., arriving at a restaurant. We say…", "8 da noite, chegando a um restaurante. Dizemos…",
       "Good evening!", "Good night!", "Good morning!", "Good afternoon!"),
    _q("\"Good night\" is for…", "Usamos \"Good night\" para…", "going to bed or saying bye at night",
       "arriving at a party", "the morning", "the afternoon"),
])
AULA4_VIDEO = _video(4, "Aula 04 — Daily Routine", "Video — Sofia's routine",
                     "a Sofia conta a rotina dela, do despertador até a hora de dormir.", "aula4-video", [
    _q("Sofia: \"I wake up at…\"", "Sofia: \"Eu acordo às…\"", "6:30", "7:30", "5:30", "6:00"),
    _q("Sofia: \"First, I take a shower. Then I…\"", "Sofia: \"Primeiro, eu tomo banho. Depois eu…\"",
       "get dressed.", "go to bed.", "have lunch.", "go to the gym."),
    _q("Sofia: \"I have breakfast at…\"", "Sofia: \"Eu tomo café da manhã às…\"", "seven.", "six.", "eight.", "nine."),
    _q("Sofia: \"I start work at…\"", "Sofia: \"Eu começo a trabalhar às…\"", "eight.", "seven.", "nine.", "noon."),
    _q("Sofia: \"After work, I go to…\"", "Sofia: \"Depois do trabalho, eu vou…\"", "the gym.", "bed.", "school.", "the beach."),
])
AULA5_VIDEO = _video(5, "Aula 05 — Numbers", "Video — Nice to meet you, Lily!",
                     "o Tom conhece a Lily: idade, telefone e horário.", "aula5-video", [
    _q("Lily: \"I'm … years old.\"", "Lily: \"Eu tenho … anos.\"", "23", "25", "33", "32"),
    _q("Lily's phone number:", "O telefone da Lily:", "987-554-2130", "987-544-2130", "978-554-2130", "987-554-3120"),
    _q("What time is it?", "Que horas são?", "6:15", "6:30", "6:50", "5:15"),
    _q("Lily: \"My English class is at…\"", "Lily: \"A minha aula de inglês é às…\"", "6:30", "6:15", "7:30", "6:13"),
])
AULA6_VIDEO = _video(6, "Aula 06 — Days of the Week, Seasons, Months", "Video — Mia's favorite season",
                     "a Mia fala das estações do ano e dos favoritos dela.", "aula6-video", [
    _q("Mia: \"In winter, I drink…\"", "Mia: \"No inverno, eu tomo…\"", "hot chocolate.", "coffee.", "juice.", "water."),
    _q("Mia: \"My birthday is in…\"", "Mia: \"Meu aniversário é em…\"", "September.", "December.", "April.", "July."),
    _q("Mia: \"My favorite season is summer because…\"", "Mia: \"Minha estação favorita é o verão porque…\"",
       "I love the beach.", "I love Christmas.", "it's cold.", "I love the flowers."),
    _q("Mia: \"My favorite day of the week is…\"", "Mia: \"Meu dia da semana favorito é…\"",
       "Saturday.", "Sunday.", "Friday.", "Tuesday."),
])
AULA7_VIDEO = _video(7, "Aula 07 — Subject Pronouns", "Video — Ben's photos",
                     "o Ben mostra as fotos dele: o cachorro, as gatas, os amigos e a família.", "aula7-video", [
    _q("Max is a dog. We use…", "O Max é um cachorro. Usamos…", "it", "he", "she", "they"),
    _q("Luna and Mimi (two cats) = …", "Luna e Mimi (duas gatas) = …", "they", "it", "she", "we"),
    _q("Sara = …", "Sara = …", "she", "he", "it", "they"),
    _q("My family and I = …", "Minha família e eu = …", "we", "they", "you", "it"),
])
AULA8_VIDEO = _video(8, "Aula 08 — Present Simple (affirmative)", "Video — My dad's day",
                     "a filha do Carlos conta o dia dele (he wakes up, he goes, he studies…).", "aula8-video", [
    _q("Carlos wakes up at…", "O Carlos acorda às…", "six.", "seven.", "eight.", "five."),
    _q("Carlos goes to work…", "O Carlos vai para o trabalho…", "by bus.", "by car.", "by bike.", "by taxi."),
    _q("Carlos finishes work at…", "O Carlos termina o trabalho às…", "5 p.m.", "6 p.m.", "4 p.m.", "7 p.m."),
    _q("At night, Carlos…", "À noite, o Carlos…", "studies English.", "goes to work.", "takes a shower.", "drinks coffee."),
])
AULA10_VIDEO = _video(10, "Aula 10 — Present Simple (negative)", "Video — Nina's food",
                      "a Nina conta o que ela e a família gostam e não gostam de comer.", "aula10-video", [
    _q("Nina eats pizza every…", "A Nina come pizza toda…", "Friday.", "Sunday.", "Monday.", "Tuesday."),
    _q("Nina … salad.", "A Nina … salada.", "doesn't like", "likes", "don't like", "doesn't likes"),
    _q("Theo …", "O Theo …", "doesn't eat cake.", "don't eat cake.", "eats cake every day.", "doesn't eats cake."),
    _q("Nina drinks…", "A Nina bebe…", "juice.", "coffee.", "tea.", "milk."),
])

# ---------- Aula 11 — Present Simple (interrogative 1: yes/no questions) (https://youtu.be/fdghwGUAq40) ----------

AULA11_TOPIC = "Aula 11 — Present Simple (interrogative 1)"

AULA11_DO_DOES = {
    "title": "Do or does?",
    "lesson": 11,
    "description": "Perguntas de YES or NO no present simple: começam com o verbo auxiliar.\n"
                   "• I, you, we, they → DO: Do you like sushi?\n"
                   "• He, she, it → DOES: Does he like pizza?\n"
                   "• O S aparece UMA vez só, no DOES. O verbo volta para a forma básica: Does she like… (NÃO \"Does she likes\").\n"
                   "• Em português só mudamos a entonação (\"Você estuda inglês?\"). Em inglês PRECISA do DO / DOES no começo.",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Do or does?",
         "translation": "Do ou does? Olhe o sujeito da pergunta!",
         "example": "[Does] he like pizza?",
         "text": "1. [*Do|Does] you like sushi?\n"
                 "2. [*Does|Do] she like salad?\n"
                 "3. [*Do|Does] they like tea?\n"
                 "4. [*Does|Do] your father drink coffee?\n"
                 "5. [*Do|Does] we have English class today?\n"
                 "6. [*Does|Do] your dog sleep a lot?\n"
                 "7. [*Do|Does] your friends play soccer?"},
        {"type": "group",
         "prompt": "Which auxiliary do we use? Put the subjects in the correct group.",
         "translation": "Qual auxiliar usamos? Coloque os sujeitos no grupo certo.",
         "example": "you → Do (Do you…?)",
         "categories": ["Do", "Does"],
         "words": [
             {"text": "I", "category": "Do"}, {"text": "you", "category": "Do"}, {"text": "we", "category": "Do"},
             {"text": "they", "category": "Do"}, {"text": "Ana and Paul", "category": "Do"},
             {"text": "he", "category": "Does"}, {"text": "she", "category": "Does"}, {"text": "it", "category": "Does"},
             {"text": "my mother", "category": "Does"}, {"text": "your cat", "category": "Does"},
         ]},
        {"type": "truefalse",
         "prompt": "Is this sentence correct? Choose True (correct) or False (incorrect).",
         "translation": "Esta frase está correta? Escolha True (correta) ou False (errada).",
         "example": "\"Does he like ice cream?\" → True",
         "statements": [
             {"text": "Do he like ice cream?", "answer": False, "translation": "Ele gosta de sorvete?"},
             {"text": "Does she likes coffee?", "answer": False, "translation": "Ela gosta de café?"},
             {"text": "Do you like milk? — Yes, I like.", "answer": False, "translation": "Você gosta de leite? — Sim, eu gosto."},
             {"text": "Does she like salad? — Yes, she does.", "answer": True, "translation": "Ela gosta de salada? — Sim, gosta."},
             {"text": "Do you like soup? — No, I don't.", "answer": True, "translation": "Você gosta de sopa? — Não, não gosto."},
         ]},
        {"type": "choice",
         "prompt": "What is the correct question? (Ela acorda às 6?)",
         "translation": "Qual é a pergunta correta? (Ela acorda às 6?)",
         "options": ["Does she wake up at 6?", "She wakes up at 6?", "Does she wakes up at 6?", "Do she wake up at 6?"],
         "correct": 0},
        {"type": "choice",
         "prompt": "Do you like milk? — Yes, …",
         "translation": "Você gosta de leite? — Sim, … (resposta curta)",
         "options": ["I do.", "I like.", "I does.", "I likes."], "correct": 0},
    ],
}

AULA11_SHORT_ANSWERS = {
    "title": "Questions and short answers",
    "lesson": 11,
    "description": "Responda com SHORT ANSWERS (respostas curtas, mas completas): repita o auxiliar da pergunta.\n"
                   "Do you…? → Yes, I do. / No, I don't.\n"
                   "Does he…? → Yes, he does. / No, he doesn't.\n"
                   "Cuidado: \"Yes, he likes.\" está ERRADO (falta o complemento). Use: Yes, he does.",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Complete the short answers.",
         "translation": "Complete as respostas curtas.",
         "example": "Does she like salad? — Yes, she [does].",
         "text": "1. Do they like tea? — Yes, they [*do|does].\n"
                 "2. Do you like soup? — No, I [*don't|doesn't].\n"
                 "3. Does he like cake? — No, he [*doesn't|don't].\n"
                 "4. Does your sister speak English? — Yes, she [*does|do].\n"
                 "5. Do your parents live in Rio? — No, they [*don't|doesn't]."},
        {"type": "fill",
         "prompt": "Make questions. Use Do or Does.",
         "translation": "Transforme as frases em perguntas. Use Do ou Does.",
         "example": "You study English. → Do you study English?",
         "text": "1. She wakes up at 6. → [Does she wake up at 6?]\n"
                 "2. They like pizza. → [Do they like pizza?]\n"
                 "3. He works in an office. → [Does he work in an office?]\n"
                 "4. You have a pet. → [Do you have a pet?]\n"
                 "5. Your brother plays the guitar. → [Does your brother play the guitar?]"},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (O seu pai bebe café?)",
         "example": "you / Do / like / sushi → Do you like sushi?",
         "tokens": ["Does", "your", "father", "drink", "coffee?"], "alternatives": []},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas.",
         "example": "Do you like bacon? → Yes, I do.",
         "pairs": [
             {"left": "Does Maria cook dinner?", "right": "Yes, she does."},
             {"left": "Do your friends play tennis?", "right": "No, they don't."},
             {"left": "Does Tom wear glasses?", "right": "No, he doesn't."},
             {"left": "Do you speak English?", "right": "Yes, I do."},
             {"left": "Does your dog sleep on the sofa?", "right": "Yes, it does."},
         ]},
        {"type": "choice",
         "prompt": "Ele gosta de pizza? Sim, ele gosta. → ?",
         "translation": "Qual é a forma natural em inglês?",
         "options": ["Does he like pizza? — Yes, he does.", "Does he like pizza? — Yes, he likes.",
                     "He likes pizza? — Yes, he does.", "Do he like pizza? — Yes, he do."], "correct": 0},
    ],
}

AULA11_LISTENING = {
    "title": "Listening — do you…?",
    "lesson": 11,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Repare: a voz SOBE no final das perguntas de yes or no. ↗",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Do or does? Listen and choose.",
         "translation": "Do ou does? Ouça e escolha o que você ouvir.",
         "example": "Você ouve: \"Does she like tea?\" → Does",
         "audio": f"{AUDIO}/aula11-dodoes.m4a",
         "text": "1. [*Does|Do] he like pizza?\n"
                 "2. [*Do|Does] you speak English?\n"
                 "3. [*Do|Does] they live in Rio?\n"
                 "4. [*Does|Do] she drink coffee?\n"
                 "5. [*Does|Do] it sleep a lot?"},
        {"type": "fill",
         "prompt": "Dictation: listen and write the short answers.",
         "translation": "Ditado: ouça e escreva as respostas curtas.",
         "example": "Você ouve: \"Do you like cake? Yes, I do.\" → Yes, I do.",
         "audio": f"{AUDIO}/aula11-answers.m4a",
         "text": "1. [Yes, I do.|Yes I do]\n"
                 "2. [No, she doesn't.|No she doesn't|No, she does not.]\n"
                 "3. [Yes, they do.|Yes they do]\n"
                 "4. [No, he doesn't.|No he doesn't|No, he does not.]"},
        {"type": "info",
         "prompt": "Now listen to Emma and Jake. They are new classmates.",
         "translation": "Agora ouça a Emma e o Jake. Eles são colegas novos de turma e fazem perguntas um ao outro. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula11-classmates.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose the short answer.",
         "translation": "Ouça de novo e escolha a resposta curta correta.",
         "example": "Does Jake live near the school? → [Yes, he does.]",
         "text": "1. Does Jake work? → [*No, he doesn't.|Yes, he does.]\n"
                 "2. Does Emma work? → [*Yes, she does.|No, she doesn't.]\n"
                 "3. Does Jake play soccer? → [*Yes, he does.|No, he doesn't.]\n"
                 "4. Does Emma like soccer? → [*No, she doesn't.|Yes, she does.]\n"
                 "5. Do they like coffee? → [*Yes, they do.|No, they don't.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the audio.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o áudio.",
         "example": "Jake lives near the school. → True",
         "statements": [
             {"text": "Jake is a student.", "answer": True, "translation": "O Jake é estudante."},
             {"text": "Emma works in a hospital.", "answer": False, "translation": "A Emma trabalha num hospital."},
             {"text": "Emma plays the piano.", "answer": True, "translation": "A Emma toca piano."},
         ]},
    ],
}

AULA11_SPEAKING = {
    "title": "Speaking — Do you…? Yes, I do!",
    "lesson": 11,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica da aula: nas perguntas de yes or no, a voz SOBE no final ↗. DO YOU fica rápido e junto: \"du-iu\". "
                   "DOES = \"dâz\" · DOESN'T = \"dâzunt\".",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the questions. Your voice goes up at the end ↗.",
         "translation": "Ouça e repita as perguntas. A sua voz sobe no final ↗.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula11-say-q{i}.m4a"} for i, t in enumerate(
             ["Do you like sushi?", "Do you like salad?", "Does he like pizza?", "Does she like salad?",
              "Do they like tea?", "Do you study English?", "Does she wake up at six?"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the short answers.",
         "translation": "Ouça e repita as respostas curtas.",
         "example": "\"Yes, I do.\" — \"No, he doesn't.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula11-say-a{i}.m4a"} for i, t in enumerate(
             ["Yes, I do.", "No, I don't.", "Yes, he does.", "No, he doesn't.", "Yes, she does.", "No, they don't."], 1)]},
        {"type": "speak",
         "prompt": "Now answer about YOU with a short answer.",
         "translation": "Agora responda sobre VOCÊ com uma resposta curta (Yes, I do. / No, I don't.).",
         "example": "\"Do you like coffee?\" → \"Yes, I do.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula11-say-y{i}.m4a"} for i, t in enumerate(
             ["Do you like coffee?", "Do you have a pet?", "Do you speak English?", "Do you wake up early?"], 1)]},
    ],
}

AULA11_READING = {
    "title": "Reading — family quiz",
    "lesson": 11,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Leo's family quiz.",
         "translation": "Leia e ouça o quiz que o Leo fez com a família dele. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula11-reading.m4a",
         "text": "FAMILY QUIZ — by Leo\n\n"
                 "I ask my family some questions. Here are the answers!\n\n"
                 "Mom, do you like coffee? — Yes, I do. I drink coffee every morning.\n"
                 "Dad, do you cook? — No, I don't. But I do the housework!\n"
                 "Ana (my sister), do you play the guitar? — Yes, I do. I play every day.\n"
                 "Mom and Dad, do you speak English? — Mom: Yes, I do. Dad: No, I don't. I speak Spanish.\n"
                 "And our dog, Toby? Does he sleep on the sofa? Yes, he does! Every night!"},
        {"type": "dropdown",
         "prompt": "Choose the correct short answer according to the text.",
         "translation": "Escolha a resposta curta correta de acordo com o texto.",
         "example": "Does Leo's mom like coffee? → [Yes, she does.]",
         "text": "1. Does Leo's dad cook? → [*No, he doesn't.|Yes, he does.|No, he don't.]\n"
                 "2. Does Ana play the guitar? → [*Yes, she does.|No, she doesn't.|Yes, she plays.]\n"
                 "3. Does Leo's dad speak English? → [*No, he doesn't.|Yes, he does.|No, he don't.]\n"
                 "4. Does Toby sleep on the sofa? → [*Yes, he does.|No, he doesn't.|Yes, he do.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Leo's mom drinks coffee every morning. → True",
         "statements": [
             {"text": "Leo's dad does the housework.", "answer": True, "translation": "O pai do Leo faz as tarefas de casa."},
             {"text": "Ana plays the guitar on Saturdays only.", "answer": False,
              "translation": "A Ana toca violão só aos sábados."},
             {"text": "Leo's dad speaks Spanish.", "answer": True, "translation": "O pai do Leo fala espanhol."},
             {"text": "Toby is a cat.", "answer": False, "translation": "O Toby é um gato."},
         ]},
        {"type": "fill",
         "prompt": "Write the questions from the text.",
         "translation": "Complete as perguntas do texto.",
         "example": "Mom, [do] you like coffee?",
         "text": "1. Dad, [do] you cook?\n"
                 "2. [Does] he sleep on the sofa?\n"
                 "3. Mom and Dad, [do] you speak English?"},
    ],
}

AULA11_WRITING = {
    "title": "Writing — questions for a new friend",
    "lesson": 11,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Escreva perguntas de yes or no e responda com short answers.\n"
                   "Lembre: Do you…? / Does he…? / Does she…? e o verbo SEM S depois do DOES.",
    "topic": AULA11_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the questions in English.",
         "translation": "Escreva as perguntas em inglês.",
         "example": "Você gosta de chocolate? → Do you like chocolate?",
         "text": "1. Você estuda inglês? → [Do you study English?]\n"
                 "2. Ela acorda às 6? → [Does she wake up at 6?|Does she wake up at six?]\n"
                 "3. Eles bebem café? → [Do they drink coffee?]\n"
                 "4. O seu irmão joga tênis? → [Does your brother play tennis?]"},
        {"type": "fill",
         "prompt": "Correct the mistakes.",
         "translation": "Corrija os erros (todas as frases têm um erro).",
         "example": "Do he like ice cream? → Does he like ice cream?",
         "text": "1. Does she likes coffee? → [Does she like coffee?]\n"
                 "2. Do you like milk? Yes, I like. → [Yes, I do.|Yes, I do]\n"
                 "3. You speak English? → [Do you speak English?]"},
        {"type": "free",
         "prompt": "You have a new friend. Write 5 yes/no questions for him or her (Do you…?). "
                   "Then answer the questions about YOU with short answers.",
         "translation": "Você tem um amigo novo. Escreva 5 perguntas de yes or no para ele ou ela (Do you…?). "
                        "Depois responda às perguntas sobre VOCÊ com short answers (Yes, I do. / No, I don't.).",
         "example": "Do you like pizza? — Yes, I do.",
         "model_answer": "Do you like pizza? — Yes, I do.\n"
                         "Do you have a pet? — No, I don't.\n"
                         "Do you play the guitar? — No, I don't.\n"
                         "Do you speak English? — Yes, I do.\n"
                         "Do you wake up early? — Yes, I do.",
         "keywords": ["Do you", "I do", "I don't"], "min_words": 25, "points": 4},
    ],
}

AULA11_VIDEO = _video(11, AULA11_TOPIC, "Video — A new roommate",
                      "a Paula procura alguém para dividir o apartamento e faz perguntas para o Mike.", "aula11-video", [
    _q("Does Mike like cats?", "O Mike gosta de gatos?", "Yes, he does.", "No, he doesn't.", "Yes, he likes.", "Yes, he do."),
    _q("Does Mike cook?", "O Mike cozinha?", "Yes, he does.", "No, he doesn't.", "Yes, he cooks.", "No, he don't."),
    _q("Does Mike play the guitar at night?", "O Mike toca violão à noite?", "No, he doesn't.", "Yes, he does.",
       "No, he don't.", "No, he not."),
    _q("Does Paula work from home?", "A Paula trabalha de casa?", "Yes, she does.", "No, she doesn't.", "Yes, she do.",
       "Yes, she works."),
    _q("Do they see the flat on Saturday?", "Eles vão ver o apartamento no sábado?", "Yes, they do.", "No, they don't.",
       "Yes, they does.", "Yes, they see."),
])

# ---------- Aula 12 — Present Simple (interrogative 2: wh-questions) (https://youtu.be/YUP0oOSb26A) ----------

AULA12_TOPIC = "Aula 12 — Present Simple (interrogative 2)"

AULA12_WORDS = {
    "title": "Question words",
    "lesson": 12,
    "description": "WH question words: perguntas que pedem uma informação (não só yes or no).\n"
                   "what (o que / qual) · where (onde) · when (quando) · who (quem — só para pessoas) · why (por que) · "
                   "which (qual — quando há opções) · how (como)\n"
                   "Blocos para memorizar: what time (que horas) · what kind of (que tipo de) · how many (quantos) · "
                   "how much (quanto) · how often (com que frequência) · how old (quantos anos)\n"
                   "WHY na pergunta → BECAUSE na resposta. Cuidado: HOW (ráu) ≠ WHO (rú).",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the question words to Portuguese.",
         "translation": "Ligue as question words ao português.",
         "example": "where → onde",
         "pairs": [
             {"left": "what", "right": "o que / qual"},
             {"left": "when", "right": "quando"},
             {"left": "who", "right": "quem"},
             {"left": "why", "right": "por que"},
             {"left": "which", "right": "qual (entre opções)"},
             {"left": "how", "right": "como"},
         ]},
        {"type": "match",
         "prompt": "Match the blocks of words to Portuguese.",
         "translation": "Ligue os blocos de palavras ao português.",
         "example": "how old → quantos anos",
         "pairs": [
             {"left": "what time", "right": "que horas"},
             {"left": "what kind of", "right": "que tipo de"},
             {"left": "how many", "right": "quantos / quantas"},
             {"left": "how much", "right": "quanto (preço, quantidade)"},
             {"left": "how often", "right": "com que frequência"},
         ]},
        {"type": "dropdown",
         "prompt": "Look at the answer and choose the question word.",
         "translation": "Olhe a resposta e escolha a question word certa.",
         "example": "[Where] do you live? — I live in Florianópolis.",
         "text": "1. [*When|Where|Who] do you have English class? — On Saturdays.\n"
                 "2. [*Who|How|Where] do you admire? — My father.\n"
                 "3. [*Why|What|When] do you wake up early? — Because I go to the gym before work.\n"
                 "4. [*How|Who|Which] do you go to work? — By bus.\n"
                 "5. [*Which|Who|When] do you prefer, cats or dogs? — Dogs.\n"
                 "6. [*What|Where|Who] do you do? — I'm a teacher."},
        {"type": "dropdown",
         "prompt": "Complete with the right block of words.",
         "translation": "Complete com o bloco de palavras certo.",
         "example": "[What time] do you go to bed? — At 11 p.m.",
         "text": "1. [*How many|How much|How old] sisters do you have? — Three.\n"
                 "2. [*What kind of|What time|How often] music do you like? — Pop music.\n"
                 "3. [*How much|How many|How old] coffee do you drink? — A lot!\n"
                 "4. [*How old|How many|What time] are you? — I'm 25 years old.\n"
                 "5. [*How often|What kind of|How many] do you go to the gym? — Every day."},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Who\" is for people. → True",
         "statements": [
             {"text": "The question word is always the first word of the question.", "answer": True,
              "translation": "A question word é sempre a primeira palavra da pergunta."},
             {"text": "\"How\" and \"who\" have the same pronunciation.", "answer": False,
              "translation": "\"How\" e \"who\" têm a mesma pronúncia."},
             {"text": "We use \"which\" when there are options.", "answer": True,
              "translation": "Usamos \"which\" quando há opções."},
             {"text": "To say \"faço home office\", we say \"I work from home\".", "answer": True,
              "translation": "Para dizer \"faço home office\", dizemos \"I work from home\"."},
             {"text": "\"Siblings\" means only sisters.", "answer": False,
              "translation": "\"Siblings\" significa só irmãs."},
         ]},
    ],
}

AULA12_ORDER = {
    "title": "Making wh-questions",
    "lesson": 12,
    "description": "A ordem da pergunta: QUESTION WORD + DO / DOES + SUJEITO + VERBO + complemento.\n"
                   "Where do you live? · What time does she wake up? · How many sisters does Daniel have?\n"
                   "He, she, it (Daniel, your best friend…) → DOES, e o verbo sem S.",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Que tipo de comida você gosta?)",
         "example": "you / do / Where / live → Where do you live?",
         "tokens": ["What", "kind", "of", "food", "do", "you", "like?"], "alternatives": []},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Onde o seu melhor amigo mora?)",
         "example": "does / Where / she / work → Where does she work?",
         "tokens": ["Where", "does", "your", "best", "friend", "live?"], "alternatives": []},
        {"type": "dropdown",
         "prompt": "Do or does?",
         "translation": "Do ou does?",
         "example": "How many sisters [does] Daniel have?",
         "text": "1. Where [*do|does] you work?\n"
                 "2. What time [*does|do] she wake up?\n"
                 "3. Why [*do|does] they study English?\n"
                 "4. What [*does|do] your father do?\n"
                 "5. How [*does|do] Maria go to work?"},
        {"type": "fill",
         "prompt": "Translate the questions (from the lesson).",
         "translation": "Traduza as perguntas da aula.",
         "example": "Que horas você toma café da manhã? → What time do you have breakfast?",
         "text": "1. Quando você estuda inglês? → [When do you study English?]\n"
                 "2. Como você vai para o trabalho? → [How do you go to work?]\n"
                 "3. Quem você admira? → [Who do you admire?]\n"
                 "4. Por que você acorda cedo? → [Why do you wake up early?]\n"
                 "5. Quantas irmãs você tem? → [How many sisters do you have?]"},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas.",
         "example": "Where do you live? → I live in São Paulo.",
         "pairs": [
             {"left": "What kind of food do you like?", "right": "I like Japanese food."},
             {"left": "Why do you study English?", "right": "Because I want to travel the world."},
             {"left": "How do you go to work?", "right": "I work from home."},
             {"left": "Which do you prefer, cats or dogs?", "right": "I prefer cats."},
             {"left": "When is your birthday?", "right": "In May."},
         ]},
    ],
}

AULA12_LISTENING = {
    "title": "Listening — wh-questions",
    "lesson": 12,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Atenção: HOW (ráu) ≠ WHO (rú).",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "How or who? Listen and choose.",
         "translation": "How (como) ou who (quem)? Ouça e escolha.",
         "example": "Você ouve: \"Who do you admire?\" → Who",
         "audio": f"{AUDIO}/aula12-howwho.m4a",
         "text": "1. [*How|Who] do you go to work?\n"
                 "2. [*Who|How] do you admire?\n"
                 "3. [*Who|How] is your favorite singer?\n"
                 "4. [*How|Who] are you?\n"
                 "5. [*How|Who] old are you?"},
        {"type": "fill",
         "prompt": "Dictation: listen and write the question word or block.",
         "translation": "Ditado: ouça e escreva a question word (ou o bloco) que começa cada pergunta.",
         "example": "Você ouve: \"Where do you live?\" → [Where] do you live?",
         "audio": f"{AUDIO}/aula12-dictation.m4a",
         "text": "1. [When] do you have English class?\n"
                 "2. [Why] do you wake up early?\n"
                 "3. [What time] do you go to bed?\n"
                 "4. [How many] brothers do you have?\n"
                 "5. [Which] do you prefer, tea or coffee?"},
        {"type": "info",
         "prompt": "Now listen to a radio interview with Sofia, a nurse.",
         "translation": "Agora ouça uma entrevista de rádio com a Sofia, uma enfermeira. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula12-interview.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "fill",
         "prompt": "Listen again and complete Sofia's answers.",
         "translation": "Ouça de novo e complete as respostas da Sofia.",
         "example": "Where does Sofia work? — At a [hospital].",
         "text": "1. Where does she live? — In [Recife].\n"
                 "2. What time does she start work? — At [7|7:00|seven|7 a.m.].\n"
                 "3. How does she go to work? — By [bike|bicycle].\n"
                 "4. How many children does she have? — [Two|2]."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the interview.",
         "translation": "Verdadeiro ou falso? Responda de acordo com a entrevista.",
         "example": "Sofia is a nurse. → True",
         "statements": [
             {"text": "Sofia loves her job because she helps people.", "answer": True,
              "translation": "A Sofia ama o trabalho dela porque ela ajuda as pessoas."},
             {"text": "Sofia admires her father.", "answer": False, "translation": "A Sofia admira o pai dela."},
             {"text": "Sofia prefers dogs.", "answer": False, "translation": "A Sofia prefere cachorros."},
         ]},
    ],
}

AULA12_SPEAKING = {
    "title": "Speaking — wh-questions",
    "lesson": 12,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: HOW = \"ráu\" · WHO = \"rú\" · WHAT KIND OF = \"uót kaind óv\" (o F soa como V) · EARLY = \"ârli\".",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the question words.",
         "translation": "Ouça e repita as question words e os blocos.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula12-say-w{i}.m4a"} for i, t in enumerate(
             ["what", "where", "when", "who", "why", "which", "how", "what time", "what kind of", "how many", "how often"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the questions.",
         "translation": "Ouça e repita as perguntas da aula.",
         "example": "\"Where do you live?\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula12-say-q{i}.m4a"} for i, t in enumerate(
             ["What time do you have breakfast?", "When do you study English?", "How do you go to work?",
              "What kind of food do you like?", "Who do you admire?", "Why do you wake up early?",
              "How many sisters do you have?", "Which do you prefer, cats or dogs?"], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOU.",
         "translation": "Agora responda às perguntas sobre VOCÊ com uma frase completa.",
         "example": "\"Where do you live?\" → \"I live in Salvador.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula12-say-y{i}.m4a"} for i, t in enumerate(
             ["Where do you live?", "What do you do?", "Why do you study English?", "What kind of music do you like?"], 1)]},
    ],
}

AULA12_READING = {
    "title": "Reading — meet Daniel",
    "lesson": 12,
    "subject": "Reading",
    "description": "Leia (e ouça) o perfil e responda às perguntas de acordo com o texto.",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text about Daniel.",
         "translation": "Leia e ouça o texto sobre o Daniel. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula12-reading.m4a",
         "text": "MEET DANIEL\n\n"
                 "Daniel is 32 years old. He lives in Porto Alegre with his wife and their cat.\n"
                 "He is an engineer, but he doesn't go to an office: he works from home.\n"
                 "He wakes up at 6:30 because he runs in the park before work.\n"
                 "He has two siblings: one sister and one brother.\n"
                 "He loves rock music and Japanese food. He admires his mother, a doctor.\n"
                 "He studies English on Tuesdays and Thursdays because he wants to work in Canada."},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "How old is Daniel? → [32]",
         "text": "1. Where does Daniel live? → [*In Porto Alegre.|In Canada.|In São Paulo.]\n"
                 "2. What does he do? → [*He's an engineer.|He's a doctor.|He's a teacher.]\n"
                 "3. Why does he wake up at 6:30? → [*Because he runs in the park.|Because he goes to the office.|Because he studies English.]\n"
                 "4. How many siblings does he have? → [*Two.|One.|Three.]\n"
                 "5. Who does he admire? → [*His mother.|His wife.|His sister.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Daniel has a cat. → True",
         "statements": [
             {"text": "Daniel works in an office.", "answer": False, "translation": "O Daniel trabalha num escritório."},
             {"text": "Daniel likes Japanese food.", "answer": True, "translation": "O Daniel gosta de comida japonesa."},
             {"text": "Daniel studies English on Saturdays.", "answer": False,
              "translation": "O Daniel estuda inglês aos sábados."},
             {"text": "Daniel wants to work in Canada.", "answer": True, "translation": "O Daniel quer trabalhar no Canadá."},
         ]},
        {"type": "fill",
         "prompt": "Complete the questions about the text.",
         "translation": "Complete as perguntas sobre o texto com a question word certa.",
         "example": "[Where] does Daniel live? — In Porto Alegre.",
         "text": "1. [What kind of] music does he like? — Rock music.\n"
                 "2. [When] does he study English? — On Tuesdays and Thursdays.\n"
                 "3. [Why] does he study English? — Because he wants to work in Canada."},
    ],
}

AULA12_WRITING = {
    "title": "Writing — an interview",
    "lesson": 12,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Escreva perguntas com WH question words e responda.\n"
                   "Ordem: question word + do/does + sujeito + verbo + complemento.",
    "topic": AULA12_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the question for each answer.",
         "translation": "Escreva a pergunta para cada resposta (use you).",
         "example": "I live in Rio. → Where do you live?",
         "text": "1. I wake up at 7. → [What time do you wake up?|When do you wake up?]\n"
                 "2. I go to work by car. → [How do you go to work?]\n"
                 "3. I like pop music. → [What kind of music do you like?|What music do you like?]\n"
                 "4. Because I love my job. → [Why do you love your job?|Why do you like your job?]"},
        {"type": "fill",
         "prompt": "Write the questions about Daniel (he → does).",
         "translation": "Escreva as perguntas sobre o Daniel (he → does).",
         "example": "Onde o Daniel mora? → Where does Daniel live?",
         "text": "1. O que o Daniel faz? → [What does Daniel do?]\n"
                 "2. Quantos irmãos o Daniel tem? → [How many siblings does Daniel have?|How many brothers does Daniel have?]\n"
                 "3. Quando o Daniel estuda inglês? → [When does Daniel study English?]"},
        {"type": "free",
         "prompt": "Interview a friend or a person in your family. Write 5 questions with different question words "
                   "and his or her answers.",
         "translation": "Entreviste um amigo ou alguém da sua família. Escreva 5 perguntas com question words diferentes "
                        "e as respostas da pessoa.",
         "example": "Where do you live? — I live in Belo Horizonte.",
         "model_answer": "Where do you live? — I live in Belo Horizonte.\n"
                         "What do you do? — I'm a nurse.\n"
                         "What time do you wake up? — I wake up at 6 a.m.\n"
                         "Why do you study English? — Because I want to travel.\n"
                         "How do you go to work? — By bus.",
         "keywords": ["where", "what", "why", "how", "do you"], "min_words": 30, "points": 4},
    ],
}

AULA12_VIDEO = _video(12, AULA12_TOPIC, "Video — Meet Chef Marco",
                      "uma entrevista com o Marco, um chef de cozinha italiana: what, where, how, what time, who, why.",
                      "aula12-video", [
    _q("What kind of food does Marco cook?", "Que tipo de comida o Marco cozinha?",
       "Italian food.", "Japanese food.", "Brazilian food.", "Mexican food."),
    _q("How does Marco go to work?", "Como o Marco vai para o trabalho?", "By bike.", "By car.", "By bus.", "On foot."),
    _q("What time does Marco start work?", "Que horas o Marco começa a trabalhar?", "At 10 a.m.", "At 10 p.m.", "At 2 p.m.",
       "At noon."),
    _q("Who does Marco admire?", "Quem o Marco admira?", "His grandmother.", "His father.", "His sister.", "His wife."),
    _q("Why does Marco love his job?", "Por que o Marco ama o trabalho dele?", "Because he makes people happy.",
       "Because he works from home.", "Because he wakes up late.", "Because he lives in Italy."),
])

# ---------- Aula 13 — Sports: play, do, go (https://youtu.be/kZaL_6T0Oqg) ----------

AULA13_TOPIC = "Aula 13 — Sports"

AULA13_WORDS = {
    "title": "Sports: play, do, go",
    "lesson": 13,
    "description": "Três verbos para falar de esportes e atividades:\n"
                   "PLAY → esportes em equipe e com bola: play soccer, play basketball, play volleyball, play tennis.\n"
                   "DO → atividades individuais, artes marciais e exercícios: do karate, do judo, do yoga, do pilates.\n"
                   "GO → atividades que terminam em -ING e envolvem movimento: go swimming, go running, go cycling, go hiking.\n"
                   "Cuidado: em CLIMBING o B é mudo (\"cláimin\").",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the sports to Portuguese.",
         "translation": "Ligue os esportes ao português.",
         "example": "soccer → futebol",
         "pairs": [
             {"left": "volleyball", "right": "vôlei"},
             {"left": "weightlifting", "right": "levantamento de peso"},
             {"left": "fencing", "right": "esgrima"},
             {"left": "swimming", "right": "natação"},
             {"left": "hiking", "right": "trilha (caminhada)"},
             {"left": "fishing", "right": "pesca"},
         ]},
        {"type": "group",
         "prompt": "Play, do or go? Put each sport in the right group.",
         "translation": "Play, do ou go? Coloque cada esporte no grupo do verbo certo.",
         "example": "soccer → play (esporte com bola, em equipe)",
         "categories": ["play", "do", "go"],
         "words": [
             {"text": "basketball", "category": "play"}, {"text": "tennis", "category": "play"},
             {"text": "golf", "category": "play"}, {"text": "hockey", "category": "play"},
             {"text": "judo", "category": "do"}, {"text": "yoga", "category": "do"},
             {"text": "boxing", "category": "do"}, {"text": "aerobics", "category": "do"},
             {"text": "running", "category": "go"}, {"text": "surfing", "category": "go"},
             {"text": "skiing", "category": "go"}, {"text": "climbing", "category": "go"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the right verb: play, do or go.",
         "translation": "Escolha o verbo certo: play, do ou go.",
         "example": "I [play] volleyball at school.",
         "text": "1. I [*go|play|do] swimming on Saturdays.\n"
                 "2. They [*play|do|go] baseball in the park.\n"
                 "3. We [*do|play|go] pilates on Mondays.\n"
                 "4. I [*go|do|play] cycling with my father.\n"
                 "5. You [*do|play|go] weightlifting at the gym.\n"
                 "6. They [*play|go|do] handball after class."},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "We use \"play\" for team sports and ball games. → True",
         "statements": [
             {"text": "We use \"do\" for martial arts, like karate and judo.", "answer": True,
              "translation": "Usamos \"do\" para artes marciais, como caratê e judô."},
             {"text": "We say \"play yoga\".", "answer": False, "translation": "Dizemos \"play yoga\"."},
             {"text": "With \"go\", the activity usually ends in -ING.", "answer": True,
              "translation": "Com \"go\", a atividade normalmente termina em -ING."},
             {"text": "In \"climbing\", we say the letter B.", "answer": False,
              "translation": "Em \"climbing\", a gente pronuncia a letra B."},
             {"text": "\"Fencing\" means esgrima in Portuguese.", "answer": True,
              "translation": "\"Fencing\" significa esgrima em português."},
         ]},
    ],
}

AULA13_QUESTIONS = {
    "title": "Do you practice any sports?",
    "lesson": 13,
    "description": "Revisão do Present Simple interrogative:\n"
                   "DO + I / you / we / they + verbo + complemento → Do you go to the gym every day?\n"
                   "DOES + he / she / it + verbo (sem S) + complemento → Does she go cycling in the afternoon?\n"
                   "Do you practice any sports or activities? → Yes, I do. / No, I don't.\n"
                   "What sports or activities do you practice? → I go running and swimming. I do pilates and I play volleyball.",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Você pratica algum esporte ou atividade?)",
         "example": "you / Do / play / tennis → Do you play tennis?",
         "tokens": ["Do", "you", "practice", "any", "sports", "or", "activities?"], "alternatives": []},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Ele joga basquete depois da aula?)",
         "example": "she / Does / yoga / do → Does she do yoga?",
         "tokens": ["Does", "he", "play", "basketball", "after", "class?"], "alternatives": []},
        {"type": "dropdown",
         "prompt": "Do or does?",
         "translation": "Do ou does?",
         "example": "[Does] she go cycling in the afternoon?",
         "text": "1. [*Do|Does] you go to the gym every day?\n"
                 "2. [*Does|Do] he go running at the park?\n"
                 "3. [*Do|Does] they play volleyball at school?\n"
                 "4. [*Do|Does] we do judo on Mondays?\n"
                 "5. [*Does|Do] your sister do karate?"},
        {"type": "fill",
         "prompt": "Translate the questions (from the lesson).",
         "translation": "Traduza as perguntas da aula.",
         "example": "Você vai à academia todo dia? → Do you go to the gym every day?",
         "text": "1. Eles jogam vôlei na escola? → [Do they play volleyball at school?]\n"
                 "2. A gente faz judô às segundas? → [Do we do judo on Mondays?]\n"
                 "3. Ela pedala à tarde? → [Does she go cycling in the afternoon?]\n"
                 "4. Ele joga basquete depois da aula? → [Does he play basketball after class?]"},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas.",
         "example": "Do you play tennis? → Yes, I do.",
         "pairs": [
             {"left": "Do you practice any sports?", "right": "No, I don't."},
             {"left": "Does he go swimming?", "right": "Yes, he does."},
             {"left": "Do they play golf?", "right": "No, they don't."},
             {"left": "What sports do you practice?", "right": "I go running and I do yoga."},
             {"left": "When does she do pilates?", "right": "On Tuesdays."},
         ]},
    ],
}

AULA13_LISTENING = {
    "title": "Listening — sports",
    "lesson": 13,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the verb you hear: play, do or go.",
         "translation": "Ouça e escolha o verbo que você ouve: play, do ou go.",
         "example": "Você ouve: \"I play soccer.\" → play",
         "audio": f"{AUDIO}/aula13-verbs.m4a",
         "text": "1. I [*do|play|go] karate.\n"
                 "2. We [*go|do|play] fishing.\n"
                 "3. They [*play|do|go] hockey.\n"
                 "4. I [*go|play|do] hiking.\n"
                 "5. You [*do|go|play] aerobics."},
        {"type": "fill",
         "prompt": "Dictation: listen and write the sport.",
         "translation": "Ditado: ouça e escreva o nome do esporte ou da atividade.",
         "example": "Você ouve: \"Number one: tennis\" → [tennis]",
         "audio": f"{AUDIO}/aula13-dictation.m4a",
         "text": "1. [basketball]\n2. [swimming]\n3. [yoga]\n4. [surfing]\n5. [boxing]"},
        {"type": "info",
         "prompt": "Now listen to Mike and Laura talking about sports.",
         "translation": "Agora ouça o Mike e a Laura conversando sobre esportes. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula13-dialogue.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "fill",
         "prompt": "Listen again and complete.",
         "translation": "Ouça de novo e complete com o esporte ou a atividade.",
         "example": "Mike goes to the [gym] every day.",
         "text": "1. Laura does [pilates] on Tuesdays and Thursdays.\n"
                 "2. On Sundays, Laura goes [cycling] with her husband.\n"
                 "3. Mike plays [tennis] with his brother.\n"
                 "4. Mike's son does [judo] after school."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Laura practices sports. → True",
         "statements": [
             {"text": "Mike goes swimming on Saturdays.", "answer": True, "translation": "O Mike nada aos sábados."},
             {"text": "Laura plays volleyball.", "answer": False, "translation": "A Laura joga vôlei."},
             {"text": "Laura's daughter goes running with her.", "answer": False,
              "translation": "A filha da Laura corre com ela."},
         ]},
    ],
}

AULA13_SPEAKING = {
    "title": "Speaking — sports",
    "lesson": 13,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: CLIMBING = \"cláimin\" (B mudo) · VOLLEYBALL = \"válibol\" · YOGA = \"iôuga\" · "
                   "PILATES = \"piláris\".",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the sports.",
         "translation": "Ouça e repita os esportes e as atividades.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula13-say-w{i}.m4a"} for i, t in enumerate(
             ["soccer", "basketball", "volleyball", "tennis", "karate", "yoga", "pilates", "weightlifting",
              "swimming", "running", "cycling", "climbing"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat: verb + sport.",
         "translation": "Ouça e repita: verbo + esporte.",
         "example": "\"play soccer\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula13-say-v{i}.m4a"} for i, t in enumerate(
             ["play soccer", "play tennis", "do judo", "do yoga", "go swimming", "go hiking",
              "Do you practice any sports or activities?", "Does she go cycling in the afternoon?"], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOU.",
         "translation": "Agora responda às perguntas sobre VOCÊ com uma frase completa.",
         "example": "\"What sports or activities do you practice?\" → \"I go running and I do yoga.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula13-say-y{i}.m4a"} for i, t in enumerate(
             ["Do you practice any sports or activities?", "What sports or activities do you practice?",
              "Do you go to the gym every day?", "What sports does your best friend practice?"], 1)]},
    ],
}

AULA13_READING = {
    "title": "Reading — a sporty family",
    "lesson": 13,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text about Carol's family.",
         "translation": "Leia e ouça o texto sobre a família da Carol. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula13-reading.m4a",
         "text": "A SPORTY FAMILY\n\n"
                 "Hi! I'm Carol, and my family loves sports.\n"
                 "My father, Jorge, goes running in the park every morning. On Saturdays, he plays soccer with his friends.\n"
                 "My mother, Helena, does yoga at home and goes swimming on Wednesdays.\n"
                 "My brother, Tiago, plays basketball at school and does karate on Fridays.\n"
                 "And me? I go surfing on the weekend, and I do pilates on Mondays.\n"
                 "We all go hiking together in the summer. It's my favorite day of the year!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Who is Jorge? → [Carol's father.]",
         "text": "1. What does Jorge do every morning? → [*He goes running.|He goes swimming.|He does yoga.]\n"
                 "2. When does Helena go swimming? → [*On Wednesdays.|On Saturdays.|Every morning.]\n"
                 "3. Where does Tiago play basketball? → [*At school.|In the park.|At home.]\n"
                 "4. When does Carol go surfing? → [*On the weekend.|On Mondays.|On Fridays.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Helena does yoga. → True",
         "statements": [
             {"text": "Jorge plays soccer on Saturdays.", "answer": True, "translation": "O Jorge joga futebol aos sábados."},
             {"text": "Tiago does judo.", "answer": False, "translation": "O Tiago faz judô."},
             {"text": "Carol does pilates on Mondays.", "answer": True, "translation": "A Carol faz pilates às segundas."},
             {"text": "The family goes hiking together in the winter.", "answer": False,
              "translation": "A família faz trilha junta no inverno."},
         ]},
        {"type": "fill",
         "prompt": "Complete with plays, does or goes (he / she → verb + S).",
         "translation": "Complete com plays, does ou goes, de acordo com o texto (he / she → verbo com S).",
         "example": "Jorge [goes] running in the park.",
         "text": "1. Helena [does] yoga at home.\n"
                 "2. Tiago [plays] basketball at school.\n"
                 "3. Tiago [does] karate on Fridays.\n"
                 "4. Carol [goes] surfing on the weekend."},
    ],
}

AULA13_WRITING = {
    "title": "Writing — my sports",
    "lesson": 13,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Use PLAY (bola e equipe), DO (artes marciais e exercícios) e GO (atividades com -ING).\n"
                   "Perguntas: Do you…? / Does he / she…? → Yes, I do. / No, she doesn't.",
    "topic": AULA13_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the activity in English with play, do or go.",
         "translation": "Escreva a atividade em inglês com play, do ou go.",
         "example": "jogar futebol → play soccer",
         "text": "1. fazer caratê → [do karate]\n"
                 "2. nadar → [go swimming]\n"
                 "3. jogar tênis → [play tennis]\n"
                 "4. fazer trilha → [go hiking]\n"
                 "5. fazer pilates → [do pilates]"},
        {"type": "fill",
         "prompt": "Write the questions in English.",
         "translation": "Escreva as perguntas em inglês.",
         "example": "Você faz ioga? → Do you do yoga?",
         "text": "1. Você joga vôlei? → [Do you play volleyball?]\n"
                 "2. Ela faz boxe? → [Does she do boxing?]\n"
                 "3. Eles pescam aos domingos? → [Do they go fishing on Sundays?]"},
        {"type": "free",
         "prompt": "Write about you and your family: what sports or activities do you practice? When? Where? "
                   "Use play, do and go about YOU (I play… / I do… / I go…).",
         "translation": "Escreva sobre você e a sua família: que esportes ou atividades vocês praticam? Quando? Onde? "
                        "Use play, do e go nas frases sobre VOCÊ (I play… / I do… / I go…).",
         "example": "I go running in the park on Saturdays.",
         "model_answer": "I go running in the park on Saturdays, and I do yoga at home on Mondays. I play tennis with my sister.\n"
                         "My brother plays soccer with his friends after work.\n"
                         "My mother goes swimming on Wednesdays.\n"
                         "My father doesn't practice any sports, but he goes fishing on Sundays.",
         "keywords": ["play", "do", "go"], "min_words": 30, "points": 4},
    ],
}

AULA13_VIDEO = _video(13, AULA13_TOPIC, "Video — What sports do they practice?",
                      "a Bia apresenta os amigos e os esportes que eles praticam: play, do or go?",
                      "aula13-video", [
    _q("What sport does Lucas play?", "Que esporte o Lucas joga?", "Soccer.", "Basketball.", "Tennis.", "Volleyball."),
    _q("What does Julia do every morning?", "O que a Julia faz todas as manhãs?", "She does yoga.", "She plays yoga.",
       "She goes swimming.", "She does karate."),
    _q("When does Pedro go cycling?", "Quando o Pedro pedala?", "On Saturdays.", "On Sundays.", "Every day.", "On Mondays."),
    _q("Which sentence is correct?", "Qual frase está correta?", "Carla does karate.", "Carla plays karate.",
       "Carla goes karate.", "Carla go karate."),
    _q("What does Rafa do on the weekend?", "O que o Rafa faz no fim de semana?", "He goes surfing.", "He plays surfing.",
       "He does surfing.", "He goes swimming."),
    _q("Do Bia's friends play volleyball on the beach?", "Os amigos da Bia jogam vôlei na praia?", "Yes, they do.",
       "No, they don't.", "Yes, they does.", "No, they doesn't."),
])


# ---------- Aula 14 — How often… (Frequency) (https://youtu.be/8ArfWmb5UEQ) ----------

AULA14_TOPIC = "Aula 14 — How often… (Frequency)"

AULA14_WORDS = {
    "title": "How often? Adverbs of frequency",
    "lesson": 14,
    "description": "HOW OFTEN…? = Com que frequência…? (o T de often pode ficar mudo: \"ófen\").\n"
                   "Adverbs of frequency (lista fixa, do 100% ao 0%): always (sempre) · often (frequentemente) · "
                   "usually (normalmente) · sometimes (às vezes) · hardly ever (quase nunca) · never (nunca).\n"
                   "Expressions of frequency (flexíveis): once a week (uma vez por semana) · twice a month (duas vezes por mês) · "
                   "three times a year · every day · every other day (dia sim, dia não) · every 15 days (a cada 15 dias).\n"
                   "Uma vez = ONCE (som de \"uans\") · duas vezes = TWICE · a partir de três: three times, four times…",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the adverbs of frequency to Portuguese.",
         "translation": "Ligue os advérbios de frequência ao português.",
         "example": "always → sempre",
         "pairs": [
             {"left": "often", "right": "frequentemente"},
             {"left": "usually", "right": "normalmente"},
             {"left": "sometimes", "right": "às vezes"},
             {"left": "hardly ever", "right": "quase nunca"},
             {"left": "never", "right": "nunca"},
         ]},
        {"type": "match",
         "prompt": "Match the expressions of frequency to Portuguese.",
         "translation": "Ligue as expressões de frequência ao português.",
         "example": "every day → todo dia",
         "pairs": [
             {"left": "once a week", "right": "uma vez por semana"},
             {"left": "twice a month", "right": "duas vezes por mês"},
             {"left": "three times a year", "right": "três vezes por ano"},
             {"left": "every other day", "right": "dia sim, dia não"},
             {"left": "every 15 days", "right": "a cada 15 dias"},
             {"left": "every 4 hours", "right": "a cada 4 horas"},
         ]},
        {"type": "group",
         "prompt": "Adverb or expression of frequency? Put each one in the right group.",
         "translation": "Advérbio (lista fixa) ou expressão de frequência (flexível)? Coloque cada um no grupo certo.",
         "example": "sometimes → adverb · twice a week → expression",
         "categories": ["adverb of frequency", "expression of frequency"],
         "words": [
             {"text": "always", "category": "adverb of frequency"}, {"text": "usually", "category": "adverb of frequency"},
             {"text": "hardly ever", "category": "adverb of frequency"}, {"text": "never", "category": "adverb of frequency"},
             {"text": "once a year", "category": "expression of frequency"},
             {"text": "every other day", "category": "expression of frequency"},
             {"text": "four times a month", "category": "expression of frequency"},
             {"text": "every two months", "category": "expression of frequency"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the right expression.",
         "translation": "Escolha a expressão certa.",
         "example": "uma vez por dia → [once a day]",
         "text": "1. duas vezes por semana → [*twice a week|two a week|twice week]\n"
                 "2. uma vez por ano → [*once a year|one a year|once year]\n"
                 "3. três vezes por mês → [*three times a month|three a month|thrice a month]\n"
                 "4. dia sim, dia não → [*every other day|every day|other every day]\n"
                 "5. a cada 12 horas → [*every 12 hours|once 12 hours|12 times a hour]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Always\" is 100%. → True",
         "statements": [
             {"text": "\"Hardly ever\" means almost never.", "answer": True,
              "translation": "\"Hardly ever\" significa quase nunca."},
             {"text": "We say \"twice times a week\".", "answer": False, "translation": "Dizemos \"twice times a week\"."},
             {"text": "\"Once\" starts with the same sound as \"one\".", "answer": True,
              "translation": "\"Once\" começa com o mesmo som de \"one\"."},
             {"text": "\"Every other day\" means every day.", "answer": False,
              "translation": "\"Every other day\" significa todo dia."},
             {"text": "We say \"once a week\", with \"a\" before week.", "answer": True,
              "translation": "Dizemos \"once a week\", com \"a\" antes de week."},
         ]},
    ],
}

AULA14_PHRASES = {
    "title": "Word order + go, have, get",
    "lesson": 14,
    "description": "Onde fica a frequência na frase?\n"
                   "ADVERB → antes do verbo principal: I hardly ever watch TV. · She usually goes to the gym.\n"
                   "EXPRESSION → normalmente no final: I watch TV twice a week. · I go to the beach three times a year.\n"
                   "Verb phrases: GO to the beach / for a walk / to bed late · HAVE breakfast / a good time (se divertir) / a shower · "
                   "GET up early (levantar) / dressed (se vestir) / home late (chegar) / an email (receber) / a bus (pegar).",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras em ordem. (Ela normalmente vai à academia pela manhã.)",
         "example": "never / They / TV / watch → They never watch TV.",
         "tokens": ["She", "usually", "goes", "to", "the", "gym", "in", "the", "morning."], "alternatives": []},
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras em ordem. (Eu tenho aula de inglês uma vez por semana.)",
         "example": "TV / I / twice a week / watch → I watch TV twice a week.",
         "tokens": ["I", "have", "English", "class", "once", "a", "week."], "alternatives": []},
        {"type": "dropdown",
         "prompt": "Correct or incorrect?",
         "translation": "A frase está correta ou incorreta?",
         "example": "They watch TV never. → [incorrect] (They never watch TV.)",
         "text": "1. I hardly ever go to bed late. → [*correct|incorrect]\n"
                 "2. I take a shower every day. → [*correct|incorrect]\n"
                 "3. She goes always to church. → [*incorrect|correct]\n"
                 "4. We sometimes have a drink after work. → [*correct|incorrect]\n"
                 "5. He gets up early never. → [*incorrect|correct]"},
        {"type": "group",
         "prompt": "Go, have or get? Put each phrase in the right group.",
         "translation": "Go, have ou get? Coloque cada expressão no grupo do verbo certo.",
         "example": "___ to the beach → go",
         "categories": ["go", "have", "get"],
         "words": [
             {"text": "___ for a walk", "category": "go"}, {"text": "___ to the dentist", "category": "go"},
             {"text": "___ to the hairdresser", "category": "go"},
             {"text": "___ breakfast", "category": "have"}, {"text": "___ long hair", "category": "have"},
             {"text": "___ a good time", "category": "have"},
             {"text": "___ dressed", "category": "get"}, {"text": "___ an email", "category": "get"},
             {"text": "___ to the airport", "category": "get"},
         ]},
        {"type": "match",
         "prompt": "Match the verb phrases to Portuguese.",
         "translation": "Ligue as expressões ao português. Repare que o verbo get muda de sentido!",
         "example": "get a taxi → pegar um táxi",
         "pairs": [
             {"left": "get up early", "right": "levantar cedo"},
             {"left": "get home late", "right": "chegar em casa tarde"},
             {"left": "get an email", "right": "receber um e-mail"},
             {"left": "have a good time", "right": "se divertir"},
             {"left": "go for a walk", "right": "fazer uma caminhada"},
             {"left": "go to bed late", "right": "ir dormir tarde"},
         ]},
    ],
}

AULA14_LISTENING = {
    "title": "Listening — how often?",
    "lesson": 14,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the adverb you hear.",
         "translation": "Ouça e escolha o advérbio de frequência que você ouve.",
         "example": "Você ouve: \"I always have breakfast.\" → always",
         "audio": f"{AUDIO}/aula14-adverbs.m4a",
         "text": "1. I [*usually|always|never] get up early.\n"
                 "2. She [*hardly ever|often|always] goes to bed late.\n"
                 "3. We [*sometimes|usually|never] go to a restaurant.\n"
                 "4. They [*never|often|sometimes] watch TV.\n"
                 "5. He [*often|usually|hardly ever] goes for a walk."},
        {"type": "fill",
         "prompt": "Dictation: listen and write the expression of frequency.",
         "translation": "Ditado: ouça e escreva a expressão de frequência.",
         "example": "Você ouve: \"I go to the gym every day.\" → [every day]",
         "audio": f"{AUDIO}/aula14-dictation.m4a",
         "text": "1. I go to the dentist [twice a year].\n"
                 "2. We go to the beach [once a month].\n"
                 "3. She goes running [every other day].\n"
                 "4. I go to the hairdresser [every two months|every 2 months]."},
        {"type": "info",
         "prompt": "Now listen to a survey about healthy habits.",
         "translation": "Agora ouça uma pesquisa sobre hábitos saudáveis: um entrevistador faz perguntas para a Jenny. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula14-survey.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose Jenny's answers.",
         "translation": "Ouça de novo e escolha as respostas da Jenny.",
         "example": "How often does Jenny have breakfast? → [Every day.]",
         "text": "1. How often does she go to the gym? → [*Three times a week.|Twice a week.|Every day.]\n"
                 "2. How often does she go for a walk? → [*Every other day.|Every day.|Once a week.]\n"
                 "3. How often does she eat fast food? → [*Hardly ever.|Always.|Often.]\n"
                 "4. How often does she go to the doctor? → [*Once a year.|Twice a year.|Every month.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the survey.",
         "translation": "Verdadeiro ou falso? Responda de acordo com a pesquisa.",
         "example": "Jenny always has breakfast. → True",
         "statements": [
             {"text": "Jenny usually goes to bed late.", "answer": False,
              "translation": "A Jenny normalmente vai dormir tarde."},
             {"text": "Jenny drinks water every day.", "answer": True, "translation": "A Jenny bebe água todo dia."},
             {"text": "Jenny never watches TV.", "answer": False, "translation": "A Jenny nunca assiste TV."},
         ]},
    ],
}

AULA14_SPEAKING = {
    "title": "Speaking — how often?",
    "lesson": 14,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: OFTEN = \"ófen\" (T mudo) · ONCE = \"uans\" · TWICE = \"tuáis\" · "
                   "DRESSED = \"drést\" (som final de T).",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the adverbs and expressions.",
         "translation": "Ouça e repita os advérbios e as expressões de frequência.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula14-say-w{i}.m4a"} for i, t in enumerate(
             ["always", "often", "usually", "sometimes", "hardly ever", "never", "once a week", "twice a month",
              "every other day", "How often?"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the verb phrases.",
         "translation": "Ouça e repita as expressões com go, have e get.",
         "example": "\"go for a walk\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula14-say-v{i}.m4a"} for i, t in enumerate(
             ["go to the beach", "go for a walk", "go to the hairdresser", "have breakfast", "have a good time",
              "get up early", "get dressed", "get home late"], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOU.",
         "translation": "Agora responda às perguntas sobre VOCÊ com uma frase completa.",
         "example": "\"How often do you watch TV?\" → \"I watch TV every day.\" / \"I hardly ever watch TV.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula14-say-y{i}.m4a"} for i, t in enumerate(
             ["How often do you go to the gym?", "How often do you watch TV?", "How often do you travel by car?",
              "How often do you go to the beach?"], 1)]},
    ],
}

AULA14_READING = {
    "title": "Reading — Grandpa Joe",
    "lesson": 14,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text about Grandpa Joe.",
         "translation": "Leia e ouça o texto sobre o vovô Joe. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula14-reading.m4a",
         "text": "GRANDPA JOE\n\n"
                 "My grandfather Joe is 78 years old, and he has a very active life.\n"
                 "He always gets up early, at 5:30, and he has breakfast with my grandmother.\n"
                 "He goes for a walk every other day, and he goes swimming twice a week.\n"
                 "He never watches TV in the morning, but he sometimes watches soccer at night.\n"
                 "He goes to the doctor every three months, and he goes to the hairdresser once a month.\n"
                 "He hardly ever goes to bed late. He says: \"Early to bed, early to rise!\""},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "How old is Joe? → [78]",
         "text": "1. How often does Joe go swimming? → [*Twice a week.|Every day.|Once a month.]\n"
                 "2. How often does he go for a walk? → [*Every other day.|Every day.|Twice a week.]\n"
                 "3. How often does he go to the doctor? → [*Every three months.|Once a year.|Once a month.]\n"
                 "4. When does he sometimes watch soccer? → [*At night.|In the morning.|On Sundays.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Joe gets up early. → True",
         "statements": [
             {"text": "Joe usually goes to bed late.", "answer": False,
              "translation": "O Joe normalmente vai dormir tarde."},
             {"text": "Joe has breakfast with his wife.", "answer": True,
              "translation": "O Joe toma café da manhã com a esposa."},
             {"text": "Joe watches TV every morning.", "answer": False, "translation": "O Joe assiste TV toda manhã."},
             {"text": "Joe goes to the hairdresser once a month.", "answer": True,
              "translation": "O Joe vai ao cabeleireiro uma vez por mês."},
         ]},
        {"type": "fill",
         "prompt": "Complete with the adverb or expression from the text.",
         "translation": "Complete com o advérbio ou a expressão de frequência do texto.",
         "example": "He [always] gets up early.",
         "text": "1. He [never] watches TV in the morning.\n"
                 "2. He goes swimming [twice a week].\n"
                 "3. He [hardly ever] goes to bed late."},
    ],
}

AULA14_WRITING = {
    "title": "Writing — my habits",
    "lesson": 14,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Adverb ANTES do verbo principal (I never watch TV). "
                   "Expression no FINAL da frase (I watch TV twice a week).",
    "topic": AULA14_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Rewrite the sentences with the adverb in the right place.",
         "translation": "Reescreva as frases colocando o advérbio no lugar certo (antes do verbo principal).",
         "example": "They watch TV. (never) → They never watch TV.",
         "text": "1. I go to bed late. (hardly ever) → [I hardly ever go to bed late.]\n"
                 "2. We have breakfast at home. (usually) → [We usually have breakfast at home.]\n"
                 "3. She goes to the beach. (often) → [She often goes to the beach.]"},
        {"type": "fill",
         "prompt": "Translate the sentences.",
         "translation": "Traduza as frases (expressão de frequência no final).",
         "example": "Eu vou à academia três vezes por semana. → I go to the gym three times a week.",
         "text": "1. Eu vou ao dentista duas vezes por ano. → [I go to the dentist twice a year.]\n"
                 "2. Ela corre dia sim, dia não. → [She goes running every other day.|She runs every other day.]\n"
                 "3. Nós vamos à praia uma vez por mês. → [We go to the beach once a month.]"},
        {"type": "free",
         "prompt": "Write about your habits. How often do you do these things? Use adverbs AND expressions of frequency.",
         "translation": "Escreva sobre os seus hábitos. Com que frequência você faz estas coisas? "
                        "Use advérbios E expressões de frequência (watch TV, go to the gym, go to the beach, get up early…).",
         "example": "I usually get up early. I go to the gym twice a week.",
         "model_answer": "I usually get up early, at 6:30. I always have breakfast at home.\n"
                         "I go to the gym twice a week, and I go for a walk every other day.\n"
                         "I hardly ever watch TV, but I sometimes go to a restaurant with my friends.\n"
                         "I go to the beach once a month.",
         "keywords": ["usually", "always", "sometimes", "a week"], "min_words": 30, "points": 4},
    ],
}

AULA14_VIDEO = _video(14, AULA14_TOPIC, "Video — Nina's week",
                      "a Nina conta com que frequência ela faz as coisas: always, usually, every other day, twice a week…",
                      "aula14-video", [
    _q("How often does Nina get up early?", "Com que frequência a Nina levanta cedo?", "Always.", "Never.", "Sometimes.",
       "Hardly ever."),
    _q("How often does Nina go for a walk?", "Com que frequência a Nina faz uma caminhada?", "Every other day.",
       "Every day.", "Once a week.", "Twice a month."),
    _q("How often does Nina go to the supermarket?", "Com que frequência a Nina vai ao supermercado?", "Once a week.",
       "Twice a week.", "Every day.", "Once a month."),
    _q("Which sentence is correct?", "Qual frase está correta?", "Nina hardly ever goes to a restaurant.",
       "Nina goes hardly ever to a restaurant.", "Nina goes to a restaurant hardly ever.",
       "Hardly ever Nina go to a restaurant."),
    _q("How often does Nina go to the beach?", "Com que frequência a Nina vai à praia?", "Twice a month.",
       "Twice a week.", "Once a year.", "Every other day."),
])


# ---------- Aula 15 — Verb To Be (Countries and Nationalities) (https://youtu.be/JCYicMJhXj8) ----------

AULA15_TOPIC = "Aula 15 — Verb To Be (Countries and Nationalities)"

AULA15_WORDS = {
    "title": "Countries, nationalities, languages",
    "lesson": 15,
    "description": "COUNTRY (país) · NATIONALITY (nacionalidade) · LANGUAGE (língua).\n"
                   "Em inglês, países, nacionalidades E línguas começam SEMPRE com letra maiúscula: Brazilian, Japanese, English.\n"
                   "Brazil → Brazilian (língua: Portuguese) · the USA → American (English) · the UK → British (English) · "
                   "Canada → Canadian (English and French) · Italy → Italian · Japan → Japanese · Mexico → Mexican (Spanish) · "
                   "Portugal → Portuguese · Spain → Spanish · France → French · Germany → German · China → Chinese · "
                   "Switzerland → Swiss (German, French and Italian).\n"
                   "Cuidado: FRANCE é o país, FRENCH é a nacionalidade e a língua.",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the countries to the nationalities.",
         "translation": "Ligue os países às nacionalidades.",
         "example": "Brazil → Brazilian",
         "pairs": [
             {"left": "the UK", "right": "British"},
             {"left": "Japan", "right": "Japanese"},
             {"left": "France", "right": "French"},
             {"left": "Germany", "right": "German"},
             {"left": "Poland", "right": "Polish"},
             {"left": "Switzerland", "right": "Swiss"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the nationality.",
         "translation": "Escolha a nacionalidade.",
         "example": "Mexico → [Mexican]",
         "text": "1. Italy → [*Italian|Italish|Italese]\n"
                 "2. Spain → [*Spanish|Spain|Spaniese]\n"
                 "3. Canada → [*Canadian|Canadish|Canadese]\n"
                 "4. Portugal → [*Portuguese|Portugalian|Portugish]\n"
                 "5. Scotland → [*Scottish|Scotlandian|Scottese]\n"
                 "6. Argentina → [*Argentinian|Argentinese|Argentish]"},
        {"type": "dropdown",
         "prompt": "What language do they speak?",
         "translation": "Que língua eles falam?",
         "example": "Brazil → [Portuguese]",
         "text": "1. Mexico → [*Spanish|Mexican|Portuguese]\n"
                 "2. Australia → [*English|Australian|German]\n"
                 "3. Japan → [*Japanese|Chinese|English]\n"
                 "4. Germany → [*German|Germanish|French]\n"
                 "5. Chile → [*Spanish|Chilean|Portuguese]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Country\" means país. → True",
         "statements": [
             {"text": "In English, we write nationalities with a capital letter: Brazilian.", "answer": True,
              "translation": "Em inglês, escrevemos as nacionalidades com letra maiúscula: Brazilian."},
             {"text": "\"French\" is a country.", "answer": False, "translation": "\"French\" é um país."},
             {"text": "In Canada, people speak English and French.", "answer": True,
              "translation": "No Canadá, as pessoas falam inglês e francês."},
             {"text": "In Brazil, people speak Brazilian.", "answer": False,
              "translation": "No Brasil, as pessoas falam \"brasileiro\"."},
             {"text": "\"The UK\" means the United Kingdom.", "answer": True,
              "translation": "\"The UK\" significa o Reino Unido."},
         ]},
    ],
}

AULA15_TOBE = {
    "title": "Verb to be: am, is, are",
    "lesson": 15,
    "description": "VERB TO BE = ser / estar. I AM (I'm) · you ARE (you're) · he / she / it IS (he's, she's, it's) · "
                   "we ARE (we're) · they ARE (they're).\n"
                   "NEGATIVE: só colocar NOT (sem don't / doesn't!): I am not (I'm not) · is not = ISN'T · are not = AREN'T.\n"
                   "QUESTION: inverta a ordem, o verbo vem antes do sujeito: He is a doctor. → IS HE a doctor? → Yes, he is. / No, he isn't.\n"
                   "Where are you from? → I'm from Brazil. · What nationality are you? → I'm Brazilian. · "
                   "What language do you speak? → I speak Portuguese.",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose am, is or are.",
         "translation": "Escolha am, is ou are.",
         "example": "I [am] a teacher.",
         "text": "1. She [*is|are|am] from China.\n"
                 "2. We [*are|is|am] from South America.\n"
                 "3. I [*am|is|are] Brazilian.\n"
                 "4. John [*is|are|am] a doctor.\n"
                 "5. They [*are|is|am] Canadian.\n"
                 "6. You [*are|is|am] a good student."},
        {"type": "fill",
         "prompt": "Write the contraction.",
         "translation": "Escreva a forma contraída (contraction).",
         "example": "I am → [I'm]",
         "text": "1. she is → [she's]\n2. we are → [we're]\n3. they are → [they're]\n"
                 "4. is not → [isn't]\n5. are not → [aren't]"},
        {"type": "fill",
         "prompt": "Make the sentences negative (use contractions).",
         "translation": "Passe as frases para a negativa (use contractions).",
         "example": "I am Canadian. → I'm not Canadian.",
         "text": "1. He is from Italy. → [He isn't from Italy.|He's not from Italy.]\n"
                 "2. They are Mexican. → [They aren't Mexican.|They're not Mexican.]\n"
                 "3. I am from Spain. → [I'm not from Spain.]"},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Ela é enfermeira?)",
         "example": "he / Is / a doctor → Is he a doctor?",
         "tokens": ["Is", "she", "a", "nurse?"], "alternatives": []},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas.",
         "example": "Are you Brazilian? → Yes, I am.",
         "pairs": [
             {"left": "Where are you from?", "right": "I'm from Brazil."},
             {"left": "What nationality are you?", "right": "I'm Brazilian."},
             {"left": "What language do you speak?", "right": "I speak Portuguese."},
             {"left": "Is he a doctor?", "right": "No, he isn't."},
             {"left": "Are they from Canada?", "right": "Yes, they are."},
         ]},
    ],
}

AULA15_LISTENING = {
    "title": "Listening — where are you from?",
    "lesson": 15,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Repare na sílaba forte: ITaly → itALian.",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Country or nationality? Listen and choose the word you hear.",
         "translation": "País ou nacionalidade? Ouça e escolha a palavra que você ouve.",
         "example": "Você ouve: \"I'm Italian.\" → Italian",
         "audio": f"{AUDIO}/aula15-words.m4a",
         "text": "1. [*France|French]\n2. [*Japanese|Japan]\n3. [*Germany|German]\n4. [*Italian|Italy]\n5. [*China|Chinese]"},
        {"type": "fill",
         "prompt": "Dictation: listen and write the nationality.",
         "translation": "Ditado: ouça e escreva a nacionalidade (lembre: letra maiúscula!).",
         "example": "Você ouve: \"She's Mexican.\" → She's [Mexican].",
         "audio": f"{AUDIO}/aula15-dictation.m4a",
         "text": "1. He's [British].\n2. We're [Brazilian].\n3. They're [Spanish].\n4. I'm [Canadian].\n5. She's [Portuguese]."},
        {"type": "info",
         "prompt": "Now listen: it's the first day at an English school in London.",
         "translation": "Agora ouça: é o primeiro dia numa escola de inglês em Londres. A professora conversa com os alunos novos. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula15-school.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "The teacher's name is [Emma].",
         "text": "1. Where is Carlos from? → [*Mexico.|Spain.|Argentina.]\n"
                 "2. What nationality is Yuki? → [*Japanese.|Chinese.|Korean.]\n"
                 "3. What languages does Luca speak? → [*Italian and German.|Italian and French.|Only Italian.]\n"
                 "4. Where is Marie from? → [*Canada.|France.|Switzerland.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "The school is in London. → True",
         "statements": [
             {"text": "Luca is Italian.", "answer": False, "translation": "O Luca é italiano."},
             {"text": "Marie speaks English and French.", "answer": True, "translation": "A Marie fala inglês e francês."},
             {"text": "Yuki is from Tokyo.", "answer": True, "translation": "A Yuki é de Tóquio."},
         ]},
    ],
}

AULA15_SPEAKING = {
    "title": "Speaking — countries and nationalities",
    "lesson": 15,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: COUNTRY = \"cântri\" · AUSTRALIA = \"ós-TRÊI-lia\" (AU soa como \"ó\") · "
                   "ITaly × itALian (a sílaba forte muda) · ISN'T, AREN'T: use as contrações quando falar.",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the countries.",
         "translation": "Ouça e repita os países.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula15-say-c{i}.m4a"} for i, t in enumerate(
             ["Brazil", "the USA", "the UK", "Canada", "Italy", "Japan", "Germany", "France", "Australia", "Switzerland"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the nationalities.",
         "translation": "Ouça e repita as nacionalidades.",
         "example": "\"Brazilian\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula15-say-n{i}.m4a"} for i, t in enumerate(
             ["Brazilian", "American", "British", "Canadian", "Italian", "Japanese", "German", "French", "Australian", "Swiss"], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOU.",
         "translation": "Agora responda às perguntas sobre VOCÊ com uma frase completa.",
         "example": "\"Where are you from?\" → \"I'm from Brazil. I'm from Recife.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula15-say-y{i}.m4a"} for i, t in enumerate(
             ["Where are you from?", "What nationality are you?", "What language do you speak?", "Are you a teacher?"], 1)]},
    ],
}

AULA15_READING = {
    "title": "Reading — friends around the world",
    "lesson": 15,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Bruna's text.",
         "translation": "Leia e ouça o texto da Bruna. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula15-reading.m4a",
         "text": "FRIENDS AROUND THE WORLD\n\n"
                 "Hi! I'm Bruna. I'm Brazilian, and I'm from Salvador. I'm a tour guide.\n"
                 "I have friends from many countries. Kenji is from Japan. He's Japanese, and he speaks Japanese and English.\n"
                 "Anna and Paul are from Germany. They're German, but they live in Switzerland now.\n"
                 "Sophie isn't French. She's Canadian! She's from Montreal, and she speaks English and French.\n"
                 "And Diego? He's from Argentina. He speaks Spanish and a little Portuguese.\n"
                 "We're from different countries, but we're good friends!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "What does Bruna do? → [She's a tour guide.]",
         "text": "1. Where is Bruna from? → [*Salvador.|Montreal.|Argentina.]\n"
                 "2. What nationality are Anna and Paul? → [*German.|Swiss.|French.]\n"
                 "3. What languages does Kenji speak? → [*Japanese and English.|Japanese and Chinese.|Only Japanese.]\n"
                 "4. Where is Diego from? → [*Argentina.|Spain.|Mexico.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Bruna is Brazilian. → True",
         "statements": [
             {"text": "Sophie is French.", "answer": False, "translation": "A Sophie é francesa."},
             {"text": "Anna and Paul live in Switzerland.", "answer": True, "translation": "A Anna e o Paul moram na Suíça."},
             {"text": "Diego speaks a little Portuguese.", "answer": True,
              "translation": "O Diego fala um pouco de português."},
             {"text": "Kenji is Chinese.", "answer": False, "translation": "O Kenji é chinês."},
         ]},
        {"type": "fill",
         "prompt": "Complete with am, is or are (or the negative) according to the text.",
         "translation": "Complete com am, is ou are (ou com a negativa) de acordo com o texto.",
         "example": "Bruna [is] a tour guide.",
         "text": "1. Kenji [is] from Japan.\n"
                 "2. Anna and Paul [are] German.\n"
                 "3. Sophie [isn't|is not] French.\n"
                 "4. They [are] good friends."},
    ],
}

AULA15_WRITING = {
    "title": "Writing — about me and my friends",
    "lesson": 15,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ COUNTRY → be FROM (I'm from Brazil) · NATIONALITY → be + adjetivo (I'm Brazilian) · "
                   "LANGUAGE → SPEAK (I speak Portuguese / she speaks Chinese).",
    "topic": AULA15_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write three sentences: country, nationality and language.",
         "translation": "Escreva três frases sobre as pessoas: país, nacionalidade e língua.",
         "example": "They / Canada → They are from Canada. They are Canadian. They speak English.",
         "text": "1. She / Japan → She is from [Japan]. She is [Japanese]. She speaks [Japanese].\n"
                 "2. We / Mexico → We are from [Mexico]. We are [Mexican]. We speak [Spanish].\n"
                 "3. He / France → He is from [France]. He is [French]. He speaks [French]."},
        {"type": "fill",
         "prompt": "Write the questions in English.",
         "translation": "Escreva as perguntas em inglês (verbo antes do sujeito).",
         "example": "Ele é médico? → Is he a doctor?",
         "text": "1. Você é brasileiro? → [Are you Brazilian?]\n"
                 "2. Eles são da Itália? → [Are they from Italy?]\n"
                 "3. Ela é professora? → [Is she a teacher?]"},
        {"type": "free",
         "prompt": "Write about you and two people you know: country, nationality and language.",
         "translation": "Escreva sobre você e duas pessoas que você conhece: país (from), nacionalidade e língua (speak).",
         "example": "I'm from Brazil. I'm Brazilian, and I speak Portuguese.",
         "model_answer": "I'm from Brazil. I'm Brazilian, and I speak Portuguese and a little English.\n"
                         "My friend Lucía is from Chile. She's Chilean, and she speaks Spanish.\n"
                         "My cousin Pedro lives in Portugal, but he isn't Portuguese. He's Brazilian too!",
         "keywords": ["from", "speak", "I'm"], "min_words": 30, "points": 4},
    ],
}

AULA15_VIDEO = _video(15, AULA15_TOPIC, "Video — Where are you from?",
                      "turistas do mundo todo se apresentam: country, nationality e language com o verb to be.",
                      "aula15-video", [
    _q("Where is Yuki from?", "De onde a Yuki é?", "She's from Japan.", "She's from China.", "She's from Canada.",
       "She's from Italy."),
    _q("What nationality is Marco?", "Qual a nacionalidade do Marco?", "He's Italian.", "He's Spanish.",
       "He's Mexican.", "He's Swiss."),
    _q("Is Claire French?", "A Claire é francesa?", "No, she isn't. She's Canadian.", "Yes, she is.",
       "No, she doesn't.", "Yes, she does."),
    _q("What languages does Claire speak?", "Que línguas a Claire fala?", "English and French.", "Only French.",
       "English and Spanish.", "French and Italian."),
    _q("Where are the two friends from?", "De onde são os dois amigos?", "They're from Mexico.", "They're from Spain.",
       "They're from Brazil.", "They're from the USA."),
])


# ---------- Aula 16 — Verb To Be (Feelings) (https://youtu.be/7P6M7cCeYeo) ----------

AULA16_TOPIC = "Aula 16 — Verb To Be (Feelings)"

AULA16_WORDS = {
    "title": "Feelings",
    "lesson": 16,
    "description": "FEELINGS = sentimentos. São adjetivos e vão com o verb to be (ou com o verbo feel):\n"
                   "I am happy = I'm happy = I feel happy.\n"
                   "Em português: ESTOU COM fome / sono / frio / medo. Em inglês, direto o adjetivo: I'm hungry / sleepy / cold / scared.\n"
                   "Cuidado: ANGRY (com raiva) ≠ HUNGRY (com fome, H aspirado) · SLEEP (dormir) ≠ SLEEPY (com sono).\n"
                   "Silent letter: bored = \"bórd\", tired = \"táierd\" (o E não é lido).",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the feelings to Portuguese.",
         "translation": "Ligue os sentimentos ao português.",
         "example": "happy → feliz",
         "pairs": [
             {"left": "sad", "right": "triste"},
             {"left": "scared", "right": "com medo"},
             {"left": "angry", "right": "com raiva"},
             {"left": "bored", "right": "entediado"},
             {"left": "excited", "right": "animado"},
             {"left": "shy", "right": "tímido"},
         ]},
        {"type": "match",
         "prompt": "Match more feelings to Portuguese.",
         "translation": "Ligue mais sentimentos ao português.",
         "example": "tired → cansado",
         "pairs": [
             {"left": "thirsty", "right": "com sede"},
             {"left": "sleepy", "right": "com sono"},
             {"left": "proud", "right": "orgulhoso"},
             {"left": "lonely", "right": "solitário"},
             {"left": "confused", "right": "confuso"},
             {"left": "surprised", "right": "surpreso"},
         ]},
        {"type": "dropdown",
         "prompt": "How do they feel? Choose the right word.",
         "translation": "Como eles se sentem? Escolha a palavra certa.",
         "example": "Estou com frio. → I'm [cold].",
         "text": "1. Estou com fome. → I'm [*hungry|angry|thirsty].\n"
                 "2. Ela está com raiva. → She's [*angry|hungry|scared].\n"
                 "3. Estamos com calor. → We're [*hot|cold|tired].\n"
                 "4. O bebê está com sono. → The baby is [*sleepy|sleep|bored].\n"
                 "5. Eles estão com medo. → They're [*scared|shy|sad].\n"
                 "6. Estou com sede. → I'm [*thirsty|hungry|hot]."},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"I'm happy\" and \"I feel happy\" are both correct. → True",
         "statements": [
             {"text": "In \"bored\" and \"tired\", we don't say the letter E.", "answer": True,
              "translation": "Em \"bored\" e \"tired\", a gente não pronuncia a letra E."},
             {"text": "\"Angry\" and \"hungry\" mean the same thing.", "answer": False,
              "translation": "\"Angry\" e \"hungry\" significam a mesma coisa."},
             {"text": "To say \"estou com sono\", we say \"I'm sleepy\".", "answer": True,
              "translation": "Para dizer \"estou com sono\", dizemos \"I'm sleepy\"."},
             {"text": "\"Shy\" is only for women.", "answer": False, "translation": "\"Shy\" é só para mulheres."},
             {"text": "\"Lonely\" is a sad word.", "answer": True, "translation": "\"Lonely\" é uma palavra triste."},
         ]},
    ],
}

AULA16_SENTENCES = {
    "title": "I'm tired / I feel tired",
    "lesson": 16,
    "description": "Duas formas de falar dos sentimentos:\n"
                   "VERB TO BE: I am sad · She is tired · They are happy → NEGATIVE com NOT: I'm not sad · She isn't tired · They aren't happy.\n"
                   "FEEL: I feel sad · She FEELS tired (he / she / it → S) → NEGATIVE com DON'T / DOESN'T: I don't feel sad · She doesn't feel tired.\n"
                   "Perguntas: Are you tired? → Yes, I am. / No, I'm not. · How do you feel? → I feel great!\n"
                   "Pronúncia: FEEL (sentir, som longo \"fiil\") ≠ FILL (encher).",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose the right word.",
         "translation": "Escolha a palavra certa.",
         "example": "She [is] tired. / She [feels] tired.",
         "text": "1. I [*am|is|are] happy today.\n"
                 "2. He [*feels|feel|is feel] tired.\n"
                 "3. They [*are|is|am] excited about the trip.\n"
                 "4. We [*feel|feels|are feel] relaxed on the weekend.\n"
                 "5. My sister [*is|are|am] shy."},
        {"type": "dropdown",
         "prompt": "Negative: not or don't / doesn't?",
         "translation": "Negativa: com o verb to be só NOT; com feel, DON'T / DOESN'T.",
         "example": "I'm not sad. / I don't feel sad.",
         "text": "1. She [*isn't|doesn't] angry.\n"
                 "2. She [*doesn't|isn't] feel angry.\n"
                 "3. You [*aren't|don't] bored.\n"
                 "4. You [*don't|aren't] feel bored.\n"
                 "5. I [*am not|don't] cold."},
        {"type": "fill",
         "prompt": "Write the sentence in the other way.",
         "translation": "Reescreva a frase do outro jeito: verb to be ↔ feel.",
         "example": "I am happy. → I feel happy.",
         "text": "1. He is tired. → [He feels tired.]\n"
                 "2. I am not sad. → [I don't feel sad.]\n"
                 "3. She feels scared. → [She is scared.|She's scared.]"},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Você está com fome?)",
         "example": "tired / Are / they → Are they tired?",
         "tokens": ["Are", "you", "hungry?"], "alternatives": []},
        {"type": "match",
         "prompt": "Match the situations to the feelings.",
         "translation": "Ligue as situações aos sentimentos.",
         "example": "It's my birthday! → I'm happy.",
         "pairs": [
             {"left": "It's 2 a.m., and I'm at work.", "right": "I'm sleepy."},
             {"left": "It's 40 °C today.", "right": "I'm hot."},
             {"left": "I don't understand the exercise.", "right": "I'm confused."},
             {"left": "My son is a doctor now!", "right": "I'm proud."},
             {"left": "I have nothing to do at home.", "right": "I'm bored."},
         ]},
    ],
}

AULA16_LISTENING = {
    "title": "Listening — how do you feel?",
    "lesson": 16,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Atenção: ANGRY ≠ HUNGRY · SLEEP ≠ SLEEPY · FEEL ≠ FILL.",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the word you hear.",
         "translation": "Ouça e escolha a palavra que você ouve.",
         "example": "Você ouve: \"I'm angry.\" → angry",
         "audio": f"{AUDIO}/aula16-pairs.m4a",
         "text": "1. I'm [*hungry|angry].\n2. The baby is [*sleepy|sleep].\n3. She's [*angry|hungry].\n"
                 "4. I [*feel|fill] good.\n5. We're [*sad|scared]."},
        {"type": "fill",
         "prompt": "Dictation: listen and write the feeling.",
         "translation": "Ditado: ouça e escreva o sentimento.",
         "example": "Você ouve: \"I'm happy.\" → I'm [happy].",
         "audio": f"{AUDIO}/aula16-dictation.m4a",
         "text": "1. I'm [bored].\n2. She's [excited].\n3. They're [thirsty].\n4. He's [scared].\n5. We're [cold]."},
        {"type": "info",
         "prompt": "Now listen to Tom and Lisa on the phone.",
         "translation": "Agora ouça o Tom e a Lisa conversando ao telefone. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula16-phone.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Lisa is at [home].",
         "text": "1. How does Tom feel? → [*Tired and hungry.|Happy and excited.|Cold and sleepy.]\n"
                 "2. Why is Lisa excited? → [*Because she has a new job.|Because it's her birthday.|Because she goes to Italy.]\n"
                 "3. How does Lisa feel about the first day? → [*A little scared.|Bored.|Angry.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Tom and Lisa are friends. → True",
         "statements": [
             {"text": "Tom works twelve hours today.", "answer": True, "translation": "O Tom trabalha doze horas hoje."},
             {"text": "Lisa is sad.", "answer": False, "translation": "A Lisa está triste."},
             {"text": "Tom is proud of Lisa.", "answer": True, "translation": "O Tom está orgulhoso da Lisa."},
         ]},
    ],
}

AULA16_SPEAKING = {
    "title": "Speaking — feelings",
    "lesson": 16,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: BORED = \"bórd\" · TIRED = \"táierd\" · HUNGRY = \"RRânGri\" (H aspirado) · ANGRY = \"ênGri\" · "
                   "FEEL = \"fiil\" (som longo).",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the feelings.",
         "translation": "Ouça e repita os sentimentos.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula16-say-w{i}.m4a"} for i, t in enumerate(
             ["happy", "sad", "scared", "angry", "hungry", "bored", "excited", "tired", "sleepy", "thirsty", "proud",
              "lonely"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases.",
         "example": "\"I'm hungry.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula16-say-s{i}.m4a"} for i, t in enumerate(
             ["I feel happy.", "I'm cold.", "She isn't angry.", "He doesn't feel tired.", "Are you hungry?",
              "The baby is sleepy."], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOU.",
         "translation": "Agora responda às perguntas sobre VOCÊ com uma frase completa.",
         "example": "\"How do you feel today?\" → \"I feel great!\" / \"I'm a little tired.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula16-say-y{i}.m4a"} for i, t in enumerate(
             ["How do you feel today?", "Are you hungry now?", "Are you shy?", "How do you feel on Mondays?"], 1)]},
    ],
}

AULA16_READING = {
    "title": "Reading — a long day",
    "lesson": 16,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Rafael's text.",
         "translation": "Leia e ouça o texto do Rafael. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula16-reading.m4a",
         "text": "A LONG DAY\n\n"
                 "I'm Rafael, and today is a long day.\n"
                 "In the morning, I'm sleepy because I go to bed late every night.\n"
                 "At 10 o'clock, I have a meeting with my boss. I'm a little scared, but the meeting is good. He's happy with my work, and I feel proud!\n"
                 "At lunch, I'm very hungry. I eat a big sandwich.\n"
                 "In the afternoon, I'm bored. My work isn't interesting on Fridays.\n"
                 "At 7 p.m., I get home. I'm tired, but I'm not sad: tomorrow is Saturday, and I go to the beach with my friends. I'm excited!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Is today a long day? → [Yes, it is.]",
         "text": "1. Why is Rafael sleepy in the morning? → [*Because he goes to bed late.|Because he works at night.|Because he is bored.]\n"
                 "2. How does he feel before the meeting? → [*A little scared.|Excited.|Angry.]\n"
                 "3. How does he feel after the meeting? → [*Proud.|Sad.|Confused.]\n"
                 "4. Why is he excited? → [*Because he goes to the beach tomorrow.|Because it's lunch time.|Because he has a meeting.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Rafael's boss is happy. → True",
         "statements": [
             {"text": "Rafael is hungry at lunch.", "answer": True, "translation": "O Rafael está com fome no almoço."},
             {"text": "He is excited in the afternoon.", "answer": False, "translation": "Ele está animado à tarde."},
             {"text": "He is sad at 7 p.m.", "answer": False, "translation": "Ele está triste às 7 da noite."},
         ]},
        {"type": "fill",
         "prompt": "Complete with the feeling from the text.",
         "translation": "Complete com o sentimento do texto.",
         "example": "In the morning, Rafael is [sleepy].",
         "text": "1. At lunch, he is very [hungry].\n"
                 "2. In the afternoon, he is [bored].\n"
                 "3. At 7 p.m., he is [tired]."},
    ],
}

AULA16_WRITING = {
    "title": "Writing — how do you feel?",
    "lesson": 16,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ I'm / I feel + feeling. Negativa: I'm not… / I don't feel…\n"
                   "Lembre: \"estou com fome\" = I'm hungry (sem \"with\"!).",
    "topic": AULA16_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate the sentences.",
         "translation": "Traduza as frases.",
         "example": "Estou com frio. → I'm cold.",
         "text": "1. Estou com fome. → [I'm hungry.|I am hungry.]\n"
                 "2. Ela está com sono. → [She's sleepy.|She is sleepy.]\n"
                 "3. Nós estamos animados. → [We're excited.|We are excited.]\n"
                 "4. Eles não estão com medo. → [They aren't scared.|They're not scared.|They are not scared.]"},
        {"type": "fill",
         "prompt": "Write the questions in English.",
         "translation": "Escreva as perguntas em inglês.",
         "example": "Você está cansado? → Are you tired?",
         "text": "1. Você está com sede? → [Are you thirsty?]\n"
                 "2. Ele está com raiva? → [Is he angry?]\n"
                 "3. Como você se sente? → [How do you feel?]"},
        {"type": "free",
         "prompt": "How do you feel in these situations? On Monday morning, on your birthday, at the dentist, "
                   "at 11 p.m., on a hot day…",
         "translation": "Como você se sente nestas situações? Na segunda de manhã, no seu aniversário, no dentista, "
                        "às 11 da noite, num dia quente… Use I'm / I feel e pelo menos uma negativa.",
         "example": "On Monday morning, I'm sleepy.",
         "model_answer": "On Monday morning, I'm sleepy and a little bored.\n"
                         "On my birthday, I feel happy and excited.\n"
                         "At the dentist, I'm scared!\n"
                         "At 11 p.m., I'm tired. On a hot day, I'm thirsty, but I'm not sad: I go to the beach!",
         "keywords": ["I'm", "I feel", "not"], "min_words": 30, "points": 4},
    ],
}

AULA16_VIDEO = _video(16, AULA16_TOPIC, "Video — How do they feel?",
                      "pessoas reais em situações do dia a dia: happy, tired, hungry, cold, sleepy, proud…",
                      "aula16-video", [
    _q("How does Ana feel?", "Como a Ana se sente?", "She's happy.", "She's sad.", "She's angry.", "She's scared."),
    _q("Why is Paulo tired?", "Por que o Paulo está cansado?", "Because he works ten hours a day.",
       "Because he goes to the gym.", "Because he is cold.", "Because he plays soccer."),
    _q("Is Helen hot?", "A Helen está com calor?", "No, she isn't. She's cold.", "Yes, she is.",
       "No, she doesn't.", "Yes, she does."),
    _q("How does the little boy feel?", "Como o menininho se sente?", "He's sleepy.", "He's hungry.", "He's angry.",
       "He's excited."),
    _q("Why is Marta proud?", "Por que a Marta está orgulhosa?", "Because her daughter is a doctor now.",
       "Because her daughter is hungry.", "Because it's her birthday.", "Because she is a teacher."),
])


# ---------- Aula 17 — Verb To Be (Physical Appearance) (https://youtu.be/6wT2VOuBui8) ----------

AULA17_TOPIC = "Aula 17 — Verb To Be (Physical Appearance)"

AULA17_WORDS = {
    "title": "Physical appearance",
    "lesson": 17,
    "description": "Com o VERB TO BE (ser / estar):\n"
                   "Body type: thin / slim (magro) · chubby (cheinho) · overweight (acima do peso — mais educado que fat).\n"
                   "Height: short (baixo) · tall (alto) · medium height (altura média).\n"
                   "Age: young (jovem) · grown-up (adulto) · middle-aged (de meia-idade) · old (idoso).\n"
                   "BALD (careca) também vai com to be: He is bald.\n"
                   "Short answers: Is she old? → Yes, she is. (sem contraction no YES!) / No, she isn't.",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the words to Portuguese.",
         "translation": "Ligue as palavras ao português.",
         "example": "tall → alto",
         "pairs": [
             {"left": "thin", "right": "magro"},
             {"left": "chubby", "right": "cheinho"},
             {"left": "short", "right": "baixo"},
             {"left": "middle-aged", "right": "de meia-idade"},
             {"left": "young", "right": "jovem"},
             {"left": "bald", "right": "careca"},
         ]},
        {"type": "group",
         "prompt": "Body type, height or age? Put each word in the right group.",
         "translation": "Tipo de corpo, altura ou idade? Coloque cada palavra no grupo certo.",
         "example": "slim → body type",
         "categories": ["body type", "height", "age"],
         "words": [
             {"text": "thin", "category": "body type"}, {"text": "chubby", "category": "body type"},
             {"text": "overweight", "category": "body type"},
             {"text": "tall", "category": "height"}, {"text": "short", "category": "height"},
             {"text": "medium height", "category": "height"},
             {"text": "young", "category": "age"}, {"text": "grown-up", "category": "age"},
             {"text": "old", "category": "age"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the right short answer.",
         "translation": "Escolha a resposta curta certa.",
         "example": "Is she old? → [No, she isn't.]",
         "text": "1. Is he tall? (✓) → [*Yes, he is.|Yes, he's.|Yes, he does.]\n"
                 "2. Are they young? (✗) → [*No, they aren't.|No, they don't.|No, they isn't.]\n"
                 "3. Is your father bald? (✓) → [*Yes, he is.|Yes, he has.|Yes, he's.]\n"
                 "4. Are you medium height? (✓) → [*Yes, I am.|Yes, I'm.|Yes, I do.]\n"
                 "5. Is she thin? (✗) → [*No, she isn't.|No, she doesn't.|No, she not.]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Tall\" is the opposite of \"short\". → True",
         "statements": [
             {"text": "\"Short\" can mean baixo or curto.", "answer": True,
              "translation": "\"Short\" pode significar baixo ou curto."},
             {"text": "\"Yes, he's.\" is a correct short answer.", "answer": False,
              "translation": "\"Yes, he's.\" é uma resposta curta correta."},
             {"text": "Many people prefer \"overweight\" to \"fat\".", "answer": True,
              "translation": "Muitas pessoas preferem \"overweight\" a \"fat\"."},
             {"text": "\"Middle-aged\" means very young.", "answer": False,
              "translation": "\"Middle-aged\" significa muito jovem."},
         ]},
    ],
}

AULA17_HAIR = {
    "title": "Hair, eyes and face",
    "lesson": 17,
    "description": "Com o verbo HAVE (ter) → he / she / it HAS:\n"
                   "Hair length: long · short · shoulder-length (na altura dos ombros) · a pixie cut (sem \"hair\").\n"
                   "Hair style: straight (liso) · wavy (ondulado) · curly (cacheado).\n"
                   "Hair color: black · brown (castanho) · red (ruivo) · blond · grey (grisalho) · white.\n"
                   "Eyes (\"áiz\"): brown · blue · green · hazel (cor de mel).\n"
                   "Face: beard (barba, ≠ bird, pássaro) · mustache (bigode) · goatee (cavanhaque) · sideburns (costeletas) · "
                   "freckles (sardas) · wrinkles (rugas).\n"
                   "ORDEM: o adjetivo vem ANTES — style + color + hair: She has WAVY BROWN hair. · I have BLUE eyes.\n"
                   "Pergunta com have: Does he have a beard? → Yes, he does. / No, he doesn't.",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the words to Portuguese.",
         "translation": "Ligue as palavras ao português.",
         "example": "curly → cacheado",
         "pairs": [
             {"left": "straight", "right": "liso"},
             {"left": "wavy", "right": "ondulado"},
             {"left": "beard", "right": "barba"},
             {"left": "mustache", "right": "bigode"},
             {"left": "freckles", "right": "sardas"},
             {"left": "wrinkles", "right": "rugas"},
         ]},
        {"type": "dropdown",
         "prompt": "Is, has or have?",
         "translation": "Is, has ou have? Lembre: cabelo, olhos e barba → have / has; careca, alto, jovem → is.",
         "example": "She [has] long hair.",
         "text": "1. He [*is|has|have] bald.\n"
                 "2. My mother [*has|have|is] green eyes.\n"
                 "3. I [*have|has|am] brown eyes.\n"
                 "4. She [*is|has|have] tall.\n"
                 "5. My father [*has|have|is] a beard.\n"
                 "6. They [*have|has|are] curly hair."},
        {"type": "order",
         "prompt": "Put the words in order (style + color + hair).",
         "translation": "Coloque as palavras em ordem: estilo + cor + hair. (Ela tem cabelo castanho ondulado.)",
         "example": "red / curly / hair / has / She → She has curly red hair.",
         "tokens": ["She", "has", "wavy", "brown", "hair."], "alternatives": []},
        {"type": "order",
         "prompt": "Put the words in order (style + color + hair).",
         "translation": "Coloque as palavras em ordem. (Ele tem cabelo preto liso.)",
         "example": "blond / straight / hair / has / He → He has straight blond hair.",
         "tokens": ["He", "has", "straight", "black", "hair."], "alternatives": []},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza (adjetivo antes do substantivo!).",
         "example": "cabelo comprido → long hair",
         "text": "1. olhos azuis → [blue eyes]\n2. cabelo cacheado → [curly hair]\n3. cabelo ruivo → [red hair]\n"
                 "4. cabelo grisalho → [grey hair|gray hair]"},
    ],
}

AULA17_LISTENING = {
    "title": "Listening — who is it?",
    "lesson": 17,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Atenção: BEARD (barba) ≠ BIRD (pássaro).",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the word you hear.",
         "translation": "Ouça e escolha a palavra que você ouve.",
         "example": "Você ouve: \"She has long hair.\" → long",
         "audio": f"{AUDIO}/aula17-words.m4a",
         "text": "1. He has a [*beard|bird].\n2. She has [*curly|wavy] hair.\n3. He is [*tall|short].\n"
                 "4. I have [*hazel|brown] eyes.\n5. She is [*thin|chubby]."},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete a descrição.",
         "example": "Você ouve: \"She has blue eyes.\" → She has [blue] eyes.",
         "audio": f"{AUDIO}/aula17-dictation.m4a",
         "text": "1. My brother has [straight] black hair.\n2. My grandmother has [white] hair and [wrinkles].\n"
                 "3. Ana has [freckles] and [green] eyes.\n4. Mr. Silva is [bald]."},
        {"type": "info",
         "prompt": "Now listen: Paula meets her cousin at the airport.",
         "translation": "Agora ouça: a Paula precisa buscar o primo dela, o Leo, no aeroporto, mas ela não lembra como ele é. "
                        "Ela liga para o tio. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula17-airport.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Leo is Paula's [cousin].",
         "text": "1. Is Leo tall? → [*Yes, he is.|No, he isn't.|Yes, he does.]\n"
                 "2. What hair does Leo have? → [*Short curly black hair.|Long straight blond hair.|He is bald.]\n"
                 "3. Does Leo have a beard? → [*Yes, he does.|No, he doesn't.|No, he isn't.]\n"
                 "4. What color are his eyes? → [*Green.|Brown.|Blue.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Paula calls her uncle. → True",
         "statements": [
             {"text": "Leo is old.", "answer": False, "translation": "O Leo é idoso."},
             {"text": "Leo has a mustache.", "answer": False, "translation": "O Leo tem bigode."},
             {"text": "Leo is thin.", "answer": True, "translation": "O Leo é magro."},
         ]},
    ],
}

AULA17_SPEAKING = {
    "title": "Speaking — describing people",
    "lesson": 17,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: HAIR = \"rrér\" (H aspirado) · EYES = \"áiz\" · BEARD = \"bírd\" (≠ BIRD \"bârd\") · "
                   "Yes, he is (sem contraction!).",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the words.",
         "translation": "Ouça e repita as palavras.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula17-say-w{i}.m4a"} for i, t in enumerate(
             ["tall", "short", "thin", "middle-aged", "bald", "straight", "wavy", "curly", "blond", "hazel eyes",
              "beard", "freckles"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases.",
         "example": "\"She has wavy brown hair.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula17-say-s{i}.m4a"} for i, t in enumerate(
             ["She has wavy brown hair.", "He is tall and thin.", "My mother has green eyes.", "Is she old? No, she isn't.",
              "Does he have a beard? Yes, he does."], 1)]},
        {"type": "speak",
         "prompt": "Now describe YOU.",
         "translation": "Agora fale sobre VOCÊ com uma frase completa.",
         "example": "\"What color are your eyes?\" → \"I have brown eyes.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula17-say-y{i}.m4a"} for i, t in enumerate(
             ["Are you tall?", "What hair do you have?", "What color are your eyes?", "Describe your best friend."], 1)]},
    ],
}

AULA17_READING = {
    "title": "Reading — a family photo",
    "lesson": 17,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Clara's text about a family photo.",
         "translation": "Leia e ouça o texto da Clara sobre uma foto da família. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula17-reading.m4a",
         "text": "A FAMILY PHOTO\n\n"
                 "This is a photo of my family on my birthday.\n"
                 "My father is tall and a little chubby. He's middle-aged, and he has a grey beard and a mustache.\n"
                 "My mother is short and slim. She has long wavy brown hair and hazel eyes.\n"
                 "My grandfather is old, and he's bald. He has a lot of wrinkles, but he's always happy!\n"
                 "My brother, Pedro, is young. He's eleven. He has short curly red hair and freckles.\n"
                 "And me? I'm medium height. I have shoulder-length straight black hair and brown eyes."},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Is Clara's mother tall? → [No, she isn't.]",
         "text": "1. What does Clara's father have? → [*A grey beard and a mustache.|Long hair.|Freckles.]\n"
                 "2. What hair does her mother have? → [*Long wavy brown hair.|Short curly red hair.|Straight black hair.]\n"
                 "3. Is her grandfather bald? → [*Yes, he is.|No, he isn't.|Yes, he does.]\n"
                 "4. Who has freckles? → [*Pedro.|Clara.|Her father.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Pedro is young. → True",
         "statements": [
             {"text": "Clara's mother has blue eyes.", "answer": False, "translation": "A mãe da Clara tem olhos azuis."},
             {"text": "Clara's father is tall.", "answer": True, "translation": "O pai da Clara é alto."},
             {"text": "Clara has curly hair.", "answer": False, "translation": "A Clara tem cabelo cacheado."},
             {"text": "Clara's grandfather has wrinkles.", "answer": True, "translation": "O avô da Clara tem rugas."},
         ]},
        {"type": "fill",
         "prompt": "Complete with is or has, according to the text.",
         "translation": "Complete com is ou has, de acordo com o texto.",
         "example": "Clara's mother [is] short.",
         "text": "1. Her grandfather [is] bald.\n2. Pedro [has] freckles.\n3. Her father [is] middle-aged.\n"
                 "4. Her mother [has] hazel eyes."},
    ],
}

AULA17_WRITING = {
    "title": "Writing — describe a person",
    "lesson": 17,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ BE: tall, short, thin, young, old, bald… · HAVE / HAS: hair, eyes, beard, freckles…\n"
                   "Ordem: style + color + hair (She has curly red hair).",
    "topic": AULA17_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate the sentences.",
         "translation": "Traduza as frases.",
         "example": "Eu tenho olhos castanhos. → I have brown eyes.",
         "text": "1. Ela é alta e magra. → [She is tall and thin.|She's tall and thin.|She is tall and slim.|She's tall and slim.]\n"
                 "2. Ele tem barba. → [He has a beard.]\n"
                 "3. Minha mãe tem cabelo loiro cacheado. → [My mother has curly blond hair.|My mother has curly blonde hair.]"},
        {"type": "fill",
         "prompt": "Write the questions in English.",
         "translation": "Escreva as perguntas em inglês (be → Is he…? / have → Does he have…?).",
         "example": "Ela é jovem? → Is she young?",
         "text": "1. Ele é careca? → [Is he bald?]\n"
                 "2. Ela tem olhos verdes? → [Does she have green eyes?]\n"
                 "3. Eles são altos? → [Are they tall?]"},
        {"type": "free",
         "prompt": "Describe yourself and a person in your family: height, body, age, hair, eyes, face.",
         "translation": "Descreva você e uma pessoa da sua família: altura, corpo, idade, cabelo, olhos, rosto.",
         "example": "I'm medium height. I have straight brown hair.",
         "model_answer": "I'm medium height and slim. I have long straight brown hair and brown eyes.\n"
                         "My father is tall and a little chubby. He's middle-aged.\n"
                         "He has short grey hair, blue eyes and a beard. He isn't bald!",
         "keywords": ["have", "hair", "eyes", "has"], "min_words": 30, "points": 4},
    ],
}

AULA17_VIDEO = _video(17, AULA17_TOPIC, "Video — Who is who?",
                      "a Bruna apresenta a família e os vizinhos: young, old, curly hair, beard, wrinkles…",
                      "aula17-video", [
    _q("What hair does Sara have?", "Que cabelo a Sara tem?", "Long curly hair.", "Short straight hair.",
       "A pixie cut.", "She is bald."),
    _q("Does Mr. Gomes have a beard?", "O Sr. Gomes tem barba?", "Yes, he does.", "No, he doesn't.", "Yes, he is.",
       "No, he isn't."),
    _q("What hair does Lucy have?", "Que cabelo a Lucy tem?", "Short straight blond hair.", "Long curly red hair.",
       "Long wavy black hair.", "She is bald."),
    _q("Is Grandma Rosa young?", "A vovó Rosa é jovem?", "No, she isn't. She's old.", "Yes, she is.",
       "No, she doesn't.", "Yes, she has."),
    _q("Which sentence is correct?", "Qual frase está correta?", "Tom has short blond hair.", "Tom has hair short blond.",
       "Tom is short blond hair.", "Tom have short blond hair."),
])


# ---------- Aula 18 — Verb To Be (Family Members) (https://youtu.be/A_Arhh7I7Zw) ----------

AULA18_TOPIC = "Aula 18 — Verb To Be (Family Members)"

AULA18_WORDS = {
    "title": "Family members",
    "lesson": 18,
    "description": "NUCLEAR FAMILY: mother (mom) · father (dad) · wife (esposa) · husband (marido) · daughter (filha) · son (filho) · "
                   "sister · brother.\n"
                   "Palavras que juntam os dois (neutras): PARENTS = pai e mãe (não é \"parentes\"!) · SIBLINGS = irmãos e irmãs · "
                   "CHILDREN = filhos (singular: CHILD — plural irregular, sem S).\n"
                   "Parentes = RELATIVES.\n"
                   "GRAND = uma geração antes ou depois: grandmother (avó) · grandfather (avô) · grandparents (avós) · "
                   "granddaughter (neta) · grandson (neto) · grandchildren (netos).\n"
                   "This is my mother. · These are my sisters. (plural → these are)",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the family members to Portuguese.",
         "translation": "Ligue os membros da família ao português.",
         "example": "mother → mãe",
         "pairs": [
             {"left": "wife", "right": "esposa"},
             {"left": "husband", "right": "marido"},
             {"left": "daughter", "right": "filha"},
             {"left": "son", "right": "filho"},
             {"left": "granddaughter", "right": "neta"},
             {"left": "grandson", "right": "neto"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the neutral word (for men and women together).",
         "translation": "Escolha a palavra neutra (que junta homens e mulheres).",
         "example": "mother + father = [parents]",
         "text": "1. sister + brother = [*siblings|brothers|parents]\n"
                 "2. daughter + son = [*children|sons|childs]\n"
                 "3. grandmother + grandfather = [*grandparents|grandfathers|relatives]\n"
                 "4. granddaughter + grandson = [*grandchildren|grandsons|grandchilds]\n"
                 "5. uncles, aunts, cousins… (parentes) = [*relatives|parents|siblings]"},
        {"type": "dropdown",
         "prompt": "This is or these are?",
         "translation": "This is (singular) ou these are (plural)?",
         "example": "[These are] my sisters.",
         "text": "1. [*This is|These are] my mother.\n"
                 "2. [*These are|This is] my grandparents.\n"
                 "3. [*This is|These are] my son.\n"
                 "4. [*These are|This is] my children."},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Dad\" is the same as \"father\". → True",
         "statements": [
             {"text": "\"Parents\" means all your relatives (uncles, cousins…).", "answer": False,
              "translation": "\"Parents\" significa todos os seus parentes (tios, primos…)."},
             {"text": "\"Children\" is the plural of \"child\".", "answer": True,
              "translation": "\"Children\" é o plural de \"child\"."},
             {"text": "\"Siblings\" can be brothers and sisters.", "answer": True,
              "translation": "\"Siblings\" pode ser irmãos e irmãs."},
             {"text": "\"Brothers\" is a neutral word in English, for men and women.", "answer": False,
              "translation": "\"Brothers\" é uma palavra neutra em inglês, para homens e mulheres."},
             {"text": "\"Mommy\" and \"daddy\" are words children use.", "answer": True,
              "translation": "\"Mommy\" e \"daddy\" são palavras que as crianças usam."},
         ]},
    ],
}

AULA18_EXTENDED = {
    "title": "Extended family + 's",
    "lesson": 18,
    "description": "EXTENDED FAMILY: aunt (tia — \"ént\" ou \"ânt\") · uncle (tio) · niece (sobrinha — \"níis\", ≠ nice) · "
                   "nephew (sobrinho) · cousin (primo / prima).\n"
                   "IN-LAW (família do marido / esposa): mother-in-law (sogra) · father-in-law (sogro) · sister-in-law (cunhada) · "
                   "brother-in-law (cunhado) · son-in-law (genro) · daughter-in-law (nora).\n"
                   "STEP (novo casamento): stepmother (madrasta) · stepfather (padrasto) · stepson (enteado). "
                   "HALF: half sister / half brother (filhos do mesmo pai OU da mesma mãe).\n"
                   "GOD: godmother (madrinha) · godfather (padrinho) · goddaughter (afilhada) · godson (afilhado).\n"
                   "POSSESSIVE 'S: o \"dono\" vem primeiro → Marta is Lucas's mother. (A Marta é a mãe do Lucas.)",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the words to Portuguese.",
         "translation": "Ligue as palavras ao português.",
         "example": "cousin → primo / prima",
         "pairs": [
             {"left": "aunt", "right": "tia"},
             {"left": "uncle", "right": "tio"},
             {"left": "niece", "right": "sobrinha"},
             {"left": "nephew", "right": "sobrinho"},
             {"left": "mother-in-law", "right": "sogra"},
             {"left": "stepfather", "right": "padrasto"},
         ]},
        {"type": "dropdown",
         "prompt": "Complete with the right word.",
         "translation": "Complete com a palavra certa.",
         "example": "My mother's sister is my [aunt].",
         "text": "1. My father's brother is my [*uncle|cousin|nephew].\n"
                 "2. My aunt's son is my [*cousin|brother|nephew].\n"
                 "3. My sister's daughter is my [*niece|aunt|cousin].\n"
                 "4. My husband's mother is my [*mother-in-law|stepmother|grandmother].\n"
                 "5. My wife's brother is my [*brother-in-law|half brother|stepbrother].\n"
                 "6. My mother's new husband is my [*stepfather|father-in-law|godfather]."},
        {"type": "group",
         "prompt": "Women or men? Put each word in the right group.",
         "translation": "Mulheres ou homens? Coloque cada palavra no grupo certo.",
         "example": "aunt → women · uncle → men",
         "categories": ["women", "men", "men or women"],
         "words": [
             {"text": "niece", "category": "women"}, {"text": "godmother", "category": "women"},
             {"text": "daughter-in-law", "category": "women"},
             {"text": "nephew", "category": "men"}, {"text": "son-in-law", "category": "men"},
             {"text": "stepbrother", "category": "men"},
             {"text": "cousin", "category": "men or women"}, {"text": "sibling", "category": "men or women"},
             {"text": "child", "category": "men or women"},
         ]},
        {"type": "fill",
         "prompt": "Write the sentence with 's.",
         "translation": "Escreva a frase com 's (o \"dono\" vem primeiro).",
         "example": "A Marta é a mãe do Lucas. → Marta is Lucas's mother.",
         "text": "1. O Paulo é o pai da Júlia. → [Paulo is Júlia's father.|Paulo is Julia's father.]\n"
                 "2. A Ana é a esposa do Pedro. → [Ana is Pedro's wife.]\n"
                 "3. O Leo é o primo da Bia. → [Leo is Bia's cousin.]"},
    ],
}

AULA18_LISTENING = {
    "title": "Listening — family photos",
    "lesson": 18,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Atenção: NIECE (sobrinha) ≠ NICE (legal).",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the word you hear.",
         "translation": "Ouça e escolha a palavra que você ouve.",
         "example": "Você ouve: \"This is my niece.\" → niece",
         "audio": f"{AUDIO}/aula18-words.m4a",
         "text": "1. She's very [*nice|niece].\n2. These are my [*parents|relatives].\n3. This is my [*aunt|uncle].\n"
                 "4. I have two [*children|child].\n5. He's my [*cousin|uncle]."},
        {"type": "fill",
         "prompt": "Dictation: listen and write the family member.",
         "translation": "Ditado: ouça e escreva o membro da família.",
         "example": "Você ouve: \"This is my aunt.\" → This is my [aunt].",
         "audio": f"{AUDIO}/aula18-dictation.m4a",
         "text": "1. This is my [grandmother].\n2. These are my [grandparents].\n3. This is my [nephew].\n"
                 "4. These are my [siblings].\n5. This is my [daughter]."},
        {"type": "info",
         "prompt": "Now listen: Mia shows her family photos to her friend Jack.",
         "translation": "Agora ouça: a Mia mostra as fotos da família para o amigo dela, o Jack. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula18-photos.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Mia shows photos to [Jack].",
         "text": "1. Who are the people in the first photo? → [*Mia's grandparents.|Mia's parents.|Mia's cousins.]\n"
                 "2. Who is Carla? → [*Mia's aunt.|Mia's sister.|Mia's niece.]\n"
                 "3. Who is Davi? → [*Mia's nephew.|Mia's son.|Mia's uncle.]\n"
                 "4. How many siblings does Mia have? → [*Two.|One.|Three.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Mia has family photos. → True",
         "statements": [
             {"text": "Mia's grandparents live in Portugal.", "answer": True, "translation": "Os avós da Mia moram em Portugal."},
             {"text": "Carla has three children.", "answer": False, "translation": "A Carla tem três filhos."},
             {"text": "Mia is Davi's godmother.", "answer": True, "translation": "A Mia é madrinha do Davi."},
         ]},
    ],
}

AULA18_SPEAKING = {
    "title": "Speaking — my family",
    "lesson": 18,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: DAUGHTER = \"dóter\" (GH mudo) · AUNT = \"ént\" · NIECE = \"níis\" · NEPHEW = \"néfiu\" · "
                   "CHILD = \"tcháild\" · CHILDREN = \"tchíldren\".",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the family members.",
         "translation": "Ouça e repita os membros da família.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula18-say-w{i}.m4a"} for i, t in enumerate(
             ["daughter", "son", "parents", "siblings", "child", "children", "grandparents", "aunt", "uncle", "niece",
              "nephew", "cousin", "mother-in-law"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases.",
         "example": "\"This is my mother.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula18-say-s{i}.m4a"} for i, t in enumerate(
             ["This is my father.", "These are my sisters.", "I have one sibling.", "Marta is Lucas's mother.",
              "My cousins live in Recife."], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOUR family.",
         "translation": "Agora responda às perguntas sobre a SUA família com uma frase completa.",
         "example": "\"Do you have siblings?\" → \"Yes, I do. I have one brother and one sister.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula18-say-y{i}.m4a"} for i, t in enumerate(
             ["Do you have siblings?", "Do you have children?", "Where do your parents live?",
              "How many cousins do you have?"], 1)]},
    ],
}

AULA18_READING = {
    "title": "Reading — the Costa family",
    "lesson": 18,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Lucas's text about his family.",
         "translation": "Leia e ouça o texto do Lucas sobre a família dele. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula18-reading.m4a",
         "text": "THE COSTA FAMILY\n\n"
                 "Hi! I'm Lucas Costa, and I'm fourteen. I live in Campinas with my parents and my sister, Nina.\n"
                 "My mother's name is Marta. She's a nurse. My father, Rui, is a teacher.\n"
                 "My grandparents, Lúcia and Jorge, live on a farm. They have four grandchildren: me, Nina and our two cousins.\n"
                 "Our cousins are Gabi and Tiago. They're my uncle Beto's children. Beto is my father's brother.\n"
                 "My aunt Sônia is Beto's wife. She's very nice, and she's my godmother!\n"
                 "We all have lunch at the farm on Sundays. I love my family!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Who is Nina? → [Lucas's sister.]",
         "text": "1. Who is Marta? → [*Lucas's mother.|Lucas's aunt.|Lucas's grandmother.]\n"
                 "2. Who are Gabi and Tiago? → [*Lucas's cousins.|Lucas's siblings.|Lucas's uncles.]\n"
                 "3. Who is Beto? → [*Rui's brother.|Marta's brother.|Lucas's cousin.]\n"
                 "4. How many grandchildren do Lúcia and Jorge have? → [*Four.|Two.|Three.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Lucas is fourteen. → True",
         "statements": [
             {"text": "Sônia is Lucas's godmother.", "answer": True, "translation": "A Sônia é madrinha do Lucas."},
             {"text": "Lucas's grandparents live in Campinas.", "answer": False,
              "translation": "Os avós do Lucas moram em Campinas."},
             {"text": "Rui is a nurse.", "answer": False, "translation": "O Rui é enfermeiro."},
             {"text": "The family has lunch together on Sundays.", "answer": True,
              "translation": "A família almoça junta aos domingos."},
         ]},
        {"type": "fill",
         "prompt": "Complete with the family member.",
         "translation": "Complete com o membro da família, de acordo com o texto.",
         "example": "Nina is Lucas's [sister].",
         "text": "1. Sônia is Beto's [wife].\n2. Jorge is Lucas's [grandfather].\n3. Tiago is Beto's [son].\n"
                 "4. Lucas is Beto's [nephew]."},
    ],
}

AULA18_WRITING = {
    "title": "Writing — my family",
    "lesson": 18,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ This is my… / These are my… · I have two siblings. · Possessive 's: Ana is Rui's wife.",
    "topic": AULA18_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "meus avós → my grandparents",
         "text": "1. meus pais → [my parents]\n2. meus filhos → [my children]\n3. minha sogra → [my mother-in-law]\n"
                 "4. meus primos → [my cousins]"},
        {"type": "fill",
         "prompt": "Write the sentences in English.",
         "translation": "Escreva as frases em inglês.",
         "example": "Esta é a minha irmã. → This is my sister.",
         "text": "1. Estes são os meus avós. → [These are my grandparents.]\n"
                 "2. Eu tenho três irmãos (irmãos e irmãs). → [I have three siblings.]\n"
                 "3. A Rosa é a tia do Pedro. → [Rosa is Pedro's aunt.]"},
        {"type": "free",
         "prompt": "Write about your family: names, ages, jobs, where they live. Use 's at least once.",
         "translation": "Escreva sobre a sua família: nomes, idades, profissões, onde moram. Use o 's pelo menos uma vez.",
         "example": "My mother's name is Ana. She's a teacher.",
         "model_answer": "My mother's name is Ana. She's 55, and she's a teacher.\n"
                         "My father, João, is an engineer. My parents live in Belo Horizonte.\n"
                         "I have two siblings: one brother and one sister. My sister's name is Carol.\n"
                         "My uncle Paulo is my godfather. He has three children, my cousins.",
         "keywords": ["my", "is", "have"], "min_words": 35, "points": 4},
    ],
}

AULA18_VIDEO = _video(18, AULA18_TOPIC, "Video — Grandma's birthday",
                      "a Júlia apresenta a família na festa de aniversário da avó: parents, siblings, aunt, cousins, in-laws…",
                      "aula18-video", [
    _q("Who is Rosa?", "Quem é a Rosa?", "Júlia's grandmother.", "Júlia's mother.", "Júlia's aunt.", "Júlia's cousin."),
    _q("How many grandchildren does Rosa have?", "Quantos netos a Rosa tem?", "Six.", "Four.", "Eighty.", "Two."),
    _q("Who is Marcos?", "Quem é o Marcos?", "Júlia's husband.", "Júlia's brother.", "Júlia's father.", "Júlia's son."),
    _q("Who is Teresa for Marcos?", "Quem é a Teresa para o Marcos?", "His mother-in-law.", "His sister-in-law.",
       "His stepmother.", "His grandmother."),
    _q("Who are Theo and Lili?", "Quem são o Theo e a Lili?", "Júlia's children.", "Júlia's cousins.",
       "Júlia's siblings.", "Júlia's parents."),
])


# ---------- Aula 19 — A, An, Plurals (https://youtu.be/kro-ooMgZKs) ----------

AULA19_TOPIC = "Aula 19 — A, An, Plurals"

AULA19_WORDS = {
    "title": "My things: a or an?",
    "lesson": 19,
    "description": "A / AN = um / uma (só no singular):\n"
                   "A → antes de SOM de consoante: a pen, a bag, a wallet, a key.\n"
                   "AN → antes de SOM de vogal: an umbrella, an eraser, an egg.\n"
                   "No plural, NÃO usamos a / an: keys, sunglasses, credit cards (ou um número: two keys, some pens, many pens).\n"
                   "Pronúncia: EY soa \"i\": key (\"kí\"), money, monkey, Disney. COMB: o B é mudo (\"côum\").",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the objects to Portuguese.",
         "translation": "Ligue os objetos ao português.",
         "example": "a key → uma chave",
         "pairs": [
             {"left": "a wallet", "right": "uma carteira"},
             {"left": "a key ring", "right": "um chaveiro"},
             {"left": "a charger", "right": "um carregador"},
             {"left": "a toothbrush", "right": "uma escova de dente"},
             {"left": "a comb", "right": "um pente"},
             {"left": "a backpack", "right": "uma mochila"},
         ]},
        {"type": "match",
         "prompt": "Match more objects to Portuguese.",
         "translation": "Ligue mais objetos ao português.",
         "example": "a pen → uma caneta",
         "pairs": [
             {"left": "a lipstick", "right": "um batom"},
             {"left": "sunglasses", "right": "óculos de sol"},
             {"left": "an umbrella", "right": "um guarda-chuva"},
             {"left": "an eraser", "right": "uma borracha"},
             {"left": "a passport", "right": "um passaporte"},
         ]},
        {"type": "dropdown",
         "prompt": "A, an or nothing (–)?",
         "translation": "A, an ou nada (–)? Lembre: an antes de som de vogal; no plural, nada.",
         "example": "[an] egg · [–] keys",
         "text": "1. [*an|a|–] umbrella\n2. [*a|an|–] passport\n3. [*–|a|an] credit cards\n4. [*an|a|–] eraser\n"
                 "5. [*a|an|–] smartwatch\n6. [*–|a|an] sunglasses\n7. [*an|a|–] egg\n8. [*a|an|–] cell phone"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "We say \"an umbrella\". → True",
         "statements": [
             {"text": "In \"key\" and \"money\", EY sounds like \"i\".", "answer": True,
              "translation": "Em \"key\" e \"money\", o EY soa como \"i\"."},
             {"text": "We say \"a keys\".", "answer": False, "translation": "Dizemos \"a keys\"."},
             {"text": "In \"comb\", we don't say the letter B.", "answer": True,
              "translation": "Em \"comb\", a gente não pronuncia a letra B."},
             {"text": "In English, \"a\" is for men and \"an\" is for women.", "answer": False,
              "translation": "Em inglês, \"a\" é para o masculino e \"an\" para o feminino."},
         ]},
    ],
}

AULA19_PLURALS = {
    "title": "Plurals",
    "lesson": 19,
    "description": "Regra geral: + S → pen → pens · bag → bags · key → keys (vogal + y).\n"
                   "+ ES depois de som parecido com S (ch, sh, s, x, z): watch → watches · brush → brushes · bus → buses · box → boxes.\n"
                   "Consoante + O → + ES: potato → potatoes · hero → heroes (mas radio → radios, video → videos).\n"
                   "Consoante + Y → IES: city → cities · baby → babies · party → parties.\n"
                   "F / FE → VES: life → lives · wolf → wolves.\n"
                   "IRREGULAR: man → men · woman → women · person → people · child → children · foot → feet · tooth → teeth · "
                   "mouse → mice · sheep → sheep · deer → deer.",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "How do we make the plural? Put each word in the right group.",
         "translation": "Como formamos o plural? Coloque cada palavra no grupo certo.",
         "example": "pen → + s (pens) · box → + es (boxes)",
         "categories": ["+ s", "+ es", "y → ies", "f → ves"],
         "words": [
             {"text": "bag", "category": "+ s"}, {"text": "key", "category": "+ s"}, {"text": "radio", "category": "+ s"},
             {"text": "watch", "category": "+ es"}, {"text": "bus", "category": "+ es"},
             {"text": "potato", "category": "+ es"},
             {"text": "city", "category": "y → ies"}, {"text": "baby", "category": "y → ies"},
             {"text": "party", "category": "y → ies"},
             {"text": "life", "category": "f → ves"}, {"text": "wolf", "category": "f → ves"},
         ]},
        {"type": "fill",
         "prompt": "Write the plural.",
         "translation": "Escreva o plural.",
         "example": "a pen → pens",
         "text": "1. a box → [boxes]\n2. a brush → [brushes]\n3. a hero → [heroes]\n4. a city → [cities]\n"
                 "5. a wallet → [wallets]\n6. a party → [parties]"},
        {"type": "match",
         "prompt": "Irregular plurals: match the singular to the plural.",
         "translation": "Plurais irregulares: ligue o singular ao plural.",
         "example": "man → men",
         "pairs": [
             {"left": "woman", "right": "women"},
             {"left": "child", "right": "children"},
             {"left": "person", "right": "people"},
             {"left": "foot", "right": "feet"},
             {"left": "tooth", "right": "teeth"},
             {"left": "mouse", "right": "mice"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the right word.",
         "translation": "Escolha a palavra certa.",
         "example": "five [men] (cinco homens)",
         "text": "1. three [*women|womans|womens]\n"
                 "2. two [*sheep|sheeps|sheepes]\n"
                 "3. many [*people|persons|peoples]\n"
                 "4. four [*children|childs|childrens]\n"
                 "5. some [*potatoes|potatos|potatoies]"},
    ],
}

AULA19_LISTENING = {
    "title": "Listening — what's in your bag?",
    "lesson": 19,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Singular or plural? Listen and choose.",
         "translation": "Singular ou plural? Ouça e escolha.",
         "example": "Você ouve: \"keys\" → keys",
         "audio": f"{AUDIO}/aula19-words.m4a",
         "text": "1. [*a watch|watches]\n2. [*boxes|a box]\n3. [*a woman|women]\n4. [*men|a man]\n5. [*a child|children]"},
        {"type": "fill",
         "prompt": "Dictation: listen and write the object.",
         "translation": "Ditado: ouça e escreva o objeto (com a / an quando houver).",
         "example": "Você ouve: \"a pen\" → [a pen]",
         "audio": f"{AUDIO}/aula19-dictation.m4a",
         "text": "1. [a wallet]\n2. [an umbrella]\n3. [sunglasses]\n4. [a charger]\n5. [credit cards]"},
        {"type": "info",
         "prompt": "Now listen to Olivia: what's in her bag?",
         "translation": "Agora ouça a Olivia. Um amigo pergunta o que tem na bolsa dela. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula19-bag.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "fill",
         "prompt": "Listen again and complete.",
         "translation": "Ouça de novo e complete com o número ou o objeto.",
         "example": "Olivia's bag is [big].",
         "text": "1. Olivia has [two|2] lipsticks.\n2. She has [three|3] keys.\n3. She has an [umbrella] because it's a rainy city.\n"
                 "4. She has [five|5] pens."},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Olivia has a bag. → True",
         "statements": [
             {"text": "Olivia has her passport in her bag.", "answer": False,
              "translation": "A Olivia tem o passaporte dela na bolsa."},
             {"text": "Olivia has a phone charger.", "answer": True, "translation": "A Olivia tem um carregador de celular."},
             {"text": "Olivia has sunglasses.", "answer": True, "translation": "A Olivia tem óculos de sol."},
         ]},
    ],
}

AULA19_SPEAKING = {
    "title": "Speaking — my things",
    "lesson": 19,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: KEY = \"kí\" · COMB = \"côum\" · WOMAN = \"úman\" × WOMEN = \"uímen\" · MAN × MEN (o \"é\" fecha um pouco).",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the objects.",
         "translation": "Ouça e repita os objetos.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula19-say-w{i}.m4a"} for i, t in enumerate(
             ["a key", "a key ring", "sunglasses", "a wallet", "a charger", "an umbrella", "a passport", "a toothbrush",
              "a comb", "a backpack"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat: singular → plural.",
         "translation": "Ouça e repita: singular → plural.",
         "example": "\"a man, men\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula19-say-p{i}.m4a"} for i, t in enumerate(
             ["a watch, watches", "a city, cities", "a man, men", "a woman, women", "a child, children", "a foot, feet",
              "a tooth, teeth", "a person, people"], 1)]},
        {"type": "speak",
         "prompt": "Now answer about YOU.",
         "translation": "Agora responda sobre VOCÊ com uma frase completa.",
         "example": "\"What do you have in your bag?\" → \"I have a wallet, two pens and my keys.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula19-say-y{i}.m4a"} for i, t in enumerate(
             ["What do you have in your bag?", "How many keys do you have?", "Do you have an umbrella?",
              "What do you have on your desk?"], 1)]},
    ],
}

AULA19_READING = {
    "title": "Reading — Leo's backpack",
    "lesson": 19,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Leo's text.",
         "translation": "Leia e ouça o texto do Leo. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula19-reading.m4a",
         "text": "MY BACKPACK\n\n"
                 "I'm Leo, and I'm a university student. I always have my backpack with me.\n"
                 "In my backpack, I have a notebook, three pens, a pencil and an eraser.\n"
                 "I also have a tablet and a charger, because I study on the bus.\n"
                 "I have my wallet with two credit cards, and I have my keys on a key ring.\n"
                 "I usually have an apple or a banana for lunch.\n"
                 "And on rainy days, I have an umbrella too. My backpack is very heavy!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "What does Leo do? → [He's a university student.]",
         "text": "1. How many pens does Leo have? → [*Three.|Two.|One.]\n"
                 "2. Why does he have a tablet and a charger? → [*Because he studies on the bus.|Because he plays games.|Because he works at night.]\n"
                 "3. What does he have in his wallet? → [*Two credit cards.|A key.|An eraser.]\n"
                 "4. When does he have an umbrella? → [*On rainy days.|Every day.|On Sundays.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Leo has a backpack. → True",
         "statements": [
             {"text": "Leo has an eraser.", "answer": True, "translation": "O Leo tem uma borracha."},
             {"text": "Leo has two notebooks.", "answer": False, "translation": "O Leo tem dois cadernos."},
             {"text": "Leo's backpack is light.", "answer": False, "translation": "A mochila do Leo é leve."},
         ]},
        {"type": "fill",
         "prompt": "Complete with a or an, according to the text.",
         "translation": "Complete com a ou an, de acordo com o texto.",
         "example": "He has [a] notebook.",
         "text": "1. He has [an] eraser.\n2. He has [a] tablet.\n3. He has [an] apple or [a] banana.\n4. He has [an] umbrella."},
    ],
}

AULA19_WRITING = {
    "title": "Writing — what's in my bag?",
    "lesson": 19,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Singular → a / an · Plural → só a palavra, um número, some (alguns) ou many (muitos).",
    "topic": AULA19_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write in English.",
         "translation": "Escreva em inglês.",
         "example": "duas canetas → two pens",
         "text": "1. um guarda-chuva → [an umbrella]\n2. três chaves → [three keys]\n3. duas mulheres → [two women]\n"
                 "4. cinco crianças → [five children]\n5. muitas pessoas → [many people]"},
        {"type": "fill",
         "prompt": "Correct the mistake. Write the right sentence.",
         "translation": "Corrija o erro. Escreva a frase certa.",
         "example": "I have a umbrella. → I have an umbrella.",
         "text": "1. I have two childs. → [I have two children.]\n"
                 "2. She has a keys. → [She has keys.|She has a key.]\n"
                 "3. I see three mans. → [I see three men.]"},
        {"type": "free",
         "prompt": "What do you have in your bag or backpack? Write about 8 things. Use a, an and plurals.",
         "translation": "O que você tem na sua bolsa ou mochila? Escreva sobre 8 coisas. Use a, an e plurais.",
         "example": "In my bag, I have a wallet and two pens.",
         "model_answer": "In my bag, I have a wallet with three credit cards, my cell phone and a charger.\n"
                         "I also have my keys, two pens, a lipstick and sunglasses.\n"
                         "On rainy days, I have an umbrella too.",
         "keywords": ["I have", "a", "an"], "min_words": 25, "points": 4},
    ],
}

AULA19_VIDEO = _video(19, AULA19_TOPIC, "Video — What's in my bag?",
                      "a Maya mostra o que tem na bolsa dela antes de viajar: a, an e plurais.",
                      "aula19-video", [
    _q("Does Maya have her keys?", "A Maya está com as chaves dela?", "Yes, she does.", "No, she doesn't.",
       "Yes, she is.", "No, she isn't."),
    _q("Which is correct?", "Qual está correto?", "an umbrella", "a umbrella", "umbrellas a", "an umbrellas"),
    _q("Why does Maya have her passport?", "Por que a Maya está com o passaporte?", "Because she goes to Paris today.",
       "Because she goes to the bank.", "Because it's her birthday.", "Because she works at the airport."),
    _q("What does Maya have for the sun?", "O que a Maya tem para o sol?", "Sunglasses.", "An umbrella.", "A lipstick.",
       "A comb."),
    _q("Which plural is correct?", "Qual plural está correto?", "two watches", "two watchs", "two watchies",
       "two watch"),
])


# ---------- Aula 20 — Parts of the House (https://youtu.be/QGq59Rr_y6E) ----------

AULA20_TOPIC = "Aula 20 — Parts of the House"

AULA20_WORDS = {
    "title": "Rooms and parts of the house",
    "lesson": 20,
    "description": "Do you live in a house or in an apartment? → I live in an apartment. My brother lives in a house.\n"
                   "ROOMS (cômodos): living room (sala de estar) · bedroom (quarto) · bathroom (banheiro) · dining room (sala de jantar) · "
                   "kitchen (cozinha) · garage · hall (corredor / hall) · office (escritório) · balcony (varanda) · "
                   "attic (sótão) · basement (porão).\n"
                   "PARTS: door (porta) · wall (parede / muro) · window (janela) · floor (chão) · ceiling (teto).\n"
                   "Cuidado: BEDROOM (\"bédrum\", quarto) ≠ BATHROOM (\"béthrum\", banheiro). \"My room\" = meu quarto.",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the rooms to Portuguese.",
         "translation": "Ligue os cômodos ao português.",
         "example": "kitchen → cozinha",
         "pairs": [
             {"left": "living room", "right": "sala de estar"},
             {"left": "bedroom", "right": "quarto"},
             {"left": "bathroom", "right": "banheiro"},
             {"left": "dining room", "right": "sala de jantar"},
             {"left": "balcony", "right": "varanda"},
             {"left": "basement", "right": "porão"},
         ]},
        {"type": "match",
         "prompt": "Match the parts of the house to Portuguese.",
         "translation": "Ligue as partes da casa ao português.",
         "example": "door → porta",
         "pairs": [
             {"left": "wall", "right": "parede"},
             {"left": "window", "right": "janela"},
             {"left": "floor", "right": "chão"},
             {"left": "ceiling", "right": "teto"},
             {"left": "attic", "right": "sótão"},
             {"left": "office", "right": "escritório"},
         ]},
        {"type": "dropdown",
         "prompt": "Which room is it?",
         "translation": "Qual é o cômodo?",
         "example": "I sleep here. → [bedroom]",
         "text": "1. I cook here. → [*kitchen|bathroom|garage]\n"
                 "2. I take a shower here. → [*bathroom|bedroom|dining room]\n"
                 "3. My car is here. → [*garage|attic|hall]\n"
                 "4. We have dinner here. → [*dining room|basement|balcony]\n"
                 "5. I watch TV with my family here. → [*living room|bathroom|garage]\n"
                 "6. I work at home here. → [*office|kitchen|attic]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Kitchen\" means cozinha. → True",
         "statements": [
             {"text": "\"Bedroom\" and \"bathroom\" have the same pronunciation.", "answer": False,
              "translation": "\"Bedroom\" e \"bathroom\" têm a mesma pronúncia."},
             {"text": "\"Wall\" can mean parede or muro.", "answer": True,
              "translation": "\"Wall\" pode significar parede ou muro."},
             {"text": "\"It's in my room\" can mean it's in my bedroom.", "answer": True,
              "translation": "\"It's in my room\" pode significar que está no meu quarto."},
             {"text": "\"Ceiling\" means chão.", "answer": False, "translation": "\"Ceiling\" significa chão."},
         ]},
    ],
}

AULA20_FURNITURE = {
    "title": "Furniture and things at home",
    "lesson": 20,
    "description": "LIVING ROOM: sofa / couch · rug (tapete) · lamp (luminária — lâmpada é light bulb) · armchair (poltrona) · "
                   "plant · coffee table (mesinha de centro) · pictures (quadros) · cushions (almofadas).\n"
                   "KITCHEN: stove (fogão) · fridge (geladeira — refrigerator, não é refrigerante!) · microwave · oven (forno, \"âven\") · "
                   "sink (pia) · blender (liquidificador) · dishwasher (lava-louças) · washing machine (máquina de lavar roupa).\n"
                   "BEDROOM: bed · wardrobe (guarda-roupa) · closet · pillows (travesseiros) · blanket (cobertor) · "
                   "bedside table (mesinha de cabeceira).\n"
                   "BATHROOM: toilet (vaso sanitário) · bathtub (banheira) · shower (chuveiro) · sink (pia) · faucet (torneira) · "
                   "mirror (espelho).",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "Where is it? Put each thing in the right room.",
         "translation": "Onde fica? Coloque cada coisa no cômodo certo.",
         "example": "bed → bedroom",
         "categories": ["living room", "kitchen", "bedroom", "bathroom"],
         "words": [
             {"text": "sofa", "category": "living room"}, {"text": "armchair", "category": "living room"},
             {"text": "coffee table", "category": "living room"},
             {"text": "stove", "category": "kitchen"}, {"text": "fridge", "category": "kitchen"},
             {"text": "blender", "category": "kitchen"},
             {"text": "wardrobe", "category": "bedroom"}, {"text": "pillows", "category": "bedroom"},
             {"text": "bedside table", "category": "bedroom"},
             {"text": "toilet", "category": "bathroom"}, {"text": "bathtub", "category": "bathroom"},
             {"text": "faucet", "category": "bathroom"},
         ]},
        {"type": "match",
         "prompt": "Match the words to Portuguese.",
         "translation": "Ligue as palavras ao português.",
         "example": "mirror → espelho",
         "pairs": [
             {"left": "rug", "right": "tapete"},
             {"left": "cushions", "right": "almofadas"},
             {"left": "oven", "right": "forno"},
             {"left": "sink", "right": "pia"},
             {"left": "blanket", "right": "cobertor"},
             {"left": "washing machine", "right": "máquina de lavar roupa"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the right word.",
         "translation": "Escolha a palavra certa.",
         "example": "a geladeira → the [fridge]",
         "text": "1. a luminária → the [*lamp|light bulb|lamb]\n"
                 "2. os quadros na parede → the [*pictures|paints|frames] on the wall\n"
                 "3. a lava-louças → the [*dishwasher|washing machine|sink]\n"
                 "4. a poltrona → the [*armchair|chair arm|sofa]\n"
                 "5. o chuveiro → the [*shower|bathtub|faucet]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Fridge\" is short for refrigerator. → True",
         "statements": [
             {"text": "\"Refrigerator\" means refrigerante.", "answer": False,
              "translation": "\"Refrigerator\" significa refrigerante."},
             {"text": "\"Sofa\" and \"couch\" are the same thing.", "answer": True,
              "translation": "\"Sofa\" e \"couch\" são a mesma coisa."},
             {"text": "A \"lamp\" is a light bulb.", "answer": False, "translation": "\"Lamp\" é uma lâmpada."},
             {"text": "We say \"oven\" like \"âven\".", "answer": True, "translation": "A gente fala \"oven\" como \"âven\"."},
         ]},
    ],
}

AULA20_LISTENING = {
    "title": "Listening — at home",
    "lesson": 20,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Atenção: BEDROOM ≠ BATHROOM.",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Bedroom or bathroom? Listen and choose.",
         "translation": "Bedroom (quarto) ou bathroom (banheiro)? Ouça e escolha.",
         "example": "Você ouve: \"It's in the bedroom.\" → bedroom",
         "audio": f"{AUDIO}/aula20-rooms.m4a",
         "text": "1. [*bathroom|bedroom]\n2. [*bedroom|bathroom]\n3. [*bedroom|bathroom]\n4. [*bathroom|bedroom]"},
        {"type": "fill",
         "prompt": "Dictation: listen and write the word.",
         "translation": "Ditado: ouça e escreva a palavra.",
         "example": "Você ouve: \"the sofa\" → the [sofa]",
         "audio": f"{AUDIO}/aula20-dictation.m4a",
         "text": "1. the [kitchen]\n2. the [mirror]\n3. the [fridge]\n4. the [window]\n5. the [pillows]"},
        {"type": "info",
         "prompt": "Now listen: Mr. Lopes shows an apartment to Ana.",
         "translation": "Agora ouça: o Sr. Lopes mostra um apartamento para alugar para a Ana. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula20-apartment.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Ana wants an [apartment].",
         "text": "1. How many bedrooms does the apartment have? → [*Two.|One.|Three.]\n"
                 "2. What is in the living room? → [*A sofa and an armchair.|A bed and a wardrobe.|A dishwasher.]\n"
                 "3. What does the bathroom have? → [*A shower.|A bathtub.|A washing machine.]\n"
                 "4. What does Ana love? → [*The balcony.|The garage.|The kitchen.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "The apartment has a kitchen. → True",
         "statements": [
             {"text": "The kitchen has a dishwasher.", "answer": False, "translation": "A cozinha tem lava-louças."},
             {"text": "The kitchen has a new fridge.", "answer": True, "translation": "A cozinha tem uma geladeira nova."},
             {"text": "The apartment has a garage.", "answer": False, "translation": "O apartamento tem garagem."},
         ]},
    ],
}

AULA20_SPEAKING = {
    "title": "Speaking — my house",
    "lesson": 20,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: BEDROOM = \"bédrum\" · BATHROOM = \"béthrum\" (TH com a língua entre os dentes) · "
                   "OVEN = \"âven\" · KITCHEN = \"kítchen\".",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the rooms.",
         "translation": "Ouça e repita os cômodos.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula20-say-r{i}.m4a"} for i, t in enumerate(
             ["living room", "bedroom", "bathroom", "dining room", "kitchen", "garage", "office", "balcony"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the things at home.",
         "translation": "Ouça e repita as coisas da casa.",
         "example": "\"the fridge\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula20-say-t{i}.m4a"} for i, t in enumerate(
             ["sofa", "armchair", "rug", "stove", "fridge", "oven", "wardrobe", "pillows", "mirror", "faucet"], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOUR home.",
         "translation": "Agora responda às perguntas sobre a SUA casa com uma frase completa.",
         "example": "\"Do you live in a house or in an apartment?\" → \"I live in an apartment.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula20-say-y{i}.m4a"} for i, t in enumerate(
             ["Do you live in a house or in an apartment?", "How many bedrooms does your home have?",
              "What's your favorite room?", "Do you have a balcony?"], 1)]},
    ],
}

AULA20_READING = {
    "title": "Reading — my new apartment",
    "lesson": 20,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Bia's message.",
         "translation": "Leia e ouça a mensagem da Bia para uma amiga. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula20-reading.m4a",
         "text": "MY NEW APARTMENT\n\n"
                 "Hi, Carol! I have a new apartment in Florianópolis! It's small, but it's very nice.\n"
                 "It has a living room, a kitchen, one bedroom, one bathroom and a balcony.\n"
                 "In the living room, I have a blue sofa, an armchair and a lot of plants. I don't have a TV!\n"
                 "The kitchen is small. It has a stove, a fridge and a microwave, but it doesn't have an oven.\n"
                 "My bedroom has a big window, a bed, a wardrobe and a bedside table with a lamp.\n"
                 "The bathroom has a shower and a big mirror.\n"
                 "My favorite room? The balcony! I have breakfast there every morning, and I see the sea."},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Where is Bia's apartment? → [In Florianópolis.]",
         "text": "1. How many bedrooms does it have? → [*One.|Two.|Three.]\n"
                 "2. What color is the sofa? → [*Blue.|Green.|Black.]\n"
                 "3. What doesn't the kitchen have? → [*An oven.|A fridge.|A stove.]\n"
                 "4. What is Bia's favorite room? → [*The balcony.|The bedroom.|The kitchen.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "The apartment is small. → True",
         "statements": [
             {"text": "Bia has a TV in the living room.", "answer": False, "translation": "A Bia tem uma TV na sala."},
             {"text": "The bathroom has a bathtub.", "answer": False, "translation": "O banheiro tem banheira."},
             {"text": "Bia has breakfast on the balcony.", "answer": True, "translation": "A Bia toma café da manhã na varanda."},
             {"text": "The bedroom has a big window.", "answer": True, "translation": "O quarto tem uma janela grande."},
         ]},
        {"type": "fill",
         "prompt": "Complete with the room, according to the text.",
         "translation": "Complete com o cômodo, de acordo com o texto.",
         "example": "The wardrobe is in the [bedroom].",
         "text": "1. The armchair is in the [living room].\n2. The microwave is in the [kitchen].\n"
                 "3. The mirror is in the [bathroom]."},
    ],
}

AULA20_WRITING = {
    "title": "Writing — my home",
    "lesson": 20,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ I live in a house / an apartment. · My home has… · In the kitchen, I have… · "
                   "The fridge is in the kitchen.",
    "topic": AULA20_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write in English.",
         "translation": "Escreva em inglês.",
         "example": "a cozinha → the kitchen",
         "text": "1. o quarto → [the bedroom]\n2. o banheiro → [the bathroom]\n3. a geladeira → [the fridge|the refrigerator]\n"
                 "4. o guarda-roupa → [the wardrobe]\n5. o espelho → [the mirror]"},
        {"type": "fill",
         "prompt": "Translate the sentences.",
         "translation": "Traduza as frases.",
         "example": "Eu moro numa casa. → I live in a house.",
         "text": "1. Eu moro num apartamento. → [I live in an apartment.]\n"
                 "2. O sofá está na sala de estar. → [The sofa is in the living room.]\n"
                 "3. Minha casa tem três quartos. → [My house has three bedrooms.]"},
        {"type": "free",
         "prompt": "Describe your home: rooms, furniture and your favorite room.",
         "translation": "Descreva a sua casa: os cômodos, os móveis e o seu cômodo favorito (e por quê).",
         "example": "I live in an apartment. It has two bedrooms.",
         "model_answer": "I live in an apartment in Curitiba. It has a living room, a kitchen, two bedrooms and a bathroom.\n"
                         "In the living room, I have a big sofa, a rug and a TV.\n"
                         "My bedroom has a bed, a wardrobe and a desk.\n"
                         "My favorite room is the kitchen because I love to cook.",
         "keywords": ["live", "room", "kitchen", "favorite"], "min_words": 30, "points": 4},
    ],
}

AULA20_VIDEO = _video(20, AULA20_TOPIC, "Video — House tour",
                      "a Kate mostra a casa dela: living room, dining room, kitchen, bedroom, bathroom…",
                      "aula20-video", [
    _q("What is in the living room?", "O que tem na sala de estar?", "A big sofa and cushions.", "A bed and pillows.",
       "A stove and a fridge.", "A bathtub."),
    _q("Where does the family have dinner?", "Onde a família janta?", "In the dining room.", "In the bedroom.",
       "In the garage.", "In the bathroom."),
    _q("What does Kate love in the kitchen?", "O que a Kate ama na cozinha?", "The big oven.", "The small fridge.",
       "The dishwasher.", "The microwave."),
    _q("What is in the bedroom?", "O que tem no quarto?", "A bed, a bedside table and a lamp.", "A washing machine.",
       "A stove and an oven.", "A bathtub."),
    _q("What is Kate's favorite room?", "Qual o cômodo favorito da Kate?", "The bathroom.", "The kitchen.",
       "The garage.", "The office."),
])


# ---------- Aula 21 — There is / There are (https://youtu.be/72EcsgXqA30) ----------

AULA21_TOPIC = "Aula 21 — There is / There are"

AULA21_THERE = {
    "title": "There is / There are",
    "lesson": 21,
    "description": "TER no sentido de EXISTIR (\"tem um sofá na sala\") → THERE IS / THERE ARE. Não use have / has!\n"
                   "Singular → THERE IS (there's): There is a sofa in the living room. · There's a clock on the wall.\n"
                   "Plural → THERE ARE (sem contraction): There are two chairs in the office. · There are some books.\n"
                   "HAVE é o ter de posse: I have a car. ≠ There is a car in the garage.\n"
                   "Lembre: a / an no singular (there is an armchair) · número, some ou many no plural.\n"
                   "Adjetivo antes do substantivo: an orange cushion (uma almofada laranja).",
    "topic": AULA21_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "There is or there are?",
         "translation": "There is (singular) ou there are (plural)?",
         "example": "[There is] a lamp in the living room.",
         "text": "1. [*There are|There is] four pillows on the bed.\n"
                 "2. [*There is|There are] a chair in the bedroom.\n"
                 "3. [*There are|There is] three boxes in the garage.\n"
                 "4. [*There is|There are] a clock on the wall.\n"
                 "5. [*There are|There is] five people in the meeting.\n"
                 "6. [*There is|There are] a TV in the living room."},
        {"type": "choice",
         "prompt": "Which sentence is correct?",
         "translation": "Qual frase está correta?",
         "example": "There is an armchair in the living room. ✓",
         "options": ["There is an armchair in the living room.", "There is a armchair in the living room.",
                     "There are an armchair in the living room.", "Has an armchair in the living room."],
         "correct": 0},
        {"type": "choice",
         "prompt": "Which sentence is correct?",
         "translation": "Qual frase está correta?",
         "example": "There is a TV in the living room. ✓",
         "options": ["There is a TV in the living room.", "There is TV in the living room.",
                     "There are a TV in the living room.", "It has a TV in the living room."],
         "correct": 0},
        {"type": "dropdown",
         "prompt": "Have / has or there is / there are?",
         "translation": "Have / has (posse) ou there is / there are (existir)?",
         "example": "I [have] a car. · [There is] a car in the garage.",
         "text": "1. My brother [*has|there is] two cats.\n"
                 "2. [*There is|Has] a table in the dining room.\n"
                 "3. I [*have|there are] three cushions.\n"
                 "4. [*There are|Have] many plants on the balcony."},
        {"type": "fill",
         "prompt": "Write a / an + color + object.",
         "translation": "Escreva a / an + cor + objeto (a cor vem antes!).",
         "example": "uma almofada verde → a green cushion",
         "text": "1. uma almofada laranja → [an orange cushion]\n2. um sofá azul → [a blue sofa]\n"
                 "3. um tapete vermelho → [a red rug]"},
    ],
}

AULA21_QUESTIONS = {
    "title": "Is there…? Are there…?",
    "lesson": 21,
    "description": "NEGATIVE: there isn't (there is not) · there aren't (there are not).\n"
                   "There isn't a sofa in the living room. · There aren't chairs in the office.\n"
                   "QUESTION: inverta! IS THERE…? / ARE THERE…?\n"
                   "Is there a TV in the bedroom? → Yes, there is. / No, there isn't.\n"
                   "Are there pictures on the wall? → Yes, there are. / No, there aren't.\n"
                   "\"Professora, tem dever de casa?\" → Is there homework? (não \"Have homework?\")",
    "topic": AULA21_TOPIC,
    "items": [
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Tem um sofá na sala?)",
         "example": "there / Is / a TV → Is there a TV?",
         "tokens": ["Is", "there", "a", "sofa", "in", "the", "living", "room?"], "alternatives": []},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Tem quadros na parede?)",
         "example": "there / Are / books → Are there books?",
         "tokens": ["Are", "there", "pictures", "on", "the", "wall?"], "alternatives": []},
        {"type": "dropdown",
         "prompt": "Choose the right short answer.",
         "translation": "Escolha a resposta curta certa.",
         "example": "Is there a cushion on the bed? (✓) → [Yes, there is.]",
         "text": "1. Is there a TV in the bedroom? (✗) → [*No, there isn't.|No, there aren't.|No, it isn't.]\n"
                 "2. Are there pictures on the wall? (✓) → [*Yes, there are.|Yes, there is.|Yes, they have.]\n"
                 "3. Is there a garage? (✓) → [*Yes, there is.|Yes, there's.|Yes, it has.]\n"
                 "4. Are there plants on the balcony? (✗) → [*No, there aren't.|No, there isn't.|No, they don't.]"},
        {"type": "fill",
         "prompt": "Make the sentences negative.",
         "translation": "Passe as frases para a negativa (use contractions).",
         "example": "There is a sofa. → There isn't a sofa.",
         "text": "1. There is a TV in the kitchen. → [There isn't a TV in the kitchen.]\n"
                 "2. There are chairs in the office. → [There aren't chairs in the office.|There aren't any chairs in the office.]"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Tem dever de casa? → Is there homework?",
         "text": "1. Tem uma cadeira no quarto. → [There is a chair in the bedroom.|There's a chair in the bedroom.]\n"
                 "2. Tem três alunos na minha turma. → [There are three students in my class.]\n"
                 "3. Tem um espelho no banheiro? → [Is there a mirror in the bathroom?]"},
    ],
}

AULA21_LISTENING = {
    "title": "Listening — there is, there are",
    "lesson": 21,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧\n"
                   "Repare: THERE IS vira \"there's\" na fala; THERE ARE não tem contraction.",
    "topic": AULA21_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose what you hear.",
         "translation": "Ouça e escolha o que você ouve.",
         "example": "Você ouve: \"There's a lamp.\" → There's",
         "audio": f"{AUDIO}/aula21-forms.m4a",
         "text": "1. [*There's|There are] a clock on the wall.\n2. [*There are|There's] two beds.\n"
                 "3. [*There isn't|There aren't] a garage.\n4. [*Are there|Is there] pictures on the wall?\n"
                 "5. [*Is there|Are there] a TV in the bedroom?"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"There are some books.\" → There are some [books].",
         "audio": f"{AUDIO}/aula21-dictation.m4a",
         "text": "1. There is a [rug] in the living room.\n2. There are [three|3] boxes in the garage.\n"
                 "3. There isn't a [microwave] in the kitchen.\n4. There are many [plants] on the balcony."},
        {"type": "info",
         "prompt": "Now listen: Sam calls about a room in a hotel.",
         "translation": "Agora ouça: o Sam liga para um hotel e pergunta sobre o quarto. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula21-hotel.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Sam calls a [hotel].",
         "text": "1. Is there a TV in the room? → [*Yes, there is.|No, there isn't.|Yes, there are.]\n"
                 "2. How many beds are there? → [*Two.|One.|Three.]\n"
                 "3. Is there a bathtub? → [*No, there isn't.|Yes, there is.|No, there aren't.]\n"
                 "4. What is there on the balcony? → [*Two chairs and a small table.|A sofa.|Many plants.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Sam asks about a room. → True",
         "statements": [
             {"text": "There is a fridge in the room.", "answer": True, "translation": "Tem uma geladeira no quarto."},
             {"text": "There is a restaurant in the hotel.", "answer": True, "translation": "Tem um restaurante no hotel."},
             {"text": "There are two pools in the hotel.", "answer": False, "translation": "Tem duas piscinas no hotel."},
         ]},
    ],
}

AULA21_SPEAKING = {
    "title": "Speaking — there is, there are",
    "lesson": 21,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: THERE = \"dhér\" (TH com a língua entre os dentes, vibrando) · THERE'S = \"dhérz\" · "
                   "THERE ARE = \"dhér ar\" (sem juntar).",
    "topic": AULA21_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula21-say-s{i}.m4a"} for i, t in enumerate(
             ["There's a chair in the bedroom.", "There's a TV in the living room.", "There's a pillow on the bed.",
              "There are four pillows on the bed.", "There are two chairs in the office.",
              "There isn't a sofa in the living room."], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the questions and answers.",
         "translation": "Ouça e repita as perguntas e respostas.",
         "example": "\"Is there a cushion? Yes, there is.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula21-say-q{i}.m4a"} for i, t in enumerate(
             ["Is there a cushion? Yes, there is.", "Is there a TV in the bedroom? No, there isn't.",
              "Are there pictures on the wall? Yes, there are.", "Is there homework?"], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOUR home.",
         "translation": "Agora responda às perguntas sobre a SUA casa com uma frase completa.",
         "example": "\"Is there a TV in your bedroom?\" → \"No, there isn't.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula21-say-y{i}.m4a"} for i, t in enumerate(
             ["Is there a TV in your bedroom?", "How many chairs are there in your kitchen?",
              "Are there plants in your home?", "What is there in your living room?"], 1)]},
    ],
}

AULA21_READING = {
    "title": "Reading — a beach house",
    "lesson": 21,
    "subject": "Reading",
    "description": "Leia (e ouça) o anúncio e responda às perguntas de acordo com o texto.",
    "topic": AULA21_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the ad for a beach house.",
         "translation": "Leia e ouça o anúncio de uma casa de praia para alugar. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula21-reading.m4a",
         "text": "BEACH HOUSE FOR RENT — UBATUBA\n\n"
                 "This beautiful beach house is perfect for families!\n"
                 "There are three bedrooms and two bathrooms. In the main bedroom, there's a big bed and a balcony.\n"
                 "In the living room, there's a big sofa, two armchairs and a TV.\n"
                 "There's a kitchen with a stove, a big fridge and a microwave. There isn't a dishwasher.\n"
                 "There are four bikes in the garage, and there's a small pool in the garden.\n"
                 "Are there restaurants near the house? Yes, there are! And the beach is only 5 minutes from the house."},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Where is the house? → [In Ubatuba.]",
         "text": "1. How many bedrooms are there? → [*Three.|Two.|Four.]\n"
                 "2. Is there a dishwasher? → [*No, there isn't.|Yes, there is.|No, there aren't.]\n"
                 "3. What is there in the garage? → [*Four bikes.|Two cars.|A pool.]\n"
                 "4. Are there restaurants near the house? → [*Yes, there are.|No, there aren't.|Yes, there is.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "There is a TV in the living room. → True",
         "statements": [
             {"text": "There is a pool in the garden.", "answer": True, "translation": "Tem uma piscina no jardim."},
             {"text": "There are three bathrooms.", "answer": False, "translation": "Tem três banheiros."},
             {"text": "There is a balcony in the main bedroom.", "answer": True,
              "translation": "Tem uma varanda no quarto principal."},
             {"text": "The beach is far from the house.", "answer": False, "translation": "A praia é longe da casa."},
         ]},
        {"type": "fill",
         "prompt": "Complete with there is, there are, there isn't or there aren't.",
         "translation": "Complete com there is, there are, there isn't ou there aren't, de acordo com o texto.",
         "example": "[There is] a big sofa in the living room.",
         "text": "1. [There are] two armchairs in the living room.\n"
                 "2. [There isn't|There is not] a dishwasher.\n"
                 "3. [There is|There's] a small pool in the garden."},
    ],
}

AULA21_WRITING = {
    "title": "Writing — my room",
    "lesson": 21,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ There is a… / There are two… / There isn't a… / There aren't… · "
                   "Perguntas: Is there…? / Are there…?",
    "topic": AULA21_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the questions.",
         "translation": "Escreva as perguntas em inglês.",
         "example": "Tem um sofá na sala? → Is there a sofa in the living room?",
         "text": "1. Tem uma geladeira na cozinha? → [Is there a fridge in the kitchen?]\n"
                 "2. Tem quadros na parede? → [Are there pictures on the wall?]\n"
                 "3. Tem dever de casa? → [Is there homework?]"},
        {"type": "fill",
         "prompt": "Correct the mistake. Write the right sentence.",
         "translation": "Corrija o erro (ter no sentido de existir = there is / there are). Escreva a frase certa.",
         "example": "Has a TV in the bedroom. → There is a TV in the bedroom.",
         "text": "1. Have two chairs in the office. → [There are two chairs in the office.]\n"
                 "2. There are a lamp in the living room. → [There is a lamp in the living room.|There's a lamp in the living room.]"},
        {"type": "free",
         "prompt": "Describe a room in your home with there is, there are, there isn't and there aren't.",
         "translation": "Descreva um cômodo da sua casa com there is, there are, there isn't e there aren't.",
         "example": "In my bedroom, there is a big bed.",
         "model_answer": "In my bedroom, there is a big bed and there are two pillows on it.\n"
                         "There is a wardrobe and a bedside table with a lamp.\n"
                         "There are some pictures on the wall.\n"
                         "There isn't a TV, and there aren't any plants.",
         "keywords": ["there is", "there are", "there isn't"], "min_words": 30, "points": 4},
    ],
}

AULA21_VIDEO = _video(21, AULA21_TOPIC, "Video — Is there a pool?",
                      "uma família procura um hotel para as férias: there is, there are, is there…?",
                      "aula21-video", [
    _q("Is there a pool in the hotel?", "Tem piscina no hotel?", "Yes, there is.", "No, there isn't.",
       "Yes, there are.", "Yes, it has."),
    _q("How many pillows are there on the bed?", "Quantos travesseiros tem na cama?", "Four.", "One.", "Two.", "Three."),
    _q("Is there a bathtub in the bathroom?", "Tem banheira no banheiro?", "No, there isn't.", "Yes, there is.",
       "No, there aren't.", "Yes, there are."),
    _q("What is there near the hotel?", "O que tem perto do hotel?", "A beach and some restaurants.",
       "A big hospital.", "A school.", "An airport."),
    _q("Which sentence is correct?", "Qual frase está correta?", "There are many plants in the garden.",
       "There is many plants in the garden.", "Has many plants in the garden.", "There are many plant in the garden."),
])


# ---------- Aula 22 — Prepositions of Place (https://youtu.be/kszNpewvxtc) ----------

AULA22_TOPIC = "Aula 22 — Prepositions of Place"

AULA22_WORDS = {
    "title": "Prepositions of place",
    "lesson": 22,
    "description": "IN (dentro) · ON (em cima, com contato) · UNDER (embaixo) · BETWEEN (entre, no meio) · NEXT TO (ao lado) · "
                   "BEHIND (atrás) · IN FRONT OF (na frente) · ACROSS FROM (de frente para, face a face) · "
                   "ABOVE / OVER (acima, SEM contato).\n"
                   "Cuidado: ON = encostando (the cat is on the sofa) · ABOVE / OVER = sem encostar (the lamp is above the table).\n"
                   "IN FRONT OF = na frente · ACROSS FROM = de frente, um olhando para o outro.",
    "topic": AULA22_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the prepositions to Portuguese.",
         "translation": "Ligue as preposições ao português.",
         "example": "in → dentro",
         "pairs": [
             {"left": "on", "right": "em cima (encostando)"},
             {"left": "under", "right": "embaixo"},
             {"left": "between", "right": "entre / no meio"},
             {"left": "next to", "right": "ao lado"},
             {"left": "behind", "right": "atrás"},
             {"left": "in front of", "right": "na frente"},
             {"left": "across from", "right": "de frente para"},
             {"left": "above / over", "right": "acima (sem encostar)"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the right preposition.",
         "translation": "Escolha a preposição certa.",
         "example": "O gato está dentro da caixa. → The cat is [in] the box.",
         "text": "1. O gato está em cima do sofá. → The cat is [*on|in|over] the sofa.\n"
                 "2. O gato está embaixo da cadeira. → The cat is [*under|on|behind] the chair.\n"
                 "3. O gato está entre os cachorros. → The cat is [*between|next to|across from] the dogs.\n"
                 "4. O gato está ao lado do relógio. → The cat is [*next to|in front of|on] the clock.\n"
                 "5. O gato está atrás do muro. → The cat is [*behind|in front of|under] the wall.\n"
                 "6. O gato está na frente do computador. → The cat is [*in front of|behind|between] the computer."},
        {"type": "dropdown",
         "prompt": "On or above / over?",
         "translation": "On (encostando) ou above / over (sem encostar)?",
         "example": "The lamp is [above] the table. (pendurada, sem encostar)",
         "text": "1. The book is [*on|above] the table.\n"
                 "2. The plane is [*over|on] the city.\n"
                 "3. The clock is [*on|over] the wall.\n"
                 "4. The pillows are [*on|above] the bed."},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "\"Under\" means embaixo. → True",
         "statements": [
             {"text": "We use \"on\" when there is contact.", "answer": True,
              "translation": "Usamos \"on\" quando há contato."},
             {"text": "\"In front of\" and \"across from\" are the same.", "answer": False,
              "translation": "\"In front of\" e \"across from\" são a mesma coisa."},
             {"text": "\"Between\" is for something in the middle of two things.", "answer": True,
              "translation": "\"Between\" é para algo no meio de duas coisas."},
             {"text": "\"Above\" means embaixo.", "answer": False, "translation": "\"Above\" significa embaixo."},
         ]},
    ],
}

AULA22_WHERE = {
    "title": "Where is…? Where are…?",
    "lesson": 22,
    "description": "WHERE IS the dog? → The dog IS on the bed. (singular)\n"
                   "WHERE ARE my keys? → They ARE in your bag. (plural)\n"
                   "Estrutura: THE + coisa + IS / ARE + preposição + THE + lugar → The ball is under the box.",
    "topic": AULA22_TOPIC,
    "items": [
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras em ordem. (A bola está entre as caixas.)",
         "example": "is / The dog / on / the bed → The dog is on the bed.",
         "tokens": ["The", "ball", "is", "between", "the", "boxes."], "alternatives": []},
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras em ordem. (Meus sapatos estão embaixo da cama.)",
         "example": "are / The books / on / the table → The books are on the table.",
         "tokens": ["My", "shoes", "are", "under", "the", "bed."], "alternatives": []},
        {"type": "dropdown",
         "prompt": "Where is or where are?",
         "translation": "Where is (singular) ou where are (plural)?",
         "example": "[Where are] my keys?",
         "text": "1. [*Where is|Where are] the remote control?\n2. [*Where are|Where is] my glasses?\n"
                 "3. [*Where is|Where are] the cat?\n4. [*Where are|Where is] the children?"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "O cachorro está em cima da cama. → The dog is on the bed.",
         "text": "1. A bola está embaixo da caixa. → [The ball is under the box.]\n"
                 "2. O abajur está ao lado da cama. → [The lamp is next to the bed.]\n"
                 "3. O carro está na frente da casa. → [The car is in front of the house.]\n"
                 "4. Onde está o gato? → [Where is the cat?|Where's the cat?]"},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas.",
         "example": "Where is the dog? → It's on the bed.",
         "pairs": [
             {"left": "Where are my keys?", "right": "They're in your bag."},
             {"left": "Where is the clock?", "right": "It's on the wall."},
             {"left": "Where is the bank?", "right": "It's across from the school."},
             {"left": "Where are the shoes?", "right": "They're under the bed."},
         ]},
    ],
}

AULA22_LISTENING = {
    "title": "Listening — where is it?",
    "lesson": 22,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧",
    "topic": AULA22_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the preposition.",
         "translation": "Ouça e escolha a preposição.",
         "example": "Você ouve: \"The cat is in the box.\" → in",
         "audio": f"{AUDIO}/aula22-preps.m4a",
         "text": "1. The ball is [*under|on|in] the box.\n2. The cat is [*behind|between|next to] the sofa.\n"
                 "3. The lamp is [*next to|in front of|across from] the bed.\n4. The bank is [*across from|behind|on] the park.\n"
                 "5. The picture is [*above|under|in] the sofa."},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete com a preposição.",
         "example": "Você ouve: \"The book is on the table.\" → The book is [on] the table.",
         "audio": f"{AUDIO}/aula22-dictation.m4a",
         "text": "1. My phone is [in] my bag.\n2. The keys are [on] the table.\n3. The dog is [between] the chairs.\n"
                 "4. The car is [in front of] the garage."},
        {"type": "info",
         "prompt": "Now listen: Ben can't find his things!",
         "translation": "Agora ouça: o Ben está atrasado e procura as coisas dele. A mãe dele ajuda. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula22-where.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Ben is late for [school].",
         "text": "1. Where are Ben's shoes? → [*Under the bed.|On the bed.|Behind the door.]\n"
                 "2. Where is his backpack? → [*Behind the door.|In the kitchen.|Under the table.]\n"
                 "3. Where is his phone? → [*In his pocket.|On the sofa.|Next to the TV.]\n"
                 "4. Where is the bus stop? → [*Across from the bakery.|Next to the school.|Behind the house.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Ben is late. → True",
         "statements": [
             {"text": "Ben's keys are on the kitchen table.", "answer": True,
              "translation": "As chaves do Ben estão na mesa da cozinha."},
             {"text": "Ben's mother is angry.", "answer": False, "translation": "A mãe do Ben está com raiva."},
             {"text": "The bus stop is in front of the house.", "answer": False,
              "translation": "O ponto de ônibus fica na frente da casa."},
         ]},
    ],
}

AULA22_SPEAKING = {
    "title": "Speaking — prepositions",
    "lesson": 22,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: BEHIND = \"bi-ráind\" · BETWEEN = \"bi-tuín\" · ABOVE = \"a-bâv\" · "
                   "IN FRONT OF = \"in frânt ov\".",
    "topic": AULA22_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the prepositions.",
         "translation": "Ouça e repita as preposições.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula22-say-w{i}.m4a"} for i, t in enumerate(
             ["in", "on", "under", "between", "next to", "behind", "in front of", "across from", "above", "over"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases.",
         "example": "\"The cat is in the box.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula22-say-s{i}.m4a"} for i, t in enumerate(
             ["The cat is on the sofa.", "The cat is under the chair.", "The cat is between the dogs.",
              "The cat is next to the clock.", "The cat is behind the wall.", "The cat is in front of the computer.",
              "Where is the dog? The dog is on the bed."], 1)]},
        {"type": "speak",
         "prompt": "Now answer about YOUR home.",
         "translation": "Agora responda sobre a SUA casa com uma frase completa.",
         "example": "\"Where is your phone now?\" → \"It's on the table.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula22-say-y{i}.m4a"} for i, t in enumerate(
             ["Where is your phone now?", "Where is your TV?", "Where are your keys?", "What is next to your bed?"], 1)]},
    ],
}

AULA22_READING = {
    "title": "Reading — my neighborhood",
    "lesson": 22,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA22_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Gabriel's text.",
         "translation": "Leia e ouça o texto do Gabriel sobre o bairro dele. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula22-reading.m4a",
         "text": "MY NEIGHBORHOOD\n\n"
                 "I live in a small apartment on Flores Street. I love my neighborhood!\n"
                 "There's a bakery next to my building. I buy bread there every morning.\n"
                 "Across from my building, there's a big park with a lake. There are many trees in the park.\n"
                 "The supermarket is between the bank and the pharmacy.\n"
                 "My gym is behind the supermarket, and there's a bus stop in front of the gym.\n"
                 "And my favorite place? A small Japanese restaurant over the bakery, on the second floor!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Where does Gabriel live? → [On Flores Street.]",
         "text": "1. Where is the bakery? → [*Next to his building.|Behind the gym.|In the park.]\n"
                 "2. What is across from his building? → [*A big park.|The bank.|A restaurant.]\n"
                 "3. Where is the supermarket? → [*Between the bank and the pharmacy.|Next to the park.|Over the bakery.]\n"
                 "4. Where is the bus stop? → [*In front of the gym.|Behind the supermarket.|Next to the bank.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "There is a lake in the park. → True",
         "statements": [
             {"text": "The gym is in front of the supermarket.", "answer": False,
              "translation": "A academia fica na frente do supermercado."},
             {"text": "The restaurant is over the bakery.", "answer": True,
              "translation": "O restaurante fica em cima da padaria."},
             {"text": "Gabriel buys bread every morning.", "answer": True, "translation": "O Gabriel compra pão toda manhã."},
         ]},
        {"type": "fill",
         "prompt": "Complete with the preposition from the text.",
         "translation": "Complete com a preposição do texto.",
         "example": "The bakery is [next to] his building.",
         "text": "1. The park is [across from] his building.\n2. The gym is [behind] the supermarket.\n"
                 "3. The supermarket is [between] the bank and the pharmacy."},
    ],
}

AULA22_WRITING = {
    "title": "Writing — where is it?",
    "lesson": 22,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ The … is / The … are + preposition + the … · "
                   "There is a … next to … · Where is …? / Where are …?",
    "topic": AULA22_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the sentences in English.",
         "translation": "Escreva as frases em inglês.",
         "example": "O gato está embaixo da mesa. → The cat is under the table.",
         "text": "1. Os livros estão na mesa. → [The books are on the table.]\n"
                 "2. O banco fica de frente para a escola. → [The bank is across from the school.]\n"
                 "3. O cachorro está atrás da porta. → [The dog is behind the door.]"},
        {"type": "fill",
         "prompt": "Write the questions.",
         "translation": "Escreva as perguntas em inglês.",
         "example": "Onde está o cachorro? → Where is the dog?",
         "text": "1. Onde estão as minhas chaves? → [Where are my keys?]\n2. Onde está a padaria? → [Where is the bakery?|Where's the bakery?]"},
        {"type": "free",
         "prompt": "Describe your bedroom or your living room. Where are the things? Use 5 different prepositions.",
         "translation": "Descreva o seu quarto ou a sua sala. Onde estão as coisas? Use 5 preposições diferentes.",
         "example": "My bed is between the window and the wardrobe.",
         "model_answer": "In my bedroom, my bed is between the window and the wardrobe.\n"
                         "There is a lamp on the bedside table, next to the bed.\n"
                         "My shoes are under the bed, and there's a picture above the bed.\n"
                         "My desk is in front of the window.",
         "keywords": ["next to", "under", "between", "on"], "min_words": 30, "points": 4},
    ],
}

AULA22_VIDEO = _video(22, AULA22_TOPIC, "Video — Where are the pets?",
                      "a Ana mostra onde estão os bichinhos dela e dos vizinhos: on, behind, across from, in front of, in…",
                      "aula22-video", [
    _q("Where is Luna?", "Onde está a Luna?", "On the bed.", "Under the bed.", "Behind the bed.", "Next to the bed."),
    _q("Where is Snow?", "Onde está o Snow?", "Behind the window.", "On the window.", "Under the window.",
       "Between the windows."),
    _q("Where is Mimi?", "Onde está a Mimi?", "Across from Tiger.", "Under Tiger.", "Behind Tiger.", "On Tiger."),
    _q("Where is Bob's ball?", "Onde está a bola do Bob?", "In front of Bob.", "Behind Bob.", "Over Bob.",
       "In the box."),
    _q("Where are Ana and Tom?", "Onde estão a Ana e o Tom?", "In the park.", "In the bedroom.", "On the sofa.",
       "Behind the house."),
])


# ---------- Aula 23 — Present Continuous (affirmative) (https://youtu.be/SMzz0WFTnv0) ----------

AULA23_TOPIC = "Aula 23 — Present Continuous (affirmative)"

AULA23_ING = {
    "title": "Verbs + ING",
    "lesson": 23,
    "description": "PRESENT CONTINUOUS = o que está acontecendo AGORA (eu estou trabalhando, ele está dormindo).\n"
                   "Verbo + ING = nosso \"-ando, -endo, -indo\": cook → cooking · watch → watching · read → reading.\n"
                   "Termina em E → o E cai: move → moving · dance → dancing · drive → driving · ride → riding · use → using.\n"
                   "Consoante + vogal + consoante (1 sílaba) → dobra a última letra: shop → shopping · swim → swimming · "
                   "sit → sitting · cut → cutting · rob → robbing.\n"
                   "Pronúncia: o G do ING quase some (\"cúkin\"). TALK: L mudo (\"tók\") · LISTEN: T mudo (\"lísen\").",
    "topic": AULA23_TOPIC,
    "items": [
        {"type": "match",
         "prompt": "Match the verbs to Portuguese.",
         "translation": "Ligue os verbos ao português.",
         "example": "to sleep → dormir",
         "pairs": [
             {"left": "to talk", "right": "conversar"},
             {"left": "to listen", "right": "escutar"},
             {"left": "to wear", "right": "usar (roupa, acessório)"},
             {"left": "to ride", "right": "andar (de bicicleta, moto)"},
             {"left": "to move", "right": "mudar / mexer"},
             {"left": "to cut", "right": "cortar"},
         ]},
        {"type": "group",
         "prompt": "How do we add ING? Put each verb in the right group.",
         "translation": "Como acrescentamos o ING? Coloque cada verbo no grupo certo.",
         "example": "cook → + ing (cooking) · dance → e cai (dancing) · swim → dobra (swimming)",
         "categories": ["+ ing", "drop the E + ing", "double + ing"],
         "words": [
             {"text": "work", "category": "+ ing"}, {"text": "study", "category": "+ ing"},
             {"text": "play", "category": "+ ing"}, {"text": "wear", "category": "+ ing"},
             {"text": "drive", "category": "drop the E + ing"}, {"text": "ride", "category": "drop the E + ing"},
             {"text": "use", "category": "drop the E + ing"}, {"text": "move", "category": "drop the E + ing"},
             {"text": "shop", "category": "double + ing"}, {"text": "sit", "category": "double + ing"},
             {"text": "cut", "category": "double + ing"}, {"text": "swim", "category": "double + ing"},
         ]},
        {"type": "fill",
         "prompt": "Write the verb + ING.",
         "translation": "Escreva o verbo com ING.",
         "example": "read → reading",
         "text": "1. dance → [dancing]\n2. swim → [swimming]\n3. drink → [drinking]\n4. sit → [sitting]\n"
                 "5. go → [going]\n6. drive → [driving]"},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "We use the present continuous for things happening now. → True",
         "statements": [
             {"text": "In \"talk\", we don't say the letter L.", "answer": True,
              "translation": "Em \"talk\", a gente não pronuncia a letra L."},
             {"text": "\"Dance\" + ING = \"danceing\".", "answer": False, "translation": "\"Dance\" + ING = \"danceing\"."},
             {"text": "\"Shop\" + ING = \"shopping\", with two Ps.", "answer": True,
              "translation": "\"Shop\" + ING = \"shopping\", com dois Ps."},
             {"text": "For clothes, we use the verb \"wear\".", "answer": True,
              "translation": "Para roupas, usamos o verbo \"wear\"."},
         ]},
    ],
}

AULA23_SENTENCES = {
    "title": "What is he doing?",
    "lesson": 23,
    "description": "ESTRUTURA: sujeito + AM / IS / ARE + verbo-ING. (o verb to be aqui = estar)\n"
                   "I am (I'm) studying · you are (you're) working · he / she / it is (he's, she's) cooking · "
                   "we are (we're) dancing · they are (they're) playing tennis.\n"
                   "What is he doing? → He's cooking. · What are they doing? → They're riding a bike.\n"
                   "I'm wearing a uniform. (wear = usar roupa) · I'm sitting. (= estou sentado)",
    "topic": AULA23_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose am, is or are.",
         "translation": "Escolha am, is ou are.",
         "example": "She [is] reading a book.",
         "text": "1. I [*am|is|are] studying.\n2. My brother [*is|are|am] singing.\n3. They [*are|is|am] playing tennis.\n"
                 "4. We [*are|is|am] watching a movie.\n5. The dog [*is|are|am] sleeping."},
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras em ordem. (Ela está usando salto alto.)",
         "example": "is / He / cooking → He is cooking.",
         "tokens": ["She", "is", "wearing", "high", "heels."], "alternatives": []},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (O que eles estão fazendo?)",
         "example": "is / What / doing / she → What is she doing?",
         "tokens": ["What", "are", "they", "doing?"], "alternatives": []},
        {"type": "fill",
         "prompt": "Translate (from the lesson).",
         "translation": "Traduza as frases da aula.",
         "example": "Eu estou estudando. → I'm studying.",
         "text": "1. Meu irmão está cantando. → [My brother is singing.|My brother's singing.]\n"
                 "2. Elas estão jogando tênis. → [They are playing tennis.|They're playing tennis.]\n"
                 "3. Minha melhor amiga está assistindo TV. → [My best friend is watching TV.]\n"
                 "4. Ele está tomando banho. → [He is taking a shower.|He's taking a shower.|He is having a shower.|He's having a shower.]"},
        {"type": "match",
         "prompt": "Match the sentences to Portuguese.",
         "translation": "Ligue as frases ao português.",
         "example": "He's cooking. → Ele está cozinhando.",
         "pairs": [
             {"left": "They're riding a bike.", "right": "Eles estão andando de bicicleta."},
             {"left": "She's driving.", "right": "Ela está dirigindo."},
             {"left": "I'm sitting.", "right": "Estou sentado."},
             {"left": "We're moving.", "right": "Estamos nos mudando."},
             {"left": "He's cutting the bread.", "right": "Ele está cortando o pão."},
         ]},
    ],
}

AULA23_LISTENING = {
    "title": "Listening — what are they doing?",
    "lesson": 23,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧",
    "topic": AULA23_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the verb you hear.",
         "translation": "Ouça e escolha o verbo que você ouve.",
         "example": "Você ouve: \"She's reading.\" → reading",
         "audio": f"{AUDIO}/aula23-verbs.m4a",
         "text": "1. He's [*sitting|eating|cutting].\n2. They're [*shopping|sleeping|swimming].\n"
                 "3. I'm [*talking|walking|working].\n4. She's [*riding|reading|driving] a bike.\n5. We're [*listening|dancing|studying] to music."},
        {"type": "fill",
         "prompt": "Dictation: listen and write the verb + ING.",
         "translation": "Ditado: ouça e escreva o verbo com ING.",
         "example": "Você ouve: \"I'm cooking.\" → I'm [cooking].",
         "audio": f"{AUDIO}/aula23-dictation.m4a",
         "text": "1. She's [swimming].\n2. They're [dancing].\n3. He's [driving].\n4. I'm [studying].\n5. We're [watching] TV."},
        {"type": "info",
         "prompt": "Now listen: Lucy calls her husband, Dan.",
         "translation": "Agora ouça: a Lucy liga para o marido, o Dan, e pergunta o que a família está fazendo em casa. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula23-call.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Lucy is at [work].",
         "text": "1. What is Dan doing? → [*He's cooking dinner.|He's sleeping.|He's watching TV.]\n"
                 "2. What is Sophie doing? → [*She's studying.|She's dancing.|She's swimming.]\n"
                 "3. What is Max doing? → [*He's playing video games.|He's reading.|He's riding a bike.]\n"
                 "4. What is the dog doing? → [*It's sleeping on the sofa.|It's eating.|It's playing in the garden.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Lucy is working. → True",
         "statements": [
             {"text": "Dan is making pasta.", "answer": True, "translation": "O Dan está fazendo macarrão."},
             {"text": "Lucy is driving home now.", "answer": False, "translation": "A Lucy está dirigindo para casa agora."},
             {"text": "Sophie is listening to music.", "answer": True, "translation": "A Sophie está ouvindo música."},
         ]},
    ],
}

AULA23_SPEAKING = {
    "title": "Speaking — right now",
    "lesson": 23,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: ING = \"in\" (o G quase some) · TALK = \"tók\" · LISTEN = \"lísen\" · use as contrações: "
                   "I'm, he's, they're.",
    "topic": AULA23_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the verbs.",
         "translation": "Ouça e repita os verbos (forma base e com ING).",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula23-say-w{i}.m4a"} for i, t in enumerate(
             ["cook, cooking", "watch, watching", "read, reading", "talk, talking", "listen, listening", "dance, dancing",
              "drive, driving", "swim, swimming", "sit, sitting", "shop, shopping"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases.",
         "example": "\"He's cooking.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula23-say-s{i}.m4a"} for i, t in enumerate(
             ["What is he doing? He's cooking.", "She's watching TV.", "They're riding a bike.", "He's taking a shower.",
              "I'm wearing a uniform.", "My best friend is watching TV."], 1)]},
        {"type": "speak",
         "prompt": "Now answer about YOU, right now.",
         "translation": "Agora responda sobre VOCÊ, neste momento, com uma frase completa.",
         "example": "\"What are you doing now?\" → \"I'm studying English.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula23-say-y{i}.m4a"} for i, t in enumerate(
             ["What are you doing now?", "What are you wearing today?", "What is your family doing now?",
              "Are you sitting or standing?"], 1)]},
    ],
}

AULA23_READING = {
    "title": "Reading — a postcard from Rio",
    "lesson": 23,
    "subject": "Reading",
    "description": "Leia (e ouça) o cartão-postal e responda às perguntas de acordo com o texto.",
    "topic": AULA23_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Emma's postcard.",
         "translation": "Leia e ouça o cartão-postal da Emma, que está de férias no Rio. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula23-reading.m4a",
         "text": "A POSTCARD FROM RIO\n\n"
                 "Dear Grandma,\n"
                 "I'm writing this postcard on the beach in Copacabana! It's a beautiful day, and it's very hot.\n"
                 "Right now, Dad is swimming in the sea, and Mom is reading a book under an umbrella.\n"
                 "My brother Jack is playing volleyball with some Brazilian boys. He's having a great time!\n"
                 "I'm sitting on the sand, and I'm drinking coconut water. It's delicious!\n"
                 "People here are very friendly. A man is selling ice cream next to me, and some girls are dancing.\n"
                 "Love, Emma"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Where is Emma? → [On the beach in Copacabana.]",
         "text": "1. What is Dad doing? → [*He's swimming in the sea.|He's reading a book.|He's playing volleyball.]\n"
                 "2. What is Mom doing? → [*She's reading a book.|She's dancing.|She's swimming.]\n"
                 "3. What is Emma drinking? → [*Coconut water.|Coffee.|Orange juice.]\n"
                 "4. What is the man next to Emma doing? → [*He's selling ice cream.|He's dancing.|He's sleeping.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "It's a hot day. → True",
         "statements": [
             {"text": "Jack is playing soccer.", "answer": False, "translation": "O Jack está jogando futebol."},
             {"text": "Emma is sitting on the sand.", "answer": True, "translation": "A Emma está sentada na areia."},
             {"text": "Some girls are dancing.", "answer": True, "translation": "Algumas meninas estão dançando."},
             {"text": "Emma is writing to her mother.", "answer": False, "translation": "A Emma está escrevendo para a mãe."},
         ]},
        {"type": "fill",
         "prompt": "Complete with the verb + ING from the text.",
         "translation": "Complete com o verbo com ING do texto.",
         "example": "Emma is [writing] a postcard.",
         "text": "1. Dad is [swimming] in the sea.\n2. Jack is [playing] volleyball.\n3. Emma is [sitting] on the sand."},
    ],
}

AULA23_WRITING = {
    "title": "Writing — what's happening now?",
    "lesson": 23,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ sujeito + am / is / are + verbo-ING. Lembre das regras: dance → dancing · swim → swimming.",
    "topic": AULA23_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the sentences in the present continuous.",
         "translation": "Escreva as frases no present continuous.",
         "example": "he / cook → He is cooking.",
         "text": "1. she / dance → [She is dancing.|She's dancing.]\n"
                 "2. they / swim → [They are swimming.|They're swimming.]\n"
                 "3. I / ride a bike → [I am riding a bike.|I'm riding a bike.]\n"
                 "4. we / sit on the sofa → [We are sitting on the sofa.|We're sitting on the sofa.]"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu estou estudando. → I'm studying.",
         "text": "1. Ela está dirigindo. → [She is driving.|She's driving.]\n"
                 "2. Nós estamos ouvindo música. → [We are listening to music.|We're listening to music.]\n"
                 "3. O que você está fazendo? → [What are you doing?]"},
        {"type": "free",
         "prompt": "Look around you (at home, at work, on the street). What are the people doing right now? Write 5 sentences.",
         "translation": "Olhe ao seu redor (em casa, no trabalho, na rua). O que as pessoas estão fazendo agora? Escreva 5 frases.",
         "example": "My mother is cooking lunch.",
         "model_answer": "I'm sitting on the sofa, and I'm studying English.\n"
                         "My mother is cooking lunch in the kitchen.\n"
                         "My father is watching TV.\n"
                         "My little brother is playing video games, and the cat is sleeping on the bed.",
         "keywords": ["I'm", "is", "and"], "min_words": 25, "points": 4},
    ],
}

AULA23_VIDEO = _video(23, AULA23_TOPIC, "Video — Saturday in the city",
                      "um sábado na cidade: o que as pessoas estão fazendo agora? riding, reading, sitting, dancing, swimming…",
                      "aula23-video", [
    _q("What is the boy doing?", "O que o menino está fazendo?", "He's riding a bike.", "He's swimming.",
       "He's sleeping.", "He's cooking."),
    _q("What is the young man doing?", "O que o rapaz está fazendo?", "He's reading a book.", "He's running.",
       "He's driving.", "He's eating."),
    _q("What are the friends doing?", "O que os amigos estão fazendo?", "They're sitting on the grass and talking.",
       "They're watching TV at home.", "They're shopping.", "They're swimming."),
    _q("Which is correct?", "Qual está correto?", "She's dancing.", "She's danceing.", "She dancing.", "She's dances."),
    _q("What is the woman doing?", "O que a mulher está fazendo?", "She's swimming.", "She's sitting.", "She's talking.",
       "She's reading."),
])


# ---------- Aula 24 — Present Continuous (negative) (https://youtu.be/EDE9PHpTMN0) ----------

AULA24_TOPIC = "Aula 24 — Present Continuous (negative)"

AULA24_FORMS = {
    "title": "He isn't working",
    "lesson": 24,
    "description": "NEGATIVE: é só colocar NOT depois do verb to be (sem don't / doesn't!):\n"
                   "I am not (I'm not) working · you are not (you aren't / you're not) · he / she / it is not (isn't / he's not) · "
                   "we / they are not (aren't / we're not).\n"
                   "AM NOT não tem contraction junta: I'm not (nunca \"I amn't\").\n"
                   "He is sleeping. He isn't working. (Ele está dormindo. Ele não está trabalhando.)",
    "topic": AULA24_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Choose the right negative form.",
         "translation": "Escolha a forma negativa certa.",
         "example": "He [isn't] working.",
         "text": "1. I [*'m not|amn't|don't] sleeping.\n"
                 "2. They [*aren't|isn't|don't] eating.\n"
                 "3. She [*isn't|aren't|doesn't] walking.\n"
                 "4. We [*aren't|isn't|amn't] watching TV.\n"
                 "5. The dog [*isn't|aren't|doesn't] playing."},
        {"type": "fill",
         "prompt": "Make the sentences negative (use contractions).",
         "translation": "Passe as frases para a negativa (use contractions).",
         "example": "He is working. → He isn't working.",
         "text": "1. They are running. → [They aren't running.|They're not running.]\n"
                 "2. She is cooking. → [She isn't cooking.|She's not cooking.]\n"
                 "3. I am studying. → [I'm not studying.|I am not studying.]\n"
                 "4. We are playing tennis. → [We aren't playing tennis.|We're not playing tennis.]"},
        {"type": "order",
         "prompt": "Put the words in order.",
         "translation": "Coloque as palavras em ordem. (Eles não estão correndo.)",
         "example": "isn't / She / walking → She isn't walking.",
         "tokens": ["They", "aren't", "running."], "alternatives": []},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "We use NOT after the verb to be. → True",
         "statements": [
             {"text": "We say \"He doesn't working\".", "answer": False, "translation": "Dizemos \"He doesn't working\"."},
             {"text": "\"Isn't\" = is not, and \"aren't\" = are not.", "answer": True,
              "translation": "\"Isn't\" = is not, e \"aren't\" = are not."},
             {"text": "\"I amn't\" is correct.", "answer": False, "translation": "\"I amn't\" está correto."},
             {"text": "\"You're not\" and \"you aren't\" mean the same thing.", "answer": True,
              "translation": "\"You're not\" e \"you aren't\" significam a mesma coisa."},
         ]},
    ],
}

AULA24_PICTURES = {
    "title": "Not this… but that!",
    "lesson": 24,
    "description": "Corrigindo o que está acontecendo: NEGATIVE + AFFIRMATIVE.\n"
                   "They aren't running. They're riding a bike. · She isn't walking. She's driving.\n"
                   "run (correr) · ride a bike (andar de bicicleta) · walk (andar a pé) · drive (dirigir).",
    "topic": AULA24_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Complete: negative + affirmative.",
         "translation": "Complete: negativa + afirmativa.",
         "example": "She isn't walking. She's [driving].",
         "text": "1. They aren't running. They're [*riding|running|sleeping] a bike.\n"
                 "2. He isn't sleeping. He's [*working|sleeping|not] at the office.\n"
                 "3. I'm not eating. I'm [*cooking|eating|not] dinner for my family.\n"
                 "4. We aren't watching TV. We're [*reading|watching|aren't] books."},
        {"type": "match",
         "prompt": "Match the sentences.",
         "translation": "Ligue as frases que combinam.",
         "example": "She isn't walking. → She's driving.",
         "pairs": [
             {"left": "He isn't working.", "right": "He's sleeping."},
             {"left": "They aren't eating.", "right": "They're cooking."},
             {"left": "I'm not studying.", "right": "I'm playing video games."},
             {"left": "She isn't swimming.", "right": "She's sitting on the sand."},
         ]},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Ele não está trabalhando. → He isn't working.",
         "text": "1. Elas estão cozinhando, elas não estão comendo. → [They are cooking, they aren't eating.|They're cooking, they aren't eating.|They're cooking, they're not eating.|They are cooking, they are not eating.]\n"
                 "2. Ela não está andando. Ela está dirigindo. → [She isn't walking. She's driving.|She isn't walking. She is driving.|She's not walking. She's driving.]\n"
                 "3. Eu não estou dormindo. → [I'm not sleeping.|I am not sleeping.]"},
        {"type": "dropdown",
         "prompt": "Present simple or present continuous negative?",
         "translation": "Negativa do present simple (rotina: don't / doesn't) ou do present continuous (agora: isn't / aren't)?",
         "example": "He [doesn't] work on Sundays. · He [isn't] working now.",
         "text": "1. She [*doesn't|isn't] eat meat. (rotina)\n"
                 "2. She [*isn't|doesn't] eating now.\n"
                 "3. They [*aren't|don't] studying at the moment.\n"
                 "4. They [*don't|aren't] study on Saturdays."},
    ],
}

AULA24_LISTENING = {
    "title": "Listening — not right now!",
    "lesson": 24,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧",
    "topic": AULA24_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Affirmative or negative? Listen and choose.",
         "translation": "Afirmativa ou negativa? Ouça e escolha.",
         "example": "Você ouve: \"He isn't working.\" → He isn't working.",
         "audio": f"{AUDIO}/aula24-forms.m4a",
         "text": "1. [*She isn't cooking.|She's cooking.]\n2. [*They're running.|They aren't running.]\n"
                 "3. [*I'm not sleeping.|I'm sleeping.]\n4. [*We aren't watching TV.|We're watching TV.]\n"
                 "5. [*He's driving.|He isn't driving.]"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete.",
         "example": "Você ouve: \"She isn't walking.\" → She [isn't] walking.",
         "audio": f"{AUDIO}/aula24-dictation.m4a",
         "text": "1. They [aren't] eating. They're [cooking].\n2. He [isn't] working. He's [sleeping].\n"
                 "3. I'm [not] studying. I'm [reading]."},
        {"type": "info",
         "prompt": "Now listen: a babysitter is talking to the children's mother on the phone.",
         "translation": "Agora ouça: a mãe liga para a babá para saber o que as crianças estão fazendo. "
                        "Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula24-babysitter.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "The babysitter's name is [Ryan].",
         "text": "1. Is Mia sleeping? → [*No, she's drawing.|Yes, she is.|No, she's swimming.]\n"
                 "2. Is Leo doing his homework? → [*No, he's playing soccer in the garden.|Yes, he is.|No, he's sleeping.]\n"
                 "3. What is the baby doing? → [*She's sleeping.|She's eating.|She's crying.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "The mother is calling. → True",
         "statements": [
             {"text": "The children are watching TV.", "answer": False, "translation": "As crianças estão vendo TV."},
             {"text": "The baby isn't crying.", "answer": True, "translation": "O bebê não está chorando."},
             {"text": "Ryan is cooking dinner.", "answer": True, "translation": "O Ryan está fazendo o jantar."},
         ]},
    ],
}

AULA24_SPEAKING = {
    "title": "Speaking — negative",
    "lesson": 24,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dicas da aula: ISN'T = \"ízent\" · AREN'T = \"árent\" · I'M NOT = \"áim nót\".",
    "topic": AULA24_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat.",
         "translation": "Ouça e repita as formas negativas.",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula24-say-w{i}.m4a"} for i, t in enumerate(
             ["I'm not", "you aren't", "he isn't", "she isn't", "we aren't", "they aren't"], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the sentences.",
         "translation": "Ouça e repita as frases.",
         "example": "\"He's sleeping. He isn't working.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula24-say-s{i}.m4a"} for i, t in enumerate(
             ["He's sleeping. He isn't working.", "They're cooking. They aren't eating.",
              "They aren't running. They're riding a bike.", "She isn't walking. She's driving.",
              "I'm not watching TV. I'm studying."], 1)]},
        {"type": "speak",
         "prompt": "Now talk about YOU, right now.",
         "translation": "Agora fale sobre VOCÊ neste momento: uma frase negativa e uma afirmativa.",
         "example": "\"Are you sleeping?\" → \"No! I'm not sleeping. I'm studying English.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula24-say-y{i}.m4a"} for i, t in enumerate(
             ["Are you sleeping now?", "Are you watching TV?", "Are you working right now?",
              "Is your best friend studying now?"], 1)]},
    ],
}

AULA24_READING = {
    "title": "Reading — a lazy Sunday",
    "lesson": 24,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA24_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Paulo's message.",
         "translation": "Leia e ouça a mensagem do Paulo para um amigo. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula24-reading.m4a",
         "text": "A LAZY SUNDAY\n\n"
                 "Hi, Rafa! Today is Sunday, and nobody in my family is working!\n"
                 "My father isn't reading the newspaper today. He's sleeping on the sofa.\n"
                 "My mother isn't cooking. We're ordering pizza for lunch!\n"
                 "My sister isn't studying for her test. She's talking to her boyfriend on the phone.\n"
                 "And me? I'm not doing my homework. I'm writing to you and listening to music.\n"
                 "It's raining, so we aren't going to the beach. But it's a good day!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "What day is it? → [Sunday.]",
         "text": "1. What is Paulo's father doing? → [*He's sleeping on the sofa.|He's reading the newspaper.|He's cooking.]\n"
                 "2. Is his mother cooking? → [*No, she isn't.|Yes, she is.|No, she doesn't.]\n"
                 "3. What is his sister doing? → [*She's talking on the phone.|She's studying.|She's sleeping.]\n"
                 "4. Why aren't they going to the beach? → [*Because it's raining.|Because they're working.|Because it's cold.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "The family is having pizza. → True",
         "statements": [
             {"text": "Paulo is doing his homework.", "answer": False, "translation": "O Paulo está fazendo a lição de casa."},
             {"text": "Paulo is listening to music.", "answer": True, "translation": "O Paulo está ouvindo música."},
             {"text": "Paulo's sister is studying for a test.", "answer": False,
              "translation": "A irmã do Paulo está estudando para uma prova."},
         ]},
        {"type": "fill",
         "prompt": "Complete with isn't, aren't or 'm not.",
         "translation": "Complete com isn't, aren't ou 'm not, de acordo com o texto.",
         "example": "His mother [isn't] cooking.",
         "text": "1. His father [isn't] reading the newspaper.\n2. Paulo: \"I['m not] doing my homework.\"\n"
                 "3. They [aren't] going to the beach."},
    ],
}

AULA24_WRITING = {
    "title": "Writing — not now!",
    "lesson": 24,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ sujeito + isn't / aren't / 'm not + verbo-ING. Depois diga o que a pessoa ESTÁ fazendo.",
    "topic": AULA24_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Correct the sentences: write the negative + the affirmative.",
         "translation": "Corrija: escreva a negativa e depois a afirmativa com a palavra entre parênteses.",
         "example": "She is walking. (driving) → She isn't walking. She's driving.",
         "text": "1. He is running. (swimming) → [He isn't running. He's swimming.|He isn't running. He is swimming.|He's not running. He's swimming.]\n"
                 "2. They are sleeping. (studying) → [They aren't sleeping. They're studying.|They aren't sleeping. They are studying.|They're not sleeping. They're studying.]"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu não estou trabalhando. → I'm not working.",
         "text": "1. Ela não está usando uniforme. → [She isn't wearing a uniform.|She's not wearing a uniform.]\n"
                 "2. Nós não estamos assistindo TV. → [We aren't watching TV.|We're not watching TV.]"},
        {"type": "free",
         "prompt": "It's Sunday. What are you and your family doing? What aren't you doing? Write 5 sentences.",
         "translation": "É domingo. O que você e a sua família estão fazendo? O que vocês NÃO estão fazendo? Escreva 5 frases.",
         "example": "I'm not working. I'm reading a book.",
         "model_answer": "It's Sunday, and I'm not working. I'm reading a book on the balcony.\n"
                         "My husband isn't cooking. He's ordering pizza!\n"
                         "My children aren't studying. They're playing in the garden.\n"
                         "The dog isn't sleeping. It's playing with the children.",
         "keywords": ["I'm not", "isn't", "aren't"], "min_words": 30, "points": 4},
    ],
}

AULA24_VIDEO = _video(24, AULA24_TOPIC, "Video — Not right now!",
                      "o que as pessoas NÃO estão fazendo e o que elas estão fazendo: isn't, aren't, 'm not…",
                      "aula24-video", [
    _q("Is Carlos working?", "O Carlos está trabalhando?", "No, he isn't. He's sleeping.", "Yes, he is.",
       "No, he doesn't.", "Yes, he's."),
    _q("Are the friends running?", "Os amigos estão correndo?", "No, they aren't. They're riding bikes.",
       "Yes, they are.", "No, they don't.", "No, they isn't."),
    _q("What is Júlia doing?", "O que a Júlia está fazendo?", "She's driving.", "She's walking.",
       "She's sleeping.", "She's cooking."),
    _q("Which sentence is correct?", "Qual frase está correta?", "She isn't eating. She's cooking.",
       "She doesn't eating. She's cooking.", "She not eating. She cooking.", "She isn't eat. She's cook."),
    _q("Is Ana watching TV?", "A Ana está vendo TV?", "No, she isn't. She's reading.", "Yes, she is.",
       "No, she doesn't.", "No, she aren't."),
])


# ---------- Aula 25 — Present Continuous (interrogative) (https://youtu.be/YjheXHJCzqs) ----------

AULA25_TOPIC = "Aula 25 — Present Continuous (interrogative)"

AULA25_YESNO = {
    "title": "Is he cooking?",
    "lesson": 25,
    "description": "PERGUNTA = inverta a ordem: o verb to be vem ANTES do sujeito.\n"
                   "He is cooking. → IS HE cooking? (Ele está cozinhando?)\n"
                   "Am I…? · Are you…? · Is he / she / it…? · Are we…? · Are they…?\n"
                   "Em português só mudamos a entonação; em inglês a ORDEM muda!\n"
                   "Respostas: Yes, she is. / No, she isn't. · Yes, they are. / No, they aren't.\n"
                   "Am I speaking too fast? (Estou falando rápido demais?) · Is she feeling OK? (Ela está se sentindo bem?)",
    "topic": AULA25_TOPIC,
    "items": [
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Ela está se sentindo bem?)",
         "example": "he / Is / cooking → Is he cooking?",
         "tokens": ["Is", "she", "feeling", "OK?"], "alternatives": []},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Eu estou falando rápido demais?)",
         "example": "they / Are / working → Are they working?",
         "tokens": ["Am", "I", "speaking", "too", "fast?"], "alternatives": []},
        {"type": "dropdown",
         "prompt": "Am, is or are?",
         "translation": "Am, is ou are?",
         "example": "[Are] they working?",
         "text": "1. [*Is|Are|Am] he sleeping?\n2. [*Are|Is|Am] you studying?\n3. [*Am|Is|Are] I bothering you?\n"
                 "4. [*Are|Is|Am] your parents traveling?\n5. [*Is|Are|Am] the baby crying?"},
        {"type": "dropdown",
         "prompt": "Choose the right short answer.",
         "translation": "Escolha a resposta curta certa.",
         "example": "Is she feeling OK? (✓) → [Yes, she is.]",
         "text": "1. Are they eating sushi? (✗) → [*No, they aren't.|No, they don't.|No, they isn't.]\n"
                 "2. Is he working? (✓) → [*Yes, he is.|Yes, he does.|Yes, he's.]\n"
                 "3. Are you listening? (✓) → [*Yes, I am.|Yes, I'm.|Yes, I do.]\n"
                 "4. Is it raining? (✗) → [*No, it isn't.|No, it doesn't.|No, it not.]"},
        {"type": "fill",
         "prompt": "Make questions.",
         "translation": "Transforme as frases em perguntas.",
         "example": "He is cooking. → Is he cooking?",
         "text": "1. She is sleeping. → [Is she sleeping?]\n2. They are playing soccer. → [Are they playing soccer?]\n"
                 "3. You are working today. → [Are you working today?]"},
    ],
}

AULA25_WH = {
    "title": "What are you doing?",
    "lesson": 25,
    "description": "WH- QUESTIONS: a question word é SEMPRE a primeira palavra, depois a ordem invertida:\n"
                   "QUESTION WORD + AM / IS / ARE + sujeito + verbo-ING?\n"
                   "What is she eating? → She's eating sushi. · Why is he crying? → Because he lost his toy.\n"
                   "How is she feeling? → She's very excited. · Where are you going? → I'm going to the bank.\n"
                   "Erro comum: \"Why he is crying?\" ✗ → \"Why IS HE crying?\" ✓",
    "topic": AULA25_TOPIC,
    "items": [
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Por que ele está chorando?)",
         "example": "is / What / eating / she → What is she eating?",
         "tokens": ["Why", "is", "he", "crying?"], "alternatives": []},
        {"type": "order",
         "prompt": "Put the words in order to make a question.",
         "translation": "Coloque as palavras em ordem para formar a pergunta. (Como ela está se sentindo?)",
         "example": "are / Where / going / you → Where are you going?",
         "tokens": ["How", "is", "she", "feeling?"], "alternatives": []},
        {"type": "choice",
         "prompt": "Which question is correct?",
         "translation": "Qual pergunta está correta?",
         "example": "Why is he crying? ✓",
         "options": ["What are you doing?", "What you are doing?", "What do you doing?", "What you doing are?"],
         "correct": 0},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas.",
         "example": "What is she eating? → She's eating sushi.",
         "pairs": [
             {"left": "Why is he crying?", "right": "Because he lost his toy."},
             {"left": "How is she feeling?", "right": "She's very excited."},
             {"left": "Where are you going?", "right": "I'm going to the bank."},
             {"left": "What are they eating?", "right": "They're eating pizza."},
             {"left": "Who is she talking to?", "right": "Her mother."},
         ]},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "O que ela está comendo? → What is she eating?",
         "text": "1. O que você está fazendo? → [What are you doing?]\n"
                 "2. Por que ele está chorando? → [Why is he crying?]\n"
                 "3. Onde eles estão trabalhando? → [Where are they working?]"},
    ],
}

AULA25_LISTENING = {
    "title": "Listening — what are you doing?",
    "lesson": 25,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧",
    "topic": AULA25_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Listen and choose the question you hear.",
         "translation": "Ouça e escolha a pergunta que você ouve.",
         "example": "Você ouve: \"Is he cooking?\" → Is he cooking?",
         "audio": f"{AUDIO}/aula25-questions.m4a",
         "text": "1. [*Are they working?|Is he working?]\n2. [*What is she eating?|What are you eating?]\n"
                 "3. [*Why is he crying?|Why is she crying?]\n4. [*Are you listening?|Am I listening?]\n"
                 "5. [*Where are you going?|Where is he going?]"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete the questions.",
         "translation": "Ditado: ouça e complete as perguntas.",
         "example": "Você ouve: \"Is it raining?\" → [Is] it raining?",
         "audio": f"{AUDIO}/aula25-dictation.m4a",
         "text": "1. [Are] you studying?\n2. What [is] he [doing]?\n3. How [are] you [feeling]?\n4. [Am] I speaking too fast?"},
        {"type": "info",
         "prompt": "Now listen: two friends are on a video call.",
         "translation": "Agora ouça: dois amigos, a Nina e o Pedro, estão numa chamada de vídeo. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula25-call.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Nina and Pedro are [friends].",
         "text": "1. Where is Pedro? → [*At the airport.|At home.|At work.]\n"
                 "2. Where is he going? → [*To London.|To Paris.|To Rio.]\n"
                 "3. What is Nina eating? → [*Sushi.|Pizza.|A sandwich.]\n"
                 "4. How is Pedro feeling? → [*Excited and a little tired.|Sad.|Angry.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the dialogue.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o diálogo.",
         "example": "Pedro is traveling. → True",
         "statements": [
             {"text": "Pedro is traveling for work.", "answer": False, "translation": "O Pedro está viajando a trabalho."},
             {"text": "Nina is watching a movie.", "answer": True, "translation": "A Nina está assistindo a um filme."},
             {"text": "Pedro's sister is studying in London.", "answer": True,
              "translation": "A irmã do Pedro está estudando em Londres."},
         ]},
    ],
}

AULA25_SPEAKING = {
    "title": "Speaking — questions",
    "lesson": 25,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: nas perguntas de yes / no, a voz SOBE no final ↗ (Are you working?). "
                   "Nas perguntas com what, why, how…, a voz DESCE ↘ (What are you doing?).",
    "topic": AULA25_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the yes / no questions.",
         "translation": "Ouça e repita as perguntas de yes / no (voz sobe no final).",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula25-say-q{i}.m4a"} for i, t in enumerate(
             ["Is he cooking?", "Are they working?", "Is she feeling OK?", "Am I speaking too fast?",
              "Are they eating sushi? No, they aren't."], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the wh- questions.",
         "translation": "Ouça e repita as perguntas com question words.",
         "example": "\"What is she eating?\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula25-say-w{i}.m4a"} for i, t in enumerate(
             ["What is she eating?", "Why is he crying?", "How is she feeling?", "Where are you going?",
              "What are you doing?"], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOU.",
         "translation": "Agora responda às perguntas sobre VOCÊ com uma frase completa.",
         "example": "\"What are you doing?\" → \"I'm studying English.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula25-say-y{i}.m4a"} for i, t in enumerate(
             ["What are you doing?", "How are you feeling today?", "Are you wearing a uniform?",
              "What is your best friend doing now?"], 1)]},
    ],
}

AULA25_READING = {
    "title": "Reading — a text message chat",
    "lesson": 25,
    "subject": "Reading",
    "description": "Leia (e ouça) a conversa e responda às perguntas de acordo com o texto.",
    "topic": AULA25_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to Bia and her mother's messages.",
         "translation": "Leia e ouça as mensagens da Bia com a mãe dela. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula25-reading.m4a",
         "text": "MOM: Hi, Bia! What are you doing? Are you studying?\n"
                 "BIA: Hi, Mom! No, I'm not. I'm at the mall with Carol.\n"
                 "MOM: The mall? Why are you shopping on a Tuesday?\n"
                 "BIA: Because it's Carol's birthday on Friday! We're buying a present for her mother.\n"
                 "MOM: Oh, OK. Is Dad driving you home?\n"
                 "BIA: No, he isn't. He's working late. We're taking the bus.\n"
                 "MOM: And how are you feeling? Is your head OK now?\n"
                 "BIA: Yes, I'm feeling great, thanks! See you at dinner! ❤️"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "Who is Bia with? → [Carol.]",
         "text": "1. Is Bia studying? → [*No, she isn't.|Yes, she is.|No, she doesn't.]\n"
                 "2. Where is Bia? → [*At the mall.|At school.|At home.]\n"
                 "3. Why are they shopping? → [*Because it's Carol's birthday on Friday.|Because it's Tuesday.|Because they're bored.]\n"
                 "4. How are they going home? → [*By bus.|By car.|On foot.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Bia is feeling great. → True",
         "statements": [
             {"text": "Bia's father is working late.", "answer": True, "translation": "O pai da Bia está trabalhando até tarde."},
             {"text": "They are buying a present for Carol.", "answer": False,
              "translation": "Elas estão comprando um presente para a Carol."},
             {"text": "Today is Friday.", "answer": False, "translation": "Hoje é sexta-feira."},
         ]},
        {"type": "fill",
         "prompt": "Complete the questions from the text.",
         "translation": "Complete as perguntas do texto.",
         "example": "What [are] you doing?",
         "text": "1. [Are] you studying?\n2. Why [are] you shopping on a Tuesday?\n3. How [are] you feeling?"},
    ],
}

AULA25_WRITING = {
    "title": "Writing — questions",
    "lesson": 25,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Yes / no: AM / IS / ARE + sujeito + verbo-ING? · "
                   "WH-: question word + AM / IS / ARE + sujeito + verbo-ING?",
    "topic": AULA25_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Write the question for each answer.",
         "translation": "Escreva a pergunta para cada resposta.",
         "example": "She's eating sushi. → What is she eating?",
         "text": "1. Yes, they are. They're working. → [Are they working?]\n"
                 "2. I'm going to the supermarket. → [Where are you going?]\n"
                 "3. Because he's sad. → [Why is he crying?|Why is he sad?]"},
        {"type": "fill",
         "prompt": "Correct the mistake.",
         "translation": "Corrija o erro na ordem das palavras.",
         "example": "Why he is crying? → Why is he crying?",
         "text": "1. What you are doing? → [What are you doing?]\n2. She is sleeping? → [Is she sleeping?]\n"
                 "3. How she is feeling? → [How is she feeling?]"},
        {"type": "free",
         "prompt": "Write a short chat with a friend: 4 questions in the present continuous and the answers.",
         "translation": "Escreva uma conversa curta (mensagens) com um amigo: 4 perguntas no present continuous e as respostas.",
         "example": "A: What are you doing? — B: I'm cooking dinner.",
         "model_answer": "A: Hi! What are you doing?\nB: I'm cooking dinner.\n"
                         "A: Are you cooking pasta?\nB: No, I'm not. I'm making a chicken salad.\n"
                         "A: Is your sister helping you?\nB: No, she isn't. She's studying in her room.\n"
                         "A: How are you feeling?\nB: I'm tired, but happy!",
         "keywords": ["what are you", "are you", "is"], "min_words": 30, "points": 4},
    ],
}

AULA25_VIDEO = _video(25, AULA25_TOPIC, "Video — What are you doing?",
                      "uma repórter pergunta às pessoas na rua o que elas estão fazendo: Are you…? What are you…? Why…?",
                      "aula25-video", [
    _q("What are the women eating?", "O que as mulheres estão comendo?", "They're eating ice cream.",
       "They're eating sushi.", "They're eating pizza.", "They're drinking coffee."),
    _q("Is the man working today?", "O homem está trabalhando hoje?", "No, he isn't. He's running.", "Yes, he is.",
       "No, he doesn't.", "Yes, he does."),
    _q("Where are the friends going?", "Para onde os amigos estão indo?", "To the beach.", "To school.",
       "To work.", "To the hospital."),
    _q("Why is the boy sad?", "Por que o menino está triste?", "Because he's hungry.", "Because he's happy.",
       "Because he's playing.", "Because it's hot."),
    _q("Which question is correct?", "Qual pergunta está correta?", "What are you doing?", "What you are doing?",
       "What do you doing?", "What you doing?"),
])


# ---------- Aula 26 — Present Simple x Present Continuous (https://youtu.be/zo1KN_1U0Sk) ----------

AULA26_TOPIC = "Aula 26 — Present Simple x Present Continuous"

AULA26_CONTRAST = {
    "title": "Every day or now?",
    "lesson": 26,
    "description": "PRESENT SIMPLE → rotina, frequência, fatos: I go to the park on Sundays. · He takes a shower every day. · "
                   "She has a cat. (every day, on Mondays, twice a week, always, usually, never…)\n"
                   "PRESENT CONTINUOUS → o que está acontecendo AGORA: I'm watching TV now. · He's having a coffee now. "
                   "(now, right now, at the moment, today, look!)\n"
                   "They play basketball twice a week, but now they're playing tennis.\n"
                   "WHAT DOES HE DO? (profissão: o que ele faz) → He's a chef. He cooks very well.\n"
                   "WHAT IS HE DOING? (agora) → He's doing jiu-jitsu. He isn't cooking.",
    "topic": AULA26_TOPIC,
    "items": [
        {"type": "group",
         "prompt": "Present simple or present continuous? Put the time words in the right group.",
         "translation": "Present simple (rotina) ou present continuous (agora)? Coloque as expressões no grupo certo.",
         "example": "every day → present simple · now → present continuous",
         "categories": ["present simple", "present continuous"],
         "words": [
             {"text": "every day", "category": "present simple"}, {"text": "on Sundays", "category": "present simple"},
             {"text": "twice a week", "category": "present simple"}, {"text": "usually", "category": "present simple"},
             {"text": "now", "category": "present continuous"}, {"text": "right now", "category": "present continuous"},
             {"text": "at the moment", "category": "present continuous"}, {"text": "Look!", "category": "present continuous"},
         ]},
        {"type": "dropdown",
         "prompt": "Choose the right verb form.",
         "translation": "Escolha a forma certa do verbo.",
         "example": "I [go] to the park on Sundays. · I ['m watching] TV now.",
         "text": "1. He [*takes|is taking] a shower every day.\n"
                 "2. Look! He [*is having|has] a coffee now.\n"
                 "3. They [*play|are playing] basketball twice a week.\n"
                 "4. Shh! The baby [*is sleeping|sleeps] right now.\n"
                 "5. I usually [*wake up|am waking up] at 6 a.m.\n"
                 "6. We [*are studying|study] English at the moment."},
        {"type": "match",
         "prompt": "Match the questions to the answers.",
         "translation": "Ligue as perguntas às respostas.",
         "example": "What does he do? → He's a chef.",
         "pairs": [
             {"left": "What does she do?", "right": "She's a singer."},
             {"left": "What is she doing?", "right": "She's driving."},
             {"left": "How often do you go to the gym?", "right": "Three times a week."},
             {"left": "Are you working now?", "right": "No, I'm not. I'm at home."},
             {"left": "Do you work on Saturdays?", "right": "No, I don't."},
         ]},
        {"type": "truefalse",
         "prompt": "True or false? Think about the lesson.",
         "translation": "Verdadeiro ou falso? Pense no que foi explicado na aula.",
         "example": "We use the present simple for routines. → True",
         "statements": [
             {"text": "\"What does he do?\" asks about his job.", "answer": True,
              "translation": "\"What does he do?\" pergunta sobre a profissão dele."},
             {"text": "\"What is he doing?\" asks about his routine.", "answer": False,
              "translation": "\"What is he doing?\" pergunta sobre a rotina dele."},
             {"text": "In the present continuous, we don't use do / does.", "answer": True,
              "translation": "No present continuous, não usamos do / does."},
             {"text": "\"She is have a cat\" is correct.", "answer": False, "translation": "\"She is have a cat\" está correto."},
         ]},
    ],
}

AULA26_FORMS = {
    "title": "Negatives and questions: do / does or am / is / are?",
    "lesson": 26,
    "description": "PRESENT SIMPLE usa DO / DOES / DON'T / DOESN'T:\n"
                   "She has a cat. → She doesn't have a cat. → Does she have a cat? → Yes, she does. / No, she doesn't.\n"
                   "PRESENT CONTINUOUS usa só o verb to be (AM / IS / ARE), sem do / does:\n"
                   "She is reading a book. → She isn't reading a book. → Is she reading a book? → Yes, she is. / No, she isn't.",
    "topic": AULA26_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Do / does or am / is / are?",
         "translation": "Do / does (present simple) ou am / is / are (present continuous)?",
         "example": "[Does] she have a cat? · [Is] she reading?",
         "text": "1. [*Is|Does] she reading a book?\n2. [*Does|Is] she have a cat?\n3. [*Are|Do] they playing tennis now?\n"
                 "4. [*Do|Are] they play basketball on Fridays?\n5. What [*does|is] your father do?\n6. What [*is|does] your father doing?"},
        {"type": "dropdown",
         "prompt": "Choose the right negative.",
         "translation": "Escolha a negativa certa.",
         "example": "She [doesn't] have a cat. · She [isn't] reading.",
         "text": "1. He [*doesn't|isn't] cook on weekends.\n2. He [*isn't|doesn't] cooking now.\n"
                 "3. I [*don't|'m not] watch TV in the morning.\n4. I [*'m not|don't] watching TV now."},
        {"type": "fill",
         "prompt": "Write the negative and the question.",
         "translation": "Escreva a negativa e a pergunta.",
         "example": "She is reading. → She isn't reading. / Is she reading?",
         "text": "1. He plays tennis. → negative: [He doesn't play tennis.] · question: [Does he play tennis?]\n"
                 "2. He is playing tennis. → negative: [He isn't playing tennis.|He's not playing tennis.] · question: [Is he playing tennis?]"},
        {"type": "fill",
         "prompt": "Translate.",
         "translation": "Traduza.",
         "example": "Eu vou ao parque aos domingos. → I go to the park on Sundays.",
         "text": "1. Ele toma banho todo dia. → [He takes a shower every day.|He has a shower every day.]\n"
                 "2. Agora ele está tomando café. → [Now he's having a coffee.|Now he is having a coffee.|He's having a coffee now.|He is having a coffee now.|Now he's having coffee.|He's having coffee now.]\n"
                 "3. O que você faz? → [What do you do?]\n"
                 "4. O que você está fazendo? → [What are you doing?]"},
    ],
}

AULA26_LISTENING = {
    "title": "Listening — every day or now?",
    "lesson": 26,
    "subject": "Listening",
    "description": "Aperte o ▶ para ouvir. Você pode ouvir quantas vezes quiser. Use fones de ouvido se puder! 🎧",
    "topic": AULA26_TOPIC,
    "items": [
        {"type": "dropdown",
         "prompt": "Routine or now? Listen and choose.",
         "translation": "Rotina ou agora? Ouça e escolha.",
         "example": "Você ouve: \"I'm studying.\" → now",
         "audio": f"{AUDIO}/aula26-routine.m4a",
         "text": "1. [*routine|now]\n2. [*now|routine]\n3. [*now|routine]\n4. [*routine|now]\n5. [*routine|now]"},
        {"type": "fill",
         "prompt": "Dictation: listen and complete.",
         "translation": "Ditado: ouça e complete com o verbo.",
         "example": "Você ouve: \"She works in a bank.\" → She [works] in a bank.",
         "audio": f"{AUDIO}/aula26-dictation.m4a",
         "text": "1. He [cooks] very well, but now he's [sleeping].\n"
                 "2. They [play] soccer on Saturdays. Today they're [playing] tennis.\n"
                 "3. What [does] she do? What [is] she doing?"},
        {"type": "info",
         "prompt": "Now listen to an interview with Chef Lucas.",
         "translation": "Agora ouça uma entrevista com o chef Lucas, que está de folga hoje. Depois responda às perguntas abaixo.",
         "audio": f"{AUDIO}/aula26-chef.m4a",
         "text": "🎧 Ouça o áudio quantas vezes precisar. Depois responda às perguntas abaixo."},
        {"type": "dropdown",
         "prompt": "Listen again and choose.",
         "translation": "Ouça de novo e escolha.",
         "example": "Lucas is a [chef].",
         "text": "1. What time does Lucas usually start work? → [*At 10 a.m.|At 7 a.m.|At noon.]\n"
                 "2. What is he doing today? → [*He's doing jiu-jitsu.|He's cooking.|He's sleeping.]\n"
                 "3. How often does he do jiu-jitsu? → [*Twice a week.|Every day.|Once a month.]\n"
                 "4. Who is cooking at the restaurant today? → [*His sister.|His father.|Nobody.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the interview.",
         "translation": "Verdadeiro ou falso? Responda de acordo com a entrevista.",
         "example": "Lucas works in a restaurant. → True",
         "statements": [
             {"text": "Lucas is working today.", "answer": False, "translation": "O Lucas está trabalhando hoje."},
             {"text": "Lucas usually works on Mondays.", "answer": False, "translation": "O Lucas normalmente trabalha às segundas."},
             {"text": "Lucas loves Italian food.", "answer": True, "translation": "O Lucas ama comida italiana."},
         ]},
    ],
}

AULA26_SPEAKING = {
    "title": "Speaking — routine and now",
    "lesson": 26,
    "subject": "Speaking",
    "description": "Hora de falar! 🎙 Ouça o modelo, grave a sua voz imitando e depois ouça a sua gravação para comparar.\n"
                   "Dica: WHAT DOES HE DO? = \"uót dâz hi dú\" · WHAT IS HE DOING? = \"uóts hi dúin\".",
    "topic": AULA26_TOPIC,
    "items": [
        {"type": "speak",
         "prompt": "Listen and repeat the pairs.",
         "translation": "Ouça e repita os pares (rotina × agora).",
         "example": "Clique em 🔊 Ouvir → depois em 🎙 Gravar → fale → ⏹ Parar → ouça a sua voz e compare.",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula26-say-s{i}.m4a"} for i, t in enumerate(
             ["I go to the park on Sundays. I'm watching TV now.",
              "They play basketball twice a week, but now they're playing tennis.",
              "He takes a shower every day. He's having a coffee now.",
              "What does he do? He's a chef.", "What is he doing? He's doing jiu-jitsu."], 1)]},
        {"type": "speak",
         "prompt": "Listen and repeat the questions and answers.",
         "translation": "Ouça e repita as perguntas e as respostas.",
         "example": "\"Does she have a cat? Yes, she does.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula26-say-q{i}.m4a"} for i, t in enumerate(
             ["Does she have a cat? Yes, she does.", "Is she reading a book? No, she isn't.",
              "How often do you watch TV?", "What are you doing right now?"], 1)]},
        {"type": "speak",
         "prompt": "Now answer the questions about YOU.",
         "translation": "Agora responda às perguntas sobre VOCÊ com uma frase completa.",
         "example": "\"What do you do?\" → \"I'm a nurse.\" · \"What are you doing?\" → \"I'm studying English.\"",
         "phrases": [{"text": t, "audio": f"{AUDIO}/aula26-say-y{i}.m4a"} for i, t in enumerate(
             ["What do you do?", "What are you doing now?", "What do you usually do on Saturdays?",
              "What is your family doing now?"], 1)]},
    ],
}

AULA26_READING = {
    "title": "Reading — a nurse on vacation",
    "lesson": 26,
    "subject": "Reading",
    "description": "Leia (e ouça) o texto e responda às perguntas de acordo com o texto.",
    "topic": AULA26_TOPIC,
    "items": [
        {"type": "info",
         "prompt": "Read and listen to the text about Helena.",
         "translation": "Leia e ouça o texto sobre a Helena. As perguntas abaixo são sobre este texto.",
         "audio": f"{AUDIO}/aula26-reading.m4a",
         "text": "A NURSE ON VACATION\n\n"
                 "Helena is a nurse. She works at a big hospital in São Paulo.\n"
                 "She usually wakes up at 5 a.m., and she takes the subway to work. She works twelve hours a day, and she "
                 "hardly ever has lunch at home.\n"
                 "But this week is different: Helena is on vacation!\n"
                 "Right now, she isn't working. She's sitting on the beach in Bahia, and she's reading a book.\n"
                 "Her husband is swimming in the sea, and her children are playing volleyball.\n"
                 "Helena doesn't usually have time to relax, so she's very happy today!"},
        {"type": "dropdown",
         "prompt": "Choose the right answer according to the text.",
         "translation": "Escolha a resposta certa de acordo com o texto.",
         "example": "What does Helena do? → [She's a nurse.]",
         "text": "1. What time does Helena usually wake up? → [*At 5 a.m.|At 7 a.m.|At noon.]\n"
                 "2. How does she usually go to work? → [*By subway.|By car.|By bike.]\n"
                 "3. What is she doing right now? → [*She's reading on the beach.|She's working.|She's swimming.]\n"
                 "4. What are her children doing? → [*They're playing volleyball.|They're sleeping.|They're reading.]"},
        {"type": "truefalse",
         "prompt": "True or false? Answer according to the text.",
         "translation": "Verdadeiro ou falso? Responda de acordo com o texto.",
         "example": "Helena is on vacation. → True",
         "statements": [
             {"text": "Helena usually has lunch at home.", "answer": False,
              "translation": "A Helena normalmente almoça em casa."},
             {"text": "Helena's husband is swimming now.", "answer": True, "translation": "O marido da Helena está nadando agora."},
             {"text": "Helena is working in Bahia.", "answer": False, "translation": "A Helena está trabalhando na Bahia."},
         ]},
        {"type": "fill",
         "prompt": "Complete with the verb from the text.",
         "translation": "Complete com o verbo do texto (rotina ou agora?).",
         "example": "Helena [works] at a big hospital.",
         "text": "1. She usually [wakes] up at 5 a.m.\n2. Right now, she [is] sitting on the beach.\n"
                 "3. Her husband [is swimming] in the sea."},
    ],
}

AULA26_WRITING = {
    "title": "Writing — usually… but today…",
    "lesson": 26,
    "subject": "Writing",
    "description": "Hora de escrever! ✍️ Rotina → present simple (I usually work…) · Agora / hoje → present continuous (Today I'm…).",
    "topic": AULA26_TOPIC,
    "items": [
        {"type": "fill",
         "prompt": "Complete with the present simple or the present continuous.",
         "translation": "Complete com o present simple ou o present continuous do verbo entre parênteses.",
         "example": "I (work) every day, but today I (rest). → I work every day, but today I'm resting.",
         "text": "1. She usually [drinks] coffee in the morning, but today she [is drinking|'s drinking] tea. (drink)\n"
                 "2. We [play] soccer on Saturdays. Look! We [are playing|'re playing] now! (play)\n"
                 "3. My father [doesn't] work on Sundays. (not work)"},
        {"type": "fill",
         "prompt": "Write the questions.",
         "translation": "Escreva as perguntas em inglês.",
         "example": "Ela tem um gato? → Does she have a cat?",
         "text": "1. O que ele faz? (profissão) → [What does he do?]\n2. O que ele está fazendo? → [What is he doing?]\n"
                 "3. Você assiste TV todo dia? → [Do you watch TV every day?]"},
        {"type": "free",
         "prompt": "Write about your routine (what you usually do on weekdays) and what you are doing today / right now.",
         "translation": "Escreva sobre a sua rotina (o que você normalmente faz nos dias de semana) e o que você está fazendo hoje / agora.",
         "example": "I usually work from 9 to 6. Today I'm not working: I'm at home.",
         "model_answer": "I usually wake up at 6:30 and go to work by bus. I work in an office from 9 to 6, and I have lunch "
                         "with my colleagues.\n"
                         "But today is Saturday, and I'm not working. Right now, I'm sitting on the sofa and I'm "
                         "studying English. My husband is cooking lunch, and my son is playing video games.",
         "keywords": ["usually", "I'm", "now", "today"], "min_words": 40, "points": 4},
    ],
}

AULA26_VIDEO = _video(26, AULA26_TOPIC, "Video — What does she do? What is she doing?",
                      "a diferença entre a profissão / rotina de cada pessoa e o que ela está fazendo agora.",
                      "aula26-video", [
    _q("What does Laura do?", "O que a Laura faz (profissão)?", "She's a doctor.", "She's a chef.", "She's a pilot.",
       "She's a teacher."),
    _q("What is Laura doing now?", "O que a Laura está fazendo agora?", "She's running in the park.",
       "She's working at the hospital.", "She's sleeping.", "She's cooking."),
    _q("What does Diego do?", "O que o Diego faz?", "He's a chef.", "He's a doctor.", "He's a student.",
       "He's a driver."),
    _q("Is Diego cooking right now?", "O Diego está cozinhando agora?", "No, he isn't. He's playing the guitar.",
       "Yes, he is.", "No, he doesn't.", "Yes, he does."),
    _q("How often does Diego play the guitar?", "Com que frequência o Diego toca violão?", "Every Sunday.",
       "Every day.", "Never.", "Twice a year."),
])


SPECS = (AULA1_SOUNDS, AULA1_SPELLING, AULA1_LISTENING, AULA1_SPEAKING, AULA1_READING, AULA1_WRITING, AULA1_VIDEO,
         AULA2_QUESTIONS, AULA2_ONLINE, AULA2_LISTENING, AULA2_SPEAKING, AULA2_READING, AULA2_WRITING, AULA2_VIDEO,
         AULA3_HELLO, AULA3_TIMES, AULA3_LISTENING, AULA3_SPEAKING, AULA3_READING, AULA3_WRITING, AULA3_VIDEO,
         AULA4_VERBS, AULA4_SEQUENCE, AULA4_LISTENING, AULA4_SPEAKING, AULA4_READING, AULA4_WRITING, AULA4_VIDEO,
         AULA5_NUMBERS, AULA5_PHONE_AGE_TIME, AULA5_LISTENING, AULA5_SPEAKING, AULA5_READING, AULA5_WRITING, AULA5_VIDEO,
         AULA6_DAYS, AULA6_MONTHS, AULA6_LISTENING, AULA6_SPEAKING, AULA6_READING, AULA6_WRITING, AULA6_VIDEO,
         AULA7_PRONOUNS, AULA7_REPLACE, AULA7_LISTENING, AULA7_SPEAKING, AULA7_READING, AULA7_WRITING, AULA7_VIDEO,
         AULA8_RULES, AULA8_SENTENCES, AULA8_LISTENING, AULA8_SPEAKING, AULA8_READING, AULA8_WRITING, AULA8_VIDEO,
         AULA9_JOBS, AULA9_WHAT_DO_YOU_DO, AULA9_LISTENING, AULA9_SPEAKING, AULA9_READING, AULA9_WRITING, AULA9_VIDEO,
         AULA10_VOCAB, AULA10_NEGATIVE, AULA10_LISTENING, AULA10_SPEAKING, AULA10_READING, AULA10_WRITING, AULA10_VIDEO,
         AULA11_DO_DOES, AULA11_SHORT_ANSWERS, AULA11_LISTENING, AULA11_SPEAKING, AULA11_READING, AULA11_WRITING, AULA11_VIDEO,
         AULA12_WORDS, AULA12_ORDER, AULA12_LISTENING, AULA12_SPEAKING, AULA12_READING, AULA12_WRITING, AULA12_VIDEO,
         AULA13_WORDS, AULA13_QUESTIONS, AULA13_LISTENING, AULA13_SPEAKING, AULA13_READING, AULA13_WRITING, AULA13_VIDEO,
         AULA14_WORDS, AULA14_PHRASES, AULA14_LISTENING, AULA14_SPEAKING, AULA14_READING, AULA14_WRITING, AULA14_VIDEO,
         AULA15_WORDS, AULA15_TOBE, AULA15_LISTENING, AULA15_SPEAKING, AULA15_READING, AULA15_WRITING, AULA15_VIDEO,
         AULA16_WORDS, AULA16_SENTENCES, AULA16_LISTENING, AULA16_SPEAKING, AULA16_READING, AULA16_WRITING, AULA16_VIDEO,
         AULA17_WORDS, AULA17_HAIR, AULA17_LISTENING, AULA17_SPEAKING, AULA17_READING, AULA17_WRITING, AULA17_VIDEO,
         AULA18_WORDS, AULA18_EXTENDED, AULA18_LISTENING, AULA18_SPEAKING, AULA18_READING, AULA18_WRITING, AULA18_VIDEO,
         AULA19_WORDS, AULA19_PLURALS, AULA19_LISTENING, AULA19_SPEAKING, AULA19_READING, AULA19_WRITING, AULA19_VIDEO,
         AULA20_WORDS, AULA20_FURNITURE, AULA20_LISTENING, AULA20_SPEAKING, AULA20_READING, AULA20_WRITING, AULA20_VIDEO,
         AULA21_THERE, AULA21_QUESTIONS, AULA21_LISTENING, AULA21_SPEAKING, AULA21_READING, AULA21_WRITING, AULA21_VIDEO,
         AULA22_WORDS, AULA22_WHERE, AULA22_LISTENING, AULA22_SPEAKING, AULA22_READING, AULA22_WRITING, AULA22_VIDEO,
         AULA23_ING, AULA23_SENTENCES, AULA23_LISTENING, AULA23_SPEAKING, AULA23_READING, AULA23_WRITING, AULA23_VIDEO,
         AULA24_FORMS, AULA24_PICTURES, AULA24_LISTENING, AULA24_SPEAKING, AULA24_READING, AULA24_WRITING, AULA24_VIDEO,
         AULA25_YESNO, AULA25_WH, AULA25_LISTENING, AULA25_SPEAKING, AULA25_READING, AULA25_WRITING, AULA25_VIDEO,
         AULA26_CONTRAST, AULA26_FORMS, AULA26_LISTENING, AULA26_SPEAKING, AULA26_READING, AULA26_WRITING, AULA26_VIDEO)


def main():
    publish(SLUG, "A1", SPECS)


if __name__ == "__main__":
    main()
