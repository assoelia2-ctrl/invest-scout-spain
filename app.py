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

# 2. DER "HUNDERT PROZENT" FIX (Gegen 404 v1beta)
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # 'transport=rest' umgeht die fehlerhaften Kanäle aus deinen Screenshots
        genai.configure(api_key=api_key, transport='rest')
        # Wir definieren das Modell ohne Beta-Präfix
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Verbindungsfehler: {e}")
        st.stop()
else:
    st.error("API Key fehlt! Bitte in den 'Secrets' der Streamlit Cloud eintragen.")
    st.stop()

# Speicher für das Portfolio
if 'visit_history' not in st.session_state:
    st.session_state.visit_history = []

# 3. KI-AGENT LOGIK
def run_expert_ai(query, image=None):
    instruction = """Du bist Senior-Immobilien-Analyst für Málaga. 
    Analysiere das Investment präzise.
    Antworte IMMER am Ende mit diesem exakten Format für die Tabelle:
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
        
        # Daten-Extraktion für das Portfolio
        score = re.search(r"SCORE:\s*(\d+)", text).group(1) if re.search(r"SCORE:\s*(\d+)", text) else "N/A"
        rendite = re.search(r"RENDITE:\s*([\d,.]+%?)", text).group(1) if re.search(r"RENDITE:\s*([\d,.]+%?)", text) else "N/A"
        risiko = re.search(r"RISIKO:\s*(\w+)", text).group(1) if re.search(r"RISIKO:\s*(\w+)", text) else "N/A"
        max_p = re.search(r"MAX-PREIS:\s*(.*)", text).group(1) if re.search(r"MAX-PREIS:\s*(.*)", text) else "N/A"
        
        return text, score, rendite, risiko, max_p
    except Exception as e:
        return f"Fehler: {e}", "N/A", "N/A", "N/A", "N/A"

# 4. BENUTZEROBERFLÄCHE (UI)
st.title("🤖 Invest-Scout Pro: Málaga Dashboard")

tabs = st.tabs(["🔍 Markt-Analyse", "⚖️ Mein Portfolio", "📍 Regionen-Karte"])

# --- TAB 1: ANALYSE ---
with tabs[0]:
    st.subheader("Neuer Immobilien-Check")
    search_query = st.text_input("Deine Anfrage", placeholder="Z.B. Wohnung in Málaga Zentrum bis 200k")
    
    col_in, col_img = st.columns([2, 1])
    with col_in:
        budget = st.slider("Budget (€)", 50000, 2000000, 300000, step=10000)
    with col_img:
        uploaded_file = st.file_uploader("Foto hochladen (Optional)", type=["jpg", "png", "jpeg"])

    if st.button("🚀 Analyse starten", use_container_width=True):
        if search_query:
            with st.spinner("KI analysiert..."):
                img = Image.open(uploaded_file) if uploaded_file else None
                bericht, score, rendite, risiko, max_p = run_expert_ai(f"{search_query} Budget: {budget}€", img)
                
                # Portfolio-Speicherung
                st.session_state.visit_history.append({
                    "Datum": datetime.date.today().strftime("%d.%m.%Y"),
                    "Objekt": search_query[:35] + "...",
                    "Score": score, "Rendite": rendite, "Risiko": risiko, "Empfehlung": max_p
                })
                
                st.success("Analyse abgeschlossen!")
                st.markdown(bericht)
                
                st.divider()
                st.subheader("🔗 Direkte Links")
                c1, c2 = st.columns(2)
                c1.link_button("🏠 Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}")
                c2.link_button("🌍 Kyero", f"https://www.kyero.com/de/malaga-provinz-immobilien-kaufen-0l3?max_price={budget}")

# --- TAB 2: PORTFOLIO & EXPORT ---
with tabs[1]:
    if st.session_state.visit_history:
        st.subheader("⚖️ Dein Investment-Portfolio")
        df = pd.DataFrame(st.session_state.visit_history)
        st.dataframe(df, use_container_width=True)
        
        # EXPORT ALS CSV (Excel-kompatibel)
        csv = df.to_csv(index=False).encode('utf-8')
        col_dl, col_del = st.columns(2)
        with col_dl:
            st.download_button("📥 Als Excel/CSV speichern", data=csv, file_name="Malaga_Portfolio.csv", mime='text/csv')
        with col_del:
            if st.button("🗑️ Historie löschen"):
                st.session_state.visit_history = []
                st.rerun()
    else:
        st.info("Noch keine Analysen gespeichert.")

# --- TAB 3: KARTE ---
with tabs[2]:
    st.subheader("📍 Immobilien-Fokus")
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10)
    st.pydeck_chart(pdk.Deck(initial_view_state=view))
