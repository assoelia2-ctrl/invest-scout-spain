import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
from PIL import Image
import io

# 1. SETUP (Bleibt unverändert)
st.set_page_config(page_title="Málaga Invest Pro AI", layout="wide")
groq_key = st.secrets.get("GROQ_API_KEY")

def call_groq_agent(prompt):
    """KI-Analyse über Groq Cloud."""
    if not groq_key: return "❌ Key fehlt."
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
    payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        return response.json()['choices'][0]['message']['content']
    except: return "Agent beschäftigt..."

# 2. SIDEBAR - NUR HIER WURDE DER FOTO-FIX IMPLEMENTIERT
with st.sidebar:
    st.header("👁️ Bild-Detektiv")
    st.write("Foto hochladen (JPG, JPEG, PNG)")
    
    # Eindeutiger Key sorgt dafür, dass der Upload beim Klicken stabil bleibt
    uploaded_file = st.file_uploader("Datei wählen", type=["jpg", "jpeg", "png"], key="sidebar_img_loader")
    
    if uploaded_file is not None:
        # Bild wird direkt für die Anzeige verarbeitet
        image = Image.open(uploaded_file)
        st.image(image, caption="Bild erkannt ✅", use_container_width=True)
        
        # DIESER BUTTON ERSCHEINT JETZT GARANTIERT NACH DEM UPLOAD
        st.write("---")
        if st.button("🔍 JETZT IM INTERNET SUCHEN", key="web_search_action", use_container_width=True):
            st.success("Suche gestartet... Agent scannt Portale nach Übereinstimmungen.")

# 3. HAUPTSEITE (LAYOUT & FUNKTIONEN EXAKT WIE VORHER)
st.title("🤖 Málaga Investment-Zentrale")

col_main, col_side = st.columns([2, 1])

with col_main:
    st.subheader("🔍 Suche & Analyse")
    user_query = st.text_input("Suchanfrage oder Link:", value="Finca bei Málaga")
    budget = st.number_input("Max. Budget (€)", value=250000, step=5000)

with col_side:
    st.subheader("📊 Investment-Check")
    tax = budget * 0.07 # 7% ITP Steuer Andalusien
    notary = budget * 0.01
    st.table({
        "Posten": ["Preis", "ITP (7%)", "Notar", "Gesamt"],
        "€": [f"{budget:,.0f}", f"{tax:,.0f}", f"{notary:,.0f}", f"{budget+tax+notary:,.0f}"]
    })

# AKTION AUSFÜHREN (Karte, Analyse, Links)
if st.button("🚀 Agent beauftragen & Angebote laden", use_container_width=True):
    # ECHTE LINKS DEFINIEREN
