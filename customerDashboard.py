import tkinter as tk
from tkinter import messagebox, ttk
import databaseConnection as db
import re

# Theme colors
PRIMARY_YELLOW = "#FFC300"
PRIMARY_DARK = "#020617"
CARD_BG = "#0b1220"
TEXT_LIGHT = "#e5e7eb"
TEXT_MUTED = "#9ca3af"
ACCENT_BLUE = "#38bdf8"


# Configure ttk styles
def apply_styles():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(".", font=("Segoe UI", 10))

    # Main buttons
    for name in ("Primary.TButton", "Yellow.TButton"):
        style.configure(
            name,
            font=("Segoe UI Semibold", 10),
            padding=6,
            background=PRIMARY_YELLOW,
            foreground=PRIMARY_DARK,
            borderwidth=0,
        )
        style.map(name, background=[("active", "#e6b000")])

    # Secondary button
    style.configure(
        "Secondary.TButton",
        font=("Segoe UI", 10),
        padding=6,
        background="#111827",
        foreground=TEXT_LIGHT,
        borderwidth=0,
    )
    style.map("Secondary.TButton", background=[("active", "#1f2937")])

    # Treeview
    style.configure(
        "Treeview",
        font=("Segoe UI", 9),
        rowheight=25,
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


class CustomerDashboard:
    def __init__(self, customer):
        self.customer = customer
        self.win = tk.Tk()
        self.win.title(f"Customer Dashboard • {customer['name']}")
        self.win.geometry("1200x700")
        self.win.configure(bg=PRIMARY_DARK)

        apply_styles()

        # Header
        header = tk.Frame(self.win, bg=PRIMARY_DARK, height=80)
        header.pack(fill="x", side="top", padx=24, pady=(20, 10))
        header.pack_propagate(False)

        # Header left
        title_box = tk.Frame(header, bg=PRIMARY_DARK)
        title_box.pack(side="left")

        tk.Label(
            title_box,
            text="FastTrack Customer",
            font=("Segoe UI", 20, "bold"),
            bg=PRIMARY_DARK,
            fg=TEXT_LIGHT,
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="Book rides, track your trips, and manage bookings.",
            font=("Segoe UI", 10),
            bg=PRIMARY_DARK,
            fg=TEXT_MUTED,
        ).pack(anchor="w")

        # Header right
        welcome_box = tk.Frame(header, bg=PRIMARY_DARK)
        welcome_box.pack(side="right")

        tk.Label(
            welcome_box,
            text=f"Welcome, {customer['name']}",
            font=("Segoe UI", 12, "bold"),
            bg=PRIMARY_DARK,
            fg=PRIMARY_YELLOW,
        ).pack(anchor="e")

        # Main layout
        main_frame = tk.Frame(self.win, bg=PRIMARY_DARK)
        main_frame.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        # Left: booking form
        left_frame = tk.Frame(
            main_frame,
            bg=CARD_BG,
            bd=0,
            highlightthickness=1,
            highlightbackground="#1f2937",
        )
        left_frame.pack(side="left", fill="y", padx=(0, 18), ipadx=10, ipady=10)

        # Right: trip history
        right_frame = tk.Frame(
            main_frame,
            bg=CARD_BG,
            bd=0,
            highlightthickness=1,
            highlightbackground="#1f2937",
        )
        right_frame.pack(side="right", fill="both", expand=True, ipadx=10, ipady=10)

        # Booking form title
        tk.Label(
            left_frame,
            text="Book a Ride",
            font=("Segoe UI", 16, "bold"),
            bg=CARD_BG,
            fg=TEXT_LIGHT,
        ).pack(pady=(12, 8), padx=20, anchor="w")

        tk.Label(
            left_frame,
            text="Enter your trip details and confirm payment.",
            font=("Segoe UI", 9),
            bg=CARD_BG,
            fg=TEXT_MUTED,
        ).pack(pady=(0, 12), padx=20, anchor="w")

        form_container = tk.Frame(left_frame, bg=CARD_BG)
        form_container.pack(fill="x", padx=20, pady=(0, 10))

        self.pick = self.create_form_entry(form_container, "Pickup Location", 0)
        self.drop = self.create_form_entry(form_container, "Dropoff Location", 1)
        self.pick_date = self.create_form_entry(
            form_container, "Pickup Date (YYYY-MM-DD)", 2
        )
        self.pick_time = self.create_form_entry(
            form_container, "Pickup Time (HH:MM:SS)", 3
        )
        self.drop_date = self.create_form_entry(
            form_container, "Dropoff Date (Optional)", 4
        )
        self.drop_time = self.create_form_entry(
            form_container, "Dropoff Time (Optional)", 5
        )
        self.fare = self.create_form_entry(
            form_container, "Estimated Fare (Rs.)", 6
        )

        ttk.Button(
            left_frame,
            text="Proceed to Payment",
            style="Primary.TButton",
            command=self.open_payment_window,
        ).pack(pady=18, fill="x", padx=20)

        tk.Label(
            left_frame,
            text="Note: Drivers will be assigned by the admin.",
            font=("Segoe UI", 8),
            bg=CARD_BG,
            fg=TEXT_MUTED,
        ).pack(pady=(0, 10), padx=20, anchor="w")

        # Trip history title
        tk.Label(
            right_frame,
            text="My Trips",
            font=("Segoe UI", 16, "bold"),
            bg=CARD_BG,
            fg=TEXT_LIGHT,
        ).pack(pady=(12, 8), padx=20, anchor="w")

        tk.Label(
            right_frame,
            text="View, update, or cancel your bookings.",
            font=("Segoe UI", 9),
            bg=CARD_BG,
            fg=TEXT_MUTED,
        ).pack(pady=(0, 10), padx=20, anchor="w")

        tree_container = tk.Frame(right_frame, bg=CARD_BG)
        tree_container.pack(fill="both", expand=True, padx=20)

        cols = (
            "id",
            "driver",
            "pickup",
            "dropoff",
            "pick_date",
            "pick_time",
            "drop_date",
            "drop_time",
            "fare",
            "status",
        )
        self.tree = ttk.Treeview(
            tree_container, columns=cols, show="headings", style="Treeview"
        )

        widths = [40, 120, 160, 160, 80, 80, 80, 80, 80, 90]
        headings = [
            "ID",
            "Driver",
            "Pickup",
            "Dropoff",
            "P.Date",
            "P.Time",
            "D.Date",
            "D.Time",
            "Fare",
            "Status",
        ]
        for col, w, h in zip(cols, widths, headings):
            self.tree.heading(col, text=h)
            self.tree.column(col, width=w, anchor="center")

        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        # Trip action buttons
        btn_box = tk.Frame(right_frame, bg=CARD_BG)
        btn_box.pack(fill="x", padx=20, pady=16)

        ttk.Button(
            btn_box,
            text="Refresh List",
            style="Secondary.TButton",
            command=self.show_trips,
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            btn_box,
            text="Update Selected",
            style="Secondary.TButton",
            command=self.open_update_window,
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            btn_box,
            text="Cancel Selected",
            style="Secondary.TButton",
            command=self.cancel_trip_handler,
        ).pack(side="left")

        self.show_trips()
        self.win.mainloop()

    #  helpers to keep popups tied to parent 
    def center_window(self, win, w, h):
        self.win.update_idletasks()
        x = self.win.winfo_x() + (self.win.winfo_width() // 2) - (w // 2)
        y = self.win.winfo_y() + (self.win.winfo_height() // 2) - (h // 2)
        win.geometry(f"{w}x{h}+{x}+{y}")

    def make_modal(self, child):
        child.transient(self.win)   # attach to parent
        child.grab_set()            # modal
        child.lift()
        child.focus_force()

    # 

    def create_form_entry(self, parent, label, row):
        tk.Label(
            parent,
            text=label,
            font=("Segoe UI", 9, "bold"),
            bg=CARD_BG,
            fg=TEXT_LIGHT,
        ).grid(row=row, column=0, sticky="w", pady=(5, 0))
        entry = ttk.Entry(parent, font=("Segoe UI", 10), width=32)
        entry.grid(row=row, column=1, sticky="w", pady=(0, 10), padx=(10, 0))
        return entry

    def validate_datetime(self, date_str, time_str):
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        time_pattern = r"^\d{2}:\d{2}:\d{2}$"
        if date_str and not re.match(date_pattern, date_str):
            return "Date must be in YYYY-MM-DD format."
        if time_str and not re.match(time_pattern, time_str):
            return "Time must be in HH:MM:SS (24hr) format."
        return None

    def cancel_trip_handler(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning(
                "Selection Required",
                "Please select a trip from the list to cancel.",
                parent=self.win,
            )
            return

        trip_data = self.tree.item(selected_item, "values")
        trip_id = trip_data[0]
        trip_status = str(trip_data[-1]).lower()

        if trip_status in ["completed", "cancelled"]:
            messagebox.showerror("Error", f"Trip is already {trip_status}.", parent=self.win)
            return

        if messagebox.askyesno("Confirm", f"Cancel trip ID {trip_id}?", parent=self.win):
            self.cancel_trip(trip_id)

    def cancel_trip(self, trip_id):
        trip_info = db.run_query(
            "SELECT driver_id, status FROM trip WHERE id=?",
            (trip_id,),
            fetch=True,
        )
        if not trip_info:
            return

        driver_id = trip_info[0]["driver_id"]
        try:
            db.run_query(
                "UPDATE trip SET status='cancelled', dropoff_date=NULL, dropoff_time=NULL WHERE id=?",
                (trip_id,),
            )
            if driver_id:
                db.run_query("UPDATE driver SET available=1 WHERE id=?", (driver_id,))
            messagebox.showinfo("Success", "Trip cancelled.", parent=self.win)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to cancel: {e}", parent=self.win)

        self.show_trips()

    def open_update_window(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a trip to update.", parent=self.win)
            return

        trip_data = self.tree.item(selected_item, "values")
        trip_id, trip_status = trip_data[0], str(trip_data[-1]).lower()

        if trip_status != "requested":
            messagebox.showerror("Error", "Only 'requested' trips can be updated.", parent=self.win)
            return

        current_data = db.run_query(
            "SELECT pickup, dropoff, pickup_date, pickup_time, dropoff_date, dropoff_time, fare FROM trip WHERE id=?",
            (trip_id,),
            fetch=True,
        )
        if not current_data:
            return
        data = current_data[0]

        update_win = tk.Toplevel(self.win)
        update_win.title(f"Update Trip {trip_id}")
        update_win.configure(bg=PRIMARY_DARK)

        self.center_window(update_win, 460, 580)
        self.make_modal(update_win)

        card = tk.Frame(
            update_win,
            bg=CARD_BG,
            bd=0,
            highlightthickness=1,
            highlightbackground="#1f2937",
        )
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        accent = tk.Frame(card, bg=PRIMARY_YELLOW, height=3)
        accent.pack(fill="x", side="top")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=24, pady=24)

        tk.Label(
            inner,
            text=f"Update Trip ID: {trip_id}",
            font=("Segoe UI", 14, "bold"),
            bg=CARD_BG,
            fg=TEXT_LIGHT,
        ).pack(pady=(0, 16), anchor="w")

        def create_u_entry(label, val):
            frame = tk.Frame(inner, bg=CARD_BG)
            frame.pack(fill="x", pady=5)
            tk.Label(
                frame,
                text=label,
                font=("Segoe UI", 9, "bold"),
                bg=CARD_BG,
                fg=TEXT_LIGHT,
            ).pack(anchor="w")
            e = ttk.Entry(frame, width=40)
            e.insert(0, str(val or ""))
            e.pack(fill="x", pady=(2, 0))
            return e

        self.u_pick = create_u_entry("Pickup Location", data["pickup"])
        self.u_drop = create_u_entry("Dropoff Location", data["dropoff"])
        self.u_pick_date = create_u_entry("Pickup Date", data["pickup_date"])
        self.u_pick_time = create_u_entry("Pickup Time", data["pickup_time"])
        self.u_drop_date = create_u_entry("Dropoff Date (Opt.)", data["dropoff_date"])
        self.u_drop_time = create_u_entry("Dropoff Time (Opt.)", data["dropoff_time"])
        self.u_fare = create_u_entry("New Fare", float(data["fare"]))

        ttk.Button(
            inner,
            text="Confirm Update",
            style="Primary.TButton",
            command=lambda: self.confirm_update(update_win, trip_id),
        ).pack(pady=18, fill="x")

    def confirm_update(self, window, trip_id):
        vals = [
            self.u_pick.get(),
            self.u_drop.get(),
            self.u_fare.get(),
            self.u_pick_date.get(),
            self.u_pick_time.get(),
        ]
        if not all(v.strip() for v in vals):
            messagebox.showerror("Error", "All required fields must be filled.", parent=window)
            return

        err = self.validate_datetime(self.u_pick_date.get(), self.u_pick_time.get())
        if err:
            messagebox.showerror("Error", err, parent=window)
            return

        try:
            q = """
            UPDATE trip SET pickup=?, dropoff=?, pickup_date=?, pickup_time=?,
                            dropoff_date=?, dropoff_time=?, fare=?
            WHERE id=? AND status='requested'
            """
            db.run_query(
                q,
                (
                    self.u_pick.get(),
                    self.u_drop.get(),
                    self.u_pick_date.get(),
                    self.u_pick_time.get(),
                    self.u_drop_date.get() or None,
                    self.u_drop_time.get() or None,
                    float(self.u_fare.get()),
                    trip_id,
                ),
            )
            messagebox.showinfo("Success", "Trip updated.", parent=window)
            window.destroy()
            self.show_trips()
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}", parent=window)

    def show_trips(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        q = """
        SELECT t.id, d.name AS driver, t.pickup, t.dropoff, t.pickup_date, t.pickup_time,
               t.dropoff_date, t.dropoff_time, t.fare, t.status
        FROM trip t
        LEFT JOIN driver d ON t.driver_id = d.id
        WHERE t.customer_id=?
        ORDER BY t.created_at DESC
        """
        rows = db.run_query(q, (self.customer["id"],), fetch=True) or []
        for r in rows:
            self.tree.insert(
                "",
                "end",
                values=(
                    r["id"],
                    r["driver"] or "Not assigned",
                    r["pickup"],
                    r["dropoff"],
                    str(r["pickup_date"]),
                    str(r["pickup_time"]),
                    str(r["dropoff_date"] or ""),
                    str(r["dropoff_time"] or ""),
                    float(r["fare"]),
                    r["status"],
                ),
            )

    def clear_booking_form(self):
        for entry in (
            self.pick,
            self.drop,
            self.pick_date,
            self.pick_time,
            self.drop_date,
            self.drop_time,
            self.fare,
        ):
            entry.delete(0, tk.END)

    def open_payment_window(self):
        vals = [
            self.pick.get(),
            self.drop.get(),
            self.fare.get(),
            self.pick_date.get(),
            self.pick_time.get(),
        ]
        if not all(v.strip() for v in vals):
            messagebox.showerror("Error", "Please fill all required fields.", parent=self.win)
            return

        err = self.validate_datetime(self.pick_date.get(), self.pick_time.get())
        if err:
            messagebox.showerror("Error", err, parent=self.win)
            return

        try:
            self.temp_fare = float(self.fare.get())
        except Exception:
            messagebox.showerror("Error", "Invalid fare amount.", parent=self.win)
            return

        pay_win = tk.Toplevel(self.win)
        pay_win.title("Payment Gateway")
        pay_win.configure(bg=PRIMARY_DARK)

        self.center_window(pay_win, 420, 380)
        self.make_modal(pay_win)

        card = tk.Frame(
            pay_win,
            bg=CARD_BG,
            bd=0,
            highlightthickness=1,
            highlightbackground="#1f2937",
        )
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        accent = tk.Frame(card, bg=PRIMARY_YELLOW, height=3)
        accent.pack(fill="x", side="top")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(fill="both", expand=True, padx=24, pady=24)

        tk.Label(
            inner,
            text="Confirm Payment",
            font=("Segoe UI", 14, "bold"),
            bg=CARD_BG,
            fg=TEXT_LIGHT,
        ).pack(pady=(0, 16))

        tk.Label(
            inner,
            text=f"Total Amount: Rs. {self.temp_fare}",
            font=("Segoe UI", 12),
            bg=CARD_BG,
            fg="lightgreen",
        ).pack(pady=8)

        tk.Label(
            inner,
            text="Select Wallet",
            font=("Segoe UI", 10),
            bg=CARD_BG,
            fg=TEXT_MUTED,
        ).pack(pady=(18, 4))

        self.payment_method = ttk.Combobox(
            inner,
            values=["eSewa", "Khalti", "Fonepay"],
            state="readonly",
            width=28,
        )
        self.payment_method.pack()
        self.payment_method.current(0)

        ttk.Button(
            inner,
            text="Pay & Book",
            style="Primary.TButton",
            command=lambda: self.process_payment(pay_win),
        ).pack(pady=28, fill="x")

    def process_payment(self, window):
        try:
            method = self.payment_method.get()

            pay_id = db.run_query(
                "INSERT INTO payment (trip_id, amount, method, status) VALUES (NULL, ?, ?, 'paid')",
                (self.temp_fare, method),
            )

            driver_id = None
            status = "requested"

            trip_id = db.run_query(
                """
                INSERT INTO trip (customer_id, driver_id, pickup, dropoff, pickup_date, pickup_time,
                                  dropoff_date, dropoff_time, fare, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.customer["id"],
                    driver_id,
                    self.pick.get(),
                    self.drop.get(),
                    self.pick_date.get(),
                    self.pick_time.get(),
                    self.drop_date.get() or None,
                    self.drop_time.get() or None,
                    self.temp_fare,
                    status,
                ),
            )

            db.run_query("UPDATE payment SET trip_id=? WHERE id=?", (trip_id, pay_id))

            window.destroy()
            messagebox.showinfo("Success", f"Trip booked successfully! Status: {status}", parent=self.win)
            self.show_trips()
            self.clear_booking_form()

        except Exception as e:
            messagebox.showerror("Error", f"Payment/Booking failed: {e}", parent=window)
