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
  - The scheduler considers: task priority (1=high, 3=low), preferred_time (exact time slot), pet-specific associations, and task duration.
  - It sorts by priority first, then we manually override with preferred_time for exact scheduling.
- How did you decide which constraints mattered most?
  - Priority was chosen as the primary constraint because life-critical tasks (medications, feeding) must happen.
  - Time was secondary because pets are flexible on exact timing but not on essential care.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  - **Exact Time Matching vs. Duration Overlap:** The `detect_conflicts()` method checks for tasks at the *exact same time* (HH:MM match) rather than checking if task durations overlap. For example, a 15-min task at 08:00 and a 30-min task at 08:15 would conflict in reality (08:00-08:15 overlap), but our scheduler only flags conflicts if both start at exactly 08:00.
- Why is that tradeoff reasonable for this scenario?
  - **Simplicity:** Exact-time matching is fast (O(n)) and easy to understand—users can glance at the schedule and spot conflicts visually.
  - **Owner flexibility:** Pet owners often have buffer time between tasks (travel, cleanup). Exact matching avoids false positives and alarm fatigue.
  - **Iterative refinement:** The owner can manually adjust times by 5-10 mins if durations overlap, which is more realistic than auto-rescheduling.
  - **Trade-off cost:** Risk of over-booking time. Future enhancement: implement duration-aware overlap detection with sliding windows.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI tools extensively throughout this project for code generation, debugging, and iterative refinement. The AI served as a collaborative coding partner, helping me rapidly prototype ideas and catch implementation issues.

-

- **Code generation**: The AI generated complete class skeletons with all attributes and empty method stubs, saving significant time on boilerplate. It then helped implement all method bodies with actual logic, including complex features like recurring task auto-generation using `timedelta`, conflict detection with exact-time matching, and sorting/filtering algorithms.

- **Debugging and testing**: When tests failed, the AI helped identify issues like incorrect assertions in conflict detection tests. It suggested fixes and explained why certain edge cases needed coverage, such as handling None values in sorting or missing pet assignments in recurrence logic.

- **Refactoring and UI integration**: The AI assisted with adding comprehensive docstrings to all methods, integrating the backend classes with Streamlit (session state, UI buttons), and enhancing the UI with professional components like dataframes and conflict warnings. It also helped structure the README with features lists and testing documentation.

The most helpful prompts were specific and iterative:
- "Implement all the methods for the classes" - led to complete, working implementations
- "Add comprehensive docstrings" - resulted in detailed method documentation
- "Create tests for edge cases" - built a robust 18-test suite covering recurrence, sorting, and conflicts
- "Update the UI to use Schedule methods" - integrated sorting, filtering, and conflict detection into Streamlit
- "Fix this test failure" - resolved assertion mismatches and improved test accuracy

These targeted prompts were more effective than vague requests, as they allowed the AI to provide precise, actionable code changes while explaining the reasoning behind each implementation decision.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

I implemented a comprehensive test suite with 18 tests covering the core scheduling behaviors and edge cases. The tests were organized into four categories:

- **Recurrence Logic** (5 tests): Verified that daily and weekly tasks auto-generate next occurrences using `timedelta`, confirmed non-recurring tasks don't create duplicates, and tested edge cases like missing pet assignments or preferred times.

- **Sorting Correctness** (5 tests): Validated chronological ordering of tasks by preferred time, proper handling of None values (sorted first), stability with already-sorted tasks, and behavior with all tasks at the same time.

- **Conflict Detection** (6 tests): Tested exact-time matching for multiple tasks at the same HH:MM, single-warning output for 2+ conflicting tasks, and edge cases like tasks without times, empty schedules, or single tasks.

- **Core Operations** (2 tests): Covered basic task completion and pet task management to ensure integration between Owner, Pet, and Task objects.

These tests were important because they validated the three critical features (recurrence, sorting, conflict detection) that make PawPal+ intelligent. They covered both happy paths (normal usage) and edge cases (missing data, boundary conditions) to ensure the system is robust and reliable for real pet owners.

**b. Confidence**

I am highly confident that the scheduler works correctly. All 18 tests pass, covering the core algorithms end-to-end. The system handles the specified requirements well, with validated recurrence logic, accurate sorting, and reliable conflict detection. Core operations are tested for integration, and the exact-time conflict strategy is intentionally simple but effective for the pet care scenario.

If I had more time, I would test additional edge cases such as:
- Duration-aware conflict detection (checking for task overlaps beyond exact times)
- Multi-pet scenarios with shared tasks or conflicting schedules across pets
- Time zone handling for owners traveling with pets
- Long-term scheduling (weekly/monthly plans) and recurrence chain validation
- UI stress testing with large numbers of tasks/pets to ensure Streamlit performance
- Integration testing with real datetime scenarios (daylight saving, leap years)

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
