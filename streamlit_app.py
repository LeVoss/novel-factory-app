import streamlit as st
import google.generativeai as genai

# Seite konfigurieren
st.set_page_config(page_title="Logik-Detektiv", page_icon="🕵️‍♂️")

# Verbindung zum Key herstellen
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Fehlerkorrektur: Einrückung gefixt und Modellname präzisiert
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
else:
    st.error("Schlüssel fehlt in den Secrets! ❌")
    st.stop()

st.title("🕵️‍♂️ Der Logik-Detektiv")
st.write("Füttere mich mit deinem Plot, und ich finde die Löcher!")

# Eingabebereich
user_input = st.text_area("Beschreibe deine Szene oder deinen Plot-Punkt:", 
                          placeholder="z.B.: Der Held springt aus dem 10. Stock, landet sanft auf dem Asphalt und rennt sofort weiter...")

if st.button("Auf Logikfehler prüfen"):
    if user_input:
        with st.spinner('Der Detektiv kombiniert...'):
            try:
                # Prompt-Konstruktion
                prompt = f"Analysiere folgenden Roman-Plot auf Logikfehler oder unrealistische Abläufe: {user_input}"
                response = model.generate_content(prompt)
                
                st.subheader("Analyse-Ergebnis:")
                st.info(response.text)
            except Exception as e:
                st.error(f"Da ist was schiefgelaufen: {e}")
    else:
        st.warning("Bitte gib erst einen Text ein, den ich prüfen soll!")