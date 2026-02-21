import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk
import datetime
import re

# 1. Initiale Konfiguration
st.set_page_config(page_title="Invest-Scout: Málaga Pro", layout="wide", page_icon="🏢")

# API Setup
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # Automatischer Modell-Check
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_name = next((m for m in available_models if 'gemini-1.5-flash' in m), available_models[0])
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"KI-Verbindungsproblem: {e}")
    st.stop()

# Session State initialisieren
if 'visit_history' not in st.session_state:
    st.session_state.visit_history = []

# 2. Erweiterte Agenten-Logik für Scoring
def run_scored_ai(query, image=None):
    instruction = """
    Du bist ein Immobilien-Analyst. Analysiere das Objekt/Bild.
    WICHTIG: Gib am Ende deiner Antwort IMMER folgende Werte im Format an:
    SCORE: [Zahl 1-10]
    RENDITE: [Prozentwert]
    RISIKO: [Niedrig/Mittel/Hoch]
    """
    content = [instruction, query]
    if image:
        content.append(image)
    
    response = model.generate_content(content)
    text = response.text
    
    # Extrahiere Werte für die Tabelle
    try:
        score = re.search(r"SCORE:\s*(\d+)", text).group(1)
        rendite = re.search(r"RENDITE:\s*([\d,.]+%?)", text).group(1)
        risiko = re.search(r"RISIKO:\s*(\w+)", text).group(1)
    except:
        score, rendite, risiko = "N/A", "N/A", "N/A"
        
    return text, score, rendite, risiko

# 3. Benutzeroberfläche
st.title("🤖 Invest-Scout Pro: Málaga Dashboard")

tabs = st.tabs(["📋 Neue Besichtigung", "⚖️ Investment-Vergleich", "📍 Regionale Karte"])

# TAB 1: BESICHTIGUNG & INPUT
with tabs[0]:
    st.subheader("📸 Objekt-Check vor Ort")
    obj_name = st.text_input("Name des Objekts", placeholder="Finca Almáchar...")
    inspect_file = st.file_uploader("Foto hochladen (Mängel-Check)", type=["jpg", "png", "jpeg"])
    note = st.text_area("Eigene Notizen / Fragen", "Wie hoch ist das Risiko wegen des AFO?")

    if st.button("🚀 Analyse & Bewerten", use_container_width=True):
        with st.spinner("Agent berechnet Score..."):
            img = Image.open(inspect_file) if inspect_file else None
            bericht, score, rendite, risiko = run_scored_ai(note, img)
            
            st.session_state.visit_history.append({
                "Datum": datetime.date.today().strftime("%d.%m.%Y"),
                "Objekt": obj_name,
                "Score": score,
                "Rendite": rendite,
                "Risiko": risiko,
                "Bericht": bericht
            })
            st.success(f"Analyse abgeschlossen! Score: {score}/10")
            st.markdown(bericht)

# TAB 2: VERGLEICHSTABELLE
with tabs[1]:
    st.subheader("⚖️ Ranking deiner Favoriten")
    if st.session_state.visit_history:
        df = pd.DataFrame(st.session_state.visit_history)
        # Tabelle anzeigen (ohne den langen Berichtstext)
        st.dataframe(df[["Score", "Objekt", "Rendite", "Risiko", "Datum"]].sort_values(by="Score", ascending=False), use_container_width=True)
        
        selected = st.selectbox("Detail-Bericht öffnen:", df["Objekt"].tolist())
        st.info(next(item["Bericht"] for item in st.session_state.visit_history if item["Objekt"] == selected))
    else:
        st.write("Noch keine Daten vorhanden.")

# TAB 3: KARTE
with tabs[2]:
    st.subheader("📍 Standort-Übersicht")
    map_df = pd.DataFrame({'lat': [36.72], 'lon': [-4.42]})
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=9, pitch=45),
        layers=[pdk.Layer('ScatterplotLayer', data=map_df, get_position='[lon, lat]', get_color='[197, 255, 0]', get_radius=5000)]
    ))
