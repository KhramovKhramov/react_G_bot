from telegram import ReplyKeyboardMarkup

from utils import main_keyboard


def greet_user(update, context):
    user = update.effective_user
    update.message.reply_text(
        f"Добрый день, {user.first_name}!",
        reply_markup=main_keyboard())


def need_help(update, context):
    reply_keyboard = [['Отправить сообщение']]
    user = update.effective_user
    message = (
        f'Привет, {user.first_name}!'
        '\n'
        'Если хочешь отправить сообщение другому пользователю, напиши мне «Отправить сообщение» и следуй подсказкам'
        '\n'
        '<b>Внимание!</b> Я могу отправить сообщение только пользователю, у которого есть активный чат со мной'
    )
    update.message.reply_text(message,
                              parse_mode='html',
                              reply_markup=ReplyKeyboardMarkup(
                                    reply_keyboard, one_time_keyboard=True))


def print_update(update, context):
    print(update)
