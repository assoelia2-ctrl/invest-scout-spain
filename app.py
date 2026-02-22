import streamlit as st
import google.generativeai as genai
import pandas as pd
import pydeck as pdk
import datetime
import re

# 1. SEITE INITIALISIEREN
st.set_page_config(page_title="Málaga Invest Pro", layout="wide")

# 2. DER DEFINITIVE API-FIX
# Wir laden den Key und erzwingen die REST-Schnittstelle
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    # WICHTIG: transport='rest' unterbindet gRPC-Fehler
    genai.configure(api_key=api_key, transport='rest')
    
    # NEU: Wir erzwingen das Modell OHNE den automatischen Beta-Pfad
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        generation_config={"candidate_count": 1}
    )
else:
    st.error("API Key fehlt in den Secrets!")
    st.stop()

# Historie im Session State
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. DAS DASHBOARD
st.title("🤖 Málaga Invest-Scout")

tabs = st.tabs(["🔍 Analyse", "⚖️ Portfolio", "📍 Karte"])

with tabs[0]:
    query = st.text_input("Was suchst du?", placeholder="Z.B. Finca bei Málaga...")
    budget = st.slider("Budget (€)", 50000, 1000000, 300000)
    
    if st.button("🚀 Analyse starten"):
        if query:
            try:
                with st.spinner("KI kontaktiert Markt-Daten..."):
                    # Manueller Aufruf
                    response = model.generate_content(f"Analysiere: {query}. Budget {budget}€. SCORE: [1-10]")
                    
                    # Score finden
                    score = re.search(r"SCORE:\s*(\d+)", response.text).group(1) if "SCORE:" in response.text else "N/A"
                    st.session_state.history.append({"Datum": datetime.date.today(), "Suche": query, "Score": score})
                    
                    st.success(f"Analyse abgeschlossen (Score: {score})")
                    st.markdown(response.text)
                    
                    st.divider()
                    st.link_button("🏠 Zu Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}")
            except Exception as e:
                # Wir geben den Fehler detailliert aus, um zu sehen, ob v1beta wirklich weg ist
                st.error(f"Technischer Fehler: {str(e)}")
        else:
            st.warning("Bitte gib eine Suche ein.")

with tabs[1]:
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.table(df)
        st.download_button("📥 Als CSV exportieren", df.to_csv(index=False).encode('utf-8'), "invest.csv")
    else:
        st.info("Noch keine Daten.")

with tabs[2]:
    st.subheader("📍 Markt-Übersicht")
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10)
    st.pydeck_chart(pdk.Deck(initial_view_state=view, layers=[pdk.Layer('ScatterplotLayer', data=pd.DataFrame({'lat':[36.72], 'lon':[-4.42]}), get_position='[lon, lat]', get_radius=1000, get_color='[200, 30, 0]')]))
