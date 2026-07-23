import tkinter as tk
from theme import (
    BG_BASE, BG_CARD, BG_PILL, BG_HOVER, BORDER_COLOR,
    TEXT_PRIMARY, TEXT_SECONDARY, COLOR_GREEN, COLOR_RED,
    FONT_HEADING, FONT_SUB, FONT_MONO
)

class ResultPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_BASE)
        self.app = app

        header = tk.Frame(self, bg=BG_BASE, pady=16, padx=24)
        header.pack(fill="x")

        back_btn = tk.Button(
            header,
            text="← Edit Criteria",
            command=lambda: self.app.show_page("ConfigPage"),
            bg=BG_PILL,
            fg=TEXT_SECONDARY,
            activebackground=BG_HOVER,
            activeforeground=TEXT_PRIMARY,
            font=("SF Pro Text", 9, "bold"),
            bd=0,
            padx=12,
            pady=5,
            cursor="hand2"
        )
        back_btn.pack(anchor="w", pady=(0, 6))

        tk.Label(header, text="Generated Password", font=FONT_HEADING, bg=BG_BASE, fg=TEXT_PRIMARY).pack(anchor="w")

        card = tk.Frame(self, bg=BG_CARD, bd=1, relief="solid", highlightbackground=BORDER_COLOR)
        card.pack(fill="x", padx=24, pady=6)

        inner = tk.Frame(card, bg=BG_CARD, padx=18, pady=18)
        inner.pack(fill="x")

        tk.Label(inner, text="PASSWORD", font=("SF Pro Text", 8, "bold"), bg=BG_CARD, fg=TEXT_SECONDARY).pack(anchor="w", pady=(0, 8))

        pwd_row = tk.Frame(inner, bg=BG_CARD)
        pwd_row.pack(fill="x")

        self.pwd_entry = tk.Entry(
            pwd_row,
            font=FONT_MONO,
            bg=BG_PILL,
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            bd=0,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER_COLOR,
            justify="left"
        )
        self.pwd_entry.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 10))

        self.toggle_btn = tk.Button(
            pwd_row,
            text="Hide" if self.app.show_password_var.get() else "Show",
            command=self.app.toggle_password_visibility,
            bg=BG_PILL,
            fg=TEXT_PRIMARY,
            activebackground=BG_HOVER,
            activeforeground=TEXT_PRIMARY,
            bd=0,
            relief="flat",
            width=5,
            cursor="hand2",
            font=("SF Pro Text", 9, "bold")
        )
        self.toggle_btn.pack(side="left", padx=(0, 8))

        self.copy_btn = tk.Button(
            pwd_row,
            text="Copy",
            command=self.app.copy_to_clipboard,
            bg=TEXT_PRIMARY,
            fg=BG_BASE,
            activebackground=TEXT_SECONDARY,
            activeforeground=BG_BASE,
            font=("SF Pro Text", 10, "bold"),
            bd=0,
            relief="flat",
            padx=16,
            pady=7,
            cursor="hand2"
        )
        self.copy_btn.pack(side="right")

        self.toast_label = tk.Label(inner, text="", font=FONT_SUB, bg=BG_CARD, fg=COLOR_GREEN)
        self.toast_label.pack(anchor="w", pady=(6, 0))

        strength_card = tk.Frame(self, bg=BG_CARD, bd=1, relief="solid", highlightbackground=BORDER_COLOR)
        strength_card.pack(fill="x", padx=24, pady=6)

        strength_inner = tk.Frame(strength_card, bg=BG_CARD, padx=18, pady=14)
        strength_inner.pack(fill="x")

        top_row = tk.Frame(strength_inner, bg=BG_CARD)
        top_row.pack(fill="x", pady=(0, 6))

        tk.Label(top_row, text="SECURITY STRENGTH", font=("SF Pro Text", 8, "bold"), bg=BG_CARD, fg=TEXT_SECONDARY).pack(side="left")
        self.strength_label = tk.Label(top_row, text="-", font=("SF Pro Text", 9, "bold"), bg=BG_CARD, fg=TEXT_PRIMARY)
        self.strength_label.pack(side="right")

        self.strength_canvas = tk.Canvas(strength_inner, height=6, bg=BG_PILL, highlightthickness=0)
        self.strength_canvas.pack(fill="x")
        self.meter_bar = self.strength_canvas.create_rectangle(0, 0, 0, 6, fill=COLOR_GREEN, width=0)

        action_frame = tk.Frame(self, bg=BG_BASE, pady=8)
        action_frame.pack(fill="x", padx=24)

        self.regenerate_btn = tk.Button(
            action_frame,
            text="Generate Another",
            command=self.app._generate_password,
            bg=BG_PILL,
            fg=TEXT_PRIMARY,
            activebackground=BG_HOVER,
            activeforeground=TEXT_PRIMARY,
            font=("SF Pro Text", 11, "bold"),
            bd=0,
            relief="flat",
            pady=11,
            cursor="hand2"
        )
        self.regenerate_btn.pack(fill="x")

        history_card = tk.Frame(self, bg=BG_CARD, bd=1, relief="solid", highlightbackground=BORDER_COLOR)
        history_card.pack(fill="both", expand=True, padx=24, pady=(6, 16))

        history_inner = tk.Frame(history_card, bg=BG_CARD, padx=18, pady=12)
        history_inner.pack(fill="both", expand=True)

        hdr_row = tk.Frame(history_inner, bg=BG_CARD)
        hdr_row.pack(fill="x", pady=(0, 8))

        tk.Label(hdr_row, text="SESSION HISTORY (LAST 5)", font=("SF Pro Text", 8, "bold"), bg=BG_CARD, fg=TEXT_SECONDARY).pack(side="left")

        clear_btn = tk.Button(
            hdr_row,
            text="Clear",
            command=self.app.clear_history,
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            activebackground=BORDER_COLOR,
            activeforeground=COLOR_RED,
            font=("SF Pro Text", 8),
            bd=0,
            cursor="hand2"
        )
        clear_btn.pack(side="right")

        self.history_frame = tk.Frame(history_inner, bg=BG_CARD)
        self.history_frame.pack(fill="both", expand=True)
