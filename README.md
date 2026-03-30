# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling Features

PawPal+ includes advanced scheduling algorithms for intelligent pet care planning:

### Task Sorting
- **`Schedule.sort_by_time()`**: Sorts tasks chronologically by preferred_time. Tasks with no time are sorted first.
- Enables visualization of the day's activities in order.

### Task Filtering
- **`Schedule.filter_tasks(completed, pet_name)`**: Filters tasks by completion status and/or pet name.
- Example: Get all incomplete tasks for "Fido" to see what still needs attention.

### Recurring Tasks
- **`Task.mark_complete()`**: When a daily/weekly task is completed, automatically creates the next occurrence.
- Uses Python's `timedelta` to accurately schedule future tasks (avoiding manual re-entry).
- Example: Complete this morning's walk → next walk is automatically scheduled for tomorrow.

### Conflict Detection
- **`Schedule.detect_conflicts()`**: Identifies tasks scheduled at the exact same time (HH:MM match).
- Returns human-readable warnings instead of crashing.
- Tradeoff: Uses exact-time matching for simplicity vs. duration-overlap detection (see reflection.md for details).

### Example Output
```
Detecting scheduling conflicts...
Found conflicts:
  ⚠️ CONFLICT at 09:00: Fido morning walk (Fido), Fido grooming (Fido)
```

## Testing PawPal+

PawPal+ includes a comprehensive test suite covering core scheduling behaviors and edge cases.

### Run Tests

```bash
python -m pytest tests/test_pawpal.py -v
```

### Test Coverage

The test suite includes **18 tests** across four categories:

1. **Recurrence Logic** (5 tests)
   - Verifies that daily/weekly tasks auto-generate next occurrences using `timedelta`
   - Confirms non-recurring tasks don't create duplicates
   - Edge cases: missing pet assignment, missing preferred time

2. **Sorting Correctness** (5 tests)
   - Validates chronological ordering of tasks by time
   - Handles None values (sorted first)
   - Tests stability with already-sorted and same-time tasks

3. **Conflict Detection** (6 tests)
   - Identifies multiple tasks at the exact same time (HH:MM)
   - Validates single-warning output for 2+ tasks at same time
   - Edge cases: tasks without times, empty schedule, single task

4. **Core Operations** (2 tests)
   - Task completion and pet task management
   - Basic integration between Owner, Pet, and Task objects

### Confidence Level

⭐⭐⭐⭐⭐ **5/5 stars**

**Rationale**: All 18 tests pass, covering happy paths, edge cases, and the three critical features (recurrence, sorting, conflict detection). The exact-time conflict detection is intentionally simple but robust. Core operations are validated end-to-end. System is production-ready for the specified requirements.
