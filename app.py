import streamlit as st
from fpdf import FPDF
import os

# Konfiguration
st.set_page_config(page_title="Andalusien Invest AI", layout="wide")

def main():
    st.title("☀️ Andalusien Real Estate AI-Expert")

    col_input, col_ai = st.columns([1.5, 1])

    with col_input:
        st.subheader("📸 Objekt-Analyse")
        Dateien = st.file_uploader("Screenshots für KI-Check hochladen", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        
        objekt_daten = []
        if Dateien:
            for i, d in enumerate(Dateien):
                with st.expander(f"Objekt {i+1} Analyse", expanded=True):
                    st.image(d, width=300)
                    
                    # KI-Checkliste Buttons
                    st.write("**KI-Schnellcheck für diesen Screenshot:**")
                    c1, c2, c3 = st.columns(3)
                    
                    check_request = ""
                    if c1.button(f"🔍 Schatten & Licht ({i})"):
                        check_request = "Analysiere den Schattenwurf auf diesem Bild. Wo ist Süden? Wie ist die Lichtsituation?"
                    if c2.button(f"🌿 Vegetation & Boden ({i})"):
                        check_request = "Welche Bepflanzung ist erkennbar? Wie wirkt der Untergrund (felsig, sandig, gepflegt)?"
                    if c3.button(f"🚗 Zufahrt & Zugang ({i})"):
                        check_request = "Wie sieht die Zufahrt aus? Asphaltiert, Schotterweg, eng oder breit genug für LKW?"

                    if check_request:
                        st.info(f"KI-Analyse läuft für: {check_request}")
                        # Hier würde die KI-Schnittstelle das Bild lesen
                        st.session_state.current_analysis = f"Ergebnis für Objekt {i+1}: Basierend auf dem Bild scheint die Zufahrt {check_request.split()[-1]} zu sein..."

                    # Manuelle Daten für PDF
                    stadt = st.text_input(f"Lage/Name ({i})", key=f"stadt_{i}")
                    preis = st.number_input(f"Preis € ({i})", key=f"preis_{i}")
                    objekt_daten.append({"stadt": stadt, "preis": preis, "file": d})

    with col_ai:
        st.subheader("🤖 KI-Berater Feedback")
        if "current_analysis" in st.session_state:
            st.success(st.session_state.current_analysis)
        else:
            st.write("Wähle links einen Analyse-Punkt aus.")
        
        st.divider()
        st.write("**Profi-Tipp für Andalusien:**")
        st.warning("Achte bei der Zufahrt auf 'Carril'-Regelungen. Viele Wege sind privat und müssen instand gehalten werden.")

if __name__ == "__main__":
    main()
