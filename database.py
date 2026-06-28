"""
Database Module - SQLite Database Operations
This module handles all database operations for storing and managing patient records.
"""

import sqlite3
import os
from datetime import datetime

# Database file path
DB_FILE = "patients.db"

def get_connection():
    """
    Create and return a database connection.
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    """
    Initialize the database and create tables if they don't exist.
    This function is called when the app starts.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            glucose REAL NOT NULL,
            hemoglobin REAL NOT NULL,
            cholesterol REAL NOT NULL,
            remarks TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def add_patient(full_name, dob, email, glucose, hemoglobin, cholesterol, remarks):
    """
    Add a new patient record to the database.
    
    Args:
        full_name (str): Patient's full name
        dob (str): Date of birth in YYYY-MM-DD format
        email (str): Patient's email address
        glucose (float): Glucose level in mg/dL
        hemoglobin (float): Hemoglobin level in g/dL
        cholesterol (float): Cholesterol level in mg/dL
        remarks (str): Health prediction remarks from AI
    
    Returns:
        int: ID of the newly added patient
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO patients 
            (full_name, date_of_birth, email, glucose, hemoglobin, cholesterol, remarks, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (full_name, dob, email, glucose, hemoglobin, cholesterol, remarks, datetime.now()))
        
        conn.commit()
        patient_id = cursor.lastrowid
        conn.close()
        
        return patient_id
    except sqlite3.IntegrityError:
        raise ValueError("Email already exists in the database")
    except Exception as e:
        raise Exception(f"Error adding patient: {str(e)}")

def get_all_patients():
    """
    Retrieve all patient records from the database.
    
    Returns:
        list: List of tuples containing patient data
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, full_name, date_of_birth, email, glucose, 
                   hemoglobin, cholesterol, remarks 
            FROM patients 
            ORDER BY created_at DESC
        ''')
        
        patients = cursor.fetchall()
        conn.close()
        
        return patients
    except Exception as e:
        raise Exception(f"Error retrieving patients: {str(e)}")

def get_patient_by_id(patient_id):
    """
    Retrieve a specific patient record by ID.
    
    Args:
        patient_id (int): The ID of the patient
    
    Returns:
        tuple: Patient data if found, None otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, full_name, date_of_birth, email, glucose, 
                   hemoglobin, cholesterol, remarks 
            FROM patients 
            WHERE id = ?
        ''', (patient_id,))
        
        patient = cursor.fetchone()
        conn.close()
        
        return patient
    except Exception as e:
        raise Exception(f"Error retrieving patient: {str(e)}")

def update_patient(patient_id, full_name, dob, email, glucose, hemoglobin, cholesterol, remarks):
    """
    Update an existing patient record.
    
    Args:
        patient_id (int): The ID of the patient to update
        full_name (str): Updated patient's full name
        dob (str): Updated date of birth in YYYY-MM-DD format
        email (str): Updated email address
        glucose (float): Updated glucose level
        hemoglobin (float): Updated hemoglobin level
        cholesterol (float): Updated cholesterol level
        remarks (str): Updated health prediction remarks
    
    Returns:
        bool: True if update was successful
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE patients 
            SET full_name = ?, date_of_birth = ?, email = ?, 
                glucose = ?, hemoglobin = ?, cholesterol = ?, 
                remarks = ?, updated_at = ?
            WHERE id = ?
        ''', (full_name, dob, email, glucose, hemoglobin, cholesterol, 
              remarks, datetime.now(), patient_id))
        
        conn.commit()
        conn.close()
        
        return True
    except sqlite3.IntegrityError:
        raise ValueError("Email already exists in the database")
    except Exception as e:
        raise Exception(f"Error updating patient: {str(e)}")

def delete_patient(patient_id):
    """
    Delete a patient record from the database.
    
    Args:
        patient_id (int): The ID of the patient to delete
    
    Returns:
        bool: True if deletion was successful
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
        
        conn.commit()
        conn.close()
        
        return True
    except Exception as e:
        raise Exception(f"Error deleting patient: {str(e)}")

def search_patients(search_term):
    """
    Search patients by name or email.
    
    Args:
        search_term (str): The term to search for
    
    Returns:
        list: List of matching patient records
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, full_name, date_of_birth, email, glucose, 
                   hemoglobin, cholesterol, remarks 
            FROM patients 
            WHERE full_name LIKE ? OR email LIKE ?
            ORDER BY full_name
        ''', (f'%{search_term}%', f'%{search_term}%'))
        
        patients = cursor.fetchall()
        conn.close()
        
        return patients
    except Exception as e:
        raise Exception(f"Error searching patients: {str(e)}")
