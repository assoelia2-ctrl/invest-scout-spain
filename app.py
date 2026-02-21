import streamlit as st
import pandas as pd

st.set_page_config(page_title="Invest-Scout Spain 2026", layout="wide")

# Titel-Bereich
st.title("🏠 Invest-Scout Spain")
st.caption("Dein KI-Immobilien-Agent für den spanischen Markt")

# --- SUCHE ---
with st.container():
    with st.form("pro_search"):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            stadt = st.text_input("Zielstadt / Region", "Malaga")
        with col2:
            budget = st.number_input("Budget (€)", value=300000, step=50000)
        with col3:
            typ = st.selectbox("Objekttyp", ["Wohnung", "Haus", "Penthouse"])
        
        submit = st.form_submit_button("🔍 Analyse & Suche starten")

# --- AUSWERTUNG & ERGEBNISSE ---
if submit:
    st.divider()
    
    # 1. KI-AGENT ANALYSE (Simuliert)
    st.subheader("🤖 KI-Agent Analyse")
    c1, c2, c3 = st.columns(3)
    
    # Hier nutzen wir mathematische Variablen für die Auswertung
    rendite_est = 4.8 + (budget / 1000000) # Nur ein Beispiel-Algorithmus
    
    c1.metric("Geschätzte Rendite", f"{rendite_est:.1f}%", "+0.4%")
    c2.metric("Nachfrage-Index", "Hoch", "Top-Lage")
    c3.metric("Risiko-Level", "Gering", "Sicher")

    # 2. SUCH-ERGEBNISSE MIT LINKS
    st.subheader("📍 Top Treffer & Portale")
    
    # Wir erstellen eine Liste von "echten" Such-Links
    search_url = f"https://www.idealista.com/de/buscar/venta-viviendas/{stadt.lower()}/"
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.info(f"**Aktuelle Angebote in {stadt}**")
        st.write(f"Gefundene Objekte: 142")
        st.markdown(f"[👉 Alle Objekte auf Idealista ansehen]({search_url})")

    with col_b:
        st.success("**Investment-Tipp**")
        st.write(f"In {stadt} steigen die Preise jährlich um ca. 5.2%. Ein Kauf unter {budget}€ ist aktuell lukrativ.")

    # 3. DETAILLIERTE AUSWERTUNGSTABELLE
    st.markdown("### 📊 Rendite-Prognose")
    auswertung_data = {
        "Szenario": ["Best Case", "Realistic", "Worst Case"],
        "Jahresmiete (€)": [budget*0.07, budget*0.05, budget*0.03],
        "ROI (10 J.)": ["72%", "51%", "28%"]
    }
    st.table(pd.DataFrame(auswertung_data))

else:
    st.info("Willkommen! Gib oben deine Daten ein, damit der KI-Agent den Markt scannen kann.")
