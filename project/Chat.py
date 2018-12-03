from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
bot = ChatBot("Jarvis",trainer='chatterbot.trainers.ListTrainer', storage_adapter='chatterbot.storage.SQLStorageAdapter',
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter'
    ],
    database='./database.sqlite3')
bot.train([
    'How are you?',
    'I am good.',
    'That is good to hear.',
    'Thank you',
    'You are welcome.',
])
print("what is it...")

while True:
    try:
     bot_input = bot.get_response(None)
    except(KeyboardInterrupt, EOFError, SystemExit):
        break
