import streamlit as st
from fpdf import FPDF
import os
import urllib.parse

st.set_page_config(page_title="Andalusien Invest Cockpit Pro", layout="wide")

def main():
    st.title("☀️ Andalusien Real Estate Cockpit")
    st.markdown("---")
    
    # Layout: Links Analyse, Rechts KI-Chat
    col_main, col_chat = st.columns([2, 1])

    with col_main:
        st.subheader("📸 1. Objekt-Upload & Daten")
        Dateien = st.file_uploader("Screenshots hochladen", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        objekt_liste = []

        if Dateien:
            for i, d in enumerate(Dateien):
                with st.expander(f"Objekt {i+1}: {d.name}", expanded=(i == len(Dateien)-1)):
                    c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
                    with c1: prov = st.selectbox(f"Provinz", ["Almeria", "Cadiz", "Cordoba", "Granada", "Huelva", "Jaen", "Malaga", "Sevilla"], index=6, key=f"p{i}")
                    with c2: stadt = st.text_input(f"Stadt/Lage", placeholder="z.B. Sevilla Triana", key=f"s{i}")
                    with c3: preis = st.number_input(f"Preis €", value=0.0, step=5000.0, key=f"pr{i}")
                    with c4: flaeche = st.number_input(f"m²", value=0.0, step=1.0, key=f"m{i}")
                    
                    if stadt and preis > 0:
                        objekt_liste.append({"prov": prov, "stadt": stadt, "preis": preis, "flaeche": flaeche, "file": d})

            if objekt_liste:
                st.markdown("---")
                st.subheader("📊 2. Live-Zusammenfassung & Recherche")
                
                # Tabelle mit Recherche-Links
                for o in objekt_liste:
                    itp = o["preis"] * 0.07
                    total = o["preis"] + itp + (o["preis"] * 0.015)
                    
                    # Spalten für die Live-Vorschau
                    v1, v2, v3, v4 = st.columns([2, 1, 1, 1])
                    with v1: st.write(f"**{o['prov']}: {o['stadt']}**")
                    with v2: st.write(f"{o['preis']:,.0f} €")
                    with v3: st.write(f"Gesamt: {total:,.2f} €")
                    
                    with v4:
                        # Automatische Google-Recherche-URL bauen
                        search_term = f"site:idealista.com OR site:fotocasa.es {o['prov']} {o['stadt']} {int(o['preis'])} € {int(o['flaeche'])} m2"
                        google_url = f"https://www.google.com/search?q={urllib.parse.quote(search_term)}"
                        st.link_button("🔍 Prüfen", google_url)

                st.markdown("---")
                if st.button("🚀 Finales PDF-Dossier erstellen"):
                    with st.spinner("PDF wird generiert..."):
                        pdf = FPDF()
                        pdf.set_auto_page_break(auto=True, margin=15)
                        
                        # Titelseite
                        pdf.add_page()
                        pdf.set_font("Arial", 'B', 24)
                        pdf.ln(80)
                        pdf.cell(0, 20, "INVESTMENT-REPORT ANDALUSIEN", ln=1, align='C')
                        
                        for obj in objekt_liste:
                            pdf.add_page()
                            pdf.set_font("Arial", 'B', 16)
                            pdf.cell(0, 10, f"{obj['prov']}: {obj['stadt']}", ln=1)
                            pdf.set_font("Arial", '', 12)
                            pdf.cell(0, 10, f"Preis: {obj['preis']:,.2f} EUR | Flaeche: {obj['flaeche']} m2", ln=1)
                            
                            # Bild-Handling
                            t_name = f"temp_{obj['file'].name}"
                            with open(t_name, "wb") as f:
                                f.write(obj['file'].getbuffer())
                            pdf.image(t_name, x=10, y=40, w=180)
                            os.remove(t_name)

                        pdf.output("Andalusien_Invest_Report.pdf")
                        st.success("PDF bereit zum Download!")
                        with open("Andalusien_Invest_Report.pdf", "rb") as f:
                            st.download_button("📩 Download PDF", f, file_name="Andalusien_Invest_Report.pdf")

    # --- KI CHAT FENSTER (RECHTS) ---
    with col_chat:
        st.subheader("💬 KI-Investment-Berater")
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hola! Ich analysiere deine Objekte. Frag mich z.B.: 'Welche Provinz hat die niedrigste Steuer?'"}]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("Nachricht an KI..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            # KI Logik: Hier kann später ein API-Key rein
            response = f"Interessante Frage zu '{prompt}'. Wusstest du, dass die ITP in ganz Andalusien seit 2021 auf 7% gesenkt wurde?"
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)

if __name__ == "__main__":
    main()
