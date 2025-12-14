import streamlit as st
from services.database_manager import DatabaseManager
from models.it_ticket import ITTicket
import pandas as pd

st.set_page_config(page_title="IT Operations", page_icon="💻")

st.header("💻 IT Operations & Support")

#1. Connect to Database
db= DatabaseManager("database/platform.db")
db.connect()

#Create Ticket Form
with st.expander("🎫 Create Support Ticket"):
    with st.form("new_ticket"):
        title= st.text_input("Issue Title")
        priority =st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        assigned=st.selectbox("Assign To", ["Unassigned", "Alice", "Bob", "Charlie"])
        
        if st.form_submit_button("Open Ticket"):
            db.execute_query(
                "INSERT INTO it_tickets (title, priority, status, assigned_to) VALUES (?, ?, ?, ?)",
                (title, priority, "Open", assigned)
            )
            st.success("Ticket Created!")
            st.rerun()

#3.Fetch Data
raw_data =db.fetch_all("SELECT id, title, priority, status, assigned_to FROM it_tickets")

#4.Convert to Objects(OOP)
tickets= []
for row in raw_data:
    tickets.append(ITTicket(row[0], row[1], row[2], row[3], row[4]))

#5. Display Tickets
st.divider()
st.subheader("Ticket Queue")

# Simple filter
status_filter =st.radio("Filter by Status", ["All", "Open", "Closed"], horizontal=True)

for ticket in tickets:
    # Apply Filter
    if status_filter != "All" and ticket.get_status() != status_filter:
        continue

    with st.container(border=True):
        c1, c2, c3 =st.columns([4, 2, 2])
        
        with c1:
            st.markdown(f"**#{ticket._id} - {ticket._title}**")
            st.caption(f"Assigned to: {ticket._assigned_to}")
            
        with c2:
            prio= ticket._priority
            color= "red" if prio == "Critical" else "orange" if prio == "High" else "blue"
            st.markdown(f":{color}[{prio}]")
            
        with c3:
            # Action Button to close ticket
            if ticket.get_status()== "Open":
                if st.button("Close Ticket", key=f"close_{ticket._id}"):
                    db.execute_query("UPDATE it_tickets SET status = 'Closed' WHERE id = ?", (ticket._id,))
                    st.rerun()
            else:
                st.success("Closed")


#implementing visual analytics for IT tickets
st.divider()
st.subheader("📈 Operational Metrics")

# 1. Get Data
data=db.fetch_all("SELECT priority, status, assigned_to FROM it_tickets")
df =pd.DataFrame(data, columns=["Priority", "Status", "Assignee"])

# 2. Layout
c1, c2 =st.columns(2)

with c1:
    st.markdown("**Ticket Volume by Priority**")
    #Helps spot if there are too many 'Critical' tickets, enabling better resource allocation
    st.bar_chart(df["Priority"].value_counts())

with c2:
    st.markdown("**Workload by Staff Member**")
    #Solves the "Staff performance anomaly" problem from the PDF
    st.bar_chart(df["Assignee"].value_counts(), color="#4bbf73") #Green for staff