import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Invest-Scout Spain 2026", layout="wide")
st.title("🏠 Invest-Scout Spain: KI-Immobilien-Analyst")

api_key = st.sidebar.text_input("Gemini API Key eingeben", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.header("Input & Analyse")
        uploaded_file = st.file_uploader("Bild hochladen...", type=["jpg", "jpeg", "png"])
        user_query = st.text_area("Details zum Investment:")
        analyze_button = st.button("🚀 Analyse starten")

    with col2:
        st.header("Ergebnis")
        if analyze_button:
            with st.spinner("KI arbeitet..."):
                content = [image if uploaded_file else None, user_query]
                response = model.generate_content([c for c in content if c])
                st.markdown(response.text)
else:
    st.info("Bitte Gemini API Key in der Seitenleiste eingeben.")
