from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
import typing

class Owner:
    def __init__(self, name: str, email: str, phone: str):
        self.name: str = name
        self.email: str = email
        self.phone: str = phone
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> list[Pet]:
        pass

    def update_info(self, name: str, email: str, phone: str) -> None:
        pass


class Pet:
    def __init__(
        self,
        name: str,
        species: str,
        breed: str,
        age: int,
        weight: float,
        medical_notes: str = "",
    ):
        self.name: str = name
        self.species: str = species
        self.breed: str = breed
        self.age: int = age
        self.weight: float = weight
        self.medical_notes: str = medical_notes
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass

    def update_info(self, **kwargs) -> None:
        pass


class Task:
    def __init__(
        self,
        type: str,
        description: str,
        duration: int,
        priority: int,
        frequency: str,
        preferred_time: datetime | None = None,
        pet: Pet | None = None,
    ):
        self.type: str = type
        self.description: str = description
        self.duration: int = duration
        self.priority: int = priority
        self.frequency: str = frequency
        self.preferred_time: datetime | None = preferred_time
        self.pet: Pet | None = pet
        self.completed: bool = False

    def mark_complete(self) -> None:
        pass

    def schedule_for_day(self, on_date: date) -> None:
        pass

    def update_details(self, **kwargs) -> None:
        pass


class Schedule:
    def __init__(
        self,
        schedule_date: date,
        constraints: dict | None = None,
    ):
        self.date: date = schedule_date
        self.tasks: list[Task] = []
        self.constraints: dict = constraints or {}
        self.generated_plan: list[dict] = []

    def add_task(self, task: Task) -> None:
        pass

    def generate_plan(self, priorities: bool = True, constraints: dict | None = None) -> None:
        pass

    def resolve_conflicts(self) -> None:
        pass

    def display_plan(self) -> str:
        pass
