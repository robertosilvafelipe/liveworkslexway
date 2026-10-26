"""Text-to-speech for the lesson audios and videos: ElevenLabs (natural voices) or macOS `say` (drafts).

speak(voice, text, wav_path) writes a mono 16-bit wav. `voice` is a role from VOICES (F, M, F2, M2, ...).
ElevenLabs results are cached by (voice, text, settings), so rebuilding never spends credits twice.
The API key is read from ~/.elevenlabs_key and is never printed.
"""
import hashlib, json, os, re, shutil, subprocess, tempfile, time, urllib.error, urllib.request, wave

import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
CACHE = os.environ.get("TTS_CACHE", os.path.expanduser("~/.cache/lexway-tts"))
MODEL = "eleven_multilingual_v2"
ENGLISH_MODEL = "eleven_turbo_v2"  # English-only; the only kind that honours <phoneme> tags (used for spelled letters)

# American pronunciation of each letter name (CMU Arpabet), so spelled letters are never read in another language
ARPABET = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [
    "EY1", "B IY1", "S IY1", "D IY1", "IY1", "EH1 F", "JH IY1", "EY1 CH", "AY1", "JH EY1", "K EY1", "EH1 L", "EH1 M", "EH1 N",
    "OW1", "P IY1", "K Y UW1", "AA1 R", "EH1 S", "T IY1", "Y UW1", "V IY1", "D AH1 B AH0 L Y UW0", "EH1 K S", "W AY1", "Z IY1"]))


def letter(ch):
    """Spoken letter name with an exact pronunciation tag, e.g. letter("A") -> <phoneme …>A</phoneme>."""
    ch = ch.upper()
    return f'<phoneme alphabet="cmu-arpabet" ph="{ARPABET[ch]}">{ch}</phoneme>'
SETTINGS = {"stability": 0.75, "similarity_boost": 0.8, "style": 0.0, "use_speaker_boost": True, "speed": 0.9}

# role -> (ElevenLabs voice id, macOS fallback voice); filled with American voices from the account's library
VOICES = {
    # two official voices (user's choice): one female, one male, the same in every audio and video
    "F": ("cgSgspJ2msm6clMCkdW9", "Samantha"),   # Jessica — American, young and bright
    "M": ("cjVigY5qzO86Huf0OWal", "Fred"),       # Eric — American, smooth and clear
    "F2": ("cgSgspJ2msm6clMCkdW9", "Samantha"),  # = F
    "M2": ("cjVigY5qzO86Huf0OWal", "Fred"),      # = M
    # voices the user picked for specific audios (Aula 01 listening), from the ElevenLabs voice library
    "SARAH": ("Nhs7eitvQWFTQBsf0yiT", "Samantha"),  # Sarah - Approachable and Informative (female)
    "MAX": ("Gfpl8Yo74Is0W6cPUWWT", "Fred"),        # Max - Elearning and Documentary (male)
    "JERRY": ("tCgAUbeV0tdD1S2yFoCx", "Fred"),      # Jerry B. - Instructional & Tutorial (male)
}


def _key():
    with open(os.path.expanduser("~/.elevenlabs_key")) as f:
        return f.read().strip()


def _to_wav(src, dst, rate):
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", src, "-ac", "1", "-ar", str(rate), "-sample_fmt", "s16", dst],
                   check=True)
    return dst


def _plain(text):
    """Drop the macOS-only [[...]] commands; ElevenLabs reads plain text."""
    return re.sub(r"\s+", " ", re.sub(r"\[\[[^\]]*\]\]", " ", text)).strip()


def eleven(voice_id, text, mp3_path, settings=None):
    os.makedirs(CACHE, exist_ok=True)
    body = {"text": text, "model_id": ENGLISH_MODEL if "<phoneme" in text else MODEL, "voice_settings": settings or SETTINGS}
    digest = hashlib.sha256(json.dumps([voice_id, body], sort_keys=True).encode()).hexdigest()[:24]
    cached = os.path.join(CACHE, digest + ".mp3")
    if not os.path.exists(cached):
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128",
            data=json.dumps(body).encode(), method="POST",
            headers={"xi-api-key": _key(), "Content-Type": "application/json", "Accept": "audio/mpeg"})
        for attempt in range(4):  # network blips / rate limits: wait and try again; other errors (quota, key) stop
            try:
                with urllib.request.urlopen(req, timeout=120) as r, open(cached + ".part", "wb") as f:
                    shutil.copyfileobj(r, f)
                break
            except urllib.error.HTTPError as e:
                if e.code not in (429, 500, 502, 503, 504) or attempt == 3:
                    raise RuntimeError(f"ElevenLabs HTTP {e.code}: {e.read()[:300].decode(errors='replace')}") from None
            except (TimeoutError, OSError):
                if attempt == 3:
                    raise
            time.sleep(5 * (attempt + 1))
        os.replace(cached + ".part", cached)
    shutil.copy(cached, mp3_path)
    return mp3_path


def speak(voice, text, wav_path, rate=44100, use_say=False, speed=None):
    vid, mac = VOICES[voice]
    if use_say or not vid:
        aiff = tempfile.mktemp(suffix=".aiff")
        subprocess.run(["say", "-v", mac, "-r", "160", "-o", aiff, text], check=True)
        return _to_wav(aiff, wav_path, rate)
    settings = dict(SETTINGS, speed=round(speed, 2)) if speed else None
    text = _plain(text)
    if "<phoneme" in text and "<break" in text:
        # spelling: the English-only model skips or slurs letters around pauses inside one request,
        # so every letter (or phrase) between pauses is its own request and the silence is added here
        pcm = b""
        for k, chunk in enumerate(re.split(r'<break time="([\d.]+)s" />', text)):
            if k % 2:
                pcm += b"\0\0" * int(rate * float(chunk))
                continue
            chunk = chunk.strip(" ,")
            if not re.sub(r"<[^>]+>|[\s.,!?]", "", chunk):
                continue
            if chunk.endswith("</phoneme>"):
                chunk += "."
            part = f"{wav_path}.{k}.wav"
            _to_wav(eleven(vid, chunk, part + ".mp3", settings), part, rate)
            with wave.open(part) as w:
                pcm += w.readframes(w.getnframes())
            os.remove(part)
        with wave.open(wav_path, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm)
        return wav_path
    mp3 = eleven(vid, text, wav_path + ".mp3", settings)
    return _to_wav(mp3, wav_path, rate)
