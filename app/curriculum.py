"""Public course catalogue: the tabs and lesson menus shown on /curso/<slug>.

Exercises join a lesson through exercises.public_slug (the course) + exercises.public_lesson (the lesson number).
Courses listed here share one tab bar; any other slug is shown as a simple stand-alone page.
"""

COURSES = {
    "basico-1": {"title": "Básico 1", "lessons": [
        "Alphabet",
        "Classroom Language",
        "Greetings",
        "Daily Routine",
        "Numbers",
        "Days of the Week, Seasons, Months",
        "Subject Pronouns",
        "Present Simple (affirmative)",
        "Jobs",
        "Present Simple (negative)",
        "Present Simple (interrogative 1)",
        "Present Simple (interrogative 2)",
        "Sports",
        "How often… (Frequency)",
        "Verb To Be (Countries and Nationalities)",
        "Verb To Be (Feelings)",
        "Verb To Be (Physical Appearance)",
        "Verb To Be (Family Members)",
        "A, An, Plurals",
        "Parts of the House",
        "There is / There are",
        "Prepositions of Place",
        "Present Continuous (affirmative)",
        "Present Continuous (negative)",
        "Present Continuous (interrogative)",
        "Present Simple x Present Continuous",
    ]},
    "basico-2": {"title": "Básico 2", "lessons": [
        "Can & Can't",
        "Was & Were",
        "Prepositions of Place",
        "Past Simple (regular & irregular)",
        "-ED Pronunciation",
        "Past Simple (negative)",
        "Past Simple (interrogative)",
        "Past Continuous",
        "Past Simple vs Past Continuous",
        "Prepositions: IN, ON, AT",
        "Saying the Dates",
        "Food & Drink",
        "Countable & Uncountable Nouns",
        "Countable & Uncountable Nouns (a, an, some, any)",
        "Countable & Uncountable Nouns (Containers)",
        "Comparatives",
        "Superlatives",
        "Directions",
        "A, An, The",
        "Adverbs of Manner",
    ]},
    "basico-3": {"title": "Básico 3", "lessons": [
        "Past Simple (regular & irregular)",
        "-ED Pronunciation",
        "Past Simple (negative)",
        "Past Simple (interrogative)",
        "Possessive 's",
        "Possessive Adjectives & Possessive Pronouns",
        "Object Pronouns",
        "Be Going To for Plans",
        "Be Going To for Predictions",
        "Will for Predictions",
        "Will for Offers, Promises and Decisions",
        "Will vs Be Going To",
        "Present Continuous for Future Arrangements",
        "-ED or -ING Adjectives",
        "Parts of the Body",
        "Can & Could",
        "Be Able To",
        "May & Might",
        "Should & Shouldn't",
        "Health Problems",
        "Must & Mustn't",
        "Phone Etiquette",
        "Have To & Don't Have To",
        "Bucket List",
        "Would Like To & Want",
    ]},
}


def lesson_label(n, title):
    return f"Aula {n:02d} — {title}"


def lessons(slug):
    """[(number, title), ...] for a catalogue course, else []."""
    course = COURSES.get(slug)
    return list(enumerate(course["lessons"], 1)) if course else []


def lesson_title(slug, n):
    ls = dict(lessons(slug))
    return lesson_label(n, ls[n]) if n in ls else None
