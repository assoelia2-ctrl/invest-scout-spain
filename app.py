import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk
import datetime
import re
import io

# 1. Seite konfigurieren
st.set_page_config(page_title="Invest-Scout: Málaga Pro", layout="wide", page_icon="🏢")

# --- STABILISIERTER API-SETUP ---
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # WICHTIG: Wir erzwingen die stabile API-Version ohne 'v1beta'
        genai.configure(api_key=api_key)
        
        # Wir definieren das Modell direkt. 
        # Falls 'gemini-1.5-flash' zickt, ist 'gemini-1.5-flash-latest' der sicherste Alias.
        model = genai.GenerativeModel('gemini-1.5-flash')
        
    except Exception as e:
        st.error(f"Setup-Fehler: {e}")
        st.stop()
else:
    st.error("API Key fehlt! Bitte in den Streamlit Secrets hinterlegen.")
    st.stop()

if 'visit_history' not in st.session_state:
    st.session_state.visit_history = []

# 2. KI-Agent mit robuster Extraktion
def run_expert_ai(query, image=None):
    instruction = """Du bist Senior-Immobilien-Analyst für Málaga 2026. 
    Analysiere das Investment und gib Tipps zu Marktlage/Lizenzen.
    Antworte IMMER am Ende mit:
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
        
        # Daten-Extraktion
        score = re.search(r"SCORE:\s*(\d+)", text).group(1) if re.search(r"SCORE:\s*(\d+)", text) else "N/A"
        rendite = re.search(r"RENDITE:\s*([\d,.]+%?)", text).group(1) if re.search(r"RENDITE:\s*([\d,.]+%?)", text) else "N/A"
        risiko = re.search(r"RISIKO:\s*(\w+)", text).group(1) if re.search(r"RISIKO:\s*(\w+)", text) else "N/A"
        max_p = re.search(r"MAX-PREIS:\s*(.*)", text).group(1) if re.search(r"MAX-PREIS:\s*(.*)", text) else "N/A"
        
        return text, score, rendite, risiko, max_p
    except Exception as e:
        return f"Fehler bei der Generierung: {e}", "N/A", "N/A", "N/A", "N/A"

# 3. Das Pro-Dashboard
st.title("🤖 Invest-Scout Pro: Málaga Dashboard")
tabs = st.tabs(["🔍 Live-Suche", "⚖️ Portfolio", "📍 Regionen-Karte"])

with tabs[0]:
    search_query = st.text_input("Deine Suchanfrage", placeholder="Ich suche eine Finca in Málaga...")
    col_in, col_img = st.columns([2, 1])
    with col_in:
        budget = st.slider("Maximales Budget (€)", 50000, 2000000, 300000, step=10000)
    with col_img:
        uploaded_file = st.file_uploader("Foto analysieren", type=["jpg", "png", "jpeg"])

    if st.button("🚀 Markt-Analyse starten", use_container_width=True):
        if search_query:
            with st.spinner("KI scannt den Markt..."):
                img = Image.open(uploaded_file) if uploaded_file else None
                bericht, score, rendite, risiko, max_p = run_expert_ai(f"{search_query} Budget: {budget}€", img)
                
                st.session_state.visit_history.append({
                    "Datum": datetime.date.today().strftime("%d.%m.%Y"),
                    "Objekt": search_query[:30], "Score": score, "Rendite": rendite, "Risiko": risiko, "Max-Preis": max_p
                })
                
                st.success(f"Analyse fertig (Score: {score}/10)")
                st.markdown(bericht)
                
                st.divider()
                st.subheader("🔗 Sofort zu den Live-Angeboten")
                c1, c2 = st.columns(2)
                c1.link_button("🏠 Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}", use_container_width=True)
                c2.link_button("🌍 Kyero", f"https://www.kyero.com/de/malaga-provinz-immobilien-kaufen-0l3?max_price={budget}", use_container_width=True)

with tabs[1]:
    if st.session_state.visit_history:
        df = pd.DataFrame(st.session_state.visit_history)
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 Excel-Export (CSV)", df.to_csv(index=False).encode('utf-8'), "Malaga_Invest.csv", "text/csv")

with tabs[2]:
    st.subheader("📍 Málaga Immobilien-Fokus")
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10)
    st.pydeck_chart(pdk.Deck(initial_view_state=view))
