import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Canlı Maç Tempo Paneli", page_icon="⚽", layout="wide")

st.title("⚽ Canlı Futbol Maç Tempo Paneli")
st.markdown("Bu panel, API-Football üzerinden anlık canlı maçları tarar ve tempo skorlarını listeler.")

API_KEY = "945d0ff6734c5d774ca28db842c6a29a"
url = "https://v3.football.api-sports.io/fixtures"
querystring = {"live": "all"}
headers = {
    'x-rapidapi-host': 'v3.football.api-sports.io',
    'x-rapidapi-key': API_KEY
}

if st.button("🔄 Maçları Şimdi Yenile"):
    st.rerun()

with st.spinner("Canlı maçlar taranıyor..."):
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        fixtures = data.get("response", [])
        
        if not fixtures:
            st.info("Şu an oynanan canlı maç bulunmuyor.")
        else:
            match_list = []
            for match in fixtures:
                home = match["teams"]["home"]["name"]
                away = match["teams"]["away"]["name"]
                elapsed = match["fixture"]["status"]["elapsed"] or 0
                home_goals = match["goals"]["home"] if match["goals"]["home"] is not None else 0
                away_goals = match["goals"]["away"] if match["goals"]["away"] is not None else 0
                total_goals = home_goals + away_goals
                
                tempo_score = elapsed * total_goals
                
                match_list.append({
                    "Ev Sahibi": home,
                    "Deplasman": away,
                    "Skor": f"{home_goals} - {away_goals}",
                    "Dakika": f"{elapsed}'",
                    "Toplam Gol": total_goals,
                    "Tempo Skoru": tempo_score,
                    "Durum": "🔥 Yüksek Tempo" if tempo_score >= 15 else "Normal"
                })
                
            df = pd.DataFrame(match_list)
            st.dataframe(df, use_container_width=True)
            
    except Exception as e:
        st.error(f"Veri çekilirken hata oluştu: {e}")
