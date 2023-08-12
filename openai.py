import os
import openai
import requests

api_key = os.environ.get('openai_api_key', '')

headers = {
    'Authorization': f'Bearer {api_key}'
}

url = 'https://api.openai.com/v1/completions'

prompt = 'What is a chat bot?'

payload = {
  "model": "text-davinci-001",
  "prompt": "Say this is a test",
  "max_tokens": 7,
  "temperature": 0,
  "top_p": 1,
  "n": 1,
  "stream": False,
  "logprobs": None,
  "stop": "\n"
}