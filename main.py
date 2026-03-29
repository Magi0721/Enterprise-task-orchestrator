import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Enterprise Task Orchestrator", page_icon="📋", layout="wide")

# ---- CSS ----
st.markdown("""
<style>
.task-box {
    background-color: #f0f2f6;
    color: #000000;
    padding: 15px;
    margin-bottom: 5px;
    border-radius: 10px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
}
.status-pending { color: orange; font-weight: bold; }
.status-completed { color: green; font-weight: bold; }
.status-escalated { color: red; font-weight: bold; }
.audit-box {
    margin-left: 15px;
    margin-bottom: 15px;
    padding: 10px;
    border-left: 3px solid #999;
    background-color: #fafafa;
}
</style>
""", unsafe_allow_html=True)

st.title("📋 Enterprise Task Orchestrator Demo")

# ---- SESSION STATE ----
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"id": 1, "name": "Prepare Report", "status": "Pending", "assigned_to": "Alice", "history": []},
        {"id": 2, "name": "Approve Budget", "status": "Pending", "assigned_to": "Bob", "history": []},
    ]

if "counter" not in st.session_state:
    st.session_state.counter = 3

# ---- LOGIN ----
employees = ["Alice", "Bob", "Charlie", "David"]
role = st.selectbox("Select Role", ["Employee", "Manager"])
username = st.selectbox("Select Your Name", employees)

st.markdown("---")

# ---- HELPERS ----
def log_action(task, action):
    task["history"].append(
        f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - {username} ({role}) -> {action}"
    )

def update_task(idx, action):
    if action == "Complete":
        st.session_state.tasks[idx]["status"] = "Completed"
    elif action == "Escalate":
        st.session_state.tasks[idx]["status"] = "Escalated"
    elif action == "Reset":
        st.session_state.tasks[idx]["status"] = "Pending"
    log_action(st.session_state.tasks[idx], action)

def delete_task(idx):
    log_action(st.session_state.tasks[idx], "Deleted")
    st.session_state.tasks.pop(idx)

def add_task(name, assignee):
    task = {
        "id": st.session_state.counter,
        "name": name,
        "status": "Pending",
        "assigned_to": assignee,
        "history": [
            f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - {username} ({role}) -> Created"
        ],
    }
    st.session_state.tasks.append(task)
    st.session_state.counter += 1

# ---- DISPLAY TASKS ----
for idx, task in enumerate(st.session_state.tasks):
    if role == "Employee" and task["assigned_to"] != username:
        continue

    # Task Card
    st.markdown(
        f"""
        <div class="task-box">
            <b>#{task['id']} {task['name']}</b> - 
            <span class="status-{task['status'].lower()}">{task['status']}</span><br>
            <i>Assigned to: {task['assigned_to']}</i>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---- AUDIT TRAIL (VISIBLE) ----
    st.markdown('<div class="audit-box">', unsafe_allow_html=True)
    st.markdown("**Audit Trail:**")

    if task["history"]:
        for i, entry in enumerate(task["history"]):
            if i == len(task["history"]) - 1:
                st.markdown(f"**{entry}**")  # latest action bold
            else:
                st.markdown(entry)
    else:
        st.write("No actions yet")

    st.markdown('</div>', unsafe_allow_html=True)

    # ---- ACTION BUTTONS ----
    col1, col2, col3, col4 = st.columns([1,1,1,1])

    with col1:
        if st.button("✅ Complete", key=f"complete_{idx}"):
            update_task(idx, "Complete")

    with col2:
        if st.button("⚠️ Escalate", key=f"escalate_{idx}"):
            update_task(idx, "Escalate")

    with col3:
        if st.button("🔄 Reset", key=f"reset_{idx}"):
            update_task(idx, "Reset")

    with col4:
        if role == "Manager":
            if st.button("🗑️ Delete", key=f"delete_{idx}"):
                delete_task(idx)

# ---- ADD TASK ----
if role == "Manager":
    st.markdown("---")
    st.subheader("➕ Add New Task")

    new_name = st.text_input("Task Name", key="new_task_input")
    assignee = st.selectbox("Assign to Employee", employees, key="assign_employee")

    if st.button("Add Task"):
        if new_name.strip() != "":
            add_task(new_name.strip(), assignee)
            st.success(f"Task '{new_name.strip()}' assigned to {assignee} added!")
