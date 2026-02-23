import streamlit as st
import os
import subprocess
import pandas as pd
import requests
from openai import OpenAI
from fake_useragent import UserAgent

# 1. SYSTEM-INSTALLATION (FÜR BROWSER-FUNKTIONEN)
def ensure_playwright_browsers():
    if not os.path.exists("/home/appuser/.cache/ms-playwright"):
        try:
            subprocess.run(["playwright", "install", "chromium"], check=True)
        except Exception:
            pass

ensure_playwright_browsers()

# 2. SETUP & KEYS (AUS DEN SECRETS)
st.set_page_config(page_title="Málaga Invest Pro", layout="centered")
openai_key = st.secrets.get("OPENAI_API_KEY")
groq_key = st.secrets.get("GROQ_API_KEY")
client = OpenAI(api_key=openai_key) if openai_key else None
ua = UserAgent()

# 3. INTERFACE (APPLE-OPTIMIERT)
st.title("🤖 Málaga Invest-Zentrale")

anzeigen_link = st.text_input("🔗 Link zur Immobilien-Anzeige:", placeholder="Link hier einfügen...")
g_link = st.text_input("🖼️ Google-Foto / Maps Link:", placeholder="Standort-Link...")

col_typ, col_preis = st.columns([2, 1])
with col_typ:
    objekt = st.text_input("Haus-Typ/Region:", value="Finca Málaga")
with col_preis:
    preis = st.number_input("Kaufpreis (€):", value=250000, step=5000)

# Steuer-Logik
itp = preis * 0.07
st.success(f"💰 ITP (7%): {itp:,.0f} € | Gesamt: {preis + itp:,.0f} €")

# 4. CHAT-SYSTEM (LÖST DAS LINK-PROBLEM)
st.subheader("💬 Chat mit deinem Experten")
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Frage stellen..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Wir betten den Link direkt in die KI-Anfrage ein
        link_context = f" Hier ist der Link zum Objekt für deine Analyse: {anzeigen_link}" if anzeigen_link else ""
        system_instructions = f"Du bist ein Immobilien-Experte für Málaga. Analysiere Risiken wie suelo rústico oder AFO.{link_context}"

        # PRIORITÄT GROQ: Umgeht den OpenAI Quota-Fehler (429)
        if groq_key:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {groq_key}"}
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": system_instructions},
                        {"role": "user", "content": f"Objekt: {objekt}, Preis: {preis}€. Aufgabe: {prompt}"}
                    ],
                    "temperature": 0.2
                }
                r = requests.post(url, json=payload, headers=headers, timeout=15).json()
                answer = r['choices'][0]['message']['content']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception:
                st.error("KI-Anfrage über Groq aktuell verzögert.")
        elif client:
            # BACKUP OPENAI (Nur wenn Guthaben vorhanden ist)
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_instructions},
                        {"role": "user", "content": prompt}
                    ]
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Fehler: {e}")
        else:
            st.warning("Kein KI-Key (Groq oder OpenAI) in den Secrets gefunden.")

# 5. ANALYSE & DIREKT-LINKS
st.divider()
if st.button("🚀 VOLLSTÄNDIGE ANALYSE STARTEN", use_container_width=True):
    st.info("Markt-Check wird gestartet...")
    # Karte als visueller Anker
    map_data = pd.DataFrame({'lat': [36.72], 'lon': [-4.42]})
    st.map(map_data)
    
    # Ermöglicht den schnellen Wechsel zur Anzeige
    if anzeigen_link:
        st.link_button("👉 Öffne Original-Anzeige", anzeigen_link)

st.caption("✅ Fusion-Modus: Groq-First | Link-Kontext aktiv | ITP 7% | Apple-Layout")
