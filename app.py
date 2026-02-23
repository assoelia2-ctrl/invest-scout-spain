import streamlit as st
import os
import subprocess
import pandas as pd
import requests
from openai import OpenAI
from fake_useragent import UserAgent

# 1. SYSTEM-INSTALLATION (PUNKT 2)
def ensure_playwright_browsers():
    """Installiert die Browser-Komponenten auf dem Streamlit-Server."""
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

# Eingabemaske für Links
anzeigen_link = st.text_input("🔗 Link zur Anzeige:", placeholder="Idealista, Fotocasa...")
g_link = st.text_input("🖼️ Google-Foto / Maps Link:", placeholder="Link zum Standort...")

# Kompakte Zeile für Daten (Stapelt sich auf dem iPhone automatisch)
col_typ, col_preis = st.columns([2, 1])
with col_typ:
    objekt = st.text_input("Haus-Typ/Region:", value="Finca Málaga")
with col_preis:
    preis = st.number_input("Kaufpreis (€):", value=250000, step=5000)

# 7% ITP Steuerberechnung (Andalusien)
itp = preis * 0.07
st.success(f"💰 **Finanz-Check:** ITP (7%): {itp:,.0f} € | Gesamt-Invest: {preis + itp:,.0f} €")

# 4. CHAT-SYSTEM (FIXIERT AM UNTEREN RAND)
st.subheader("💬 Chat mit deinem Experten")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat-Verlauf anzeigen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat-Eingabe (Optimiert für mobile Tastaturen)
if prompt := st.chat_input("Frage stellen (z.B. 'Prüfe auf suelo rústico')..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Priorität: Groq (Vermeidung von OpenAI Quota-Fehler 429)
        if groq_key:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {groq_key}"}
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": "Du bist ein Immobilien-Experte für Málaga. Analysiere Risiken wie suelo rústico, AFO, DAFO oder ocupada."},
                        {"role": "user", "content": f"Objekt: {objekt}, {preis}€. Link: {anzeigen_link}. Aufgabe: {prompt}"}
                    ],
                    "temperature": 0.2
                }
                r = requests.post(url, json=payload, headers=headers, timeout=10).json()
                answer = r['choices'][0]['message']['content']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                # Fallback auf OpenAI (falls Groq scheitert und Guthaben da ist)
                if client:
                    try:
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        answer = response.choices[0].message.content
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    except Exception:
                        st.error("Be
