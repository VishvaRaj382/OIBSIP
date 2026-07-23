import secrets
import string
from typing import Tuple, List
from strength import evaluate_strength, filter_ambiguous, AMBIGUOUS_CHARS, UPPERCASE_CHARS, LOWERCASE_CHARS, DIGIT_CHARS, SYMBOL_CHARS

MIN_PASSWORD_LENGTH = 8
MIN_CHARACTER_TYPES = 2

def generate_password(
    length: int = 16,
    include_upper: bool = True,
    include_lower: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
    exclude_ambiguous: bool = False,
    min_length: int = MIN_PASSWORD_LENGTH,
    min_types: int = MIN_CHARACTER_TYPES
) -> str:
    if length < min_length:
        raise ValueError(f"Password length must be at least {min_length} characters.")

    selected_pools: List[Tuple[str, str]] = []

    if include_upper:
        pool = filter_ambiguous(UPPERCASE_CHARS) if exclude_ambiguous else UPPERCASE_CHARS
        if pool:
            selected_pools.append(("upper", pool))

    if include_lower:
        pool = filter_ambiguous(LOWERCASE_CHARS) if exclude_ambiguous else LOWERCASE_CHARS
        if pool:
            selected_pools.append(("lower", pool))

    if include_digits:
        pool = filter_ambiguous(DIGIT_CHARS) if exclude_ambiguous else DIGIT_CHARS
        if pool:
            selected_pools.append(("digits", pool))

    if include_symbols:
        pool = filter_ambiguous(SYMBOL_CHARS) if exclude_ambiguous else SYMBOL_CHARS
        if pool:
            selected_pools.append(("symbols", pool))

    if len(selected_pools) < min_types:
        raise ValueError(f"At least {min_types} character type(s) must be selected.")

    password_chars = []
    for _, pool in selected_pools:
        password_chars.append(secrets.choice(pool))

    full_pool = "".join(pool for _, pool in selected_pools)

    if not full_pool:
        raise ValueError("Selected character pools are empty after applying filters.")

    remaining_length = length - len(password_chars)
    for _ in range(remaining_length):
        password_chars.append(secrets.choice(full_pool))

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)
