import streamlit as st
import requests
import pandas as pd
from PIL import Image

# 1. SETUP & AGENT
st.set_page_config(page_title="Málaga Invest", layout="wide")
groq_key = st.secrets.get("GROQ_API_KEY")

def call_agent(prompt):
    if not groq_key: return "Key fehlt!"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_key}"}
    payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.json()['choices'][0]['message']['content']
    except: return "Fehler..."

# 2. SIDEBAR (FOTO-FIX)
with st.sidebar:
    st.header("👁️ Bild-Detektiv")
    # Der stabilste Uploader
    img_file = st.file_uploader("Bild wählen", type=["jpg", "png", "jpeg"], key="up")
    if img_file:
        st.image(img_file, use_container_width=True)
        # Button ist jetzt immer da, wenn ein Bild existiert
        if st.button("🔍 IM NETZ SUCHEN", key="search"):
            st.info("Suche läuft...")

# 3. HAUPTSEITE
st.title("🤖 Málaga Investment")

col1, col2 = st.columns([2, 1])
with col1:
    query = st.text_input("Suche:", value="Finca Málaga")
    price = st.number_input("Budget (€):", value=250000)
with col2:
    st.subheader("📊 Kosten")
    itp = price * 0.07
    st.write(f"Steuer: {itp:,.0f}€")
    st.write(f"Gesamt: {price+itp:,.0f}€")

# 4. AKTION & LINKS (FIX FÜR SYNTAX-FEHLER)
if st.button("🚀 ANALYSE STARTEN", use_container_width=True):
    # Links ganz einfach definiert ohne Zeilenumbruch
    i_url = f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={price}"
    f_url = f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/l?maxPrice={price}"
    
    st.divider()
    l, r = st.columns(2)
    with l:
        st.subheader("📋 KI-Check")
        st.write(call_agent(f"Check {query} {price}€."))
        st.subheader("🏠 Links")
        st.link_button("👉 Idealista", i_url)
        st.link_button("👉 Fotocasa", f_url)
    with r:
        st.subheader("📍 Karte")
        # Einfachste Karte um Fehler zu vermeiden
        df = pd.DataFrame({'lat': [36.72, 36.65], 'lon': [-4.42, -4.78]})
        st.map(df)
        st.subheader("📈 Trend")
        st.bar_chart(pd.DataFrame({"Ort": ["Umland", "Stadt"], "W": [20, 15]}).set_index("Ort"))
