import tkinter as tk
from tkinter import messagebox, ttk
import re
import databaseConnection as db

# Theme colors
PRIMARY_YELLOW = "#FFC300"
PRIMARY_DARK = "#020617"
CARD_BG = "#0b1220"
TEXT_LIGHT = "#e5e7eb"
TEXT_MUTED = "#9ca3af"


def open_registration(parent=None):
    # Create window (attach to parent if provided)
    try:
        win = tk.Toplevel(parent) if parent else tk.Toplevel()
    except RuntimeError:
        win = tk.Tk()

    win.title("Register Customer")
    win.configure(bg=PRIMARY_DARK)
    win.resizable(False, False)

    # ---- size + position ----
    W, H = 540, 620
    if parent:
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (W // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (H // 2)
        win.geometry(f"{W}x{H}+{x}+{y}")

        # keep attached + modal
        try:
            win.transient(parent)
            win.grab_set()
            win.lift()
            win.focus_force()
        except Exception:
            pass
    else:
        # center on screen
        win.update_idletasks()
        x = (win.winfo_screenwidth() - W) // 2
        y = (win.winfo_screenheight() - H) // 2
        win.geometry(f"{W}x{H}+{x}+{y}")

    #  STYLES
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(".", font=("Segoe UI", 10))
    style.configure("TEntry", padding=(10, 6), borderwidth=0)

    style.configure(
        "Primary.TButton",
        font=("Segoe UI Semibold", 11),
        padding=8,
        background=PRIMARY_YELLOW,
        foreground=PRIMARY_DARK,
        borderwidth=0,
    )
    style.map("Primary.TButton", background=[("active", "#e6b000")])

    #  LAYOUT
    outer = tk.Frame(win, bg=PRIMARY_DARK)
    outer.pack(fill="both", expand=True, padx=24, pady=24)

    card = tk.Frame(
        outer,
        bg=CARD_BG,
        highlightthickness=1,
        highlightbackground="#1f2937",
    )
    card.pack(fill="both", expand=True)

    tk.Frame(card, bg=PRIMARY_YELLOW, height=4).pack(fill="x")

    inner = tk.Frame(card, bg=CARD_BG)
    inner.pack(fill="both", expand=True, padx=28, pady=28)

    tk.Label(
        inner,
        text="Create Account",
        font=("Segoe UI", 22, "bold"),
        fg=TEXT_LIGHT,
        bg=CARD_BG,
    ).pack(anchor="w", pady=(10, 4))

    tk.Label(
        inner,
        text="Join FastTrack today to book and manage your rides.",
        font=("Segoe UI", 10),
        fg=TEXT_MUTED,
        bg=CARD_BG,
        wraplength=380,
        justify="left",
    ).pack(anchor="w", pady=(0, 18))

    #  INPUT HELPER
    def create_input(label, show=None):
        frame = tk.Frame(inner, bg=CARD_BG)
        frame.pack(fill="x", pady=6)

        tk.Label(
            frame,
            text=label,
            font=("Segoe UI", 9, "bold"),
            fg=TEXT_LIGHT,
            bg=CARD_BG,
        ).pack(anchor="w")

        entry = ttk.Entry(frame)
        if show:
            entry.configure(show=show)
        entry.pack(fill="x", ipady=4)
        return entry

    #  INPUTS
    name = create_input("Full Name")
    email = create_input("Email Address")
    tel = create_input("Telephone")
    pw = create_input("Password", show="*")

    #  REGISTER FUNCTION
    def register():
        n = name.get().strip()
        em = email.get().strip()
        phone = tel.get().strip()
        pwd = pw.get().strip()

        if not all([n, em, phone, pwd]):
            messagebox.showerror("Error", "All fields are required.", parent=win)
            return

        if len(n) < 3 or not re.match(r"^[A-Za-z\s'.-]+$", n):
            messagebox.showerror(
                "Invalid Name",
                "Name must be at least 3 characters and contain letters only.",
                parent=win,
            )
            return

        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", em):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.", parent=win)
            return

        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Invalid Telephone", "Telephone must be exactly 10 digits.", parent=win)
            return

        if len(pwd) < 6 or not re.search(r"[A-Za-z]", pwd) or not re.search(r"\d", pwd):
            messagebox.showerror(
                "Weak Password",
                "Password must be at least 6 characters and contain letters & numbers.",
                parent=win,
            )
            return

        check = db.run_query("SELECT 1 FROM customer WHERE email=?", (em,), fetch=True)
        if check:
            messagebox.showerror(
                "Email Already Registered",
                "This email is already registered.\nPlease login instead.",
                parent=win,
            )
            return

        try:
            db.run_query(
                "INSERT INTO customer (name, email, telephone, password) VALUES (?,?,?,?)",
                (n, em, phone, pwd),
            )
            messagebox.showinfo("Success", "Registration successful! Please login.", parent=win)
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed:\n{e}", parent=win)

    ttk.Button(
        inner,
        text="Create Account",
        style="Primary.TButton",
        command=register,
    ).pack(fill="x", pady=(26, 8))

    tk.Label(
        inner,
        text="Already registered? Close this window and login.",
        font=("Segoe UI", 8),
        fg=TEXT_MUTED,
        bg=CARD_BG,
    ).pack(side="bottom", pady=(12, 0))

    if isinstance(win, tk.Tk):
        win.mainloop()


if __name__ == "__main__":
    open_registration()
