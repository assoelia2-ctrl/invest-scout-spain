import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk

# 1. Konfiguration
st.set_page_config(page_title="Invest-Scout Pro 2026", layout="wide")

# API Setup mit Fehlerprüfung
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # Wir nutzen 'gemini-1.5-flash', da es am stabilsten verfügbar ist
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Verbindung zum KI-Gehirn fehlgeschlagen: {e}")
    st.stop()

# 2. KI-Funktion
def ask_gemini(query, image=None):
    try:
        content = [f"Du bist ein Immobilien-Agent. Analysiere für 2026: {query}"]
        if image:
            content.append(image)
        response = model.generate_content(content)
        return response.text
    except Exception as e:
        return f"Die KI hat gerade Funkstille. Fehler: {e}"

# 3. Das Dashboard Layout
st.title("🏢 Invest-Scout Pro: Agenten-Zentrale")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🔍 Analyse-Auftrag")
    query = st.text_area("Befehl", placeholder="Suche Penthouse in Malaga...", height=100)
    file = st.file_uploader("Foto hochladen", type=["jpg", "png", "jpeg"])
    
    if st.button("🚀 Agenten-Analyse starten", use_container_width=True):
        if query:
            with st.spinner("KI scannt den Markt..."):
                img = Image.open(file) if file else None
                st.session_state.last_result = ask_gemini(query, img)
        else:
            st.warning("Bitte Befehl eingeben.")

with col_right:
    st.subheader("📍 Markt-Hotspots")
    
    # Sicherer Karten-Datensatz
    df = pd.DataFrame({
        'lat': [36.72, 39.46, 40.41, 41.38, 39.57],
        'lon': [-4.42, -0.37, -3.70, 2.17, 2.65]
    })

    # Karte ohne Mapbox-Abhängigkeit
    st.pydeck_chart(pdk.Deck(
        map_style=None, # Verhindert "Missing Token" Fehler
        initial_view_state=pdk.ViewState(
            latitude=40.0, longitude=-3.7, zoom=5, pitch=45
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[lon, lat]',
                get_color='[197, 255, 0, 200]',
                get_radius=30000,
            ),
        ],
    ))

# Ergebnisse unterhalb
if 'last_result' in st.session_state:
    st.divider()
    st.markdown("### 📩 Ergebnisbericht")
    st.info(st.session_state.last_result)
