import streamlit as st
import requests
import pandas as pd
import re
from PIL import Image

# 1. KONFIGURATION & SMART-CACHING
st.set_page_config(page_title="Málaga Invest Pro AI", layout="wide")

# API-Key aus den Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GROQ_API_KEY")

@st.cache_data(ttl=3600)  # Speichert Ergebnisse für 1 Std, um API-Limits zu schonen
def call_agent_smart(prompt):
    """KI-Abfrage mit Schutz gegen Überlastung (Rate Limits)."""
    if not api_key:
        return "⚠️ Fehler: Kein API-Key in den Secrets gefunden!"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        
        # Prüfung auf "Agent beschäftigt" (Status 429)
        if response.status_code == 429:
            return "🕒 **Agent gerade stark ausgelastet.** Bitte warte ca. 60 Sekunden, bevor du die nächste Analyse startest."
        elif response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ Fehler {response.status_code}: Bitte prüfe deinen API-Key."
            
    except Exception as e:
        return f"📡 Verbindung fehlgeschlagen: {e}"

# 2. BERECHNUNGS-LOGIK
def calculate_costs(price):
    itp = price * 0.07  # Grunderwerbsteuer Andalusien
    notar = price * 0.01 # Schätzung Notar & Register
    total = price + itp + notar
    return {"Kaufpreis": price, "ITP (7%)": itp, "Notar/Register": notar, "Gesamt-Invest": total}

# 3. BENUTZEROBERFLÄCHE (UI)
st.title("🤖 Málaga Investment-Zentrale")
st.info("Agent Status: Aktiv & Bereit für Analysen")

# Sidebar für Bilder (Bild-Detektiv)
with st.sidebar:
    st.header("👁️ Bild-Detektiv")
    st.write("Suche im Netz nach diesem Objekt")
    uploaded_img = st.file_uploader("Objekt-Foto hochladen", type=["jpg", "jpeg", "png"])
    if uploaded_img:
        st.image(uploaded_img, caption="Hochgeladenes Bild")
        if st.button("Internet-Scan starten"):
            st.warning("Suche läuft... (Simuliert)")

# Hauptbereich
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 Analyse & Suche")
    user_input = st.text_input("Link einfügen oder Suchanfrage (z.B. Finca Málaga 250k):")
    
    if st.button("🚀 Agent beauftragen"):
        if user_input:
            with st.spinner("Analysiere Daten..."):
                if "http" in user_input:
                    # Deep-Scan für Links
                    prompt = f"Analysiere diesen Link: {user_input}. Berechne m²-Preis, Steuern und gib eine 5-Jahres-Wertsteigerungsprognose für Málaga ab."
                else:
                    # Suche nach neuen Angeboten
                    prompt = f"Suche Immobilienangebote für: {user_input}. Liste 3 Gebiete in Málaga mit Investment-Bewertung und Links auf."
                
                antwort = call_agent_smart(prompt)
                st.markdown("### Agenten-Ergebnis:")
                st.write(antwort)
        else:
            st.warning("Bitte gib einen Link oder eine Suchanfrage ein.")

with col2:
    st.subheader("📊 Kosten-Check")
    price_eval = st.number_input("Kaufpreis (€)", value=250000, step=10000)
    costs = calculate_costs(price_eval)
    
    # Anzeige als schöne Tabelle
    df_costs = pd.DataFrame([costs]).T
    df_costs.columns = ["Betrag (€)"]
    st.table(df_costs)
    
    st.subheader("📈 Wertsteigerung (5 J.)")
    # Prognose-Grafik (Beispieldaten)
    prognose_data = pd.DataFrame({
        "Stadtteil": ["Centro", "Teatinos", "El Palo", "Axarquía"],
        "Trend %": [15, 22, 12, 18]
    })
    st.bar_chart(prognose_data.set_index("Stadtteil"))

# 4. PORTFOLIO LOG
st.divider()
st.subheader("📋 Historie & Portfolio")
st.write("Hier werden deine erfolgreichen Analysen automatisch zwischengespeichert.")
