import streamlit as st
import requests
import pandas as pd
from PIL import Image

# 1. INITIALISIERUNG & SESSION STATE (Sorgt dafür, dass nichts verschwindet)
st.set_page_config(page_title="Málaga Invest Master", layout="wide")
if 'img' not in st.session_state: st.session_state['img'] = None

groq_key = st.secrets.get("GROQ_API_KEY")

def call_ai(prompt):
    if not groq_key: return "API Key fehlt in Secrets!"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_key}"}
    payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=15)
        return r.json()['choices'][0]['message']['content']
    except: return "Agent derzeit offline."

# 2. SIDEBAR (BILD-DETEKTIV MIT SPEICHER-LOGIK)
with st.sidebar:
    st.header("👁️ Bild-Detektiv")
    up = st.file_uploader("Foto wählen", type=["jpg", "jpeg", "png"], key="main_up")
    
    if up:
        st.session_state['img'] = up
        
    if st.session_state['img']:
        st.image(st.session_state['img'], use_container_width=True)
        if st.button("🔍 IM NETZ SUCHEN", use_container_width=True):
            st.info("Suche nach Objektdaten läuft...")

# 3. HAUPTSEITE (LAYOUT & KOSTEN-CHECK)
st.title("🤖 Málaga Investment-Zentrale")

c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("🔍 Suche & Link-Analyse")
    query = st.text_input("Anfrage oder Link:", value="Finca bei Málaga")
    price = st.number_input("Budget (€)", value=250000, step=5000)

with c2:
    st.subheader("📊 Kosten-Check")
    itp = price * 0.07 # 7% ITP Steuer
    notar = price * 0.01
    st.table({
        "Posten": ["Preis", "ITP (7%)", "Notar/Reg.", "Gesamt"],
        "€": [f"{price:,.0f}", f"{itp:,.0f}", f"{notar:,.0f}", f"{price+itp+notar:,.0f}"]
    })

# 4. AKTIONEN (ANALYSE, LINKS, KARTE, TRENDS)
if st.button("🚀 ANALYSE & ANGEBOTE LADEN", use_container_width=True):
    # Echte Links ohne Zeilenumbruch-Gefahr
    id_url = f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={price}"
    fc_url = f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/l?maxPrice={price}"

    st.divider()
    res_l, res_r = st.columns(2)

    with res_l:
        st.subheader("📋 Strategische Analyse")
        with st.spinner("Agent wertet Marktdaten aus..."):
            st.write(call_ai(f"Analysiere Investmentpotenzial für {query} bis {price}€ in Málaga."))
        
        st.subheader("🏠 Echte Live-Angebote")
        st.link_button("👉 Idealista Ergebnisse", id_url, use_container_width=True)
        st.link_button("👉 Fotocasa Ergebnisse", fc_url, use_container_width=True)

    with res_r:
        st.subheader("📍 Hotspot-Landkarte")
        # Einfache Karte zur Vermeidung von Klammer-Fehlern
        m_df = pd.DataFrame({'lat': [36.72, 36.65, 36.89], 'lon': [-4.42, -4.78, -4.52]})
        st.map(m_df)
        
        st.subheader("📈 Wertsteigerung (5 Jahre)")
        chart_data = pd.DataFrame({"Viertel": ["Umland", "Stadt", "Küste"], "Trend %": [22, 15, 12]}).set_index("Viertel")
        st.bar_chart(chart_data)

st.divider()
st.caption("Málaga Invest Pro Master - Alle Systeme bereit.")
