import streamlit as st
import pandas as pd

# 1. Konfiguration der Seite (muss ganz oben stehen)
st.set_page_config(page_title="Invest-Scout Spain 2026", layout="wide")

# 2. Titel und Logo
st.title("🏠 Invest-Scout Spain")
st.markdown("---")

# 3. Seitenleiste (Sidebar) für Filter
st.sidebar.header("Filter-Optionen")

region = st.sidebar.selectbox(
    "Region auswählen",
    ["Costa del Sol", "Costa Blanca", "Mallorca", "Kanaren", "Madrid/Barcelona"]
)

budget = st.sidebar.slider("Max. Budget (€)", 100000, 2000000, 500000, step=50000)

immobilientyp = st.sidebar.multiselect(
    "Objekttyp",
    ["Wohnung", "Haus/Villa", "Finca", "Grundstück"],
    default=["Wohnung", "Haus/Villa"]
)

# 4. Hauptbereich: Die "Fenster" (Layout mit Spalten)
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"Gefundene Objekte in {region}")
    # Platzhalter für Daten (hier würde normalerweise dein API-Call oder CSV-Import stehen)
    st.info(f"Suche nach {', '.join(immobilientyp)} bis {budget:,} €...")
    
    # Beispiel-Tabelle
    data = {
        "Stadt": ["Marbella", "Estepona", "Malaga"],
        "Preis": [450000, 320000, 280000],
        "Rendite": ["4.5%", "5.2%", "4.8%"]
    }
    df = pd.DataFrame(data)
    st.table(df)

with col2:
    st.subheader("Investment-Check")
    st.metric(label="Markttrend", value="Steigend", delta="3.2% p.a.")
    st.write("Hier kannst du Berechnungen durchführen.")
    
    if st.button("Rendite berechnen"):
        st.success("Berechnung wird gestartet...")

# 5. Footer / Status
st.sidebar.markdown("---")
st.sidebar.write("✅ System-Status: Online")
