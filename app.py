import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

# 1. SETUP & AGENTEN-KONFIGURATION
st.set_page_config(page_title="Málaga Invest Pro AI", layout="wide")
groq_key = st.secrets.get("GROQ_API_KEY")

@st.cache_data(ttl=3600)
def call_groq_agent(prompt):
    if not groq_key:
        return "❌ GROQ_API_KEY fehlt!"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
    payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        return response.json()['choices'][0]['message']['content']
    except:
        return "Agent ist gerade beschäftigt. Bitte kurz warten."

# 2. HAUPT-UI
st.title("🤖 Málaga Investment-Zentrale Full Pro")

# SIDEBAR: BILD-DETEKTIV
with st.sidebar:
    st.header("👁️ Bild-Detektiv")
    uploaded_img = st.file_uploader("Objekt-Foto hochladen", type=["jpg", "png"])
    if uploaded_img:
        st.image(uploaded_img, caption="Foto für Analyse")
        st.button("🔍 Portale nach diesem Bild scannen")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 Analyse & Suche")
    user_input = st.text_input("Suchanfrage (z.B. Finca in Coín)", value="Finca bei Málaga")
    max_price = st.number_input("Budget (€)", value=250000)
    
    if st.button("🚀 Agent beauftragen", use_container_width=True):
        with st.spinner("Agent generiert Analyse, Karte und Links..."):
            # KI ANALYSE
            prompt = f"Analysiere kurz das Potenzial für {user_input} bis {max_price}€. Nenne 3 Gebiete."
            st.markdown("### 🤖 Strategie-Check")
            st.write(call_groq_agent(prompt))
            
            # ECHTE ANGEBOTE (Links) - JETZT SICHER DEFINIERT
            id_url = f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={max_price}"
            fc_url = f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/todas-las-zonas/l?maxPrice={max_price}"
            
            st.divider()
            st.subheader("🏠 Echte Live-Angebote:")
            c1, c2 = st.columns(2)
            c1.link_button("👉 Idealista Ergebnisse", id_url, use_container_width=True)
            c2.link_button("👉 Fotocasa Ergebnisse", fc_url, use_container_width=True)
            
            # INTERAKTIVE KARTE (Málaga Investment Hotspots)
            st.divider()
            st.subheader("📍 Investment-Landkarte")
            map_data = pd.DataFrame({
                'lat': [36.7213, 36.6591, 36.7196, 36.8901],
                'lon': [-4.4214, -4.7803, -4.1000, -4.5200],
                'name': ['Málaga Stadt', 'Coín (Fincas)', 'Axarquía', 'Antequera']
            })
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(latitude=36.7, longitude=-4.5, zoom=9, pitch=50),
                layers=[pdk.Layer('ScatterplotLayer', data=map_data, get_position='[lon, lat]', 
                                  get_color='[200, 30, 0, 160]', get_radius=1000, pickable=True)]
            ))

with col2:
    st.subheader("📊 Investment-Check")
    itp = max_price * 0.07
    st.table({
        "Posten": ["Preis", "ITP (7%)", "Notar", "Gesamt"],
        "Euro": [f"{max_price:,.0f}", f"{itp:,.0f}", f"{max_price*0.01:,.0f}", f"{max_price+itp+(max_price*0.01):,.0f}"]
    })
    
    st.subheader("📈 Rendite-Aussicht")
    st.line_chart(pd.DataFrame({"Jahr": [1,2,3,4,5], "Wert": [100, 105, 112, 120, 135]}).set_index("Jahr"))
