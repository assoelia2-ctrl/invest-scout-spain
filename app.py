import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk
import datetime
import re
import io

# 1. SEITE INITIALISIEREN
st.set_page_config(page_title="Invest-Scout: Málaga Pro", layout="wide", page_icon="🏢")

# 2. STABILER API-SETUP (Verhindert den 404-v1beta Fehler)
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # 'transport=rest' ist stabiler in der Cloud
        genai.configure(api_key=api_key, transport='rest')
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Verbindungsfehler: {e}")
        st.stop()
else:
    st.warning("Bitte hinterlege deinen API Key in den Streamlit Secrets.")
    st.stop()

# Speicher für die Historie vorbereiten
if 'visit_history' not in st.session_state:
    st.session_state.visit_history = []

# 3. KI-LOGIK MIT ROBUSTER EXTRAKTION
def run_expert_ai(query, image=None):
    instruction = """Du bist Senior-Immobilien-Analyst für Málaga 2026. 
    Analysiere das Investment und gib Tipps zu Marktlage/Lizenzen.
    Antworte IMMER am Ende mit diesem exakten Format:
    SCORE: [1-10]
    RENDITE: [%]
    RISIKO: [Text]
    MAX-PREIS: [Euro]"""
    
    try:
        content = [instruction, query]
        if image:
            content.append(image)
        
        response = model.generate_content(content)
        text = response.text
        
        # Daten-Extraktion (Regex)
        score = re.search(r"SCORE:\s*(\d+)", text).group(1) if re.search(r"SCORE:\s*(\d+)", text) else "N/A"
        rendite = re.search(r"RENDITE:\s*([\d,.]+%?)", text).group(1) if re.search(r"RENDITE:\s*([\d,.]+%?)", text) else "N/A"
        risiko = re.search(r"RISIKO:\s*(\w+)", text).group(1) if re.search(r"RISIKO:\s*(\w+)", text) else "N/A"
        max_p = re.search(r"MAX-PREIS:\s*(.*)", text).group(1) if re.search(r"MAX-PREIS:\s*(.*)", text) else "N/A"
        
        return text, score, rendite, risiko, max_p
    except Exception as e:
        return f"Fehler bei der Generierung: {e}", "N/A", "N/A", "N/A", "N/A"

# 4. DAS DASHBOARD (UI)
st.title("🤖 Invest-Scout Pro: Málaga Dashboard")

tabs = st.tabs(["🔍 Live-Suche & Analyse", "⚖️ Mein Portfolio", "📍 Regionen-Karte"])

# --- TAB 1: SUCHE ---
with tabs[0]:
    st.subheader("Welche Immobilie suchen wir heute?")
    search_query = st.text_input("Deine Suchanfrage", placeholder="Ich suche eine Finca in Málaga bis 250.000 Euro...")
    
    col_input, col_vision = st.columns([2, 1])
    with col_input:
        budget = st.slider("Maximales Budget (€)", 50000, 2000000, 300000, step=10000)
    with col_vision:
        uploaded_file = st.file_uploader("Optional: Foto analysieren", type=["jpg", "png", "jpeg"])

    if st.button("🚀 Markt-Analyse starten", use_container_width=True):
        if search_query:
            with st.spinner("Agent scannt den Markt..."):
                img = Image.open(uploaded_file) if uploaded_file else None
                bericht, score, rendite, risiko, max_p = run_expert_ai(f"{search_query} Budget: {budget}€", img)
                
                # In Historie speichern
                st.session_state.visit_history.append({
                    "Datum": datetime.date.today().strftime("%d.%m.%Y"),
                    "Objekt": search_query[:40] + "...",
                    "Anfrage_Budget": f"{budget:,} €",
                    "Score": score,
                    "Rendite": rendite,
                    "Risiko": risiko,
                    "Max_Preis_Empfehlung": max_p
                })
                
                st.success(f"Analyse abgeschlossen (Score: {score}/10)")
                st.markdown(bericht)
                
                st.divider()
                st.subheader("🔗 Sofort zu den Live-Angeboten")
                l_col, r_col = st.columns(2)
                with l_col:
                    st.link_button("🏠 Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}", use_container_width=True)
                with r_col:
                    st.link_button("🌍 Kyero", f"https://www.kyero.com/de/malaga-provinz-immobilien-kaufen-0l3?max_price={budget}", use_container_width=True)
        else:
            st.warning("Bitte gib ein, was du suchst!")

# --- TAB 2: PORTFOLIO & EXCEL EXPORT ---
with tabs[1]:
    if st.session_state.visit_history:
        st.subheader("⚖️ Deine Suchhistorie")
        df = pd.DataFrame(st.session_state.visit_history)
        
        # Tabelle anzeigen
        st.dataframe(df.sort_values(by="Score", ascending=False), use_container_width=True)
        
        # CSV/Excel Export Funktion
        csv = df.to_csv(index=False).encode('utf-8')
        
        col_dl, col_del = st.columns(2)
        with col_dl:
            st.download_button(
                label="📥 Als Excel (CSV) herunterladen",
                data=csv,
                file_name=f"Malaga_Invest_Export_{datetime.date.today()}.csv",
                mime='text/csv',
                use_container_width=True
            )
        with col_del:
            if st.button("🗑️ Historie löschen", use_container_width=True):
                st.session_state.visit_history = []
                st.rerun()
    else:
        st.info("Noch keine Suchen durchgeführt.")

# --- TAB 3: KARTE ---
with tabs[2]:
    st.subheader("📍 Málaga Immobilien-Hotspots")
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
