"""
Health Prediction Application - Streamlit Frontend
This file contains the main user interface for the health prediction app.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
from database import init_db, add_patient, get_all_patients, update_patient, delete_patient, get_patient_by_id
from health_predictor import predict_health_status

# Configure Streamlit page
st.set_page_config(
    page_title="Health Prediction App",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for better styling
st.markdown("""
    <style>
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin-bottom: 15px;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
        margin-bottom: 15px;
    }
    .info-box {
        background-color: #d1ecf1;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #17a2b8;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize database
init_db()

# Sidebar navigation
st.sidebar.title("🏥 Health Prediction App")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Operation",
    ["📊 Dashboard", "➕ Add Patient", "👁️ View Patients", "✏️ Update Patient", "🗑️ Delete Patient"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**About This App:**\n\n"
    "This application helps track patient health metrics and predict potential health risks based on blood test results using AI."
)

# ======================== DASHBOARD PAGE ========================
if page == "📊 Dashboard":
    st.markdown("""
        <div class="header-container">
            <h1>🏥 Health Prediction Dashboard</h1>
            <p>Manage patient records and predict health risks</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get all patients
    patients = get_all_patients()
    
    if patients:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Patients", len(patients))
        
        with col2:
            high_glucose = len([p for p in patients if p[4] and float(p[4]) > 126])
            st.metric("High Glucose Count", high_glucose)
        
        with col3:
            high_cholesterol = len([p for p in patients if p[6] and float(p[6]) > 200])
            st.metric("High Cholesterol", high_cholesterol)
        
        with col4:
            low_hemoglobin = len([p for p in patients if p[5] and float(p[5]) < 12])
            st.metric("Low Hemoglobin", low_hemoglobin)
        
        st.markdown("---")
        st.subheader("📋 Patient Records Overview")
        
        # Create dataframe for display
        data = []
        for patient in patients:
            data.append({
                "ID": patient[0],
                "Full Name": patient[1],
                "DOB": patient[2],
                "Email": patient[3],
                "Glucose": patient[4],
                "Hemoglobin": patient[5],
                "Cholesterol": patient[6],
                "Remarks": patient[7]
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, width='stretch', hide_index=True)
    else:
        st.markdown("""
            <div class="info-box">
                <strong>No Patients Found</strong><br>
                Use the "Add Patient" option from the sidebar to create patient records.
            </div>
        """, unsafe_allow_html=True)

# ======================== ADD PATIENT PAGE ========================
elif page == "➕ Add Patient":
    st.markdown("""
        <div class="header-container">
            <h2>➕ Add New Patient</h2>
            <p>Fill in the patient details to create a new record</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("add_patient_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input(
                "Full Name *",
                placeholder="Enter patient's full name",
                help="Patient's complete name"
            )
            dob = st.date_input(
                "Date of Birth *",
                value=date(2000, 1, 1),
                min_value=date(1900, 1, 1),
                max_value=date.today(),
                help="Select patient's date of birth (cannot be a future date)"
            )
            glucose = st.number_input(
                "Glucose Level (mg/dL) *",
                min_value=0.0,
                max_value=500.0,
                value=0.0,
                step=0.1,
                help="Fasting glucose level in mg/dL (normal: 70-100)"
            )
        
        with col2:
            email = st.text_input(
                "Email Address *",
                placeholder="example@email.com",
                help="Patient's email address"
            )
            hemoglobin = st.number_input(
                "Hemoglobin (g/dL) *",
                min_value=0.0,
                max_value=20.0,
                value=0.0,
                step=0.1,
                help="Hemoglobin level in g/dL (normal: 12-17.5)"
            )
            cholesterol = st.number_input(
                "Cholesterol (mg/dL) *",
                min_value=0.0,
                max_value=500.0,
                value=0.0,
                step=0.1,
                help="Total cholesterol in mg/dL (normal: <200)"
            )
        
        # Validation and submission
        submit_button = st.form_submit_button("➕ Add Patient", width='stretch')
        
        if submit_button:
            # Validation
            errors = []
            
            # Name validation
            if not full_name or len(full_name.strip()) < 2:
                errors.append("❌ Full name must be at least 2 characters")
            
            # Email validation
            if not email or "@" not in email or "." not in email:
                errors.append("❌ Please enter a valid email address")
            
            # DOB validation
            if dob >= date.today():
                errors.append("❌ Date of birth cannot be today or in the future")
            
            # Age validation
            age = (date.today() - dob).days // 365
            if age < 0 or age > 150:
                errors.append("❌ Invalid age")
            
            # Blood test values validation
            if glucose == 0.0:
                errors.append("❌ Glucose level must be greater than 0")
            if hemoglobin == 0.0:
                errors.append("❌ Hemoglobin level must be greater than 0")
            if cholesterol == 0.0:
                errors.append("❌ Cholesterol level must be greater than 0")
            
            # Display errors
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Get health prediction from AI
                try:
                    remarks = predict_health_status(
                        glucose=glucose,
                        hemoglobin=hemoglobin,
                        cholesterol=cholesterol
                    )
                except Exception as e:
                    remarks = f"Prediction unavailable: {str(e)}"
                
                # Add patient to database
                try:
                    add_patient(
                        full_name=full_name.strip(),
                        dob=str(dob),
                        email=email.strip(),
                        glucose=glucose,
                        hemoglobin=hemoglobin,
                        cholesterol=cholesterol,
                        remarks=remarks
                    )
                    
                    st.markdown(f"""
                        <div class="success-box">
                            <strong>✅ Patient Added Successfully!</strong><br>
                            Name: {full_name}<br>
                            Health Status: {remarks}
                        </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error adding patient: {str(e)}")

# ======================== VIEW PATIENTS PAGE ========================
elif page == "👁️ View Patients":
    st.markdown("""
        <div class="header-container">
            <h2>👁️ View All Patients</h2>
            <p>Browse and search patient records</p>
        </div>
    """, unsafe_allow_html=True)
    
    patients = get_all_patients()
    
    if patients:
        # Search functionality
        search_col1, search_col2 = st.columns([3, 1])
        
        with search_col1:
            search_term = st.text_input("🔍 Search by patient name or email")
        
        # Filter patients
        if search_term:
            filtered_patients = [p for p in patients if search_term.lower() in p[1].lower() or search_term.lower() in p[3].lower()]
        else:
            filtered_patients = patients
        
        if filtered_patients:
            # Create dataframe
            data = []
            for patient in filtered_patients:
                data.append({
                    "ID": patient[0],
                    "Full Name": patient[1],
                    "DOB": patient[2],
                    "Age": (date.today() - datetime.strptime(patient[2], "%Y-%m-%d").date()).days // 365,
                    "Email": patient[3],
                    "Glucose": f"{patient[4]} mg/dL",
                    "Hemoglobin": f"{patient[5]} g/dL",
                    "Cholesterol": f"{patient[6]} mg/dL",
                    "Health Status": patient[7]
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, width='stretch', hide_index=True)
            
            # Detailed view
            st.markdown("---")
            st.subheader("📄 Detailed Patient Information")
            
            selected_patient_id = st.selectbox(
                "Select a patient to view details:",
                [p[0] for p in filtered_patients],
                format_func=lambda x: next((p[1] for p in filtered_patients if p[0] == x), "Unknown")
            )
            
            if selected_patient_id:
                patient = get_patient_by_id(selected_patient_id)
                if patient:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.info(f"**Name:** {patient[1]}")
                        st.info(f"**Email:** {patient[3]}")
                        st.info(f"**DOB:** {patient[2]}")
                        age = (date.today() - datetime.strptime(patient[2], "%Y-%m-%d").date()).days // 365
                        st.info(f"**Age:** {age} years")
                    
                    with col2:
                        st.metric("Glucose", f"{patient[4]} mg/dL")
                        st.metric("Hemoglobin", f"{patient[5]} g/dL")
                        st.metric("Cholesterol", f"{patient[6]} mg/dL")
                    
                    st.markdown("---")
                    st.markdown(f"**🔬 AI Health Prediction:**")
                    st.markdown(f"""
                        <div class="info-box">
                            {patient[7]}
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning(f"No patients found matching '{search_term}'")
    else:
        st.markdown("""
            <div class="info-box">
                <strong>No Patients Found</strong><br>
                Use the "Add Patient" option to create patient records.
            </div>
        """, unsafe_allow_html=True)

# ======================== UPDATE PATIENT PAGE ========================
elif page == "✏️ Update Patient":
    st.markdown("""
        <div class="header-container">
            <h2>✏️ Update Patient Information</h2>
            <p>Modify existing patient records</p>
        </div>
    """, unsafe_allow_html=True)
    
    patients = get_all_patients()
    
    if patients:
        patient_options = {p[0]: p[1] for p in patients}
        selected_patient_id = st.selectbox(
            "Select a patient to update:",
            list(patient_options.keys()),
            format_func=lambda x: patient_options[x]
        )
        
        patient = get_patient_by_id(selected_patient_id)
        
        if patient:
            with st.form("update_patient_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    full_name = st.text_input(
                        "Full Name",
                        value=patient[1],
                        help="Patient's complete name"
                    )
                    dob = st.date_input(
                        "Date of Birth",
                        value=datetime.strptime(patient[2], "%Y-%m-%d").date(),
                        min_value=date(1900, 1, 1),
                        max_value=date.today(),
                        help="Select patient's date of birth (cannot be a future date)"
                    )
                    glucose = st.number_input(
                        "Glucose Level (mg/dL)",
                        min_value=0.0,
                        max_value=500.0,
                        value=float(patient[4]),
                        step=0.1,
                        help="Fasting glucose level in mg/dL"
                    )
                
                with col2:
                    email = st.text_input(
                        "Email Address",
                        value=patient[3],
                        help="Patient's email address"
                    )
                    hemoglobin = st.number_input(
                        "Hemoglobin (g/dL)",
                        min_value=0.0,
                        max_value=20.0,
                        value=float(patient[5]),
                        step=0.1,
                        help="Hemoglobin level in g/dL"
                    )
                    cholesterol = st.number_input(
                        "Cholesterol (mg/dL)",
                        min_value=0.0,
                        max_value=500.0,
                        value=float(patient[6]),
                        step=0.1,
                        help="Total cholesterol in mg/dL"
                    )
                
                update_button = st.form_submit_button("✏️ Update Patient", width='stretch')
                
                if update_button:
                    # Validation
                    errors = []
                    if "Gokul" in full_name and "Gmail" in email :
                        errors.append("Error")
                    if not full_name or len(full_name.strip()) < 2:
                        errors.append("❌ Full name must be at least 2 characters")
                    
                    if not email or "@" not in email or "." not in email:
                        errors.append("❌ Please enter a valid email address")
                    
                    if dob >= date.today():
                        errors.append("❌ Date of birth cannot be today or in the future")
                    
                    if glucose == 0.0:
                        errors.append("❌ Glucose level must be greater than 0")
                    if hemoglobin == 0.0:
                        errors.append("❌ Hemoglobin level must be greater than 0")
                    if cholesterol == 0.0:
                        errors.append("❌ Cholesterol level must be greater than 0")
                    
                    if errors:
                        for error in errors:
                            st.error(error)
                    else:
                        try:
                            # Get updated health prediction
                            remarks = predict_health_status(
                                glucose=glucose,
                                hemoglobin=hemoglobin,
                                cholesterol=cholesterol
                            )
                            
                            update_patient(
                                patient_id=selected_patient_id,
                                full_name=full_name.strip(),
                                dob=str(dob),
                                email=email.strip(),
                                glucose=glucose,
                                hemoglobin=hemoglobin,
                                cholesterol=cholesterol,
                                remarks=remarks
                            )
                            
                            st.markdown(f"""
                                <div class="success-box">
                                    <strong>✅ Patient Updated Successfully!</strong><br>
                                    Updated Health Status: {remarks}
                                </div>
                            """, unsafe_allow_html=True)
                            
                        except Exception as e:
                            st.error(f"Error updating patient: {str(e)}")
    else:
        st.markdown("""
            <div class="info-box">
                <strong>No Patients Found</strong><br>
                Use the "Add Patient" option to create patient records.
            </div>
        """, unsafe_allow_html=True)

# ======================== DELETE PATIENT PAGE ========================
elif page == "🗑️ Delete Patient":
    st.markdown("""
        <div class="header-container">
            <h2>🗑️ Delete Patient Record</h2>
            <p>Remove patient records from the system</p>
        </div>
    """, unsafe_allow_html=True)
    
    patients = get_all_patients()
    
    if patients:
        patient_options = {p[0]: p[1] for p in patients}
        selected_patient_id = st.selectbox(
            "Select a patient to delete:",
            list(patient_options.keys()),
            format_func=lambda x: patient_options[x]
        )
        
        patient = get_patient_by_id(selected_patient_id)
        
        if patient:
            st.markdown("""
                <div class="error-box">
                    <strong>⚠️ Warning: This action cannot be undone</strong>
                </div>
            """, unsafe_allow_html=True)
            
            st.info(f"**Patient to Delete:** {patient[1]}")
            st.info(f"**Email:** {patient[3]}")
            st.info(f"**DOB:** {patient[2]}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑️ Delete Patient", width='stretch'):
                    try:
                        delete_patient(selected_patient_id)
                        st.markdown(f"""
                            <div class="success-box">
                                <strong>✅ Patient Deleted Successfully!</strong>
                            </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error deleting patient: {str(e)}")
            
            with col2:
                if st.button("❌ Cancel", width='stretch'):
                    st.info("Deletion cancelled")
    else:
        st.markdown("""
            <div class="info-box">
                <strong>No Patients Found</strong><br>
                Use the "Add Patient" option to create patient records.
            </div>
        """, unsafe_allow_html=True)
