import streamlit as st

from pawpal_sytem import Owner, Pet, Task, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Initialize session state for persistent data
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", email="jordan@example.com", phone="555-1234")

if 'pets' not in st.session_state:
    st.session_state.pets = []

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")

# Update owner info when it changes
if st.button("Update Owner Info"):
    st.session_state.owner.update_info(
        name=owner_name,
        email=st.session_state.owner.email,
        phone=st.session_state.owner.phone
    )
    st.success(f"✓ Owner updated: {owner_name}")

st.markdown("### Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi", key="pet_name_input")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"], key="species_input")

if st.button("Add Pet"):
    new_pet = Pet(name=pet_name, species=species, breed="Unknown", age=1, weight=50.0)
    st.session_state.owner.add_pet(new_pet)
    st.session_state.pets.append(new_pet)
    st.success(f"✓ {pet_name} ({species}) added!")

# Display current pets
if st.session_state.pets:
    st.write("**Your Pets:**")
    for pet in st.session_state.pets:
        st.write(f"  🐾 {pet.name} ({pet.species})")
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Add a Task")
if st.session_state.pets:
    selected_pet = st.selectbox("Select pet for task", [p.name for p in st.session_state.pets], key="pet_selector")
    pet_obj = next(p for p in st.session_state.pets if p.name == selected_pet)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk", key="task_input")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="duration_input")
    with col3:
        priority_map = {"high": 1, "medium": 2, "low": 3}
        priority_label = st.selectbox("Priority", ["high", "medium", "low"], index=2, key="priority_input")
        priority = priority_map[priority_label]

    if st.button("Add Task"):
        new_task = Task(
            type="Care Task",
            description=task_title,
            duration=int(duration),
            priority=priority,
            frequency="Daily",
            pet=pet_obj
        )
        pet_obj.add_task(new_task)
        st.session_state.tasks.append(new_task)
        st.success(f"✓ Task '{task_title}' added to {selected_pet}!")

    # Display tasks for selected pet
    if pet_obj.get_tasks():
        st.write(f"**Tasks for {selected_pet}:**")
        for task in pet_obj.get_tasks():
            st.write(f"  • {task.description} ({task.duration}min) - Priority: {task.priority}")
    else:
        st.info(f"No tasks yet for {selected_pet}.")
else:
    st.warning("⚠️ Add a pet first before adding tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily schedule for your pets.")

if st.button("Generate Schedule"):
    if not st.session_state.tasks:
        st.warning("⚠️ Add some tasks first!")
    else:
        # Create a schedule for today
        from datetime import date
        schedule = Schedule(schedule_date=date.today())
        
        # Add all tasks to the schedule
        for task in st.session_state.tasks:
            schedule.add_task(task)
        
        # Generate prioritized plan
        schedule.generate_plan(priorities=True)
        
        # Display the schedule
        st.subheader("📅 Today's Schedule")
        schedule_output = schedule.display_plan()
        st.text(schedule_output)
        
        st.success("✓ Schedule generated successfully!")
