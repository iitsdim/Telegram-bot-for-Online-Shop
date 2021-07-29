from telegram.ext import *
from auth_data import *
from DataBase import *
from telegram import *
from cart_data import *


def start(update, context):
    # context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)
    keyboard = [
        [InlineKeyboardButton("candies", callback_data='candies')],
        [InlineKeyboardButton("foods", callback_data='foods')],
        [InlineKeyboardButton("drinks", callback_data='drinks')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(welcome_message, reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="You selected " + query.data + "\nWe have:\n" + get_items(query.data))


def unknown_command(update, context):
    txt_for_start = "WHAT!\nThank you for your command but I do understand u please type /start"
    context.bot.send_message(chat_id=update.effective_chat.id, text=txt_for_start)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I am dummy so if u message "
                                                                    "me I will repeat after u loudly!\n"
                                                                    + update.message.text.upper())


def show_for_type(update, context):
    chat = update.effective_chat
    msg = update.message.text.split()
    return context.bot.send_message(chat_id=chat.id, text=show_items_now(msg[0][1:]))


def add_to_cart(update, context):
    chat = update.effective_chat
    msg = update.message.text.split()

    # print(msg)

    try:
        count = int(msg[-1])
        msg.pop()
        item_name = " ".join(msg[1:])
        context.bot.send_message(chat_id=chat.id, text=modify_cart(item_name, count))

    except TypeError:
        context.bot.send_message(chat_id=chat.id, text="Sorry u did mistake in number of items, "
                                                       "please write name and number of needed items")
    except Exception as e:
        context.bot.send_message(chat_id=chat.id, text="Unknown mistake" + str(e))


def rem_from_cart(update, context):
    chat = update.effective_chat
    msg = update.message.text.split()

    # print(msg)

    try:
        count = int(msg[-1])
        msg.pop()
        item_name = " ".join(msg[1:])
        context.bot.send_message(chat_id=chat.id, text=modify_cart(item_name, -count))

    except TypeError:
        context.bot.send_message(chat_id=chat.id, text="Sorry u did mistake in number of items, "
                                                       "please write name and number of needed items")
    except Exception as e:
        context.bot.send_message(chat_id=chat.id, text="Unknown mistake" + str(e))


def show_cart(update, context):
    result = "In your cart you have:"
    total_sum = 0
    for x in current_cart():
        result += "\n" + x[0] + " : " + str(x[1])
        total_sum += x[1] * get_price_for(x[0])
    result += "\n" + "in total you have to pay: " + str(total_sum)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)


def telegram_bot(t_token):
    updater = Updater(token=t_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    dispatcher.add_handler(CommandHandler('foods', show_for_type))
    dispatcher.add_handler(CommandHandler('candies', show_for_type))
    dispatcher.add_handler(CommandHandler('drinks', show_for_type))
    dispatcher.add_handler(CommandHandler('add', add_to_cart))
    dispatcher.add_handler(CommandHandler('rem', rem_from_cart))

    dispatcher.add_handler(CommandHandler('cart', show_cart))

    dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    telegram_bot(token)
