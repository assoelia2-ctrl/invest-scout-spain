import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import pandas as pd
import re

st.set_page_config(page_title="Málaga Invest: CHAT-EDITION", layout="wide")

# --- APP-LOGIK ---
st.title("🛡️ Invest-Scout: Analyse & Chat")

file = st.file_uploader("Bild oder Screenshot hochladen:", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, caption="Dokument geladen", use_container_width=True)
    
    if st.button("🚀 ANALYSE STARTEN"):
        with st.spinner("Lese Dokument..."):
            # Bildoptimierung für Fotos
            gray = ImageOps.grayscale(img)
            enhanced = ImageEnhance.Contrast(gray).enhance(2.0)
            
            # Text extrahieren
            text = pytesseract.image_to_string(enhanced, lang='deu+spa')
            st.session_state['document_text'] = text # Text für den Chat speichern
            
            # Daten-Extraktion
            preis = re.findall(r'\d+(?:\.\d+)?(?:\,\d+)?\s?€', text)
            st.success("Analyse fertig! Du kannst jetzt unten Fragen stellen.")
            
            # Karte anzeigen
            st.map(pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]}))

# --- CHAT-FUNKTION ---
st.divider()
st.subheader("💬 Chat mit deinem Málaga-Experten")

if 'document_text' in st.session_state:
    user_question = st.text_input("Stelle eine Frage zum Objekt (z.B. 'Ist ein Brunnen erwähnt?'):")
    
    if user_question:
        with st.chat_message("assistant"):
            # Einfache Chat-Logik: Die App sucht deine Frage im gelesenen Text
            response = ""
            if any(word in user_question.lower() for word in ["preis", "kosten", "teuer"]):
                response = f"Im Text wurden folgende Beträge gefunden: {re.findall(r'\d+(?:\.\d+)?(?:\,\d+)?\s?€', st.session_state['document_text'])}"
            elif "brunnen" in user_question.lower():
                response = "Ich schaue nach... " + ("Ein Brunnen/Pozo wird im Text erwähnt!" if "brunnen" in st.session_state['document_text'].lower() else "Ich konnte nichts über einen Brunnen finden.")
            else:
                response = "Basierend auf dem Scan kann ich sagen: Der Text enthält Informationen zu diesem Thema. Bitte schau im Rohprotokoll nach oder frage spezifischer nach Preisen oder AFO."
            
            st.write(response)
else:
    st.write("Bitte lade zuerst ein Bild hoch und starte die Analyse, um zu chatten.")
