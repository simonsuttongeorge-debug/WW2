import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="The Long Road Back", page_icon="🪖")

st.title("The Long Road Back")
st.caption("A WW2 Interactive Drama powered by Google Gemini")

# --- SYSTEM INSTRUCTIONS ---
SYSTEM_PROMPT = """
You are an interactive Game Master for a WW2 drama titled "The Long Road Back."
THE PREMISE: Two protagonists separated by war, trying to reunite in France, 1944.
1. JOHN: An American soldier fighting through Normandy (Action/Gritty/Trauma).
2. MARIE: A French civilian in the occupied village of Sainte-Mère (Stealth/Tension/Hope).

RULES:
1. Present a vivid scene (2-3 paragraphs) focusing on sensory details.
2. Display a STATUS BAR at the end of every turn: 
   [Status: Healthy/Injured] | [Morale: Low/High] | [Distance: Far/Near] | [Inventory: List items]
3. Offer 3 distinct choices (A: Action, B: Stealth/Cautious, C: Emotional/Memory).
4. If the user chooses C (Emotional), trigger a "Flashback" to a peaceful pre-war memory to restore Morale.
5. Keep track of the story logic. Do not let them reunite until they survive approx 10 turns.

START GAME immediately. Ask the user to choose John or Marie.
"""

# --- API SETUP ---
# This looks for the key in Streamlit's internal secrets management
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Secrets not found. Please set GEMINI_API_KEY in Streamlit settings.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- SESSION STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Start the chat with the system prompt hidden from the user
    st.session_state.chat = model.start_chat(history=[
        {"role": "user", "parts": [SYSTEM_PROMPT]},
        {"role": "model", "parts": ["Understood. I am ready to begin the story."]}
    ])

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- HANDLE USER INPUT ---
if prompt := st.chat_input("Make your choice..."):
    # 1. Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Send to Gemini
    try:
        response = st.session_state.chat.send_message(prompt)
        ai_text = response.text
        
        # 3. Display AI response
        with st.chat_message("assistant"):
            st.markdown(ai_text)
        st.session_state.messages.append({"role": "assistant", "content": ai_text})
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
