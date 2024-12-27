import streamlit as st
from parlant.client import ParlantClient

def init_chat(agent_id: str):
    """Initialize chat session state with specific agent ID"""
    # Always reinitialize messages when switching agents
    if "current_agent_id" not in st.session_state or st.session_state.current_agent_id != agent_id:
        st.session_state.messages = []
        st.session_state.current_agent_id = agent_id
        
    if "parlant_session" not in st.session_state:
        client = ParlantClient(base_url="http://localhost:8800")
        agent = client.agents.retrieve(agent_id)
        session = client.sessions.create(agent_id=agent_id, allow_greeting=False)
        st.session_state.parlant_session = session
        st.session_state.parlant_client = client

def show_chat(prompt_placeholder: str = "Ask me anything!", extra_info: str = ""):
    """Display chat interface with custom prompt placeholder"""
    st.markdown("---")
    st.subheader("Chat with AI Tutor")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"].split("*&()")[0])
    
    # Chat input
    if prompt := st.chat_input(prompt_placeholder):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt + f"*&() Use this extra information to provide better context and details: {extra_info}"})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Get AI response
        customer_event = st.session_state.parlant_client.sessions.create_event(
            session_id=st.session_state.parlant_session.id,
            source="customer",
            kind="message",
            message=prompt,
        )

        agent_event, *_ = st.session_state.parlant_client.sessions.list_events(
            session_id=st.session_state.parlant_session.id,
            source="ai_agent",
            kinds="message",
            min_offset=customer_event.offset,
        )
        
        # Display AI response
        assert agent_event.data
        agent_message = agent_event.data["message"]
        st.session_state.messages.append({"role": "assistant", "content": agent_message})
        with st.chat_message("assistant"):
            st.markdown(agent_message)
