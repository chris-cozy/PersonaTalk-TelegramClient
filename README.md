# PersonaTalk (Jasmine) - Telegram Client
This telegram bot client is an open-source Python application developed using the Telebot library. This client allows users to interact with the Jasmine agent of the Persona Talk API through the Telegram messaging platform. Users can log in using their Persona Talk API account or register for a new account using the /start command. Once logged in, they can send messages to converse with the Jasmine agent and receive responses in real-time.

## Features
- Login/Register: Users can log in to their existing Persona Talk API account or register for a new account using the /start command.
- Converse with Jasmine: Once logged in, users can send text messages to the Jasmine agent and receive responses instantly.

## Prerequisites
- Python 3.x
- Telebot library (pip install pyTelegramBotAPI)
- Persona Talk API credentials

## Installation
1. Clone the repository:
```
git clone https://github.com/your-username/jasmine-agent-telegram-bot.git
cd jasmine-agent-telegram-bot
```
2. Install the required Python libraries:
```
pip install pyTelegramBotAPI
```
3. Configure your Persona Talk API credentials:
- Open the config.py file.
- Replace YOUR_API_KEY with your Persona Talk API key.
- Modify other configurations (if necessary) such as the endpoint URL.
4. Run the bot:
```
python bot.py
```
## Usage
1. Start the bot by running the bot.py file.
2. Open your Telegram app and search for the bot using the username provided during the bot setup process.
3. Start a conversation with the bot using the /start command.
4. Log in with your Persona Talk API account or register for a new account.
5. Once logged in, send text messages to converse with the Jasmine agent.
## Commands
- /start: Initiates the conversation with the bot. If you are not logged in, it will prompt you to log in or register.
## Contributing
Contributions are welcome! Please follow the Contributing Guidelines to contribute to this project.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
