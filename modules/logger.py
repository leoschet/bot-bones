import sys
import json
from datetime import datetime

def log(msg, *args, **kwargs):
    """
    A simple wrapper for logging to stdout on heroku
    """

    try:
        if isinstance(msg, dict):
            msg = json.dumps(msg)
        else:
            msg = str(msg).format(*args, **kwargs)
        print(u"{}: {}".format(datetime.now(), msg))
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()
