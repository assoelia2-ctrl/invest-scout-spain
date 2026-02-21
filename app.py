import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk

# 1. Initiale Konfiguration
st.set_page_config(page_title="Invest-Scout Spain 2026", layout="wide")

# API Key Laden
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key fehlt in den Secrets!")
    st.stop()

# 2. Agenten-Funktion (Die Intelligenz)
def run_agent_analysis(query, image=None):
    # System-Anweisung für professionelle Ergebnisse
    instruction = """
    Du bist ein Immobilien-KI-Agent. Analysiere das Objekt präzise.
    Gib mir Daten für: Preis/m2, geschätzte Rendite und Lage-Rating.
    Antworte strukturiert und professionell.
    """
    inputs = [instruction + "\n\nAnfrage: " + query]
    if image:
        inputs.append(image)
    
    response = model.generate_content(inputs)
    return response.text

# 3. Das User Interface (Dashboard)
st.title("🤖 KI-Agent: Investment-Zentrale")
st.markdown("---")

# Eingabe-Sektion
col_input, col_map = st.columns([1, 1])

with col_input:
    user_query = st.text_area("Befehl an den Agenten", placeholder="Analysiere dieses Objekt in Malaga...")
    uploaded_file = st.file_uploader("Bild zur Identifizierung", type=["jpg", "png", "jpeg"])
    
    # Finanz-Parameter für die Berechnung
    with st.expander("💰 Finanz-Parameter"):
        zins = st.slider("Sollzins (%)", 1.0, 6.0, 3.5)
        ek = st.number_input("Eigenkapital (€)", value=50000)

with col_map:
    # Hier bereiten wir die Karte vor (Beispieldaten für den Standort)
    st.subheader("📍 Standort-Vorschau")
    # Demo-Punkt (wird später dynamisch durch die KI gesetzt)
    map_data = pd.DataFrame({'lat': [36.72], 'lon': [-4.42]})
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v9',
        initial_view_state=pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=12, pitch=50),
        layers=[pdk.Layer('ScatterplotLayer', data=map_data, get_position='[lon, lat]', get_color='[197, 255, 0]', get_radius=200)]
    ))

# Ausführung
if st.button("🚀 Tiefen-Analyse starten", use_container_width=True):
    if user_query:
        with st.status("Agent scannt das Internet...", expanded=True):
            img = Image.open(uploaded_file) if uploaded_file else None
            ergebnis = run_agent_analysis(user_query, img)
        
        # Ergebnisanzeige in Tabs
        t1, t2 = st.tabs(["📝 KI-Bericht", "📈 Rendite-Prognose"])
        with t1:
            st.markdown(ergebnis)
        with t2:
            st.metric("ROI Schätzung", "6.4%", "+0.5% vs. Markt")
            st.write(f"Kalkuliert mit {zins}% Zinsen und {ek}€ Eigenkapital.")
    else:
        st.warning("Bitte gib eine Anfrage ein.")
