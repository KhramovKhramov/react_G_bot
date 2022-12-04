import logging

from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

import settings
from dialog import (dialog_country, dialog_dontknow, dialog_ending,
                    dialog_question)
from handlers import greet_user, need_help
from send_messages import (dialog_error, get_chat_id, get_text_message,
                           send_message)

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(settings.API_KEY)
    dp = mybot.dispatcher

    dialog = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(
            '^(Задать вопрос|задать вопрос)$'), dialog_country)],
        states={'question': [MessageHandler(Filters.regex(
            '^(Болгария|Израиль|Румыния)$'), dialog_question)],
                'ending': [MessageHandler(Filters.text, dialog_ending)]},
        fallbacks=[MessageHandler(Filters.text | Filters.video |
                   Filters.photo | Filters.document |
                   Filters.location | Filters.attachment, dialog_dontknow)])

    send_messages = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(
            '^(Осьминог|осьминог)$'), get_chat_id)],
        states={'text': [MessageHandler(Filters.text, get_text_message)],
                'message': [MessageHandler(Filters.text, send_message)]},
        fallbacks=[MessageHandler(Filters.text | Filters.video |
                   Filters.photo | Filters.document |
                   Filters.location | Filters.attachment, dialog_error)]
        )

    dp.add_handler(dialog)
    dp.add_handler(send_messages)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.regex(
                   "^(Нужна помощь|нужна помощь)$"),
                   need_help))

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
