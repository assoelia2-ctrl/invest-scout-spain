import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
import datetime

# SETUP
st.set_page_config(page_title="Málaga Invest Pro", layout="wide")

api_key = st.secrets.get("GEMINI_API_KEY")

def call_ki(prompt):
    # Wir wechseln auf 'gemini-pro', das ist die stabilste Basis-Version
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Fehler: {response.status_code}. Bitte Key prüfen."

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🤖 Málaga Invest-Scout")

tab1, tab2, tab3 = st.tabs(["🔍 Analyse", "⚖️ Portfolio", "📍 Karte"])

with tab1:
    query = st.text_input("Suche", value="Finca in Málaga")
    if st.button("🚀 Analyse starten"):
        with st.spinner("KI arbeitet..."):
            bericht = call_ki(f"Analysiere: {query}. Gib Investment-Tipps für Málaga.")
            st.session_state.history.append({"Datum": datetime.date.today(), "Suche": query})
            st.markdown(bericht)
            st.link_button("🏠 Zu Idealista", "https://www.idealista.com")

with tab2:
    if st.session_state.history:
        st.table(pd.DataFrame(st.session_state.history))

with tab3:
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10)
    st.pydeck_chart(pdk.Deck(initial_view_state=view, layers=[pdk.Layer('ScatterplotLayer', data=pd.DataFrame({'lat':[36.72], 'lon':[-4.42]}), get_position='[lon, lat]', get_radius=1000, get_color='[200, 30, 0]')]))
