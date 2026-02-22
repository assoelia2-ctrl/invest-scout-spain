import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk
import datetime
import re

# 1. INITIALISIERUNG
st.set_page_config(page_title="Invest-Scout Málaga Pro", layout="wide")

# 2. DER "HARD-FIX" GEGEN DEN 404 FEHLER
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # Wir zwingen die API auf die stabile Version v1 ohne Beta-Pfad
        genai.configure(api_key=api_key, transport='rest')
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Verbindungsfehler: {e}")
        st.stop()
else:
    st.error("API Key fehlt in den Secrets!")
    st.stop()

# Speicher für das Portfolio
if 'visit_history' not in st.session_state:
    st.session_state.visit_history = []

# 3. DASHBOARD NAVIGATION
st.title("🤖 Invest-Scout Pro: Málaga")
tab1, tab2, tab3 = st.tabs(["🔍 Analyse & Suche", "⚖️ Mein Portfolio", "📍 Regionen-Karte"])

# --- TAB 1: ANALYSE & LINKS ---
with tab1:
    st.subheader("Neuer Immobilien-Check")
    query = st.text_input("Was suchst du?", placeholder="Finca in Málaga bis 250k...")
    budget = st.slider("Budget (€)", 50000, 2000000, 350000, step=10000)
    
    if st.button("🚀 Strategie-Check starten", use_container_width=True):
        if query:
            try:
                with st.spinner("KI berechnet Investment..."):
                    res = model.generate_content(f"Analysiere als Immobilien-Experte für Málaga: {query}. Budget: {budget}€. Beende mit SCORE: [1-10].")
                    bericht = res.text
                    score = re.search(r"SCORE:\s*(\d+)", bericht).group(1) if re.search(r"SCORE:\s*(\d+)", bericht) else "N/A"
                    
                    st.session_state.visit_history.append({
                        "Datum": datetime.date.today().strftime("%d.%m.%Y"),
                        "Anfrage": query[:35] + "...",
                        "Budget": f"{budget:,} €",
                        "Score": score
                    })
                    st.success(f"Analyse fertig (Score: {score}/10)")
                    st.markdown(bericht)
                    
                    st.divider()
                    st.subheader("🔗 Direkt prüfen")
                    c1, c2 = st.columns(2)
                    c1.link_button("🏠 Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}")
                    c2.link_button("🌍 Kyero", f"https://www.kyero.com/de/malaga-provinz-immobilien-kaufen-0l3?max_price={budget}")
            except Exception as e:
                st.error(f"Kritischer Fehler: {e}") # Falls v1beta Fehler bleibt, zeigt dies die Ursache
        else:
            st.warning("Bitte Suchanfrage eingeben.")

# --- TAB 2: PORTFOLIO & EXCEL EXPORT ---
with tab2:
    if st.session_state.visit_history:
        st.subheader("⚖️ Deine Suchhistorie")
        df = pd.DataFrame(st.session_state.visit_history)
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Als Excel/CSV exportieren", data=csv, file_name="Malaga_Portfolio.csv", mime='text/csv')
    else:
        st.info("Noch keine Daten gespeichert.")

# --- TAB 3: DIE MAP ---
with tab3:
    st.subheader("📍 Markt-Hotspots")
    view = pdk.ViewState(latitude=36.72, longitude=-4.42, zoom=10, pitch=45)
    st.pydeck_chart(pdk.Deck(
        initial_view_state=view,
        layers=[pdk.Layer('ScatterplotLayer', data=pd.DataFrame({'lat': [36.72], 'lon': [-4.42]}), get_position='[lon, lat]', get_radius=1000, get_color='[200, 30, 0]')]
    ))
