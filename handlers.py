'''Handlers'''
import inspect
from functools import wraps

import telegram.ext as te

_HANDLERS = dict(
    inspect.getmembers(te, lambda obj: inspect.isclass(obj) and issubclass(obj, te.Handler))
)

def handler(handler_cls: te.Handler, *args, **kwargs):
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
        ret_func.handler_inst = handler_cls(*args, **kwargs, callback=ret_func)

        return ret_func

    return ret_dec


@handler(te.CommandHandler, 'check')
def check(update, context):
    """Checks wether bot is on"""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Bot is running'
    )
