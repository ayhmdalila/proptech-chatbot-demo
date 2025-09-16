import streamlit as st
from streamlit_chat import message
from generator import generate_response  # Import the function from generator.py
from prompts import SYSTEM_PROMPT

st.title('Demo Proptech Chatbot')

# Initialize chat history with a system prompt and a user prompt for introduction
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Introduce yourself in detail, mention who are you, whats your job, and what you can help with, it could be useful to give a very short and high level summary of the data that you have."}
    ]
    
    # Generate the bot's introduction response and append it
    bot_intro = generate_response(st.session_state['chat_history'])
    st.session_state['chat_history'].append({"role": "assistant", "content": bot_intro})

print('CHAT HISTORY:\n\n\n', st.session_state['chat_history'], '\n\n\n')

if "last_input" not in st.session_state:
    st.session_state.last_input = ''

# Function to handle input submission
def submit():
    st.session_state.last_input = st.session_state.widget  # Store input in last_input
    st.session_state.widget = ""  # Clear input field

# Display messages in normal order (newest at bottom)
message_history = st.empty()

with message_history.container():
    for i, msg in enumerate(st.session_state.chat_history[2:]):  # Do not reverse
        is_user = msg["role"] == "user"
        avatar_style = "bottts-neutral" if not is_user else "avataaars"
        with st.chat_message(msg['role']):
            st.write(msg['content'])

# Use a controlled input field with on_change to clear input
st.text_input("Write here", key="widget", on_change=submit, help="Type your message and press Enter")

# Process user input only when it changes
if st.session_state.last_input:
    st.session_state.chat_history.append({"role": "user", "content": st.session_state.last_input})
    output = generate_response(st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "assistant", "content": output})
    
    # Reset last input after processing
    st.session_state.last_input = ''
    st.rerun()  # Refresh the UI and reset the input field
