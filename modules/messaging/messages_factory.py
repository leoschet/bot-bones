from enum import Enum

class GenericElementBuilder(object):
    # {
    #     "title":"Welcome to Peter'\''s Hats",
    #     "image_url":"https://petersfancybrownhats.com/company_image.png",
    #     "subtitle":"We'\''ve got the right hat for everyone.",
    #     "default_action": {
    #         "type": "web_url",
    #         "url": "https://peterssendreceiveapp.ngrok.io/view?item=103",
    #         "messenger_extensions": true,
    #         "webview_height_ratio": "tall",
    #         "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
    #     },
    #     "buttons":[
    #         {
    #         "type":"web_url",
    #         "url":"https://petersfancybrownhats.com",
    #         "title":"View Website"
    #         },{
    #         "type":"postback",
    #         "title":"Start Chatting",
    #         "payload":"DEVELOPER_DEFINED_PAYLOAD"
    #         }
    #     ]
    # }
    title = None
    subtitle = None
    image_url = None
    default_action = None
    buttons = None

    def construct_text(self, title, subtitle):
        self.title = title
        self.subtitle = subtitle

    def construct_image(self, image_url):
        self.image_url = image_url

    def construct_default_action(self, url, messenger_extensions=False, webview_height_ratio='tall'):
        self.default_action = {
            'type': 'web_url',
            'url': url,
            'messenger_extensions': messenger_extensions,
            'webview_height_ratio': webview_height_ratio
        }

    def set_buttons(self, buttons):
        if isinstance(buttons, list):
            if len(buttons) <= 3:
                if False not in [isinstance(btn, ButtonBuilder) for btn in buttons]:
                    self.buttons = buttons
                else:
                    raise TypeError(
                        'Buttons object used on Generic Element wasn\'t an Array of buttons.',
                        [type(btn) for btn in buttons]
                    )
            else:
                raise ValueError(
                    'Buttons object used on Generic Element has too many elements.',
                    len(buttons)
                )
        else:
            raise TypeError(
                'Buttons object used on Generic Element wasn\'t an Array.',
                type(self.buttons)
            )

    def get_data(self):
        data = {}

        if self.title is None:
            raise ValueError('Please set Generic Element title.')
        data['title'] = self.title

        if self.subtitle is None:
            raise ValueError('Please set Generic Element subtitle.')
        data['subtitle'] = self.subtitle

        if self.image_url is not None:
            data['image_url'] = self.image_url

        if self.default_action is not None:
            data['default_action'] = self.default_action

        if self.buttons is not None:
            data['buttons'] = [btn.get_data() for btn in self.buttons]

        return data

class ButtonBuilder(object):
    _btype = '' # More types to be added
    title = None
    payload = None
    url = None
    webview_height_ratio = 'full'
    messenger_extensions = False

    def __init__(self, btype):
        if btype == 'postback' or btype == 'web_url' or btype == 'phone_number':
            self._btype = btype
        else:
            raise TypeError(
                'Button type mismatching. Must be postback, web_url or phone_number.',
                btype
            )

    @property
    def btype(self):
        return self._btype

    def construct_title(self, value):
        self.title = value

    def construct_payload(self, value):
        if self.btype == 'web_url':
            raise TypeError(
                'This attribute won\'t be used for this button type.',
                'payload',
                self.btype
            )

        self.payload = value

    def construct_url(self, url, webview_height_ratio='full', messenger_extensions=False):
        if self.btype == 'postback' or self.btype == 'phone_number':
            raise TypeError(
                'This attribute won\'t be used for this button type.',
                'url',
                self.btype
            )

        self.url = url
        self.webview_height_ratio = webview_height_ratio
        self.messenger_extensions = messenger_extensions

    def get_data(self):
        data = {}
        data['type'] = self.btype

        if self.btype == 'postback' or self.btype == 'phone_number':
            if self.title is None:
                raise ValueError(
                    'Please set button title.',
                    self.btype
                )
            data['title'] = self.title

            if self.payload is None:
                raise ValueError(
                    'Please set button pazload.',
                    self.btype
                )
            # In case of phone_number, payload is telephone number
            # In case of postback, payload is developer defined postback
            data['payload'] = self.payload

        elif self.btype == 'web_url':
            if self.title is None:
                raise ValueError(
                    'Please set button title.',
                    self.btype
                )
            data['title'] = self.title,

            if self.url is None:
                raise ValueError(
                    'Please set button URL.',
                    self.btype
                )
            data['url'] = self.url,

            # If it wasn't set, it will use default values
            data['webview_height_ratio'] = self.webview_height_ratio,
            data['messenger_extensions'] = self.messenger_extensions

        return data

class MessagingType(Enum):
    RESPONSE = 1
    UPDATE = 2
    MESSAGE_TAG = 3
    NON_PROMOTIONAL_SUBSCRIPTION = 4

class MessageBuilder(object):
    messaging_type = None
    recipient_id = None

    # Message data
    _data_type = '' # Text or attachment must be set ('text' or 'attachment')
    text = None # UTF-8 and has a 640 character limit.
    attachment = None # Media or Structured Messages.
    quick_replies = None # Array of quick_reply.

    def __init__(self, recipient_id, messaging_type=MessagingType.RESPONSE):
        if isinstance(messaging_type, MessagingType):
            self.messaging_type = messaging_type

        self.recipient_id = recipient_id # PSID

    def construct_text(self, text, qrs=None):
        self._data_type = 'text'
        self.text = text

        if qrs is not None:
            self.quick_replies = qrs

    def construct_image(self, url):
        self._data_type = 'attachment'
        self.attachment = {
            'type': 'image',
            'payload': {
                'url': url
            }
        }

    def construct_audio(self, url):
        self._data_type = 'attachment'
        self.attachment = {
            'type': 'audio',
            'payload': {
                'url': url
            }
        }

    def construct_video(self, url):
        self._data_type = 'attachment'
        self.attachment = {
            'type': 'video',
            'payload': {
                'url': url
            }
        }

    def construct_file(self, url):
        self._data_type = 'attachment'
        self.attachment = {
            'type': 'file',
            'payload': {
                'url': url
            }
        }

    def construct_button(self, btns, qrs=None):
        self._data_type = 'attachment'

        self.attachment = {
            'type': 'template',
            'payload': {
                'template_type': 'button',
                'text': self.text,
                'buttons': btns
            }
        }

        if qrs is not None:
            self.quick_replies = qrs

    def construct_generic(self, elements, qrs=None, image_aspect_ratio='horizontal'):
        self._data_type = 'attachment'
        self.attachment = {
            'type': 'template',
            'payload': {
                'template_type': 'generic',
                'image_aspect_ratio': image_aspect_ratio,
                'elements': elements
            }
        }

        if qrs is not None:
            self.quick_replies = qrs

    def get_data(self):
        message = {}

        if self._data_type == 'text':
            message['text'] = self.text
        elif self._data_type == 'attachment':
            message['attachment'] = self.attachment
        else:
            raise TypeError(
                'Data type mismatching. Text or attachment must be set.',
                self._data_type
            )

        if self.quick_replies is not None:
            message['quick_replies'] = self.quick_replies

        data = {
            'messaging_type': self.messaging_type,
            'recipient': {
                'id': self.recipient_id # PSID
            },
            'message': message
        }

        return data
