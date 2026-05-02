import requests
import os
import hashlib

# Константы
URL = "https://raw.githubusercontent.com/Wuang26/Kaorios-Toolbox/refs/heads/main/Toolbox-data/Keybox.xml"
TOKEN = os.getenv("TELEGRAM_TOKEN")
CAPTION = "New Keybox: 🟢🟢🟢"
FILENAME = "Keybox.xml" # Теперь переменная доступна везде
HASH_FILE = "last_hash.txt"

# Список целей для отправки
TARGETS = [
    {
        "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
        "thread_id": None,
        "msg_id_file": "last_msg_id_1.txt"
    },
    {
        "chat_id": os.getenv("TELEGRAM_CHAT_ID_2"),
        "thread_id": os.getenv("TELEGRAM_THREAD_ID_2"),
        "msg_id_file": "last_msg_id_2.txt"
    }
]

def get_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def delete_old_message(target):
    if os.path.exists(target["msg_id_file"]):
        with open(target["msg_id_file"], "r") as f:
            old_msg_id = f.read().strip()
        if old_msg_id:
            del_url = f"https://api.telegram.org/bot{TOKEN}/deleteMessage"
            requests.post(del_url, data={"chat_id": target["chat_id"], "message_id": old_msg_id})

def send_to_target(target, content):
    # Удаляем старое перед отправкой нового
    delete_old_message(target)
    
    # Сохраняем файл локально
    with open(FILENAME, "w", encoding="utf-8") as f:
        f.write(content)
    
    send_url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    with open(FILENAME, "rb") as f:
        payload = {
            "chat_id": target["chat_id"],
            "caption": CAPTION,
            "parse_mode": "HTML"
        }
        # Если есть ID темы (thread_id), добавляем его
        if target["thread_id"] and target["thread_id"].strip():
            payload["message_thread_id"] = target["thread_id"]
            
        files = {"document": f}
        r = requests.post(send_url, data=payload, files=files)
        
        if r.status_code == 200:
            new_msg_id = r.json().get("result", {}).get("message_id")
            with open(target["msg_id_file"], "w") as f:
                f.write(str(new_msg_id))
            print(f"Успешно отправлено в {target['chat_id']}")
        else:
            print(f"Ошибка при отправке в {target['chat_id']}: {r.text}")

# Основная логика запуска
response = requests.get(URL)
if response.status_code == 200:
    current_content = response.text
    current_hash = get_hash(current_content)

    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            last_hash = f.read().strip()
    else:
        last_hash = ""

    if current_hash != last_hash:
        print("Найдено обновление!")
        # Проходим по всем целям
        for target in TARGETS:
            if target["chat_id"]: # Отправляем только если ID группы настроен в Secrets
                send_to_target(target, current_content)
        
        # Сохраняем новый хеш
        with open(HASH_FILE, "w") as f:
            f.write(current_hash)
    else:
        print("Изменений нет.")
else:
    print(f"Не удалось получить файл с GitHub: {response.status_code}")

def send_to_target(target, content):
    delete_old_message(target)
    
    filename = "Keybox.xml"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    send_url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    with open(filename, "rb") as f:
        payload = {
            "chat_id": target["chat_id"],
            "caption": CAPTION,
            "parse_mode": "HTML"
        }
        # Если указан thread_id, добавляем его в запрос
        if target["thread_id"]:
            payload["message_thread_id"] = target["thread_id"]
            
        files = {"document": f}
        r = requests.post(send_url, data=payload, files=files)
        
        if r.status_code == 200:
            new_msg_id = r.json().get("result", {}).get("message_id")
            with open(target["msg_id_file"], "w") as f:
                f.write(str(new_msg_id))
            print(f"Отправлено в {target['chat_id']}, тема: {target['thread_id']}")

# Логика
response = requests.get(URL)
if response.status_code == 200:
    current_content = response.text
    current_hash = get_hash(current_content)

    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            last_hash = f.read().strip()
    else:
        last_hash = ""

    if current_hash != last_hash:
        print("Обновление!")
        for target in TARGETS:
            if target["chat_id"]: # Проверяем, что ID группы вообще задан
                send_to_target(target, current_content)
        
        with open(HASH_FILE, "w") as f:
            f.write(current_hash)
    else:
        print("Изменений нет.")
    with open(filename, "rb") as f:
        payload = {
            "chat_id": CHAT_ID,
            "caption": CAPTION,
            "parse_mode": "HTML"
        }
        files = {"document": f}
        r = requests.post(send_url, data=payload, files=files)
        
        if r.status_code == 200:
            new_msg_id = r.json().get("result", {}).get("message_id")
            if new_msg_id:
                with open(MSG_ID_FILE, "w") as f:
                    f.write(str(new_msg_id))
                print(f"Новое сообщение отправлено, ID {new_msg_id} сохранен.")
        else:
            print(f"Ошибка при отправке в TG: {r.text}")

# Основная логика
response = requests.get(URL)
if response.status_code == 200:
    current_content = response.text
    current_hash = get_hash(current_content)

    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            last_hash = f.read().strip()
    else:
        last_hash = ""

    if current_hash != last_hash:
        print("Обнаружено обновление файла!")
        send_document(current_content)
        with open(HASH_FILE, "w") as f:
            f.write(current_hash)
    else:
        print("Изменений в файле нет.")
else:
    print(f"Ошибка загрузки файла с GitHub: {response.status_code}")
  
