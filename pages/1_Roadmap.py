import streamlit as st
from database import Database
from models import Roadmap, Topic, SubTopic
from datetime import datetime
from components.chat import init_chat, show_chat

# Initialize database
db = Database()

def init_session_state():
    """Initialize session state variables"""
    if "checkbox_states" not in st.session_state:
        st.session_state.checkbox_states = {}
    if "show_topic_creator" not in st.session_state:
        st.session_state.show_topic_creator = False
    if "show_subtopic_creator" not in st.session_state:
        st.session_state.show_subtopic_creator = None
    
    # Initialize chat with roadmap agent
    init_chat("w5HbpNTL14")

def get_all_roadmaps():
    """Get all available roadmaps"""
    return db.get_all_roadmaps()

def save_progress(roadmap: Roadmap):
    """Save progress by updating the roadmap"""
    try:
        # Create a copy of the roadmap to avoid modifying the original
        roadmap_data = roadmap.model_dump()
        updated_roadmap = Roadmap.model_validate(roadmap_data)
        
        # Update subtopic completion status from session state
        for topic in updated_roadmap.topics:
            for subtopic in topic.subtopics:
                checkbox_key = f"checkbox_{subtopic.name}"
                if checkbox_key in st.session_state.checkbox_states:
                    subtopic.completed = st.session_state.checkbox_states[checkbox_key]
            # Update topic completion based on subtopics
            topic.completed = all(subtopic.completed for subtopic in topic.subtopics)
        
        # Save updated roadmap
        return db.update_roadmap(str(roadmap.mongo_id), updated_roadmap)
    except Exception as e:
        st.error(f"Error saving progress: {str(e)}")
        return False

def toggle_checkbox(key):
    """Toggle checkbox without triggering rerun"""
    st.session_state.checkbox_states[key] = not st.session_state.checkbox_states.get(key, False)

def create_topic_form(roadmap: Roadmap):
    """Show form to create a new topic"""
    with st.form(key="new_topic_form"):
        st.subheader("Create New Topic")
        name = st.text_input("Topic Name")
        
        if st.form_submit_button("Create Topic"):
            if name:
                # Create new topic
                new_topic = Topic(
                    name=name,
                    subtopics=[],
                    completed=False
                )
                roadmap.topics.append(new_topic)
                
                # Save roadmap
                if db.update_roadmap(str(roadmap.mongo_id), roadmap):
                    st.success("Topic created successfully!")
                    st.session_state.show_topic_creator = False
                    st.rerun()
                else:
                    st.error("Failed to create topic. Please try again.")
            else:
                st.error("Please fill in all fields.")

def create_subtopic_form(roadmap: Roadmap, parent_topic: Topic):
    """Show form to create a new subtopic"""
    with st.form(key=f"new_subtopic_form_{parent_topic.name}"):
        st.subheader(f"Create New Subtopic in {parent_topic.name}")
        name = st.text_input("Subtopic Name")
        
        if st.form_submit_button("Create Subtopic"):
            if name:
                # Create new subtopic
                new_subtopic = SubTopic(
                    name=name,
                    completed=False
                )
                
                # Find parent topic and add subtopic
                for topic in roadmap.topics:
                    if topic.name == parent_topic.name:
                        topic.subtopics.append(new_subtopic)
                        break
                
                # Save roadmap
                if db.update_roadmap(str(roadmap.mongo_id), roadmap):
                    st.success("Subtopic created successfully!")
                    st.session_state.show_subtopic_creator = None
                    st.rerun()
                else:
                    st.error("Failed to create subtopic. Please try again.")
            else:
                st.error("Please fill in all fields.")

@st.fragment()
def display_topic(topic: Topic, roadmap: Roadmap):
    """Display a single topic and its subtopics"""
    # Display subtopics
    for subtopic in topic.subtopics:
        checkbox_key = f"checkbox_{subtopic.name}"
        
        # Initialize checkbox state if not exists
        if checkbox_key not in st.session_state.checkbox_states:
            st.session_state.checkbox_states[checkbox_key] = subtopic.completed

        st.checkbox(
            label=subtopic.name,
            value=st.session_state.checkbox_states[checkbox_key],
            key=checkbox_key,
            on_change=toggle_checkbox,
            args=(checkbox_key,),
        )

    if st.button("Add Subtopic", key=f"add_subtopic_{topic.name}", help="Add new subtopic"):
        st.session_state.show_subtopic_creator = topic.name

    if st.session_state.show_subtopic_creator == topic.name:
        create_subtopic_form(roadmap, topic)

def show_roadmap():
    st.title("Learning Roadmap")
    
    # Initialize session state
    init_session_state()
    
    roadmaps = get_all_roadmaps()
    
    if not roadmaps:
        st.warning("No roadmaps available. Please check your database connection.")
        return
    
    # If we have multiple roadmaps, let user select one
    if len(roadmaps) > 1:
        selected_roadmap = st.selectbox(
            "Select a Roadmap",
            roadmaps,
            format_func=lambda x: x.title
        )
    else:
        selected_roadmap = roadmaps[0]
    
    # Display roadmap details
    st.header(selected_roadmap.title)
    if selected_roadmap.description:
        st.write(selected_roadmap.description)
    
    # Display topics
    for topic in selected_roadmap.topics:
        with st.expander(topic.name, expanded=True):
            display_topic(topic, selected_roadmap)

    if st.button("Add Topic", key="add_topic", help="Add new topic"):
        st.session_state.show_topic_creator = True

    if st.button("Save Progress", type="primary"):
        if save_progress(selected_roadmap):
            st.success("Progress saved successfully!")
        else:
            st.error("Failed to save progress. Please try again.")
    
    # Show topic creator if requested
    if st.session_state.show_topic_creator:
        create_topic_form(selected_roadmap)
    
    # Show chat interface at the bottom
    show_chat()

if __name__ == "__main__":
    show_roadmap()
