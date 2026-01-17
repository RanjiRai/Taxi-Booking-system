import tkinter as tk
from tkinter import messagebox
import databaseConnection as db


def process_payment(parent, trip_id, amount):
    """Payment window attached to parent (no extra Tk root)."""

    # Create a child window, not a new Tk()
    win = tk.Toplevel(parent)
    win.title("Payment")
    win.configure(bg="white")
    win.resizable(False, False)

    W, H = 320, 220

    # Center on parent
    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() // 2) - (W // 2)
    y = parent.winfo_y() + (parent.winfo_height() // 2) - (H // 2)
    win.geometry(f"{W}x{H}+{x}+{y}")

    # Make modal (stays with current process)
    win.transient(parent)
    win.grab_set()
    win.lift()
    win.focus_force()

    tk.Label(win, text=f"Trip ID: {trip_id}", bg="white").pack(pady=4)
    tk.Label(win, text=f"Amount: {amount}", bg="white").pack(pady=4)

    tk.Label(win, text="Payment Method", bg="white").pack()
    method = tk.StringVar(value="eSewa")
    tk.OptionMenu(win, method, "eSewa", "Fonepay", "Cash").pack()

    def pay():
        try:
            # Save payment
            db.run_query(
                "INSERT INTO payment (trip_id, amount, method, status) VALUES (?,?,?,?)",
                (trip_id, amount, method.get(), "paid"),
            )

            # Update trip status (only if your system uses 'paid')
            db.run_query(
                "UPDATE trip SET status='paid' WHERE id=?",
                (trip_id,),
            )

            messagebox.showinfo("Paid", "Payment recorded", parent=win)
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Payment failed:\n{e}", parent=win)

    tk.Button(win, text="Pay", command=pay).pack(pady=10)


if __name__ == "__main__":
    print("Use process_payment(parent_window, trip_id, amount) to open the payment UI.")
