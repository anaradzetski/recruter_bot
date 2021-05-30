"""Main module"""
import re
import logging
import inspect
import telegram.ext as te

import handlers

def load_token(token_file: 'str' = 'token.txt') -> str:
    """Loads token from specified file"""
    with open(token_file) as f:
        return re.match(r'\S+', f.read()).group(0)


def register_handlers(dispatcher: te.Dispatcher) -> None:
    """Registers handlers from handlers.py"""
    handler_callbacks = inspect.getmembers(
            handlers, lambda obj: hasattr(obj, 'handler_inst')
    )
    for _, handler_callback in handler_callbacks:
        dispatcher.add_handler(handler_callback.handler_inst)


def main():
    """main function"""
    logging.basicConfig(level=logging.INFO)
    updater = te.Updater(load_token())
    dispatcher = updater.dispatcher
    register_handlers(dispatcher)
    updater.start_polling()


if __name__ == '__main__':
    main()
