from telegram import ReplyKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import ConversationHandler

import settings
from utils import main_keyboard


def dialog_country(update, context):
    reply_keyboard = [['Болгария'], ['Израиль'], ['Румыния']]
    update.message.reply_text(
        'Пожалуйста, выберите страну:',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )

    return 'question'


def dialog_question(update, context):
    context.user_data['dialog'] = {'country': update.message.text}
    update.message.reply_text(
        'Задайте ваш вопрос:'
    )

    return "ending"


def dialog_ending(update, context):
    context.user_data['dialog']['question'] = update.message.text
    user = update.effective_user
    message = (
        f'<b>Новый запрос от @{user.username}</b>\n'
        '\n'
        f'<b>Имя пользователя</b>: {user.first_name} {user.last_name}\n'
        f'<b>ID чата</b>: <code>{update.message.chat.id}</code>\n'
        f'<b>Страна</b>: {context.user_data["dialog"]["country"]}\n'
        f'<b>Текст запроса</b>: {context.user_data["dialog"]["question"]}'
    )
    try:
        context.bot.send_message(chat_id=int(settings.GROUP_ID),
                                 text=message,
                                 parse_mode='html')

        update.message.reply_text('Спасибо, скоро мы свяжемся с вами!',
                                  reply_markup=main_keyboard())

        return ConversationHandler.END

    except (BadRequest, ValueError):
        update.message.reply_text('Спасибо, скоро мы свяжемся с вами!',
                                  reply_markup=main_keyboard())

    return ConversationHandler.END


def dialog_dontknow(update, context):
    update.message.reply_text(
        'Прошу прощения: либо вы не выбрали страну, либо прислали не текст'
        )
