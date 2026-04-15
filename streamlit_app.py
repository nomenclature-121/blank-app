import streamlit as st
from openai import OpenAI
import google.generativeai as genai
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="🎮💻 All-in-One Coding AI", page_icon="🚀", layout="wide")

st.title("🚀 All-in-One Coding AI")
st.markdown("**Game Dev • Web Dev • Any Language** | Powered by **Grok (xAI) + Gemini (Google)**")

# Sidebar
with st.sidebar:
    st.header("🔑 API Keys (stored locally)")
    xai_key = st.text_input("xAI Grok API Key", value=os.getenv("XAI_API_KEY", ""), type="password")
    google_key = st.text_input("Google Gemini API Key", value=os.getenv("GOOGLE_API_KEY", ""), type="password")
    
    st.header("⚙️ Settings")
    model_choice = st.selectbox(
        "Primary Model",
        ["Grok 4.20 (xAI) - Best for coding", "Gemini 3.1 Pro (Google)", "Compare Both"]
    )
    
    project_type = st.selectbox(
        "Project Category",
        ["Game Development", "Website / Full-Stack", "General Coding / Scripts", "Language / Engine Conversion"]
    )
    
    preferred = st.text_input("Preferred Language/Engine (optional)", placeholder="GDScript, Unity C#, Next.js TypeScript, etc.")

# Clients
@st.cache_resource
def get_grok_client(key):
    if not key: return None
    return OpenAI(api_key=key, base_url="https://api.x.ai/v1")

@st.cache_resource
def get_gemini_client(key):
    if not key: return None
    genai.configure(api_key=key)
    return genai.GenerativeModel("gemini-3.1-pro")  # Latest capable model as of 2026

grok_client = get_grok_client(xai_key)
gemini_client = get_gemini_client(google_key)

SYSTEM_PROMPT = f"""You are an elite Coding AI expert in:
- Game Development (Unity C#, Godot GDScript/C#, Pygame, Unreal C++, Phaser, etc.)
- Website & Full-Stack (Next.js 15, React, Tailwind, TypeScript, FastAPI, Node.js, Django, etc.)
- Every major programming language

Rules:
- Always output COMPLETE, ready-to-copy code with comments
- Include installation/setup steps
- Suggest next improvements/features
- Use best practices and performance tips

Today: {datetime.now().strftime('%Y-%m-%d')}
Category: {project_type}
Preferred: {preferred or 'auto'}

User will describe games or websites. Deliver production-quality results.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Describe your project (e.g. 2D platformer in Godot, Next.js portfolio site...)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_text = ""
        spinner_text = "Calling Grok + Gemini..."

        with st.spinner(spinner_text):
            if "Grok" in model_choice or model_choice == "Compare Both":
                if grok_client:
                    try:
                        completion = grok_client.chat.completions.create(
                            model="grok-4.20",   # Current flagship
                            messages=[
                                {"role": "system", "content": SYSTEM_PROMPT},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.7,
                            max_tokens=8192
                        )
                        grok_out = completion.choices[0].message.content
                        response_text += f"### 🟢 **Grok 4.20 Response**\n\n{grok_out}\n\n---\n\n"
                    except Exception as e:
                        response_text += f"❌ Grok error: {str(e)}\n\n"

            if "Gemini" in model_choice or model_choice == "Compare Both":
                if gemini_client:
                    try:
                        gemini_out = gemini_client.generate_content(
                            f"{SYSTEM_PROMPT}\n\nUser request: {prompt}"
                        )
                        response_text += f"### 🔵 **Gemini 3.1 Pro Response**\n\n{gemini_out.text}\n\n"
                    except Exception as e:
                        response_text += f"❌ Gemini error: {str(e)}\n\n"

            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# Quick examples
st.divider()
st.subheader("🔥 One-click starters")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("2D Platformer - Godot 4 (GDScript)"):
        st.session_state.messages.append({"role": "user", "content": "Create a complete 2D platformer game in Godot 4 using GDScript. Include player movement, jumping, double jump, coin collection, simple enemy AI, and scene transition."})
        st.rerun()

with col2:
    if st.button("Next.js 15 Portfolio Website"):
        st.session_state.messages.append({"role": "user", "content": "Build a modern dark-mode personal portfolio website using Next.js 15 App Router, Tailwind CSS, TypeScript, Framer Motion for animations, and a working contact form."})
        st.rerun()

with col3:
    if st.button("Unity C# Endless Runner"):
        st.session_state.messages.append({"role": "user", "content": "Create a full Unity C# endless runner game with procedural obstacle generation, score system, high score persistence, jump mechanics, and mobile touch controls."})
        st.rerun()

st.caption("Your personal Coding AI for games & websites • Integrated with Grok & Gemini")