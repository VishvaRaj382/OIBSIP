import sys

def main():
    if "--cli" in sys.argv or "-c" in sys.argv:
        from cli import main as run_cli
        run_cli()
    else:
        try:
            from gui import launch_gui
            launch_gui()
        except Exception as err:
            print(f"Could not launch GUI ({err}). Falling back to CLI mode.\n")
            from cli import main as run_cli
            run_cli()

if __name__ == "__main__":
    main()
