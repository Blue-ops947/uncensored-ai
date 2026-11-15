import streamlit as st
import requests

st.set_page_config(page_title="UNCENSORED AI", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #05050A; }
    .glowing-title {
        font-size: 3.5em; font-weight: 900; color: #ffffff; text-align: center;
        letter-spacing: 2px;
        text-shadow: 0 0 10px #00F0FF, 0 0 20px #00F0FF, 0 0 40px #00F0FF, 0 0 80px #00F0FF;
        margin-bottom: 5px;
    }
    .quote-text {
        text-align: center; color: #FF003C; font-style: italic;
        font-size: 1.1em; margin-bottom: 40px; font-weight: 600;
    }
    h1, h2, h3, p, span, div { color: #ffffff !important; }
    
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #0D0E15 !important; border: 1px solid #FF003C; border-radius: 8px; padding: 15px;
    }
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #0D0E15 !important; border: 1px solid #00F0FF; border-radius: 8px; padding: 15px;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.15);
    }
    .stChatInputContainer textarea {
        background-color: #0D0E15 !important; color: white !important;
        border: 1px solid #00F0FF !important; box-shadow: inset 0 0 10px rgba(0, 240, 255, 0.1);
    }
    #MainMenu, footer {visibility: hidden;}

    /* Yahan se Bubble Typing Animation shuru hoti hai */
    @keyframes typing {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animated-bubble {
        animation: typing 0.5s ease-out forwards;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="glowing-title">UNCENSORED AI</div>', unsafe_allow_html=True)
st.markdown('<div class="quote-text">"AI is the tool. Intention is the operator."</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    avatar_icon = "👤" if msg["role"] == "user" else "⚡"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(f'<div class="animated-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

prompt = st.chat_input("Enter your prompt here...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(f'<div class="animated-bubble">{prompt}</div>', unsafe_allow_html=True)

    api_key = "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"
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    # Naya Venice Uncensored + Free Model
    data = {
        "model": "venice/uncensored:free",
        "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    }

    with st.chat_message("assistant", avatar="⚡"):
        placeholder = st.empty()
        placeholder.markdown('<div class="animated-bubble">*(Bypassing filters...)*</div>', unsafe_allow_html=True)
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            
            if 'choices' in result:
                ai_reply = result['choices'][0]['message']['content']
                placeholder.markdown(f'<div class="animated-bubble">{ai_reply}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            else:
                placeholder.error(f"API Error: {result}")
        except Exception as e:
            placeholder.error(f"System Error: {str(e)}")