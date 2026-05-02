import requests
import os
import hashlib

# Константы
URL = "https://raw.githubusercontent.com/Wuang26/Kaorios-Toolbox/refs/heads/main/Toolbox-data/Keybox.xml"
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HASH_FILE = "last_hash.txt"
MSG_ID_FILE = "last_msg_id.txt"
CAPTION = "Keybox 🟢🟢🟢"

def get_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def delete_old_message():
    """Удаляет предыдущее сообщение, если его ID сохранен."""
    if os.path.exists(MSG_ID_FILE):
        with open(MSG_ID_FILE, "r") as f:
            old_msg_id = f.read().strip()
        
        if old_msg_id:
            del_url = f"https://api.telegram.org/bot{TOKEN}/deleteMessage"
            # Пробуем удалить. Если сообщения нет или оно слишком старое, TG вернет ошибку, которую мы просто игнорируем.
            requests.post(del_url, data={"chat_id": CHAT_ID, "message_id": old_msg_id})
            print(f"Попытка удаления старого сообщения ID: {old_msg_id}")

def send_document(content):
    """Удаляет старое сообщение и отправляет новое, сохраняя его ID."""
    delete_old_message()

    filename = "Keybox.xml"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    send_url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
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
  
