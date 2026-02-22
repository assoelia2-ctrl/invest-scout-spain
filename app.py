import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk
import datetime
import re

# 1. SEITE INITIALISIEREN
st.set_page_config(page_title="Invest-Scout: Málaga Pro", layout="wide", page_icon="🏢")

# 2. STABILER API-SETUP (Fix gegen 404 v1beta)
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # transport='rest' zwingt die App auf den stabilen Pfad
        genai.configure(api_key=api_key, transport='rest')
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Verbindungsfehler: {e}")
        st.stop()
else:
    st.error("API Key fehlt in den Streamlit Secrets!")
    st.stop()

# Speicher für die Historie
if 'visit_history' not in st.session_state:
    st.session_state.visit_history = []

# 3. DASHBOARD OBERFLÄCHE
st.title("🤖 Invest-Scout Pro: Málaga")

tabs = st.tabs(["🔍 KI-Analyse", "⚖️ Mein Portfolio", "📍 Regionen-Karte"])

# --- TAB 1: ANALYSE ---
with tabs[0]:
    st.subheader("Neuer Immobilien-Check")
    search_query = st.text_input("Was suchst du?", placeholder="Z.B. Finca in Málaga bis 300.000€")
    budget = st.slider("Max. Budget (€)", 50000, 2000000, 350000, step=10000)
    
    if st.button("🚀 Analyse starten", use_container_width=True):
        if search_query:
            try:
                with st.spinner("KI analysiert den Standort..."):
                    res = model.generate_content(f"Analysiere als Immobilien-Experte für Málaga: {search_query}. Budget: {budget}€. Gib Tipps zu Lage und Rendite. Beende mit SCORE: [1-10].")
                    bericht = res.text
                    
                    # Daten für Portfolio extrahieren
                    score_match = re.search(r"SCORE:\s*(\d+)", bericht)
                    score = score_match.group(1) if score_match else "N/A"
                    
                    st.session_state.visit_history.append({
                        "Datum": datetime.date.today().strftime("%d.%m.%Y"),
                        "Objekt": search_query[:35] + "...",
                        "Budget": f"{budget:,} €",
                        "Score": score
                    })
                    
                    st.success(f"Analyse fertig (Score: {score}/10)")
                    st.markdown(bericht)
                    
                    st.divider()
                    st.subheader("🔗 Direkt zu den Angeboten")
                    c1, c2 = st.columns(2)
                    c1.link_button("🏠 Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}")
                    c2.link_button("🌍 Kyero", f"https://www.kyero.com/de/malaga-provinz-immobilien-kaufen-0l3?max_price={budget}")
            except Exception as e:
                st.error(f"Fehler: {e}")
        else:
            st.warning("Bitte gib eine Suchanfrage ein.")

# --- TAB 2: PORTFOLIO & EXPORT ---
with tabs[1]:
    if st.session_state.visit_history:
        st.subheader("⚖️ Deine Suchhistorie")
        df = pd.DataFrame(st.session_state.visit_history)
        st.dataframe(df, use_container_width=True)
        
        # Export Button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Portfolio als CSV exportieren", data=csv, file_name="Malaga_Investments.csv", mime='text/csv')
    else:
        st.info("Noch keine Analysen gespeichert.")

# --- TAB 3: KARTE ---
with tabs[2]:
    st.subheader("📍 Markt-Übersicht Málaga")
    # Fokus auf Málaga Zentrum
    view = pdk.ViewState(latitude=36.7212, longitude=-4.4214, zoom=10, pitch=45)
    st.pydeck_chart(pdk.Deck(
        initial_view_state=view,
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]}),
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=1000,
            ),
        ]
    ))
