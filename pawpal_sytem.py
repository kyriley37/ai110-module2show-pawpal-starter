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
        """Add a pet to the owner's collection."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's collection."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pets(self) -> list[Pet]:
        """Return the list of pets owned by this owner."""
        return self.pets

    def update_info(self, name: str, email: str, phone: str) -> None:
        """Update the owner's contact information."""
        self.name = name
        self.email = email
        self.phone = phone


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
        """Add a care task to this pet's task list."""
        self.tasks.append(task)
        task.pet = self

    def get_tasks(self) -> list[Task]:
        """Return the list of tasks associated with this pet."""
        return self.tasks

    def update_info(self, **kwargs) -> None:
        """Update pet attributes dynamically."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


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
        """Mark this task as completed."""
        self.completed = True

    def schedule_for_day(self, on_date: date) -> None:
        """Reschedule this task to a specific date."""
        if self.preferred_time:
            self.preferred_time = self.preferred_time.replace(year=on_date.year, month=on_date.month, day=on_date.day)

    def update_details(self, **kwargs) -> None:
        """Update task attributes dynamically."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


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
        """Add a task to the schedule if not already present."""
        if task not in self.tasks:
            self.tasks.append(task)

    def generate_plan(self, priorities: bool = True, constraints: dict | None = None) -> None:
        """Generate a prioritized task schedule for the day."""
        if priorities:
            self.tasks.sort(key=lambda t: t.priority)
        
        self.generated_plan = [
            {
                "time": task.preferred_time.strftime("%H:%M") if task.preferred_time else "No time",
                "task": task.description,
                "pet": task.pet.name if task.pet else "Unknown",
                "duration": task.duration,
            }
            for task in self.tasks
        ]

    def resolve_conflicts(self) -> None:
        """Detect and handle overlapping tasks in the schedule."""
        # Simple check: warn if tasks overlap by 30+ min
        for i, task1 in enumerate(self.tasks):
            for task2 in self.tasks[i+1:]:
                if task1.preferred_time and task2.preferred_time:
                    time_diff = abs((task2.preferred_time - task1.preferred_time).total_seconds() / 60)
                    if time_diff < task1.duration:
                        pass  # Conflict detected (could log or reschedule)

    def display_plan(self) -> str:
        """Return a formatted string representation of the daily schedule."""
        if not self.tasks:
            return "No tasks scheduled for today."
        
        output = []
        sorted_tasks = sorted(self.tasks, key=lambda t: t.preferred_time if t.preferred_time else datetime.min)
        
        for task in sorted_tasks:
            time_str = task.preferred_time.strftime("%H:%M") if task.preferred_time else "No time set"
            pet_name = task.pet.name if task.pet else "Unknown pet"
            output.append(f"{time_str} - [{task.type}] {task.description} ({pet_name}) - {task.duration}min")
        
        return "\n".join(output)
