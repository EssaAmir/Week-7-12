import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager

st.set_page_config(page_title="Login", page_icon="🔐")

st.header("🔐 Secure Login")

# Initialize Services
db = DatabaseManager("database/platform.db")
auth = AuthManager(db)

# 1. Check if already logged in
if "current_user" in st.session_state and st.session_state["current_user"]:
    st.success(f"You are already logged in as **{st.session_state['current_user']}**.")
    if st.button("Go to Home Dashboard"):
        st.switch_page("Home.py")
    st.stop() # Stop showing the login form

# 2. Login / Register Tabs
tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            user = auth.login_user(username, password)
            if user:
                # Login Success
                st.session_state["current_user"] = user.get_username()
                st.session_state["current_role"] = user.get_role()
                
                st.success(f"Welcome back, {user.get_username()}!")
                
                # --- THIS IS THE FIX ---
                # Force the app to move to Home.py immediately
                st.switch_page("Home.py") 
            else:
                st.error("❌ Invalid username or password")

with tab2:
    with st.form("register_form"):
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        role = st.selectbox("Role", ["user", "admin", "analyst"])
        reg_submit = st.form_submit_button("Register")
        
        if reg_submit:
            if new_user and new_pass:
                try:
                    auth.register_user(new_user, new_pass, role)
                    st.success("✅ Registration successful! Please switch to the Login tab.")
                except Exception as e:
                    st.error("Registration failed. Username may already exist.")
            else:
                st.warning("Please fill in all fields.")