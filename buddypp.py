import streamlit as st
from textblob import TextBlob  # For basic sentiment analysis

# 1. Setup UI
st.title("💪 AI Gym Buddy")
st.write("Crush your goals and track your mood!")

# 2. State Management for Chat & Emotion Tracking
if "messages" not in st.session_state:
    st.session_state.messages = []
if "moods" not in st.session_state:
    st.session_state.moods = []

# 3. Sidebar Tracking
with st.sidebar:
    st.header("📈 Emotional Progress")
    if st.session_state.moods:
        st.line_chart(st.session_state.moods) # Simple visualization of polarity

# 4. Chat Interface
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Tell me how you're feeling about today's workout..."):
    # Analyze Sentiment
    analysis = TextBlob(prompt).sentiment.polarity
    st.session_state.moods.append(analysis)
    
    # Store User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Dynamic Motivation Logic
    if analysis > 0.3:
        response = "That's the spirit! You're in the zone. Let's push for an extra set today! 🔥"
    elif analysis < -0.1:
        response = "I hear you. Don't be too hard on yourself. Maybe a light active recovery session is better today? 🧘‍♂️"
    else:
        response = "Consistency is key. You've got this. What's the plan for the next 30 minutes? 🏋️"

    # Store & Show AI Response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
