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
    font-size: 24px;
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

df = pd.DataFrame(timetable).T

# ---------------- FUNCTIONS ----------------
def get_current_class():
    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = now.time()

    if current_day not in timetable:
        return "No College Today", "-", "-"

    for slot, subject in timetable[current_day].items():
        start, end = slot_times[slot]
        if start <= current_time <= end:
            return subject, slot, current_day

    return "No Class Right Now", "-", current_day


def get_next_class():
    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = now.time()
    days = list(timetable.keys())

    if current_day in days:
        today_slots = timetable[current_day]
        for slot, subject in today_slots.items():
            start, end = slot_times[slot]
            if current_time < start and subject != "Free Period":
                return subject, slot, current_day

    if current_day in days:
        start_index = days.index(current_day) + 1
    else:
        start_index = 0

    for i in range(len(days)):
        day = days[(start_index + i) % len(days)]
        for slot, subject in timetable[day].items():
            if subject != "Free Period":
                return subject, slot, day

    return "No Upcoming Class", "-", "-"


def get_today_schedule():
    today = datetime.now().strftime("%A")
    if today in timetable:
        return today, timetable[today]
    return today, {}


# ---------------- HEADER ----------------
st.markdown("""
<div class="main-title">
    <h1>🎓 MBA IV Trimester Timetable App</h1>
    <h3>Personalized Timetable: OP&C + DEIB</h3>
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
            with cols[i]:
                if subject == "Free Period":
                    st.markdown(f"""
                    <div class="free-card">
                        <div class="small-text">{slot}</div><br>
                        <div class="big-text">Free Period</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="class-card">
                        <div class="small-text">{slot}</div><br>
                        <div class="big-text">{subject}</div>
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
            if subject == "Free Period":
                st.success(f"{slot} : Free Period")
            else:
                st.info(f"{slot} : {subject}")
    else:
        st.success("No classes today!")

# ---------------- WEEKLY CALENDAR ----------------
elif menu == "Weekly Calendar":
    st.subheader("🗓️ Weekly Calendar View")
    st.dataframe(df, use_container_width=True)

    st.markdown("### Colored View")

    for day, slots in timetable.items():
        st.markdown(f"#### {day}")
        cols = st.columns(4)

        for i, (slot, subject) in enumerate(slots.items()):
            with cols[i]:
                if subject == "Free Period":
                    st.markdown(f"""
                    <div class="free-card">
                        <div class="small-text">{slot}</div><br>
                        <div class="big-text">Free</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="class-card">
                        <div class="small-text">{slot}</div><br>
                        <div class="big-text">{subject}</div>
                    </div>
                    """, unsafe_allow_html=True)

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
            if subject != "Free Period":
                all_subjects.append(subject)

    summary_df = pd.DataFrame(all_subjects, columns=["Subject"])
    subject_count = summary_df["Subject"].value_counts().reset_index()
    subject_count.columns = ["Subject", "Sessions per Week"]

    st.dataframe(subject_count, use_container_width=True)

    total_classes = len(all_subjects)
    total_free = sum(
        1 for day in timetable.values()
        for subject in day.values()
        if subject == "Free Period"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Classes per Week", total_classes)

    with col2:
        st.metric("Total Free Periods per Week", total_free)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<center>Designed for MBA IV Trimester | Timetable + Attendance Dashboard</center>",
    unsafe_allow_html=True
)
