import sqlite3 as sqlite
from os import system, name
from telethon import TelegramClient

def clear():
    if name == 'nt':
        _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def find_bot(telephone):
    try:
        connect = sqlite.Connection("ParsedAccounts.db")
        cur = connect.cursor()
        cur.execute(f"SELECT ID FROM Bots WHERE Telephone = {telephone}")
        ids = cur.fetchone()[0]
        if ids is not None:
            return ids
        else:
            return -1
    except Exception as e:
        print(f"Ошибка {str(e)}.")


def add_new_bots(telephone, api_id, api_hash, session):
    try:
        connect = sqlite.Connection("ParsedAccounts.db")
        cur = connect.cursor()
        cur.execute("""Insert Into RegistredBots(Phone, API_ID, API_HASH, Session) VALUES (?, ?, ?, ?);""",
                    (telephone, api_id, api_hash, session))
        connect.commit()
        cur.execute(f"DELETE FROM Bots WHERE Telephone = {telephone}")
        connect.commit()
        print("Аккаунт перемещен в таблицу RegistredBots")
    except Exception as e:
        print(f"Ошибка {str(e)}.")



print("Введите телефон: ")
telephone = input()
print("Введите API_ID: ")
api_id = input()
print("Введите API_HASH: ")
api_hash = input()
id = find_bot(telephone)
if id != -1:
    while True:
        i = 0
        connect = sqlite.Connection("ParsedAccounts.db")
        cur = connect.cursor()
        session = f"anon{id+i}"
        cur.execute(f"SELECT Session FROM RegistredBots WHERE Session = '{session}'")
        sess_name = cur.fetchone()
        if sess_name is not None:
            print(f"Сессия anon{id+i} уже существует")
            i += 1
        else:
            break

    client = TelegramClient(session, api_id, api_hash)
    client.start()
    print("Успешно!")
    add_new_bots(telephone, api_id, api_hash, session)
else:
    print("Телефон не найдет в таблице Bots")

#TODO Отформатировать код.
#TODO Перевести на PostgreSQL