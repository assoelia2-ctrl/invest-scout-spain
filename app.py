import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk
import datetime
import re
import io

# 1. Konfiguration
st.set_page_config(page_title="Invest-Scout: Málaga Pro", layout="wide", page_icon="🏢")

# STABILISIERTER API-SETUP
# Wir suchen nach verschiedenen möglichen Namen für den Key in deinen Secrets
api_key = None
for key_name in ["GEMINI_API_KEY", "GOOGLE_API_KEY"]:
    if key_name in st.secrets:
        api_key = st.secrets[key_name]
        break

if not api_key:
    api_key = st.sidebar.text_input("Gemini API Key manuell eingeben", type="password")

if api_key:
    try:
        # Konfiguration für stabile API-Anbindung
        genai.configure(api_key=api_key)
        
        # WICHTIG: Wir nutzen den Namen ohne Pfade, um v1beta-Fehler zu vermeiden
        model = genai.GenerativeModel('gemini-1.5-flash')
        
    except Exception as e:
        st.error(f"Setup-Fehler: {e}")
        st.stop()
else:
    st.info("Bitte API Key in den Streamlit Cloud Secrets hinterlegen.")
    st.stop()

if 'visit_history' not in st.session_state:
    st.session_state.visit_history = []

# 2. KI-Logik (stabilisiert)
def run_expert_ai(query, image=None):
    instruction = """Du bist ein Immobilien-Experte für Málaga. Analysiere das Investment. 
    Beende deine Antwort IMMER exakt mit diesem Format für die Tabelle:
    SCORE: [1-10]
    RENDITE: [%]
    RISIKO: [Text]
    MAX-PREIS: [Euro]"""
    
    content_parts = [instruction, query]
    if image:
        content_parts.append(image)
    
    # Generierung über die stabile Instanz
    response = model.generate_content(content_parts)
    text = response.text
    
    # Daten-Extraktion
    try:
        score = re.search(r"SCORE:\s*(\d+)", text).group(1)
        rendite = re.search(r"RENDITE:\s*([\d,.]+%?)", text).group(1)
        risiko = re.search(r"RISIKO:\s*(\w+)", text).group(1)
        max_p = re.search(r"MAX-PREIS:\s*(.*)", text).group(1)
    except:
        score, rendite, risiko, max_p = "N/A", "N/A", "N/A", "N/A"
        
    return text, score, rendite, risiko, max_p

# 3. Dashboard
st.title("🤖 Invest-Scout Pro: Málaga Dashboard")
tabs = st.tabs(["🔍 Analyse", "⚖️ Portfolio", "📍 Karte"])

with tabs[0]:
    search_query = st.text_input("Was suchst du in Málaga?", placeholder="Z.B. Wohnung in Strandnähe...")
    budget = st.slider("Budget (€)", 50000, 2000000, 300000)
    uploaded_file = st.file_uploader("Objekt-Foto hochladen", type=["jpg", "png", "jpeg"])

    if st.button("🚀 Markt-Analyse starten", use_container_width=True):
        if search_query:
            with st.spinner("KI analysiert den Markt..."):
                img = Image.open(uploaded_file) if uploaded_file else None
                bericht, score, rendite, risiko, max_p = run_expert_ai(f"{search_query} Budget: {budget}€", img)
                
                st.session_state.visit_history.append({
                    "Datum": datetime.date.today().strftime("%d.%m.%Y"),
                    "Objekt": search_query[:40],
                    "Budget": f"{budget:,} €",
                    "Score": score,
                    "Rendite": rendite,
                    "Risiko": risiko,
                    "Empfehlung": max_p
                })
                
                st.success(f"Analyse fertig! Score: {score}/10")
                st.markdown(bericht)
                
                st.divider()
                st.subheader("🔗 Live-Angebote")
                c1, c2 = st.columns(2)
                c1.link_button("Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}")
                c2.link_button("Kyero", f"https://www.kyero.com/de/malaga-provinz-immobilien-kaufen-0l3?max_price={budget}")
        else:
            st.warning("Bitte gib eine Suchanfrage ein.")

with tabs[1]:
    if st.session_state.visit_history:
        df = pd.DataFrame(st.session_state.visit_history)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export als CSV (Excel)", data=csv, file_name="Malaga_Investment_History.csv", mime='text/csv')
    else:
        st.info("Noch keine Daten vorhanden.")

with tabs[2]:
    st.subheader("📍 Málaga Immobilien-Fokus")
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10)
    st.pydeck_chart(pdk.Deck(initial_view_state=view))
