import requests

API_KEY = "945d0ff6734c5d774ca28db842c6a29a"
TELEGRAM_TOKEN = "8637941503:AAGjJRu5uPOxzheXf9jYvd1Mws2egRz_K8s"
CHAT_ID = "-1004394085948"

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("Telegram Hatası:", e)

def check_matches():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {"x-apisports-key": API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        matches = data.get("response", [])

        print(f"Taranan canlı maç sayısı: {len(matches)}")

        for m in matches:
            fixture = m.get("fixture", {})
            teams = m.get("teams", {})
            goals = m.get("goals", {})
            league = m.get("league", {})

            elapsed = fixture.get("status", {}).get("elapsed", 0)
            home_goals = goals.get("home", 0) or 0
            away_goals = goals.get("away", 0) or 0
            total_goals = home_goals + away_goals

            home_name = teams.get("home", {}).get("name", "Ev Sahibi")
            away_name = teams.get("away", {}).get("name", "Deplasman")
            league_name = league.get("name", "Lig")

            base_tempo = (elapsed * 0.22) + (total_goals * 5.5)
            if elapsed > 75 and total_goals == 0:
                base_tempo += 6
            tempo_score = round(base_tempo, 1)

            if tempo_score >= 15:
                msg = (
                    f"🔥 <b>YÜKSEK TEMPO / FİLTREYE TAKILDI!</b>\n\n"
                    f"🏆 <b>{league_name}</b>\n"
                    f"⚔️ <b>{home_name} {home_goals} - {away_goals} {away_name}</b>\n"
                    f"⏱️ Dakika: <b>{elapsed}'</b>\n"
                    f"⚡ Tempo Skoru: <b>{tempo_score}</b>"
                )
                send_telegram(msg)
    except Exception as e:
        print("API Hatası:", e)

if __name__ == "__main__":
    check_matches()
