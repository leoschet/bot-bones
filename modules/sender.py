import os

import json
import requests
from botbones.logger import log as Log

def send_message(recipient_id, messages):
    """
    Basic message sender
    """

    for message_text in messages:
        Log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

        params = {
            "access_token": os.environ["PAGE_ACCESS_TOKEN"]
        }

        headers = {
            "Content-Type": "application/json"
        }
        
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
        })

        r = requests.post(
            "https://graph.facebook.com/v2.6/me/messages",
            params=params,
            headers=headers,
            data=data
        )

        if r.status_code != 200:
            Log(r.status_code)
            Log(r.text)
            break
