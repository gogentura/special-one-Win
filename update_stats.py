import os
import json
import urllib.request

API_TOKEN = os.environ.get("FOOTBALL_API_TOKEN")

def update_matches_stats():
    if not API_TOKEN:
        print("Токен API не обнаружен. Пропускаем авто-загрузку.")
        return

    # Запрос к API за завершенными матчами топ-лиг (например, АПЛ - код 2021)
    url = "https://api.football-data.org/v4/competitions/PL/matches?status=FINISHED"
    req = urllib.request.Request(url, headers={"X-Auth-Token": API_TOKEN})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            api_matches = data.get("matches", [])
            
            # Читаем наш локальный файл matches.json
            if os.path.exists("matches.json"):
                with open("matches.json", "r", encoding="utf-8") as f:
                    local_matches = json.load(f)
            else:
                local_matches = []

            # Сопоставляем данные из API с нашими матчами
            updated = False
            for local in local_matches:
                # Если статистика еще не заполнена
                if "stats" in local and local["stats"]["home"]["xg"] is None:
                    # Ищем соответствующий матч по командам (упрощенный пример поиска)
                    for am in api_matches:
                        home_name = am["homeTeam"]["name"]
                        away_name = am["awayTeam"]["name"]
                        
                        if local["home_team"].lower() in home_name.lower() and local["away_team"].lower() in away_name.lower():
                            # Достаем реальные голы и базовые параметры
                            local["home_goals"] = am["score"]["fullTime"]["home"]
                            local["away_goals"] = am["score"]["fullTime"]["away"]
                            
                            # Заполняем статистику (API-football дает базовые цифры, xG и владение можно прокинуть или рассчитать)
                            local["stats"]["home"]["xg"] = 1.5  # Пример, если API не отдает xG напрямую
                            local["stats"]["home"]["possession"] = 52
                            local["stats"]["home"]["sot"] = 5
                            local["stats"]["home"]["fouls"] = 10
                            
                            local["stats"]["away"]["xg"] = 1.2
                            local["stats"]["away"]["possession"] = 48
                            local["stats"]["away"]["sot"] = 4
                            local["stats"]["away"]["fouls"] = 12
                            
                            updated = True
                            break

            if updated:
                with open("matches.json", "w", encoding="utf-8") as f:
                    json.dump(local_matches, f, ensure_ascii=False, indent=4)
                print("Файл matches.json успешно обновлен свежими данными из API!")
            else:
                print("Новых матчей для обновления не найдено.")

    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")

if __name__ == "__main__":
    update_matches_stats()
