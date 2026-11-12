import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from password_generator import generate_password, generate_passphrase
from password_core import evaluate_password, load_dictionary_words


class PasswordApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("620x460")

        self.dictionary = load_dictionary_words("dictionary.txt")

        # variables
        self.mode = tk.StringVar(value="characters")
        self.length = tk.IntVar(value=16)

        self.upper = tk.BooleanVar(value=True)
        self.lower = tk.BooleanVar(value=True)
        self.numbers = tk.BooleanVar(value=True)
        self.symbols = tk.BooleanVar(value=True)
        self.ambiguous = tk.BooleanVar(value=False)

        self.separator = tk.StringVar(value="-")
        self.pass_caps = tk.BooleanVar(value=False)
        self.pass_digits = tk.BooleanVar(value=False)

        self.password_var = tk.StringVar()

        self.build_ui()

    # ------------------------------

    def build_ui(self):

        main = ttk.Frame(self.root, padding=15)
        main.pack(fill="both", expand=True)

        title = ttk.Label(
            main,
            text="Password Generator",
            font=("Segoe UI", 16, "bold")
        )
        title.pack(pady=10)

        # mode selection
        mode_frame = ttk.Frame(main)
        mode_frame.pack(pady=5)

        ttk.Radiobutton(
            mode_frame,
            text="Characters",
            variable=self.mode,
            value="characters",
            command=self.update_mode
        ).pack(side="left", padx=10)

        ttk.Radiobutton(
            mode_frame,
            text="Words",
            variable=self.mode,
            value="words",
            command=self.update_mode
        ).pack(side="left", padx=10)

        # slider label
        self.length_label = ttk.Label(main, text="Password Length")
        self.length_label.pack()

        # slider
        self.slider = ttk.Scale(
            main,
            from_=8,
            to=64,
            orient="horizontal",
            variable=self.length,
            command=self.update_slider_label
        )

        self.slider.pack(fill="x", padx=40)

        self.slider_value = ttk.Label(main, text="16")
        self.slider_value.pack()

        # ---------------------------
        # character options
        # ---------------------------

        self.char_frame = ttk.LabelFrame(main, text="Character Options")
        self.char_frame.pack(fill="x", pady=10)

        ttk.Checkbutton(
            self.char_frame,
            text="Uppercase",
            variable=self.upper
        ).grid(row=0, column=0, sticky="w", padx=10)

        ttk.Checkbutton(
            self.char_frame,
            text="Lowercase",
            variable=self.lower
        ).grid(row=0, column=1, sticky="w", padx=10)

        ttk.Checkbutton(
            self.char_frame,
            text="Numbers",
            variable=self.numbers
        ).grid(row=1, column=0, sticky="w", padx=10)

        ttk.Checkbutton(
            self.char_frame,
            text="Symbols",
            variable=self.symbols
        ).grid(row=1, column=1, sticky="w", padx=10)

        ttk.Checkbutton(
            self.char_frame,
            text="Avoid Ambiguous Characters",
            variable=self.ambiguous
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=10)

        # ---------------------------
        # passphrase options
        # ---------------------------

        self.word_frame = ttk.LabelFrame(main, text="Passphrase Options")

        ttk.Label(self.word_frame, text="Separator").grid(
            row=0,
            column=0,
            padx=10,
            pady=5
        )

        ttk.Combobox(
            self.word_frame,
            textvariable=self.separator,
            values=["-", "_", ".", ",", " "],
            width=5,
            state="readonly"
        ).grid(row=0, column=1)

        ttk.Checkbutton(
            self.word_frame,
            text="Use Capital Letters",
            variable=self.pass_caps
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=10)

        ttk.Checkbutton(
            self.word_frame,
            text="Use Digit Substitution",
            variable=self.pass_digits
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=10)

        # ---------------------------
        # generate button
        # ---------------------------

        ttk.Button(
            main,
            text="Generate",
            command=self.generate
        ).pack(pady=10)

        # output
        output_frame = ttk.Frame(main)
        output_frame.pack(fill="x", pady=5)

        ttk.Entry(
            output_frame,
            textvariable=self.password_var,
            width=60
        ).pack(side="left", fill="x", expand=True)

        ttk.Button(
            output_frame,
            text="Copy",
            command=self.copy
        ).pack(side="left", padx=5)

        # strength meter
        self.progress = ttk.Progressbar(
            main,
            maximum=10,
            length=450
        )
        self.progress.pack(pady=10)

        self.strength_label = ttk.Label(main, text="Strength: N/A")
        self.strength_label.pack()

        self.update_mode()

    # ------------------------------

    def update_slider_label(self, event=None):

        value = int(self.length.get())
        self.slider_value.config(text=str(value))

    # ------------------------------

    def update_mode(self):

        if self.mode.get() == "words":

            self.length_label.config(text="Number of Words")

            self.slider.config(from_=3, to=10)

            if self.length.get() > 10:
                self.length.set(4)

            self.char_frame.pack_forget()
            self.word_frame.pack(fill="x", pady=10)

        else:

            self.length_label.config(text="Password Length")

            self.slider.config(from_=8, to=64)

            if self.length.get() < 8:
                self.length.set(16)

            self.word_frame.pack_forget()
            self.char_frame.pack(fill="x", pady=10)

        self.update_slider_label()

    # ------------------------------

    def generate(self):

        # Only check when generating character passwords
        if self.mode.get() == "characters":

            if not (
                self.upper.get()
                or self.lower.get()
                or self.numbers.get()
                or self.symbols.get()
            ):
                messagebox.showerror(
                    "Invalid Selection",
                    "Please select at least one character type."
                )
                return

            password = generate_password(
                int(self.length.get()),
                self.upper.get(),
                self.lower.get(),
                self.numbers.get(),
                self.symbols.get(),
                self.ambiguous.get()
            )

        else:

            password = generate_passphrase(
                int(self.length.get()),
                self.separator.get(),
                self.pass_caps.get(),
                self.pass_digits.get()
            )

        self.password_var.set(password)

        result = evaluate_password(password, self.dictionary)

        self.progress["value"] = result.score
        self.strength_label.config(text=f"Strength: {result.label}")

    # ------------------------------

    def copy(self):

        text = self.password_var.get()

        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)


def main():

    root = tk.Tk()
    PasswordApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()