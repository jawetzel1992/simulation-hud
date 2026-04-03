import streamlit as st
from openai import OpenAI
import pandas as pd

# --- NEURAL CONFIGURATION ---
# Accesses key from .streamlit/secrets.toml [26, 31]
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Neural Shield HUD", layout="wide")
st.title("🛡️ Neural Shield: Cognitive Defense")

# --- PROMPT ARCHITECTURE ---
SYSTEM_PROMPT = """
You are a 2026 Neural Propaganda Auditor. Analyze the input for logical glitches.
Output your reasoning first, then a list of detected fallacies.
Use 'GLITCH DETECTED' if the text uses manipulation tactics.
"""

# --- SCANNER INTERFACE ---
with st.form("neural_scan"):
    content = st.text_area("Input suspected propaganda:", 
                           "Everyone knows the traitor scientists are hiding the truth!")
    submitted = st.form_submit_button("Initiate Neural Link")

    if submitted:
        with st.spinner("Decoding Narrative DNA..."):
            response = client.chat.completions.create(
                model="gpt-4-turbo", # Latest 2026-ready model [15]
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": content}
                ]
            )
            analysis = response.choices[0].message.content
            
            if "GLITCH DETECTED" in analysis.upper():
                st.error("🚨 NEURAL GLITCH INTERCEPTED")
                st.markdown(f"**Brain Reasoning:**\n{analysis}")
            else:
                st.success("✅ CONTENT SECURE: No engineering markers detected.")
