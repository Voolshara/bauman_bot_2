from aiogram import Bot, Dispatcher, executor, types
import re


# Объект бота
bot_user = Bot(token="5986102792:AAH2yOoYEsgMctoerx6ajQh3xAU1zKi9eZI")
# Диспетчер для бота
dp = Dispatcher(bot_user)
# Включаем логирование, чтобы не пропустить важные сообщения


def phone_validation(x):
    return re.fullmatch(r'[+]?[78]\(?\d{3}\)?\-?\d{3}\-?\d{2}\-?\d{2}', x) is not None


def validation(message):
    mes_arr = message.split('\n')
    if(len(mes_arr) != 6):
        return False, "Неправильный формат\nСверьтесь с примером"
    if phone_validation(mes_arr[2].lower()) is False:
        return False, "Неправильный формат телефона\nФормат:\n+7(999)999-99-99\n89999999999"
    return True, "Принято"


def add_record(id, user, message):
    with open("src/all_answers.csv", 'a') as file:
        file.write(",".join([id, user] + message) + "\n")

    with open("src/is_ready.csv", 'a') as file:
        file.write(id + "\n")


# Хэндлер на команду /start
@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    # DBW.new_user(message.from_id)
    await message.reply("""Привет
Введи свои ФИО, группу, номер телефона и три песни, которые хочешь услышать
Введи ответ в шести строках

Пример:
Иванов Иванович Иван
РК6-21Б
+79999498202
GSPD Бесконечное Лето
GSPD Бесконечное Лето
GSPD Бесконечное Лето

P.S. Если хочешь поменять песни, просто отправь сообщение заново)
""")
  

@dp.message_handler(commands="get")
async def get_info(message: types.Message):
    
    whitelist = ["808547261", "771943260", "1029341343", "508893221", "588558797"]
    
    if not str(message.from_id) in whitelist:
        await message.reply("Ошибка Доступа")
        return

    with open("src/is_ready.csv", 'r') as file:
        ready_users = list(map(lambda x: x.strip(), file.readlines()))

    s = ["Список пользователей:\n"]
    
    users = []
    all_users = []
    with open("src/all_answers.csv", 'r') as file:
        rows = file.readlines()
        for i in range(len(rows) - 1, -1, -1):
            row = rows[i].strip().split(',')
            if row[0] in users:
                continue
            users.append(row[0])
            all_users.append([row[1], row[0] in ready_users] + row[2:])

    all_users.sort(key=lambda x: x[1])
    
    for user in all_users:
        s.append(" | ".join([user[0], "Готов" if user[1] else "Не готов"] + user[2:] + ["\n"]))

    s.append(f"\nКолличество учатсников: %d" % len(all_users))
    await message.reply("\n".join(s))


@dp.message_handler(commands="check")
async def start_check(message: types.Message):

    whitelist = ["808547261", "771943260", "1029341343", "508893221", "588558797"]
    
    if not str(message.from_id) in whitelist:
        await message.reply("Ошибка Доступа")
        return

    with open("src/all_answers.csv", 'r') as file:
        all_users = list(map(lambda x: x.strip().split(',')[0], file.readlines()))

    with open("src/is_ready.csv", 'w') as file:
        pass

    users = []
    for row in all_users:
        if row in users:
            continue
        await bot_user.send_message(int(row), f"Привет, мы решили проверить твою готовность участвовать на меро\nНажми  /ready  для проверки")
        users.append(row)


@dp.message_handler(commands="ready")
async def ready_user(message: types.Message):
    with open("src/is_ready.csv", 'a') as file:
        file.write(str(message.from_id) + "\n")
    await message.reply("Спасибо за уделённое время")


@dp.message_handler()
async def any_text_message2(message: types.Message):
    status, mes = validation(message.text)
    await message.answer(mes)
    if status:
        add_record(str(message.from_id), '@' + message.from_user["username"], message.text.replace(",", " ").split('\n'))


def run():
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)