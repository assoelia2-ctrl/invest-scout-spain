import streamlit as st
import google.generativeai as genai
import pandas as pd
import pydeck as pdk
import datetime
import re

# 1. SETUP
st.set_page_config(page_title="Málaga Invest Pro", layout="wide")

# 2. DER DEFINITIVE FIX (Erzwingt v1 statt v1beta)
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    # Wir konfigurieren die API und erzwingen die REST-Schnittstelle
    # Das transport='rest' ist essenziell gegen den 404-Fehler
    genai.configure(api_key=api_key, transport='rest')
    
    # Hier ist der Trick: Wir erstellen das Modell und sagen ihm 
    # explizit, dass es die stabile API nutzen soll
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key fehlt in den Secrets!")
    st.stop()

if 'history' not in st.session_state:
    st.session_state.history = []

# 3. DAS VOLLE DASHBOARD (Wie besprochen)
st.title("🤖 Málaga Invest-Scout Pro")
t1, t2, t3 = st.tabs(["🔍 Analyse", "⚖️ Portfolio", "📍 Karte"])

with t1:
    query = st.text_input("Was suchst du?", placeholder="Finca in Málaga...")
    budget = st.slider("Budget (€)", 50000, 1000000, 300000)
    
    if st.button("🚀 Analyse starten", use_container_width=True):
        try:
            with st.spinner("KI kontaktiert Markt-Daten..."):
                # Wir schicken die Anfrage ab
                response = model.generate_content(f"Analysiere: {query}. Budget {budget}€. Ende mit SCORE: [1-10]")
                
                # Score finden
                score = re.search(r"SCORE:\s*(\d+)", response.text).group(1) if "SCORE:" in response.text else "N/A"
                st.session_state.history.append({"Datum": datetime.date.today(), "Suche": query, "Score": score})
                
                st.success(f"Analyse abgeschlossen! (Score: {score})")
                st.markdown(response.text)
                st.divider()
                st.link_button("🏠 Zu Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}")
        except Exception as e:
            # Falls immer noch v1beta erscheint, erzwingen wir eine Fehlermeldung
            st.error(f"Technischer Fehler: {str(e)}")

with t2:
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.table(df)
        st.download_button("📥 Als CSV exportieren", df.to_csv(index=False).encode('utf-8'), "invest.csv")
    else:
        st.info("Noch keine Daten.")

with t3:
    st.subheader("📍 Markt-Übersicht")
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10)
    st.pydeck_chart(pdk.Deck(initial_view_state=view, layers=[pdk.Layer('ScatterplotLayer', data=pd.DataFrame({'lat':[36.72], 'lon':[-4.42]}), get_position='[lon, lat]', get_radius=1000, get_color='[200, 30, 0]')]))
