import logging
import telebot
import requests
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

user_states = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    # Send the user the menu with Login and Register options
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Login', 'Register')
    bot.send_message(
        message.chat.id, "Welcome! Please choose an option:", reply_markup=markup)
    # Set user state to initial state (neither login nor register)
    user_states[message.chat.id] = {'state': 'initial'}


@bot.message_handler(func=lambda message: True)
def handle_user_input(message):
    chat_id = message.chat.id
    user_input = message.text

    if user_states[chat_id]['state'] == 'initial':
        # Handle menu options
        if user_input.lower() == 'login':
            bot.send_message(
                chat_id, "Please enter your username and password separated by space (e.g., username password).")
            user_states[chat_id]['state'] = 'login'
        elif user_input.lower() == 'register':
            bot.send_message(
                chat_id, "Please enter your desired username, password, and display name separated by space (e.g., username password displayname).")
            user_states[chat_id]['state'] = 'register'
        else:
            bot.send_message(
                chat_id, "Invalid choice. Please choose 'Login' or 'Register'.")
    elif user_states[chat_id]['state'] == 'login':
        # Assume message format: "username password"
        username, password = user_input.split()
        login_success = perform_login(chat_id, username, password)
        if login_success:
            bot.send_message(
                chat_id, "Login successful! You can now start chatting.")
            user_states[chat_id]["state"] = 'chat'
            user_states[chat_id]['username'] = username
        else:
            bot.send_message(chat_id, "Invalid credentials. Please try again.")
    elif user_states[chat_id]['state'] == 'register':
        # Assume message format: "username password display_name"
        username, password, display_name = user_input.split()
        registration_success = perform_registration(
            username, password, display_name)
        if registration_success:
            bot.send_message(
                chat_id, "Registration successful! You can now login.")
            user_states[chat_id] = 'login'
        else:
            bot.send_message(chat_id, "Registration failed. Please try again.")
    elif user_states[chat_id]['state'] == 'chat':
        headers = user_states[chat_id]['headers']
        print(headers)
        username = user_states[chat_id]['username']
        agent_name = 'Jasmine'
        response = send_message_to_persona(
            headers, username, agent_name, user_input)
        bot.send_message(chat_id, response)


def perform_login(chat_id, username, password):
    login_data = {
        'username': username,
        'password': password
    }
    response = requests.post(
        os.getenv('LOGIN_ENDPOINT'), json=login_data)
    if response.status_code == 200:
        print("Login successful.")
        session_cookie = response.cookies.get('connect.sid')

        # Include session cookie in the headers of the next request
        headers = {
            'Cookie': f'connect.sid={session_cookie}'
        }

        user_states[chat_id]['headers'] = headers

        return True

    return False


def perform_registration(username, password, display_name):
    # Make a POST request to the registration endpoint with username, password, and display_name
    registration_data = {
        'username': username,
        'password': password,
        'display_name': display_name
    }
    response = requests.post(
        os.getenv('REGISTER_ENDPOINT'), json=registration_data)
    return response.status_code == 200


def send_message_to_persona(headers, username, agent_name, message):
    chat_data = {
        'username': username,
        'agent_name': agent_name,
        'message': message
    }
    response = requests.post(
        os.getenv('CHAT_ENDPOINT'), json=chat_data, headers=headers)
    print(response.json())
    return response.json().get('message_reply', 'Error processing your request')


bot.polling()
