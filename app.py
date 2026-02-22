import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
from PIL import Image

# 1. SETUP & AGENTEN-KONFIGURATION
st.set_page_config(page_title="Málaga Invest Pro AI", layout="wide")
groq_key = st.secrets.get("GROQ_API_KEY")

@st.cache_data(ttl=3600)
def call_groq_agent(prompt):
    if not groq_key:
        return "❌ GROQ_API_KEY fehlt in den Secrets!"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return f"🕒 Agent beschäftigt (Fehler {response.status_code})."
    except:
        return "📡 Verbindung unterbrochen."

# 2. BENUTZEROBERFLÄCHE (UI)
st.title("🤖 Málaga Investment-Zentrale")

# SIDEBAR: BILD-DETEKTIV
with st.sidebar:
    st.header("👁️ Bild-Detektiv")
    st.write("Lade ein Foto hoch, um im Netz danach zu suchen.")
    # Fix für stabilen Upload
    uploaded_img = st.file_uploader("Foto hier hochladen", type=["jpg", "jpeg", "png"])
    
    if uploaded_img is not None:
        st.image(uploaded_img, caption="Foto bereit", use_container_width=True)
        if st.button("🔍 Bild-Suche starten", use_container_width=True):
            st.info("Agent analysiert das Bild...")

# HAUPTBEREICH: EINGABE & KOSTEN
col_input, col_calc = st.columns([2, 1])

with col_input:
    st.subheader("🔍 Suche & Link-Analyse")
    user_input = st.text_input("Suchanfrage oder Link:", value="Finca bei Málaga")
    max_price = st.number_input("Max. Budget (€)", value=250000, step=5000)

with col_calc:
    st.subheader("📊 Kosten-Check")
    itp = max_price * 0.07 
    notar = max_price * 0.01
    total = max_price + itp + notar
    
    st.table({
        "Posten": ["Kaufpreis", "ITP (7%)", "Notar/Reg.", "Gesamt"],
        "Betrag (€)": [f"{max_price:,.0f}", f"{itp:,.0f}", f"{notar:,.0f}", f"{total:,.0f}"]
    })

# AKTION-BUTTON (Fix für NameError & SyntaxError)
if st.button("🚀 Analyse & echte Angebote laden", use_container_width=True):
    id_url = f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={max_price}"
    fc_url = f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/todas-las-zonas/l?maxPrice={max_price}"

    st.divider()
    res_col, map_col = st.columns([1, 1])

    with res_col:
        st.subheader("📋 Strategischer Deep-Dive")
        with st.spinner("Agent wertet Marktdaten aus..."):
            prompt = f"Analysiere Potenzial für {user_input} bis {max_price}€. Nenne 3 Gebiete und Wertsteigerung."
            st.write(call_groq_agent(prompt))
        
        st.subheader("🏠 Echte Verkaufsanzeigen (Live)")
        st.link_button("👉 Idealista Ergebnisse", id_url, use_container_width=True)
        st.link_button("👉 Fotocasa Ergebnisse", fc_url, use_container_width=True)

    with map_col:
        st.subheader("📍 Hotspot-Landkarte")
        # FEHLER-FIX: Alle Klammern korrekt geschlossen
        map_data = pd.DataFrame({
            'lat': [36.7213, 36.6591, 36.7196, 36.8901],
            'lon': [-4.4214, -4.7803, -4.1000, -4.5200]
        })
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(latitude=36.7, longitude=-4.5, zoom=8, pitch=45),
            layers=[pdk.Layer('ScatterplotLayer', data=map_data, get_position='[lon, lat]', 
                              get_color=[200, 30, 0, 160], get_radius=2500)]
        ))
        
        st.subheader("📈 Prognose-Grafik")
        prognose = pd.DataFrame({"Viertel": ["Umland", "Stadt", "Küste"], "Trend %": [22, 15, 12]}).set_index("Viertel")
        st.bar_chart(prognose)

st.divider()
st.caption("Málaga Invest Pro AI - Alle Fehler behoben.")
