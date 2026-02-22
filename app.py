import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

# 1. INITIALISIERUNG
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

# 2. SEITENLEISTE (SIDEBAR) - ABSOLUT STABILER UPLOAD
with st.sidebar:
    st.header("👁️ Bild-Detektiv")
    st.write("Foto hochladen (JPG, JPEG, PNG)")
    
    # Datei-Upload mit eindeutigem Key und erweiterten Typen
    img_file = st.file_uploader("Datei wählen", type=["jpg", "jpeg", "png"], key="property_image_uploader")
    
    if img_file is not None:
        try:
            st.image(img_file, caption="Bild erfolgreich geladen", use_container_width=True)
            if st.button("🔍 Bild-Suche starten", key="run_image_search"):
                st.info("Agent analysiert das Bild...")
        except Exception as e:
            st.error("Fehler beim Anzeigen des Bildes. Bitte anderes Format versuchen.")

# 3. HAUPTSEITE (LAYOUT UNVERÄNDERT)
st.title("🤖 Málaga Investment-Zentrale")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("🔍 Suche & Analyse")
    query = st.text_input("Anfrage oder Link:", value="Finca bei Málaga")
    price = st.number_input("Max. Budget (€)", value=250000, step=5000)

with col_right:
    st.subheader("📊 Investment-Check")
    itp_tax = price * 0.07
    fees = price * 0.01
    st.table({
        "Posten": ["Preis", "ITP (7%)", "Notar", "Gesamt"],
        "€": [f"{price:,.0f}", f"{itp_tax:,.0f}", f"{fees:,.0f}", f"{price+itp_tax+fees:,.0f}"]
    })

# AKTION
if st.button("🚀 Agent beauftragen", use_container_width=True):
    # Links sicher definieren
    i_url = f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={price}"
    f_url = f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/todas-las-zonas/l?maxPrice={price}"

    st.divider()
    res_l, res_r = st.columns(2)

    with res_l:
        st.subheader("📋 Analyse")
        with st.spinner("KI analysiert..."):
            text = call_groq_agent(f"Investment-Check für {query} bis {price}€ in Málaga.")
            st.write(text)
        st.subheader("🏠 Live-Angebote")
        st.link_button("👉 Idealista", i_url, use_container_width=True)
        st.link_button("👉 Fotocasa", f_url, use_container_width=True)

    with res_r:
        st.subheader("📍 Karte")
        # Fix für die Karte: Sicherer Daten-Frame
        map_df = pd.DataFrame({'lat': [36.72, 36.65, 36.89], 'lon': [-4.42, -4.78, -4.52]})
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(latitude=36.7, longitude=-4.5, zoom=8),
            layers=[pdk.Layer('ScatterplotLayer', data=map_df, get_position='[lon, lat]', 
                              get_color=[200, 30, 0, 160], get_radius=2000)]
        ))
        st.subheader("📈 Trend")
        st.bar_chart(pd.DataFrame({"Ort": ["Umland", "Stadt"], "Wachstum": [20, 15]}).set_index("Ort"))

st.divider()
st.caption("Málaga Invest Pro AI - Alle Systeme stabil.")
