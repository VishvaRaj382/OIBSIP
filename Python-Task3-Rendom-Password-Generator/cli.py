import sys
from generator import generate_password, evaluate_strength, MIN_PASSWORD_LENGTH


def prompt_bool(question: str, default: bool = True) -> bool:
    default_str = "[Y/n]" if default else "[y/N]"
    while True:
        choice = input(f"{question} {default_str}: ").strip().lower()
        if not choice:
            return default
        if choice in ('y', 'yes'):
            return True
        if choice in ('n', 'no'):
            return False
        print("Invalid input. Please enter 'y' or 'n'.")


def prompt_length() -> int:
    while True:
        val = input(f"Password length (minimum {MIN_PASSWORD_LENGTH}): ").strip()
        if not val.isdigit():
            print("Please enter a valid integer.")
            continue
        length = int(val)
        if length < MIN_PASSWORD_LENGTH:
            print(f"Length must be at least {MIN_PASSWORD_LENGTH}.")
            continue
        return length


def main():
    print("=" * 48)
    print("         Random Password Generator")
    print("=" * 48)

    while True:
        print("\n--- Configuration ---")
        length = prompt_length()

        while True:
            print("\nCharacter Types (select at least 2):")
            inc_upper = prompt_bool("Include uppercase letters (A-Z)?", True)
            inc_lower = prompt_bool("Include lowercase letters (a-z)?", True)
            inc_digits = prompt_bool("Include numbers (0-9)?", True)
            inc_symbols = prompt_bool("Include symbols (!@#$...)?", True)

            if sum([inc_upper, inc_lower, inc_digits, inc_symbols]) < 2:
                print("\nError: You must select at least 2 character types.\n")
                continue
            break

        exc_ambiguous = prompt_bool("Exclude ambiguous characters (0, O, o, 1, l, I)?", False)

        try:
            password = generate_password(
                length=length,
                include_upper=inc_upper,
                include_lower=inc_lower,
                include_digits=inc_digits,
                include_symbols=inc_symbols,
                exclude_ambiguous=exc_ambiguous
            )

            strength = evaluate_strength(
                password,
                include_upper=inc_upper,
                include_lower=inc_lower,
                include_digits=inc_digits,
                include_symbols=inc_symbols,
                exclude_ambiguous=exc_ambiguous
            )

            print("\n" + "-" * 48)
            print(f"Generated Password: {password}")
            print(f"Strength Rating:    {strength['label']} ({strength['entropy']} bits entropy)")
            print("-" * 48)

        except ValueError as err:
            print(f"\nError: {err}")

        print()
        if not prompt_bool("Generate another password?", True):
            print("\nGoodbye.")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)
