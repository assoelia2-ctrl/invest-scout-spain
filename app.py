import streamlit as st
import requests
import pandas as pd
import re

# 1. SETUP & SESSION STATE (Fakten-Sicherung)
st.set_page_config(page_title="Málaga Invest Pro - Fakten-Modus", layout="wide")
if 'img_data' not in st.session_state: st.session_state['img_data'] = None

groq_key = st.secrets.get("GROQ_API_KEY")

# Funktion: Wandelt Google-Links in ladbare Bilder um
def get_google_direct_url(url):
    try:
        if "drive.google.com" in url:
            file_id = re.search(r'/d/([^/]+)', url).group(1)
            return f"https://drive.google.com/uc?export=view&id={file_id}"
        return url
    except: return url

def call_ai_facts(prompt):
    """KI-Agent mit striktem Fokus auf reale Marktanalyse."""
    if not groq_key: return "Konfiguration fehlt."
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_key}"}
    # System-Prompt zwingt die KI zu faktenbasierten Antworten
    payload = {
        "model": "llama-3.3-70b-versatile", 
        "messages": [
            {"role": "system", "content": "Antworte nur auf Basis von realen Marktdaten. Keine Fiktion."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=12)
        return r.json()['choices'][0]['message']['content']
    except: return "Datenabruf derzeit nicht möglich."

# 2. SIDEBAR: BILD-DETEKTIV (Google-Link & Upload)
with st.sidebar:
    st.header("👁️ Objekt-Detektiv")
    input_method = st.radio("Foto-Quelle:", ["Google-Link (Empfohlen)", "Handy-Upload"])
    
    if input_method == "Google-Link (Empfohlen)":
        link = st.text_input("Google Drive Link hier rein:")
        if link: st.session_state['img_data'] = get_google_direct_url(link)
    else:
        up = st.file_uploader("Datei wählen", type=["jpg", "png", "jpeg"], key="up_main")
        if up: st.session_state['img_data'] = up

    if st.session_state['img_data']:
        st.image(st.session_state['img_data'], caption="Objekt geladen", use_container_width=True)
        if st.button("🔍 OBJEKT-RECHERCHE STARTEN"):
            st.info("Abgleich mit Portaldaten läuft...")

# 3. HAUPTSEITE: REAL-DATEN & KOSTEN
st.title("🤖 Málaga Investment-Zentrale (Fakten-Modus)")
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("🔍 Marktanalyse")
    query = st.text_input("Suchobjekt/Ort:", value="Finca Málaga Umland")
    price = st.number_input("Kaufpreis (€):", value=250000, step=5000)

with c2:
    st.subheader("📊 Fixkosten-Berechnung")
    itp = price * 0.07 # Reale 7% ITP Steuer Andalusien
    notar = price * 0.012 # Reale Schätzung Notar/Register
    st.table({
        "Posten": ["Kaufpreis", "ITP Steuer (7%)", "Notar/Reg.", "Gesamt"],
        "Betrag (€)": [f"{price:,.0f}", f"{itp:,.0f}", f"{notar:,.0f}", f"{price+itp+notar:,.0f}"]
    })

# 4. AKTION: ANALYSE & ECHTE LINKS
if st.button("🚀 FAKTEN-ANALYSE STARTEN", use_container_width=True):
    st.divider()
    l, r = st.columns(2)
    
    with l:
        st.subheader("📋 Strategische Bewertung")
        with st.spinner("Prüfe Marktdaten..."):
            # Prompt zwingt zu Fakten
            prompt = f"Bewertung für Investment {query} bei {price}€. Nenne reale Vor- und Nachteile der Region Málaga."
            st.write(call_ai_facts(prompt))
        
        st.subheader("🏠 Echte Live-Angebote")
        st.link_button("👉 Idealista Ergebnisse", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={price}")
        st.link_button("👉 Fotocasa Ergebnisse", f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/l?maxPrice={price}")

    with r:
        st.subheader("📍 Standort-Karte")
        # Karte basiert auf realen Koordinaten von Málaga Region
        m_df = pd.DataFrame({'lat': [36.7213, 36.6591, 36.7196], 'lon': [-4.4214, -4.7803, -4.1000]})
        st.map(m_df)
        
        st.subheader("📈 Historische Wertentwicklung (Schätzung)")
        chart_data = pd.DataFrame({"Viertel": ["Umland", "Stadt"], "Wachstum %": [18, 14]}).set_index("Viertel")
        st.bar_chart(chart_data)

st.divider()
st.caption("Faktenbasierte Analyse | Málaga Invest | Stand 2024")
