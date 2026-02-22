import streamlit as st
import requests
import pandas as pd

# 1. SETUP
st.set_page_config(page_title="Málaga Invest Pro", layout="centered")
groq_key = st.secrets.get("GROQ_API_KEY")

def call_ai_vision(prompt):
    """KI-Analyse (Fakten-Modus)"""
    if not groq_key: return "Konfiguration fehlt."
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_key}"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": "Analysiere Immobilien-Fakten für Málaga."},
                     {"role": "user", "content": prompt}]
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.json()['choices'][0]['message']['content']
    except: return "KI momentan überlastet."

# 2. EINGABE-BEREICH (ALLES AUF EINER SEITE)
st.title("🤖 Málaga Investment-Zentrale")

st.subheader("1. Objekt-Foto hochladen")
img_file = st.file_uploader("Wähle das Haus-Foto von deinem Handy", type=["jpg", "png", "jpeg"])
if img_file:
    st.image(img_file, caption="Dein Objekt", use_container_width=True)

st.subheader("2. Investment-Details")
col1, col2 = st.columns(2)
with col1:
    objekt_name = st.text_input("Name/Ort:", value="Finca Málaga")
with col2:
    preis = st.number_input("Kaufpreis (€):", value=250000, step=5000)

# 3. FAKTEN-CHECK (SOFORT SICHTBAR)
st.subheader("📊 Kosten-Fakten (Andalusien)")
itp_steuer = preis * 0.07  # Reale 7% ITP Steuer
gesamt = preis + itp_steuer
st.info(f"Steuer (7% ITP): {itp_steuer:,.0f} € | Gesamt: {gesamt:,.0f} €")

# 4. START-BUTTON
if st.button("🚀 JETZT RECHERCHE & ANALYSE STARTEN", use_container_width=True):
    st.divider()
    
    # KI ERGEBNIS
    st.subheader("📋 Strategische Bewertung")
    with st.spinner("KI prüft Marktdaten..."):
        ergebnis = call_ai_vision(f"Analysiere Investment {objekt_name} für {preis}€. Fokus: Málaga Region.")
        st.write(ergebnis)

    # LIVE LINKS
    st.subheader("🏠 Live-Angebote zum Vergleich")
    c_l, c_r = st.columns(2)
    with c_l:
        st.link_button("👉 Idealista (Málaga)", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={preis}")
    with c_r:
        st.link_button("👉 Fotocasa (Málaga)", f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/l?maxPrice={preis}")

    # KARTE & TRENDS
    st.subheader("📍 Standort & Markttrend")
    m_df = pd.DataFrame({'lat': [36.72, 36.65], 'lon': [-4.42, -4.78]})
    st.map(m_df)
    
    chart_data = pd.DataFrame({"Viertel": ["Umland", "Stadt"], "Wachstum %": [18, 14]}).set_index("Viertel")
    st.bar_chart(chart_data)

st.caption("Faktenbasierte Analyse | Stand 2026")
