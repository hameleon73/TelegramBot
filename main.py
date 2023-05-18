import telebot
from extensions import ConvertionException, CryptoConverter
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    bot.reply_to(message, f'Приветствую, {message.chat.username}\n'
    'данный бот позволяет получать информацию о конвертации валют\n'
    'используйте следующие команды:\n'
    '/help - информация о боте\n'
    '/values - просмотреть список доступных валют\n'
    'Чтобы получить конвертацию по актуальному курсу,\n'
    'введите команду в следующем формате:'
    '<имя валюты> <в какую валюту перевести> <количество валюты для перевода>')

@bot.message_handler(commands=['values',])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types='text',)
def convert(message: telebot.types.Message):

    try:
        values_ = message.text.split(' ')

        if len(values_) > 3:
            raise ConvertionException('Слишком много параметров!')
        elif len(values_) < 3:
            raise ConvertionException('Слишком мало параметров!')


        quote, base, amount = values_

        total_base = float(CryptoConverter.get_price(quote, base, amount))*float(amount)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:

        text = f'Цена {amount} {quote} в {base} : {total_base}'

        bot.send_message(message.chat.id, text)

bot.polling(non_stop = True)