# PawPal+ Project Reflection

## 1. System Design

 3 core action s a user should be able to complete are
 - User enter basic owner + pet info
 - Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
 - Generate a daily schedule/plan based on constraints and priorities

**a. Initial design**

The initial UML design uses a class diagram to model the PawPal+ system, focusing on the core features: entering owner/pet info, tracking care tasks, and generating schedules. The main classes are Owner, Pet, Task, and Schedule.

- **Owner**: Manages user information and their pets. Responsibilities: add/remove pets, update info, retrieve pet list.
- **Pet**: Represents individual pets with details and tasks. Responsibilities: add tasks, update info, retrieve task list.
- **Task**: Defines care activities with scheduling details. Responsibilities: mark complete, schedule for day, update details.
- **Schedule**: Generates daily plans. Responsibilities: add tasks, generate prioritized plan, resolve conflicts, display plan.

```mermaid
classDiagram
    class Owner {
        +name: string
        +email: string
        +phone: string
        +pets: list[Pet]
        +add_pet(pet: Pet)
        +remove_pet(pet: Pet)
        +get_pets(): list[Pet]
        +update_info(name, email, phone)
    }
    class Pet {
        +name: string
        +species: string
        +breed: string
        +age: int
        +weight: float
        +medical_notes: string
        +tasks: list[Task]
        +add_task(task: Task)
        +get_tasks(): list[Task]
        +update_info(name, species, etc.)
    }
    class Task {
        +type: string
        +description: string
        +duration: int
        +priority: int
        +frequency: string
        +preferred_time: datetime
        +pet: Pet
        +completed: boolean
        +mark_complete()
        +schedule_for_day(date)
        +update_details(type, priority, etc.)
    }
    class Schedule {
        +date: date
        +tasks: list[Task]
        +constraints: dict
        +generated_plan: list[dict]
        +add_task(task: Task)
        +generate_plan(priorities, constraints)
        +resolve_conflicts()
        +display_plan()
    }
    Owner ||--o{ Pet : owns
    Pet ||--o{ Task : has
    Schedule o--o{ Task : aggregates
```

**b. Design changes**

- Did your design change during implementation?
  - Yes. As the requirements clarified, I moved from a flat Task-centric model to a stronger domain model where Schedule owns task placement and Owner links to daily schedules.
- If yes, describe at least one change and why you made it.
  - Originally, `Task.schedule_for_day()` was intended to do assignment logic, but I changed it to keep `Task` as a data object and move all planning/resolution into `Schedule`. This simplifies responsibility and avoids duplicated scheduling logic.
  - Added `Owner.schedules: list[Schedule]` and introduced a `ScheduleEntry` concept (time slot + task + pet) to track exact placement and avoid contention.
  - Kept `Pet.tasks` in place but made `Schedule` the source of truth for “what happens today”, while `Task` remains generic.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
