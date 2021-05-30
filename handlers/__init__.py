"""inits HANDLERS"""
import json
from telegram.ext import MessageHandler, Filters
from .handlers import HANDLERS, _SHORTCUTS_FILE, handler

def make_reply_lambda(text):
    """Tmp function to avoid lambdas in loops."""
    return lambda update, context: update.message.reply_text(text)

with open(_SHORTCUTS_FILE) as f:
    shortcuts = json.load(f)
    for key, val in shortcuts.items():
        handler(MessageHandler, Filters.regex(key))(make_reply_lambda(val))
