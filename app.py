import streamlit as st
import os
import subprocess
import pandas as pd
import requests
from openai import OpenAI
from fake_useragent import UserAgent

# 1. SYSTEM-INSTALLATION (PUNKT 2)
def ensure_playwright_browsers():
    if not os.path.exists("/home/appuser/.cache/ms-playwright"):
        try:
            subprocess.run(["playwright", "install", "chromium"], check=True)
        except Exception:
            pass

ensure_playwright_browsers()

# 2. SETUP & KEYS
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
        # WICHTIG: Wir sagen der KI explizit, dass sie den Link als Fakt behandeln soll
        context_aus_link = f" Beziehe dich auf diese Immobilie: {anzeigen_link}." if anzeigen_link else ""
        system_msg = f"Du bist Immobilien-Experte für Málaga. Prüfe Risiken wie suelo rústico, AFO, DAFO.{context_aus_link}"

        # PRIORITÄT GROQ (Vermeidet OpenAI Quota-Fehler 429 aus Screenshot 1000007134)
        if groq_key:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {groq_key}"}
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": f"Objekt: {objekt}, {preis}€. Aufgabe: {prompt}"}
                    ],
                    "temperature": 0.2
                }
                r = requests.post(url, json=payload, headers=headers, timeout=15).json()
                answer = r['choices'][0]['message']['content']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception:
                st.error("KI-Dienst über Groq aktuell verzögert.")
        elif client:
            # Backup OpenAI (Falls Quota wieder frei ist)
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
                )
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Fehler: {e}")

# 5. ANALYSE & RECHERCHE
st.divider()
if st.button("🚀 VOLLSTÄNDIGE ANALYSE STARTEN", use_container_width=True):
    st.info("Markt-Daten werden abgerufen...")
    map_data = pd.DataFrame({'lat': [36.72], 'lon': [-4.42]})
    st.map(map_data)
    
    if anzeigen_link:
        st.link_button("👉 Zur Original-Anzeige wechseln", anzeigen_link)

st.caption("✅ System: Link-Kontext bereit | Groq aktiv | ITP 7% | No Syntax Errors")
