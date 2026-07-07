#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


API_ROOT = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "gemini-omni-flash-preview"


PROMPTS = {
    "q1": {
        "image": "assets/forgiveness-question.png",
        "output": "assets/gemini-story-q1.mp4",
        "prompt": """
Create a short 10 second 16:9 animated Bible story video for an elementary children's worship lesson.
Use the provided image as the first frame and preserve the same warm 3D animated style, the same Jesus, Peter, disciples, clothing, lighting, and sunny courtyard setting.

Single continuous shot, no scene cuts. The camera slowly pushes in from Peter toward Jesus.
Peter gently asks Jesus about forgiveness, and Jesus listens with a kind smile.
Keep the scene bright, hopeful, reverent, child-friendly, and colorful.

Audio: soft warm background music, gentle outdoor ambience.
Korean child-friendly narration in a calm teacher voice:
"베드로는 예수님께 물었어요. 형제가 죄를 지으면 몇 번이나 용서해야 할까요? 베드로는 일곱 번이면 충분하다고 생각했지만, 예수님은 끝없이 용서하는 마음을 가르쳐 주셨어요."

No scary mood, no dark lighting, no modern objects, no on-screen gibberish text.
""".strip(),
    },
    "q2": {
        "output": "assets/gemini-story-q2.mp4",
        "prompt": """
Create a short 10 second 16:9 animated Bible story video for an elementary children's worship lesson.
Warm 3D animated Bible story style, bright sunny palace courtyard, colorful but reverent, child-friendly.

Single continuous shot, no scene cuts. A humble servant kneels before a kind king on a simple throne.
The servant looks worried because his debt is impossible to repay. The king slowly raises his hand with compassion and forgives the entire debt.
The servant looks amazed and relieved. Golden warm light fills the room.

Audio: soft warm background music, gentle palace ambience.
Korean child-friendly narration in a calm teacher voice:
"종은 왕에게 엄청나게 큰 빚을 졌어요. 스스로는 절대로 갚을 수 없는 빚이었지요. 그런데 왕은 그 빚을 전부 탕감해 주었어요."

No scary mood, no dark lighting, no modern objects, no violence, no on-screen gibberish text.
""".strip(),
    },
    "q3": {
        "output": "assets/gemini-story-q3.mp4",
        "prompt": """
Create a short 10 second 16:9 animated Bible story video for an elementary children's worship lesson.
Warm 3D animated Bible story style, bright village street outside the palace, colorful but reverent, child-friendly.

Single continuous shot, no scene cuts. The same servant who was forgiven walks outside and meets another servant who owes him a small debt.
The forgiven servant looks angry and points at the other servant, while the other servant pleads gently.
Do not show violence; keep the emotion clear but suitable for children. The camera slowly moves closer to show the contrast between receiving mercy and refusing mercy.

Audio: soft but thoughtful background music, gentle outdoor ambience.
Korean child-friendly narration in a calm teacher voice:
"그런데 용서받은 종은 밖으로 나가 자기에게 작은 빚을 진 친구를 만났어요. 큰 은혜를 받았지만, 그 은혜를 친구에게 흘려보내지 못했어요."

No scary mood, no dark lighting, no modern objects, no physical violence, no on-screen gibberish text.
""".strip(),
    },
    "q4": {
        "image": "assets/forgiveness-gospel.png",
        "output": "assets/gemini-story-q4.mp4",
        "prompt": """
Create a short 10 second 16:9 animated Bible story video for an elementary children's worship lesson.
Use the provided image as visual inspiration and preserve its warm, bright, hopeful gospel tone.

Single continuous shot, no scene cuts. A gentle cross-shaped light glows warmly in the background.
A group of children stand together, then one child reaches out to forgive and comfort another child.
The scene should feel peaceful, hopeful, and full of grace. The camera slowly pulls back as warm light spreads.

Audio: soft worshipful background music, gentle ambience.
Korean child-friendly narration in a calm teacher voice:
"예수님은 우리를 먼저 용서해 주셨어요. 그래서 우리도 용서받은 사람답게 서로를 용서하며 살아갈 수 있어요."

No scary mood, no dark lighting, no modern objects, no on-screen gibberish text.
""".strip(),
    },
}


def request_json(method, url, api_key, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("x-goog-api-key", api_key)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            raw = resp.read()
            if not raw:
                return {}
            return json.loads(raw.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc


def download_file(uri, api_key, out_path):
    if uri.startswith("https://"):
        url = uri
    else:
        file_id = uri.split("/")[-1]
        url = f"{API_ROOT}/files/{file_id}:download?alt=media"
    req = urllib.request.Request(url)
    req.add_header("x-goog-api-key", api_key)
    with urllib.request.urlopen(req, timeout=600) as resp:
        out_path.write_bytes(resp.read())


def find_video_content(response):
    if isinstance(response.get("output_video"), dict):
        video = response["output_video"]
        if video.get("data") or video.get("uri"):
            return video
    for step in response.get("steps", []):
        for item in step.get("content", []):
            if item.get("type") == "video":
                return item
    return None


def generate_video(config, api_key):
    out_path = Path(config["output"])
    input_items = []
    task = "text_to_video"
    if config.get("image"):
        image_path = Path(config["image"])
        mime_type = mimetypes.guess_type(image_path.name)[0] or "image/png"
        image_b64 = base64.b64encode(image_path.read_bytes()).decode("ascii")
        input_items.append({"type": "image", "data": image_b64, "mime_type": mime_type})
        task = "image_to_video"
    input_items.append({"type": "text", "text": config["prompt"]})
    payload = {
        "model": MODEL,
        "input": input_items,
        "response_format": {"type": "video", "aspect_ratio": "16:9", "delivery": "uri"},
        "generation_config": {"video_config": {"task": task}},
    }

    response = request_json("POST", f"{API_ROOT}/interactions", api_key, payload)
    video = find_video_content(response)
    if not video:
        debug_path = out_path.with_suffix(".response.json")
        debug_path.write_text(json.dumps(response, ensure_ascii=False, indent=2), encoding="utf-8")
        raise RuntimeError(f"No video found in response. Wrote {debug_path}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    if video.get("data"):
        out_path.write_bytes(base64.b64decode(video["data"]))
    elif video.get("uri"):
        uri = video["uri"]
        if "/files/" in uri:
            file_id = uri.split("/files/")[-1].split(":")[0].split("?")[0]
        else:
            file_id = uri.split("/")[-1]
        for _ in range(120):
            info = request_json("GET", f"{API_ROOT}/files/{file_id}", api_key)
            state = info.get("state", "")
            if state == "ACTIVE":
                break
            if state == "FAILED":
                raise RuntimeError(f"Video generation failed: {json.dumps(info, ensure_ascii=False)}")
            time.sleep(5)
        download_file(uri, api_key, out_path)
    else:
        raise RuntimeError("Video response had neither data nor uri.")

    return out_path


def main():
    parser = argparse.ArgumentParser(description="Generate B-QUEST story videos with Gemini Omni Flash.")
    parser.add_argument("scene", choices=sorted(PROMPTS.keys()))
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Set GEMINI_API_KEY or GOOGLE_API_KEY before running.", file=sys.stderr)
        return 2

    out_path = generate_video(PROMPTS[args.scene], api_key)
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
