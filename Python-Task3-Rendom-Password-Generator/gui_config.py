import tkinter as tk
from tkinter import ttk
from theme import (
    BG_BASE, BG_CARD, BG_PILL, BG_HOVER, BORDER_COLOR,
    TEXT_PRIMARY, TEXT_SECONDARY, COLOR_RED,
    FONT_HEADING, FONT_SUB
)

class ConfigPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_BASE)
        self.app = app

        header = tk.Frame(self, bg=BG_BASE, pady=20, padx=24)
        header.pack(fill="x")

        tk.Label(header, text="PassShield", font=FONT_HEADING, bg=BG_BASE, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Label(header, text="Select your password requirements", font=FONT_SUB, bg=BG_BASE, fg=TEXT_SECONDARY).pack(anchor="w", pady=(4, 0))

        presets_bar = tk.Frame(self, bg=BG_BASE, padx=24, pady=4)
        presets_bar.pack(fill="x")

        tk.Label(presets_bar, text="Presets:", font=("SF Pro Text", 8, "bold"), bg=BG_BASE, fg=TEXT_SECONDARY).pack(side="left", padx=(0, 8))

        preset_options = [
            ("Standard (16)", 16, True, True, True, True, False),
            ("Strong (24)", 24, True, True, True, True, False),
            ("PIN (6)", 6, False, False, True, False, False),
            ("Ultra (32)", 32, True, True, True, True, True),
        ]

        for label, len_val, up, low, dig, sym, amb in preset_options:
            btn = tk.Button(
                presets_bar,
                text=label,
                command=lambda l=len_val, u=up, lw=low, d=dig, s=sym, a=amb: self.app.apply_preset(l, u, lw, d, s, a),
                bg=BG_PILL,
                fg=TEXT_SECONDARY,
                activebackground=BG_HOVER,
                activeforeground=TEXT_PRIMARY,
                font=("SF Pro Text", 9),
                bd=0,
                relief="flat",
                padx=10,
                pady=4,
                cursor="hand2"
            )
            btn.pack(side="left", padx=3)

        card = tk.Frame(self, bg=BG_CARD, bd=1, relief="solid", highlightbackground=BORDER_COLOR)
        card.pack(fill="x", padx=24, pady=12)

        inner = tk.Frame(card, bg=BG_CARD, padx=20, pady=18)
        inner.pack(fill="x")

        len_header = tk.Frame(inner, bg=BG_CARD)
        len_header.pack(fill="x", pady=(0, 6))
        tk.Label(len_header, text="PASSWORD LENGTH", font=("SF Pro Text", 8, "bold"), bg=BG_CARD, fg=TEXT_SECONDARY).pack(side="left")

        len_controls = tk.Frame(inner, bg=BG_CARD)
        len_controls.pack(fill="x", pady=(0, 16))

        self.spinbox = tk.Spinbox(
            len_controls,
            from_=4,
            to=64,
            textvariable=self.app.length_var,
            width=4,
            font=("SF Pro Text", 11, "bold"),
            bg=BG_PILL,
            fg=TEXT_PRIMARY,
            buttonbackground=BG_PILL,
            bd=1,
            relief="solid"
        )
        self.spinbox.pack(side="right", padx=(12, 0))

        self.slider = ttk.Scale(
            len_controls,
            from_=4,
            to=64,
            variable=self.app.length_var,
            style="Apple.Horizontal.TScale",
            command=self._on_slider_change
        )
        self.slider.pack(side="left", fill="x", expand=True)

        divider = tk.Frame(inner, height=1, bg=BORDER_COLOR)
        divider.pack(fill="x", pady=(0, 14))

        tk.Label(inner, text="CHARACTER SETS (SELECT AT LEAST 2)", font=("SF Pro Text", 8, "bold"), bg=BG_CARD, fg=TEXT_SECONDARY).pack(anchor="w", pady=(0, 10))

        grid_frame = tk.Frame(inner, bg=BG_CARD)
        grid_frame.pack(fill="x")

        upper_chk = ttk.Checkbutton(grid_frame, text="Uppercase (A-Z)", variable=self.app.upper_var, style="Apple.TCheckbutton")
        upper_chk.grid(row=0, column=0, sticky="w", pady=6, padx=(0, 20))

        lower_chk = ttk.Checkbutton(grid_frame, text="Lowercase (a-z)", variable=self.app.lower_var, style="Apple.TCheckbutton")
        lower_chk.grid(row=0, column=1, sticky="w", pady=6)

        digits_chk = ttk.Checkbutton(grid_frame, text="Digits (0-9)", variable=self.app.digits_var, style="Apple.TCheckbutton")
        digits_chk.grid(row=1, column=0, sticky="w", pady=6, padx=(0, 20))

        symbols_chk = ttk.Checkbutton(grid_frame, text="Symbols (!@#$)", variable=self.app.symbols_var, style="Apple.TCheckbutton")
        symbols_chk.grid(row=1, column=1, sticky="w", pady=6)

        divider2 = tk.Frame(inner, height=1, bg=BORDER_COLOR)
        divider2.pack(fill="x", pady=(12, 12))

        ambiguous_chk = ttk.Checkbutton(inner, text="Exclude Ambiguous Characters (0, O, o, 1, l, I, |)", variable=self.app.ambiguous_var, style="Apple.TCheckbutton")
        ambiguous_chk.pack(anchor="w")

        self.error_label = tk.Label(self, text="", font=FONT_SUB, bg=BG_BASE, fg=COLOR_RED)
        self.error_label.pack(padx=24, pady=(4, 0))

        action_frame = tk.Frame(self, bg=BG_BASE, pady=16)
        action_frame.pack(fill="x", padx=24)

        self.generate_btn = tk.Button(
            action_frame,
            text="Generate Password",
            command=self.app.on_generate_submit,
            bg=TEXT_PRIMARY,
            fg=BG_BASE,
            activebackground=TEXT_SECONDARY,
            activeforeground=BG_BASE,
            font=("SF Pro Text", 12, "bold"),
            bd=0,
            relief="flat",
            pady=14,
            cursor="hand2"
        )
        self.generate_btn.pack(fill="x")

    def _on_slider_change(self, val):
        try:
            self.app.length_var.set(int(round(float(val))))
        except ValueError:
            pass
