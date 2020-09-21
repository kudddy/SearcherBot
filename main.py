# from SearchEngine.EasySearchEngine import InversIndexSearch
from Service.engine import FlaskApp


# TODO логирование, фильтраци по города, готов не готов к переезду, автоматический апдейтер индексов и вакансий
try:
    app = FlaskApp().run()
except Exception as e:
    print(e)



























