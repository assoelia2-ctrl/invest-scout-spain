import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk
import datetime

# 1. Initiale Konfiguration
st.set_page_config(page_title="Invest-Scout Pro 2026", layout="wide", page_icon="🏢")

# API Key Laden
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key fehlt in den Streamlit Secrets!")
    st.stop()

# Session State initialisieren
if 'history' not in st.session_state:
    st.session_state.history = []

# 2. Agenten-Logik
def run_pro_analysis(query, image=None):
    instruction = "Du bist ein Senior-Immobilienanalyst für Spanien. Analysiere präzise Preise, Renditen und Standorte für 2026."
    inputs = [instruction + "\n\nAnfrage: " + query]
    if image:
        inputs.append(image)
    response = model.generate_content(inputs)
    return response.text

# 3. Benutzeroberfläche
st.title("🏢 Invest-Scout Pro: KI-Agenten-Zentrale")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🔍 Analyse-Auftrag")
    user_query = st.text_area("Befehl an den Agenten", placeholder="Suche Penthouse in Malaga...", height=150)
    uploaded_file = st.file_uploader("Objekt-Foto (Vision Engine)", type=["jpg", "png", "jpeg"])
    
    if st.button("🚀 Agenten-Analyse starten", use_container_width=True):
        if user_query:
            with st.spinner("KI-Agent scannt das Internet..."):
                img = Image.open(uploaded_file) if uploaded_file else None
                ergebnis = run_pro_analysis(user_query, img)
                st.session_state.history.append({"query": user_query, "result": ergebnis})
                st.session_state.current_result = ergebnis
        else:
            st.warning("Bitte gib eine Anfrage ein.")

with col_right:
    st.subheader("📍 Markt-Karte Spanien")
    
    # DATEN FÜR DIE KARTE (Damit sie sicher angezeigt wird)
    # Wir erstellen ein paar Fixpunkte in Spanien
    map_df = pd.DataFrame({
        'lat': [36.72, 39.46, 40.41, 41.38, 39.57],
        'lon': [-4.42, -0.37, -3.70, 2.17, 2.65],
        'name': ['Malaga', 'Valencia', 'Madrid', 'Barcelona', 'Mallorca']
    })

    # Sichtbare Karten-Konfiguration
    view_state = pdk.ViewState(
        latitude=40.0, 
        longitude=-3.7, 
        zoom=5, 
        pitch=40
    )

    layer = pdk.Layer(
        'ScatterplotLayer',
        data=map_df,
        get_position='[lon, lat]',
        get_color='[197, 255, 0, 200]', # Unser Neongrün
        get_radius=20000,
        pickable=True
    )

    # Darstellung der Karte
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style=None # Nutzt den Standard-Stil ohne Mapbox-Key
    ))

# Ergebnisanzeige unter der Karte/Eingabe
if 'current_result' in st.session_state:
    st.divider()
    st.subheader("📩 Bericht vom KI-Agenten")
    st.info(st.session_state.current_result)
