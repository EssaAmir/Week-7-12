import streamlit as st
from services.database_manager import DatabaseManager
from models.dataset import Dataset
import pandas as pd

st.set_page_config(page_title="Data Science", page_icon="📊")

st.header("📊 Data Science & Analytics")

#Connect to the Database
db= DatabaseManager("database/platform.db")
db.connect()

#2. Add New Dataset Form
with st.expander("📂 Upload New Dataset Metadata"):
    with st.form("new_dataset"):
        name =st.text_input("Dataset Name")
        source= st.text_input("Source URL/Path")
        rows =st.number_input("Number of Rows", min_value=0)
        size= st.number_input("Size in Bytes", min_value=0)
        
        if st.form_submit_button("Save Metadata"):
            db.execute_query(
                "INSERT INTO datasets_metadata (name, size_bytes, rows, source) VALUES (?, ?, ?, ?)",
                (name, size, rows, source)
            )
            st.success("Dataset saved!")
            st.rerun()

# 3.Fetch Data
raw_data= db.fetch_all("SELECT id, name, size_bytes, rows, source FROM datasets_metadata")

#4. Convert to Objects (OOP)
datasets= []
for row in raw_data:
    #row=(id, name, size, rows, source)
    datasets.append(Dataset(row[0], row[1], row[2], row[3], row[4]))

#5. Display Dashboard
col1, col2=st.columns(2)
col1.metric("Total Datasets", len(datasets))
col2.metric("Total Rows Processed", sum(d._rows for d in datasets)) #Accessing the attribute directly for sum

st.divider()
st.subheader("Available Datasets")

for data in datasets:
    with st.container(border=True):
        c1, c2= st.columns([3, 1])
        with c1:
            st.markdown(f"**{data._name}**")
            st.caption(f"Source: {data.get_source()}")
        with c2:
            # Uses the OOP method calculate_size_mb() defined in Week 11 PDF
            st.info(f"{data.calculate_size_mb():.2f} MB")

#implementing visual analytics for dataset metadata
            st.divider()
st.subheader("💾 Storage Analytics")

#1. Get Data
#We already have 'datasets' list, but for charts, we'll use a DataFrame
data= db.fetch_all("SELECT name, size_bytes, rows FROM datasets_metadata")
df =pd.DataFrame(data, columns=["Name", "Size (Bytes)", "Rows"])

#Convert Bytes to MB for easier reading
df["Size (MB)"]= df["Size (Bytes)"] / (1024 * 1024)

#2. Layout
c1, c2= st.columns(2)

with c1:
    st.markdown("**Top Largest Datasets (MB)**")
    #barbchart showing which datasets take up the most space
    st.bar_chart(df.set_index("Name")["Size (MB)"])

with c2:
    st.markdown("**Row Count Distribution**")
    #scatter plot to see relationship between size and rows
    st.scatter_chart(df, x="Rows", y="Size (MB)")