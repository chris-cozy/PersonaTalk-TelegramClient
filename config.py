import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
LOGIN_ENDPOINT = os.getenv('LOGIN_ENDPOINT')
REGISTER_ENDPOINT = os.getenv('REGISTER_ENDPOINT')
CHAT_ENDPOINT = os.getenv('CHAT_ENDPOINT')
