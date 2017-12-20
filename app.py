"""
Base skeleton for python bots.

To run this application locally:
$ set FLASK_APP=botbones\app.py
$ python -m flask run

"""

import os

from flask import Flask, request



from botbones.logger import log as Log
from botbones.sender import send_message as Send

app = Flask(__name__)

INFORMATION_MESSAGE = "Hello, this is a messenger bot application!"

@app.route('/')
def app_greetings():
    return INFORMATION_MESSAGE

@app.route('/webhook', methods=['GET'])
def verify():
    """
    When the endpoint is registered as a webhook, it must echo back
    the 'hub.challenge' value it receives in the query arguments
    """

    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return INFORMATION_MESSAGE, 200


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Endpoint for processing incoming messaging events
    """

    data = request.get_json()
    Log(data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    # the facebook ID of the person sending you the message
                    sender_id = messaging_event["sender"]["id"]
                    # the recipient's ID, which should be your page's facebook ID
                    recipient_id = messaging_event["recipient"]["id"]
                    # the message's text
                    message_text = messaging_event["message"]["text"]

                    Send(sender_id, ["roger that!", "u sent me: " + message_text])

                # delivery confirmation
                if messaging_event.get("delivery"):
                    pass

                # optin confirmation
                if messaging_event.get("optin"):
                    pass

                # user clicked/tapped "postback" button in earlier message
                if messaging_event.get("postback"):
                    pass

    return "ok", 200


if __name__ == '__main__':
    app.run(debug=True)