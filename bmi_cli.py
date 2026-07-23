"""
Professional BMI Calculator — Command-Line Interface (CLI)
Executive terminal tool with Metric/Imperial unit support, input validation,
WHO sub-classifications, summary statistics, and CSV export.
"""

import sys
from bmi_calculator import (
    parse_and_validate_inputs, parse_imperial_inputs, calculate_bmi,
    classify_bmi, calculate_healthy_weight_range, estimate_body_fat_percentage
)
from database import DatabaseManager, DatabaseError


def print_banner():
    print("=" * 65)
    print("      💪 EXECUTIVE BMI CALCULATOR & HEALTH ANALYTICS (CLI) 💪")
    print("=" * 65)


def print_categories_reference():
    print("\n📊 WHO World Health Organization BMI Reference:")
    print("  • Underweight : < 18.5  (Severe < 16.0 | Moderate 16.0–16.9 | Mild 17.0–18.4)")
    print("  • Normal      : 18.5 – 24.9 (Optimal Range)")
    print("  • Overweight  : 25.0 – 29.9 (Pre-obesity)")
    print("  • Obese       : ≥ 30.0 (Class I: 30–34.9 | Class II: 35–39.9 | Class III: ≥ 40)")
    print("-" * 65)


def run_cli():
    print_banner()
    print_categories_reference()

    # Database Initialization
    try:
        db = DatabaseManager()
    except DatabaseError as e:
        print(f"⚠️ Database Warning: {e}")
        print("Running in memory mode (results won't be saved).\n")
        db = None

    user_name = "Default User"
    user_id = None

    if db:
        user_input_name = input("👤 Enter profile name (or press Enter for 'Default User'): ").strip()
        if user_input_name:
            user_name = user_input_name
        try:
            user_info = db.get_or_create_user(user_name)
            user_id = user_info["id"]
            print(f"Welcome back, {user_info['name']}! (Profile ID: {user_id})\n")
        except DatabaseError as e:
            print(f"⚠️ Could not load user: {e}\n")

    while True:
        print("\n--- NEW BMI MEASUREMENT ENTRY ---")
        print(" Choose Unit System:")
        print("  [1] Metric (Kilograms & Meters / Centimeters)")
        print("  [2] Imperial (Pounds & Feet / Inches)")
        unit_choice = input(" Select option (1-2, default 1): ").strip()

        weight_kg = None
        height_m = None

        if unit_choice == "2":
            # Imperial Entry
            while True:
                lbs = input(" Enter weight in lbs (e.g. 154): ").strip()
                feet = input(" Enter height in feet (e.g. 5): ").strip()
                inches = input(" Enter height in inches (e.g. 9): ").strip()
                w_kg, h_m, err = parse_imperial_inputs(lbs, feet, inches)
                if err:
                    print(f"❌ {err}")
                else:
                    weight_kg, height_m = w_kg, h_m
                    break
        else:
            # Metric Entry
            while True:
                w_str = input(" Enter weight in kg (e.g. 70 or 68.5): ").strip()
                h_str = input(" Enter height in meters or cm (e.g. 1.75 or 175): ").strip()
                w_kg, h_m, err = parse_and_validate_inputs(w_str, h_str)
                if err:
                    print(f"❌ {err}")
                else:
                    weight_kg, height_m = w_kg, h_m
                    break

        # Calculate Results
        bmi = calculate_bmi(weight_kg, height_m)
        category, color_code, desc, advice = classify_bmi(bmi)
        min_k, max_k, min_l, max_l = calculate_healthy_weight_range(height_m)

        # Print Executive Summary
        print("\n" + "=" * 65)
        print("                  🎯 CLINICAL BMI RESULT SUMMARY")
        print("=" * 65)
        print(f"  • Weight                : {weight_kg:.2f} kg ({weight_kg * 2.20462:.1f} lbs)")
        print(f"  • Height                : {height_m:.2f} m ({height_m * 100:.1f} cm)")
        print(f"  • Calculated BMI        : {bmi:.2f}")
        print(f"  • WHO Classification    : {category.upper()}")
        print(f"  • Category Sub-Details  : {desc}")
        print(f"  • Healthy Target Weight : {min_k} kg – {max_k} kg ({min_l} lbs – {max_l} lbs)")
        print(f"  • Clinical Advice       : {advice}")
        print("=" * 65)

        # Database Storage
        if db and user_id:
            try:
                rec_id = db.add_bmi_record(user_id, weight_kg, height_m, bmi, category)
                print(f"✅ Record #{rec_id} saved to database successfully!")
            except DatabaseError as e:
                print(f"⚠️ Storage Error: {e}")

        # Menu Options
        print("\nOptions:")
        print(" [1] Calculate another BMI")
        print(" [2] View historical logs & statistics for " + user_name)
        print(" [3] Export history to CSV file")
        print(" [4] Switch user profile")
        print(" [5] Exit")

        choice = input("Select an option (1-5): ").strip()
        if choice == "2":
            if db and user_id:
                try:
                    records = db.get_user_history(user_id)
                    stats = db.get_user_stats(user_id)
                    if not records:
                        print(f"\n📜 No historical records found for {user_name}.")
                    else:
                        print(f"\n📊 SUMMARY STATS FOR {user_name.upper()}:")
                        print(f"  Total Logs: {stats['total_records']} | Latest BMI: {stats['latest_bmi']} | Weight Delta: {stats['weight_change']} kg | Avg BMI: {stats['avg_bmi']}")
                        print("\n📜 BMI HISTORY:")
                        print("-" * 65)
                        print(f"{'ID':<5} | {'Date & Time':<20} | {'Weight':<8} | {'Height':<8} | {'BMI':<6} | {'Category'}")
                        print("-" * 65)
                        for r in records:
                            print(f"{r['id']:<5} | {r['timestamp']:<20} | {r['weight_kg']:<8.1f} | {r['height_m']:<8.2f} | {r['bmi_value']:<6.2f} | {r['category']}")
                        print("-" * 65)
                except DatabaseError as e:
                    print(f"⚠️ History Error: {e}")

            cont = input("\nPress Enter to return or 'q' to quit: ").strip().lower()
            if cont == 'q':
                break
        elif choice == "3":
            if db and user_id:
                csv_path = f"{user_name.lower().replace(' ', '_')}_bmi_history.csv"
                try:
                    db.export_user_history_to_csv(user_id, csv_path)
                    print(f"✅ Exported CSV to: {csv_path}")
                except Exception as e:
                    print(f"❌ Export Failed: {e}")
        elif choice == "4":
            new_name = input("Enter new user profile name: ").strip()
            if new_name and db:
                try:
                    user_info = db.get_or_create_user(new_name)
                    user_name = user_info["name"]
                    user_id = user_info["id"]
                    print(f"Switched profile to '{user_name}'.")
                except DatabaseError as e:
                    print(f"⚠️ Failed to switch profile: {e}")
        elif choice == "5":
            print("\nThank you for using the BMI Calculator & Health Analytics Suite. 👋")
            break


if __name__ == "__main__":
    run_cli()
