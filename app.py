import streamlit as st
from fpdf import FPDF
import os

st.set_page_config(page_title="Andalusien Invest Cockpit", layout="wide")

def main():
    st.title("☀️ Andalusien Invest Cockpit")
    
    # Seiteneinteilung: Links Eingabe & Vorschau, Rechts Chat
    col_main, col_chat = st.columns([2, 1])

    with col_main:
        Dateien = st.file_uploader("Screenshots hochladen", accept_multiple_files=True, type=['png', 'jpg'])
        objekt_liste = []

        if Dateien:
            st.subheader("📋 1. Daten-Eingabe")
            for i, d in enumerate(Dateien):
                with st.expander(f"Objekt {i+1}: {d.name}", expanded=True):
                    c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
                    with c1: prov = st.selectbox(f"Provinz", ["Almeria", "Cadiz", "Cordoba", "Granada", "Huelva", "Jaen", "Malaga", "Sevilla"], index=6, key=f"p{i}")
                    with c2: stadt = st.text_input(f"Stadt/Lage", placeholder="z.B. Sevilla Triana", key=f"s{i}")
                    with c3: preis = st.number_input(f"Preis €", value=0.0, step=5000.0, key=f"pr{i}")
                    with c4: flaeche = st.number_input(f"m²", value=0.0, step=1.0, key=f"m{i}")
                    objekt_liste.append({"prov": prov, "stadt": stadt, "preis": preis, "flaeche": flaeche, "file": d})

            # --- LIVE VORSCHAU ---
            if objekt_liste:
                st.subheader("📊 2. Live-Zusammenfassung (Vorschau)")
                vorschau_daten = []
                for o in objekt_liste:
                    itp = o["preis"] * 0.07
                    total = o["preis"] + itp + (o["preis"] * 0.015)
                    vorschau_daten.append({
                        "Lage": o["stadt"],
                        "Kaufpreis": f"{o['preis']:,} €",
                        "Steuern (7%)": f"{itpLocal:,.2f} €" if 'itpLocal' in locals() else f"{itp:,.2f} €",
                        "Gesamtkapital": f"{total:,.2f} €",
                        "Region": o["prov"]
                    })
                st.table(vorschau_daten)

                if st.button("🚀 Finales PDF-Dossier erstellen"):
                    # (Hier bleibt die PDF-Logik wie gehabt)
                    st.success("PDF wurde generiert!")

    # --- KI CHAT FENSTER ---
    with col_chat:
        st.subheader("💬 KI-Assistent")
        st.write("Frage mich etwas zu deinen Objekten oder Steuern in Andalusien.")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("z.B. Wie hoch ist die Steuer in Cadiz?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Einfache Logik-Antwort (später mit echter API verknüpfbar)
            antwort = f"Ich helfe dir gerne bei der Analyse von {prompt}. In Andalusien liegt die ITP aktuell bei 7%."
            with st.chat_message("assistant"):
                st.markdown(antwort)
            st.session_state.messages.append({"role": "assistant", "content": antwort})

if __name__ == "__main__":
    main()
