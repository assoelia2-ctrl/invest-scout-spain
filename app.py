import streamlit as st
import pandas as pd

st.set_page_config(page_title="Invest-Scout Spain 2026", layout="wide")

st.title("🏠 Invest-Scout Spain")

# --- EINGABEBEREICH DIREKT IM HAUPTFENSTER ---
st.subheader("Deine Suchkriterien")
col_input1, col_input2 = st.columns(2)

with col_input1:
    # Textfeld für die Stadt oder Region
    stadt_eingabe = st.text_input("Welche Stadt suchst du?", "Malaga")
    region = st.selectbox("Region", ["Costa del Sol", "Costa Blanca", "Mallorca"])

with col_input2:
    budget = st.number_input("Dein Budget (€)", value=500000, step=10000)
    immobilientyp = st.multiselect("Objekttyp", ["Wohnung", "Haus", "Finca"], default=["Wohnung"])

st.markdown("---")

# --- ERGEBNISSE ---
st.subheader(f"Gefundene Objekte in {stadt_eingabe}")
st.info(f"Suche nach {', '.join(immobilientyp)} bis {budget:,} €...")

# Beispiel-Daten
data = {
    "Stadt": [stadt_eingabe, "Estepona", "Marbella"],
    "Preis": [budget - 20000, 320000, 450000],
    "Rendite": ["4.8%", "5.2%", "4.5%"]
}
df = pd.DataFrame(data)
st.table(df)

# Investment-Check
st.subheader("Investment-Check")
st.metric(label="Markttrend", value="Steigend", delta="3.2% p.a.")
