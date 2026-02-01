from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

class TaskTimelineItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    date: date
    description: str
    project: "Project" = Relationship(back_populates="timeline")

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    category: Optional[str] = None
    task_name: str
    timeline: List[TaskTimelineItem] = Relationship(back_populates="project")
