"""
Configuration File
Customize your app here without modifying core code!
"""

# ============================================================================
# APP SETTINGS
# ============================================================================

APP_TITLE = "🏥 Health Prediction Application"
APP_ICON = "🏥"
APP_DESCRIPTION = "Manage patient records and predict health risks using AI"

# Page layout: "wide" or "centered"
PAGE_LAYOUT = "wide"

# ============================================================================
# DATABASE SETTINGS
# ============================================================================

# Database filename
DATABASE_FILE = "patients.db"

# Enable/disable automatic backups (future feature)
ENABLE_BACKUPS = True

# Backup location
BACKUP_LOCATION = "./backups"

# ============================================================================
# HEALTH METRICS - NORMAL RANGES
# ============================================================================

HEALTH_RANGES = {
    "glucose": {
        "normal": {"min": 70, "max": 100},
        "prediabetic": {"min": 100, "max": 125},
        "diabetic": {"min": 125, "max": 500},
        "hypoglycemia": {"min": 0, "max": 70},
        "unit": "mg/dL"
    },
    "hemoglobin": {
        "normal_male": {"min": 13.5, "max": 17.5},
        "normal_female": {"min": 12.0, "max": 15.5},
        "anemia": {"min": 0, "max": 12},
        "high": {"min": 17.5, "max": 20},
        "unit": "g/dL"
    },
    "cholesterol": {
        "desirable": {"min": 0, "max": 200},
        "borderline": {"min": 200, "max": 240},
        "high": {"min": 240, "max": 500},
        "unit": "mg/dL"
    }
}

# ============================================================================
# VALIDATION SETTINGS
# ============================================================================

# Minimum name length
MIN_NAME_LENGTH = 2

# Maximum name length
MAX_NAME_LENGTH = 100

# Maximum patient age allowed
MAX_PATIENT_AGE = 150

# Minimum patient age allowed
MIN_PATIENT_AGE = 0

# Email validation (regex pattern)
EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# ============================================================================
# UI/STYLING SETTINGS
# ============================================================================

# Color scheme - hex colors
COLORS = {
    "primary": "#667eea",
    "secondary": "#764ba2",
    "success": "#28a745",
    "error": "#dc3545",
    "warning": "#ffc107",
    "info": "#17a2b8"
}

# Success message styling
SUCCESS_MESSAGE_CLASS = "success-box"

# Error message styling
ERROR_MESSAGE_CLASS = "error-box"

# Info message styling
INFO_MESSAGE_CLASS = "info-box"

# ============================================================================
# PREDICTION SETTINGS
# ============================================================================

# AI Model to use: "rule-based", "huggingface", "openai", "local"
PREDICTION_MODEL = "rule-based"

# API Keys (NEVER put real keys here in production!)
# Use environment variables instead
API_KEYS = {
    "huggingface": None,  # Set via environment: HF_API_KEY
    "openai": None,       # Set via environment: OPENAI_API_KEY
    "rapidapi": None,     # Set via environment: RAPIDAPI_KEY
}

# Prediction timeout in seconds
PREDICTION_TIMEOUT = 10

# ============================================================================
# DISPLAY SETTINGS
# ============================================================================

# Number of records per page
RECORDS_PER_PAGE = 10

# Date format for display
DATE_FORMAT = "%Y-%m-%d"

# Time format for display
TIME_FORMAT = "%H:%M:%S"

# Table display options
TABLE_OPTIONS = {
    "use_container_width": True,
    "hide_index": True
}

# ============================================================================
# NAVIGATION SETTINGS
# ============================================================================

# Available pages/operations
PAGES = {
    "dashboard": {
        "icon": "📊",
        "label": "Dashboard",
        "description": "View overview and patient statistics"
    },
    "add_patient": {
        "icon": "➕",
        "label": "Add Patient",
        "description": "Create new patient record"
    },
    "view_patients": {
        "icon": "👁️",
        "label": "View Patients",
        "description": "Browse and search patient records"
    },
    "update_patient": {
        "icon": "✏️",
        "label": "Update Patient",
        "description": "Modify existing patient records"
    },
    "delete_patient": {
        "icon": "🗑️",
        "label": "Delete Patient",
        "description": "Remove patient records"
    }
}

# ============================================================================
# FEATURE FLAGS
# ============================================================================

# Enable/disable features
FEATURES = {
    "search": True,
    "export": True,
    "charts": False,  # Coming soon
    "notifications": False,  # Coming soon
    "multi_user": False,  # Coming soon
}

# ============================================================================
# ERROR MESSAGES
# ============================================================================

ERROR_MESSAGES = {
    "invalid_name": "❌ Full name must be at least {min} characters",
    "invalid_email": "❌ Please enter a valid email address",
    "future_dob": "❌ Date of birth cannot be today or in the future",
    "invalid_age": "❌ Invalid age",
    "zero_glucose": "❌ Glucose level must be greater than 0",
    "zero_hemoglobin": "❌ Hemoglobin level must be greater than 0",
    "zero_cholesterol": "❌ Cholesterol level must be greater than 0",
    "duplicate_email": "❌ Email already exists in the database",
    "db_error": "❌ Database error: {error}",
    "api_error": "❌ API error: {error}"
}

# ============================================================================
# SUCCESS MESSAGES
# ============================================================================

SUCCESS_MESSAGES = {
    "patient_added": "✅ Patient Added Successfully!",
    "patient_updated": "✅ Patient Updated Successfully!",
    "patient_deleted": "✅ Patient Deleted Successfully!",
}

# ============================================================================
# INFO MESSAGES
# ============================================================================

INFO_MESSAGES = {
    "no_patients": "No Patients Found. Use the 'Add Patient' option to create patient records.",
    "welcome": "Welcome to Health Prediction Application. Manage patient records and predict health risks.",
}

# ============================================================================
# RECOMMENDATIONS MAPPING
# ============================================================================

HEALTH_RECOMMENDATIONS = {
    "normal_glucose": "✅ Glucose levels are healthy - maintain current diet and exercise",
    "prediabetic": "⚠️ Reduce sugar intake and increase physical activity",
    "diabetic": "🚨 URGENT: Consult an endocrinologist immediately",
    "low_hemoglobin": "⚠️ Increase iron intake (spinach, red meat, legumes)",
    "normal_hemoglobin": "✅ Hemoglobin levels are healthy",
    "high_cholesterol": "⚠️ Reduce saturated fat intake",
    "normal_cholesterol": "✅ Cholesterol levels are optimal",
}

# ============================================================================
# EXPORT SETTINGS (Future)
# ============================================================================

EXPORT_FORMATS = {
    "csv": {
        "enabled": True,
        "extension": ".csv"
    },
    "pdf": {
        "enabled": False,  # Requires additional library
        "extension": ".pdf"
    },
    "excel": {
        "enabled": False,  # Requires additional library
        "extension": ".xlsx"
    }
}

# ============================================================================
# LOGGING SETTINGS
# ============================================================================

# Enable/disable logging
ENABLE_LOGGING = True

# Log file location
LOG_FILE = "app.log"

# Log level: "DEBUG", "INFO", "WARNING", "ERROR"
LOG_LEVEL = "INFO"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_config(key, default=None):
    """
    Get configuration value by key.
    Supports nested keys using dot notation.
    
    Example:
        get_config("COLORS.primary")  # Returns "#667eea"
        get_config("MAX_PATIENT_AGE")  # Returns 150
    
    Args:
        key (str): Configuration key
        default: Default value if key not found
    
    Returns:
        Any: Configuration value
    """
    
    # Handle nested keys (e.g., "COLORS.primary")
    if "." in key:
        keys = key.split(".")
        value = globals().get(keys[0])
        
        for k in keys[1:]:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    # Handle top-level keys
    return globals().get(key, default)

def set_config(key, value):
    """
    Set configuration value.
    
    Args:
        key (str): Configuration key
        value: New value
    """
    
    # Handle nested keys
    if "." in key:
        keys = key.split(".")
        obj = globals()[keys[0]]
        
        for k in keys[:-1]:
            obj = obj[k]
        
        obj[keys[-1]] = value
    else:
        globals()[key] = value

def get_health_status(metric_type, value):
    """
    Determine health status based on metric and value.
    
    Args:
        metric_type (str): "glucose", "hemoglobin", or "cholesterol"
        value (float): The metric value
    
    Returns:
        str: Health status (e.g., "normal", "high", "low")
    """
    
    if metric_type not in HEALTH_RANGES:
        return "unknown"
    
    ranges = HEALTH_RANGES[metric_type]
    
    for status, range_values in ranges.items():
        if isinstance(range_values, dict) and "min" in range_values:
            if range_values["min"] <= value <= range_values["max"]:
                return status
    
    return "unknown"

# ============================================================================
# VALIDATION HELPER
# ============================================================================

def get_validation_rules():
    """
    Get all validation rules as a dictionary.
    
    Returns:
        dict: Validation rules
    """
    
    return {
        "name": {
            "min_length": MIN_NAME_LENGTH,
            "max_length": MAX_NAME_LENGTH,
            "pattern": r"^[a-zA-Z\s'-]+$"  # Only letters, spaces, hyphens, apostrophes
        },
        "email": {
            "pattern": EMAIL_PATTERN,
            "max_length": 100
        },
        "age": {
            "min": MIN_PATIENT_AGE,
            "max": MAX_PATIENT_AGE
        },
        "glucose": {
            "min": 0,
            "max": 500
        },
        "hemoglobin": {
            "min": 0,
            "max": 20
        },
        "cholesterol": {
            "min": 0,
            "max": 500
        }
    }

# ============================================================================
# TEST DATA
# ============================================================================

TEST_PATIENTS = [
    {
        "name": "John Doe",
        "dob": "1985-03-15",
        "email": "john.doe@email.com",
        "glucose": 95,
        "hemoglobin": 14.5,
        "cholesterol": 180
    },
    {
        "name": "Jane Smith",
        "dob": "1990-07-22",
        "email": "jane.smith@email.com",
        "glucose": 110,
        "hemoglobin": 13.2,
        "cholesterol": 210
    },
    {
        "name": "Bob Johnson",
        "dob": "1975-11-08",
        "email": "bob.johnson@email.com",
        "glucose": 135,
        "hemoglobin": 10.5,
        "cholesterol": 250
    }
]

# ============================================================================
# EXAMPLE USAGE IN YOUR CODE
# ============================================================================

"""
# In your Python files, import and use config like this:

from config import (
    APP_TITLE,
    HEALTH_RANGES,
    ERROR_MESSAGES,
    get_config,
    get_health_status
)

# Use it in your code:
st.title(APP_TITLE)

if glucose_value > HEALTH_RANGES["glucose"]["diabetic"]["min"]:
    st.error(ERROR_MESSAGES["diabetic"])

status = get_health_status("glucose", 115)
print(f"Status: {status}")  # Output: "prediabetic"
"""
