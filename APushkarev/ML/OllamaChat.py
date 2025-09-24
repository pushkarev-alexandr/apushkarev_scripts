# Chat with artificial intelligence

# v1.1.0
# created by: Pushkarev Aleksandr

import nuke
import os, json
from urllib.request import Request, urlopen

host = os.getenv("OLLAMA_HOST", "localhost")
url = f"http://{host}:11434/api/generate"

data = {
    "model": "llama3.2",
    "prompt": "",
    "stream": False
}

def main():
    msg = nuke.getInput("Message")
    if not msg:
        return
    data["prompt"] = msg
    try:
        payload = json.dumps(data).encode("utf-8")
        req = Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        with urlopen(req, timeout=30) as resp:
            resp_body = resp.read().decode("utf-8")
            resp_json = json.loads(resp_body)
            response_msg = resp_json.get("response", "")
    except Exception as e:
        response_msg = f"Unexpected error: {e}"

    nuke.message(response_msg)
