import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
import datetime

# SETUP
st.set_page_config(page_title="Málaga Invest Pro", layout="wide")

# API KEY aus Secrets laden
api_key = st.secrets.get("GEMINI_API_KEY")

def call_ki(prompt):
    # Wir nutzen die stabilste Route: gemini-pro über v1beta
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Fehler: {response.status_code}. Bitte Key prüfen."
    except Exception as e:
        return f"Verbindungsfehler: {e}"

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🤖 Málaga Invest-Scout")

# TABS FÜR DAS PORTFOLIO UND DIE KARTE
tab1, tab2, tab3 = st.tabs(["🔍 Analyse", "⚖️ Portfolio", "📍 Karte"])

with tab1:
    query = st.text_input("Deine Suchanfrage:", value="Finca in Málaga")
    if st.button("🚀 Markt-Analyse starten"):
        if not api_key:
            st.error("API Key fehlt in den Secrets!")
        else:
            with st.spinner("KI analysiert den Markt..."):
                bericht = call_ki(f"Analysiere Immobilien-Investment: {query}. Gib Tipps für Málaga.")
                st.session_state.history.append({"Datum": datetime.date.today(), "Anfrage": query})
                st.markdown(bericht)
                st.divider()
                st.link_button("🏠 Zu Idealista", "https://www.idealista.com")

with tab2:
    if st.session_state.history:
        st.subheader("Deine Such-Historie")
        st.table(pd.DataFrame(st.session_state.history))
    else:
        st.info("Noch keine Daten gespeichert.")

with tab3:
    st.subheader("📍 Hotspots")
    # Einfache Karte von Málaga
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10)
    st.pydeck_chart(pdk.Deck(
        initial_view_state=view,
        layers=[pdk.Layer('ScatterplotLayer', data=pd.DataFrame({'lat':[36.72], 'lon':[-4.42]}), get_position='[lon, lat]', get_radius=1000, get_color='[200, 30, 0]')]
    ))
