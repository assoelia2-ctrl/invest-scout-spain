import streamlit as st
import google.generativeai as genai
import pandas as pd
import pydeck as pdk
import datetime
import re

# 1. SETUP & FEHLER-BLOCKER (v1 erzwingen)
st.set_page_config(page_title="Málaga Invest Pro", layout="wide")

api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    # transport='rest' ist die Versicherung gegen den 404-Fehler
    genai.configure(api_key=api_key, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key fehlt in den Secrets!")
    st.stop()

# Speicher für deine Analysen (Portfolio)
if 'history' not in st.session_state:
    st.session_state.history = []

# 2. DAS VOLLE DASHBOARD
st.title("🤖 Dein Málaga Invest-Scout")

tab1, tab2, tab3 = st.tabs(["🔍 Analyse", "⚖️ Portfolio", "📍 Karte"])

with tab1:
    st.subheader("Immobilien-Check")
    query = st.text_input("Was suchst du?", placeholder="Finca in Málaga bis 300k...")
    budget = st.slider("Budget (€)", 50000, 1000000, 300000)
    
    if st.button("🚀 Analyse starten"):
        try:
            with st.spinner("KI scannt den Markt..."):
                res = model.generate_content(f"Analysiere: {query}. Budget: {budget}€. Beende mit SCORE: [1-10].")
                score = re.search(r"SCORE:\s*(\d+)", res.text).group(1) if "SCORE:" in res.text else "N/A"
                
                st.session_state.history.append({"Datum": datetime.date.today(), "Suche": query, "Score": score})
                st.success(f"Analyse fertig! Score: {score}")
                st.markdown(res.text)
                
                st.divider()
                st.link_button("🏠 Idealista Angebote", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}")
        except Exception as e:
            st.error(f"Fehler: {e}")

with tab2:
    st.subheader("⚖️ Dein Portfolio")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 Excel/CSV Export", df.to_csv(index=False).encode('utf-8'), "investments.csv")
    else:
        st.info("Noch keine Daten.")

with tab3:
    st.subheader("📍 Standort-Vorschau")
    # Die Karte von Málaga
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10)
    st.pydeck_chart(pdk.Deck(initial_view_state=view, layers=[pdk.Layer('ScatterplotLayer', data=pd.DataFrame({'lat':[36.72], 'lon':[-4.42]}), get_position='[lon, lat]', get_radius=1000, get_color='[200, 30, 0]')]))
