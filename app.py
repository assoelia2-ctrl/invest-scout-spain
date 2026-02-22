import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import pydeck as pdk
import datetime
import re

# 1. SETUP
st.set_page_config(page_title="Invest-Scout Málaga", layout="wide")

# 2. DER DEFINITIVE FIX GEGEN 404 (transport='rest' ist entscheidend)
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Wir erzwingen die stabile REST-Verbindung
    genai.configure(api_key=api_key, transport='rest')
    # Wir nutzen das Modell ohne den fehlerhaften Beta-Pfad
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key fehlt in den Streamlit Secrets!")
    st.stop()

# Speicher für Portfolio (Historie)
if 'visit_history' not in st.session_state:
    st.session_state.visit_history = []

# 3. BENUTZEROBERFLÄCHE (Tabs für Ordnung)
st.title("🤖 Invest-Scout: Málaga Pro")

tab1, tab2 = st.tabs(["🔍 Neue Analyse", "⚖️ Mein Portfolio"])

with tab1:
    query = st.text_input("Was suchst du?", placeholder="Z.B. Haus in Málaga bis 300.000€")
    budget = st.number_input("Budget (€)", value=300000, step=10000)
    
    if st.button("🚀 Markt-Analyse starten", use_container_width=True):
        if query:
            try:
                with st.spinner("Verbindung zur KI wird aufgebaut..."):
                    # Die Anfrage an die KI
                    res = model.generate_content(f"Analysiere als Immobilien-Experte: {query}. Budget: {budget}€. Antworte mit Tipps und am Ende mit SCORE: [1-10].")
                    bericht = res.text
                    
                    # Score extrahieren für die Tabelle
                    score_match = re.search(r"SCORE:\s*(\d+)", bericht)
                    score = score_match.group(1) if score_match else "N/A"
                    
                    # In Historie speichern
                    st.session_state.visit_history.append({
                        "Datum": datetime.date.today().strftime("%d.%m.%Y"),
                        "Anfrage": query[:40] + "...",
                        "Budget": f"{budget:,} €",
                        "Score": score
                    })
                    
                    st.success("Analyse erfolgreich!")
                    st.markdown(bericht)
            except Exception as e:
                st.error(f"Fehler: {str(e)}")
                st.info("Falls der 404-Fehler bleibt, klicke unten rechts auf 'Manage app' -> 'Reboot app'.")
        else:
            st.warning("Bitte gib eine Suchanfrage ein.")

with tab2:
    if st.session_state.visit_history:
        st.subheader("Deine gespeicherten Analysen")
        df = pd.DataFrame(st.session_state.visit_history)
        st.table(df)
        
        # CSV Export
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Als Excel (CSV) exportieren", data=csv, file_name="Malaga_Investments.csv", mime='text/csv')
    else:
        st.info("Noch keine Analysen im Portfolio.")
