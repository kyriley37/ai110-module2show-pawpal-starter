from datetime import datetime, date, time

from pawpal_sytem import Owner, Pet, Task, Schedule


def main():
    # owner setup
    owner = Owner(name="Jess", email="jess@example.com", phone="555-1234")

    # pets
    fido = Pet(name="Fido", species="Dog", breed="Labrador", age=5, weight=70.0)
    whiskers = Pet(name="Whiskers", species="Cat", breed="Siamese", age=3, weight=10.0)

    owner.add_pet(fido)
    owner.add_pet(whiskers)

    # tasks (added out of order to test sorting)
    task3 = Task(
        type="Medication",
        description="Whiskers medication",
        duration=10,
        priority=1,
        frequency="Daily",
        preferred_time=datetime.combine(date.today(), time(hour=18, minute=0)),
        pet=whiskers,
    )
    task1 = Task(
        type="Feeding",
        description="Fido breakfast",
        duration=15,
        priority=1,
        frequency="Daily",
        preferred_time=datetime.combine(date.today(), time(hour=8, minute=0)),
        pet=fido,
    )
    task2 = Task(
        type="Walk",
        description="Fido morning walk",
        duration=30,
        priority=2,
        frequency="Daily",
        preferred_time=datetime.combine(date.today(), time(hour=9, minute=0)),
        pet=fido,
    )

    fido.add_task(task1)
    fido.add_task(task2)
    whiskers.add_task(task3)

    # Add a conflicting task (same time as task2)
    task4 = Task(
        type="Grooming",
        description="Fido grooming",
        duration=45,
        priority=2,
        frequency="Weekly",
        preferred_time=datetime.combine(date.today(), time(hour=9, minute=0)),
        pet=fido,
    )
    fido.add_task(task4)

    # schedule
    schedule = Schedule(schedule_date=date.today())
    schedule.add_task(task1)
    schedule.add_task(task2)
    schedule.add_task(task3)
    schedule.add_task(task4)

    # Test sorting
    print("Tasks before sorting:")
    for task in schedule.tasks:
        time_str = task.preferred_time.strftime("%H:%M") if task.preferred_time else "No time"
        print(f"  {time_str} - {task.description}")

    schedule.sort_by_time()
    print("\nTasks after sorting by time:")
    for task in schedule.tasks:
        time_str = task.preferred_time.strftime("%H:%M") if task.preferred_time else "No time"
        print(f"  {time_str} - {task.description}")

    # Test filtering
    print("\nFiltered tasks for Fido:")
    fido_tasks = schedule.filter_tasks(pet_name="Fido")
    for task in fido_tasks:
        time_str = task.preferred_time.strftime("%H:%M") if task.preferred_time else "No time"
        print(f"  {time_str} - {task.description}")

    # Mark a task complete and filter
    task1.mark_complete()
    print("\nAfter marking breakfast complete, Fido's tasks:")
    for task in fido.get_tasks():
        time_str = task.preferred_time.strftime("%H:%M") if task.preferred_time else "No time"
        status = "✓" if task.completed else "○"
        print(f"  {status} {time_str} - {task.description}")

    print("\nIncomplete tasks:")
    incomplete = schedule.filter_tasks(completed=False)
    for task in incomplete:
        time_str = task.preferred_time.strftime("%H:%M") if task.preferred_time else "No time"
        print(f"  {time_str} - {task.description}")

    # Check for scheduling conflicts
    print("\nDetecting scheduling conflicts...")
    conflicts = schedule.detect_conflicts()
    if conflicts:
        print("Found conflicts:")
        for conflict in conflicts:
            print(f"  {conflict}")
    else:
        print("  No conflicts detected!")

    # placeholder date-based plan generator and output
    schedule.generate_plan()

    print("\nToday's Schedule")
    print("--------------")
    print(schedule.display_plan())


if __name__ == "__main__":
    main()
