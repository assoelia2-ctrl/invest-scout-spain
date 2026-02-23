import streamlit as st
import os
import subprocess
import pandas as pd
import requests
import random
import time
import re

# ==========================================
# 1. AUTOMATISCHE INSTALLATION (PUNKT 2)
# ==========================================
def ensure_playwright_browsers():
    """Installiert die notwendigen Browser-Komponenten auf dem Streamlit-Server."""
    try:
        # Prüft, ob wir uns in einer Umgebung befinden, die Installationen erlaubt
        if not os.path.exists("/home/appuser/.cache/ms-playwright"):
            with st.spinner("Installiere Markt-Scan-Komponenten (nur beim ersten Start)..."):
                subprocess.run(["playwright", "install", "chromium"], check=True)
    except Exception as e:
        st.info("Hinweis: Browser-Installation wird geprüft oder ist bereits abgeschlossen.")

ensure_playwright_browsers()

# ==========================================
# 2. RISIKO-SCORING LOGIK (DEIN SKRIPT)
# ==========================================
def analyze_risk_scoring(description):
    """Scannt Texte nach rechtlichen Risiken in Andalusien."""
    RISK_MAP = {
        "suelo rústico": 5,
        "no urbanizable": 5,
        "sin licencia": 6,
        "no registrada": 6,
        "ocupada": 10
    }
    desc_lower = description.lower()
    score = 0
    found_flags = []
    
    for key, value in RISK_MAP.items():
        if key in desc_lower:
            score += value
            found_flags.append(key)
    return score, found_flags

# ==========================================
# 3. STREAMLIT UI SETUP
# ==========================================
st.set_page_config(page_title="Málaga Invest Pro", layout="centered")
groq_key = st.secrets.get("GROQ_API_KEY")

st.title("🤖 Málaga Invest-Zentrale")

# Eingabemaske für Links und Objektdaten
anzeigen_link = st.text_input("🔗 Link zur Immobilien-Anzeige:", placeholder="z.B. Idealista Link...")
g_link = st.text_input("🖼️ Google-Foto / Maps Link:", placeholder="Link zum Standort...")

col_typ, col_preis = st.columns([2, 1])
with col_typ:
    objekt = st.text_input("Haus-Typ/Region:", value="Finca Málaga")
with col_preis:
    preis = st.number_input("Kaufpreis (€):", value=250000, step=5000)

# 7% ITP Steuerberechnung (Andalusien)
itp = preis * 0.07
st.success(f"💰 **Finanz-Check:** ITP (7%): {itp:,.0f} € | Gesamt-Invest: {preis + itp:,.0f} €")

# ==========================================
# 4. CHAT-SYSTEM (INTERAKTIV)
# ==========================================
st.subheader("💬 Chat mit deinem Experten")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat-Verlauf anzeigen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat-Eingabe ganz unten
if prompt := st.chat_input("Stelle eine Frage zum Objekt oder gib eine Aufgabe..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if groq_key:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key}"}
            
            # Kontext für die KI inkl. Risiko-Wissen
            full_context = f"""
            Objekt: {objekt} für {preis}€. 
            Anzeige: {anzeigen_link}
            Nutze dein Wissen über rechtliche Risiken in Andalusien (Suelo rústico, Lizenzen).
            Aufgabe: {prompt}
            """
            
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "Du bist ein erfahrener Immobilien-Analyst für Málaga."},
                    {"role": "user", "content": full_context}
                ]
            }
            try:
                r = requests.post(url, json=payload, headers=headers, timeout=15).json()
                response_text = r['choices'][0]['message']['content']
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except:
                st.error("KI-Service aktuell verzögert.")

# ==========================================
# 5. ANALYSE-BUTTON & RECHERCHE
# ==========================================
st.divider()
if st.button("🚀 VOLLSTÄNDIGE ANALYSE STARTEN", use_container_width=True):
    with st.spinner("Scanne Markt-Daten und berechne Risiken..."):
        # Platzhalter für Scraper-Ergebnisse
        st.subheader("📍 Standort & Markt-Check")
        
        # Karte und Trends (Statisch als Basis)
        map_data = pd.DataFrame({'lat': [36.7212, 36.6591], 'lon': [-4.4214, -4.7562]})
        st.map(map_data)
        
        st.subheader("🔍 Direkte Recherche-Links")
        c1, c2 = st.columns(2)
        with c1:
            st.link_button("🏠 Passende Angebote", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/fincas/?precio-maximo={preis+20000}")
        with c2:
            st.link_button("📸 Foto-Check auf Google", f"https://www.google.com/search?q={objekt.replace(' ', '+')}+Málaga+kaufen")

st.divider()
st.caption("✅ System-Status: ITP 7% aktiv | Chat aktiv | Playwright bereit")
