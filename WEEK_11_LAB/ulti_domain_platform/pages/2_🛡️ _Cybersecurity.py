import streamlit as st
import pandas as pd
from services.database_manager import DatabaseManager
from models.security_incident import SecurityIncident

st.set_page_config(page_title="Cybersecurity", page_icon="🛡️")

st.header("🛡️ Cybersecurity Operations")

#1.Connect to Database
db= DatabaseManager("database/platform.db")
db.connect()

#2. Incident Form
with st.expander("🚨 Report New Incident"):
    with st.form("new_incident"):
        title= st.text_input("Incident Title")
        inc_type=st.selectbox("Type", ["Phishing", "Malware", "DDoS", "Ransomware", "Insider Threat"])
        severity= st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        desc=st.text_area("Description")
        
        if st.form_submit_button("Submit Report"):
            #Saves the 'incident_type' correctly now
            db.execute_query(
                "INSERT INTO cyber_incidents (title, incident_type, severity, description, status) VALUES (?, ?, ?, ?, ?)",
                (title, inc_type, severity, desc, "Open")
            )
            st.success("Incident Reported!")
            st.rerun()

#Fetch Data
#This query matches the new database structure, including 'incident_type' as required
rows = db.fetch_all("SELECT id, title, severity, status, description, incident_type FROM cyber_incidents")

#4.Convert to Objects
incidents= []
for row in rows:
    # row indices: 0=id, 1=title, 2=severity, 3=status, 4=desc, 5=type
    inc =SecurityIncident(row[0], row[1], row[2], row[3], row[4])
    # We attach the type manually since it wasn't in the original Week 11 class
    inc.type= row[5] 
    incidents.append(inc)

#5. Visualizations (The Requirement for Tier 1/2/3)
st.divider()
st.subheader("📈 Threat Analytics")

if incidents:
    #Create a DataFrame for the charts
    df= pd.DataFrame(rows, columns=["ID", "Title", "Severity", "Status", "Description", "Type"])

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Incident Frequency by Type**")
        st.bar_chart(df["Type"].value_counts())

    with col2:
        st.markdown("**Severity Distribution**")
        st.bar_chart(df["Severity"].value_counts(), color="#ff4b4b")
else:
    st.info("No incidents found. Add one above to see analytics!")

#6. Incident List
st.divider()
st.subheader("📋 Active Incidents")
for incident in incidents:
    with st.container(border=True):
        c1, c2 =st.columns([3, 1])
        with c1:
            st.markdown(f"**{incident.title}**")
            st.caption(f"Type: {getattr(incident, 'type', 'Unknown')} | {incident.get_description()}")
        with c2:
            st.error(f"{incident.get_severity()}")