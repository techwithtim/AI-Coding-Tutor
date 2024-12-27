import streamlit as st
from database import Database
from models import Resource
from datetime import datetime
from components.chat import init_chat, show_chat

# Initialize database
db = Database()

def init_session_state():    
    # Initialize chat with resources agent
    init_chat("QWODNTNOhX")

def display_resources():
    """Display all resources"""
    resources = db.get_all_resources()
    
    if not resources:
        st.info("No resources available yet. Add some using the form below!")
        return
    
    # Group resources by type
    resources_by_type = {}
    for resource in resources:
        if resource.resource_type.lower() not in resources_by_type:
            resources_by_type[resource.resource_type.lower()] = []
        resources_by_type[resource.resource_type.lower()].append(resource)
    
    # Display resources by type
    for resource_type, type_resources in resources_by_type.items():
        st.header(resource_type.title())
        for resource in type_resources:
            with st.expander(resource.name):
                st.write(resource.description)
                if resource.asset:
                    st.write(f"Link: {resource.asset}")
                st.caption(f"Added on: {resource.created_at.strftime('%Y-%m-%d')}")

def main():
    st.title("Learning Resources")
    st.write("Explore our curated collection of learning resources")
    
    # Initialize session state
    init_session_state()
    
    # Display existing resources
    display_resources()
    
    # Show chat interface at the bottom
    show_chat("Ask me about learning resources!")

if __name__ == "__main__":
    main()
