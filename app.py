import streamlit as st
import google.generativeai as genai
from google.generativeai import types
import pandas as pd
import pydeck as pdk
import datetime
import re

# SETUP
st.set_page_config(page_title="Málaga Invest Pro", layout="wide")

# API FIX: Wir erzwingen die API-Version 'v1'
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Dieser Teil ist neu und schaltet den v1beta-Pfad hart ab
    genai.configure(api_key=api_key, transport='rest')
    # Wir erstellen den Client explizit für das Modell
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key fehlt!")
    st.stop()

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🤖 Invest-Scout: Málaga")

t1, t2, t3 = st.tabs(["🔍 Analyse", "⚖️ Portfolio", "📍 Karte"])

with t1:
    query = st.text_input("Suche", placeholder="Finca in Málaga...")
    budget = st.slider("Budget (€)", 50000, 1000000, 300000)
    
    if st.button("🚀 Strategie-Check starten"):
        try:
            # Wir senden die Anfrage explizit ohne Beta-Parameter
            response = model.generate_content(f"Immo-Check Málaga: {query}, Budget {budget}€. Ende mit SCORE: [1-10]")
            
            score = re.search(r"SCORE:\s*(\d+)", response.text).group(1) if "SCORE:" in response.text else "N/A"
            st.session_state.history.append({"Datum": datetime.date.today(), "Suche": query, "Score": score})
            
            st.success("Analyse fertig!")
            st.markdown(response.text)
            
            st.divider()
            st.link_button("🏠 Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}")
        except Exception as e:
            st.error(f"Fehler: {e}")

with t2:
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)
        st.download_button("📥 Export CSV", df.to_csv(index=False).encode('utf-8'), "invest.csv")

with t3:
    st.subheader("📍 Markt-Hotspots")
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10),
        layers=[pdk.Layer('ScatterplotLayer', data=pd.DataFrame({'lat':[36.72], 'lon':[-4.42]}), get_position='[lon, lat]', get_radius=1000, get_color='[200, 30, 0]')]
    ))
