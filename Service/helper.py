import requests
import json
from ext.pickler import Pickler as pcl


def send_message(url: str,
                 chat_id: int,
                 text: str,
                 buttons: list or None = None,
                 one_time_keyboard: bool = True,
                 resize_keyboard: bool = True,
                 remove_keyboard: bool = False):
    if buttons is None:
        payload = {
            "chat_id": chat_id,
            "text": text,
        }
        if remove_keyboard:
            payload.update({"reply_markup": {
                "remove_keyboard": remove_keyboard
            }})
            payload["reply_markup"].update({'remove_keyboard': remove_keyboard})
    elif isinstance(buttons, list) is True:
        print('мы тут')
        reply_markup = [[{"text": text}] for text in buttons]

        payload = {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": {"keyboard": reply_markup,
                             "resize_keyboard": resize_keyboard,
                             "one_time_keyboard": one_time_keyboard}
        }
        if remove_keyboard:
            payload["reply_markup"].update({'remove_keyboard': remove_keyboard})


    headers = {
        "Content-Type": "application/json",
    }
    payload = json.dumps(payload)
    data = requests.get(url, data=payload, headers=headers)

    print(data.content)


class GetVac:
    def __init__(self, vacs_filename):
        self.vacs = pcl.get_pickle_file(vacs_filename)

    def get_vac_by_id(self, key: int):
        if key in self.vacs.keys():
            return self.vacs[key]
        else:
            return False

    def update_cache(self, new_cache):
        self.vacs = new_cache
