import os
import logging

import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def convert_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    spotify_token = os.getenv("SPOTIFY_API_TOKEN")
    query = update.message.text
    limit = 3
    _type = "track"
    url = f"https://api.spotify.com/v1/search?q={query}&limit={limit}&access_token={spotify_token}&type={_type}&access_token={spotify_token}"
    response = requests.get(url=url)
    response = response.json()
    logging.info(response)

    spotify_link = response["tracks"]["items"][0]["external_urls"]["spotify"]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=spotify_link)

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    auth_filter = filters.Chat(username="lizaa_t")

    start_handler = CommandHandler('start', start, filters=auth_filter)
    application.add_handler(start_handler)

    convert_link_handler = MessageHandler(auth_filter, convert_link)
    application.add_handler(convert_link_handler)

    application.run_polling()
