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
                for message_element in messages:
                    if 'message' in message_element:
                        recieved_message(message_element)
                    elif 'postback' in message_element:
                        recieved_postback(message_element)
                    else:
                        print("Unknown event: " + message_element)

def recieved_postback(postback_data):
    sender_id = postback_data['sender']['id']
    payload_id = postback_data['postback']['payload']
    payload_title = postback_data['postback']['title']

    print(payload_id)

    # payload para todo lo que es del grupo Carta

    if (payload_id == 'CARTA_PASTAS'):
        send_payload_pastas_message(sender_id)
    elif (payload_id == 'CARTA_PIZZAS'):
        send_payload_pizzas_message(sender_id)
    elif (payload_id == 'CARTA_PARRILLAS'):
        send_payload_parrillas_message(sender_id)

    # payload para todo lo que es el grupo Locales

    elif (payload_id == 'JUNIN_LOCALES'):
        send_payload_ljunin_message(sender_id)
    elif (payload_id == 'AYACUCHO_LOCALES'):
        send_payload_layacucho_message(sender_id)
    elif (payload_id == 'LIMA_LOCALES'):
        send_payload_layacucho_message(sender_id)

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
        send_text_message(sender_id)
    elif 'attachments' in message_data['message']:
        message_value_attachments = message_value['attachments']
        print(message_value_attachments)
        send_text_message(sender_id)

def send_payload_message(recipientid, messagetext):
    message_answer = {
        'recipient': {
            'id': recipientid
        },
        'message': {
            'text': messagetext
        }
    }
    call_send_api(message_answer)

def send_payload_pastas_message(recipientid):
    message_answer = {
        'recipient': {
            'id': recipientid
        },
        'message': {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [
                        {
                            'title': 'Tallarin a Bolognesa',
                            'image_url': 'https://static.pexels.com/photos/8500/food-dinner-pasta-spaghetti-8500.jpg',
                        },
                        {
                            'title': 'Tallarin a lo Alfredo',
                            'image_url': 'https://static.pexels.com/photos/46182/pasta-noodles-plate-eat-46182.jpeg',
                        }
                    ]
                }
            }
        }
    }

    call_send_api(message_answer)

def send_payload_pizzas_message(recipientid):
    message_answer = {
        'recipient': {
            'id': recipientid
        },
        'message': {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [
                        {
                            'title': 'Tallarin a Bolognesa',
                            'image_url': 'https://static.pexels.com/photos/8500/food-dinner-pasta-spaghetti-8500.jpg',
                        },
                        {
                            'title': 'Tallarin a lo Alfredo',
                            'image_url': 'https://static.pexels.com/photos/46182/pasta-noodles-plate-eat-46182.jpeg',
                        }
                    ]
                }
            }
        }
    }

    call_send_api(message_answer)

def send_payload_parrillas_message(self, arg):
    message_answer = {
        'recipient': {
            'id': recipientid
        },
        'message': {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [
                        {
                            'title': 'Tallarin a Bolognesa',
                            'image_url': 'https://static.pexels.com/photos/8500/food-dinner-pasta-spaghetti-8500.jpg',
                        },
                        {
                            'title': 'Tallarin a lo Alfredo',
                            'image_url': 'https://static.pexels.com/photos/46182/pasta-noodles-plate-eat-46182.jpeg',
                        }
                    ]
                }
            }
        }
    }

    call_send_api(message_answer)

def send_payload_ljunin_message(recipientid):
    message_answer = {
        'recipient': {
            'id': recipientid
        },
        'message': {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [
                        {
                            'title': 'Toto\'s Huancayo',
                            'image_url': 'https://maps.googleapis.com/maps/api/staticmap?center=Toto%27s+Pizza+Huancayo&zoom=17&size=640x400&markers=red:blue|Toto%27s+Pizza+Huancayo&key',
                            'subtitle': 'Av. Leandra Torres N°112, San Carlos - Huancayo',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'url': 'https://www.facebook.com/totospizza.pe/',
                                    'title': 'Fanpage'
                                },
                                {
                                    'type': 'phone_number',
                                    'title': 'Llamar',
                                    'payload': '(064) 235496'
                                },
                                {
                                    'type': 'element_share'
                                }
                            ]
                        },
                        {
                            'title': 'Toto\'s San Carlos',
                            'image_url': 'https://maps.googleapis.com/maps/api/staticmap?center=Toto%27s+Pizza+Huancayo&zoom=17&size=640x400&markers=red:blue|Toto%27s+Pizza+Huancayo&key',
                            'subtitle': 'Av. Leandra Torres N°112, San Carlos - Huancayo',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'url': 'https://www.facebook.com/totospizza.pe/',
                                    'title': 'Fanpage'
                                },
                                {
                                    'type': 'phone_number',
                                    'title': 'Llamar',
                                    'payload': '(064) 235496'
                                },
                                {
                                    'type': 'element_share'
                                }
                            ]
                        },
                        {
                            'title': 'Toto\'s El Tambo',
                            'image_url': 'https://maps.googleapis.com/maps/api/staticmap?center=Toto%27s+Pizza+Huancayo&zoom=17&size=640x400&markers=red:blue|Toto%27s+Pizza+Huancayo&key',
                            'subtitle': 'Av. Leandra Torres N°112, San Carlos - Huancayo',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'url': 'https://www.facebook.com/totospizza.pe/',
                                    'title': 'Fanpage'
                                },
                                {
                                    'type': 'phone_number',
                                    'title': 'Llamar',
                                    'payload': '(064) 235496'
                                },
                                {
                                    'type': 'element_share'
                                }
                            ]
                        },
                        {
                            'title': 'Toto\'s Tarma',
                            'image_url': 'https://maps.googleapis.com/maps/api/staticmap?center=Toto%27s+Pizza+Huancayo&zoom=17&size=640x400&markers=red:blue|Toto%27s+Pizza+Huancayo&key',
                            'subtitle': 'Av. Leandra Torres N°112, San Carlos - Huancayo',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'url': 'https://www.facebook.com/totospizza.pe/',
                                    'title': 'Fanpage'
                                },
                                {
                                    'type': 'phone_number',
                                    'title': 'Llamar',
                                    'payload': '(064) 235496'
                                },
                                {
                                    'type': 'element_share'
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }

    call_send_api(message_answer)

def send_payload_layacucho_message(recipientid):
    message_answer = {
        'recipient': {
            'id': recipientid
        },
        'message': {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [
                        {
                            'title': 'Toto\'s Huancayo',
                            'image_url': 'https://maps.googleapis.com/maps/api/staticmap?center=Toto%27s+Pizza+Huancayo&zoom=17&size=640x400&markers=red:blue|Toto%27s+Pizza+Huancayo&key',
                            'subtitle': 'Av. Leandra Torres N°112, San Carlos - Huancayo',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'url': 'https://www.facebook.com/totospizza.pe/',
                                    'title': 'Fanpage'
                                },
                                {
                                    'type': 'phone_number',
                                    'title': 'Llamar',
                                    'payload': '(064) 235496'
                                },
                                {
                                    'type': 'element_share'
                                }
                            ]
                        },
                        {
                            'title': 'Toto\'s San Carlos',
                            'image_url': 'https://maps.googleapis.com/maps/api/staticmap?center=Toto%27s+Pizza+Huancayo&zoom=17&size=640x400&markers=red:blue|Toto%27s+Pizza+Huancayo&key',
                            'subtitle': 'Av. Leandra Torres N°112, San Carlos - Huancayo',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'url': 'https://www.facebook.com/totospizza.pe/',
                                    'title': 'Fanpage'
                                },
                                {
                                    'type': 'phone_number',
                                    'title': 'Llamar',
                                    'payload': '(064) 235496'
                                },
                                {
                                    'type': 'element_share'
                                }
                            ]
                        },
                        {
                            'title': 'Toto\'s El Tambo',
                            'image_url': 'https://maps.googleapis.com/maps/api/staticmap?center=Toto%27s+Pizza+Huancayo&zoom=17&size=640x400&markers=red:blue|Toto%27s+Pizza+Huancayo&key',
                            'subtitle': 'Av. Leandra Torres N°112, San Carlos - Huancayo',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'url': 'https://www.facebook.com/totospizza.pe/',
                                    'title': 'Fanpage'
                                },
                                {
                                    'type': 'phone_number',
                                    'title': 'Llamar',
                                    'payload': '(064) 235496'
                                },
                                {
                                    'type': 'element_share'
                                }
                            ]
                        },
                        {
                            'title': 'Toto\'s Tarma',
                            'image_url': 'https://maps.googleapis.com/maps/api/staticmap?center=Toto%27s+Pizza+Huancayo&zoom=17&size=640x400&markers=red:blue|Toto%27s+Pizza+Huancayo&key',
                            'subtitle': 'Av. Leandra Torres N°112, San Carlos - Huancayo',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'url': 'https://www.facebook.com/totospizza.pe/',
                                    'title': 'Fanpage'
                                },
                                {
                                    'type': 'phone_number',
                                    'title': 'Llamar',
                                    'payload': '(064) 235496'
                                },
                                {
                                    'type': 'element_share'
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }

    call_send_api(message_answer)

def send_payload_llima_message(recipientid):
    message_answer = {
        'recipient': {
            'id': recipientid
        },
        'message': {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [
                        {
                            'title': 'Toto\'s Huancayo',
                            'image_url': 'https://maps.googleapis.com/maps/api/staticmap?center=Toto%27s+Pizza+Huancayo&zoom=17&size=640x400&markers=red:blue|Toto%27s+Pizza+Huancayo&key',
                            'subtitle': 'Av. Leandra Torres N°112, San Carlos - Huancayo',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'url': 'https://www.facebook.com/totospizza.pe/',
                                    'title': 'Fanpage'
                                },
                                {
                                    'type': 'phone_number',
                                    'title': 'Llamar',
                                    'payload': '(064) 235496'
                                },
                                {
                                    'type': 'element_share'
                                }
                            ]
                        },
                        {
                            'title': 'Toto\'s San Carlos',
                            'image_url': 'https://maps.googleapis.com/maps/api/staticmap?center=Toto%27s+Pizza+Huancayo&zoom=17&size=640x400&markers=red:blue|Toto%27s+Pizza+Huancayo&key',
                            'subtitle': 'Av. Leandra Torres N°112, San Carlos - Huancayo',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'url': 'https://www.facebook.com/totospizza.pe/',
                                    'title': 'Fanpage'
                                },
                                {
                                    'type': 'phone_number',
                                    'title': 'Llamar',
                                    'payload': '(064) 235496'
                                },
                                {
                                    'type': 'element_share'
                                }
                            ]
                        },
                        {
                            'title': 'Toto\'s El Tambo',
                            'image_url': 'https://maps.googleapis.com/maps/api/staticmap?center=Toto%27s+Pizza+Huancayo&zoom=17&size=640x400&markers=red:blue|Toto%27s+Pizza+Huancayo&key',
                            'subtitle': 'Av. Leandra Torres N°112, San Carlos - Huancayo',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'url': 'https://www.facebook.com/totospizza.pe/',
                                    'title': 'Fanpage'
                                },
                                {
                                    'type': 'phone_number',
                                    'title': 'Llamar',
                                    'payload': '(064) 235496'
                                },
                                {
                                    'type': 'element_share'
                                }
                            ]
                        },
                        {
                            'title': 'Toto\'s Tarma',
                            'image_url': 'https://maps.googleapis.com/maps/api/staticmap?center=Toto%27s+Pizza+Huancayo&zoom=17&size=640x400&markers=red:blue|Toto%27s+Pizza+Huancayo&key',
                            'subtitle': 'Av. Leandra Torres N°112, San Carlos - Huancayo',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'url': 'https://www.facebook.com/totospizza.pe/',
                                    'title': 'Fanpage'
                                },
                                {
                                    'type': 'phone_number',
                                    'title': 'Llamar',
                                    'payload': '(064) 235496'
                                },
                                {
                                    'type': 'element_share'
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }

    call_send_api(message_answer)

def send_text_message(recipientid):
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
                'composer_input_disabled': False,
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
