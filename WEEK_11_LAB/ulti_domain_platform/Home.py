import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Intelligence Platform",
    page_icon="🖥️",
    layout="wide"
)

# 2. Session State Initialization (CRITICAL for Week 11)
# We must ensure these variables exist so other pages don't crash
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
    st.session_state["current_role"] = None

# 3. Main Dashboard UI
col1, col2 = st.columns([3, 1]) 

with col1:
    st.title("🖥️ Multi-Domain Intelligence Platform")
    st.markdown("### Centralized Command Center")
    st.info("""
    **System Architecture (Week 11 Refactor)**
    This application has been refactored into a micro-service architecture:
    * **📂 Models:** OOP Classes for data (User, Incident, Ticket)
    * **⚙️ Services:** Managers for Database, Auth, and AI
    * **📄 Pages:** Modular interfaces for each domain
    """)

with col2:
    # A simple status dashboard
    st.metric(label="System Status", value="Online", delta="Stable")
    st.metric(label="Architecture", value="OOP", delta="Week 11")

st.divider()

# 4. Login Status Check
# This logic uses the variables we set up in pages/1_Login.py
if st.session_state["current_user"]:
    with st.container(border=True):
        st.success(f"✅ Active Session: **{st.session_state['current_user']}**")
        st.caption(f"Role: {st.session_state['current_role']}")
        st.write("👈 You may now access the **Cybersecurity**, **Data Science**, and **IT Operations** modules.")
else:
    st.warning("⚠️ Access Restricted")
    st.write("You are currently browsing as a guest.")
    st.markdown("Please navigate to **🔐 Login** in the sidebar to access full features.")