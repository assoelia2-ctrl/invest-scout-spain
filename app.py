import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

# 1. SETUP
st.set_page_config(page_title="Málaga Invest Pro AI", layout="wide")
groq_key = st.secrets.get("GROQ_API_KEY")

@st.cache_data(ttl=3600)
def call_groq_agent(prompt):
    if not groq_key: return "❌ Key fehlt!"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
    payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        return response.json()['choices'][0]['message']['content']
    except: return "Agent beschäftigt..."

# 2. UI - ALLES AUF EINER SEITE
st.title("🤖 Málaga Investment-Zentrale (All-in-One)")

# Oberer Bereich: Suche & Bild-Upload
col_input, col_img = st.columns([2, 1])

with col_input:
    user_input = st.text_input("Was suchst du? (z.B. Finca in Antequera)", value="Finca mit Pool Málaga")
    max_price = st.number_input("Maximales Budget (€)", value=250000, step=5000)

with col_img:
    uploaded_img = st.file_uploader("👁️ Bild-Detektiv (Foto hochladen)", type=["jpg", "png"])
    if uploaded_img:
        st.image(uploaded_img, caption="Analyse läuft...", width=150)

if st.button("🚀 Gesamtanalyse & Angebote laden", use_container_width=True):
    # ECHTE LINKS GENERIEREN
    id_url = f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={max_price}"
    fc_url = f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/todas-las-zonas/l?maxPrice={max_price}"

    # LAYOUT: LINKS (ANALYSE) & RECHTS (KOSTEN)
    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("📋 Agenten-Strategie & Gebiete")
        with st.spinner("KI wertet Markt aus..."):
            prompt = f"Analysiere Investmentpotenzial für {user_input} bis {max_price}€. Nenne 3 Top-Dörfer."
            st.write(call_groq_agent(prompt))
        
        st.divider()
        st.subheader("🏠 Echte Verkaufsanzeigen (Live-Links)")
        st.warning("Hinweis: Da sich Inserate sekündlich ändern, klicke hier für die aktuelle Live-Liste:")
        
        # Große Buttons als "Anzeigen-Ersatz"
        st.link_button(f"👉 {user_input} bis {max_price}€ auf IDEALISTA ansehen", id_url, use_container_width=True)
        st.link_button(f"👉 {user_input} bis {max_price}€ auf FOTOCASA ansehen", fc_url, use_container_width=True)

    with c2:
        st.subheader("📊 Kosten-Check")
        itp = max_price * 0.07
        st.table({
            "Posten": ["Preis", "ITP (7% Steuer)", "Notar/Register", "Gesamt"],
            "Betrag (€)": [f"{max_price:,.0f}", f"{itp:,.0f}", f"{max_price*0.01:,.0f}", f"{max_price+itp+(max_price*0.01):,.0f}"]
        })

    # UNTERER BEREICH: KARTE
    st.divider()
    st.subheader("📍 Investment-Hotspots (Provinz Málaga)")
    map_data = pd.DataFrame({
        'lat': [36.7213, 36.6591, 36.7196, 36.8901],
        'lon': [-4.4214, -4.7803, -4.1000, -4.5200]
    })
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(latitude=36.7, longitude=-4.5, zoom=8, pitch=45),
        layers=[pdk.Layer('ScatterplotLayer', data=map_data, get_position='[lon, lat]', get_color='[200, 30, 0, 160]', get_radius=2000)]
    ))
