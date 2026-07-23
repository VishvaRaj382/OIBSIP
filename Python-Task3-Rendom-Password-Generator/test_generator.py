import unittest
from generator import (
    generate_password,
    evaluate_strength,
    AMBIGUOUS_CHARS,
    UPPERCASE_CHARS,
    LOWERCASE_CHARS,
    DIGIT_CHARS,
    SYMBOL_CHARS
)

class TestPasswordGenerator(unittest.TestCase):

    def test_minimum_length_enforced(self):
        with self.assertRaises(ValueError):
            generate_password(length=7)

    def test_minimum_character_types_enforced(self):
        with self.assertRaises(ValueError):
            generate_password(
                length=12,
                include_upper=True,
                include_lower=False,
                include_digits=False,
                include_symbols=False
            )

    def test_exact_password_length(self):
        for len_req in [8, 12, 16, 32, 64]:
            pwd = generate_password(length=len_req)
            self.assertEqual(len(pwd), len_req)

    def test_guaranteed_type_inclusion(self):
        for _ in range(20):
            pwd = generate_password(
                length=10,
                include_upper=True,
                include_lower=True,
                include_digits=True,
                include_symbols=True
            )
            has_upper = any(c in UPPERCASE_CHARS for c in pwd)
            has_lower = any(c in LOWERCASE_CHARS for c in pwd)
            has_digits = any(c in DIGIT_CHARS for c in pwd)
            has_symbols = any(c in SYMBOL_CHARS for c in pwd)

            self.assertTrue(has_upper, f"Missing uppercase in {pwd}")
            self.assertTrue(has_lower, f"Missing lowercase in {pwd}")
            self.assertTrue(has_digits, f"Missing digits in {pwd}")
            self.assertTrue(has_symbols, f"Missing symbols in {pwd}")

    def test_ambiguous_character_exclusion(self):
        for _ in range(30):
            pwd = generate_password(
                length=20,
                include_upper=True,
                include_lower=True,
                include_digits=True,
                include_symbols=True,
                exclude_ambiguous=True
            )
            for char in pwd:
                self.assertNotIn(
                    char,
                    AMBIGUOUS_CHARS,
                    f"Ambiguous character '{char}' found in {pwd}"
                )

    def test_evaluate_strength(self):
        res_weak = evaluate_strength("abcd1234", include_upper=False, include_symbols=False)
        self.assertIn(res_weak["label"], ["Very Weak", "Weak", "Medium"])

        res_strong = evaluate_strength(
            "X9#pL2$mQ8!vW1&k",
            include_upper=True,
            include_lower=True,
            include_digits=True,
            include_symbols=True
        )
        self.assertIn(res_strong["label"], ["Strong", "Very Strong"])
        self.assertGreater(res_strong["entropy"], 60.0)

if __name__ == "__main__":
    unittest.main()
