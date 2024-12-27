import streamlit as st
from database import Database
from models import Quiz
from components.chat import init_chat, show_chat

# Initialize database
db = Database()

def init_session_state():
    """Initialize session state variables"""
    if "selected_quiz" not in st.session_state:
        st.session_state.selected_quiz = None
    if "show_quiz_creator" not in st.session_state:
        st.session_state.show_quiz_creator = False
    if "selected_roadmap" not in st.session_state:
        st.session_state.selected_roadmap = None
    
    # Initialize chat with quiz agent
    init_chat("dkJPs3GbXG")

def format_roadmap_info(roadmap):
    """Format roadmap information into a detailed string"""
    if not roadmap:
        return ""
    
    # Format topics and subtopics
    topics_info = []
    for topic in roadmap.topics:
        topic_info = f"\nTopic: {topic.name}\n"
        
        if topic.subtopics:
            topic_info += "Subtopics:\n"
            for subtopic in topic.subtopics:
                completion_status = "Yes" if subtopic.completed else "No"
                topic_info += f"- {subtopic.name} - Completed: {completion_status}\n"
        
        topics_info.append(topic_info)
    
    # Create formatted string
    info = f"""
        Roadmap: {roadmap.title}
        Description: {roadmap.description}

        Topics:{' '.join(topics_info)}
        """
    return info

def display_quiz(quiz: Quiz):
    """Display a quiz and handle responses"""
    st.subheader(quiz.title)
    st.write(quiz.description)
    
    with st.form(key=f"quiz_{quiz.mongo_id}"):
        score = 0
        user_answers = {}
        
        for i, question in enumerate(quiz.questions):
            st.write(f"\n**Question {i+1}:** {question.question}")
            
            # Create radio buttons for choices
            answer = st.radio(
                "Choose your answer:",
                [choice.text for choice in question.choices],
                key=f"q_{quiz.mongo_id}_{i}"
            )
            user_answers[i] = answer
            
        submitted = st.form_submit_button("Submit Quiz")
        
        if submitted:
            score = 0
            feedback = []
            
            for i, question in enumerate(quiz.questions):
                user_answer = user_answers[i]
                correct_choice = next(
                    choice.text for choice in question.choices 
                    if choice.is_correct
                )
                
                if user_answer == correct_choice:
                    score += 1
                    feedback.append(f"✅ Question {i+1}: Correct!")
                else:
                    feedback.append(
                        f"❌ Question {i+1}: Incorrect. "
                        f"The correct answer was: {correct_choice}\n"
                        f"Explanation: {question.explanation}"
                    )
            
            st.success(f"Your score: {score}/{len(quiz.questions)}")
            for fb in feedback:
                st.write(fb)

def show_roadmap_selector():
    """Show roadmap selection for quiz generation"""
    st.subheader("Generate Quiz from Roadmap")
    
    # Get all roadmaps
    roadmaps = db.get_all_roadmaps()
    
    if not roadmaps:
        st.warning("No roadmaps available. Create a roadmap first!")
        return
    
    # Create roadmap selection
    roadmap_titles = [roadmap.title for roadmap in roadmaps]
    selected_title = st.selectbox(
        "Select a Roadmap to Generate Quiz From:",
        roadmap_titles,
        key="roadmap_selector"
    )
    
    if selected_title:
        selected_roadmap = next(r for r in roadmaps if r.title == selected_title)
        st.session_state.selected_roadmap = selected_roadmap

def show_quizzes():
    """Main function to display quizzes page"""
    st.title("Programming Quizzes")
    
    # Initialize session state
    init_session_state()
    
    # Create tabs for different sections
    quiz_tab, generate_tab = st.tabs([
        "Available Quizzes", 
        "Generate Quiz"
    ])
    
    with quiz_tab:
        # Get all quizzes from database
        quizzes = db.get_all_quizzes()
        
        if not quizzes:
            st.info("No quizzes available yet. Generate one from a roadmap!")
        else:
            # Quiz selection
            quiz_titles = [quiz.title for quiz in quizzes]
            selected_title = st.selectbox(
                "Select Quiz",
                quiz_titles
            )
            
            if selected_title:
                selected_quiz = next(q for q in quizzes if q.title == selected_title)
                display_quiz(selected_quiz)
    
    with generate_tab:
        # Show roadmap selector first
        show_roadmap_selector()
        
        # Get roadmap info if one is selected
        roadmap_info = format_roadmap_info(st.session_state.selected_roadmap)
        
        # Show chat with roadmap context
        show_chat(
            prompt_placeholder="Describe what you want to generate a quiz about!",
            extra_info=roadmap_info
        )

if __name__ == "__main__":
    show_quizzes()
