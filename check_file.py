import requests
import os
import hashlib

# Константы
URL = "https://raw.githubusercontent.com/Wuang26/Kaorios-Toolbox/refs/heads/main/Toolbox-data/Keybox.xml"
TOKEN = os.getenv("TELEGRAM_TOKEN")
CAPTION = "New Keybox (by Kaorios Toolbox): 🟢🟢🟢"
FILENAME = "Keybox.xml"
HASH_FILE = "last_hash.txt"

# Настройки для двух групп
TARGETS = [
    {
        "name": "Группа 1 (Без темы)",
        "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
        "thread_id": None,
        "msg_id_file": "last_msg_id_1.txt"
    },
    {
        "name": "Группа 2 (С темой)",
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
    delete_old_message(target)
    
    with open(FILENAME, "w", encoding="utf-8") as f:
        f.write(content)
    
    send_url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    with open(FILENAME, "rb") as f:
        payload = {
            "chat_id": target["chat_id"],
            "caption": CAPTION,
            "parse_mode": "HTML"
        }
        # Если есть ID темы, добавляем его
        t_id = target.get("thread_id")
        if t_id and str(t_id).strip():
            payload["message_thread_id"] = t_id
            
        r = requests.post(send_url, data=payload, files={"document": f})
        
        if r.status_code == 200:
            new_id = r.json().get("result", {}).get("message_id")
            with open(target["msg_id_file"], "w") as f:
                f.write(str(new_id))
            print(f"✅ Успешно отправлено в: {target['name']}")
        else:
            print(f"❌ Ошибка TG для {target['name']}: {r.text}")

# Основной запуск
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
        print("🚀 Найдено обновление файла на GitHub!")
        for target in TARGETS:
            if target["chat_id"]: # Отправляем, только если секрет не пустой
                send_to_target(target, current_content)
        
        # Обновляем хеш после отправки
        with open(HASH_FILE, "w") as f:
            f.write(current_hash)
    else:
        print("💤 Изменений нет. Файл тот же самый.")
else:
    print(f"⚠️ Ошибка загрузки с GitHub: {response.status_code}")
    
