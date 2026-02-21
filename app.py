import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk

# 1. Konfiguration
st.set_page_config(page_title="Invest-Scout Pro 2026", layout="wide")

# API Setup mit automatischer Modell-Prüfung
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # KORREKTUR: Wir nutzen den stabilen Namen 'gemini-1.5-flash-latest'
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"KI-Verbindungsproblem: {e}")
    st.stop()

# 2. KI-Funktion (Agenten-Gehirn)
def ask_gemini(query, image=None):
    try:
        # Instruktion für den Agenten
        instruction = "Du bist ein Immobilien-Experte. Scanne den Markt und gib Investitions-Tipps für 2026."
        content = [instruction, f"Kunden-Anfrage: {query}"]
        
        if image:
            content.append(image)
            
        response = model.generate_content(content)
        return response.text
    except Exception as e:
        return f"Agenten-Fehler: {e}. Tipp: Überprüfe, ob dein API-Key für Gemini 1.5 Flash freigeschaltet ist."

# 3. Das Dashboard Layout
st.title("🤖 Invest-Scout Pro: Agenten-Zentrale")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🔍 Analyse-Auftrag")
    query = st.text_area("Befehl an den Agenten", placeholder="Suche Penthouse in Malaga...", height=120)
    file = st.file_uploader("Objekt-Foto hochladen", type=["jpg", "png", "jpeg"])
    
    if st.button("🚀 Agenten beauftragen", use_container_width=True):
        if query:
            with st.spinner("KI-Agent durchsucht das Netz..."):
                img = Image.open(file) if file else None
                st.session_state.last_result = ask_gemini(query, img)
        else:
            st.warning("Bitte gib eine Anfrage ein.")

with col_right:
    st.subheader("📍 Markt-Hotspots")
    
    # Karte (jetzt funktionsfähig)
    df = pd.DataFrame({
        'lat': [36.72, 39.46, 40.41, 41.38, 39.57],
        'lon': [-4.42, -0.37, -3.70, 2.17, 2.65]
    })

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=36.72, longitude=-4.42, zoom=7, pitch=45
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[lon, lat]',
                get_color='[197, 255, 0, 160]',
                get_radius=10000,
            ),
        ],
    ))

# Ergebnisanzeige
if 'last_result' in st.session_state:
    st.divider()
    st.markdown("### 📩 Ergebnisbericht")
    # Hier wird das Ergebnis in einer schönen Box angezeigt
    st.info(st.session_state.last_result)
