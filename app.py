import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import pandas as pd
import re

# --- KONFIGURATION ---
st.set_page_config(page_title="Málaga Invest: Pro-Expert", layout="wide")

if 'doc_text' not in st.session_state:
    st.session_state['doc_text'] = ""

st.title("🛡️ Invest-Scout: Experten-Analyse")

# --- UPLOAD ---
file = st.file_uploader("Bild/Screenshot hochladen:", type=["jpg", "png", "jpeg"], key="stable_up")

if file:
    img = Image.open(file)
    # Foto-Optimierung gegen Abstürze
    if img.width > 1800 or img.height > 1800:
        img.thumbnail((1500, 1500))
    
    st.image(img, caption="Dokument geladen", use_container_width=True)
    
    if st.button("🚀 KOMPLETT-CHECK STARTEN"):
        with st.spinner("Extrahiere und analysiere Daten..."):
            try:
                # Bildverbesserung
                proc = ImageOps.grayscale(img)
                proc = ImageEnhance.Contrast(proc).enhance(2.0)
                text = pytesseract.image_to_string(proc, lang='deu+spa')
                st.session_state['doc_text'] = text
                
                # --- AUTOMATISCHE AUSWERTUNG ---
                st.divider()
                st.subheader("📋 Analyse-Bericht")
                
                # Suche nach Fläche (z.B. 12.000 m2)
                flaeche = re.findall(r'\d+[\d.,]*\s?m2', text)
                # Suche nach Preisen (€)
                preise = re.findall(r'\d+[\d.,]*\s?€', text)
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Größe", flaeche[0] if flaeche else "Nicht erkannt")
                with c2:
                    st.metric("Preis", preise[0] if preise else "Nicht erkannt")
                with c3:
                    afo_status = "✅ Erwähnt" if "AFO" in text.upper() else "⚠️ Nicht gefunden"
                    st.info(f"**AFO Status:** {afo_status}")

                # Check für Bohrbrunnen
                if any(w in text.lower() for w in ["bohrbrunnen", "pozo", "brunnen"]):
                    st.success("💧 Wasserquelle: Bohrbrunnen im Text identifiziert!")

            except Exception as e:
                st.error(f"Fehler: {e}")

# --- 2. RECHERCHE & KOMMUNIKATION ---
if st.session_state['doc_text']:
    st.divider()
    
    # Der Recherche-Button für Internet-Abgleich
    st.markdown("### 🔍 Internet-Recherche")
    if st.button("Dubletten im Internet prüfen"):
        # Wir generieren eine Google-Suche mit den wichtigsten Schlagworten aus dem Text
        search_query = "Málaga Grundstück " + " ".join(re.findall(r'\d+[\d.,]*\s?m2', st.session_state['doc_text'])[:1])
        url = f"https://www.google.com/search?q={search_query}"
        st.write(f"👉 [Hier klicken für Google-Recherche]({url})")

    # Chat-Bereich
    st.subheader("💬 Rückfragen zum Scan")
    q = st.text_input("Frag nach Details (z.B. 'Zustand Dach'):")
    if q:
        t = st.session_state['doc_text'].lower()
        if q.lower() in t:
            pos = t.find(q.lower())
            st.write(f"✅ Gefunden: ...{st.session_state['doc_text'][max(0, pos-50):pos+100]}...")
        else:
            st.write("❌ Kein Treffer im Text.")
