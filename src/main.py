from aiogram import Bot, Dispatcher, executor, types
import re


# Объект бота
bot_user = Bot(token="5986102792:AAH2yOoYEsgMctoerx6ajQh3xAU1zKi9eZI")
# Диспетчер для бота
dp = Dispatcher(bot_user)
# Включаем логирование, чтобы не пропустить важные сообщения


def phone_validation(x):
    return re.fullmatch(r'[+]?[78]\(?\d{3}\)?\-?\d{3}\-?\d{2}\-?\d{2}', x) is not None

def ready_validation(x):
    return re.fullmatch(r'[гГ]ото(в|ва)\n\d{2}.\d{2}.\d{4}', x) is not None


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]
                    

def validation(message):
    mes_arr = message.split('\n')
    if(len(mes_arr) != 6):
        return False, "Неправильный формат\nСверьтесь с примером"
    if phone_validation(mes_arr[2].lower()) is False:
        return False, "Неправильный формат телефона\nФормат:\n+7(999)999-99-99\n89999999999"
    return True, "Принято"


def add_record(id, user, message):
    with open("src/all_answers.csv", 'a', encoding="utf-8") as file:
        file.write(",".join([id, user] + message) + "\n")

    with open("src/is_ready.csv", 'a', encoding="utf-8") as file:
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

    ready_users = {}
    with open("src/is_ready.csv", 'r', encoding="utf-8") as file:
        for line in file.readlines():
            try:
                x, y = line.strip().split(',')
            except ValueError:
                print("[NOT CORRECT FORMAT]", line.strip())
                continue
            ready_users[x] = y

    s = ["Список пользователей:\n"]
    
    users = []
    all_users = []
    with open("src/all_answers.csv", 'r', encoding="utf-8") as file:
        rows = file.readlines()
        for i in range(len(rows) - 1, -1, -1):
            row = rows[i].strip().split(',')
            if row[0] in users:
                continue
            users.append(row[0])
            all_users.append([row[0], row[1], row[0] in ready_users] + row[2:])

    all_users.sort(key=lambda x: x[1])
    for user in all_users:
        if user[2]:
            s.append(" | ".join([user[1], "Готов"] + user[3:] + [ready_users[user[0]]] + ["\n"]))
        else:
            s.append(" | ".join([user[1], "Не готов"] + user[3:] + ["\n"]))

    s.append(f"\nКолличество учатсников: %d" % len(all_users))
    a_chunks = list(divide_chunks(s, 20))
    for el in a_chunks:
        await message.reply("\n".join(el))


@dp.message_handler(commands="check")
async def start_check(message: types.Message):

    whitelist = ["808547261", "771943260", "1029341343", "508893221", "588558797"]
    
    if not str(message.from_id) in whitelist:
        await message.reply("Ошибка Доступа")
        return

    with open("src/all_answers.csv", 'r', encoding="utf-8") as file:
        all_users = list(map(lambda x: x.strip().split(',')[0], file.readlines()))

    with open("src/is_ready.csv", 'w', encoding="utf-8") as file:
        pass

    users = []
    for row in all_users:
        if row in users:
            continue
        await bot_user.send_message(int(row), f"Привет, мы решили проверить твою готовность участвовать на меро\nЕсли да то нам нужно знать дату твоего рождения\nДля проверки напиши в ответном сообщении готов(-а) и введи дату рождения\n\nПример: \nГотов\n08.08.2003")
        users.append(row)


@dp.message_handler(commands="mem")
async def mem_user(message: types.Message):
    
    flag = True
    with open("src/mem.csv", 'a', encoding="utf-8") as file_mem:
        with open("src/all_answers.csv", 'r', encoding="utf-8") as file:
            lines = file.readlines()
            for i in range(len(lines) - 1, -1, -1):
                data = lines[i].strip().split(',')
                if data[0] == str(message.from_id):
                    file_mem.write(",".join(data[:5]) + "\n")
                    await message.reply("Молодец)")
                    flag = False
                    break
    if flag:
        await message.reply("М-да.......")
    

@dp.message_handler(commands="mem_admin")
async def mem_user(message: types.Message):
    whitelist = ["808547261", "771943260", "1029341343", "508893221", "588558797"]
    
    if not str(message.from_id) in whitelist:
        await message.reply("Ошибка Доступа")
        return

    s = ["Мем:\n"]
    user = []
    with open("src/mem.csv", 'r', encoding="utf-8") as file:
        lines = file.readlines()
        for i in range(len(lines) - 1, -1, -1):
            data = lines[i].strip().split(',')
            if data[0] in user:
                continue
            s.append(" | ".join(data[1:]))
            user.append(data[0])
    a_chunks = list(divide_chunks(s, 20))
    for el in a_chunks:
        await message.reply("\n".join(el))



@dp.message_handler()
async def any_text_message2(message: types.Message):
    if ready_validation(message.text):
        await message.reply("Спасибо за ответ!")
        
        with open("src/is_ready.csv", 'a', encoding="utf-8") as file:
            file.write(','.join([str(message.from_id), message.text.split("\n")[1]]) + "\n")
    
        return

    status, mes = validation(message.text)
    await message.answer(mes)
    if status:
        id = str(message.from_id)
        try:
            username = '@' + message.from_user["username"]
        except:
            username = '@' + id
        mess = message.text.replace(",", " ").split('\n')
        add_record(id, username, mess)


def run():
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)