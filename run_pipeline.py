import json
from engine import SOWEngine

def run():
    engine = SOWEngine()
    
    try:
        with open('matches.json', 'r', encoding='utf-8') as f:
            matches = json.load(f)
    except FileNotFoundError:
        print("Файл matches.json не найден.")
        return

    updated_matches = []
    for match in matches:
        # Проверяем, есть ли введенная статистика для матча
        if "stats" in match and match["stats"]["home"]["xg"] is not None:
            home_s = match["stats"]["home"]
            away_s = match["stats"]["away"]
            
            # Прогоняем через наш движок SOW-X
            prediction = engine.predict_match(home_s, away_s)
            
            # Сохраняем результаты в структуру матча
            match["prediction"] = {
                "lambda_home": prediction["lambda_home"],
                "lambda_away": prediction["lambda_away"],
                "most_likely_score": prediction["most_likely_score"],
                "probabilities": prediction["probabilities"]
            }
        
        updated_matches.append(match)

    # Сохраняем обновленный файл (можно выгрузить обратно)
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(updated_matches, f, ensure_ascii=False, indent=4)
    
    print("Пайплайн SOW-X успешно выполнен, прогнозы обновлены!")

if __name__ == "__main__":
    run()
