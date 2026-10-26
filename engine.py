import math

class SOWEngine:
    def __init__(self):
        # Базовый коэффициент домашнего поля
        self.HOME_ADVANTAGE = 1.10
        
    def calculate_lambda(self, home_stats, away_stats):
        """
        Рассчитывает ожидаемые голы (lambda) для хозяев и гостей 
        на основе xG, владения, ударов в створ и фолов (хаоса).
        """
        # 1. Фундаментальный xG-ориентир (база)
        lambda_h0 = (home_stats.get('xg_f', 1.5) + away_stats.get('xg_a', 1.2)) / 2
        lambda_a0 = (away_stats.get('xg_f', 1.2) + home_stats.get('xg_a', 1.5)) / 2
        
        # 2. Модификатор контроля (Владение мячом, норма = 50%)
        home_poss = home_stats.get('possession', 50)
        away_poss = away_stats.get('possession', 50)
        
        # Если владение выше 50%, получаем бонус к давлению, если ниже — штраф
        control_h = max(0.85, min(1.15, 1.0 + (home_poss - 50) * 0.003))
        control_a = max(0.85, min(1.15, 1.0 + (away_poss - 50) * 0.003))
        
        # 3. Модификатор ударов в створ (SoT, норма для топ-уровня ~ 4-5)
        home_sot = home_stats.get('sot', 4)
        away_sot = away_stats.get('sot', 4)
        sot_mod_h = 1.0 + (home_sot - 4) * 0.03
        sot_mod_a = 1.0 + (away_sot - 4) * 0.03
        
        # 4. Модификатор хаоса и грубости (Фолы, норма ~ 11 за матч)
        home_fouls = home_stats.get('fouls', 11)
        away_fouls = away_stats.get('fouls', 11)
        
        chaos_h = 1.0 - max(0, (home_fouls - 11) * 0.02)
        chaos_a = 1.0 - max(0, (away_fouls - 11) * 0.02)
        
        # 5. Сборка итоговых лямбд с учетом фактора поля
        lambda_h = lambda_h0 * control_h * sot_mod_h * chaos_h * self.HOME_ADVANTAGE
        lambda_a = lambda_a0 * control_a * sot_mod_a * chaos_a
        
        # Ограничиваем разумными пределами футбола
        return round(max(0.2, lambda_h), 2), round(max(0.2, lambda_a), 2)

    def poisson_probability(self, lmbda, k):
        """Классическое распределение Пуассона для k голов."""
        return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

    def predict_match(self, home_stats, away_stats):
        """Строит матрицу вероятностей и находит наиболее вероятный счет."""
        lam_h, lam_a = self.calculate_lambda(home_stats, away_stats)
        
        score_matrix = {}
        max_prob = -1
        most_likely_score = "0:0"
        
        p_home_win = 0
        p_draw = 0
        p_away_win = 0
        
        # Просчитываем сетку счетов от 0:0 до 6:6
        for h in range(7):
            for a in range(7):
                prob = self.poisson_probability(lam_h, h) * self.poisson_probability(lam_a, a)
                score_matrix[f"{h}:{a}"] = prob
                
                if h > a:
                    p_home_win += prob
                elif h == a:
                    p_draw += prob
                else:
                
                    p_away_win += prob
                    
                if prob > max_prob:
                    max_prob = prob
                    most_likely_score = f"{h}:{a}"
                    
        return {
            "lambda_home": lam_h,
            "lambda_away": lam_a,
            "most_likely_score": most_likely_score,
            "probabilities": {
                "home_win": round(p_home_win * 100, 1),
                "draw": round(p_draw * 100, 1),
                "away_win": round(p_away_win * 100, 1)
            }
        }
