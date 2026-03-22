import streamlit as st
import google.generativeai as genai

# Seite konfigurieren
st.set_page_config(page_title="Profi-Logik-Detektiv", page_icon="🕵️‍♂️", layout="wide")

# Verbindung zum Key herstellen
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(available_models[0])
    except Exception as e:
        st.error(f"Fehler beim Laden: {e}")
        st.stop()
else:
    st.error("Schlüssel fehlt! ❌")
    st.stop()

st.title("🕵️‍♂️ Der Profi-Logik-Detektiv")
st.markdown("---")

# Zwei Spalten Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Dein Manuskript-Auszug")
    user_input = st.text_area("Hier den Text hineinkopieren:", height=400, 
                              placeholder="Tippe oder kopiere deine Szene hierher...")
    
    analyze_button = st.button("🔍 Tiefen-Analyse starten", use_container_width=True)

with col2:
    st.subheader("Analyse-Protokoll")
    if analyze_button and user_input:
        with st.spinner('Der Detektiv untersucht die Indizien...'):
            try:
                # Der "System-Prompt" gibt die Struktur vor
                system_instruction = """
                Du bist ein erfahrener Lektor und Logik-Experte für Romane. 
                Analysiere den folgenden Text streng auf Widersprüche. 
                Strukturiere deine Antwort IMMER in diesen Kategorien:
                1. 🌍 PHYSIK & UMGEBUNG (z.B. Lichtverhältnisse, Entfernungen)
                2. ⏱️ ZEIT & ABLAUF (z.B. unmögliche Gleichzeitigkeit)
                3. 👤 CHARAKTER-LOGIK (z.B. Wissen, das die Figur noch nicht haben kann)
                4. 💡 VERBESSERUNGSVORSCHLAG (Wie könnte man es logisch lösen?)
                Wenn du in einer Kategorie nichts findest, schreibe 'Keine Auffälligkeiten'.
                """
                
                response = model.generate_content(f"{system_instruction}\n\nText: {user_input}")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Analyse abgebrochen: {e}")
    elif analyze_button:
        st.warning("Bitte gib zuerst einen Text ein!")
    else:
        st.info("Warte auf Eingabe... Sobald du links Text einfügst und den Button drückst, erscheint hier das Protokoll.")