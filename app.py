import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk
import datetime
import re
import os

# 1. Konfiguration & KI-Setup
st.set_page_config(page_title="Invest-Scout: Málaga Pro", layout="wide", page_icon="🏢")

# API-Verbindung mit Fallback-Logik
try:
    # Sucht erst in Secrets, dann in Umgebungsvariablen
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    elif "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        api_key = st.sidebar.text_input("Gemini API Key manuell eingeben", type="password")

    if api_key:
        genai.configure(api_key=api_key)
        # Wir nutzen das stabilste Modell direkt beim Namen
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.warning("Bitte hinterlege einen API Key in den Streamlit Secrets.")
        st.stop()
except Exception as e:
    st.error(f"KI-Verbindungsproblem: {e}")
    st.stop()

if 'visit_history' not in st.session_state:
    st.session_state.visit_history = []

# 2. KI-Agent mit Such-Logik
def run_expert_ai(query, image=None):
    instruction = """
    Du bist ein Senior-Immobilien-Analyst für Málaga, Spanien im Jahr 2026.
    Wenn der User eine Suchanfrage stellt:
    1. Analysiere das Potenzial der Region/des Budgets.
    2. Gib Tipps zur aktuellen Marktlage und rechtlichen Besonderheiten (z.B. Tourismus-Lizenzen).
    3. Erstelle am Ende IMMER dieses Kurz-Fazit:
    SCORE: [Wert 1-10]
    RENDITE: [Wert in %]
    RISIKO: [Niedrig/Mittel/Hoch]
    MAX-PREIS: [Dein empfohlener Limit-Preis in Euro]
    """
    content = [instruction, query]
    if image:
        content.append(image)
    
    response = model.generate_content(content)
    text = response.text
    
    # Daten-Extraktion mit Regex (verbesserte Fehlertoleranz)
    try:
        score = re.search(r"SCORE:\s*(\d+)", text).group(1)
        rendite = re.search(r"RENDITE:\s*([\d,.]+%?)", text).group(1)
        risiko = re.search(r"RISIKO:\s*(\w+)", text).group(1)
        max_p = re.search(r"MAX-PREIS:\s*(.*)", text).group(1)
    except:
        score, rendite, risiko, max_p = "N/A", "N/A", "N/A", "N/A"
        
    return text, score, rendite, risiko, max_p

# 3. Das Dashboard
st.title("🤖 Invest-Scout Pro: Málaga Dashboard")

tabs = st.tabs(["🔍 Live-Suche & Analyse", "⚖️ Mein Portfolio", "📍 Regionen-Karte"])

# --- TAB 1: DIE SUCHE ---
with tabs[0]:
    st.subheader("Welche Immobilie suchen wir heute?")
    search_query = st.text_input("Deine Suchanfrage", placeholder="Ich suche eine Finca in Málaga bis 250.000 Euro...")
    
    col_input, col_vision = st.columns([2, 1])
    with col_input:
        budget = st.slider("Maximales Budget (€)", 50000, 2000000, 300000, step=10000)
    with col_vision:
        uploaded_file = st.file_uploader("Optional: Foto analysieren", type=["jpg", "png", "jpeg"])

    if st.button("🚀 Markt-Analyse & Angebote finden", use_container_width=True):
        if search_query:
            with st.spinner("Agent scannt den Markt..."):
                img = Image.open(uploaded_file) if uploaded_file else None
                bericht, score, rendite, risiko, max_p = run_expert_ai(f"{search_query} Budget: {budget}€", img)
                
                # Speichern für den Vergleich
                st.session_state.visit_history.append({
                    "Datum": datetime.date.today().strftime("%d.%m.%Y"),
                    "Objekt": search_query[:30] + "...",
                    "Preis": f"{budget:,} €",
                    "Score": score,
                    "Rendite": rendite,
                    "Risiko": risiko,
                    "Max-Preis": max_p,
                    "Bericht": bericht
                })
                
                # Anzeige
                st.success(f"Analyse abgeschlossen (Score: {score}/10)")
                st.markdown(bericht)
                
                # LIVE-LINKS GENERATOR
                st.divider()
                st.subheader("🔗 Sofort zu den Live-Angeboten")
                
                l_col, r_col = st.columns(2)
                url_idealista = f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}"
                url_kyero = f"https://www.kyero.com/de/malaga-provinz-immobilien-kaufen-0l3?max_price={budget}"
                
                with l_col:
                    st.link_button("🏠 Idealista (Málaga Local)", url_idealista, use_container_width=True)
                with r_col:
                    st.link_button("🌍 Kyero (International)", url_kyero, use_container_width=True)
        else:
            st.warning("Bitte gib ein, was du suchst!")

# --- TAB 2: PORTFOLIO ---
with tabs[1]:
    if st.session_state.visit_history:
        st.subheader("⚖️ Deine Suchhistorie & Favoriten")
        df = pd.DataFrame(st.session_state.visit_history)
        st.dataframe(df[["Datum", "Score", "Objekt", "Preis", "Max-Preis", "Rendite", "Risiko"]].sort_values(by="Score", ascending=False), use_container_width=True)
        if st.button("Historie löschen"):
            st.session_state.visit_history = []
            st.rerun()
    else:
        st.info("Noch keine Suchen durchgeführt.")

# --- TAB 3: KARTE ---
with tabs[2]:
    st.subheader("📍 Málaga Immobilien-Hotspots")
    # Fokus auf Málaga Stadt und Umland
    view = pdk.ViewState(latitude=36.7212, longitude=-4.4214, zoom=10, pitch=45)
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view, 
        layers=[
            pdk.Layer(
                'ScatterplotLayer', 
                data=pd.DataFrame({'lat':[36.7212],'lon':[-4.4214]}), 
                get_position='[lon, lat]', 
                get_color='[255, 75, 75, 160]', 
                get_radius=2000
            )
        ]
    ))
