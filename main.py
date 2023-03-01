from config import openai_key, bot_token, chat_list
import telebot
import openai

bot = telebot.TeleBot(bot_token)
openai.api_key = openai_key

@bot.message_handler(commands=['chat'])
def echo_all(message):
    if message.chat.id in chat_list:
        if len(message.text) >= 2401:
            bot.reply_to(message, "Ваше сообщение не может быть более 2400 символов!")
        else:
            if len(message.text) <= 6:
                bot.reply_to(message, "Привет, Всем! Я юзербот телеграма для общения с ChatGPT через апи OpenAi. Напиши мне что-нибудь, чтобы начать общение.")
            else:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=message.text[1:],
                    max_tokens=2400,
                    temperature=0.3,
                    n=1
                )
                bot.reply_to(message, response['choices'][0]['text'])
    else:
        bot.reply_to(message, "Иди в попу")

bot.polling()