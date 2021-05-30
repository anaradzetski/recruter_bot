"""Main module"""
import re
import logging
import telegram.ext as te

from handlers import HANDLERS

def load_token(token_file: 'str' = 'conf/token.txt') -> str:
    """Loads token from specified file"""
    with open(token_file) as f:
        return re.match(r'\S+', f.read()).group(0)


def register_handlers(dispatcher: te.Dispatcher) -> None:
    """Registers handlers from handlers.py"""
    for handler in HANDLERS:
        dispatcher.add_handler(handler)


def main():
    """main function"""
    logging.basicConfig(level=logging.INFO)
    updater = te.Updater(load_token())
    dispatcher = updater.dispatcher
    register_handlers(dispatcher)
    updater.start_polling()


if __name__ == '__main__':
    main()
