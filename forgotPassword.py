import tkinter as tk
from tkinter import messagebox, ttk
import databaseConnection as db

# Theme colors
PRIMARY_YELLOW = "#FFC300"
PRIMARY_DARK = "#020617"
CARD_BG = "#0b1220"
TEXT_LIGHT = "#e5e7eb"
TEXT_MUTED = "#9ca3af"


def open_forgot(parent=None):
    """Forgot password window (attached to parent)."""
    try:
        win = tk.Toplevel(parent) if parent else tk.Toplevel()
    except RuntimeError:
        win = tk.Tk()

    win.title("Forgot Password")
    win.configure(bg=PRIMARY_DARK)
    win.resizable(False, False)

    W, H = 520, 500

    # Center + attach
    if parent:
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (W // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (H // 2)
        win.geometry(f"{W}x{H}+{x}+{y}")

        # Modal behavior
        try:
            win.transient(parent)
            win.grab_set()
            win.lift()
            win.focus_force()
        except Exception:
            pass
    else:
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (W // 2)
        y = (win.winfo_screenheight() // 2) - (H // 2)
        win.geometry(f"{W}x{H}+{x}+{y}")

    # Styles
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
    )
    style.map("Primary.TButton", background=[("active", "#e6b000")])

    # Layout
    outer = tk.Frame(win, bg=PRIMARY_DARK)
    outer.pack(fill="both", expand=True, padx=24, pady=24)

    card = tk.Frame(
        outer, bg=CARD_BG,
        highlightbackground="#1f2937",
        highlightthickness=1
    )
    card.pack(fill="both", expand=True)

    tk.Frame(card, bg=PRIMARY_YELLOW, height=4).pack(fill="x", side="top")

    inner = tk.Frame(card, bg=CARD_BG)
    inner.pack(fill="both", expand=True, padx=28, pady=28)

    tk.Label(
        inner,
        text="Reset Password",
        font=("Segoe UI", 20, "bold"),
        bg=CARD_BG,
        fg=TEXT_LIGHT
    ).pack(anchor="w")

    tk.Label(
        inner,
        text="Enter your registered email and new password.",
        font=("Segoe UI", 10),
        bg=CARD_BG,
        fg=TEXT_MUTED
    ).pack(anchor="w", pady=(4, 18))

    # Input helper
    def create_input(label, show=None):
        frame = tk.Frame(inner, bg=CARD_BG)
        frame.pack(fill="x", pady=6)

        tk.Label(
            frame,
            text=label,
            font=("Segoe UI", 9, "bold"),
            bg=CARD_BG,
            fg=TEXT_LIGHT
        ).pack(fill="x")

        entry = ttk.Entry(frame, font=("Segoe UI", 10), show=show)
        entry.pack(fill="x", pady=(3, 0), ipady=4)
        return entry

    # Inputs
    email = create_input("Registered Email")
    newpw = create_input("New Password", show="*")

    # Update logic
    def change_pw():
        if not email.get().strip() or not newpw.get().strip():
            messagebox.showerror("Error", "All fields are required", parent=win)
            return

        q = "UPDATE customer SET password=? WHERE email=?"
        try:
            db.run_query(q, (newpw.get().strip(), email.get().strip()))
            messagebox.showinfo("Success", "Password updated (if email exists).", parent=win)
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update password: {e}", parent=win)

    ttk.Button(
        inner,
        text="Update Password",
        style="Primary.TButton",
        command=change_pw
    ).pack(fill="x", pady=(24, 8))

    tk.Label(
        inner,
        text="If the email is not registered, nothing will change.",
        font=("Segoe UI", 8),
        bg=CARD_BG,
        fg=TEXT_MUTED,
        wraplength=360,
        justify="center",
    ).pack(side="bottom", pady=10)

    if isinstance(win, tk.Tk):
        win.mainloop()


if __name__ == "__main__":
    open_forgot()
