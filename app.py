import streamlit as st
from fpdf import FPDF
import os

# App-Konfiguration
st.set_page_config(page_title="Andalusien Invest Pro", layout="wide")

def main():
    st.title("☀️ Andalusien Real Estate Scout")
    st.subheader("Analyse-Tool für Investment-Objekte")

    # 1. Datei-Upload
    st.info("Lade hier deine Screenshots hoch. Die Daten für Stadt und Lage kannst du unten manuell anpassen.")
    Dateien = st.file_uploader("Screenshots auswählen", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
    
    objekt_liste = []

    if Dateien:
        st.write(f"---")
        st.subheader("📋 Daten-Check & Finanz-Eingabe")
        
        # Formular für jedes Bild
        for i, d in enumerate(Dateien):
            # Versuche Daten aus Name zu lesen - falls fehlgeschlagen, leere Felder nutzen
            parts = d.name.split('.')[0].split('_')
            
            # Intelligente Vorbefüllung: Nur wenn es nach unserem Schema aussieht, 
            # ansonsten lassen wir das Feld für die Stadt leer/sauber.
            if len(parts) >= 2 and not parts[1].replace('-','').isdigit():
                v_prov = parts[0].capitalize()
                v_stadt = parts[1].replace('-', ' ')
                v_preis = float(parts[2]) if len(parts) > 2 and parts[2].replace('.','').isdigit() else 0.0
                v_flaeche = float(parts[3]) if len(parts) > 3 and parts[3].replace('.','').isdigit() else 0.0
            else:
                v_prov = "Malaga"
                v_stadt = "" # Bleibt leer, damit der technische Screenshot-Name verschwindet
                v_preis = 0.0
                v_flaeche = 0.0

            col1, col2, col3, col4 = st.columns([2, 3, 2, 1]) # Stadt-Spalte etwas breiter
            
            with col1:
                prov = st.selectbox(f"Provinz ({i})", 
                                    ["Almeria", "Cadiz", "Cordoba", "Granada", "Huelva", "Jaen", "Malaga", "Sevilla"], 
                                    index=["Almeria", "Cadiz", "Cordoba", "Granada", "Huelva", "Jaen", "Malaga", "Sevilla"].index(v_prov) if v_prov in ["Almeria", "Cadiz", "Cordoba", "Granada", "Huelva", "Jaen", "Malaga", "Sevilla"] else 6,
                                    key=f"prov_{i}")
            with col2:
                # Hier die Korrektur: Wir nutzen einen aussagekräftigen Platzhalter
                stadt = st.text_input(f"Stadt/Lage ({i})", value=v_stadt, placeholder="z.B. Marbella Zentrum oder El Palo", key=f"stadt_{i}")
            with col3:
                preis = st.number_input(f"Kaufpreis € ({i})", value=v_preis, step=5000.0, key=f"preis_{i}")
            with col4:
                flaeche = st.number_input(f"m² ({i})", value=v_flaeche, step=1.0, key=f"m2_{i}")
            
            objekt_liste.append({
                "prov": prov, 
                "stadt": stadt if stadt else "Unbekannte Lage", # Fallback für das PDF
                "preis": preis, 
                "flaeche": flaeche, 
                "file": d
            })
            st.divider()

        # 2. PDF-Generierung
        if st.button("🚀 Gesamten Andalusien-Report erstellen"):
            if not objekt_liste:
                st.error("Keine Daten vorhanden.")
                return

            with st.spinner("Kalkuliere Steuern und erstelle PDF..."):
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)

                # Gruppieren nach Provinzen
                provinzen_im_set = sorted(list(set([o["prov"] for o in objekt_liste])))
                
                # TITELSEITE
                pdf.add_page()
                pdf.set_font("Arial", 'B', 25)
                pdf.ln(80)
                pdf.cell(0, 20, "INVESTMENT-ANALYSE", ln=1, align='C')
                pdf.set_font("Arial", '', 18)
                pdf.cell(0, 15, "Immobilienmarkt Andalusien", ln=1, align='C')

                for p in provinzen_im_set:
                    pdf.add_page()
                    pdf.set_font("Arial", 'B', 20)
                    pdf.cell(0, 20, f"Region: {p}", ln=1)
                    
                    prov_objekte = [o for o in objekt_liste if o["prov"] == p]
                    
                    for obj in prov_objekte:
                        kaufpreis = obj["preis"]
                        itp_steuer = kaufpreis * 0.07 
                        nebenkosten = kaufpreis * 0.015 
                        total_investment = kaufpreis + itp_steuer + nebenkosten
                        qm_preis = kaufpreis / obj["flaeche"] if obj["flaeche"] > 0 else 0

                        pdf.set_font("Arial", 'B', 14)
                        pdf.set_fill_color(240, 240, 240)
                        pdf.cell(0, 12, f"Objekt: {obj['stadt']}", ln=1, fill=True)
                        
                        pdf.set_font("Arial", '', 11)
                        pdf.cell(95, 8, f"Kaufpreis: {kaufpreis:,.2f} EUR", 0)
                        pdf.cell(95, 8, f"Flaeche: {obj['flaeche']} m2", ln=1)
                        pdf.cell(95, 8, f"Gesamtkosten inkl. Steuer: {total_investment:,.2f} EUR", ln=1)
                        pdf.ln(5)

                        t_name = f"temp_{obj['file'].name}"
                        with open(t_name, "wb") as f:
                            f.write(obj["file"].getbuffer())
                        
                        # Bild-Check: Verhindern, dass Bilder über den Seitenrand ragen
                        pdf.image(t_name, x=10, y=pdf.get_y(), w=180)
                        pdf.ln(130) 
                        os.remove(t_name)
                        
                        if pdf.get_y() > 220:
                            pdf.add_page()

                report_name = "Andalusien_Investment_Report.pdf"
                pdf.output(report_name)
                
                st.success("✅ Report erfolgreich generiert!")
                with open(report_name, "rb") as f:
                    st.download_button("📩 PDF-Dossier herunterladen", f, file_name=report_name)

if __name__ == "__main__":
    main()
