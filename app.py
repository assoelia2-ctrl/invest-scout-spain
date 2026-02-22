import streamlit as st
import requests
import pandas as pd

# 1. SETUP & KEY
st.set_page_config(page_title="Málaga Invest Pro AI", layout="wide")
# Dein Groq-Key aus den Secrets
groq_key = st.secrets.get("GROQ_API_KEY")

@st.cache_data(ttl=3600)
def call_groq_agent(prompt):
    if not groq_key:
        return "❌ GROQ_API_KEY fehlt!"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        return response.json()['choices'][0]['message']['content']
    except:
        return "Agent ist gerade beschäftigt. Bitte kurz warten."

# 2. UI DESIGN
st.title("🤖 Málaga Investment-Zentrale")
st.success("System bereit")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 Suche & Strategie")
    user_input = st.text_input("Was suchst du?", value="Finca im Umland von Málaga")
    max_price = st.number_input("Budget (€)", value=250000)
    
    if st.button("🚀 Analyse starten", use_container_width=True):
        with st.spinner("Agent wertet Daten aus..."):
            prompt = f"Analysiere kurz das Potenzial für {user_input} bis {max_price} Euro in Málaga. Nenne 3 Top-Gebiete."
            st.markdown(call_groq_agent(prompt))
            
            # ECHTE LINKS generieren (keine Phantom-Links mehr)
            id_url
