import tkinter as tk
from tkinter import messagebox, ttk
import re
import databaseConnection as db
import assignDriver

# Theme colors
PRIMARY_YELLOW = "#FFC300"
PRIMARY_DARK = "#020617"
CARD_BG = "#0b1220"
TEXT_LIGHT = "#e5e7eb"
TEXT_MUTED = "#9ca3af"
ACCENT_BLUE = "#38bdf8"


#  Window Helpers 
def make_modal(child: tk.Toplevel, parent: tk.Misc):
    """Attach child to parent and keep it on top until closed."""
    try:
        child.transient(parent)
        child.grab_set()
        child.lift()
        child.focus_force()
    except Exception:
        pass


def center_on_parent(child: tk.Toplevel, parent: tk.Misc, w: int, h: int):
    """Center a toplevel window over its parent."""
    try:
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (w // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (h // 2)
        child.geometry(f"{w}x{h}+{x}+{y}")
    except Exception:
        # fallback: center on screen
        child.update_idletasks()
        sw = child.winfo_screenwidth()
        sh = child.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        child.geometry(f"{w}x{h}+{x}+{y}")


#  Admin Dashboard 
class AdminDashboard:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Admin Dashboard • FastTrack")
        self.win.geometry("1040x640")
        self.win.configure(bg=PRIMARY_DARK)
        self.win.resizable(False, False)

        # Styles
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure(".", font=("Segoe UI", 10))

        self.style.configure(
            "Primary.TButton",
            font=("Segoe UI Semibold", 11),
            padding=8,
            background=PRIMARY_YELLOW,
            foreground=PRIMARY_DARK,
            borderwidth=0,
        )
        self.style.map("Primary.TButton", background=[("active", "#e6b000")])

        self.style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 10),
            padding=8,
            background="#111827",
            foreground=TEXT_LIGHT,
            borderwidth=0,
        )
        self.style.map("Secondary.TButton", background=[("active", "#1f2937")])

        self.style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=28,
            background="#020617",
            fieldbackground="#020617",
            foreground=TEXT_LIGHT,
        )
        self.style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#111827",
            foreground=TEXT_LIGHT,
        )

        # Layout
        main_container = tk.Frame(self.win, bg=PRIMARY_DARK)
        main_container.pack(fill="both", expand=True, padx=40, pady=40)

        # Left side text
        left = tk.Frame(main_container, bg=PRIMARY_DARK)
        left.pack(side="left", fill="both", expand=True, padx=(0, 24))

        tk.Label(
            left,
            text="FastTrack Admin Console",
            font=("Segoe UI Black", 26, "bold"),
            fg="white",
            bg=PRIMARY_DARK,
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Monitor trips, manage drivers,\nand keep payments in sync.",
            font=("Segoe UI", 11),
            fg=TEXT_MUTED,
            bg=PRIMARY_DARK,
            justify="left",
        ).pack(anchor="w", pady=(8, 24))

        tk.Label(
            left,
            text="● Live trip history   • Driver availability   • Secure payments",
            font=("Segoe UI", 9),
            fg=ACCENT_BLUE,
            bg=PRIMARY_DARK,
        ).pack(anchor="w")

        # Right actions card
        right = tk.Frame(main_container, bg=PRIMARY_DARK)
        right.pack(side="right", fill="y")

        card = tk.Frame(
            right,
            bg=CARD_BG,
            bd=0,
            highlightthickness=1,
            highlightbackground="#1f2937",
        )
        card.pack(fill="both", expand=True, ipadx=40, ipady=40)

        accent = tk.Frame(card, bg=PRIMARY_YELLOW, height=3)
        accent.pack(fill="x", side="top")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=28, pady=28)

        tk.Label(
            inner,
            text="Admin Dashboard",
            font=("Segoe UI Semibold", 18),
            fg=TEXT_LIGHT,
            bg=CARD_BG,
        ).pack(anchor="w")

        tk.Label(
            inner,
            text="Choose a section to manage your system.",
            font=("Segoe UI", 10),
            fg=TEXT_MUTED,
            bg=CARD_BG,
        ).pack(anchor="w", pady=(4, 18))

        ttk.Separator(inner, orient="horizontal").pack(fill="x", pady=(0, 18))

        grid = tk.Frame(inner, bg=CARD_BG)
        grid.pack(expand=True)

        btn_w = 22

        ttk.Button(
            grid,
            text="Manage Drivers",
            style="Primary.TButton",
            width=btn_w,
            command=self.open_drivers,
        ).grid(row=0, column=0, padx=10, pady=10, ipady=4)

        ttk.Button(
            grid,
            text="View All Trips",
            style="Primary.TButton",
            width=btn_w,
            command=self.open_trips,
        ).grid(row=0, column=1, padx=10, pady=10, ipady=4)

        ttk.Button(
            grid,
            text="Assign Driver",
            style="Secondary.TButton",
            width=btn_w,
            command=self.open_assign,
        ).grid(row=1, column=0, padx=10, pady=10, ipady=4)

        ttk.Button(
            grid,
            text="Payment Records",
            style="Secondary.TButton",
            width=btn_w,
            command=self.open_payments,
        ).grid(row=1, column=1, padx=10, pady=10, ipady=4)

        tk.Label(
            inner,
            text="FastTrack Taxi Services • Admin Panel",
            font=("Segoe UI", 8),
            fg=TEXT_MUTED,
            bg=CARD_BG,
        ).pack(side="bottom", pady=(18, 0))

        self.win.mainloop()

    # Navigation
    def open_drivers(self):
        DriverManager(self.win)

    def open_trips(self):
        TripManager(self.win)

    def open_assign(self):
        # assignDriver already fixed; it will use parent=self.win
        assignDriver.AssignDriverWindow(self.win)

    def open_payments(self):
        PaymentManager(self.win)


#  Driver Manager 
class DriverManager:
    def __init__(self, parent):
        self.parent = parent
        self.win = tk.Toplevel(parent)
        self.win.title("Driver Management • FastTrack")
        self.win.configure(bg=PRIMARY_DARK)

        center_on_parent(self.win, parent, 980, 560)
        make_modal(self.win, parent)

        # Header
        top_frame = tk.Frame(self.win, bg=PRIMARY_DARK)
        top_frame.pack(fill="x", padx=24, pady=20)

        tk.Label(
            top_frame,
            text="Registered Drivers",
            font=("Segoe UI", 18, "bold"),
            bg=PRIMARY_DARK,
            fg=TEXT_LIGHT,
        ).pack(side="left")

        action_frame = tk.Frame(top_frame, bg=PRIMARY_DARK)
        action_frame.pack(side="right")

        ttk.Button(
            action_frame,
            text="Refresh List",
            style="Secondary.TButton",
            command=self.load,
        ).pack(side="left", padx=6)

        ttk.Button(
            action_frame,
            text="+ Add New Driver",
            style="Primary.TButton",
            command=self.add_driver,
        ).pack(side="left", padx=6)

        ttk.Button(
            action_frame,
            text="Update Driver",
            style="Secondary.TButton",
            command=self.edit_driver,
        ).pack(side="left", padx=6)

        ttk.Button(
            action_frame,
            text="Delete Driver",
            style="Secondary.TButton",
            command=self.delete_driver,
        ).pack(side="left", padx=6)

        # Table
        tree_frame = tk.Frame(self.win, bg=CARD_BG, bd=1, relief=tk.SOLID)
        tree_frame.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        cols = ("id", "name", "email", "phone", "license", "avail")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", style="Treeview")

        headings = {
            "id": "ID",
            "name": "Name",
            "email": "Email",
            "phone": "Phone",
            "license": "License No.",
            "avail": "Available",
        }
        widths = {
            "id": 60,
            "name": 160,
            "email": 220,
            "phone": 120,
            "license": 140,
            "avail": 90,
        }

        for col in cols:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")

        y_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)

        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        self.load()

    def load(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        rows = db.run_query("SELECT * FROM driver", fetch=True) or []
        for r in rows:
            status = "Yes" if r["available"] == 1 else "No"
            self.tree.insert(
                "",
                "end",
                values=(
                    r["id"],
                    r["name"],
                    r["email"],
                    r["phone"],
                    r["license_number"],
                    status,
                ),
            )

    def add_driver(self):
        AddDriverWindow(self.win, self)

    def get_selected_driver_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select Driver", "Please select a driver first.", parent=self.win)
            return None
        item = self.tree.item(sel[0])
        driver_id = item["values"][0]
        return driver_id

    def edit_driver(self):
        driver_id = self.get_selected_driver_id()
        if driver_id is None:
            return
        EditDriverWindow(self.win, self, driver_id)

    def delete_driver(self):
        driver_id = self.get_selected_driver_id()
        if driver_id is None:
            return

        if not messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete driver ID {driver_id}?",
            parent=self.win,
        ):
            return

        try:
            db.run_query("DELETE FROM driver WHERE id=?", (driver_id,))
            messagebox.showinfo("Deleted", "Driver deleted successfully.", parent=self.win)
            self.load()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete driver: {e}", parent=self.win)


#  Add Driver 
class AddDriverWindow:
    def __init__(self, parent_win, manager):
        self.manager = manager
        self.parent = parent_win
        self.win = tk.Toplevel(parent_win)
        self.win.title("Add New Driver")
        self.win.configure(bg=PRIMARY_DARK)
        self.win.resizable(False, False)

        center_on_parent(self.win, parent_win, 480, 560)
        make_modal(self.win, parent_win)

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

        accent = tk.Frame(card, bg=PRIMARY_YELLOW, height=3)
        accent.pack(fill="x", side="top")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=26, pady=26)

        tk.Label(
            inner,
            text="Add Driver",
            font=("Segoe UI", 18, "bold"),
            fg=TEXT_LIGHT,
            bg=CARD_BG,
        ).pack(anchor="w", pady=(0, 16))

        def create_entry(label_text, show=None):
            frame = tk.Frame(inner, bg=CARD_BG)
            frame.pack(fill="x", pady=6)

            tk.Label(
                frame,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                bg=CARD_BG,
                fg=TEXT_LIGHT,
                anchor="w",
            ).pack(fill="x")
            entry = ttk.Entry(frame, font=("Segoe UI", 10), show=show)
            entry.pack(fill="x", pady=(3, 0), ipady=3)
            return entry

        self.name = create_entry("Full Name")
        self.email = create_entry("Email Address")
        self.phone = create_entry("Phone Number")
        self.lic = create_entry("License Number")
        self.pw = create_entry("Password", show="*")

        ttk.Button(
            inner,
            text="Save Driver",
            style="Primary.TButton",
            command=self.add,
        ).pack(fill="x", pady=(24, 0))

        self.win.geometry("480x560")

    def add(self):
        name = self.name.get().strip()
        email = self.email.get().strip()
        phone = self.phone.get().strip()
        lic = self.lic.get().strip()
        pw = self.pw.get().strip()

        if not all([name, email, phone, lic, pw]):
            messagebox.showerror("Error", "All fields are required", parent=self.win)
            return

        if len(name) < 3 or not re.match(r"^[A-Za-z\s'.-]+$", name):
            messagebox.showerror(
                "Invalid Name",
                "Enter a valid name (at least 3 letters, letters and spaces only).",
                parent=self.win,
            )
            return

        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            messagebox.showerror("Invalid Email", "Enter a valid email address.", parent=self.win)
            return

        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Invalid Phone", "Enter a valid 10-digit phone number.", parent=self.win)
            return

        if len(lic) < 3 or not re.match(r"^[A-Za-z0-9\- ]+$", lic):
            messagebox.showerror("Invalid License", "Enter a valid license number.", parent=self.win)
            return

        if len(pw) < 6:
            messagebox.showerror("Weak Password", "Password must be at least 6 characters long.", parent=self.win)
            return

        if not re.search(r"[A-Za-z]", pw) or not re.search(r"\d", pw):
            messagebox.showerror(
                "Weak Password",
                "Password must contain at least one letter and one number.",
                parent=self.win,
            )
            return

        q = "INSERT INTO driver (name,email,phone,license_number,password) VALUES (?,?,?,?,?)"
        try:
            db.run_query(q, (name, email, phone, lic, pw))
            messagebox.showinfo("Success", "Driver added successfully", parent=self.win)
            self.win.destroy()
            self.manager.load()
        except Exception as e:
            err = str(e)
            if "UNIQUE constraint failed" in err and "driver.email" in err:
                messagebox.showerror("Email Exists", "This email is already registered for another driver.", parent=self.win)
            else:
                messagebox.showerror("Error", f"Failed to add driver: {err}", parent=self.win)


#  Edit Driver 
class EditDriverWindow:
    def __init__(self, parent_win, manager, driver_id):
        self.manager = manager
        self.driver_id = driver_id
        self.parent = parent_win
        self.win = tk.Toplevel(parent_win)
        self.win.title(f"Edit Driver #{driver_id}")
        self.win.configure(bg=PRIMARY_DARK)
        self.win.resizable(False, False)

        center_on_parent(self.win, parent_win, 480, 560)
        make_modal(self.win, parent_win)

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

        accent = tk.Frame(card, bg=PRIMARY_YELLOW, height=3)
        accent.pack(fill="x", side="top")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=26, pady=26)

        tk.Label(
            inner,
            text=f"Edit Driver (ID: {driver_id})",
            font=("Segoe UI", 18, "bold"),
            fg=TEXT_LIGHT,
            bg=CARD_BG,
        ).pack(anchor="w", pady=(0, 16))

        def create_entry(label_text):
            frame = tk.Frame(inner, bg=CARD_BG)
            frame.pack(fill="x", pady=6)

            tk.Label(
                frame,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                bg=CARD_BG,
                fg=TEXT_LIGHT,
                anchor="w",
            ).pack(fill="x")
            entry = ttk.Entry(frame, font=("Segoe UI", 10))
            entry.pack(fill="x", pady=(3, 0), ipady=3)
            return entry

        self.name = create_entry("Full Name")
        self.email = create_entry("Email Address")
        self.phone = create_entry("Phone Number")
        self.lic = create_entry("License Number")
        self.pw = create_entry("Password (leave blank to keep same)")

        row = db.run_query("SELECT * FROM driver WHERE id=?", (self.driver_id,), fetch=True)
        if row:
            data = row[0]
            self.name.insert(0, data["name"])
            self.email.insert(0, data["email"])
            self.phone.insert(0, data["phone"])
            self.lic.insert(0, data["license_number"])

        ttk.Button(
            inner,
            text="Update Driver",
            style="Primary.TButton",
            command=self.update_driver,
        ).pack(fill="x", pady=(24, 0))

        self.win.geometry("480x560")

    def update_driver(self):
        name = self.name.get().strip()
        email = self.email.get().strip()
        phone = self.phone.get().strip()
        lic = self.lic.get().strip()
        pw = self.pw.get().strip()

        if not all([name, email, phone, lic]):
            messagebox.showerror("Error", "Name, email, phone and license are required.", parent=self.win)
            return

        if len(name) < 3 or not re.match(r"^[A-Za-z\s'.-]+$", name):
            messagebox.showerror("Invalid Name", "Enter a valid name (at least 3 letters, letters and spaces only).", parent=self.win)
            return

        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            messagebox.showerror("Invalid Email", "Enter a valid email address.", parent=self.win)
            return

        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Invalid Phone", "Enter a valid 10-digit phone number.", parent=self.win)
            return

        if len(lic) < 3 or not re.match(r"^[A-Za-z0-9\- ]+$", lic):
            messagebox.showerror("Invalid License", "Enter a valid license number.", parent=self.win)
            return

        if pw:
            if len(pw) < 6:
                messagebox.showerror("Weak Password", "Password must be at least 6 characters long.", parent=self.win)
                return
            if not re.search(r"[A-Za-z]", pw) or not re.search(r"\d", pw):
                messagebox.showerror("Weak Password", "Password must contain at least one letter and one number.", parent=self.win)
                return

            q = """
            UPDATE driver
            SET name=?, email=?, phone=?, license_number=?, password=?
            WHERE id=?
            """
            params = (name, email, phone, lic, pw, self.driver_id)
        else:
            q = """
            UPDATE driver
            SET name=?, email=?, phone=?, license_number=?
            WHERE id=?
            """
            params = (name, email, phone, lic, self.driver_id)

        try:
            db.run_query(q, params)
            messagebox.showinfo("Success", "Driver updated successfully.", parent=self.win)
            self.win.destroy()
            self.manager.load()
        except Exception as e:
            err = str(e)
            if "UNIQUE constraint failed" in err and "driver.email" in err:
                messagebox.showerror("Email Exists", "This email is already registered for another driver.", parent=self.win)
            else:
                messagebox.showerror("Error", f"Failed to update driver: {err}", parent=self.win)


#  Trip Manager 
class TripManager:
    def __init__(self, parent):
        self.parent = parent
        self.win = tk.Toplevel(parent)
        self.win.title("Trip Records • FastTrack")
        self.win.configure(bg=PRIMARY_DARK)

        center_on_parent(self.win, parent, 1200, 600)
        make_modal(self.win, parent)

        top_frame = tk.Frame(self.win, bg=PRIMARY_DARK)
        top_frame.pack(fill="x", padx=24, pady=20)

        tk.Label(
            top_frame,
            text="Trip History",
            font=("Segoe UI", 18, "bold"),
            bg=PRIMARY_DARK,
            fg=TEXT_LIGHT,
        ).pack(side="left")

        ttk.Button(
            top_frame,
            text="Refresh Data",
            style="Secondary.TButton",
            command=self.load,
        ).pack(side="right")

        tree_frame = tk.Frame(self.win, bg=CARD_BG, bd=1, relief=tk.SOLID)
        tree_frame.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        columns = (
            "id", "customer", "driver", "pickup", "dropoff",
            "pick_date", "pick_time", "drop_date", "drop_time",
            "fare", "status",
        )

        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Treeview")

        head_names = [
            "ID", "Customer", "Driver", "Pickup", "Dropoff",
            "P. Date", "P. Time", "D. Date", "D. Time",
            "Fare", "Status",
        ]
        widths = [50, 130, 130, 190, 190, 90, 80, 90, 80, 80, 90]

        for c, name, w in zip(columns, head_names, widths):
            self.tree.heading(c, text=name)
            self.tree.column(c, width=w, anchor="center")

        y_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)

        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.tag_configure("cancelled", background="#3b0f0f", foreground="#fecaca")
        self.tree.tag_configure("completed", background="#022c22", foreground="#bbf7d0")

        self.load()

    def load(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        q = """
        SELECT t.id, c.name as customer, d.name as driver, t.pickup, t.dropoff,
               t.pickup_date, t.pickup_time, t.dropoff_date, t.dropoff_time,
               t.fare, t.status
        FROM trip t
        LEFT JOIN customer c ON t.customer_id = c.id
        LEFT JOIN driver d   ON t.driver_id   = d.id
        """
        rows = db.run_query(q, fetch=True) or []

        for r in rows:
            p_date = str(r["pickup_date"]) if r["pickup_date"] else ""
            p_time = str(r["pickup_time"]) if r["pickup_time"] else ""
            d_date = str(r["dropoff_date"]) if r["dropoff_date"] else ""
            d_time = str(r["dropoff_time"]) if r["dropoff_time"] else ""

            tags = ()
            if r["status"] == "cancelled":
                tags = ("cancelled",)
            elif r["status"] == "completed":
                tags = ("completed",)

            self.tree.insert(
                "",
                "end",
                values=(
                    r["id"],
                    r["customer"] or "-",
                    r["driver"] or "-",
                    r["pickup"],
                    r["dropoff"],
                    p_date,
                    p_time,
                    d_date,
                    d_time,
                    float(r["fare"]) if r["fare"] else 0.0,
                    r["status"],
                ),
                tags=tags,
            )


#  Payment Manager 
class PaymentManager:
    def __init__(self, parent):
        self.parent = parent
        self.win = tk.Toplevel(parent)
        self.win.title("Payment Logs • FastTrack")
        self.win.configure(bg=PRIMARY_DARK)

        center_on_parent(self.win, parent, 980, 520)
        make_modal(self.win, parent)

        top_frame = tk.Frame(self.win, bg=PRIMARY_DARK)
        top_frame.pack(fill="x", padx=24, pady=20)

        tk.Label(
            top_frame,
            text="Payment Transactions",
            font=("Segoe UI", 18, "bold"),
            bg=PRIMARY_DARK,
            fg=TEXT_LIGHT,
        ).pack(side="left")

        ttk.Button(
            top_frame,
            text="Refresh Logs",
            style="Secondary.TButton",
            command=self.load,
        ).pack(side="right")

        tree_frame = tk.Frame(self.win, bg=CARD_BG, bd=1, relief=tk.SOLID)
        tree_frame.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("id", "trip", "amount", "method", "status", "paid_at"),
            show="headings",
            style="Treeview",
        )

        headings = {
            "id": "ID",
            "trip": "Trip ID",
            "amount": "Amount",
            "method": "Method",
            "status": "Status",
            "paid_at": "Timestamp",
        }

        for c, text in headings.items():
            self.tree.heading(c, text=text)
            self.tree.column(c, anchor="center", width=140)

        y_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)

        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        self.load()

    def load(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        rows = db.run_query("SELECT * FROM payment", fetch=True) or []
        for r in rows:
            self.tree.insert(
                "",
                "end",
                values=(
                    r["id"],
                    r["trip_id"],
                    float(r["amount"]),
                    r["method"],
                    r["status"],
                    r["paid_at"],
                ),
            )


if __name__ == "__main__":
    AdminDashboard()
