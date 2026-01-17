import tkinter as tk
from tkinter import messagebox, ttk
import databaseConnection as db
import datetime

# Theme colors
PRIMARY_YELLOW = "#FFC300"
PRIMARY_DARK = "#020617"
CARD_BG = "#0b1220"
TEXT_LIGHT = "#e5e7eb"
TEXT_MUTED = "#9ca3af"


def apply_styles():
    """Apply shared styles."""
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(".", font=("Segoe UI", 10))

    for name in ("Primary.TButton", "Yellow.TButton"):
        style.configure(
            name,
            font=("Segoe UI Semibold", 11),
            padding=6,
            background=PRIMARY_YELLOW,
            foreground=PRIMARY_DARK,
        )
        style.map(name, background=[("active", "#e6b000")])

    style.configure(
        "Secondary.TButton",
        font=("Segoe UI", 10),
        padding=6,
        background="#111827",
        foreground=TEXT_LIGHT,
    )
    style.map("Secondary.TButton", background=[("active", "#1f2937")])

    style.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=28,
        background=PRIMARY_DARK,
        fieldbackground=PRIMARY_DARK,
        foreground=TEXT_LIGHT,
    )
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        background="#111827",
        foreground=TEXT_LIGHT,
    )


def make_modal(win, parent):
    """Keep window attached to parent and focus it."""
    try:
        win.transient(parent)
        win.grab_set()
        win.lift()
        win.focus_force()
    except Exception:
        pass


def center_on_parent(win, parent, w, h):
    """Center win on parent."""
    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() // 2) - (w // 2)
    y = parent.winfo_y() + (parent.winfo_height() // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")


def center_on_screen(win, w, h):
    """Center win on screen."""
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (w // 2)
    y = (win.winfo_screenheight() // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")


#  Driver Login 
class DriverLogin:
    def __init__(self, root=None):
        self.parent = root
        self.win = tk.Toplevel(root) if root else tk.Tk()

        self.win.title("Driver Login")
        self.win.configure(bg=PRIMARY_DARK)
        self.win.resizable(False, False)

        apply_styles()

        outer = tk.Frame(self.win, bg=PRIMARY_DARK)
        outer.pack(fill="both", expand=True, padx=24, pady=24)

        card = tk.Frame(
            outer,
            bg=CARD_BG,
            highlightbackground="#1f2937",
            highlightthickness=1
        )
        card.pack(fill="both", expand=True)

        tk.Frame(card, bg=PRIMARY_YELLOW, height=3).pack(fill="x", side="top")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=28, pady=28)

        tk.Label(
            inner,
            text="Driver Login",
            font=("Segoe UI", 20, "bold"),
            bg=CARD_BG,
            fg=TEXT_LIGHT
        ).pack(anchor="w")

        tk.Label(
            inner,
            text="Enter your credentials to continue.",
            font=("Segoe UI", 10),
            bg=CARD_BG,
            fg=TEXT_MUTED
        ).pack(anchor="w", pady=(4, 20))

        self.email = self.create_input(inner, "Email Address")
        self.pw = self.create_input(inner, "Password", show="*")

        ttk.Button(
            inner,
            text="Login",
            style="Primary.TButton",
            command=self.login
        ).pack(fill="x", pady=24)

        self.email.focus()

        # Set fixed size
        W, H = 520, 420
        self.win.update_idletasks()
        self.win.geometry(f"{W}x{H}")

        # attach + modal if opened from parent
        if self.parent:
            center_on_parent(self.win, self.parent, W, H)
            make_modal(self.win, self.parent)
        else:
            center_on_screen(self.win, W, H)

        if root is None:
            self.win.mainloop()

    def create_input(self, parent, label, show=None):
        frame = tk.Frame(parent, bg=CARD_BG)
        frame.pack(fill="x", pady=6)

        tk.Label(
            frame,
            text=label,
            font=("Segoe UI", 9, "bold"),
            bg=CARD_BG,
            fg=TEXT_LIGHT
        ).pack(fill="x")

        entry = ttk.Entry(frame, font=("Segoe UI", 10), show=show)
        entry.pack(fill="x", pady=(3, 0), ipady=3)
        return entry

    def login(self):
        email = self.email.get().strip()
        pw = self.pw.get()

        if not email or not pw:
            messagebox.showerror("Error", "All fields are required", parent=self.win)
            return

        q = "SELECT * FROM driver WHERE email=? AND password=?"
        r = db.run_query(q, (email, pw), fetch=True) or []

        if r:
            # close login window
            self.win.destroy()

            # open dashboard attached to parent (or standalone)
            DriverDashboard(r[0], parent=self.parent)
        else:
            messagebox.showerror("Error", "Invalid driver credentials", parent=self.win)


#  Driver Dashboard 
class DriverDashboard:
    def __init__(self, driver, parent=None):
        self.driver = driver

        #  IMPORTANT: Use Toplevel, not Tk()
        self.win = tk.Toplevel(parent) if parent else tk.Toplevel()
        self.win.title(f"Driver Dashboard • {driver['name']}")
        self.win.geometry("1150x620")
        self.win.configure(bg=PRIMARY_DARK)

        apply_styles()

        # Header
        header = tk.Frame(self.win, bg=PRIMARY_DARK, height=80)
        header.pack(fill="x", padx=24, pady=(20, 10))
        header.pack_propagate(False)

        left = tk.Frame(header, bg=PRIMARY_DARK)
        left.pack(side="left")

        tk.Label(
            left,
            text="Driver Dashboard",
            font=("Segoe UI", 20, "bold"),
            bg=PRIMARY_DARK,
            fg=TEXT_LIGHT
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Your assigned trips and status updates.",
            font=("Segoe UI", 10),
            bg=PRIMARY_DARK,
            fg=TEXT_MUTED
        ).pack(anchor="w")

        right = tk.Frame(header, bg=PRIMARY_DARK)
        right.pack(side="right")

        tk.Label(
            right,
            text=self.driver["name"],
            font=("Segoe UI", 12, "bold"),
            bg=PRIMARY_DARK,
            fg=TEXT_LIGHT
        ).pack(anchor="e")

        status = "Available" if int(self.driver["available"]) == 1 else "On Trip"
        self.status_label = tk.Label(
            right,
            text=status,
            font=("Segoe UI", 10),
            bg=PRIMARY_DARK,
            fg="green" if status == "Available" else "red"
        )
        self.status_label.pack(anchor="e")

        # Content
        content = tk.Frame(self.win, bg=PRIMARY_DARK)
        content.pack(fill="both", expand=True, padx=24, pady=10)

        tk.Label(
            content,
            text="Assigned Trips",
            font=("Segoe UI", 16, "bold"),
            bg=PRIMARY_DARK,
            fg=TEXT_LIGHT
        ).pack(anchor="w", pady=(0, 12))

        table_card = tk.Frame(
            content,
            bg=CARD_BG,
            bd=1,
            relief=tk.SOLID,
            highlightbackground="#1f2937",
            highlightthickness=1
        )
        table_card.pack(fill="both", expand=True)

        columns = (
            "id", "customer", "pickup", "dropoff",
            "pick_date", "pick_time", "drop_date",
            "drop_time", "fare", "status"
        )

        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", style="Treeview")

        col_names = [
            "ID", "Customer", "Pickup", "Drop-off", "P. Date", "P. Time",
            "D. Date", "D. Time", "Fare", "Status"
        ]
        col_widths = [50, 120, 150, 150, 90, 80, 90, 80, 80, 90]

        for col, name, w in zip(columns, col_names, col_widths):
            self.tree.heading(col, text=name)
            self.tree.column(col, width=w, anchor="center")

        vsb = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_card, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        btn_frame = tk.Frame(content, bg=PRIMARY_DARK)
        btn_frame.pack(fill="x", pady=16)

        ttk.Button(
            btn_frame,
            text="Refresh",
            style="Secondary.TButton",
            command=self.load_trips
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            btn_frame,
            text="✓ Mark Completed",
            style="Primary.TButton",
            command=self.complete_trip
        ).pack(side="left")

        self.tree.bind("<Double-1>", lambda e: self.complete_trip())

        self.load_trips()

    def refresh_driver_data(self):
        r = db.run_query("SELECT * FROM driver WHERE id=?", (self.driver["id"],), fetch=True) or []
        if r:
            self.driver = r[0]
            status = "Available" if int(self.driver["available"]) == 1 else "On Trip"
            self.status_label.config(
                text=status,
                fg="green" if status == "Available" else "red"
            )

    def load_trips(self):
        self.tree.delete(*self.tree.get_children())

        q = """
        SELECT t.id, c.name as customer, t.pickup, t.dropoff,
               t.pickup_date, t.pickup_time,
               t.dropoff_date, t.dropoff_time,
               t.fare, t.status
        FROM trip t
        LEFT JOIN customer c ON t.customer_id = c.id
        WHERE t.driver_id=? AND t.status NOT IN ('completed', 'cancelled')
        ORDER BY t.created_at DESC
        """

        rows = db.run_query(q, (self.driver["id"],), fetch=True) or []

        for r in rows:
            fare = f"Rs. {float(r['fare']):.2f}"
            p_date = r["pickup_date"] or ""
            p_time = r["pickup_time"] or ""
            d_date = r["dropoff_date"] or ""
            d_time = r["dropoff_time"] or ""
            status = str(r["status"]).capitalize()

            self.tree.insert("", "end", values=(
                r["id"], r["customer"] or "Unknown",
                r["pickup"], r["dropoff"],
                p_date, p_time, d_date, d_time,
                fare, status,
            ))

        #  FIX: no .get() here
        if not rows and int(self.driver["available"]) == 0:
            db.run_query("UPDATE driver SET available=1 WHERE id=?", (self.driver["id"],))
            self.refresh_driver_data()

    def complete_trip(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select Trip", "Please select a trip.", parent=self.win)
            return

        data = self.tree.item(sel[0])["values"]
        trip_id = data[0]
        status = str(data[-1]).lower()

        if status == "cancelled":
            messagebox.showerror("Error", "This trip is cancelled.", parent=self.win)
            return

        date = datetime.date.today().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")

        db.run_query(
            "UPDATE trip SET status='completed', dropoff_date=?, dropoff_time=? WHERE id=?",
            (date, time, trip_id),
        )
        db.run_query("UPDATE driver SET available=1 WHERE id=?", (self.driver["id"],))

        self.refresh_driver_data()
        messagebox.showinfo("Success", "Trip marked completed.", parent=self.win)
        self.load_trips()


if __name__ == "__main__":
    DriverLogin()
