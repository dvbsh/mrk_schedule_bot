from dotenv import load_dotenv, dotenv_values
load_dotenv()

environment = dotenv_values()

bot_token = environment['BOT_TOKEN']
admins = [int(i) for i in environment['ADMINS'].split(',')]
chat_id = environment['CHAT']

welcome_text = ("👋 Привет\!\n\n"
                '🤖 *Я \- Бот*, при помощи которого ты можешь узнавать __актуальное__ расписание в *МРК* на _ближайшее время_\.\n\n\n'
                '⚙️ Я имею *следующие команды:* \n\n'
                '📚 _Узнать расписание_:\n      "*/пара*", "*/расп*", "*/sch*"\n\n'
                '✅ _Напоминание о начале пары_:\n\      "*/follow*"\n\n'
                '❌ _Отключить напоминание_:\n      "*/unfollow*"\n\n\n'
                '💬 Ты *также* можешь использовать это в _личных сообщениях_, если так тебе будет *удобнее*\.\n\n'
                '||🙏 _Большая просьба \- если я не сработаю должным образом хотя бы один раз, сообщи об этом @dvbsh\._||\n')
