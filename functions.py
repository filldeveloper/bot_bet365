from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
import telegram
import os

token = os.getenv('TOKEN_TELEGRAM')
updater = Updater(token = token, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Hello there.")

def get_word_info(update, context):
    message = f"Deu certo"
    update.message.reply_text(message)

# run the start function when the user invokes the /start command 
dispatcher.add_handler(CommandHandler("start", start))


# invoke the get_word_info function when the user sends a message 
# that is not a command.
dispatcher.add_handler(MessageHandler(Filters.text, get_word_info))
updater.start_polling()