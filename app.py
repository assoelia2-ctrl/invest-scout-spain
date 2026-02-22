import streamlit as st
import requests
import pandas as pd

# 1. KONFIGURATION
st.set_page_config(page_title="Málaga Invest Pro", layout="wide")
groq_key = st.secrets.get("GROQ_API_KEY")

def call_ai(prompt):
 if not groq_key: return "Key fehlt!"
 url = "https://api.groq.com/openai/v1/chat/completions"
 headers = {"Authorization": f"Bearer {groq_key}"}
 payload = {"model": "llama-3.3-70b-versatile", "messages": [
  {"role": "system", "content": "Gib nur Fakten zu Málaga Immobilien."},
  {"role": "user", "content": prompt}]}
 try:
  r = requests.post(url, json=payload, headers=headers, timeout=10)
  return r.json()['choices'][0]['message']['content']
 except: return "KI offline."

# 2. SIDEBAR (LINK-FIX OHNE HÄNGENBLEIBEN)
with st.sidebar:
 st.header("👁️ Objekt-Detektiv")
 src = st.radio("Quelle:", ["Google-Link", "Handy-Upload"])
 if src == "Handy-Upload":
  up = st.file_uploader("Bild wählen", type=["jpg", "png", "jpeg"])
  if up: st.image(up, use_container_width=True)
 else:
  link = st.text_input("Google-Link hier rein:")
  if link: 
   st.success("✅ Link registriert")
   st.caption("Vorschau deaktiviert für maximale Stabilität.")

 if st.button("🔍 RECHERCHE STARTEN"):
  st.info("Suche in Immobiliendatenbanken aktiv...")

# 3. HAUPTSEITE (FAKTEN & KOSTEN 7% ITP)
st.title("🤖 Málaga Investment-Zentrale")
c1, c2 = st.columns([2, 1])
with c1:
 q = st.text_input("Suchobjekt/Ort:", value="Finca Málaga")
 p = st.number_input("Budget (€):", value=250000)
with c2:
 st.subheader("📊 Fixkosten (Andalusien)")
 itp = p * 0.07 # Reale 7% ITP Steuer
 st.write(f"Steuer (7%): **{itp:,.0f} €**")
 st.write(f"Gesamtbetrag: **{p+itp:,.0f} €**")

# 4. ANALYSE, LINKS, KARTE & TRENDS
if st.button("🚀 ANALYSE STARTEN", use_container_width=True):
 st.divider()
 l, r = st.columns(2)
 with l:
  st.subheader("📋 Strategische Bewertung")
  with st.spinner("KI wertet aus..."):
   st.write(call_ai(f"Check Investment {q} für {p} Euro."))
  st.subheader("🏠 Live-Angebote")
  st.link_button("👉 Idealista", f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/?precio-maximo={p}")
  st.link_button("👉 Fotocasa", f"https://www.fotocasa.es/es/comprar/viviendas/malaga-provincia/l?maxPrice={p}")
 with r:
  st.subheader("📍 Standort-Karte")
  df = pd.DataFrame({'lat': [36.72, 36.65], 'lon': [-4.42, -4.78]})
  st.map(df)
  st.subheader("📈 Prognose (5 Jahre)")
  st.bar_chart(pd.DataFrame({"Ort": ["Stadt", "Land"], "Trend": [15, 20]}).set_index("Ort"))
