# Random Password Generator

A Python tool for generating cryptographically secure passwords based on custom criteria. Supports both an Apple Dark Mode desktop GUI and a command-line interface (CLI).

## Features

- **Cryptographic Randomness**: Uses Python's standard `secrets` module instead of `random` for unpredictable generation.
- **Criteria-First Workflow**: Select your desired password options (length, uppercase, lowercase, numbers, symbols, ambiguous character exclusion) before generating.
- **Guaranteed Diversity**: Guarantees that at least one character from each selected set is included in the output.
- **Strength Evaluation**: Computes Shannon entropy in bits to display real-time strength feedback (*Weak*, *Medium*, *Strong*, *Very Strong*).
- **Clipboard Integration**: Automatically copies passwords to system clipboard using `pyperclip` (with native Tkinter fallback).
- **Session History**: Keeps the last 5 generated passwords in volatile memory during the current session (never saved to disk).

## Requirements

- Python 3.8+
- Tkinter (standard on Windows/Linux; on macOS: `brew install python-tk`)
- `pyperclip` (optional, for clipboard actions)

## Quick Start

1. Clone or download the repository and open the directory:
   ```bash
   cd Python-Task3-Rendom-Password-Generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the application:

   - **GUI App (Default)**:
     ```bash
     python3 main.py
     ```

   - **CLI App**:
     ```bash
     python3 main.py --cli
     ```

## Project Structure

- `main.py` - Primary launcher script. Defaults to GUI, or CLI via `--cli`.
- `gui.py` - Tkinter desktop interface styled with Apple Dark Mode HIG.
- `cli.py` - Command-line interface with interactive prompts.
- `generator.py` - Core generation logic, entropy calculation, and validation rules.
- `test_generator.py` - Unit test suite.

## Running Tests

To run the automated test suite:
```bash
python3 test_generator.py
```
