from lagom import Container

from parlant.core.background_tasks import BackgroundTaskService
from parlant.core.services.tools.plugins import PluginServer, tool
from parlant.core.services.tools.service_registry import ServiceRegistry
from parlant.core.tools import ToolContext, ToolResult

from database import Database
from models import (
    Roadmap, Quiz, Resource, QuizQuestion, QuizChoice,
    Topic, SubTopic
)
from datetime import datetime
import json

# Initialize database
db = Database()

server_instance: PluginServer | None = None

@tool
async def create_roadmap(
    context: ToolContext,
    title: str,
    description: str,
    topics_json: str  # JSON string containing list of topics
) -> ToolResult:
    """Create a new roadmap
    
    The topics_json argument should be a JSON string representing a list of dictionaries with this structure:
    [
        {
            "name": "Python Basics",
            "subtopics": [
                {"name": "Variables and Data Types"},
                {"name": "Basic Operators"},
                {"name": "Control Flow (if/else)"}
            ]
        },
        {
            "name": "Data Structures",
            "subtopics": [
                {"name": "Lists and Arrays"},
                {"name": "Dictionaries"},
                {"name": "Sets and Tuples"}
            ]
        }
    ]
    """
    # Parse JSON string to list of dicts
    topics_data = json.loads(topics_json)
    
    # Convert dictionaries to Topic models
    topic_models = [
        Topic(
            name=topic["name"],
            subtopics=[SubTopic(name=subtopic["name"], completed=False) for subtopic in topic["subtopics"]],
            completed=False
        )
        for topic in topics_data
    ]
    
    roadmap = Roadmap(
        title=title,
        description=description,
        topics=topic_models,
        created_at=datetime.now()
    )
    roadmap_id = db.create_roadmap(roadmap)
    return ToolResult({"roadmap_id": roadmap_id})

@tool
async def create_quiz(
    context: ToolContext,
    title: str,
    description: str,
    questions_json: str  # JSON string containing questions data
) -> ToolResult:
    """Create a new quiz
    
    The questions_json argument should be a JSON string representing a list of questions with this structure:
    [
        {
            "question": "What is a variable in Python?",
            "choices": [
                {
                    "text": "A container for storing data values",
                    "is_correct": true
                },
                {
                    "text": "A loop statement",
                    "is_correct": false
                },
                {
                    "text": "A function definition",
                    "is_correct": false
                }
            ],
            "explanation": "A variable is a container that holds data values while a program is running"
        },
        {
            "question": "Which of these is a valid variable name in Python?",
            "choices": [
                {
                    "text": "2myvar",
                    "is_correct": false
                },
                {
                    "text": "my-var",
                    "is_correct": false
                },
                {
                    "text": "my_var",
                    "is_correct": true
                }
            ],
            "explanation": "my_var is valid because it starts with a letter and uses underscore for spacing"
        }
    ]
    """
    # Parse JSON string to list of dicts
    questions_data = json.loads(questions_json)
    
    # Convert to QuizQuestion models manually
    question_models = []
    for q in questions_data:
        # Create QuizChoice models for each choice
        choice_models = [
            QuizChoice(
                text=choice["text"],
                is_correct=choice["is_correct"]
            )
            for choice in q["choices"]
        ]
        
        # Create QuizQuestion model
        question_model = QuizQuestion(
            question=q["question"],
            choices=choice_models,
            explanation=q["explanation"]
        )
        question_models.append(question_model)
    
    # Create Quiz model
    quiz = Quiz(
        title=title,
        description=description,
        questions=question_models,
        created_at=datetime.now()
    )
    quiz_id = db.create_quiz(quiz)
    return ToolResult({"quiz_id": quiz_id})


@tool
async def create_resource(
    context: ToolContext,
    name: str,
    description: str,
    asset: str,
    resource_type: str
) -> ToolResult:
    """Create a new resource"""
    resource = Resource(
        name=name,
        description=description,
        asset=asset,
        resource_type=resource_type,
        created_at=datetime.now()
    )
    resource_id = db.create_resource(resource)
    return ToolResult({"resource_id": resource_id})

@tool
async def search_resources(
    context: ToolContext,
    query: str,
    limit: int = 2
) -> ToolResult:
    """Search for resources using vector similarity
    
    Args:
        query: The search query text
        limit: Maximum number of results to return (default: 5)
    
    Returns:
        List of resources sorted by relevance to the query
    """
    try:
        resources = db.search_resources(query, limit)
        return ToolResult(
            {
            "message":f"Found {len(resources)} relevant resources",
            "data":[resource.model_dump(exclude={"created_at"}) for resource in resources]
            }
        )
    except Exception as e:
        return ToolResult(
            {"message": f"Failed to search resources: {str(e)}"}
        )

TOOLS = [
    create_roadmap,
    create_quiz,
    create_resource,
    search_resources,
]

async def initialize_module(container: Container) -> None:
    global server_instance
    _background_task_service = container[BackgroundTaskService]

    server = PluginServer(
        tools=TOOLS,
        port=8094,
        host="127.0.0.1",
    )
    await _background_task_service.start(
        server.serve(),
        tag="Database Plugin",
    )

    server_instance = server

    service_registry = container[ServiceRegistry]
    await service_registry.update_tool_service(
        name="database",
        kind="sdk",
        url="http://127.0.0.1:8094",
        transient=True,
    )


async def shutdown_module() -> None:
    global server_instance

    if server_instance is not None:
        await server_instance.shutdown()
        server_instance = None

if __name__ == "__main__":
    asyncio.run(main())