from chalice import Chalice
from chalicelib import FB_TOKEN
from chalicelib import VER_FB_TOKEN

app = Chalice(app_name='messenger-bot')
app.debug = True


@app.route('/')
def index():
    return {'hello': 'Toto\'s Pizza Messenger Bot'}

@app.route('/webhook', methods=['GET'])
def api_verification():
    token = VER_FB_TOKEN
    request = app.current_request
    if request.method == 'GET':
        if (request.query_params['hub.mode'] == 'subscribe') and (request.query_params['hub.verify_token'] == token):
            print('Validacion de webhook por parte de FB')
            print(token)
            return request.query_params['hub.challenge']
        else:
            print('Validacion incorrecta')
            return 'Validacion incorrecta', 403

@app.route('/webhook', methods=['POST'])
def bot_webhook():
    s