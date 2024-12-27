import streamlit as st
from components.chat import init_chat, show_chat

def init_session_state():
    """Initialize session state variables"""
    # Initialize chat with home page agent
    init_chat("yCkrWvHkgm")

def main():
    st.title("AI Coding Tutor")
    st.write("Welcome to your personalized AI Coding Tutor! I'm here to help you learn programming effectively.")
    
    # Initialize session state
    init_session_state()
    
    # Show features
    st.subheader("Features")
    st.write("""
    - 📚 **Learning Roadmap**: Follow a structured learning path tailored to your goals
    - 🧪 **Interactive Quizzes**: Test your knowledge with quizzes and get instant feedback
    - 📖 **Learning Resources**: Access curated resources to support your learning journey
    - 💬 **AI Chat Support**: Get help from our AI tutor anytime
    """)
    
    # Show chat interface
    show_chat("Hi! I'm your AI Coding Tutor. How can I help you today?")

if __name__ == "__main__":
    main()
