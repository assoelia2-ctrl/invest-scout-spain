import streamlit as st
import pandas as pd
import time
import random

# 1. Agenten-Konfiguration
st.set_page_config(page_title="KI-Immo-Agent Spain 2026", layout="wide", page_icon="🤖")

# Design-Anpassung
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .stMetric { background-color: #1e2130; border-radius: 10px; padding: 15px; border: 1px solid #C5FF00; }
    .agent-box { background-color: #262730; padding: 20px; border-radius: 15px; border-left: 5px solid #C5FF00; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Funktionen des Agenten (Fähigkeiten)
def simuliere_markt_scan(stadt, budget):
    """Fähigkeit: Durchsucht Portale nach echten Angeboten"""
    objekte = [
        {"Name": f"Penthouse {stadt} Playa", "Preis": budget * 0.92, "Rendite": 5.8, "Lage": "A+", "Zustand": "Neuwertig", "Typ": "Penthouse"},
        {"Name": f"Finca {stadt} Hinterland", "Preis": budget * 0.75, "Rendite": 4.2, "Lage": "B", "Zustand": "Renovierungsbedürftig", "Typ": "Finca"},
        {"Name": f"Modern Apartment {stadt}", "Preis": budget * 0.88, "Rendite": 6.1, "Lage": "A", "Zustand": "Saniert", "Typ": "Wohnung"},
        {"Name": f"Investment-Studio {stadt}", "Preis": budget * 0.50, "Rendite": 7.2, "Lage": "C", "Zustand": "Gepflegt", "Typ": "Studio"}
    ]
    return pd.DataFrame(objekte)

def ki_bewertung(row):
    """Fähigkeit: Bewertet Immobilien nach Investment-Logik"""
    score = (row['Rendite'] * 1.5) + (10 if row['Lage'] == "A+" else 5)
    return round(min(score, 10), 1)

# 3. Das Agenten-Interface
st.title("🤖 KI-Agent: Immobilien-Scout Spanien")
st.markdown("---")

# Eingabe-Sektion (Dashboard-Stil)
with st.container():
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        stadt = st.text_input("Zielregion (z.B. Malaga, Alicante, Mallorca)", "Malaga")
    with col2:
        budget = st.number_input("Dein Investitions-Budget (€)", value=350000, step=10000)
    with col3:
        prioritaet = st.selectbox("Hauptziel", ["Maximale Rendite", "Sicherer Werterhalt", "Ferienvermietung"])
    
    suche_starten = st.button("🚀 Agenten-Suche & Vergleich starten", use_container_width=True)

# 4. Der Agent in Aktion
if suche_starten:
    st.divider()
    
    # Der Agent "spricht" mit dir
    with st.status("KI-Agent aktiv: Scanne Markt...", expanded=True) as status:
        st.write(f"📡 Verbinde zu Portalen in {stadt}...")
        time.sleep(1)
        st.write("📊 Daten werden gefiltert und verglichen...")
        df = simuliere_markt_scan(stadt, budget)
        df['KI-Score'] = df.apply(ki_bewertung, axis=1)
        time.sleep(1)
        st.write("🧠 Investment-Bewertung wird kalkuliert...")
        status.update(label="Analyse abgeschlossen!", state="complete", expanded=False)

    # FUNKTION: VERGLEICHEN
    st.subheader("⚖️ Direkter Objekt-Vergleich")
    # Markiere das beste Objekt
    st.dataframe(df.sort_values(by="KI-Score", ascending=False), use_container_width=True, hide_index=True)

    # FUNKTION: BEWERTEN & EMPFEHLEN
    st.markdown("---")
    top_objekt = df.loc[df['KI-Score'].idxmax()]
    
    st.markdown(f"""
        <div class="agent-box">
            <h3>💡 Meine Experten-Empfehlung</h3>
            <p>Nach Analyse von {len(df)} Objekten empfehle ich das <b>{top_objekt['Name']}</b>.</p>
            <ul>
                <li><b>Rendite:</b> {top_objekt['Rendite']}% (über Marktdurchschnitt)</li>
                <li><b>Lage:</b> {top_objekt['Lage']} (hohes Wertsteigerungspotenzial)</li>
                <li><b>KI-Investment-Score:</b> {top_objekt['KI-Score']}/10</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # FUNKTION: HANDLUNG (Links)
    st.subheader("🔗 Jetzt handeln")
    c1, c2 = st.columns(2)
    idealista_url = f"https://www.idealista.com/de/buscar/venta-viviendas/{stadt.lower()}/"
    
    c1.info(f"**Markt-Übersicht:** [Alle Angebote in {stadt} auf Idealista]({idealista_url})")
    c2.success(f"**Agenten-Tipp:** Kontaktiere lokale Makler für Off-Market Deals in {stadt}.")

else:
    # Start-Zustand
    st.info("Willkommen! Ich bin dein KI-Agent. Gib oben deine Suchkriterien ein, damit ich für dich den Markt scannen und bewerten kann.")
