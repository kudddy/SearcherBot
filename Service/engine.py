from flask import Flask, request
from flask_json import FlaskJSON, as_json
from flask import abort
from Service.validform import Updater
from Service.statemachine import Stages
from Service.callback import hello_message, analyze_text_and_give_vacancy, goodbye_message

state = {0: hello_message, 1: analyze_text_and_give_vacancy, 2: goodbye_message}

stage = Stages(state)


class FlaskApp:
    def __init__(self):
        pass

    @staticmethod
    def create_flask_app():
        app = Flask(__name__)
        app.config['JSON_AS_ASCII'] = False

        @as_json
        @app.route("/", methods=['POST'])
        def post():
            try:
                data = request.form if request.form else request.json
                if request.method == "POST":
                    message = Updater(**dict(data))
                    print('му тут')
                    stage.next(message)
                    print('а теперь тут')
                    return "ok"
            except Exception as e:
                print(e)
                abort(404)

        @app.route("/health_status", methods=['GET'])
        def health():
            return "status ok"

        FlaskJSON(app)
        return app

    def run(self):
        app = self.create_flask_app()
        # app = app.run(host='0.0.0.0', port=80, debug=False)
        return app
