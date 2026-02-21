import streamlit as st
import pandas as pd

st.set_page_config(page_title="Invest-Scout Spain 2026", layout="wide")

st.title("🏠 Invest-Scout Spain")

# --- FORMULAR FÜR DIE SUCHE ---
with st.form("such_formular"):
    st.subheader("Deine Suchkriterien")
    
    col1, col2 = st.columns(2)
    
    with col1:
        stadt_eingabe = st.text_input("Welche Stadt suchst du?", "Malaga")
        region = st.selectbox("Region", ["Costa del Sol", "Costa Blanca", "Mallorca"])
    
    with col2:
        budget = st.number_input("Dein Budget (€)", value=500000, step=10000)
        objekttyp = st.multiselect("Objekttyp", ["Wohnung", "Haus", "Finca"], default=["Wohnung"])
    
    # Der "Suche starten" Button
    submit_button = st.form_submit_button(label="🔍 Suche starten")

# --- LOGIK: WAS PASSIERT NACH DEM KLICK? ---
if submit_button:
    st.markdown("---")
    st.subheader(f"Ergebnisse für {stadt_eingabe}")
    
    # Hier simulieren wir die Filterung der Daten
    st.success(f"Suche abgeschlossen! Zeige Objekte für {region} bis {budget:,} €.")
    
    # Beispiel-Ergebnisliste (Hier könnte man später eine echte CSV filtern)
    data = {
        "Stadt": [stadt_eingabe, stadt_eingabe, "Umfeld"],
        "Typ": [objekttyp[0] if objekttyp else "Alle", "Haus", "Wohnung"],
        "Preis": [budget - 15000, budget - 50000, 250000],
        "Rendite": ["4.9%", "5.1%", "4.2%"]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True) # Schickere Tabelle

    # Investment-Check Metriken
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("Markttrend", "Steigend", "3.2%")
    with col_m2:
        st.metric("Verfügbarkeit", "12 Objekte", "-2")
else:
    # Hinweis, wenn noch nicht gesucht wurde
    st.info("Bitte gib deine Kriterien ein und klicke auf 'Suche starten'.")
