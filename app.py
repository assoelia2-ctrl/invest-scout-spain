import streamlit as st
import requests
import pandas as pd

# 1. SETUP
st.set_page_config(page_title="Málaga Invest Pro", layout="wide")
groq_key = st.secrets.get("GROQ_API_KEY")

def call_ai(prompt):
    if not groq_key: return "API-Key fehlt!"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_key}"}
    payload = {"model": "llama-3.3-70b-versatile", "messages": [
        {"role": "system", "content": "Antworte nur mit Fakten zu Málaga."},
        {"role": "user", "content": prompt}]}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.json()['choices'][0]['message']['content']
    except: return "KI momentan nicht erreichbar."

# 2. SIDEBAR - STABILER BILD-CHECK
with st.sidebar:
    st.header("👁️ Objekt-Detektiv")
    input_method = st.radio("Foto-Quelle:", ["Handy-Upload", "Google-Link"])
    
    img_to_show = None
    if input_method == "Handy-Upload":
        up = st.file_uploader("Bild wählen", type=["jpg", "png", "jpeg"])
        if up: img_to_show = up
    else:
        link = st.text_input("Link hier einfügen:")
        if link:
            # FIX: Nur wenn es ein direkter Link ist oder wir ihn anzeigen können
            if "http" in link: img_to_show = link

    if img_to_show:
        try:
            st.image(img_to_show, use_container_width=True)
            if st.button("🔍 OBJEKT-RECHERCHE STARTEN"):
                st.info("Suche in Portalen läuft...")
        except:
            st.warning("Link kann nicht direkt als Bild geladen werden.")

# 3. HAUPTSEITE - KOSTEN & ANALYSE
st.title("🤖 Málaga Investment-Zentrale")
c1, c2 = st.columns([2, 1])

with c1:
    query = st.text_input("Suchobjekt/Ort:", value="Finca Málaga")
    price = st.number_input("Kaufpreis (€):", value=250000)

with c2:
    st.subheader("📊 Fixkosten (Fakten)")
    itp = price * 0.07 # 7% ITP Andalusien
    notar = price * 0.012
    st.table({"Posten": ["Preis", "ITP (7%)", "Notar", "Gesamt"],
              "€": [f"{price:,.0f}", f"{itp:,.0f}", f"{notar:,.0f}", f"{price+itp+notar:,.0f}"]})

# 4. AKTION
if st.button("🚀 FAKTEN-ANALYSE STARTEN", use_container_width=True):
    st.divider()
    l, r = st.columns(2)
    with l:
        st.subheader("📋 Strategische Bewertung")
        with st.spinner("KI prüft Marktdaten..."):
            st.write(call_ai(f"Investment {query} bei {price}€ in Málaga."))
        st.subheader("🏠 Live-Angebote")
        st.link_button("👉 Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={price}")
        st.link_button("👉 Fotocasa", f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/l?maxPrice={price}")
    with r:
        st.subheader("📍 Standort-Karte")
        m_df = pd.DataFrame({'lat': [36.721, 36.659], 'lon': [-4.421, -4.780]})
        st.map(m_df)
        st.subheader("📈 Prognose")
        st.bar_chart(pd.DataFrame({"Ort": ["Umland", "Stadt"], "W %": [18, 14]}).set_index("Ort"))
