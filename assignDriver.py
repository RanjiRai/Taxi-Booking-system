import tkinter as tk
from tkinter import messagebox, ttk
import databaseConnection as db

# Color theme
PRIMARY_YELLOW = "#FFC300"
PRIMARY_DARK = "#020617"
CARD_BG = "#0b1220"
TEXT_LIGHT = "#e5e7eb"
TEXT_MUTED = "#9ca3af"


class AssignDriverWindow:
    def __init__(self, root=None):
        #  WINDOW CREATION 
        self.parent = root

        if root:
            self.win = tk.Toplevel(root)
            self.make_modal()
            self.center_window(1100, 620)
        else:
            self.win = tk.Tk()
            self.win.geometry("1100x620")

        self.win.title("Assign Driver • FastTrack")
        self.win.configure(bg=PRIMARY_DARK)

        #  STYLES 
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(".", font=("Segoe UI", 10))

        style.configure(
            "Primary.TButton",
            font=("Segoe UI Semibold", 10),
            padding=6,
            background=PRIMARY_YELLOW,
            foreground=PRIMARY_DARK,
        )
        style.map("Primary.TButton", background=[("active", "#e6b000")])

        style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 10),
            padding=6,
            background="#111827",
            foreground=TEXT_LIGHT,
        )

        style.configure(
            "Treeview",
            font=("Segoe UI", 9),
            rowheight=26,
            background=PRIMARY_DARK,
            fieldbackground=PRIMARY_DARK,
            foreground=TEXT_LIGHT,
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 9, "bold"),
            background="#111827",
            foreground=TEXT_LIGHT,
        )

        #  HEADER 
        header = tk.Frame(self.win, bg=PRIMARY_DARK)
        header.pack(fill="x", padx=24, pady=(20, 10))

        tk.Label(
            header,
            text="Assign Drivers",
            font=("Segoe UI Black", 22),
            bg=PRIMARY_DARK,
            fg=TEXT_LIGHT,
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Pick a trip and assign a driver.",
            font=("Segoe UI", 10),
            bg=PRIMARY_DARK,
            fg=TEXT_MUTED,
        ).pack(anchor="w")

        #  MAIN CONTENT 
        main = tk.Frame(self.win, bg=PRIMARY_DARK)
        main.pack(fill="both", expand=True, padx=24, pady=(10, 16))

        # ---- LEFT: TRIPS ----
        left_card = tk.Frame(main, bg=CARD_BG, highlightbackground="#1f2937", highlightthickness=1)
        left_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left_card, text="Pending Trips",
                 font=("Segoe UI Semibold", 12), bg=CARD_BG, fg=TEXT_LIGHT).pack(anchor="w", padx=16, pady=(12, 4))

        trip_frame = tk.Frame(left_card, bg=CARD_BG)
        trip_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        trip_cols = ("id", "customer", "pickup", "dropoff", "date", "time")
        self.trips_tree = ttk.Treeview(trip_frame, columns=trip_cols, show="headings")

        titles = ["ID", "Customer", "Pickup", "Dropoff", "P.Date", "P.Time"]
        widths = [50, 150, 190, 190, 90, 80]

        for col, title, width in zip(trip_cols, titles, widths):
            self.trips_tree.heading(col, text=title)
            self.trips_tree.column(col, width=width, anchor="center")

        vsb_t = ttk.Scrollbar(trip_frame, orient="vertical", command=self.trips_tree.yview)
        hsb_t = ttk.Scrollbar(trip_frame, orient="horizontal", command=self.trips_tree.xview)
        self.trips_tree.configure(yscrollcommand=vsb_t.set, xscrollcommand=hsb_t.set)

        vsb_t.pack(side="right", fill="y")
        hsb_t.pack(side="bottom", fill="x")
        self.trips_tree.pack(side="left", fill="both", expand=True)

        # ---- RIGHT: DRIVERS ----
        right_card = tk.Frame(main, bg=CARD_BG, highlightbackground="#1f2937", highlightthickness=1)
        right_card.pack(side="right", fill="both", expand=True, padx=(10, 0))

        tk.Label(right_card, text="Available Drivers",
                 font=("Segoe UI Semibold", 12), bg=CARD_BG, fg=TEXT_LIGHT).pack(anchor="w", padx=16, pady=(12, 4))

        drv_frame = tk.Frame(right_card, bg=CARD_BG)
        drv_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        drv_cols = ("id", "name", "email", "phone")
        self.drv_tree = ttk.Treeview(drv_frame, columns=drv_cols, show="headings")

        d_titles = ["ID", "Name", "Email", "Phone"]
        d_widths = [50, 150, 220, 140]

        for col, title, width in zip(drv_cols, d_titles, d_widths):
            self.drv_tree.heading(col, text=title)
            self.drv_tree.column(col, width=width, anchor="center")

        vsb_d = ttk.Scrollbar(drv_frame, orient="vertical", command=self.drv_tree.yview)
        hsb_d = ttk.Scrollbar(drv_frame, orient="horizontal", command=self.drv_tree.xview)
        self.drv_tree.configure(yscrollcommand=vsb_d.set, xscrollcommand=hsb_d.set)

        vsb_d.pack(side="right", fill="y")
        hsb_d.pack(side="bottom", fill="x")
        self.drv_tree.pack(side="left", fill="both", expand=True)

        #  FOOTER BUTTONS 
        footer = tk.Frame(self.win, bg=PRIMARY_DARK)
        footer.pack(fill="x", padx=24, pady=10)

        ttk.Button(footer, text="Refresh", style="Secondary.TButton",
                   command=self.refresh).pack(side="left")

        ttk.Button(footer, text="Assign", style="Primary.TButton",
                   command=self.assign_selected).pack(side="right")

        self.refresh()

        if root is None:
            self.win.mainloop()

    #  WINDOW HELPERS 
    def make_modal(self):
        self.win.transient(self.parent)
        self.win.grab_set()
        self.win.lift()
        self.win.focus_force()

    def center_window(self, w, h):
        self.parent.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (w // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (h // 2)
        self.win.geometry(f"{w}x{h}+{x}+{y}")

    #  DATA 
    def refresh(self):
        self.load_trips()
        self.load_drivers()

    def load_trips(self):
        self.trips_tree.delete(*self.trips_tree.get_children())
        rows = db.run_query(
            """
            SELECT t.id, c.name, t.pickup, t.dropoff,
                   t.pickup_date, t.pickup_time
            FROM trip t
            LEFT JOIN customer c ON t.customer_id = c.id
            WHERE t.status='requested' AND t.driver_id IS NULL
            ORDER BY t.created_at ASC
            """,
            fetch=True,
        ) or []

        for r in rows:
            self.trips_tree.insert("", "end", values=(
                r["id"], r["name"] or "Unknown",
                r["pickup"], r["dropoff"],
                r["pickup_date"], r["pickup_time"]
            ))

    def load_drivers(self):
        self.drv_tree.delete(*self.drv_tree.get_children())
        rows = db.run_query(
            """
            SELECT id, name, email, phone
            FROM driver
            WHERE available=1
            ORDER BY name ASC
            """,
            fetch=True,
        ) or []

        for r in rows:
            self.drv_tree.insert("", "end", values=(
                r["id"], r["name"], r["email"], r["phone"]
            ))

    #  ASSIGN 
    def assign_selected(self):
        sel_trip = self.trips_tree.selection()
        sel_drv = self.drv_tree.selection()

        if not sel_trip:
            messagebox.showwarning("Trip Required", "Select a trip.", parent=self.win)
            return
        if not sel_drv:
            messagebox.showwarning("Driver Required", "Select a driver.", parent=self.win)
            return

        trip_id = int(self.trips_tree.item(sel_trip[0])["values"][0])
        driver_id = int(self.drv_tree.item(sel_drv[0])["values"][0])

        t = db.run_query("SELECT status, driver_id FROM trip WHERE id=?",
                         (trip_id,), fetch=True)
        if not t or t[0]["driver_id"] or t[0]["status"] != "requested":
            messagebox.showerror("Error", "Trip unavailable.", parent=self.win)
            self.refresh()
            return

        d = db.run_query("SELECT available, name FROM driver WHERE id=?",
                         (driver_id,), fetch=True)
        if not d or d[0]["available"] != 1:
            messagebox.showerror("Error", "Driver unavailable.", parent=self.win)
            self.refresh()
            return

        db.run_query("UPDATE trip SET driver_id=?, status='assigned' WHERE id=?",
                     (driver_id, trip_id))
        db.run_query("UPDATE driver SET available=0 WHERE id=?",
                     (driver_id,))

        messagebox.showinfo(
            "Assigned",
            f"Driver '{d[0]['name']}' assigned successfully.",
            parent=self.win
        )
        self.refresh()


if __name__ == "__main__":
    AssignDriverWindow()
