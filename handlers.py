'''Handlers'''
import json
import inspect
from functools import wraps

import telegram as tel
import telegram.ext as telex

HANDLERS = []

def handler(handler_cls: telex.Handler, *args, **kwargs):
    """Indicates that this function will be used as handler.

    Args:
        cls:
            name of Handler or a Handler class. If handler
            decorator is used, than function will be registred as
            `cls` callback.
    """
    def ret_dec(func):
        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())
        if (
            len(param_names) != 2 or
            param_names[0] != 'update' or
            param_names[1] != 'context'
        ):
            raise ValueError('Handler callback should have two params: update and context')

        @wraps(func)
        def ret_func(update, context):
            return func(update, context)
        HANDLERS.append(handler_cls(*args, **kwargs, callback=ret_func))

        return ret_func

    return ret_dec


@handler(telex.CommandHandler, 'check')
def check(update, context):
    """Checks wether bot is on"""
    context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text='Bot is running'
    )


@handler(telex.CommandHandler, 'start')
def start(update, context):
    """Enables buttons with shortcuts."""
    if not hasattr(start, 'markup'):
        with open('shortcuts.json') as f:
            shortcuts_json = json.load(f)
        keyboard = [[key] for key in shortcuts_json.keys()]
        start.markup = tel.ReplyKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text='Enabling buttons...',
        reply_markup=start.markup
    )


@handler(telex.CommandHandler, 'stop')
def stop(update, context):
    """Disables buttons with shortcuts."""
    context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text='Disabling buttons...',
        reply_markup=tel.ReplyKeyboardRemove()
    )
