import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(
    page_title="MBA Timetable App",
    page_icon="🎓",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.main-title {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
}
.card {
    background-color: white;
    padding: 18px;
    border-radius: 15px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.10);
    text-align: center;
    min-height: 120px;
}
.big-text {
    font-size: 23px;
    font-weight: 700;
    color: #1e3c72;
}
.small-text {
    font-size: 15px;
    color: #555;
}
.free-card {
    background-color: #eafaf1;
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    min-height: 120px;
    border: 1px solid #b7e4c7;
}
.class-card {
    background-color: #f8f9ff;
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    min-height: 120px;
    border: 1px solid #d6e0ff;
}
.cancel-card {
    background-color: #fdecea;
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    min-height: 120px;
    border: 1px solid #f5b7b1;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TIMETABLE DATA ----------------
timetable = {
    "Monday": {
        "8:30 - 10:00": "Strategic Management (SM)",
        "10:30 - 12:00": "Operations Planning & Control (OP&C)",
        "1:00 - 2:30": "Operations Planning & Control (OP&C)",
        "2:45 - 4:15": "Free Period"
    },
    "Tuesday": {
        "8:30 - 10:00": "Free Period",
        "10:30 - 12:00": "Supply Chain & Logistics Management (SC&LM)",
        "1:00 - 2:30": "Research Competency / Current Affairs",
        "2:45 - 4:15": "Free Period"
    },
    "Wednesday": {
        "8:30 - 10:00": "Supply Chain & Logistics Management (SC&LM)",
        "10:30 - 12:00": "Business Intelligence & Analytics (BI&A)",
        "1:00 - 2:30": "Free Period",
        "2:45 - 4:15": "Research Competency / Current Affairs"
    },
    "Thursday": {
        "8:30 - 10:00": "Ascend - Communication",
        "10:30 - 12:00": "Strategic Management (SM)",
        "1:00 - 2:30": "Ascend - Communication",
        "2:45 - 4:15": "Free Period"
    },
    "Friday": {
        "8:30 - 10:00": "Free Period",
        "10:30 - 12:00": "DEIB",
        "1:00 - 2:30": "DEIB",
        "2:45 - 4:15": "Free Period"
    },
    "Saturday": {
        "8:30 - 10:00": "Business Intelligence & Analytics (BI&A)",
        "10:30 - 12:00": "Free Period",
        "1:00 - 2:30": "Free Period",
        "2:45 - 4:15": "Free Period"
    }
}

slot_times = {
    "8:30 - 10:00": (time(8, 30), time(10, 0)),
    "10:30 - 12:00": (time(10, 30), time(12, 0)),
    "1:00 - 2:30": (time(13, 0), time(14, 30)),
    "2:45 - 4:15": (time(14, 45), time(16, 15))
}

# ---------------- SESSION STATE ----------------
if "cancelled_classes" not in st.session_state:
    st.session_state.cancelled_classes = []

# ---------------- HELPER FUNCTIONS ----------------
def is_cancelled(day, slot):
    return f"{day}_{slot}" in st.session_state.cancelled_classes


def get_effective_subject(day, slot):
    subject = timetable[day][slot]
    if is_cancelled(day, slot):
        return "Class Cancelled"
    return subject


def get_current_class():
    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = now.time()

    if current_day not in timetable:
        return "No College Today", "-", "-"

    for slot, subject in timetable[current_day].items():
        start, end = slot_times[slot]

        if start <= current_time <= end:
            if subject == "Free Period":
                return "Free Period", slot, current_day

            if is_cancelled(current_day, slot):
                return "Class Cancelled", slot, current_day

            return subject, slot, current_day

    return "No Class Right Now", "-", current_day


def get_next_class():
    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = now.time()
    days = list(timetable.keys())

    if current_day in days:
        for slot, subject in timetable[current_day].items():
            start, end = slot_times[slot]

            if current_time < start:
                if subject != "Free Period" and not is_cancelled(current_day, slot):
                    return subject, slot, current_day

    if current_day in days:
        start_index = days.index(current_day) + 1
    else:
        start_index = 0

    for i in range(len(days)):
        day = days[(start_index + i) % len(days)]

        for slot, subject in timetable[day].items():
            if subject != "Free Period" and not is_cancelled(day, slot):
                return subject, slot, day

    return "No Upcoming Class", "-", "-"


def get_today_schedule():
    today = datetime.now().strftime("%A")
    if today in timetable:
        return today, timetable[today]
    return today, {}


def get_subject_status(day, slot):
    subject = timetable[day][slot]

    if subject == "Free Period":
        return "Free Period"

    if is_cancelled(day, slot):
        return "Class Cancelled"

    return subject


def create_effective_dataframe():
    effective = {}

    for day, slots in timetable.items():
        effective[day] = {}

        for slot, subject in slots.items():
            if subject != "Free Period" and is_cancelled(day, slot):
                effective[day][slot] = "Class Cancelled"
            else:
                effective[day][slot] = subject

    return pd.DataFrame(effective).T


# ---------------- HEADER ----------------
st.markdown("""
<div class="main-title">
    <h1>🎓 MBA IV Trimester Timetable App</h1>
    <h3>Personalized Timetable: OP&C + DEIB</h3>
    <p>With Live Current Class, Next Class & Class Cancellation Update</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Menu")
menu = st.sidebar.radio(
    "Select View",
    [
        "Dashboard",
        "Today's Schedule",
        "Weekly Calendar",
        "Cancel / Restore Class",
        "Attendance Tracker",
        "Subject Summary"
    ]
)

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.subheader("📍 Live Timetable Dashboard")

    current_subject, current_slot, current_day = get_current_class()
    next_subject, next_slot, next_day = get_next_class()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="small-text">Current Status</div><br>
            <div class="big-text">{current_subject}</div><br>
            <div class="small-text">{current_day} | {current_slot}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="small-text">Next Class</div><br>
            <div class="big-text">{next_subject}</div><br>
            <div class="small-text">{next_day} | {next_slot}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    today, today_schedule = get_today_schedule()
    st.subheader(f"📅 Today's Schedule - {today}")

    if today_schedule:
        cols = st.columns(4)

        for i, (slot, subject) in enumerate(today_schedule.items()):
            effective_subject = get_subject_status(today, slot)

            with cols[i]:
                if effective_subject == "Free Period":
                    st.markdown(f"""
                    <div class="free-card">
                        <div class="small-text">{slot}</div><br>
                        <div class="big-text">Free Period</div>
                    </div>
                    """, unsafe_allow_html=True)

                elif effective_subject == "Class Cancelled":
                    st.markdown(f"""
                    <div class="cancel-card">
                        <div class="small-text">{slot}</div><br>
                        <div class="big-text">Class Cancelled</div>
                        <div class="small-text">{subject}</div>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    st.markdown(f"""
                    <div class="class-card">
                        <div class="small-text">{slot}</div><br>
                        <div class="big-text">{effective_subject}</div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.success("No classes today!")

# ---------------- TODAY'S SCHEDULE ----------------
elif menu == "Today's Schedule":
    today, today_schedule = get_today_schedule()
    st.subheader(f"📅 Today's Schedule - {today}")

    if today_schedule:
        for slot, subject in today_schedule.items():
            effective_subject = get_subject_status(today, slot)

            if effective_subject == "Free Period":
                st.success(f"{slot} : Free Period")

            elif effective_subject == "Class Cancelled":
                st.error(f"{slot} : Class Cancelled - {subject}")

            else:
                st.info(f"{slot} : {effective_subject}")
    else:
        st.success("No classes today!")

# ---------------- WEEKLY CALENDAR ----------------
elif menu == "Weekly Calendar":
    st.subheader("🗓️ Weekly Calendar View")

    effective_df = create_effective_dataframe()
    st.dataframe(effective_df, use_container_width=True)

    st.markdown("### Colored View")

    for day, slots in timetable.items():
        st.markdown(f"#### {day}")
        cols = st.columns(4)

        for i, (slot, subject) in enumerate(slots.items()):
            effective_subject = get_subject_status(day, slot)

            with cols[i]:
                if effective_subject == "Free Period":
                    st.markdown(f"""
                    <div class="free-card">
                        <div class="small-text">{slot}</div><br>
                        <div class="big-text">Free</div>
                    </div>
                    """, unsafe_allow_html=True)

                elif effective_subject == "Class Cancelled":
                    st.markdown(f"""
                    <div class="cancel-card">
                        <div class="small-text">{slot}</div><br>
                        <div class="big-text">Cancelled</div>
                        <div class="small-text">{subject}</div>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    st.markdown(f"""
                    <div class="class-card">
                        <div class="small-text">{slot}</div><br>
                        <div class="big-text">{effective_subject}</div>
                    </div>
                    """, unsafe_allow_html=True)

# ---------------- CANCEL / RESTORE CLASS ----------------
elif menu == "Cancel / Restore Class":
    st.subheader("❌ Cancel / Restore Class")

    selected_day = st.selectbox("Select Day", list(timetable.keys()))

    selected_slot = st.selectbox("Select Time Slot", list(timetable[selected_day].keys()))

    selected_subject = timetable[selected_day][selected_slot]

    st.info(f"Selected: {selected_day} | {selected_slot} | {selected_subject}")

    if selected_subject == "Free Period":
        st.warning("This is already a free period. No need to cancel it.")

    else:
        class_key = f"{selected_day}_{selected_slot}"

        if class_key in st.session_state.cancelled_classes:
            st.error("Status: This class is currently marked as cancelled.")

            if st.button("Restore Class"):
                st.session_state.cancelled_classes.remove(class_key)
                st.success("Class restored successfully.")
                st.rerun()

        else:
            st.success("Status: This class is currently active.")

            if st.button("Cancel This Class"):
                st.session_state.cancelled_classes.append(class_key)
                st.success("Class cancelled successfully.")
                st.rerun()

    st.markdown("---")
    st.subheader("Cancelled Classes List")

    if st.session_state.cancelled_classes:
        cancelled_list = []

        for item in st.session_state.cancelled_classes:
            day, slot = item.split("_", 1)
            cancelled_list.append({
                "Day": day,
                "Time Slot": slot,
                "Subject": timetable[day][slot]
            })

        cancelled_df = pd.DataFrame(cancelled_list)
        st.dataframe(cancelled_df, use_container_width=True)

    else:
        st.success("No classes are cancelled.")

# ---------------- ATTENDANCE TRACKER ----------------
elif menu == "Attendance Tracker":
    st.subheader("✅ Subject Attendance Tracker")

    subjects = [
        "Strategic Management (SM)",
        "Operations Planning & Control (OP&C)",
        "Supply Chain & Logistics Management (SC&LM)",
        "Business Intelligence & Analytics (BI&A)",
        "Research Competency / Current Affairs",
        "Ascend - Communication",
        "DEIB"
    ]

    attendance_data = []

    st.write("Enter conducted and attended classes for each subject:")

    for subject in subjects:
        st.markdown(f"### {subject}")
        col1, col2 = st.columns(2)

        with col1:
            conducted = st.number_input(
                f"Classes Conducted - {subject}",
                min_value=0,
                value=0,
                key=f"conducted_{subject}"
            )

        with col2:
            attended = st.number_input(
                f"Classes Attended - {subject}",
                min_value=0,
                value=0,
                key=f"attended_{subject}"
            )

        if attended > conducted:
            st.warning("Attended classes cannot be more than conducted classes.")

        if conducted > 0:
            attendance_percent = round((attended / conducted) * 100, 2)
        else:
            attendance_percent = 0

        attendance_data.append({
            "Subject": subject,
            "Classes Conducted": conducted,
            "Classes Attended": attended,
            "Attendance %": attendance_percent
        })

    attendance_df = pd.DataFrame(attendance_data)

    st.markdown("---")
    st.subheader("📊 Attendance Summary")
    st.dataframe(attendance_df, use_container_width=True)

    overall_conducted = attendance_df["Classes Conducted"].sum()
    overall_attended = attendance_df["Classes Attended"].sum()

    if overall_conducted > 0:
        overall_percentage = round((overall_attended / overall_conducted) * 100, 2)
    else:
        overall_percentage = 0

    st.metric("Overall Attendance Percentage", f"{overall_percentage}%")

    if overall_percentage >= 85:
        st.success("Excellent attendance status.")
    elif overall_percentage >= 75:
        st.warning("Attendance is safe, but keep monitoring.")
    else:
        st.error("Attendance is below 75%. Focus on attending more classes.")

# ---------------- SUBJECT SUMMARY ----------------
elif menu == "Subject Summary":
    st.subheader("📚 Weekly Subject Summary")

    all_subjects = []

    for day, slots in timetable.items():
        for slot, subject in slots.items():
            if subject != "Free Period" and not is_cancelled(day, slot):
                all_subjects.append(subject)

    summary_df = pd.DataFrame(all_subjects, columns=["Subject"])
    subject_count = summary_df["Subject"].value_counts().reset_index()
    subject_count.columns = ["Subject", "Active Sessions per Week"]

    st.dataframe(subject_count, use_container_width=True)

    total_classes = len(all_subjects)
    total_free = sum(
        1 for day in timetable.values()
        for subject in day.values()
        if subject == "Free Period"
    )
    total_cancelled = len(st.session_state.cancelled_classes)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Active Classes per Week", total_classes)

    with col2:
        st.metric("Free Periods per Week", total_free)

    with col3:
        st.metric("Cancelled Classes", total_cancelled)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<center>Designed for MBA IV Trimester | Smart Timetable + Cancellation Tracker</center>",
    unsafe_allow_html=True
)
