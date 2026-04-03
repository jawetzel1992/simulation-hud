import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
from io import BytesIO

# 1. Initialize Neural Link
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Neural Shield HUD", layout="wide")
st.title("🛡️ Neural Shield: Cognitive Defense v2.5")

# 2. Strict Output Architecture
SYSTEM_PROMPT = """
You are a 2026 Neural Propaganda Auditor. 
Your response MUST strictly follow this exact format:

VERDICT: [Either 'PROPAGANDA DETECTED' or 'CONTENT SECURE']
Input suspected propaganda: [1-sentence summary of the input]
Brain Reasoning: [Detailed analysis of logical glitches]
List of detected fallacies: [Bulleted list of detected flaws]
"""

# 3. Form Interface
with st.form("neural_scan"):
    content = st.text_area("Input suspected propaganda:", 
                           placeholder="Paste text here or use the uploader below...")
    uploaded_file = st.file_uploader("Optional: Upload Visual Propaganda", type=['png', 'jpg', 'jpeg'])
    submitted = st.form_submit_button("Initiate Neural Link")

    if submitted:
        if not content and not uploaded_file:
            st.warning("Neural Shield requires text or an image to begin.")
        else:
            with st.spinner("Decoding Narrative DNA..."):
                message_content = [{"type": "text", "text": content if content else "Analyze the attached image."}]
                
                # 4. Image Optimizer (Forces 85-token low-res mode)
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    img = img.resize((512, 512)) 
                    buffered = BytesIO()
                    img.save(buffered, format="JPEG")
                    encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    message_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}})

                # 5. Multimodal API Call
                response = client.chat.completions.create(
                    model="gpt-5.4-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": message_content}]
                )
                
                analysis = response.choices[0].message.content
                
                # 6. Visual Alert Logic (Cleaned of citations)
                if "PROPAGANDA DETECTED" in analysis.upper():
                    st.error("🚨 NEURAL GLITCH INTERCEPTED: Propaganda Markers Found", icon="🚨")
                else:
                    st.success("✅ CONTENT SECURE: No engineering markers detected", icon="🛡️")
                
                st.divider()
                st.write(analysis)
