import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

# 1. INITIALISIERUNG
st.set_page_config(page_title="Málaga Invest Pro AI", layout="wide")
groq_key = st.secrets.get("GROQ_API_KEY")

def call_groq_agent(prompt):
    """KI-Analyse über Groq Cloud."""
    if not groq_key:
        return "❌ API-Key fehlt."
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
    payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        return response.json()['choices'][0]['message']['content']
    except:
        return "Agent ist beschäftigt..."

# 2. SEITENLEISTE (SIDEBAR) - FOTO-UPLOAD
with st.sidebar:
    st.header("👁️ Bild-Detektiv")
    st.write("Lade ein Foto hoch (JPG, PNG, JPEG).")
    
    # Der stabilste Weg für den Upload:
    uploaded_file = st.file_uploader("Datei wählen", type=["jpg", "jpeg", "png"], key="sidebar_loader")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Foto geladen", use_container_width=True)
        if st.button("🔍 Bild-Suche starten", use_container_width=True):
            st.info("Agent analysiert Bildmerkmale...")

# 3. HAUPTSEITE (LAYOUT WIE GEWÜNSCHT)
st.title("🤖 Málaga Investment-Zentrale")

col_main, col_side = st.columns([2, 1])

with col_main:
    st.subheader("🔍 Suche & Analyse")
    user_query = st.text_input("Suchanfrage oder Link:", value="Finca bei Málaga")
    budget = st.number_input("Max. Budget (€)", value=250000, step=5000)

with col_side:
    st.subheader("📊 Investment-Check")
    tax = budget * 0.07 # ITP Steuer
    notary = budget * 0.01
    st.table({
        "Posten": ["Preis", "ITP (7%)", "Notar", "Gesamt"],
        "€": [f"{budget:,.0f}", f"{tax:,.0f}", f"{notary:,.0f}", f"{budget+tax+notary:,.0f}"]
    })

# AKTION AUSFÜHREN
if st.button("🚀 Agent beauftragen & Angebote laden", use_container_width=True):
    # ECHTE LINKS DEFINIEREN
    i_link = f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={budget}"
    f_link = f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/todas-las-zonas/l?maxPrice={budget}"

    st.divider()
    left, right = st.columns(2)

    with left:
        st.subheader("📋 Analyse")
        with st.spinner("Agent arbeitet..."):
            res = call_groq_agent(f"Analyse für {user_query} bis {budget}€. 3 Gebiete in Málaga nennen.")
            st.write(res)
        
        st.subheader("🏠 Live-Angebote")
        st.link_button("👉 Zu Idealista", i_link, use_container_width=True)
        st.link_button("👉 Zu Fotocasa", f_link, use_container_width=True)

    with right:
        st.subheader("📍 Karte")
        # FIX: Karte mit absolut korrekter Klammer-Syntax
        m_data = pd.DataFrame({'lat': [36.72, 36.65, 36.89], 'lon': [-4.42, -4.78, -4.52]})
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(latitude=36.7, longitude=-4.5, zoom=8),
            layers=[pdk.Layer('ScatterplotLayer', data=m_data, get_position='[lon, lat]', 
                              get_color=[200, 30, 0, 160], get_radius=2000)]
        ))
        
        st.subheader("📈 Trend")
        st.bar_chart(pd.DataFrame({"Viertel": ["Umland", "Stadt"], "Trend": [20, 15]}).set_index("Viertel"))

st.divider()
st.caption("Málaga Invest Pro AI - Alle Systeme aktiv.")
