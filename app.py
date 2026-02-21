import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk
import datetime

# 1. Initiale Konfiguration
st.set_page_config(page_title="Invest-Scout: Málaga Pro", layout="wide", page_icon="🏠")

# API Setup
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"KI-Verbindungsproblem: {e}")
    st.stop()

# Session State für den Vergleichsspeicher initialisieren
if 'visit_history' not in st.session_state:
    st.session_state.visit_history = []

# 2. Agenten-Logik
def run_ai(query, image=None, mode="general"):
    instruction = "Du bist ein Immobilien-Experte für Málaga."
    if mode == "inspection":
        instruction = "Du bist ein Bau-Sachverständiger. Analysiere Bilder auf Mängel (Risse, Feuchtigkeit) und bewerte das Investitionsrisiko."
    
    content = [instruction + "\n\nAnfrage: " + query]
    if image:
        content.append(image)
    response = model.generate_content(content)
    return response.text

# 3. Benutzeroberfläche
st.title("🤖 Invest-Scout Pro: Málaga")

tabs = st.tabs(["🔍 Analyse", "📋 Besichtigung & Foto-Check", "⚖️ Objekt-Vergleich"])

# TAB 1: MARKT-ANALYSE
with tabs[0]:
    c1, c2 = st.columns([1, 1])
    with c1:
        query = st.text_area("Suchauftrag", "Finca bis 250k in Axarquía...")
        if st.button("🚀 Markt-Scan"):
            st.session_state.market_res = run_ai(query)
    with c2:
        df = pd.DataFrame({'lat': [36.72], 'lon': [-4.42]})
        st.pydeck_chart(pdk.Deck(map_style=None, initial_view_state=pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=9),
                                layers=[pdk.Layer('ScatterplotLayer', data=df, get_position='[lon, lat]', get_color='[197, 255, 0]', get_radius=5000)]))
    if 'market_res' in st.session_state:
        st.info(st.session_state.market_res)

# TAB 2: BESICHTIGUNG
with tabs[1]:
    st.subheader("📸 Live-Check & Speicherung")
    obj_name = st.text_input("Name/Adresse des Objekts", placeholder="z.B. Finca Almáchar")
    inspect_file = st.file_uploader("Foto hochladen", type=["jpg", "png", "jpeg"])
    
    if st.button("🧐 Analyse & Speichern"):
        with st.spinner("Sachverständiger prüft..."):
            img = Image.open(inspect_file) if inspect_file else None
            res = run_ai("Bewerte dieses Objekt/Foto", img, mode="inspection")
            
            # Objekt in Historie speichern
            st.session_state.visit_history.append({
                "Datum": datetime.date.today().strftime("%d.%m.%Y"),
                "Objekt": obj_name,
                "Bewertung": res[:150] + "...",
                "Volltext": res
            })
            st.success(f"Objekt '{obj_name}' wurde zur Vergleichsliste hinzugefügt!")
            st.markdown(res)

# TAB 3: VERGLEICH (Die neue Funktion)
with tabs[2]:
    st.subheader("⚖️ Deine Favoriten im Vergleich")
    if st.session_state.visit_history:
        comparison_df = pd.DataFrame(st.session_state.visit_history)
        st.table(comparison_df[["Datum", "Objekt", "Bewertung"]])
        
        selected_obj = st.selectbox("Wähle ein Objekt für den Detail-Bericht:", 
                                   options=[item["Objekt"] for item in st.session_state.visit_history])
        
        detail = next(item for item in st.session_state.visit_history if item["Objekt"] == selected_obj)
        st.write(f"**Vollständiges Gutachten für {selected_obj}:**")
        st.info(detail["Volltext"])
    else:
        st.write("Noch keine Objekte gespeichert. Nutze den Besichtigungs-Check!")
