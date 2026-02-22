import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
from PIL import Image

# 1. SETUP
st.set_page_config(page_title="Málaga Invest Pro AI", layout="wide")
groq_key = st.secrets.get("GROQ_API_KEY")

def call_groq_agent(prompt):
    if not groq_key: return "❌ Key fehlt."
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
    payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        return response.json()['choices'][0]['message']['content']
    except: return "Agent beschäftigt..."

# 2. SIDEBAR (FOTO-LOGIK)
with st.sidebar:
    st.header("👁️ Bild-Detektiv")
    # Einfacher Uploader ohne komplizierte Puffer
    up_file = st.file_uploader("Bild wählen", type=["jpg", "jpeg", "png"], key="loader")
    
    if up_file:
        st.image(up_file, caption="Bild bereit", use_container_width=True)
        # Der Button ist jetzt völlig unabhängig platziert
        if st.button("🔍 IM NETZ SUCHEN", use_container_width=True):
            st.info("Suche läuft...")

# 3. HAUPTSEITE
st.title("🤖 Málaga Investment-Zentrale")

c1, c2 = st.columns([2, 1])
with c1:
    query = st.text_input("Suche:", value="Finca bei Málaga")
    price = st.number_input("Budget (€)", value=250000)
with c2:
    st.subheader("📊 Kosten")
    itp = price * 0.07
    st.write(f"Steuer (7%): {itp:,.0f} €")
    st.write(f"Gesamt: {price+itp:,.0f} €")

# 4. DER AKTION-BUTTON (Gereinigt von Einrückungsfehlern)
if st.button("🚀 ANALYSE STARTEN", use_container_width=True):
    # Definitionen ohne Umwege
    i_url = f"
