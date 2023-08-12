from flask import Flask, request, render_template, session, redirect
from .message_handler import read_message, send_message, get_token, read_direct_message
import random
import os
import requests
import time
import asyncio

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(64)
    bot_token = os.environ['token'] 
    #token = 'YjM4ZjBhMmYtNjc5NC00MWUyLTgxM2YtMzFlNzM5YzViZWQ0OTE3NmZiMzAtOTJl_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'
    base_authorize_url = 'https://webexapis.com/v1/authorize'
    client_id = 'C77646935d75379bd7afcece0b9430e71b3d33abe239701613efe8f7464423ca1'
    client_secret = '9f9c0e62573d1167c2ce4576c937c5e98408cd5b320a00aca7977b59709a398a'
    redirect_uri = 'http://localhost:5005/oauth'
    scope = 'spark:all'

    @app.post('/')
    def webhook_handler():
        payload = request.get_json()
        person_email = payload.get('data', {}).get('personEmail', '')
        if person_email == 'devcor2023-chatbot@webex.bot':
            return 'OK'
        else:
            message_id = payload.get('data', {}).get('id', '')
            room_id = payload.get('data', {}).get('roomId', '')
            message = read_message(token=bot_token, message_id=message_id)
            response_message = f'Your question is "{message}"'
            send_message(token=bot_token, room_id=room_id, message=response_message)
            return f'Responsed'
    
    @app.get('/')
    def home():
        token = session.get('token')
        if token:
            return chatbot(token)
        authorize_url = initialize_url()
        return render_template('home.html', authorize_url = authorize_url)
    
    def initialize_url():
        state = session.get('state') or random.getrandbits(256)
        session['state'] = state
        authorize_url = f'{base_authorize_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}'
        return authorize_url
    
    @app.route('/oauth')
    def oauth():
        if request.args.get('error'):
            return str(request.args.get('error')) + ': ' + str(request.args.get('error_description'))
        
        code = request.args.get('code')
        state = request.args.get('state')
        
        if not (state and code):
            return 'No sate or code'
        
        if str(session.get('state')) != str(state):
            return 'State mismatch'
        
        token = get_token(client_id=client_id, client_secret=client_secret, code=code, redirect_uri=redirect_uri)
        session['token'] = token
        if token:
            return chatbot(token)
        else:
            return 'Failed to get token'
        
    def chatbot(token):
        response = read_direct_message(token)
        messages = [{'email':item['personEmail'], 'text': item['text']} for item in response["items"]]
        messages.reverse()
        return render_template('chatbot.html', token=token, messages = messages)
    
    @app.route('/send-message-to-bot', methods = ['POST'])
    def send_message_to_bot():
        if request.method == 'POST':
            person_email = 'devcor2023-chatbot@webex.bot'
            text = request.form.get('message')
            token = session.get('token')
            if token:
                send_message(token, text, person_email=person_email)
                return redirect('/chats')
            else:
                return redirect('/')
    
    @app.route('/chats')
    def chats():
        token = session.get('token')
        if token:
            return chatbot(token)
        else:
            return redirect('/')
    return app
