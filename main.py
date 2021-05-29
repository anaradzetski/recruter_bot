"""Main module"""
import re
import logging
from telegram.ext import Updater, CommandHandler
from handlers import check

TOKEN_FILE = 'token.txt'

def main():
    """main function"""
    logging.basicConfig(level=logging.INFO)
    with open(TOKEN_FILE) as f:
        token = re.match(r'\S+', f.read()).group(0)
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('check', check))
    updater.start_polling()


if __name__ == '__main__':
    main()
