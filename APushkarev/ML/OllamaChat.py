# Chat with artificial intelligence

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke
import requests

url = "http://192.168.100.102:11434/api/generate"
data = {
    "model": "mazhor",
    "prompt": "Hello, how are you?",
    "stream": False
}

def main():
    msg = nuke.getInput("Message")
    if not msg:
        return
    data["prompt"] = msg
    response = requests.post(url, json=data)
    response_msg = response.json().get("response", "")
    nuke.message(response_msg)
