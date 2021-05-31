'''Handlers'''
import json
import inspect
from functools import wraps
from typing import Iterable, Union

import telegram as tel
import telegram.ext as telex

HANDLERS = []
_SHORTCUTS_FILE = 'conf/shortcuts.json'
_KEYBOARD_CONF_FILE = 'conf/keyboard_conf.json'

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


def build_keyboard(
    buttons: Iterable[str],
    inline: bool = False
) -> Union[tel.ReplyKeyboardMarkup, tel.InlineKeyboardMarkup]:
    """Buids keyboard from button list

    Args:
        buttons: iterable with button names.
        inline: inline mode flag.
    Returns:
        keyboard markup.
    """
    if not hasattr(build_keyboard, 'buttons_in_row'):
        with open(_KEYBOARD_CONF_FILE) as f:
            keyboard_json = json.load(f)
        build_keyboard.buttons_in_row = keyboard_json['buttons_in_row']
    chunk = build_keyboard.buttons_in_row
    buttons_lst = list(buttons)
    button_cls = tel.InlineKeyboardButton if inline else tel.KeyboardButton
    keyboard = [
        [button_cls(name) for name in buttons_lst[i: i + chunk]]
        for i in range(0, len(buttons_lst), chunk)
    ]
    keyboard_cls = tel.InlineKeyboardMarkup if inline else tel.ReplyKeyboardMarkup
    return keyboard_cls(keyboard)


@handler(telex.CommandHandler, 'start')
def start(update, context):
    """Enables buttons with shortcuts."""
    if not hasattr(start, 'markup'):
        with open(_SHORTCUTS_FILE) as f:
            shortcuts_json = json.load(f)
        start.markup = build_keyboard(shortcuts_json.keys())
    context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text='Enabling buttons...',
        reply_markup=start.markup
    )

def _init_buttons_respond():
    def make_reply_lambda(text):
        """Tmp function to avoid lambdas in loops."""
        return lambda update, context: update.message.reply_text(text)

    with open(_SHORTCUTS_FILE) as f:
        shortcuts = json.load(f)
        for key, val in shortcuts.items():
            handler(telex.MessageHandler, telex.Filters.regex(key))(make_reply_lambda(val))


@handler(telex.CommandHandler, 'stop')
def stop(update, context):
    """Disables buttons with shortcuts."""
    context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text='Disabling buttons...',
        reply_markup=tel.ReplyKeyboardRemove()
    )
