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

# Session State für die Historie initialisieren
if 'history' not in st.session_state:
    st.session_state.history = []

# 2. Agenten-Logik (Erweiterte Analyse)
def run_pro_analysis(query, image=None):
    instruction = """
    Du bist ein Senior-Immobilienanalyst. 
    Untersuche das Objekt oder die Region extrem detailliert.
    STRUKTUR:
    - ZUSAMMENFASSUNG: (Max 2 Sätze)
    - INVESTMENT-DATEN: (Preisschätzung, Erwartete Rendite in %, Risiko 1-10)
    - STANDORT-CHECK: (Infrastruktur, Trends 2026)
    - BILD-ANALYSE: (Falls Bild vorhanden: Zustand, Besonderheiten)
    Gib am Ende immer eine klare EMPFEHLUNG ab.
    """
    inputs = [instruction + "\n\nAnfrage: " + query]
    if image:
        inputs.append(image)
    
    response = model.generate_content(inputs)
    return response.text

# 3. Benutzeroberfläche (Single Page Workflow)
st.title("🏢 Invest-Scout Pro: KI-Agenten-Zentrale")
st.caption(f"Status: Online | Datum: {datetime.date.today().strftime('%d.%m.%Y')}")

# Layout: Links Eingabe & Historie, Rechts Karte & Ergebnis
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("🔍 Neue Analyse")
    user_query = st.text_area("Befehl an den Agenten", placeholder="Suche Penthouse in Marbella bis 600k...", height=120)
    uploaded_file = st.file_uploader("Objekt-Foto hochladen (Vision Engine)", type=["jpg", "png", "jpeg"])
    
    with st.expander("⚙️ Experten-Filter"):
        zins = st.slider("Zinssatz (%)", 0.0, 8.0, 3.8)
        strategie = st.selectbox("Strategie", ["Maximale Rendite", "Eigennutzung", "Fix & Flip"])

    if st.button("🚀 Agenten-Analyse starten", use_container_width=True):
        if user_query:
            with st.status("Agent durchsucht das Internet & analysiert Vision-Daten...", expanded=True) as status:
                img = Image.open(uploaded_file) if uploaded_file else None
                ergebnis = run_pro_analysis(user_query, img)
                
                # In Historie speichern
                st.session_state.history.append({"query": user_query, "result": ergebnis, "date": datetime.datetime.now()})
                status.update(label="Analyse abgeschlossen!", state="complete")
            
            st.session_state.current_result = ergebnis
        else:
            st.warning("Bitte gib eine Anfrage ein.")

    # Historie-Bereich (Sidebar-Ersatz)
    if st.session_state.history:
        st.divider()
        st.subheader("📜 Letzte Analysen")
        for i, item in enumerate(reversed(st.session_state.history[-5:])):
            if st.button(f"{item['date'].strftime('%H:%M')} - {item['query'][:30]}...", key=f"hist_{i}"):
                st.session_state.current_result = item['result']

with col_right:
    # Karten-Modul
    st.subheader("📍 Regionaler Markt-Fokus")
    map_data = pd.DataFrame({'lat': [36.51, 36.72, 39.57], 'lon': [-4.88, -4.42, 2.65]}) # Beispielpunkte
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v9',
        initial_view_state=pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=6, pitch=45),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=map_data,
                get_position='[lon, lat]',
                radius=5000,
                elevation_scale=50,
                elevation_range=[0, 1000],
                extruded=True,
            ),
        ],
    ))

    # Ergebnisanzeige
    if 'current_result' in st.session_state:
        st.markdown("---")
        st.subheader("📩 Aktueller Agenten-Bericht")
        st.info(st.session_state.current_result)
        
        # Action Buttons
        c1, c2 = st.columns(2)
        with c1:
            st.button("📄 PDF Export", on_click=lambda: st.toast("Export gestartet..."))
        with c2:
            idealista_url = f"https://www.idealista.com/de/"
            st.link_button("🌐 Live-Angebote prüfen", idealista_url)
