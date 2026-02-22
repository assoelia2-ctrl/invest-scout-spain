import streamlit as st
import google.generativeai as genai
import pandas as pd
import pydeck as pdk
import datetime
import re

# 1. SETUP & DESIGN
st.set_page_config(page_title="Málaga Invest-Scout Pro", layout="wide")

# 2. DER DEFINITIVE FIX (Gegen 404 v1beta)
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Wir erzwingen REST und überschreiben alle fehlerhaften Standardwerte
    genai.configure(api_key=api_key, transport='rest')
    # Wir nutzen das Modell direkt ohne v1beta-Präfix
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key fehlt in den Secrets!")
    st.stop()

# Speicher für Portfolio
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. DASHBOARD
st.title("🤖 Invest-Scout: Málaga")

t1, t2, t3 = st.tabs(["🔍 KI-Analyse", "⚖️ Portfolio", "📍 Karte"])

with t1:
    query = st.text_input("Suche", placeholder="Z.B. Haus in Málaga bis 300k...")
    budget = st.slider("Budget (€)", 50000, 1000000, 300000)
    
    if st.button("🚀 Strategie-Check starten", use_container_width=True):
        if query:
            try:
                with st.spinner("KI berechnet Investment..."):
                    # Anfrage ohne Beta-Parameter
                    res = model.generate_content(f"Analysiere: {query}. Budget: {budget}€. Beende mit SCORE: [1-10].")
                    
                    # Daten extrahieren
                    score = re.search(r"SCORE:\s*(\d+)", res.text).group(1) if "SCORE:" in res.text else "N/A"
                    st.session_state.history.append({"Datum": datetime.date.today(), "Suche": query, "Score": score})
                    
                    st.success(f"Analyse fertig! (Score: {score}/10)")
                    st.markdown(res.text)
                    st.divider()
                    st.link_button("🏠 Direkt zu Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}")
            except Exception as e:
                st.error(f"Fehler: {e}")
                st.info("Falls hier immer noch '404 v1beta' steht, befolge bitte Schritt 3 (App löschen).")

with t2:
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.table(df)
        st.download_button("📥 Export CSV", df.to_csv(index=False).encode('utf-8'), "invest.csv")
    else:
        st.info("Noch keine Daten vorhanden.")

with t3:
    st.subheader("📍 Markt-Hotspots")
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10)
    st.pydeck_chart(pdk.Deck(initial_view_state=view, layers=[pdk.Layer('ScatterplotLayer', data=pd.DataFrame({'lat':[36.72], 'lon':[-4.42]}), get_position='[lon, lat]', get_radius=1000, get_color='[200, 30, 0]')]))
