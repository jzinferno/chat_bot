from config import openai_key, bot_token, chat_list
from datetime import datetime
import asyncio
import telebot
import openai

now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
bot = telebot.TeleBot(bot_token)
openai.api_key = openai_key

@bot.message_handler(commands=['id'])
def main_id(message):
    if message.chat.id in chat_list:
        status = 0
    else:
        status = -1
    bot.reply_to(message, message.chat.id)
    print(now, message.chat.id, "/id", status)

@bot.message_handler(commands=['chat'])
def main_chat(message):
    if message.chat.id in chat_list:
        status = 0
        if len(message.text) >= 2401:
            bot.reply_to(message, "Ваше сообщение не может быть более 2400 символов!")
            status = 1
        else:
            if len(message.text) <= 6:
                bot.reply_to(message, "Привет, Всем! Я юзербот телеграма для общения с ChatGPT через апи OpenAi. Напиши мне что-нибудь, чтобы начать общение.")
                status = 1
            else:
                try:
                    response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=message.text[6:],
                        max_tokens=2400,
                        temperature=0.3,
                        n=1
                    )
                except:
                    status = 2
                if status == 0:
                    if len(response['choices'][0]['text']) > 0:
                        bot.reply_to(message, response['choices'][0]['text'])
                else:
                    bot.reply_to(message, 'Произошла ошибка')
    else:
        bot.reply_to(message, "Иди в попу")
        status = -1
    print(now, message.chat.id, "/chat", status)

@bot.message_handler(commands=['img'])
def main_img(message):
    if message.chat.id in chat_list:
        status = 0
        try:
            response = openai.Image.create(
                prompt=message.text[5:],
                size="256x256",
                n=3,
            )
        except:
            status = 2
        if status == 0:
            if len(response["data"][0]["url"]) > 0:
                bot.send_photo(message.chat.id, response["data"][0]["url"], caption=message.text[5:])
        else:
            bot.reply_to(message, 'Произошла ошибка')
    else:
        bot.reply_to(message, "Иди в попу")
        status = -1
    print(now, message.chat.id, "/img", status)

bot.polling()