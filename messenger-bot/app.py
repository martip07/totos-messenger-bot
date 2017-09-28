from chalice import Chalice
from chalicelib import FB_TOKEN
from chalicelib import VER_FB_TOKEN
import requests
import json

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
    request = app.current_request
    data = request.json_body
    entries = data['entry']
    print(entries)
    messages = data['entry'][0]['messaging']
    if request.method == 'POST':
        if (data['object'] == 'page'):
            print(entries)
            for entry_element in entries:
                page_id = entry_element['id']
                time_event = entry_element['time']
                #print(str(page_id) + ' ' + str(time_event))
                for message_element in messages:
                    #print(message_element['message'])
                    #if message_element['message']:
                        #print('pruebas: ' + str(message_element['message']))
                    #    recieved_message(message_element)
                    if 'message' in message_element:
                        recieved_message(message_element)
                    elif 'postback' in message_element:
                        started_action(message_element)
                    else:
                        print("Unknown event: " + message_element)

def started_action(messagedata):

    print(str(messagedata['sender']['id']))

    message_answer = {
        'recipient': {
            'id': str(messagedata['sender']['id'])
        },
        'message': {
            'text': 'En momento se comunicaran contigo, gracias!'
        }
    }

    headers = {'Content-type': 'application/json'}
    r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token='+ FB_TOKEN, json=message_answer, headers=headers)
    print(r.url)

    if r.status_code != requests.codes.ok:
        print(r.text)

                        
def recieved_message(message_data):
    print("Message data: " + str(message_data['message']))
    
    sender_id = message_data['sender']['id']
    recipient_id = message_data['recipient']['id']
    time_message = message_data['timestamp']
    message_value = message_data['message']

    print('Message for user ' + str(sender_id) + ', fb page: ' + str(recipient_id) + ' at ' + str(time_message) + ', the message is: ' + str(message_value))

    message_value_id = message_value['mid']
    if 'text' in message_data['message']:
        message_value_text = message_value['text']
        print(message_value_text)
        if (message_value_text == 'demo'):
            send_generic_message(sender_id, message_value_text)
        elif (message_value_text != 'generic'):
            send_text_message(sender_id, message_value_text)        
    elif 'attachments' in message_data['message']:
        message_value_attachments = message_value['attachments']
        print(message_value_attachments)       
        send_text_message(sender_id, 'Message with attachment recieved')

def send_generic_message(recipientid, messagetext):
    print('Generic message for ' + str(recipientid))

def send_text_message(recipientid, messagetext):
    message_answer = {
        'recipient': {
            'id': recipientid
        },
        'message': {
            'text': 'En momento se comunicaran contigo, gracias!'
        }
    }
    print(message_answer)
    call_send_api(message_answer)

def call_send_api(messagedata):
    headers = {'Content-type': 'application/json'}
    r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token='+ FB_TOKEN, json=messagedata, headers=headers)
    print(r.url)

    if r.status_code != requests.codes.ok:
        print(r.text)

@app.route('/bot-extras', methods=['GET'])
def bot_extras():
    data = {
        'get_started': {
            'payload': 'GET_STARTED_PAYLOAD'
        },
        'greeting': [
            {
                'locale': 'default',
                'text': 'Hola! {{user_first_name}}'
            },
            {
                'locale': 'es_ES',
                'text': 'Hola, {{user_first_name}}. Soy el bot de Toto\'s Pizza, empecemos'
            }
        ],
        'persistent_menu': [
            {
                'locale': 'default',
                'composer_input_disabled': True,
                'call_to_actions': [
                    {
                        'title': 'Carta',
                        'type': 'nested',
                        'call_to_actions': [
                            {
                                'title': 'Pastas',
                                'type': 'postback',
                                'payload': 'CARTA_PASTAS'
                            },
                            {
                                'title': 'Pizzas',
                                'type': 'postback',
                                'payload': 'CARTA_PIZZAS'                            
                            },
                            {
                                'title': 'Parrillas',
                                'type': 'postback',
                                'payload': 'CARTA_PARRILLAS'                            
                            }                       
                        ]
                    },
                    {
                        'title': 'Locales',
                        'type': 'nested',
                        'call_to_actions': [
                            {
                                'title': 'Junin',
                                'type': 'postback',
                                'payload': 'JUNIN_LOCALES'
                            },
                            {
                                'title': 'Ayacucho',
                                'type': 'postback',
                                'payload': 'AYACUCHO_LOCALES'                            
                            },
                            {
                                'title': 'Lima',
                                'type': 'postback',
                                'payload': 'LIMA_LOCALES'                            
                            }                       
                        ]
                    }
                ]
            },
            {
                'locale': 'es_ES',
                'composer_input_disabled': False
            }
        ]
    }
    headers = {'Content-type': 'application/json'}
    r = requests.post('https://graph.facebook.com/v2.6/me/messenger_profile?access_token='+ FB_TOKEN, json=data, headers=headers)
    print(r.url)

    if r.status_code != requests.codes.ok:
        print(r.text)
        return r.text