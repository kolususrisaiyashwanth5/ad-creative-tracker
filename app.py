import streamlit as st
import pandas as pd
import os

# --- CONFIG ---
st.set_page_config(page_title="Ad Creative Tracker", layout="centered")

# --- FILE PATH ---
DATA_FILE = "creatives.csv"

# --- PAGE HEADER ---
st.title(" Ad Creative Tracker")
st.markdown("Track and manage ad creatives across campaigns with live status and feedback.")

st.markdown("---")

# --- CREATIVE FORM ---
st.subheader("➕ Add New Creative")

with st.form("creative_form"):
    col1, col2 = st.columns(2)
    with col1:
        creative_name = st.text_input("Creative Name")
        campaign = st.text_input("Campaign Name")
    with col2:
        status = st.selectbox("Status", ["Submitted", "In Review", "Approved", "Rejected"])
        notes = st.text_area("Client Notes / Feedback")

    submitted = st.form_submit_button("Add Creative")

# --- SAVE DATA ---
if submitted:
    new_entry = {
        "Creative Name": creative_name,
        "Campaign": campaign,
        "Status": status,
        "Notes": notes
    }

    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    else:
        df = pd.DataFrame([new_entry])

    df.to_csv(DATA_FILE, index=False)
    st.success(f"Creative '{creative_name}' added successfully!")

# --- DISPLAY ENTRIES ---
st.markdown("---")
st.subheader("📋 Creative List")

# Load data if file exists
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        campaign_filter = st.selectbox("Filter by Campaign", ["All"] + sorted(df["Campaign"].dropna().unique()))
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All"] + sorted(df["Status"].dropna().unique()))

    filtered_df = df.copy()
    if campaign_filter != "All":
        filtered_df = filtered_df[filtered_df["Campaign"] == campaign_filter]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]

    st.dataframe(filtered_df, use_container_width=True)
else:
    st.info("No creatives added yet.")
