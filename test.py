import unittest
from time import sleep

from db.schema import mc
from ext.ClientFasttext import ClientFasttext

from Service.const import url_fasttext, token_fastext
from SearchEngine.EasySearchEngine import InversIndexSearch

from Service.validform import Updater
from Service.statemachine import Stages
from Service.callback import hello_message, analyze_text_and_give_vacancy, goodbye_message

from Service.const import timeout_for_chat

state = {0: hello_message, 1: analyze_text_and_give_vacancy, 2: goodbye_message}

stage = Stages(state)


class TestExternalSystem(unittest.TestCase):

    def test_set_get_memcached(self):
        mc.set("1", "True")
        self.assertEqual("True", mc.get("1"))

    def test_w2v(self):
        fast_text = ClientFasttext(url_fasttext, token_fastext)

        vector = fast_text.get_vector("python")

        w2vector = [[
            0.3831615746021271,
            0.0579051673412323,
            -0.3102169930934906,
            -6.0114474763395265e-05,
            -0.3712293207645416,
            -0.6409314274787903,
            0.053606513887643814,
            0.2954348921775818,
            -0.2621344029903412,
            -0.2599843442440033,
            0.05775520205497742,
            -0.15478941798210144,
            0.7503441572189331,
            0.024714624509215355,
            -0.2166610062122345,
            -0.10067377239465714,
            -0.11167310923337936,
            0.6095190048217773,
            0.37952184677124023,
            0.2928634285926819,
            -0.05554569885134697,
            -0.6183294653892517,
            -0.32901743054389954,
            0.008030018769204617,
            0.16778695583343506,
            0.3403465151786804,
            -0.21320435404777527,
            -0.39287400245666504,
            -0.26639360189437866,
            0.7491536736488342,
            0.16045859456062317,
            -0.2057056427001953,
            0.29343363642692566,
            0.30280977487564087,
            -0.20980900526046753,
            -0.10072995722293854,
            -0.6806819438934326,
            0.2195231169462204,
            0.010341045446693897,
            -0.2623165547847748,
            -0.386874794960022,
            -0.1462601274251938,
            -0.4416371285915375,
            -0.6314334869384766,
            0.01630767434835434,
            0.07702244818210602,
            0.028970392420887947,
            -0.11687956005334854,
            0.23166175186634064,
            0.19385799765586853,
            -0.008978605270385742,
            -0.3631614148616791,
            -0.019861014559864998,
            -0.26669490337371826,
            0.05698290839791298,
            -0.09984977543354034,
            -0.33519503474235535,
            -0.029964203014969826,
            -0.6388673186302185,
            -0.04549388214945793
        ]]

        self.assertEqual(w2vector, vector)


class TestInternalSystem(unittest.TestCase):
    maxDiff = None

    def test_inverse_search_system(self):
        search = InversIndexSearch(url=url_fasttext, token=token_fastext)
        result = search.search("python")

        self.assertEqual(list, type(result))

    def test_message_valid_form_user_one(self):
        data = {
            "update_id": 243475549,
            "message": {
                "message_id": 9450,
                "from": {
                    "id": 81432612,
                    "is_bot": False,
                    "first_name": "Kirill",
                    "username": "kkkkk_kkk_kkkkk",
                    "language_code": "ru"
                },
                "chat": {
                    "id": 81432612,
                    "first_name": "Kirill",
                    "username": "kkkkk_kkk_kkkkk",
                    "type": "private"
                },
                "date": 1589404439,
                "text": "python"
            }
        }

        message = Updater(**data)

        stage.next(message)

        stage.next(message)

        stage.next(message)

        sleep(timeout_for_chat + 2)

        stage.next(message)

    def test_message_valid_form_user_two(self):
        data = {
            "update_id": 632560263,
            "message": {
                "message_id": 505,
                "from": {
                    "id": 710828013,
                    "is_bot": False,
                    "first_name": "Серега",
                    "language_code": "ru"
                },
                "chat": {
                    "id": 710828013,
                    "first_name": "Серега",
                    "type": "private"
                },
                "date": 1600629554,
                "text": "java"
            }
        }

        message = Updater(**data)

        stage.next(message)

        stage.next(message)

        stage.next(message)
        data = {
            "update_id": 632560263,
            "message": {
                "message_id": 505,
                "from": {
                    "id": 710828013,
                    "is_bot": False,
                    "first_name": "Серега",
                    "language_code": "ru"
                },
                "chat": {
                    "id": 710828013,
                    "first_name": "Серега",
                    "type": "private"
                },
                "date": 1600629554,
                "text": "Нет"
            }
        }

        message = Updater(**data)

        stage.next(message)

        sleep(timeout_for_chat + 2)

        stage.next(message)


if __name__ == "__main__":
    unittest.main()
