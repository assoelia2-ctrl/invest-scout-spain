import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Málaga Invest: Letzter Versuch")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("Key fehlt!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# WIR PROBIEREN JETZT EIN ANDERES MODELL
# Falls Flash (404) nicht geht, nehmen wir das Pro-Modell
try:
    model = genai.GenerativeModel('gemini-1.5-pro')
except:
    model = genai.GenerativeModel('gemini-pro-vision')

st.title("🛡️ Invest-Scout: Modell-Wechsel")

f = st.file_uploader("Bild:", type=["jpg", "png", "jpeg"])

if f and st.button("🚀 ANALYSE"):
    with st.spinner("Suche funktionierendes Modell..."):
        try:
            img = Image.open(f)
            # Wir halten den Prompt simpel für den Test
            res = model.generate_content(["Was ist der AFO Status hier?", img])
            st.markdown(res.text)
        except Exception as e:
            st.error(f"Google sagt immer noch Nein: {e}")
            st.info("Das bedeutet: Dein Google Account/Key ist für KI-Modelle in dieser Region noch nicht aktiv.")
