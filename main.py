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

    # tasks (time assigned in task description for demonstration)
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
    task3 = Task(
        type="Medication",
        description="Whiskers medication",
        duration=10,
        priority=1,
        frequency="Daily",
        preferred_time=datetime.combine(date.today(), time(hour=18, minute=0)),
        pet=whiskers,
    )

    fido.add_task(task1)
    fido.add_task(task2)
    whiskers.add_task(task3)

    # schedule
    schedule = Schedule(schedule_date=date.today())
    schedule.add_task(task1)
    schedule.add_task(task2)
    schedule.add_task(task3)

    # placeholder date-based plan generator and output
    schedule.generate_plan()

    print("Today's Schedule")
    print("--------------")
    print(schedule.display_plan())


if __name__ == "__main__":
    main()
