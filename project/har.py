from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

bot = ChatBot('GOD')
bot.set_trainer(ListTrainer)

for files in os.listdir('chatterbot-corpus/chatterbot_corpus/data/english/'):
    data = open('chatterbot-corpus/chatterbot_corpus/data/english/' + files , 'r').readlines()
    bot.train(data)

while True:
    message = input("Creator:")
    if message.strip() != "Bye":
        reply = bot.get_response(message)
        print("GOD :" ,reply)
    if message.strip() == "Bye":
        print("GOD : Bye")
        break
