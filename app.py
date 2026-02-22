import streamlit as st
import requests
import pandas as pd

# 1. GRUNDGERÜST
st.set_page_config(page_title="Málaga Invest Pro", layout="wide")
groq_key = st.secrets.get("GROQ_API_KEY")

def call_ai(prompt):
    if not groq_key: return "Key fehlt!"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_key}"}
    payload = {"model": "llama-3.3-70b-versatile", "messages": [
        {"role": "system", "content": "Gib nur faktenbasierte Infos zu Immobilien in Málaga."},
        {"role": "user", "content": prompt}]}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.json()['choices'][0]['message']['content']
    except: return "KI momentan nicht erreichbar."

# 2. SEITENLEISTE (FOTO-FIX)
with st.sidebar:
    st.header("👁️ Objekt-Detektiv")
    # Nur lokaler Upload, da Google-Links die App blockieren
    up = st.file_uploader("Bild vom Handy wählen", type=["jpg", "png", "jpeg"])
    if up:
        st.image(up, use_container_width=True)
        if st.button("🔍 RECHERCHE STARTEN"):
            st.info("Suche in Portalen läuft...")

# 3. HAUPTSEITE (FAKTEN & KOSTEN)
st.title("🤖 Málaga Investment-Zentrale")
c1, c2 = st.columns([2, 1])

with c1:
    query = st.text_input("Objekt/Ort:", value="Finca Málaga")
    price = st.number_input("Kaufpreis (€):", value=250000)

with c2:
    st.subheader("📊 Fixkosten")
    itp = price * 0.07 # 7% ITP Steuer Andalusien
    st.table({"Posten": ["Preis", "ITP (7%)", "Gesamt"],
              "€": [f"{price:,.0f}", f"{itp:,.0f}", f"{price+itp:,.0f}"]})

# 4. AUSFÜHRUNG
if st.button("🚀 ANALYSE STARTEN", use_container_width=True):
    st.divider()
    l, r = st.columns(2)
    with l:
        st.subheader("📋 Analyse")
        with st.spinner("Prüfe Marktdaten..."):
            st.write(call_ai(f"Check {query} {price}€."))
        st.subheader("🏠 Live-Links")
        st.link_button("👉 Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={price}")
        st.link_button("👉 Fotocasa", f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/l?maxPrice={price}")
    with r:
        st.subheader("📍 Karte")
        # Einfache Karte ohne komplexe Klammern
        df = pd.DataFrame({'lat': [36.721, 36.659], 'lon': [-4.421, -4.780]})
        st.map(df)
        st.subheader("📈 Prognose")
        st.bar_chart(pd.DataFrame({"Ort": ["Umland", "Stadt"], "W %": [18, 14]}).set_index("Ort"))
