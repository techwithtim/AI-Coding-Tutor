from database import Database
from models import Roadmap, Topic, SubTopic, Quiz, QuizQuestion, QuizChoice, Resource
from datetime import datetime

def test_roadmap():
    print("\n=== Testing Roadmap Operations ===")
    db = Database()
    
    # Create a roadmap
    roadmap = Roadmap(
        slug="python-beginner-roadmap",
        title="Python Beginner's Roadmap",
        description="A comprehensive guide to Python programming for beginners",
        topics=[
            Topic(
                slug="python-fundamentals",
                name="Python Fundamentals",
                subtopics=[
                    SubTopic(
                        slug="variables-and-types",
                        name="Variables and Data Types",
                        completed=False
                    ),
                    SubTopic(
                        slug="control-flow",
                        name="Control Flow",
                        completed=True
                    )
                ]
            ),
            Topic(
                slug="python-oop",
                name="Object-Oriented Programming",
                subtopics=[
                    SubTopic(
                        slug="classes-and-objects",
                        name="Classes and Objects",
                        completed=False
                    ),
                    SubTopic(
                        slug="inheritance",
                        name="Inheritance",
                        completed=False
                    )
                ]
            )
        ]
    )
    
    # Save roadmap
    roadmap_id = db.create_roadmap(roadmap)
    print(f"Created roadmap with ID: {roadmap_id}")
    
    # Retrieve roadmap
    saved_roadmap = db.get_roadmap(roadmap_id)
    if saved_roadmap:
        print(f"Retrieved roadmap: {saved_roadmap.model_dump_json(indent=2)}")
    else:
        print("Failed to retrieve roadmap")
    
    return roadmap_id

def test_quiz():
    print("\n=== Testing Quiz Operations ===")
    db = Database()
    
    # Create a quiz
    quiz = Quiz(
        slug="python-basics-quiz",
        title="Python Basics Quiz",
        description="Test your Python fundamentals",
        questions=[
            QuizQuestion(
                slug="type-function-output",
                question="What is the output of print(type(5))?",
                choices=[
                    QuizChoice(text="<class 'int'>", is_correct=True),
                    QuizChoice(text="<class 'str'>", is_correct=False),
                    QuizChoice(text="<class 'float'>", is_correct=False)
                ],
                explanation="In Python, 5 is an integer literal"
            ),
            QuizQuestion(
                slug="valid-variable-name",
                question="Which of these is a valid variable name?",
                choices=[
                    QuizChoice(text="_variable", is_correct=True),
                    QuizChoice(text="2variable", is_correct=False),
                    QuizChoice(text="my-var", is_correct=False)
                ],
                explanation="Variable names can start with underscore but not with numbers or contain hyphens"
            )
        ]
    )
    
    # Save quiz
    quiz_id = db.create_quiz(quiz)
    print(f"Created quiz with ID: {quiz_id}")
    
    # Retrieve quiz
    saved_quiz = db.get_quiz(quiz_id)
    if saved_quiz:
        print(f"Retrieved quiz: {saved_quiz.model_dump_json(indent=2)}")
    else:
        print("Failed to retrieve quiz")
    
    return quiz_id

def test_resource():
    print("\n=== Testing Resource Operations ===")
    db = Database()
    
    # Create a resource
    resource = Resource(
        slug="python-variables-tutorial",
        name="Python Variables Tutorial",
        description="Learn about Python variables and data types",
        asset="https://example.com/python-variables",
        resource_type="video"
    )
    
    # Save resource
    resource_id = db.create_resource(resource)
    print(f"Created resource with ID: {resource_id}")
    
    # Retrieve resource
    saved_resource = db.get_resource(resource_id)
    if saved_resource:
        print(f"Retrieved resource: {saved_resource.model_dump_json(indent=2)}")
    else:
        print("Failed to retrieve resource")
    
    return resource_id

def main():
    try:
        print("Starting database tests...")
        
        # Test all operations
        roadmap_id = test_roadmap()
        quiz_id = test_quiz()
        resource_id = test_resource()
        test_user_progress("python-beginner-roadmap")
        
        print("\nAll tests completed successfully!")
    except Exception as e:
        print(f"\nError during testing: {str(e)}")

if __name__ == "__main__":
    main()
