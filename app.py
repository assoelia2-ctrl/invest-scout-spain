import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
import datetime
import re

# 1. SETUP
st.set_page_config(page_title="Málaga Invest Pro", layout="wide")

# 2. DIE MANUELLE API-SCHNITTSTELLE (KEIN V1BETA MEHR!)
api_key = st.secrets.get("GEMINI_API_KEY")

def call_gemini_manual(prompt):
    # Wir bauen die URL von Hand für die stabile v1 Version
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Fehler: {response.status_code} - {response.text}"

# Historie-Speicher
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. DAS DASHBOARD
st.title("🤖 Málaga Invest-Scout Pro")
t1, t2, t3 = st.tabs(["🔍 Analyse", "⚖️ Portfolio", "📍 Karte"])

with t1:
    query = st.text_input("Was suchst du?", placeholder="Finca in Málaga...")
    budget = st.slider("Budget (€)", 50000, 1000000, 300000)
    
    if st.button("🚀 Analyse starten", use_container_width=True):
        if not api_key:
            st.error("API Key fehlt!")
        else:
            try:
                with st.spinner("KI berechnet Investment..."):
                    bericht = call_gemini_manual(f"Analysiere: {query}. Budget {budget}€. SCORE: [1-10]")
                    
                    # Score finden
                    score_match = re.search(r"SCORE:\s*(\d+)", bericht)
                    score = score_match.group(1) if score_match else "N/A"
                    
                    st.session_state.history.append({"Datum": datetime.date.today(), "Suche": query, "Score": score})
                    st.success(f"Analyse abgeschlossen! (Score: {score}/10)")
                    st.markdown(bericht)
                    st.divider()
                    st.link_button("🏠 Zu Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}")
            except Exception as e:
                st.error(f"Kritischer Fehler: {e}")

with t2:
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 Als CSV exportieren", df.to_csv(index=False).encode('utf-8'), "invest.csv")
    else:
        st.info("Noch keine Daten vorhanden.")

with t3:
    st.subheader("📍 Hotspots")
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10)
    st.pydeck_chart(pdk.Deck(initial_view_state=view, layers=[pdk.Layer('ScatterplotLayer', data=pd.DataFrame({'lat':[36.72], 'lon':[-4.42]}), get_position='[lon, lat]', get_radius=1000, get_color='[200, 30, 0]')]))
