import pytest
from datetime import datetime, date, time
from pawpal_sytem import Owner, Pet, Task, Schedule


class TestTask:
    def test_task_completion(self):
        """Verify that calling mark_complete() changes the task's completed status."""
        task = Task(
            type="Feeding",
            description="Morning breakfast",
            duration=15,
            priority=1,
            frequency="Daily",
        )
        
        assert task.completed is False, "Task should start as incomplete"
        task.mark_complete()
        assert task.completed is True, "Task should be marked as complete after mark_complete()"


class TestPet:
    def test_task_addition(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        pet = Pet(
            name="Buddy",
            species="Dog",
            breed="Golden Retriever",
            age=3,
            weight=65.0,
        )
        
        initial_count = len(pet.get_tasks())
        assert initial_count == 0, "Pet should start with no tasks"
        
        task = Task(
            type="Walk",
            description="Morning walk",
            duration=30,
            priority=2,
            frequency="Daily",
        )
        
        pet.add_task(task)
        final_count = len(pet.get_tasks())
        assert final_count == 1, "Pet should have 1 task after adding"
        assert pet.get_tasks()[0] == task, "Added task should be in pet's task list"
