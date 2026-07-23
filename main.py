"""
BMI Calculator — Application Entry Point
Launches the PyQt6 GUI application by default, or the CLI mode when run with '--cli'.
"""

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Body Mass Index (BMI) Calculator & Health Tracker")
    parser.add_argument("--cli", action="store_true", help="Launch in Beginner Command-Line Interface (CLI) mode")
    args = parser.parse_args()

    if args.cli:
        from bmi_cli import run_cli
        run_cli()
    else:
        try:
            from gui import launch_gui
            launch_gui()
        except Exception as e:
            print(f"⚠️ Failed to launch GUI: {e}")
            print("Falling back to CLI mode...")
            from bmi_cli import run_cli
            run_cli()


if __name__ == "__main__":
    main()
