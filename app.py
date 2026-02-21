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

# 2. STABILER API-SETUP (Behebt den 404-Fehler aus deinen Screenshots)
# Wir suchen nach dem Key in deinen Secrets
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # 'transport=rest' ist die sicherste Methode gegen 404/v1beta Fehler
        genai.configure(api_key=api_key, transport='rest')
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Verbindungsfehler: {e}")
        st.stop()
else:
    st.warning("Kein API Key gefunden. Bitte in den Streamlit Secrets hinterlegen.")
    st.stop()

# Speicher für deine Suchen (Portfolio)
if 'visit_history' not in st.session_state:
    st.session_state.visit_history = []

# 3. KI-AGENT LOGIK
def run_expert_ai(query, image=None):
    instruction = """Du bist Senior-Immobilien-Analyst für Málaga 2026. 
    Analysiere das Investment präzise.
    Beende deine Antwort IMMER exakt mit diesem Format für das Portfolio:
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
        
        # Daten-Extraktion für die Tabelle
        score = re.search(r"SCORE:\s*(\d+)", text).group(1) if re.search(r"SCORE:\s*(\d+)", text) else "N/A"
        rendite = re.search(r"RENDITE:\s*([\d,.]+%?)", text).group(1) if re.search(r"RENDITE:\s*([\d,.]+%?)", text) else "N/A"
        risiko = re.search(r"RISIKO:\s*(\w+)", text).group(1) if re.search(r"RISIKO:\s*(\w+)", text) else "N/A"
        max_p = re.search(r"MAX-PREIS:\s*(.*)", text).group(1) if re.search(r"MAX-PREIS:\s*(.*)", text) else "N/A"
        
        return text, score, rendite, risiko, max_p
    except Exception as e:
        return f"Fehler bei der Generierung: {e}", "N/A", "N/A", "N/A", "N/A"

# 4. DAS DASHBOARD (UI)
st.title("🤖 Invest-Scout Pro: Málaga Dashboard")

tabs = st.tabs(["🔍 Analyse & Suche", "⚖️ Mein Portfolio", "📍 Hotspot-Karte"])

# --- TAB 1: ANALYSE ---
with tabs[0]:
    st.subheader("Neuen Investment-Check starten")
    search_query = st.text_input("Was suchst du?", placeholder="Z.B. Haus in Málaga mit Meerblick...")
    
    col_in, col_img = st.columns([2, 1])
    with col_in:
        budget = st.slider("Budget (€)", 50000, 2000000, 30000, step=10000)
    with col_img:
        uploaded_file = st.file_uploader("Objekt-Foto (Optional)", type=["jpg", "png", "jpeg"])

    if st.button("🚀 Markt-Analyse starten", use_container_width=True):
        if search_query:
            with st.spinner("KI scannt den Markt..."):
                img = Image.open(uploaded_file) if uploaded_file else None
                bericht, score, rendite, risiko, max_p = run_expert_ai(f"{search_query} Budget: {budget}€", img)
                
                # Speichern für Tab 2
                st.session_state.visit_history.append({
                    "Datum": datetime.date.today().strftime("%d.%m.%Y"),
                    "Objekt": search_query[:35] + "...",
                    "Anfrage_Budget": f"{budget:,} €",
                    "Score": score, "Rendite": rendite, "Risiko": risiko, "Empfehlung": max_p
                })
                
                st.success(f"Analyse fertig (Score: {score}/10)")
                st.markdown(bericht)
                
                st.divider()
                st.subheader("🔗 Live-Angebote prüfen")
                c1, c2 = st.columns(2)
                c1.link_button("🏠 Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}")
                c2.link_button("🌍 Kyero", f"https://www.kyero.com/de/malaga-provinz-immobilien-kaufen-0l3?max_price={budget}")

# --- TAB 2: PORTFOLIO & EXCEL ---
with tabs[1]:
    if st.session_state.visit_history:
        st.subheader("⚖️ Deine Analyse-Historie")
        df = pd.DataFrame(st.session_state.visit_history)
        st.dataframe(df, use_container_width=True)
        
        # EXCEL/CSV EXPORT
        csv = df.to_csv(index=False).encode('utf-8')
        col_dl, col_del = st.columns(2)
        with col_dl:
            st.download_button("📥 Als CSV herunterladen", data=csv, file_name="Malaga_Investment_Portfolio.csv", mime='text/csv')
        with col_del:
            if st.button("🗑️ Historie löschen"):
                st.session_state.visit_history = []
                st.rerun()
    else:
        st.info("Noch keine Suchen gespeichert. Starte eine Analyse im ersten Tab!")

# --- TAB 3: KARTE ---
with tabs[2]:
    st.subheader("📍 Málaga Immobilien-Region")
    # Einfache Karte von Málaga
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10)
    st.pydeck_chart(pdk.Deck(initial_view_state=view))
