import math

UPPERCASE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWERCASE_CHARS = "abcdefghijklmnopqrstuvwxyz"
DIGIT_CHARS = "0123456789"
SYMBOL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
AMBIGUOUS_CHARS = set("0Oo1Il|")

def filter_ambiguous(chars: str) -> str:
    return "".join(c for c in chars if c not in AMBIGUOUS_CHARS)

def evaluate_strength(
    password: str,
    include_upper: bool = True,
    include_lower: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
    exclude_ambiguous: bool = False
):
    if not password:
        return {
            "entropy": 0.0,
            "score": 0,
            "label": "None",
            "color": "#6c757d"
        }

    pool_size = 0
    if include_upper:
        pool_size += len(filter_ambiguous(UPPERCASE_CHARS) if exclude_ambiguous else UPPERCASE_CHARS)
    if include_lower:
        pool_size += len(filter_ambiguous(LOWERCASE_CHARS) if exclude_ambiguous else LOWERCASE_CHARS)
    if include_digits:
        pool_size += len(filter_ambiguous(DIGIT_CHARS) if exclude_ambiguous else DIGIT_CHARS)
    if include_symbols:
        pool_size += len(filter_ambiguous(SYMBOL_CHARS) if exclude_ambiguous else SYMBOL_CHARS)

    if pool_size <= 0:
        pool_size = 1

    length = len(password)
    entropy = length * math.log2(pool_size)
    score = min(100, int((entropy / 96.0) * 100))

    if entropy < 28:
        label = "Very Weak"
        color = "#ff453a"
    elif entropy < 46:
        label = "Weak"
        color = "#ff9f0a"
    elif entropy < 64:
        label = "Medium"
        color = "#ffd60a"
    elif entropy < 84:
        label = "Strong"
        color = "#30d158"
    else:
        label = "Very Strong"
        color = "#0a84ff"

    return {
        "entropy": round(entropy, 1),
        "score": score,
        "label": label,
        "color": color
    }
