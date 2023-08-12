import requests
import os
import asyncio
import aiohttp

token = os.environ.get('token', '')

base_url = 'https://webexapis.com'

def read_message(token, message_id = '', room_id = ''):

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    if message_id:
        url = f'{base_url}/v1/messages/{message_id}'
        response = requests.get(url, headers=headers)
        return response.json().get('text', '')
    
    if room_id:
        url = f'{base_url}/v1/messages'
        params = {'roomId': room_id, 'max': 10}
        response = requests.get(url, headers=headers, params=params)
        messages = [{'email':item['personEmail'], 'text': item['text']} for item in response.json()["items"]]
        return messages

def send_message(token,message, room_id='', person_email=''):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    url = f'{base_url}/v1/messages/'
    payload = {}
    if room_id:
        payload = {
            'roomId': room_id, 
            'text': message
        }
    if person_email:
        payload = {
            'toPersonEmail': person_email, 
            'text': message
        }
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code

def read_direct_message(token):
    url = 'https://webexapis.com/v1/messages/direct?personEmail=devcor2023-chatbot%40webex.bot'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def get_token(client_id, client_secret, code, redirect_uri):
    url = 'https://webexapis.com/v1/access_token'
    params = {
        'grant_type': 'authorization_code',
        'client_id': client_id, 
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        return response.json().get('access_token', '')
    return None

# async def send_message(token,message, room_id='', person_email=''):
#     headers = {
#         'Authorization': f'Bearer {token}',
#         'Content-Type': 'application/json'
#     }
#     url = f'{base_url}/v1/messages/'
#     if room_id:
#         payload = {
#             'roomId': room_id, 
#             'text': message
#         }
#     if person_email:
#         payload = {
#             'toPersonEmail': person_email, 
#             'text': message
#         }
    
#     async with aiohttp.ClientSession(headers=headers) as session:
#         async with session.post(url, json=payload) as response:
#             return await response.json()

# async def read_direct_message(token):
#     url = 'https://webexapis.com/v1/messages/direct?personEmail=devcor2023-chatbot%40webex.bot'
#     headers = {
#         'Authorization': f'Bearer {token}',
#         'Content-Type': 'application/json'
#     }
#     async with aiohttp.ClientSession(headers=headers) as session:
#         async with session.get(url) as response:
#             return await response.json()
        
if __name__ == '__main__':
    room_id = 'Y2lzY29zcGFyazovL3VzL1JPT00vZTA0YTVhZTAtMjkxNy0xMWVlLWE0ZDUtMmQwNDkxNzFhZDVj'
    message = 'I am a bot'
    send_message(token=token, room_id=room_id, message=message)
