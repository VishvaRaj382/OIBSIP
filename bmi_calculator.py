"""
Professional BMI Calculator Module
Contains business logic for calculating BMI, detailed WHO classifications,
unit conversions (Metric & Imperial), body fat estimation, and input validation.
"""

from typing import Tuple, Optional, Dict


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    Calculate Body Mass Index (BMI).
    Formula: BMI = weight (kg) / (height (m))^2
    """
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    if weight_kg <= 0:
        raise ValueError("Weight must be greater than zero.")
    
    return weight_kg / (height_m ** 2)


def lbs_to_kg(lbs: float) -> float:
    """Convert pounds (lbs) to kilograms (kg)."""
    return lbs * 0.45359237


def kg_to_lbs(kg: float) -> float:
    """Convert kilograms (kg) to pounds (lbs)."""
    return kg / 0.45359237


def feet_inches_to_m(feet: float, inches: float = 0.0) -> float:
    """Convert feet and inches to meters."""
    total_inches = (feet * 12.0) + inches
    return total_inches * 0.0254


def m_to_feet_inches(meters: float) -> Tuple[int, float]:
    """Convert meters to (feet, inches)."""
    total_inches = meters / 0.0254
    feet = int(total_inches // 12)
    inches = total_inches % 12
    return (feet, round(inches, 1))


def classify_bmi(bmi: float) -> Tuple[str, str, str, str]:
    """
    Classify BMI value into WHO health categories with color, description, and advice.
    
    Returns:
        tuple: (category_name, hex_color, description, health_advice)
    """
    if bmi < 18.5:
        if bmi < 16.0:
            desc = "Severe Thinness (BMI < 16.0)"
        elif bmi < 17.0:
            desc = "Moderate Thinness (16.0 - 16.9)"
        else:
            desc = "Mild Thinness (17.0 - 18.4)"
        return (
            "Underweight",
            "#38BDF8",  # Sky Blue
            desc,
            "Consider consulting a healthcare provider or nutritionist to achieve a balanced, nutrient-dense diet."
        )
    elif 18.5 <= bmi < 25.0:
        return (
            "Normal Weight",
            "#4ADE80",  # Emerald Green
            "Optimal BMI range (18.5 – 24.9)",
            "Outstanding! Maintain your healthy lifestyle with regular exercise and balanced nutrition."
        )
    elif 25.0 <= bmi < 30.0:
        return (
            "Overweight",
            "#FACC15",  # Warm Amber Yellow
            "Pre-obesity range (25.0 – 29.9)",
            "Incorporate moderate physical activity into your daily routine and monitor diet portions."
        )
    elif 30.0 <= bmi < 35.0:
        return (
            "Obese (Class I)",
            "#FB923C",  # Vibrant Orange
            "Class I Obesity (30.0 – 34.9)",
            "Consult a medical professional to establish a safe, sustainable weight management plan."
        )
    elif 35.0 <= bmi < 40.0:
        return (
            "Obese (Class II)",
            "#F87171",  # Soft Coral Red
            "Class II Obesity (35.0 – 39.9)",
            "High health risk. Medical supervision is recommended to manage cardiovascular and metabolic health."
        )
    else:
        return (
            "Obese (Class III)",
            "#EF4444",  # Crimson Red
            "Class III Extreme Obesity (≥ 40.0)",
            "Very high health risk. Seek guidance from a healthcare specialist for dedicated medical support."
        )


def calculate_healthy_weight_range(height_m: float) -> Tuple[float, float, float, float]:
    """
    Calculate recommended healthy weight range for height_m in both KG and LBS.
    
    Returns:
        (min_kg, max_kg, min_lbs, max_lbs)
    """
    if height_m <= 0:
        return (0.0, 0.0, 0.0, 0.0)
    min_kg = 18.5 * (height_m ** 2)
    max_kg = 24.9 * (height_m ** 2)
    return (
        round(min_kg, 1),
        round(max_kg, 1),
        round(kg_to_lbs(min_kg), 1),
        round(kg_to_lbs(max_kg), 1)
    )


def estimate_body_fat_percentage(bmi: float, age: int = 30, gender: str = "male") -> Optional[float]:
    """
    Estimate adult body fat percentage using Deurenberg formula:
    Body Fat % = (1.20 × BMI) + (0.23 × Age) - (10.8 × gender_val) - 5.4
    where gender_val = 1 for male, 0 for female.
    """
    if bmi <= 0 or age <= 0:
        return None
    g_val = 1 if gender.lower() in ["male", "m"] else 0
    fat_pct = (1.20 * bmi) + (0.23 * age) - (10.8 * g_val) - 5.4
    return round(max(3.0, min(60.0, fat_pct)), 1)


def parse_and_validate_inputs(weight_input: str, height_input: str) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    """
    Validates metric input for weight and height.
    
    Accepts:
    - Weight in kilograms (e.g. 70, 68.5)
    - Height in meters (e.g. 1.75) or centimeters (e.g. 175)
    
    Returns:
        (weight_kg, height_m, error_message)
    """
    if not weight_input or not weight_input.strip():
        return (None, None, "Weight input cannot be empty.")
    if not height_input or not height_input.strip():
        return (None, None, "Height input cannot be empty.")
    
    try:
        weight_kg = float(weight_input.strip())
    except ValueError:
        return (None, None, "Invalid weight: Please enter a numerical value (e.g., 70 or 68.5).")
    
    try:
        height_val = float(height_input.strip())
    except ValueError:
        return (None, None, "Invalid height: Please enter a numerical value (e.g., 1.75 or 175).")
    
    if weight_kg <= 0:
        return (None, None, "Weight must be a positive number greater than 0.")
        
    if height_val <= 0:
        return (None, None, "Height must be a positive number greater than 0.")
    
    # Auto-convert height if entered in cm (e.g. 175 -> 1.75m)
    if height_val > 10.0:
        height_m = height_val / 100.0
    else:
        height_m = height_val
        
    return (weight_kg, height_m, None)


def parse_imperial_inputs(weight_lbs_str: str, feet_str: str, inches_str: str = "0") -> Tuple[Optional[float], Optional[float], Optional[str]]:
    """
    Validates imperial inputs for weight (lbs) and height (feet, inches).
    
    Returns:
        (weight_kg, height_m, error_message)
    """
    if not weight_lbs_str or not weight_lbs_str.strip():
        return (None, None, "Weight (lbs) cannot be empty.")
    if not feet_str or not feet_str.strip():
        return (None, None, "Height (feet) cannot be empty.")
        
    try:
        lbs = float(weight_lbs_str.strip())
    except ValueError:
        return (None, None, "Invalid weight: Please enter a valid number in lbs.")
        
    try:
        feet = float(feet_str.strip())
    except ValueError:
        return (None, None, "Invalid feet: Please enter a valid number for feet.")
        
    inches = 0.0
    if inches_str and inches_str.strip():
        try:
            inches = float(inches_str.strip())
        except ValueError:
            return (None, None, "Invalid inches: Please enter a valid number for inches.")
            
    if lbs <= 0:
        return (None, None, "Weight must be greater than 0 lbs.")
    if feet < 0 or inches < 0:
        return (None, None, "Height values cannot be negative.")
    if feet == 0 and inches == 0:
        return (None, None, "Height must be greater than 0.")
        
    weight_kg = lbs_to_kg(lbs)
    height_m = feet_inches_to_m(feet, inches)
    
    return (weight_kg, height_m, None)
