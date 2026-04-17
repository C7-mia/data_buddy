import streamlit as st
import pandas as pd
from data_buddy import project_analyzer
import solver
import os

st.set_page_config(page_title="Universal Data Buddy", page_icon="🌍")

st.title("🌍 Universal Data Buddy")
st.markdown("### The No-Code Assistant for Maji Ndogo & Beyond")

# 1. THE UPLOADER (The "No-Code" Help)
uploaded_file = st.file_uploader("Drop your CSV or Student ZIP here", type=['csv', 'zip'])

if uploaded_file is not None:
    # Save the file temporarily
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"Loaded: {uploaded_file.name}")
    
    # 2. THE LOGIC (Using your previous project_analyzer)
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file.name)
        df = project_analyzer.universal_cleaner(df)
        
        st.subheader("📊 Quick Analysis")
        st.write(df.describe())
        
        # Check for Maji Ndogo specific patterns
        if 'type_of_water_source' in df.columns:
            st.info("💡 Maji Ndogo Data Detected! Calculating outputs...")
            answers = solver.solve_maji_ndogo_challenge(df)
            st.json(answers)
            
    elif uploaded_file.name.endswith('.zip'):
        st.warning("📦 ZIP detected. Extracting files...")
        folder, files = project_analyzer.unpack_and_list_data(uploaded_file.name)
        st.write(f"Files found inside: {files}")
        # Further extraction logic would go here