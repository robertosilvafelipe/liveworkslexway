"""Build interactive-video lessons (mp4 + English subtitles + pause times) on a Mac.

Usage: python deploy/make_video.py <name> [--say]
  Needs Pillow-free tooling only: headless Google Chrome (renders each scene from HTML) and imageio-ffmpeg (bundled ffmpeg).
  Voices come from ElevenLabs (key in ~/.elevenlabs_key); --say uses the macOS voice instead (quick drafts).
Output in app/static/video/basico-1/: <name>.mp4, <name>.vtt and <name>.json ({"stops": [seconds, ...]}),
which the seed reads to place each question exactly where its scene ends.
"""
import html, json, os, subprocess, sys, tempfile, wave

import imageio_ffmpeg

sys.path.insert(0, os.path.dirname(__file__))
import tts  # noqa: E402

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "app", "static", "video", "basico-1")
W, H, FPS, RATE = 1280, 720, 25, 44100
GAP, STOP_PAD = 0.45, 1.2  # silence between lines; silence after a scene that ends with a question

PAGE = """<!doctype html><meta charset=utf-8><style>
body{margin:0;width:%(w)dpx;height:%(h)dpx;overflow:hidden;font-family:-apple-system,'Helvetica Neue',sans-serif;
 background:%(bg)s;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative}
.place{position:absolute;font-size:340px;opacity:.16;right:70px;bottom:20px}
.place2{position:absolute;font-size:150px;opacity:.22;left:70px;top:60px}
.who{font-size:230px;line-height:1;filter:drop-shadow(0 14px 18px rgba(0,0,0,.25))}
.name{margin-top:22px;background:#fff;color:#123;padding:12px 34px;border-radius:999px;font-size:44px;font-weight:700;
 box-shadow:0 6px 16px rgba(0,0,0,.18)}
.sub{margin-top:14px;color:#fff;font-size:30px;font-weight:600;text-shadow:0 2px 6px rgba(0,0,0,.35)}
.title{color:#fff;font-size:86px;font-weight:800;text-align:center;text-shadow:0 4px 14px rgba(0,0,0,.3);line-height:1.15}
.tag{position:absolute;left:40px;bottom:30px;color:rgba(255,255,255,.85);font-size:24px;font-weight:600;letter-spacing:.06em}
.wave{position:absolute;top:40px;right:48px;font-size:46px}
</style>%(body)s<div class=tag>LexWay · %(tag)s</div>"""


def scene_html(scene, tag):
    if scene.get("title"):
        body = (f'<div class=place2>{scene.get("icon", "")}</div><div class=title>{html.escape(scene["title"])}</div>'
                + (f'<div class=sub>{html.escape(scene["subtitle"])}</div>' if scene.get("subtitle") else ""))
    else:
        body = (f'<div class=place>{scene.get("place", "")}</div><div class=wave>🔊</div>'
                f'<div class=who>{scene["who"]}</div><div class=name>{html.escape(scene["name"])}</div>'
                + (f'<div class=sub>{html.escape(scene["caption"])}</div>' if scene.get("caption") else ""))
    return PAGE % {"w": W, "h": H, "bg": scene.get("bg", "linear-gradient(135deg,#0b6e6e,#3aa79b)"), "body": body, "tag": tag}


OVERLAY = """<!doctype html><meta charset=utf-8><style>
html,body{margin:0;width:%(w)dpx;height:%(h)dpx;background:transparent;font-family:-apple-system,'Helvetica Neue',sans-serif}
.name{position:absolute;left:40px;bottom:78px;background:rgba(255,255,255,.94);color:#123;padding:10px 30px;border-radius:999px;
 font-size:40px;font-weight:700;box-shadow:0 6px 16px rgba(0,0,0,.25)}
.tag{position:absolute;left:40px;bottom:28px;color:#fff;font-size:22px;font-weight:600;letter-spacing:.05em;text-shadow:0 1px 6px rgba(0,0,0,.7)}
</style>%(name)s<div class=tag>LexWay · %(tag)s</div>"""
CLIPS = os.environ.get("VIDEO_CLIPS", os.path.join(os.path.dirname(__file__), "..", "..", "pix", "clips"))


def overlay(scene, tag, path, tmp):
    """Transparent PNG with the person's name and the course tag, laid over real footage."""
    page = os.path.join(tmp, os.path.basename(path) + ".html")
    name = f'<div class=name>{html.escape(scene["name"])}</div>' if scene.get("name") else ""
    open(page, "w").write(OVERLAY % {"w": W, "h": H, "name": name, "tag": tag})
    subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=1", "--default-background-color=00000000",
                    f"--window-size={W},{H}", f"--screenshot={path}", "file://" + page], check=True, capture_output=True)


def footage(scene, dur, tmp, k, tag):
    """Real footage (Pixabay clips, free for commercial use): the scene time is split between its clips."""
    ov = os.path.join(tmp, f"ov{k:02d}.png")
    overlay(scene, tag, ov, tmp)
    seg, parts = dur / len(scene["clips"]), []
    for j, (clip, start) in enumerate(scene["clips"]):
        part = os.path.join(tmp, f"p{k:02d}{j}.mp4")
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", str(start), "-i", os.path.join(CLIPS, f"{clip}.mp4"), "-i", ov,
                        "-filter_complex", f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1,"
                        f"tpad=stop_mode=clone:stop_duration=60[v];[v][1:v]overlay=0:0,format=yuv420p",
                        "-t", f"{seg:.3f}", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-r", str(FPS), part], check=True)
        parts.append(part)
    return parts


def shot(scene, tag, path, tmp):
    page = os.path.join(tmp, os.path.basename(path) + ".html")
    open(page, "w").write(scene_html(scene, tag))
    subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={W},{H}", f"--screenshot={path}", "file://" + page],
                   check=True, capture_output=True)


def silence(sec):
    return b"\x00\x00" * int(sec * RATE)


def wav_frames(path):
    with wave.open(path) as w:
        assert w.getframerate() == RATE and w.getnchannels() == 1 and w.getsampwidth() == 2, path
        return w.readframes(w.getnframes())


def vtt_time(t):
    return f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{t % 60:06.3f}"


def build(name, video, use_say=False):
    global OUT_DIR
    pre = {"b2-": "basico-2", "b3-": "basico-3"}.get(name[:3])  # b2- / b3- = Básico 2 / 3 (own folders)
    course, fname = (pre, name[3:]) if pre else ("basico-1", name)
    OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "app", "static", "video", course)
    os.makedirs(OUT_DIR, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="vid-")
    pcm, cues, stops, segments, t = b"", [], [], [], 0.0
    for i, sc in enumerate(video["scenes"]):
        img = os.path.join(tmp, f"s{i:02d}.png")
        if not sc.get("clips"):
            shot(sc, video["tag"], img, tmp)
        start = t
        audio = silence(sc.get("lead", 0.6))
        t += sc.get("lead", 0.6)
        for j, (voice, text, *spoken) in enumerate(sc.get("lines", [])):
            # optional 3rd item = what the voice reads (e.g. spelled letters "kay ay tee ee"); the subtitle keeps "K, A, T, E"
            wav = tts.speak(voice, spoken[0] if spoken else text, os.path.join(tmp, f"s{i:02d}l{j}.wav"), rate=RATE, use_say=use_say)
            frames = wav_frames(wav)
            dur = len(frames) / 2 / RATE
            cues.append((t, t + dur, text))
            audio += frames + silence(GAP)
            t += dur + GAP
        if sc.get("hold"):
            audio += silence(sc["hold"])
            t += sc["hold"]
        if sc.get("stop"):
            stops.append(round(t + 0.15, 2))
            audio += silence(STOP_PAD)
            t += STOP_PAD
        pcm += audio
        segments.append((sc, img, t - start))
        if i == 0 and not sc.get("clips"):  # poster shown before the student presses play
            subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", img, "-q:v", "4", os.path.join(OUT_DIR, fname + ".jpg")], check=True)

    wav_path = os.path.join(tmp, "track.wav")
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE); w.writeframes(pcm)

    # each scene: a still image with a slow zoom, then all scenes joined and muxed with the narration
    parts = []
    for k, (sc, img, dur) in enumerate(segments):
        if sc.get("clips"):
            parts += footage(sc, dur, tmp, k, video["tag"])
            continue
        n = max(1, round(dur * FPS))
        part = os.path.join(tmp, f"p{k:02d}.mp4")
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-loop", "1", "-i", img, "-frames:v", str(n), "-vf",
                        f"scale={W * 2}:{H * 2},zoompan=z='1+0.04*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                        f":d=1:s={W}x{H}:fps={FPS},format=yuv420p", "-r", str(FPS), "-c:v", "libx264", "-preset", "medium",
                        "-crf", "23", part], check=True)
        parts.append(part)
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    out = os.path.join(OUT_DIR, fname + ".mp4")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav_path,
                    "-c:v", "libx264", "-preset", "slow", "-crf", "26", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out], check=True)

    with open(os.path.join(OUT_DIR, fname + ".vtt"), "w") as f:
        f.write("WEBVTT\n\n" + "".join(f"{k + 1}\n{vtt_time(a)} --> {vtt_time(b)}\n{txt}\n\n" for k, (a, b, txt) in enumerate(cues)))
    json.dump({"stops": stops, "duration": round(t, 2)}, open(os.path.join(OUT_DIR, fname + ".json"), "w"))
    print(f"{out}  {t:.0f}s  stops={stops}  {os.path.getsize(out) // 1024} KB")


if __name__ == "__main__":
    from videos import VIDEOS
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for name in args or VIDEOS:
        build(name, VIDEOS[name], use_say="--say" in sys.argv)
