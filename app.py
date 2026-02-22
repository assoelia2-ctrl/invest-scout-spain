import streamlit as st
import requests
import pandas as pd

# 1. KONFIGURATION
st.set_page_config(page_title="Málaga Invest Pro", layout="centered")
groq_key = st.secrets.get("GROQ_API_KEY")

# 2. KOMPAKTES INTERFACE (Preisleiste gelöscht & integriert)
st.title("🤖 Málaga Invest-Zentrale")
st.markdown("### 🔍 Objekt-Analyse")

# Anzeigen-Link und Foto-Link als Basis
anzeigen_link = st.text_input("🔗 Link zur Immobilien-Anzeige:")
g_link = st.text_input("🖼️ Google-Foto Link des Objekts:")

# Integrierte Zeile: Typ und Preis (Keine separate Preisleiste mehr)
c_typ, c_preis = st.columns([2, 1])
with c_typ:
    objekt = st.text_input("Haus-Typ/Region:", value="Finca Málaga")
with c_preis:
    preis = st.number_input("Preis (€):", value=250000, step=5000)

# Automatische Steuer-Berechnung (7% ITP Andalusien)
itp = preis * 0.07
st.success(f"💰 **Kosten-Struktur:** ITP (7%): {itp:,.0f} € | Gesamt: {preis + itp:,.0f} €")

# 3. RECHERCHE-SCHALTZENTRALE
st.subheader("🌐 Markt-Check")
r_col1, r_col2 = st.columns(2)
with r_col1:
    st.link_button("🏠 Ähnliche Angebote", 
                   f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/fincas/?precio-maximo={preis + 20000}")
with r_col2:
    search_q = f"{objekt} Málaga kaufen {preis} Euro"
    st.link_button("📸 Foto-Marktcheck", 
                   f"https://www.google.com/search?q={search_q.replace(' ', '+')}+site:idealista.com+OR+site:fotocasa.es")

# 4. DIE VOLLE ERGEBNIS-ANALYSE
st.divider()
if st.button("🚀 VOLLSTÄNDIGE ANALYSE STARTEN", use_container_width=True):
    
    # A. KI-EXPERTE (Analyse der Links & Fakten)
    st.subheader("📋 Strategische Bewertung")
    if groq_key:
        with st.spinner("KI scannt Daten..."):
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key}"}
            prompt = f"Analyse für {objekt} ({preis}€). Anzeige: {anzeigen_link}. Foto-Link: {g_link}. Fokus: Málaga."
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "system", "content": "Du bist Immobilien-Experte für Málaga."},
                             {"role": "user", "content": prompt}]
            }
            try:
                r = requests.post(url, json=payload, headers=headers, timeout=15)
                st.write(r.json()['choices'][0]['message']['content'])
            except:
                st.error("KI-Dienst antwortet verzögert. Bitte Recherche-Buttons oben nutzen.")

    # B. STANDORT-KARTE
    st.subheader("📍 Regionaler Fokus")
    st.map(pd.DataFrame({'lat': [36.721, 36.659, 37.019], 'lon': [-4.421, -4.756, -4.559]}))

    # C. MARKT-TRENDS
    st.subheader("📈 Wertzuwachs (Prognose)")
    st.bar_chart(pd.DataFrame({"Region": ["Umland", "Stadt", "Küste"], "Trend %": [22, 15, 12]}).set_index("Region"))

st.divider()
st.caption("✅ Alles aktiv: 7% ITP | Anzeigen-Check | Foto-Recherche | KI | Karte | Trends")
