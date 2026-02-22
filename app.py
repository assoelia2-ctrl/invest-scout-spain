import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk
import datetime
import re

# 1. DESIGN & TAB-STRUKTUR
st.set_page_config(page_title="Invest-Scout Málaga Pro", layout="wide")

# 2. DER API-RETIREMENT-FIX (Wir zwingen die v1 Version)
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # Dieser Befehl überschreibt die fehlerhafte Standard-Einstellung der Cloud
        # Wir nutzen explizit die stabile API v1 via REST
        genai.configure(api_key=api_key, transport='rest')
        # Wir rufen das Modell direkt über den Namen auf
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    except Exception as e:
        st.error(f"Setup-Fehler: {e}")
        st.stop()
else:
    st.error("API Key fehlt in den Secrets!")
    st.stop()

# Speicher für das Portfolio
if 'visit_history' not in st.session_state:
    st.session_state.visit_history = []

# 3. DAS HAUPTMENÜ
st.title("🤖 Invest-Scout Pro: Málaga")
tab1, tab2, tab3 = st.tabs(["🔍 Analyse", "⚖️ Portfolio", "📍 Karte"])

# --- TAB 1: ANALYSE & LINKS ---
with tab1:
    st.subheader("Neuer Immobilien-Check")
    query = st.text_input("Was suchst du?", placeholder="Z.B. Finca in Málaga bis 250k")
    budget = st.slider("Budget (€)", 50000, 2000000, 350000, step=10000)
    
    if st.button("🚀 Analyse starten", use_container_width=True):
        if query:
            try:
                with st.spinner("KI berechnet Investment..."):
                    # Die Anfrage
                    res = model.generate_content(f"Analysiere als Immobilien-Experte für Málaga: {query}. Budget: {budget}€. Antworte strukturiert und beende mit SCORE: [1-10].")
                    text = res.text
                    
                    # Score für die Tabelle finden
                    score = re.search(r"SCORE:\s*(\d+)", text).group(1) if re.search(r"SCORE:\s*(\d+)", text) else "N/A"
                    
                    # Speichern
                    st.session_state.visit_history.append({
                        "Datum": datetime.date.today().strftime("%d.%m.%Y"),
                        "Anfrage": query[:35] + "...",
                        "Budget": f"{budget:,} €",
                        "Score": score
                    })
                    
                    st.success(f"Analyse abgeschlossen (Score: {score}/10)")
                    st.markdown(text)
                    
                    st.divider()
                    st.subheader("🔗 Direkte Suche")
                    c1, c2 = st.columns(2)
                    c1.link_button("🏠 Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}")
                    c2.link_button("🌍 Kyero", f"https://www.kyero.com/de/malaga-provinz-immobilien-kaufen-0l3?max_price={budget}")
            except Exception as e:
                st.error(f"Fehler: {e}")
        else:
            st.warning("Bitte Suchanfrage eingeben.")

# --- TAB 2: PORTFOLIO & EXCEL ---
with tab2:
    if st.session_state.visit_history:
        st.subheader("⚖️ Deine Suchhistorie")
        df = pd.DataFrame(st.session_state.visit_history)
        st.table(df)
        
        # EXCEL EXPORT
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Als Excel/CSV laden", data=csv, file_name="Malaga_Investment.csv", mime='text/csv')
    else:
        st.info("Noch keine Daten vorhanden.")

# --- TAB 3: DIE MAP ---
with tab3:
    st.subheader("📍 Markt-Übersicht")
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10, pitch=40)
    st.pydeck_chart(pdk.Deck(
        initial_view_state=view,
        layers=[pdk.Layer('ScatterplotLayer', data=pd.DataFrame({'lat': [36.72], 'lon': [-4.42]}), get_position='[lon, lat]', get_radius=1000, get_color='[200, 30, 0]')]
    ))
