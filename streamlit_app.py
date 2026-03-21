import streamlit as st
import google.generativeai as genai

# Verbindung zum Key herstellen
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    st.sidebar.success("Schlüssel geladen! ✅")
else:
    st.sidebar.error("Schlüssel fehlt! ❌")

st.title("🕵️‍♂️ Der Logik-Detektiv")