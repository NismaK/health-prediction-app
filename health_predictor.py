"""
Health Predictor Module - AI/ML Integration
This module uses health metrics to predict possible health conditions and risks.
It calls the free Hugging Face Inference API for a real AI-generated assessment,
and automatically falls back to local rule-based logic if the API is unavailable.
"""

import os
import requests



HF_MODEL_URL = "https://router.huggingface.co/v1/chat/completions"


HF_MODEL_CANDIDATES = [
    "deepseek-ai/DeepSeek-V3-0324:fireworks-ai",
    "Qwen/QwQ-32B:fireworks-ai",
    "meta-llama/Llama-3.1-8B-Instruct:novita",
]


def get_hf_api_key():
    """
    Retrieve the Hugging Face API key from Streamlit secrets or
    environment variables, in that order. Never raises an exception --
    always returns either the key string or None.

    Returns:
        str or None: The API key if found, otherwise None
    """

    try:
        import streamlit as st
        try:
            value = st.secrets.get("HF_API_KEY", None)
            if value:
                return value
        except Exception:
            pass
    except Exception:
        pass

    # Fall back to environment variable
    return os.environ.get("HF_API_KEY")


def predict_health_status(glucose, hemoglobin, cholesterol):
    """
    Predict health status based on blood test results.

    Tries the Hugging Face Inference API first (real external AI/ML API).
    If that is unavailable for any reason, falls back to local rule-based
    logic and tells the user why, instead of failing silently.

    Args:
        glucose (float): Glucose level in mg/dL
        hemoglobin (float): Hemoglobin level in g/dL
        cholesterol (float): Cholesterol level in mg/dL

    Returns:
        str: Health prediction and recommendations
    """
    fallback_reason = "unknown error"

    try:
        api_result, fallback_reason = predict_with_api(glucose, hemoglobin, cholesterol)
        if api_result:
            return api_result
    except Exception as e:
        fallback_reason = f"unexpected error: {str(e)}"

    fallback = predict_with_rules(glucose, hemoglobin, cholesterol)
    return (
        f"*Note: AI service unavailable ({fallback_reason}). "
        f"Showing rule-based assessment instead.*\n\n"
        f"{fallback}"
    )


def predict_with_api(glucose, hemoglobin, cholesterol):
    """
    Call the Hugging Face Inference API (router-based, OpenAI-compatible
    chat completions endpoint) to generate a health assessment.

    Tries each model in HF_MODEL_CANDIDATES in order. If a model/provider
    combo is rejected (400 "not supported by provider", retired, etc.),
    it automatically moves on to the next candidate instead of failing.

    Returns:
        tuple: (result_text_or_None, reason_string)
    """
    api_key = get_hf_api_key()

    if not api_key:
        reason = "no HF_API_KEY found in .streamlit/secrets.toml or environment variables"
        return None, reason

    prompt = (
        "You are a clinical assistant writing a structured health risk note. "
        "Use ONLY the values provided. Do NOT invent or misquote reference ranges. "
        "Do NOT give a generic cardiovascular warning if cholesterol is below 200 mg/dL.\n\n"
        "Standard reference ranges you MUST follow strictly:\n"
        "- Glucose: Normal = 70-99 mg/dL | Prediabetic = 100-125 mg/dL | Diabetic = 126+ mg/dL\n"
        "- Haemoglobin: Normal = 12.0-17.5 g/dL | Low (anaemia) = below 12.0 g/dL | High = above 17.5 g/dL\n"
        "- Cholesterol: Desirable = below 200 mg/dL | Borderline High = 200-239 mg/dL | High = 240+ mg/dL\n\n"
        f"Patient values:\n"
        f"- Glucose: {glucose} mg/dL\n"
        f"- Haemoglobin: {hemoglobin} g/dL\n"
        f"- Cholesterol: {cholesterol} mg/dL\n\n"
        "Instructions:\n"
        "1. Compare each value against the reference ranges above.\n"
        "2. Identify which values are abnormal and which are normal.\n"
        "3. If a value is within the normal range, explicitly state it is normal — do not flag it as a risk.\n"
        "4. Base your risk level only on values that are actually outside the normal range.\n\n"
        "Write your response in exactly this structure:\n\n"
        "**Primary Risk Assessment:** One sentence naming the specific risk(s) based only on "
        "the abnormal values, and whether the risk is mild, moderate, or significant. "
        "If all values are normal, state the patient appears healthy.\n\n"
        "**Clinical Rationale:** Two to three sentences citing the exact patient values and "
        "comparing them to the reference ranges above. State clearly which values are normal "
        "and which are not.\n\n"
        "**Recommended Action:** One specific, practical next step appropriate to the actual findings.\n\n"
        "Do not use emojis. Do not use exclamation marks. Be precise and clinical."
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    last_reason = "no models attempted"

    for model_name in HF_MODEL_CANDIDATES:
        try:
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 350,
                "temperature": 0.1
            }

            response = requests.post(HF_MODEL_URL, headers=headers, json=payload, timeout=30)

            if response.status_code != 200:
                last_reason = f"model '{model_name}' returned status {response.status_code}: {response.text[:120]}"
                continue  # try the next candidate model

            result = response.json()

            generated_text = None
            try:
                generated_text = result["choices"][0]["message"]["content"]
            except (KeyError, IndexError, TypeError):
                generated_text = None

            if not generated_text:
                last_reason = f"model '{model_name}' returned an unexpected response format"
                continue

            success_text = (
                f"### AI-Generated Health Assessment\n"
                f"*Model: {model_name}*\n\n"
                f"---\n\n"
                f"{generated_text.strip()}"
            )
            return success_text, ""

        except requests.exceptions.ConnectionError as e:
            last_reason = f"could not connect to Hugging Face (network/DNS issue): {str(e)[:120]}"
            # A connection-level failure will likely affect every model too,
            # so stop trying further candidates and report immediately.
            return None, last_reason
        except requests.exceptions.Timeout:
            last_reason = f"model '{model_name}' timed out after 30 seconds"
            continue
        except Exception as e:
            last_reason = f"error calling model '{model_name}': {str(e)[:120]}"
            continue

    # If we reach here, every candidate model failed
    return None, last_reason


def predict_with_rules(glucose, hemoglobin, cholesterol):
    """
    Rule-based health prediction using standard medical reference ranges.

    Reference Ranges:
        Glucose: 70-100 (normal), 100-125 (prediabetic), >125 (diabetic)
        Hemoglobin: 12.0-17.5 (normal), <12 (anemic), >17.5 (elevated)
        Cholesterol: <200 (desirable), 200-239 (borderline), >=240 (high)

    Args:
        glucose (float): Glucose level in mg/dL
        hemoglobin (float): Hemoglobin level in g/dL
        cholesterol (float): Cholesterol level in mg/dL

    Returns:
        str: Formatted health prediction report
    """

    risk_level = "LOW"
    risk_factors = []
    recommendations = []

    # ===== GLUCOSE ANALYSIS =====
    if glucose < 70:
        risk_level = "MEDIUM"
        risk_factors.append("Hypoglycemia (low blood sugar)")
        recommendations.append("Consult a doctor about low blood sugar levels.")
    elif glucose <= 100:
        risk_factors.append("Glucose within normal range")
        recommendations.append("Maintain current diet and exercise routine.")
    elif glucose <= 125:
        risk_level = "MEDIUM"
        risk_factors.append("Prediabetic range (elevated glucose)")
        recommendations.append("Reduce sugar intake and increase physical activity.")
        recommendations.append("Schedule regular glucose monitoring.")
    else:
        risk_level = "HIGH"
        risk_factors.append("Diabetic range (high glucose)")
        recommendations.append("Consult an endocrinologist as soon as possible.")
        recommendations.append("Consider a structured diabetes management plan.")

    # ===== HEMOGLOBIN ANALYSIS =====
    if hemoglobin < 12.0:
        if risk_level == "LOW":
            risk_level = "MEDIUM"
        risk_factors.append("Anemia (low hemoglobin)")
        recommendations.append("Increase iron intake (spinach, red meat, legumes).")
        recommendations.append("Consult a doctor regarding anemia treatment.")
    elif hemoglobin <= 17.5:
        risk_factors.append("Hemoglobin within normal range")
        recommendations.append("No action needed for hemoglobin levels.")
    else:
        risk_factors.append("Elevated hemoglobin (possible polycythemia)")
        recommendations.append("Stay hydrated and consult a doctor for evaluation.")

    # ===== CHOLESTEROL ANALYSIS =====
    if cholesterol < 200:
        risk_factors.append("Cholesterol within desirable range")
        recommendations.append("No action needed for cholesterol levels.")
    elif cholesterol < 240:
        if risk_level == "LOW":
            risk_level = "MEDIUM"
        risk_factors.append("Borderline high cholesterol")
        recommendations.append("Reduce saturated fat intake; increase fiber and exercise.")
    else:
        risk_level = "HIGH"
        risk_factors.append("High cholesterol (cardiovascular risk)")
        recommendations.append("Begin a cholesterol-lowering diet plan.")
        recommendations.append("Consult a cardiologist regarding medication options.")

    # ===== BUILD REPORT =====
    findings_text = "\n".join(f"- {factor}" for factor in risk_factors)
    recommendations_text = "\n".join(f"- {rec}" for rec in recommendations)

    report = (
        "### Health Risk Assessment (Rule-Based)\n\n"
        f"**Overall Risk Level:** {risk_level}\n\n"
        "---\n\n"
        "**Key Findings**\n\n"
        f"{findings_text}\n\n"
        "**Recommendations**\n\n"
        f"{recommendations_text}\n\n"
        "*This is a rule-based assessment generated from blood test values against "
        "standard reference ranges. It is not a substitute for professional medical advice. "
        "Please consult a healthcare provider for an accurate diagnosis.*"
    )

    return report


def calculate_health_score(glucose, hemoglobin, cholesterol):
    """
    Calculate an overall health score from 0-100.
    Higher score = better health.

    Args:
        glucose (float): Glucose level in mg/dL
        hemoglobin (float): Hemoglobin level in g/dL
        cholesterol (float): Cholesterol level in mg/dL

    Returns:
        int: Health score from 0-100
    """
    score = 100

    if 70 <= glucose <= 100:
        pass
    elif glucose < 70:
        score -= 20
    elif glucose <= 125:
        score -= 15
    else:
        score -= 30

    if 12 <= hemoglobin <= 17.5:
        pass
    elif hemoglobin < 12:
        score -= 20
    else:
        score -= 10

    if cholesterol < 200:
        pass
    elif cholesterol < 240:
        score -= 15
    else:
        score -= 25

    return max(0, score)


def get_health_metrics_info():
    """
    Provide information about health metrics and their normal ranges.

    Returns:
        dict: Information about each health metric
    """
    return {
        "Glucose": {
            "Normal": "70-100 mg/dL (fasting)",
            "Prediabetic": "100-125 mg/dL",
            "Diabetic": ">125 mg/dL",
            "Health Condition": "Regulates blood sugar and energy",
            "Recommendations": "Maintain balanced diet, regular exercise"
        },
        "Hemoglobin": {
            "Normal_Male": "13.5-17.5 g/dL",
            "Normal_Female": "12.0-15.5 g/dL",
            "Low": "<12 g/dL (Anemia)",
            "Health Condition": "Carries oxygen in blood",
            "Recommendations": "Increase iron intake, eat red meat, leafy greens"
        },
        "Cholesterol": {
            "Desirable": "<200 mg/dL",
            "Borderline": "200-239 mg/dL",
            "High": ">240 mg/dL",
            "Health Condition": "Fat in blood affecting heart health",
            "Recommendations": "Reduce saturated fats, increase fiber, exercise"
        }
    }
