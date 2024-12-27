from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema
from bson import ObjectId

class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetJsonSchemaHandler,
    ) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.str_schema(),
                core_schema.is_instance_schema(ObjectId),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x) if isinstance(x, ObjectId) else x
            ),
        )

class SubTopic(BaseModel):
    name: str
    completed: bool = False

class Topic(BaseModel):
    name: str
    subtopics: List[SubTopic] = []
    completed: bool = False

class Roadmap(BaseModel):
    title: str
    description: str = ""
    topics: List[Topic]
    created_at: datetime = Field(default_factory=datetime.now)
    mongo_id: Optional[PyObjectId] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class QuizChoice(BaseModel):
    text: str
    is_correct: bool

class QuizQuestion(BaseModel):
    question: str
    choices: List[QuizChoice]
    explanation: str = ""

class Quiz(BaseModel):
    title: str
    description: str = ""
    questions: List[QuizQuestion]
    created_at: datetime = Field(default_factory=datetime.now)
    mongo_id: Optional[PyObjectId] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class Resource(BaseModel):
    name: str
    description: str
    asset: str = ""  # URL or file path
    resource_type: str  # video, article, code_example, etc.
    created_at: datetime = Field(default_factory=datetime.now)
    mongo_id: Optional[PyObjectId] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }