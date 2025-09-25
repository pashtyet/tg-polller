import os
import time
import requests

TOKEN = "8107121115:AAHIKF5ks6QPrsH7ZbxL2xK-dQkbMiMCKGA"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
session = requests.Session()

def main():
    offset = None
    
    while True:
        try:
            # Формируем параметры запроса
            params = {"timeout": 30}
            if offset is not None:
                params["offset"] = offset
            
            # Выполняем запрос getUpdates
            response = session.get(f"{BASE_URL}/getUpdates", params=params)
            response.raise_for_status()
            
            data = response.json()
            if not data.get("ok"):
                print("API Error:", data.get("description"))
                time.sleep(1)
                continue
            
            updates = data["result"]
            if not updates:
                continue
            
            # Обрабатываем каждый апдейт
            max_update_id = 0
            for update in updates:
                update_id = update["update_id"]
                max_update_id = max(max_update_id, update_id)
                
                # Извлекаем chat_id только для текстовых сообщений
                message = update.get("message")
                if not message:
                    continue
                    
                chat_id = message.get("chat", {}).get("id")
                text = message.get("text")
                if not chat_id or not text:
                    continue
                
                print(f"Обработал апдейт с айди {update_id}")
                
                # Отправляем ответ
                session.post(
                    f"{BASE_URL}/sendMessage",
                    json={"chat_id": chat_id, "text": text}
                )
            
            # Обновляем offset
            offset = max_update_id + 1
            
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            time.sleep(1)
        except KeyboardInterrupt:
            print("\nЗавершение работы")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()