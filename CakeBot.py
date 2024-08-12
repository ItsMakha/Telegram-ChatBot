from typing import Final
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes

token: Final = '7306843774:AAHiA6YcIcc2Z3fmj2_J6hbyWOUMMPqjaeU'
bot_username: Final = '@swazibakesbot'

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, do you need help!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your bot.")
    
async def custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Custom command")

def handler(text: str) -> str:
    processed: str = text.lower()
    if "hello" in processed:
        return "Hello there!"
    if "how are you" in processed:
        return "I'm doing great!"
    return "I don't understand!"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type == 'group':
        if bot_username in text:
            new_text = text.replace(bot_username, '').strip()
            response = handler(new_text)
        else:
            response = handler(text)
    else:
        response = handler(text)
        
    print('Bot:', response)
    await update.message.reply_text(response)   

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting Bot...')
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('custom', custom))
    
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    application.add_error_handler(error)
    print("Polling...")
    application.run_polling(poll_interval=3)
