import telebot
from Config import keys, TOKEN
from Utils import ConversionExeption, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Добро пожаловвать в бота для конвертации валюты!\n\n" \
                   "Для использования бота, следуйте инструкциям:\n" \
                   "1. Выберите валюту, которую хотите конвертировать.\n" \
                   "2. Выберите валюту, в которую хотите конвертировать.\n" \
                   "3. Введите количество конвертируемой валюты:\n\n" \
                   "Пример использования:\n" \
                   "доллар евро 100\n" \
                   "Это вернет эквивалент 100 долларов США в Евро\n" \
                   "Для списка доступной валюты, используйте команду /values'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Список доступных валют:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConversionExeption('Слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConversionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()