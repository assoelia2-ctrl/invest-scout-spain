import streamlit as st
import os
import subprocess
import pandas as pd
import requests
from openai import OpenAI
from fake_useragent import UserAgent

# ==========================================
# 1. SYSTEM-INSTALLATION (PUNKT 2)
# ==========================================
def ensure_playwright_browsers():
    if not os.path.exists("/home/appuser/.cache/ms-playwright"):
        try:
            subprocess.run(["playwright", "install", "chromium"], check=True)
        except Exception:
            pass

ensure_playwright_browsers()

# ==========================================
# 2. SETUP & KEYS
# ==========================================
st.set_page_config(page_title="Málaga Invest Pro", layout="centered")

openai_key = st.secrets.get("OPENAI_API_KEY")
groq_key = st.secrets.get("GROQ_API_KEY")
client = OpenAI(api_key=openai_key) if openai_key else None
ua = UserAgent()

# ==========================================
# 3. INTERFACE (APPLE-OPTIMIERT)
# ==========================================
st.title("🤖 Málaga Invest-Zentrale")

anzeigen_link = st.text_input("🔗 Link zur Anzeige:", placeholder="Idealista...")
g_link = st.text_input("🖼️ Google-Foto Link:", placeholder="Maps-Link...")

col_typ, col_preis = st.columns([2, 1])
with col_typ:
    objekt = st.text_input("Haus-Typ/Region:", value="Finca Málaga")
with col_preis:
    preis = st.number_input("Kaufpreis (€):", value=250000, step=5000)

itp = preis * 0.07
st.success(f"💰 **Finanz-Check:** ITP (7%): {itp:,.0f} € | Gesamt: {preis + itp:,.0f} €")

# ==========================================
# 4. INTELLIGENTES CHAT-SYSTEM (GROQ + OPENAI)
# ==========================================
st.subheader("💬 Chat mit deinem Experten")
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Frage zum Risiko stellen..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # PRIORITÄT 1: GROQ (Um Quota-Fehler zu vermeiden)
        if groq_key:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {groq_key}"}
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": "Du bist Immobilien-Experte für Málaga. Analysiere Risiken wie suelo rústico, AFO, DAFO."},
                        {"role": "user", "content": f"Objekt: {objekt}, {preis}€. Link: {anzeigen_link}. Aufgabe: {prompt}"
