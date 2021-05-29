'''Handlers'''
def check(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Bot is running'
    )
