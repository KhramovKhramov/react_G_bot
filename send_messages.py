from telegram import ReplyKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import ConversationHandler


def get_chat_id(update, context):
    update.message.reply_text(
        'Введите Chat ID пользователя, которому хотите отправить сообщение:'
        )

    return 'text'


def get_text_message(update, context):
    context.user_data['data'] = {'chat_id': int(update.message.text)}
    update.message.reply_text(
        'Введите текст сообщения:'
    )

    return 'message'


def send_message(update, context):
    context.user_data['data']['text'] = update.message.text
    text = context.user_data['data']['text']
    chat_id = context.user_data['data']['chat_id']
    reply_keyboard = [['Отправить сообщение']]
    try:
        context.bot.send_message(
            chat_id=chat_id,
            text=text
        )

        update.message.reply_text('Сообщение отправлено!',
                                  reply_markup=ReplyKeyboardMarkup(
                                    reply_keyboard, one_time_keyboard=True))
    except BadRequest:
        message = (
            f'<b>К сожалению, чат с ID {chat_id} не найден</b>\n'
            '\n'
            'Возможно, он уже удалил диалог с ботом'
        )
        update.message.reply_text(message,
                                  parse_mode='html',
                                  reply_markup=ReplyKeyboardMarkup(
                                    reply_keyboard, one_time_keyboard=True))

    return ConversationHandler.END


def dialog_error(update, context):
    update.message.reply_text(
        'Пожалуйста, пришлите текстовое сообщение'
        )
