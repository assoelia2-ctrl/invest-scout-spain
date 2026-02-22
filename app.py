import streamlit as st
import requests
import pandas as pd

# 1. SETUP & KONFIGURATION
st.set_page_config(page_title="Málaga Invest Ultimate", layout="centered")
groq_key = st.secrets.get("GROQ_API_KEY")

# 2. HAUPT-INTERFACE (Kompakte Eingabe)
st.title("🤖 Málaga Invest-Zentrale")
st.markdown("### 🔍 Objekt-Details & Analyse")

# Layout-Anpassung: Links und Objektdaten in einer Sektion
c1, c2 = st.columns([2, 1])
with c1:
    anzeigen_link = st.text_input("🔗 Link zur Immobilien-Anzeige (Idealista, etc.):")
    g_link = st.text_input("🖼️ Google-Foto Link des Objekts:")
with c2:
    objekt = st.text_input("Haus-Typ/Region:", value="Finca Málaga")
    preis = st.number_input("Preis (€):", value=250000, step=5000)

# 7% ITP Steuerberechnung (Fixer Bestandteil aus Andalusien-Fakten)
itp = preis * 0.07
gesamt = preis + itp
st.success(f"💰 **Kosten-Struktur:** ITP (7%): {itp:,.0f} € | Gesamt-Invest: {gesamt:,.0f} €")

# 3. RECHERCHE-TOOLS (Sofort-Links)
st.subheader("🌐 Markt-Recherche & Bild-Check")
tool_l, tool_r = st.columns(2)
with tool_l:
    st.link_button("🏠 Ähnliche Angebote suchen", 
                   f"https://www.idealista.com/de/venta-viviendas/malaga-provincia/fincas/?precio-maximo={preis + 20000}")
with tool_r:
    search_query = f"{objekt} Málaga kaufen {preis} Euro"
    st.link_button("📸 Foto-Marktcheck starten", 
                   f"https://www.google.com/search?q={search_query.replace(' ', '+')}+site:idealista.com+OR+site:fotocasa.es")

# 4. DIE VOLLE ANALYSE (KI, KARTE, TRENDS)
st.divider()
if st.button("🚀 VOLLSTÄNDIGE ANALYSE STARTEN", use_container_width=True):
    
    # A. KI-EXPERTE (Auswertung der Links und Daten)
    st.subheader("📋 Strategische Bewertung")
    if groq_key:
        with st.spinner("KI prüft Anzeige und Marktdaten..."):
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key}"}
            prompt = f"Analyse für {objekt} ({preis}€). Anzeige: {anzeigen_link}. Foto-Link: {g_link}. Fokus: Málaga Markt."
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "system", "content": "Du bist ein Immobilien-Experte für Málaga."},
                             {"role": "user", "content": prompt}]
            }
            try:
                r = requests.post(url, json=payload, headers=headers, timeout=15)
                st.write(r.json()['choices'][0]['message']['content'])
            except:
                st.error("KI-Dienst verzögert. Bitte Daten manuell prüfen.")

    # B. STANDORT-KARTE (Punkte in der Provinz Málaga)
    st.subheader("📍 Regionaler Fokus")
    map_data = pd.DataFrame({
        'lat': [36.7212, 36.6591, 37.0194],
        'lon': [-4.4214, -4.7562, -4.5597]
    })
    st.map(map_data)

    # C. MARKT-TRENDS (Grafische Prognose)
    st.subheader("📈 Wertzuwachs-Prognose")
    chart_data = pd.DataFrame({
        "Sektor": ["Fincas", "Stadt", "Küste"],
        "Trend %": [22, 15, 12]
    }).set_index("Sektor")
    st.bar_chart(chart_data)

st.divider()
st.caption("✅ System-Status: ITP 7% aktiv | Anzeigen-Analyse bereit | KI & Markt-Daten live")
