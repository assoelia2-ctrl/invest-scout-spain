import streamlit as st
import requests
import pandas as pd
import re
from PIL import Image

# 1. KONFIGURATION & STYLING
st.set_page_config(page_title="Málaga Invest Pro AI", layout="wide")
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GROQ_API_KEY")

def call_agent(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(url, json=payload, timeout=20)
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Agent ist gerade beschäftigt. Bitte kurz warten."

# 2. FUNKTIONEN DES AGENTEN
def calculate_costs(price):
    itp = price * 0.07
    notar = price * 0.01
    total = price + itp + notar
    return {"Kaufpreis": price, "ITP (7%)": itp, "Notar/Register": notar, "Gesamt": total}

# 3. UI - LAYOUT
st.title("🤖 Málaga Investment-Zentrale")
st.markdown("---")

# Sidebar für Bild-Upload & Vision
with st.sidebar:
    st.header("👁️ Bild-Detektiv")
    uploaded_img = st.file_uploader("Objekt-Foto hochladen", type=["jpg", "jpeg", "png"])
    if uploaded_img:
        st.image(uploaded_img, caption="Zu suchendes Objekt")
        if st.button("Netz nach Bild scannen"):
            st.info("Agent scannt Idealista, Fotocasa & Kyero nach optischen Treffern...")
            # Hier greift die Vision-Logik
            st.warning("Feature: Reverse-Image-Search über Google Lens wird simuliert.")

# Hauptbereich: Suche & Link-Analyse
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 Suche & Analyse")
    user_input = st.text_input("Link einfügen ODER Suchanfrage stellen (z.B. Finca in Coín bis 250k):")
    
    if st.button("🚀 Agent beauftragen"):
        with st.spinner("Agent analysiert..."):
            if "http" in user_input:
                # Modus: Link-Experte
                prompt = f"Analysiere diesen Immobilien-Link detailliert: {user_input}. Berechne m²-Preis, ITP-Steuer und gib eine 5-Jahres-Wertsteigerungsprognose für diese Lage in Málaga ab."
                result = call_agent(prompt)
                st.markdown(result)
            else:
                # Modus: Proaktiver Scout
                prompt = f"Suche Immobilienangebote für: {user_input}. Erstelle eine Liste mit 3 passenden Gebieten in Málaga, inkl. fiktiver Beispiellinks und einer Investment-Bewertung."
                result = call_agent(prompt)
                st.markdown(result)

with col2:
    st.subheader("📊 Investment-Check")
    price_eval = st.number_input("Kaufpreis für Kostencheck (€)", value=250000, step=10000)
    costs = calculate_costs(price_eval)
    
    st.table(pd.DataFrame([costs]).T.rename(columns={0: "Betrag (€)"}))
    
    st.subheader("📈 Prognose (5 Jahre)")
    # Statische Daten für die Prognose-Visualisierung
    prognose_data = pd.DataFrame({
        "Viertel": ["Centro", "Teatinos", "El Palo", "Estepona"],
        "Wachstum %": [15, 22, 12, 18]
    })
    st.bar_chart(prognose_data.set_index("Viertel"))

# 4. PORTFOLIO LOG
st.markdown("---")
st.subheader("📋 Dein Investment-Portfolio")
if 'history' not in st.session_state:
    st.session_state.history = []
# Hier werden Ergebnisse gespeichert...
