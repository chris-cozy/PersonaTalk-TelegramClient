import logging
import telebot
import requests
from config import BOT_TOKEN, LOGIN_ENDPOINT, REGISTER_ENDPOINT, CHAT_ENDPOINT
from user_state import UserState

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

bot = telebot.TeleBot(BOT_TOKEN)


user_states = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if user_id not in user_states:
        user_states[user_id] = UserState()
    handle_start(message)


def handle_start(message):
    # Send the user the menu with Login and Register options
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Login', 'Register')
    bot.send_message(
        message.chat.id, "Welcome! Please choose an option:", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_user_input(message):
    chat_id = message.chat.id
    user_input = message.text
    user_state = user_states[chat_id]

    if user_state.state == 'initial':
        # Handle menu options
        if user_input.lower() == 'login':
            bot.send_message(
                chat_id, "Please enter your username and password separated by space (e.g., username password).")
            user_state.set_login_state()
        elif user_input.lower() == 'register':
            bot.send_message(
                chat_id, "Please enter your desired username, password, and display name separated by space (e.g., username password displayname).")
            user_state.set_register_state()
        else:
            bot.send_message(
                chat_id, "Invalid choice. Please choose 'Login' or 'Register'.")
    elif user_state.state == 'login':
        # Assume message format: "username password"
        username, password = user_input.split()
        login_success = perform_login(user_state, username, password)
        if login_success:
            bot.send_message(
                chat_id, "Login successful! You can now start chatting.")
        else:
            bot.send_message(chat_id, "Invalid credentials. Please try again.")
    elif user_state.state == 'register':
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
    elif user_state.state == 'chat':
        agent_name = 'Jasmine'
        response = send_message_to_persona(
            user_state, agent_name, user_input)
        bot.send_message(chat_id, response)


def perform_login(user_state, username, password):
    login_data = {
        'username': username,
        'password': password
    }
    response = requests.post(
        LOGIN_ENDPOINT, json=login_data)
    if response.status_code == 200:
        print("Login successful.")
        session_cookie = response.cookies.get('connect.sid')

        # Include session cookie in the headers of the next request
        headers = {
            'Cookie': f'connect.sid={session_cookie}'
        }

        user_state.set_chat_state(username, password, headers)

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
        REGISTER_ENDPOINT, json=registration_data)
    return response.status_code == 200


def send_message_to_persona(user_state, agent_name, message):
    chat_data = {
        'username': user_state.username,
        'agent_name': agent_name,
        'message': message
    }
    response = requests.post(
        CHAT_ENDPOINT, json=chat_data, headers=user_state.headers)

    if response.status_code == 500:
        # Relog and try again
        if perform_login(user_state, user_state.username, user_state.password):
            response = requests.post(
                CHAT_ENDPOINT, json=chat_data, headers=user_state.headers)

    print(response.json())
    return response.json().get('message_reply', 'Error processing your request')


bot.polling()
