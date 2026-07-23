import tkinter as tk
from tkinter import ttk
from typing import List, Dict

from theme import (
    BG_BASE, BG_CARD, BG_PILL, BG_HOVER, BORDER_COLOR,
    TEXT_PRIMARY, TEXT_SECONDARY, COLOR_BLUE, COLOR_GREEN, COLOR_RED, FONT_MAIN, FONT_MONO
)
from generator import (
    generate_password,
    evaluate_strength,
    MIN_PASSWORD_LENGTH,
    MIN_CHARACTER_TYPES
)
from gui_config import ConfigPage
from gui_result import ResultPage

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

class PasswordGeneratorGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PassShield")
        self.root.geometry("540x740")
        self.root.minsize(500, 680)
        self.root.configure(bg=BG_BASE)

        self.length_var = tk.IntVar(value=16)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.ambiguous_var = tk.BooleanVar(value=False)
        self.show_password_var = tk.BooleanVar(value=True)

        self.current_password = ""
        self.history: List[str] = []

        self._configure_styles()

        self.container = tk.Frame(self.root, bg=BG_BASE)
        self.container.pack(fill="both", expand=True)

        self.pages: Dict[str, tk.Frame] = {}

        self.config_page = ConfigPage(self.container, self)
        self.config_page.grid(row=0, column=0, sticky="nsew")
        self.pages["ConfigPage"] = self.config_page

        self.result_page = ResultPage(self.container, self)
        self.result_page.grid(row=0, column=0, sticky="nsew")
        self.pages["ResultPage"] = self.result_page

        self.show_page("ConfigPage")

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(".", background=BG_BASE, foreground=TEXT_PRIMARY, font=FONT_MAIN)

        style.configure(
            "Apple.TCheckbutton",
            background=BG_CARD,
            foreground=TEXT_PRIMARY,
            font=FONT_MAIN,
            focuscolor=""
        )
        style.map("Apple.TCheckbutton",
            background=[("active", BG_CARD)],
            foreground=[("active", COLOR_BLUE)]
        )

        style.configure(
            "Apple.Horizontal.TScale",
            background=BG_CARD,
            troughcolor=BG_PILL,
            sliderlength=18,
            sliderthickness=18
        )

    def show_page(self, page_name: str):
        page = self.pages[page_name]
        page.tkraise()

    def apply_preset(self, length: int, upper: bool, lower: bool, digits: bool, symbols: bool, ambiguous: bool):
        self.length_var.set(length)
        self.upper_var.set(upper)
        self.lower_var.set(lower)
        self.digits_var.set(digits)
        self.symbols_var.set(symbols)
        self.ambiguous_var.set(ambiguous)
        self.config_page.error_label.config(text="")

    def on_generate_submit(self):
        if self._generate_password():
            self.show_page("ResultPage")

    def toggle_password_visibility(self):
        self.show_password_var.set(not self.show_password_var.get())
        if self.show_password_var.get():
            self.result_page.pwd_entry.config(show="")
            self.result_page.toggle_btn.config(text="Hide")
        else:
            self.result_page.pwd_entry.config(show="•")
            self.result_page.toggle_btn.config(text="Show")

    def _generate_password(self) -> bool:
        length = self.length_var.get()
        upper = self.upper_var.get()
        lower = self.lower_var.get()
        digits = self.digits_var.get()
        symbols = self.symbols_var.get()
        ambiguous = self.ambiguous_var.get()

        selected_types = sum([upper, lower, digits, symbols])
        min_types = 1 if (digits and not upper and not lower and not symbols) else MIN_CHARACTER_TYPES

        if selected_types < min_types:
            self.config_page.error_label.config(text="Select at least 2 character types.")
            return False

        self.config_page.error_label.config(text="")

        try:
            min_l = 4 if (digits and not upper and not lower and not symbols) else MIN_PASSWORD_LENGTH
            password = generate_password(
                length=length,
                include_upper=upper,
                include_lower=lower,
                include_digits=digits,
                include_symbols=symbols,
                exclude_ambiguous=ambiguous,
                min_length=min_l,
                min_types=min_types
            )
            self.current_password = password

            self.result_page.pwd_entry.delete(0, tk.END)
            self.result_page.pwd_entry.insert(0, password)

            self.copy_to_clipboard(show_toast=False)
            self.result_page.toast_label.config(text="Password generated and copied to clipboard", fg=COLOR_GREEN)

            self._update_strength_display(password, upper, lower, digits, symbols, ambiguous)
            self._update_history(password)
            return True

        except ValueError as err:
            self.config_page.error_label.config(text=str(err))
            return False

    def _update_strength_display(self, password, upper, lower, digits, symbols, ambiguous):
        info = evaluate_strength(password, upper, lower, digits, symbols, ambiguous)

        self.result_page.strength_label.config(
            text=f"{info['label']}  •  {info['entropy']} bits entropy",
            fg=info['color']
        )

        self.root.update_idletasks()
        canvas_width = self.result_page.strength_canvas.winfo_width()
        bar_width = int((info['score'] / 100.0) * canvas_width)

        self.result_page.strength_canvas.coords(self.result_page.meter_bar, 0, 0, bar_width, 6)
        self.result_page.strength_canvas.itemconfig(self.result_page.meter_bar, fill=info['color'])

    def copy_to_clipboard(self, show_toast: bool = True):
        if not self.current_password:
            return

        copied = False
        if HAS_PYPERCLIP:
            try:
                pyperclip.copy(self.current_password)
                copied = True
            except Exception:
                copied = False

        if not copied:
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(self.current_password)
                self.root.update()
                copied = True
            except Exception:
                copied = False

        if show_toast and copied:
            self.result_page.toast_label.config(text="Copied to clipboard", fg=COLOR_GREEN)
            self.root.after(2000, lambda: self.result_page.toast_label.config(text=""))

    def clear_history(self):
        self.history.clear()
        for widget in self.result_page.history_frame.winfo_children():
            widget.destroy()

    def _update_history(self, password: str):
        if password in self.history:
            self.history.remove(password)
        self.history.insert(0, password)
        self.history = self.history[:5]

        for widget in self.result_page.history_frame.winfo_children():
            widget.destroy()

        for pwd in self.history:
            row = tk.Frame(self.result_page.history_frame, bg=BG_PILL, pady=4, padx=12)
            row.pack(fill="x", pady=2)

            masked_pwd = pwd if self.show_password_var.get() else "•" * len(pwd)
            lbl = tk.Label(
                row,
                text=masked_pwd,
                font=FONT_MONO,
                bg=BG_PILL,
                fg=TEXT_PRIMARY,
                anchor="w"
            )
            lbl.pack(side="left", fill="x", expand=True)

            btn = tk.Button(
                row,
                text="Copy",
                command=lambda p=pwd: self._quick_copy(p),
                bg=BG_CARD,
                fg=TEXT_SECONDARY,
                activebackground=BG_HOVER,
                activeforeground=TEXT_PRIMARY,
                font=("SF Pro Text", 8, "bold"),
                bd=0,
                padx=8,
                pady=2,
                cursor="hand2"
            )
            btn.pack(side="right")

    def _quick_copy(self, password: str):
        self.current_password = password
        self.copy_to_clipboard(show_toast=True)
        self.result_page.toast_label.config(text=f"Copied item: {password[:6]}...", fg=COLOR_GREEN)

def launch_gui():
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
