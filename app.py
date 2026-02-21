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
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    try:
        # Erzwungene Konfiguration für stabile v1 API
        genai.configure(api_key=api_key)
        
        # WICHTIG: Wir definieren das Modell direkt ohne v1beta-Präfix
        model = genai.GenerativeModel('gemini-1.5-flash')
        
    except Exception as e:
        st.error(f"Setup-Fehler: {e}")
        st.stop()
else:
    st.info("Bitte API Key in den Secrets oder der Sidebar hinterlegen.")
    st.stop()

if 'visit_history' not in st.session_state:
    st.session_state.visit_history = []

# 2. KI-Logik (unverändert, aber stabil aufgerufen)
def run_expert_ai(query, image=None):
    instruction = "Du bist ein Immobilien-Experte für Málaga. Analysiere das Investment und schließe ab mit SCORE: [1-10], RENDITE: [%], RISIKO: [Text], MAX-PREIS: [Euro]."
    content = [instruction, query]
    if image:
        content.append(image)
    
    # Der Aufruf nutzt jetzt die stabilisierte Modell-Instanz
    response = model.generate_content(content)
    text = response.text
    
    try:
        score = re.search(r"SCORE:\s*(\d+)", text).group(1)
        rendite = re.search(r"RENDITE:\s*([\d,.]+%?)", text).group(1)
        risiko = re.search(r"RISIKO:\s*(\w+)", text).group(1)
        max_p = re.search(r"MAX-PREIS:\s*(.*)", text).group(1)
    except:
        score, rendite, risiko, max_p = "N/A", "N/A", "N/A", "N/A"
        
    return text, score, rendite, risiko, max_p

# 3. Dashboard (Deine Pro-Version)
st.title("🤖 Invest-Scout Pro: Málaga Dashboard")
tabs = st.tabs(["🔍 Analyse", "⚖️ Portfolio", "📍 Karte"])

with tabs[0]:
    search_query = st.text_input("Suchanfrage", placeholder="Finca in Málaga...")
    budget = st.slider("Budget (€)", 50000, 2000000, 300000)
    uploaded_file = st.file_uploader("Foto", type=["jpg", "png", "jpeg"])

    if st.button("🚀 Markt-Analyse starten", use_container_width=True):
        with st.spinner("KI arbeitet..."):
            img = Image.open(uploaded_file) if uploaded_file else None
            bericht, score, rendite, risiko, max_p = run_expert_ai(f"{search_query} Budget: {budget}€", img)
            
            st.session_state.visit_history.append({
                "Datum": datetime.date.today().strftime("%d.%m.%Y"),
                "Objekt": search_query[:40],
                "Budget": f"{budget} €",
                "Score": score,
                "Rendite": rendite,
                "Risiko": risiko,
                "Max_Preis": max_p
            })
            st.markdown(bericht)

with tabs[1]:
    if st.session_state.visit_history:
        df = pd.DataFrame(st.session_state.visit_history)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export CSV", data=csv, file_name="Malaga_Invest.csv", mime='text/csv')

with tabs[2]:
    st.subheader("📍 Standort-Vorschau")
    st.pydeck_chart(pdk.Deck(initial_view_state=pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10)))
