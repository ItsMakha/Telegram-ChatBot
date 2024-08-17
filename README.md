#Swazi Bakes Telegram Bot
Welcome to the Swazi Bakes Telegram Bot project! This bot, named Robo Baker, is designed to assist customers of Swazi Bakes with various queries related to cakes, bakery services, and more. The bot utilizes Python and the python-telegram-bot library for its functionality.

Features
Greeting and Help: Responds to /start and /help commands with a friendly introduction and assistance offer.
Custom Commands: Handles /custom command for specific responses.
Message Handling: Analyzes and responds to user messages about bakery details, cake prices, ordering, delivery, and more.
Error Handling: Logs errors encountered during bot operations.
Installation
Clone the Repository:

bash
Copy code
git clone <repository-url>
Navigate to the Project Directory:

bash
Copy code
cd <project-directory>
Install Dependencies:
Ensure you have Python 3.8+ installed. Then, install the required packages using:

bash
Copy code
pip install python-telegram-bot
Configuration
Update the token and bot_username with your bot's token and username. These are crucial for connecting your bot to the Telegram API.

python
Copy code
token: Final = 'YOUR_BOT_TOKEN'
bot_username: Final = '@your_bot_username'
Usage
Run the Bot:

bash
Copy code
python bot.py
Interact with the Bot:

Start the conversation with /start.
Get help with /help.
Use custom commands as defined in the custom function.
Bot Functions
/start: Sends a welcome message.
/help: Provides help information.
/custom: Responds with a custom message.
Message Handling
The bot responds to user messages based on predefined patterns. It recognizes greetings, location queries, cake prices, and more. If a message does not match any predefined patterns, the bot will ask for clarification.

Error Handling
Errors during bot operation are logged to the console for debugging purposes.

Contributing
If you have any suggestions or improvements, feel free to open an issue or submit a pull request.
