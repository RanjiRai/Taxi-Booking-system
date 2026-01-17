import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import databaseConnection as db
import customerRegistration, forgotPassword, dashboard, customerDashboard
import driverDashboard

# global constants
PRIMARY_YELLOW = "#FFC300"
PRIMARY_DARK = "#020617"
PRIMARY_DARK_ALT = "#0f172a"
CARD_BG = "#0b1220"
TEXT_LIGHT = "#e5e7eb"
TEXT_MUTED = "#9ca3af"
ACCENT_BLUE = "#38bdf8"


#  helpers 
def make_modal(child, parent):
    try:
        child.transient(parent)
        child.grab_set()
        child.lift()
        child.focus_force()
    except Exception:
        pass


def center_on_parent(child, parent, w, h):
    try:
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (w // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (h // 2)
        child.geometry(f"{w}x{h}+{x}+{y}")
    except Exception:
        child.update_idletasks()
        x = (child.winfo_screenwidth() // 2) - (w // 2)
        y = (child.winfo_screenheight() // 2) - (h // 2)
        child.geometry(f"{w}x{h}+{x}+{y}")


def new_portal_window(parent, title, w, h):
    win = tk.Toplevel(parent)
    win.title(title)
    win.configure(bg=PRIMARY_DARK)
    win.resizable(False, False)
    center_on_parent(win, parent, w, h)
    make_modal(win, parent)
    return win


# customer login
class CustomerLogin:
    def __init__(self, win):
        self.win = win
        self.win.title("Customer Login")
        self.win.geometry("520x560")
        self.win.resizable(False, False)
        self.win.configure(bg=PRIMARY_DARK)

        self._build_ui()

    def _build_ui(self):
        outer = tk.Frame(self.win, bg=PRIMARY_DARK)
        outer.pack(fill="both", expand=True, padx=24, pady=24)

        card = tk.Frame(
            outer,
            bg=CARD_BG,
            bd=0,
            highlightthickness=1,
            highlightbackground="#1f2937",
        )
        card.pack(fill="both", expand=True)

        tk.Frame(card, bg=PRIMARY_YELLOW, height=4).pack(fill="x", side="top")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=28, pady=28)

        tk.Label(
            inner, text="Customer Login",
            font=("Segoe UI", 20, "bold"),
            fg=TEXT_LIGHT, bg=CARD_BG
        ).pack(anchor="w")

        tk.Label(
            inner,
            text="Sign in to book, manage,\nand track your rides.",
            font=("Segoe UI", 10),
            fg=TEXT_MUTED, bg=CARD_BG,
            justify="left",
        ).pack(anchor="w", pady=(4, 20))

        tk.Label(inner, text="Email", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_LIGHT, bg=CARD_BG).pack(anchor="w")

        self.email = ttk.Entry(inner, width=35, font=("Segoe UI", 11))
        self.email.pack(pady=(4, 14), ipady=4)

        tk.Label(inner, text="Password", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_LIGHT, bg=CARD_BG).pack(anchor="w")

        self.pw = ttk.Entry(inner, show="*", width=35, font=("Segoe UI", 11))
        self.pw.pack(pady=(4, 16), ipady=4)

        ttk.Button(inner, text="Login", style="Primary.TButton",
                   command=self.login).pack(fill="x", pady=(6, 10))

        ttk.Button(
            inner, text="Register New Account",
            style="Ghost.TButton",
            command=self.open_register,
        ).pack(fill="x", pady=4)

        ttk.Button(
            inner, text="Forgot Password",
            style="Ghost.TButton",
            command=self.open_forgot,
        ).pack(fill="x", pady=4)

    def login(self):
        q = "SELECT * FROM customer WHERE email=? AND password=?"
        res = db.run_query(q, (self.email.get().strip(), self.pw.get()), fetch=True)

        if res:
            self.win.destroy()
            customerDashboard.CustomerDashboard(res[0])
        else:
            messagebox.showerror("Error", "Invalid email or password", parent=self.win)

    def open_register(self):
        #  do NOT destroy login window
        customerRegistration.open_registration(self.win)

    def open_forgot(self):
        #  do NOT destroy login window
        forgotPassword.open_forgot(self.win)


# admin login
class AdminLogin:
    def __init__(self, win):
        self.win = win
        self.win.title("Admin Login")
        self.win.geometry("520x520")
        self.win.resizable(False, False)
        self.win.configure(bg=PRIMARY_DARK)

        self._build_ui()

    def _build_ui(self):
        outer = tk.Frame(self.win, bg=PRIMARY_DARK)
        outer.pack(fill="both", expand=True, padx=24, pady=24)

        card = tk.Frame(
            outer,
            bg=CARD_BG,
            bd=0,
            highlightthickness=1,
            highlightbackground="#1f2937",
        )
        card.pack(fill="both", expand=True)

        tk.Frame(card, bg=ACCENT_BLUE, height=4).pack(fill="x", side="top")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=28, pady=28)

        tk.Label(
            inner, text="Admin Portal",
            font=("Segoe UI", 20, "bold"),
            fg=TEXT_LIGHT, bg=CARD_BG
        ).pack(anchor="w")

        tk.Label(
            inner,
            text="Manage drivers, bookings,\nand dispatch.",
            font=("Segoe UI", 10),
            fg=TEXT_MUTED, bg=CARD_BG,
            justify="left",
        ).pack(anchor="w", pady=(4, 20))

        tk.Label(inner, text="Username", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_LIGHT, bg=CARD_BG).pack(anchor="w")

        self.user = ttk.Entry(inner, width=35, font=("Segoe UI", 11))
        self.user.pack(pady=(4, 14), ipady=4)

        tk.Label(inner, text="Password", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_LIGHT, bg=CARD_BG).pack(anchor="w")

        self.pw = ttk.Entry(inner, show="*", width=35, font=("Segoe UI", 11))
        self.pw.pack(pady=(4, 18), ipady=4)

        ttk.Button(inner, text="Login", style="Primary.TButton",
                   command=self.login).pack(fill="x", pady=(10, 4))

    def login(self):
        q = "SELECT * FROM admin WHERE username=? AND password=?"
        res = db.run_query(q, (self.user.get().strip(), self.pw.get()), fetch=True)

        if res:
            self.win.destroy()
            dashboard.AdminDashboard()
        else:
            messagebox.showerror("Error", "Invalid admin credentials", parent=self.win)


# driver login
class DriverLogin:
    def __init__(self, win):
        self.win = win
        self.win.title("Driver Login")
        self.win.geometry("520x540")
        self.win.resizable(False, False)
        self.win.configure(bg=PRIMARY_DARK)

        self._build_ui()

    def _build_ui(self):
        outer = tk.Frame(self.win, bg=PRIMARY_DARK)
        outer.pack(fill="both", expand=True, padx=24, pady=24)

        card = tk.Frame(
            outer,
            bg=CARD_BG,
            bd=0,
            highlightthickness=1,
            highlightbackground="#1f2937",
        )
        card.pack(fill="both", expand=True)

        tk.Frame(card, bg=PRIMARY_YELLOW, height=4).pack(fill="x", side="top")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=28, pady=28)

        tk.Label(
            inner, text="Driver Login",
            font=("Segoe UI", 20, "bold"),
            fg=TEXT_LIGHT, bg=CARD_BG
        ).pack(anchor="w")

        tk.Label(
            inner,
            text="Access your upcoming trips\nand schedules.",
            font=("Segoe UI", 10),
            fg=TEXT_MUTED, bg=CARD_BG,
            justify="left",
        ).pack(anchor="w", pady=(4, 20))

        tk.Label(inner, text="Email", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_LIGHT, bg=CARD_BG).pack(anchor="w")

        self.email = ttk.Entry(inner, width=35, font=("Segoe UI", 11))
        self.email.pack(pady=(4, 14), ipady=4)

        tk.Label(inner, text="Password", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_LIGHT, bg=CARD_BG).pack(anchor="w")

        self.pw = ttk.Entry(inner, show="*", width=35, font=("Segoe UI", 11))
        self.pw.pack(pady=(4, 18), ipady=4)

        ttk.Button(inner, text="Login", style="Primary.TButton",
                   command=self.login).pack(fill="x", pady=(10, 4))

    def login(self):
        q = "SELECT * FROM driver WHERE email=? AND password=?"
        res = db.run_query(q, (self.email.get().strip(), self.pw.get()), fetch=True)

        if res:
            self.win.destroy()
            driverDashboard.DriverDashboard(res[0])
        else:
            messagebox.showerror("Error", "Invalid driver credentials", parent=self.win)


# open windows
def open_customer_login():
    win = new_portal_window(root, "Customer Login", 520, 560)
    CustomerLogin(win)


def open_admin_login():
    win = new_portal_window(root, "Admin Login", 520, 520)
    AdminLogin(win)


def open_driver_login():
    win = new_portal_window(root, "Driver Login", 520, 540)
    DriverLogin(win)


# main window
if __name__ == "__main__":
    db.create_tables()

    root = tk.Tk()
    root.title("Taxi Booking System")
    root.geometry("960x560")
    root.minsize(860, 520)

    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(".", font=("Segoe UI", 10))
    style.configure("TEntry", padding=(10, 6), borderwidth=0)

    style.configure(
        "Primary.TButton",
        font=("Segoe UI Semibold", 10),
        padding=8,
        background=PRIMARY_YELLOW,
        foreground=PRIMARY_DARK,
        borderwidth=0,
        focusthickness=0,
    )
    style.map("Primary.TButton", background=[("active", "#e6b000")])

    style.configure(
        "Ghost.TButton",
        font=("Segoe UI", 10),
        padding=8,
        background=CARD_BG,
        foreground=TEXT_LIGHT,
        borderwidth=1,
        relief="solid",
    )
    style.map("Ghost.TButton", background=[("active", "#111827")])

    style.configure(
        "Menu.TButton",
        font=("Segoe UI Semibold", 11),
        padding=10,
        background="#111827",
        foreground=TEXT_LIGHT,
        borderwidth=0,
    )
    style.map("Menu.TButton", background=[("active", "#1f2933")])

    style.configure(
        "MenuHover.TButton",
        font=("Segoe UI Semibold", 11),
        padding=10,
        background="#1f2937",
        foreground=TEXT_LIGHT,
        borderwidth=0,
    )
    style.map("MenuHover.TButton", background=[("active", "#1f2933")])

    root.configure(bg=PRIMARY_DARK)

    main_container = tk.Frame(root, bg=PRIMARY_DARK)
    main_container.place(relx=0.5, rely=0.5, anchor="center",
                         relwidth=0.9, relheight=0.8)

    left = tk.Frame(main_container, bg=PRIMARY_DARK)
    left.pack(side="left", fill="both", expand=True, padx=(0, 20))

    right = tk.Frame(main_container, bg=PRIMARY_DARK)
    right.pack(side="right", fill="y")

    tk.Label(
        left,
        text="FASTTRACK",
        font=("Segoe UI Black", 18),
        fg=PRIMARY_YELLOW,
        bg=PRIMARY_DARK,
    ).pack(anchor="w", pady=(0, 10))

    tk.Label(
        left,
        text="FastTrack Taxi Services",
        font=("Segoe UI Black", 32, "bold"),
        fg="white",
        bg=PRIMARY_DARK,
    ).pack(anchor="w")

    tk.Label(
        left,
        text="Book reliable cabs in seconds.\nLive tracking, instant confirmations,\nno more waiting on the curb.",
        font=("Segoe UI", 12),
        fg=TEXT_MUTED,
        bg=PRIMARY_DARK,
        justify="left",
    ).pack(anchor="w", pady=(10, 25))

    tk.Label(
        left,
        text="● 24/7 city coverage • Real-time tracking • Trusted drivers",
        font=("Segoe UI", 10),
        fg=ACCENT_BLUE,
        bg=PRIMARY_DARK,
    ).pack(anchor="w")

    card = tk.Frame(
        right,
        bg=CARD_BG,
        bd=0,
        highlightthickness=1,
        highlightbackground="#1f2937",
    )
    card.pack(fill="both", expand=True, ipadx=40, ipady=40)

    tk.Frame(card, bg=PRIMARY_YELLOW, height=3).pack(fill="x", side="top")

    inner = tk.Frame(card, bg=CARD_BG)
    inner.pack(fill="both", expand=True, padx=28, pady=28)

    tk.Label(
        inner,
        text="Sign in to continue",
        font=("Segoe UI Semibold", 16),
        fg=TEXT_LIGHT,
        bg=CARD_BG,
    ).pack(anchor="w")

    tk.Label(
        inner,
        text="Choose your portal below to get started.",
        font=("Segoe UI", 10),
        fg=TEXT_MUTED,
        bg=CARD_BG,
    ).pack(anchor="w", pady=(4, 18))

    ttk.Separator(inner, orient="horizontal").pack(fill="x", pady=(0, 16))

    def add_menu_hover(widget):
        def on_enter(e):
            widget.configure(style="MenuHover.TButton")

        def on_leave(e):
            widget.configure(style="Menu.TButton")

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    btn_customer = ttk.Button(
        inner,
        text="Customer Login / Register",
        style="Menu.TButton",
        command=open_customer_login,
    )
    btn_customer.pack(fill="x", pady=6)
    add_menu_hover(btn_customer)

    btn_admin = ttk.Button(
        inner,
        text="Admin Login",
        style="Menu.TButton",
        command=open_admin_login,
    )
    btn_admin.pack(fill="x", pady=6)
    add_menu_hover(btn_admin)

    btn_driver = ttk.Button(
        inner,
        text="Driver Login",
        style="Menu.TButton",
        command=open_driver_login,
    )
    btn_driver.pack(fill="x", pady=6)
    add_menu_hover(btn_driver)

    tk.Label(
        inner,
        text="CityCab • FastTrack Taxi Booking System",
        font=("Segoe UI", 8),
        fg=TEXT_MUTED,
        bg=CARD_BG,
    ).pack(side="bottom", pady=(18, 0))

    root.mainloop()
