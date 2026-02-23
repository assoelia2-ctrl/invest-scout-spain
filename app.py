import streamlit as st
from fpdf import FPDF
import google.generativeai as genai
import os
from PIL import Image
import urllib.parse

# --- 1. APP KONFIGURATION ---
st.set_page_config(page_title="Andalusien Invest Master Pro", layout="wide")

# Sidebar für API-Key und Einstellungen
with st.sidebar:
    st.header("⚙️ Konfiguration")
    api_key = st.text_input("Gemini API Key eingeben", type="password")
    st.info("Kein Key? Hol dir einen bei: aistudio.google.com")
    st.markdown("---")
    st.write("v4.0 - Bauplatz & Investment Check")

# KI-Modell Setup
if api_key:
    genai.configure(api_key=api_key)
    # Wir nutzen das neueste 1.5-Flash Modell für schnelle Bildanalyse
    model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. DIE SPEZIALISIERTE ANALYSE-FUNKTION (REQUIREMENT TEXT) ---
def analyze_image(img):
    """
    Dies ist der Requirement-Text. Er definiert das Verhalten der KI.
    """
    prompt = """
    ROLLE: 
    Du bist ein zertifizierter Baugutachter und Investment-Analyst für Immobilien in Andalusien, Spanien. 
    Analysiere diesen Screenshot technisch und investitionsorientiert.

    DEINE CHECKLISTE (REQUIREMENTS):
    1. SUBSTANZ & BAUWEISE: 
       - Suche nach Feuchtigkeitsrändern (Salpeter) an den unteren Fassadenbereichen. 
       - Prüfe den Zustand der Dachziegel (Tejas Arabes) und das Vorhandensein von Regenrinnen.
       - Identifiziere statische Risse (Fisuras) über Fenstern oder an Gebäudeecken.

    2. TOPOGRAPHIE & ZUFAHRT:
       - Prüfe die Zufahrt: Ist es eine asphaltierte Straße oder ein Feldweg (Carril)? 
       - Bewerte die Steigung und Breite (Befahrbarkeit für LKW/Baumaschinen).
       - Vegetation: Erkennst du geschützte Bäume (Oliven, Korkeichen/Alcornoques)?

    3. SCHATTEN & ENERGIE:
       - Analysiere den Schattenwurf von Nachbargebäuden oder nahen Bergen.
       - Schätze die Eignung der Dachflächen für Photovoltaik (Süd-Ausrichtung).

    4. INFRASTRUKTUR-DETEKTION:
       - Siehst du Anzeichen für Strommasten, Wassertanks (Depósitos) oder Glasfaser-Boxen?

    STRUKTUR DER ANTWORT:
    Gliedere deine Antwort zwingend in folgende Abschnitte:
    🚩 KRITISCHE RISIKEN (Baulich & Rechtliche Anzeichen)
    ✨ INVESTITIONS-CHANCEN (Potenzial zur Wertsteigerung)
    💶 KOSTEN-SCHÄTZUNG (Grobe Richtung für sofortige Instandsetzung/Modernisierung)
    """
    response = model.generate_content([prompt, img])
    return response.text

# --- 3. HAUPTPROGRAMM ---
def main():
    st.title("☀️ Andalusien Real Estate AI-Master")
    
    # Layout: Recherche (Links) und Analyse (Rechts)
    col_search, col_analysis = st.columns([1, 2])

    with col_search:
        st.subheader("🔍 Marktsuche")
        search_query = st.text_input("Region/Objekt suchen", placeholder="z.B. Finca Malaga Meerblick")
        if search_query:
            q_encoded = urllib.parse.quote(search_query)
            st.link_button("🏠 Idealista Suche öffnen", f"https://www.idealista.com/buscar/venta-viviendas/{q_encoded}/")
            st.link_button("🏢 Fotocasa Suche öffnen", f"https://www.fotocasa.es/es/comprar/viviendas/{q_encoded}/l/1")

    with col_analysis:
        st.subheader("📸 Objekt-Check & Gutachten")
        Dateien = st.file_uploader("Screenshots hochladen", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

        objekt_daten = []

        if Dateien:
            if not api_key:
                st.warning("⚠️ Bitte gib zuerst deinen API-Key in der Sidebar ein!")
            
            for i, d in enumerate(Dateien):
                st.markdown(f"---")
                c1, c2 = st.columns([1, 1.2])
                
                img = Image.open(d)
                with c1:
                    st.image(img, use_container_width=True)
                    stadt = st.text_input(f"Lage/Objektname ({i})", key=f"s_{i}")
                    preis = st.number_input(f"Kaufpreis € ({i})", key=f"p_{i}")
                
                with c2:
                    if st.button(f"🔍 KI-Gutachten anfordern ({i})", key=f"btn_{i}"):
                        if api_key:
                            with st.spinner("Experte untersucht das Bild..."):
                                result = analyze_image(img)
                                st.session_state[f"res_{i}"] = result
                        else:
                            st.error("API-Key fehlt!")

                    if f"res_{i}" in st.session_state:
                        st.markdown(st.session_state[f"res_{i}"])
                        objekt_daten.append({
                            "stadt": stadt,
                            "preis": preis,
                            "analyse": st.session_state[f"res_{i}"],
                            "file": d
                        })

        # PDF Generierung
        if objekt_daten and st.button("🚀 Gesamten Investment-Report als PDF speichern"):
            pdf = FPDF()
            for obj in objekt_daten:
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(0, 10, f"Dossier: {obj['stadt']}", ln=1)
                pdf.set_font("Arial", '', 12)
                pdf.cell(0, 10, f"Preis: {obj['preis']:,.2f} EUR", ln=1)
                pdf.ln(5)
                pdf.set_font("Arial", '', 10)
                # Entferne Markdown-Symbole für sauberes PDF
                clean_text = obj['analyse'].replace('*', '').replace('#', '')
                pdf.multi_cell(0, 6, clean_text)

            pdf.output("Andalusien_Invest_Report.pdf")
            st.success("PDF Dossier fertig!")
            with open("Andalusien_Invest_Report.pdf", "rb") as f:
                st.download_button("📥 PDF Herunterladen", f, file_name="Andalusien_Invest_Report.pdf")

if __name__ == "__main__":
    main()
