import pytest
from datetime import datetime, date, time, timedelta
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


class TestRecurrenceLogic:
    """Test suite for recurring task auto-generation."""
    
    def test_daily_task_creates_next_occurrence(self):
        """Verify that marking a daily task complete creates a task for tomorrow."""
        pet = Pet("Fido", "Dog", "Labrador", 5, 70.0)
        today = date.today()
        today_0800 = datetime.combine(today, time(8, 0))
        
        task = Task(
            type="Feeding",
            description="Breakfast",
            duration=15,
            priority=1,
            frequency="Daily",
            preferred_time=today_0800,
            pet=pet
        )
        pet.add_task(task)
        
        # Before completion: 1 task
        assert len(pet.get_tasks()) == 1, "Should have 1 task before completion"
        
        # Mark complete and check next occurrence created
        task.mark_complete()
        
        # After completion: should have 2 tasks (original + next)
        assert len(pet.get_tasks()) == 2, "Should have 2 tasks after completion"
        assert pet.get_tasks()[0].completed is True, "Original should be marked complete"
        assert pet.get_tasks()[1].completed is False, "New task should be incomplete"
        
        # Check new task is scheduled for tomorrow at same time
        tomorrow_0800 = datetime.combine(today + timedelta(days=1), time(8, 0))
        assert pet.get_tasks()[1].preferred_time == tomorrow_0800, "New task should be tomorrow at 08:00"
    
    def test_weekly_task_creates_next_occurrence(self):
        """Verify that marking a weekly task complete creates a task for next week."""
        pet = Pet("Whiskers", "Cat", "Siamese", 3, 10.0)
        today = date.today()
        today_1000 = datetime.combine(today, time(10, 0))
        
        task = Task(
            type="Grooming",
            description="Weekly grooming",
            duration=60,
            priority=2,
            frequency="Weekly",
            preferred_time=today_1000,
            pet=pet
        )
        pet.add_task(task)
        task.mark_complete()
        
        # Check new task is scheduled for next week
        next_week = today + timedelta(days=7)
        next_week_1000 = datetime.combine(next_week, time(10, 0))
        assert pet.get_tasks()[1].preferred_time == next_week_1000, "New task should be in 7 days"
    
    def test_non_recurring_task_no_next_occurrence(self):
        """Verify that non-recurring tasks don't create next occurrences."""
        pet = Pet("Max", "Dog", "Poodle", 2, 20.0)
        today_0900 = datetime.combine(date.today(), time(9, 0))
        
        task = Task(
            type="Vet Visit",
            description="Annual checkup",
            duration=60,
            priority=1,
            frequency="Once",  # Non-recurring
            preferred_time=today_0900,
            pet=pet
        )
        pet.add_task(task)
        initial_count = len(pet.get_tasks())
        
        task.mark_complete()
        
        # After completion: should still have same count (no next occurrence)
        assert len(pet.get_tasks()) == initial_count, "Non-recurring task should not create next occurrence"
    
    def test_recurring_task_without_preferred_time(self):
        """Verify that recurring tasks without preferred_time don't create next occurrence."""
        pet = Pet("Bella", "Cat", "Tabby", 4, 12.0)
        
        task = Task(
            type="Feeding",
            description="Breakfast",
            duration=15,
            priority=1,
            frequency="Daily",
            preferred_time=None,  # No time set
            pet=pet
        )
        pet.add_task(task)
        initial_count = len(pet.get_tasks())
        
        task.mark_complete()
        
        # Should not create next occurrence (no time reference)
        assert len(pet.get_tasks()) == initial_count, "Task without time should not create next occurrence"
    
    def test_recurring_task_without_pet_assignment(self):
        """Verify that recurring tasks without pet don't create next occurrence."""
        task = Task(
            type="Feeding",
            description="Breakfast",
            duration=15,
            priority=1,
            frequency="Daily",
            preferred_time=datetime.combine(date.today(), time(8, 0)),
            pet=None  # No pet assigned
        )
        
        # Should not raise error, just skip next occurrence creation
        task.mark_complete()
        assert task.completed is True, "Task should be marked complete"


class TestSortingCorrectness:
    """Test suite for schedule sorting by time."""
    
    def test_sort_tasks_chronologically(self):
        """Verify that sort_by_time() returns tasks in chronological order."""
        schedule = Schedule(date.today())
        today = date.today()
        
        # Add tasks out of order
        task_1800 = Task("Dinner", "Evening feed", 20, 3, "Daily", 
                        preferred_time=datetime.combine(today, time(18, 0)))
        task_0800 = Task("Breakfast", "Morning feed", 15, 1, "Daily",
                        preferred_time=datetime.combine(today, time(8, 0)))
        task_1200 = Task("Lunch", "Midday feed", 15, 2, "Daily",
                        preferred_time=datetime.combine(today, time(12, 0)))
        
        schedule.add_task(task_1800)
        schedule.add_task(task_0800)
        schedule.add_task(task_1200)
        
        # Before sort: 18, 8, 12
        assert schedule.tasks[0].preferred_time.hour == 18
        
        # After sort: should be 8, 12, 18
        schedule.sort_by_time()
        assert schedule.tasks[0].preferred_time.hour == 8, "First task should be 08:00"
        assert schedule.tasks[1].preferred_time.hour == 12, "Second task should be 12:00"
        assert schedule.tasks[2].preferred_time.hour == 18, "Third task should be 18:00"
    
    def test_sort_tasks_with_none_time(self):
        """Verify that tasks without preferred_time are sorted to beginning."""
        schedule = Schedule(date.today())
        today = date.today()
        
        task_no_time = Task("Unknown time", "No time set", 15, 2, "Daily", preferred_time=None)
        task_0900 = Task("Walk", "Morning", 30, 2, "Daily",
                        preferred_time=datetime.combine(today, time(9, 0)))
        
        schedule.add_task(task_0900)
        schedule.add_task(task_no_time)
        
        schedule.sort_by_time()
        
        # Task with None should be first
        assert schedule.tasks[0].preferred_time is None, "Task without time should be first"
        assert schedule.tasks[1].preferred_time is not None, "Task with time should be second"
    
    def test_sort_empty_schedule(self):
        """Verify that sorting empty schedule doesn't raise error."""
        schedule = Schedule(date.today())
        schedule.sort_by_time()  # Should not raise
        assert schedule.tasks == [], "Empty schedule should remain empty"
    
    def test_sort_already_sorted(self):
        """Verify that sorting already-sorted tasks maintains order."""
        schedule = Schedule(date.today())
        today = date.today()
        
        task_0800 = Task("Breakfast", "Morning", 15, 1, "Daily",
                        preferred_time=datetime.combine(today, time(8, 0)))
        task_1200 = Task("Lunch", "Midday", 15, 2, "Daily",
                        preferred_time=datetime.combine(today, time(12, 0)))
        
        schedule.add_task(task_0800)
        schedule.add_task(task_1200)
        
        schedule.sort_by_time()
        
        # Should maintain order
        assert schedule.tasks[0].preferred_time.hour == 8
        assert schedule.tasks[1].preferred_time.hour == 12
    
    def test_sort_all_same_time(self):
        """Verify that sorting tasks at same time doesn't raise error."""
        schedule = Schedule(date.today())
        today = date.today()
        same_time = datetime.combine(today, time(9, 0))
        
        task1 = Task("Task 1", "First", 15, 1, "Daily", preferred_time=same_time)
        task2 = Task("Task 2", "Second", 15, 2, "Daily", preferred_time=same_time)
        task3 = Task("Task 3", "Third", 15, 3, "Daily", preferred_time=same_time)
        
        schedule.add_task(task1)
        schedule.add_task(task2)
        schedule.add_task(task3)
        
        schedule.sort_by_time()  # Should not raise
        assert len(schedule.tasks) == 3, "All tasks should be present"


class TestConflictDetection:
    """Test suite for conflict detection."""
    
    def test_detect_conflict_two_tasks_same_time(self):
        """Verify that scheduler flags two tasks at exact same time."""
        schedule = Schedule(date.today())
        today = date.today()
        same_time = datetime.combine(today, time(9, 0))
        
        pet1 = Pet("Fido", "Dog", "Lab", 5, 70.0)
        task1 = Task("Walk", "Morning walk", 30, 2, "Daily", preferred_time=same_time, pet=pet1)
        
        pet2 = Pet("Whiskers", "Cat", "Siamese", 3, 10.0)
        task2 = Task("Feed", "Breakfast", 15, 1, "Daily", preferred_time=same_time, pet=pet2)
        
        schedule.add_task(task1)
        schedule.add_task(task2)
        
        conflicts = schedule.detect_conflicts()
        
        assert len(conflicts) == 1, "Should detect exactly 1 conflict"
        assert "CONFLICT" in conflicts[0], "Should contain 'CONFLICT' warning"
        assert "09:00" in conflicts[0], "Should show conflicting time"
        assert "Morning walk" in conflicts[0] and "Breakfast" in conflicts[0], "Should list both task descriptions"
    
    def test_no_conflicts_different_times(self):
        """Verify that tasks at different times don't trigger conflicts."""
        schedule = Schedule(date.today())
        today = date.today()
        
        pet = Pet("Fido", "Dog", "Lab", 5, 70.0)
        task1 = Task("Walk", "Morning", 30, 2, "Daily",
                    preferred_time=datetime.combine(today, time(8, 0)), pet=pet)
        task2 = Task("Dinner", "Evening", 20, 3, "Daily",
                    preferred_time=datetime.combine(today, time(18, 0)), pet=pet)
        
        schedule.add_task(task1)
        schedule.add_task(task2)
        
        conflicts = schedule.detect_conflicts()
        
        assert conflicts == [], "Should have no conflicts for different times"
    
    def test_detect_conflict_three_tasks_same_time(self):
        """Verify that scheduler detects multiple tasks at same time in one warning."""
        schedule = Schedule(date.today())
        today = date.today()
        same_time = datetime.combine(today, time(10, 0))
        
        pet = Pet("Fido", "Dog", "Lab", 5, 70.0)
        task1 = Task("Walk", "Morning walk", 30, 2, "Daily", preferred_time=same_time, pet=pet)
        task2 = Task("Feed", "Breakfast feed", 15, 1, "Daily", preferred_time=same_time, pet=pet)
        task3 = Task("Groom", "Weekly grooming", 45, 2, "Weekly", preferred_time=same_time, pet=pet)
        
        schedule.add_task(task1)
        schedule.add_task(task2)
        schedule.add_task(task3)
        
        conflicts = schedule.detect_conflicts()
        
        assert len(conflicts) == 1, "Should have 1 conflict warning for 3 tasks at same time"
        assert "Morning walk" in conflicts[0] and "Breakfast feed" in conflicts[0] and "Weekly grooming" in conflicts[0]
    
    def test_conflicts_with_no_preferred_time(self):
        """Verify that tasks without preferred_time are skipped in conflict detection."""
        schedule = Schedule(date.today())
        today = date.today()
        
        pet = Pet("Fido", "Dog", "Lab", 5, 70.0)
        task_no_time = Task("Unknown", "Unknown", 15, 2, "Daily", preferred_time=None, pet=pet)
        task_with_time = Task("Walk", "Walk", 30, 2, "Daily",
                             preferred_time=datetime.combine(today, time(9, 0)), pet=pet)
        
        schedule.add_task(task_no_time)
        schedule.add_task(task_with_time)
        
        conflicts = schedule.detect_conflicts()
        
        assert conflicts == [], "Task without time should not trigger conflict"
    
    def test_empty_schedule_no_conflicts(self):
        """Verify that empty schedule has no conflicts."""
        schedule = Schedule(date.today())
        conflicts = schedule.detect_conflicts()
        
        assert conflicts == [], "Empty schedule should have no conflicts"
    
    def test_single_task_no_conflict(self):
        """Verify that single task doesn't trigger conflict."""
        schedule = Schedule(date.today())
        today = date.today()
        
        pet = Pet("Fido", "Dog", "Lab", 5, 70.0)
        task = Task("Walk", "Walk", 30, 2, "Daily",
                   preferred_time=datetime.combine(today, time(9, 0)), pet=pet)
        
        schedule.add_task(task)
        conflicts = schedule.detect_conflicts()
        
        assert conflicts == [], "Single task should not trigger conflict"
