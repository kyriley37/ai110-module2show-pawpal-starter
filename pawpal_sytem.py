from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
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
        """Mark this task as completed and create next occurrence if recurring.
        
        For tasks with frequency="Daily", creates a new task instance for tomorrow at the same time.
        For tasks with frequency="Weekly", creates a new task instance for next week at the same time.
        Uses timedelta for accurate date calculations.
        
        Only generates next occurrence if the task is associated with a pet and has a preferred_time.
        """
        self.completed = True
        
        # Create next occurrence for recurring tasks
        if self.frequency.lower() == "daily" and self.pet and self.preferred_time:
            next_time = self.preferred_time + timedelta(days=1)
            next_task = Task(
                type=self.type,
                description=self.description,
                duration=self.duration,
                priority=self.priority,
                frequency=self.frequency,
                preferred_time=next_time,
                pet=self.pet
            )
            self.pet.add_task(next_task)
        elif self.frequency.lower() == "weekly" and self.pet and self.preferred_time:
            next_time = self.preferred_time + timedelta(days=7)
            next_task = Task(
                type=self.type,
                description=self.description,
                duration=self.duration,
                priority=self.priority,
                frequency=self.frequency,
                preferred_time=next_time,
                pet=self.pet
            )
            self.pet.add_task(next_task)

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

    def filter_tasks(self, completed: bool | None = None, pet_name: str | None = None) -> list[Task]:
        """Filter tasks by completion status and/or pet name.
        
        Args:
            completed: If True, return only completed tasks. If False, return only incomplete. If None, return all.
            pet_name: Filter by pet name. If None, return tasks for all pets.
        
        Returns:
            A filtered list of Task objects matching the criteria.
        """
        filtered = self.tasks
        if completed is not None:
            filtered = [t for t in filtered if t.completed == completed]
        if pet_name is not None:
            filtered = [t for t in filtered if t.pet and t.pet.name == pet_name]
        return filtered

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule if not already present."""
        if task not in self.tasks:
            self.tasks.append(task)

    def sort_by_time(self) -> None:
        """Sort tasks chronologically by preferred_time in ascending order.
        
        Tasks without a preferred_time (None) are sorted to the beginning.
        Modifies self.tasks in place.
        """
        self.tasks.sort(key=lambda t: t.preferred_time if t.preferred_time else datetime.min)

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

    def detect_conflicts(self) -> list[str]:
        """Detect task conflicts and return warning messages (lightweight strategy).
        
        Identifies tasks scheduled at the exact same time (HH:MM match).
        Uses exact-time matching rather than duration overlap for simplicity and performance.
        
        Returns:
            A list of warning messages (str) for each time slot with multiple tasks.
            Empty list if no conflicts found.
        """
        conflicts = []
        
        # Group tasks by preferred_time
        time_groups = {}
        for task in self.tasks:
            if task.preferred_time:
                time_key = task.preferred_time.strftime("%H:%M")
                if time_key not in time_groups:
                    time_groups[time_key] = []
                time_groups[time_key].append(task)
        
        # Find conflicts: multiple tasks at same time
        for time_str, tasks in time_groups.items():
            if len(tasks) > 1:
                task_names = [f"{t.description} ({t.pet.name if t.pet else 'Unknown'})" for t in tasks]
                warning = f"⚠️ CONFLICT at {time_str}: {', '.join(task_names)}"
                conflicts.append(warning)
        
        return conflicts

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
