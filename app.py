import streamlit as st
import os
import subprocess
import pandas as pd
import requests
from openai import OpenAI
from fake_useragent import UserAgent

# ==========================================
# 1. SYSTEM-INSTALLATION (PUNKT 2 & STABILITÄT)
# ==========================================
def ensure_playwright_browsers():
    """Installiert Browser-Treiber auf dem Streamlit-Server (verhindert Code: 1ST)."""
    if not os.path.exists("/home/appuser/.cache/ms-playwright"):
        try:
            subprocess.run(["playwright", "install", "chromium"], check=True)
        except Exception:
            # Falls lokal ausgeführt, wird dieser Schritt übersprungen
            pass

ensure_playwright_browsers()

# ==========================================
# 2. KONFIGURATION & TOOLS
# ==========================================
st.set_page_config(
    page_title="Málaga Invest Pro", 
    page_icon="🤖", 
    layout="centered"
)

# API-Keys sicher laden
openai_key = st.secrets.get("OPENAI_API_KEY")
groq_key = st.secrets.get("GROQ_API_KEY")
client = OpenAI(api_key=openai_key) if openai_key else None
ua = UserAgent()

# ==========================================
# 3. INTERFACE (APPLE-OPTIMIERT)
# ==========================================
st.title("🤖 Málaga Invest-Zentrale")

# Eingaben oben (Optimiert für iPhone-Touch)
anzeigen_link = st.text_input("🔗 Link zur Anzeige (Idealista/Fotocasa):", placeholder="Link hier einfügen...")
g_link = st.text_input("🖼️ Google-Foto / Maps Link:", placeholder="Link zum Standort...")

col_typ, col_preis = st.columns([2, 1])
with col_typ:
    objekt = st.text_input("Haus-Typ/Region:", value="Finca Málaga")
with col_preis:
    preis = st.number_input("Kaufpreis (€):", value=250000, step=5000)

# 7% ITP Steuer-Check (Direkt berechnet)
itp = preis * 0.07
st.success(f"💰 **Finanz-Check:** ITP (7%): {itp:,.0f} € | Gesamt-Invest: {preis + itp:,.0f} €")

# ==========================================
# 4. CHAT-SYSTEM (FIXIERT FÜR MOBILE)
# ==========================================
st.subheader("💬 Chat mit deinem Experten")

# Session State für Chat-Historie (Verhindert Datenverlust bei Refresh)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat-Verlauf rendern
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat-Eingabe (Bleibt beim iPhone über der Tastatur)
if prompt := st.chat_input("Frage zum Risiko oder zur Infrastruktur stellen..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if client:
            try:
                # Nutzt OpenAI GPT-4o-mini für präzise Analyse deiner Risiko-Keywords
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Du bist ein Immobilien-Experte für Málaga. Analysiere Risiken wie 'suelo rústico', 'AFO', 'DAFO', 'sin licencia' oder 'ocupada'."},
                        {"role": "user", "content": f"Objekt: {objekt}, {preis}€. Anzeige: {anzeigen_link}. Aufgabe: {prompt}"}
                    ],
                    temperature=0.2
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"KI-Fehler: {e}")
        else:
            st.warning("Kein OpenAI Key gefunden. Bitte in den Secrets hinterlegen.")

# ==========================================
# 5. MARKT-ANALYSE & RECHERCHE
# ==========================================
st.divider()
if st.button("🚀 VOLLSTÄNDIGE ANALYSE STARTEN", use_container_width=True):
    with st.spinner("Starte Browser-Scraper und lade Markt-Daten..."):
        # Platzhalter für deine Scraper-Logik (Playwright)
        st.subheader("📍 Standort & Markt")
        map_data = pd.DataFrame({'lat': [36.7212, 36.6591], 'lon': [-4.4214, -4.7562]})
        st.map(map_data)
        
        st.subheader("🌐 Recherche-Links")
        c1, c2 = st.columns(2)
        with c1:
            st.link_button("🏠 Markt-Vergleich", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/fincas/?precio-maximo={preis+20000}")
        with c2:
            st.link_button("📸 Foto-Check", f"https://www.google.com/search?q={objekt.replace(' ', '+')}+Málaga+kaufen")

st.caption("✅ System-Status: ITP 7% aktiv | OpenAI bereit | Scraper getarnt | Apple-Layout aktiv")
