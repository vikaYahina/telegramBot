import telebot
from extensions import APIException, Converter
from config import keys, TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Введите через пробел:\nколичество переводимой валюты, её название, \
в какую валюту перевести\n-----\nСписок доступных валют /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys:
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    try:
        user_input = message.text.split(' ')
        if not len(user_input) == 3:
            raise APIException('Введены некорректные данные')
        amount, quote, base = user_input
        total_base = Converter.get_price(amount, quote, base)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f"Цена {amount} {quote} в {base} = {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)