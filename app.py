import streamlit as st
import google.generativeai as genai
import pandas as pd
import pydeck as pdk
import datetime
import re

# 1. SETUP
st.set_page_config(page_title="Invest-Scout Málaga", layout="wide")

# 2. DER DEFINITIVE API-FIX (Umgeht v1beta Fehler)
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Wir konfigurieren die API und erzwingen REST statt gRPC
    genai.configure(api_key=api_key, transport='rest')
    # WICHTIG: Wir definieren das Modell OHNE 'models/' Präfix, um den Pfad-Fehler zu vermeiden
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key fehlt in den Secrets!")
    st.stop()

if 'history' not in st.session_state:
    st.session_state.history = []

# 3. UI STRUKTUR
st.title("🤖 Málaga Invest-Scout Pro")
t1, t2, t3 = st.tabs(["🔍 Analyse", "⚖️ Portfolio", "📍 Karte"])

with t1:
    query = st.text_input("Suche", placeholder="Finca bei Málaga...")
    budget = st.slider("Budget (€)", 50000, 1000000, 300000)
    
    if st.button("🚀 Markt-Analyse starten", use_container_width=True):
        if query:
            try:
                with st.spinner("KI kontaktiert Markt-Daten..."):
                    # Wir nutzen eine einfache Anfrage ohne komplexe Parameter
                    response = model.generate_content(f"Analysiere: {query}. Budget: {budget} Euro. Gib Investment-Tipps und am Ende SCORE: [1-10]")
                    
                    # Score extrahieren
                    score = re.search(r"SCORE:\s*(\d+)", response.text).group(1) if "SCORE:" in response.text else "N/A"
                    st.session_state.history.append({"Datum": datetime.date.today(), "Suche": query, "Score": score})
                    
                    st.success(f"Analyse abgeschlossen! (Score: {score})")
                    st.markdown(response.text)
                    st.divider()
                    st.link_button("🏠 Angebote auf Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}")
            except Exception as e:
                st.error(f"Technischer Fehler: {e}")
                st.info("Falls hier '404' steht, musst du die App in Streamlit löschen und neu erstellen.")

with t2:
    if st.session_state.history:
        st.subheader("Deine Analysen")
        df = pd.DataFrame(st.session_state.history)
        st.table(df)
        st.download_button("📥 Als CSV exportieren", df.to_csv(index=False).encode('utf-8'), "portfolio.csv")
    else:
        st.info("Noch keine Daten vorhanden.")

with t3:
    st.subheader("📍 Standort-Vorschau")
    # Einfache Karte von Málaga
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10)
    st.pydeck_chart(pdk.Deck(initial_view_state=view, layers=[pdk.Layer('ScatterplotLayer', data=pd.DataFrame({'lat':[36.72], 'lon':[-4.42]}), get_position='[lon, lat]', get_radius=1000, get_color='[200, 30, 0]')]))
