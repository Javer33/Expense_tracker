import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import math
import expense_manager as manager

# ============================================================
# COLORS
# ============================================================

BG = "#F3F6F8"
NAVY = "#142B3B"
NAVY_LIGHT = "#203F52"
TEAL = "#0F9D8A"
TEXT = "#20313D"
MUTED = "#71808B"
WHITE = "#FFFFFF"
LIGHT = "#E9EFF2"
RED = "#B94B4B"
BLUE = "#3976A8"
GOLD = "#D69B35"
PURPLE = "#8A6DB1"


# ============================================================
# EXPENSE CATEGORIES
# ============================================================

CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Health",
    "Education",
    "Entertainment",
    "Home",
    "Other",
]


# ============================================================
# MAIN APPLICATION
# ============================================================


class ExpenseTracker:

    def __init__(self, root):
        self.root = root
        self.root.title("My Smart Expenses | Expense Tracker")
        self.root.geometry("1120x720")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)

        self.expenses = []
        self.selected_id = None
        self.form_vars = {}

        self.setup_style()

        # Load saved data automatically when application starts
        try:
            self.expenses = manager.load_expenses()
        except RuntimeError as error:
            messagebox.showerror("Data Loading Problem", str(error))
            self.root.destroy()
            return

        self.build_shell()
        self.show_dashboard()

    # ========================================================
    # STYLE
    # ========================================================

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT,
            rowheight=34,
            borderwidth=0,
            font=("Segoe UI", 10),
        )

        style.configure(
            "Treeview.Heading",
            background="#E8EEF1",
            foreground=NAVY,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=9,
        )

        style.map(
            "Treeview",
            background=[("selected", "#D5F0EB")],
            foreground=[("selected", NAVY)],
        )

        style.configure("TCombobox", padding=7, font=("Segoe UI", 10))

        style.configure("TEntry", padding=8, font=("Segoe UI", 10))

    # ========================================================
    # MAIN WINDOW / SIDEBAR
    # ========================================================

    def build_shell(self):

        # ----------------------------------------------------
        # SIDEBAR
        # ----------------------------------------------------

        self.sidebar = tk.Frame(self.root, bg=NAVY, width=220)

        self.sidebar.pack(side="left", fill="y")

        self.sidebar.pack_propagate(False)

        # ----------------------------------------------------
        # APPLICATION NAME
        # ----------------------------------------------------

        tk.Label(
            self.sidebar,
            text="◈  pennywise",
            bg=NAVY,
            fg=WHITE,
            font=("Segoe UI", 19, "bold"),
        ).pack(anchor="w", padx=22, pady=(28, 4))

        # ----------------------------------------------------
        # SUBTITLE
        # ----------------------------------------------------

        tk.Label(
            self.sidebar,
            text="PERSONAL FINANCE",
            bg=NAVY,
            fg="#A9BAC4",
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", padx=24, pady=(0, 25))

        # ----------------------------------------------------
        # SIDEBAR NAVIGATION
        # ----------------------------------------------------

        self.nav_buttons = {}

        navigation = [
            ("▦   Dashboard", self.show_dashboard),
            ("＋   Add Expense", self.show_add),
            ("▤   View Expenses", self.show_all),
            ("✎   Update Expense", self.update_from_sidebar),
            ("🗑   Delete Expense", self.delete_from_sidebar),
            ("⌕   Search Expense", self.show_search),
        ]

        # ----------------------------------------------------
        # CREATE SIDEBAR BUTTONS
        # ----------------------------------------------------

        for label, command in navigation:

            button = tk.Button(
                self.sidebar,
                text=label,
                command=command,
                anchor="w",
                padx=20,
                pady=12,
                bd=0,
                bg=NAVY,
                fg="#D7E1E6",
                activebackground=NAVY_LIGHT,
                activeforeground=WHITE,
                font=("Segoe UI", 10),
                cursor="hand2",
            )

            button.pack(fill="x", padx=10, pady=2)

            self.nav_buttons[label] = button

        # ----------------------------------------------------
        # SIDEBAR FOOTER
        # ----------------------------------------------------

        tk.Label(
            self.sidebar,
            text=("Expense Manager\n" "Add • View • Update\n" "Delete • Search"),
            bg=NAVY,
            fg="#A9BAC4",
            justify="left",
            font=("Segoe UI", 8),
        ).pack(side="bottom", anchor="w", padx=24, pady=22)

        # ----------------------------------------------------
        # MAIN CONTENT AREA
        # ----------------------------------------------------

        self.main = tk.Frame(self.root, bg=BG)

        self.main.pack(side="left", fill="both", expand=True)

    # ========================================================
    # SIDEBAR UPDATE ACTION
    # ========================================================

    def update_from_sidebar(self):

        if not self.expenses:
            messagebox.showinfo(
                "Update Expense", "There are no expense records available to update."
            )
            return

        self.show_all()

        messagebox.showinfo(
            "Update Expense",
            "Select an expense from the list and click "
            "'Edit Selected' to update its details.",
        )

    # ========================================================
    # SIDEBAR DELETE ACTION
    # ========================================================

    def delete_from_sidebar(self):

        if not self.expenses:
            messagebox.showinfo(
                "Delete Expense", "There are no expense records available to delete."
            )
            return

        self.show_all()

        messagebox.showinfo(
            "Delete Expense",
            "Select an expense from the list and click "
            "'Delete Selected' to remove it.",
        )

    # ========================================================
    # CLEAR MAIN AREA
    # ========================================================

    def clear_main(self):

        for widget in self.main.winfo_children():
            widget.destroy()

    # ========================================================
    # PAGE HEADING
    # ========================================================

    def heading(self, title, subtitle):

        top = tk.Frame(self.main, bg=BG)

        top.pack(fill="x", padx=30, pady=(25, 18))

        tk.Label(top, text=title, bg=BG, fg=NAVY, font=("Segoe UI", 22, "bold")).pack(
            anchor="w"
        )

        tk.Label(top, text=subtitle, bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(
            anchor="w", pady=(4, 0)
        )

    # ========================================================
    # DASHBOARD CARD
    # ========================================================

    def card(self, parent, label, value, accent):

        frame = tk.Frame(
            parent, bg=WHITE, highlightthickness=1, highlightbackground="#E5EAED"
        )

        frame.pack(side="left", fill="both", expand=True, padx=(0, 12))

        tk.Frame(frame, bg=accent, height=4).pack(fill="x")

        tk.Label(
            frame, text=label.upper(), bg=WHITE, fg=MUTED, font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=16, pady=(13, 4))

        tk.Label(
            frame, text=value, bg=WHITE, fg=NAVY, font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=16, pady=(0, 15))

    # ========================================================
    # TABLE
    # ========================================================

    def table(self, parent, records, height=9):

        wrap = tk.Frame(parent, bg=WHITE)

        wrap.pack(fill="both", expand=True)

        columns = ("title", "category", "amount", "date", "description")

        tree = ttk.Treeview(
            wrap, columns=columns, show="headings", height=height, selectmode="browse"
        )

        headings = {
            "title": "Expense",
            "category": "Category",
            "amount": "Amount",
            "date": "Date",
            "description": "Description",
        }

        widths = {
            "title": 175,
            "category": 125,
            "amount": 105,
            "date": 115,
            "description": 260,
        }

        for column in columns:

            tree.heading(column, text=headings[column])

            tree.column(
                column,
                width=widths[column],
                minwidth=75,
                anchor="e" if column == "amount" else "w",
            )

        scrollbar = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)

        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)

        scrollbar.pack(side="right", fill="y")

        # Insert records into table
        for record in records:

            tree.insert(
                "",
                "end",
                iid=record["id"],
                values=(
                    record.get("title", ""),
                    record.get("category", ""),
                    f'{float(record.get("amount", 0)):.2f}',
                    record.get("date", ""),
                    record.get("description", ""),
                ),
            )

        return tree

    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.clear_main()

        self.heading(
            "Good to see you, Javeria", "Here's a clear view of your spending."
        )

        today = date.today()

        # ----------------------------------------------------
        # DASHBOARD ADD BUTTON
        # ----------------------------------------------------

        tk.Button(
            self.main,
            text="＋  Add a New Expense",
            command=self.show_add,
            bg=TEAL,
            fg=WHITE,
            activebackground="#0B8274",
            activeforeground=WHITE,
            bd=0,
            padx=18,
            pady=10,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        ).pack(anchor="e", padx=30, pady=(0, 18))

        # ----------------------------------------------------
        # TOTAL EXPENSES
        # ----------------------------------------------------

        total = sum(float(expense.get("amount", 0)) for expense in self.expenses)

        # ----------------------------------------------------
        # THIS MONTH
        # ----------------------------------------------------

        month_total = sum(
            float(expense.get("amount", 0))
            for expense in self.expenses
            if expense.get("date", "").startswith(today.strftime("%Y-%m"))
        )

        # ----------------------------------------------------
        # HIGHEST EXPENSE
        # ----------------------------------------------------

        highest = max(
            (float(expense.get("amount", 0)) for expense in self.expenses), default=0
        )

        # ----------------------------------------------------
        # SUMMARY CARDS
        # ----------------------------------------------------

        cards = tk.Frame(self.main, bg=BG)

        cards.pack(fill="x", padx=30, pady=(0, 22))

        self.card(cards, "Total Expenses", f"{total:,.2f}", TEAL)

        self.card(cards, "Transactions", str(len(self.expenses)), BLUE)

        self.card(cards, "This Month", f"{month_total:,.2f}", GOLD)

        self.card(cards, "Largest Expense", f"{highest:,.2f}", PURPLE)

        # ----------------------------------------------------
        # LOWER SECTION
        # ----------------------------------------------------

        lower = tk.Frame(self.main, bg=BG)

        lower.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        # ----------------------------------------------------
        # RECENT EXPENSES
        # ----------------------------------------------------

        left = tk.Frame(lower, bg=WHITE, padx=15, pady=14)

        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        tk.Label(
            left,
            text="Recent Expenses",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", pady=(0, 12))

        recent = sorted(
            self.expenses, key=lambda item: item.get("date", ""), reverse=True
        )[:8]

        self.table(left, recent, height=9)

        # ----------------------------------------------------
        # CATEGORY SECTION
        # ----------------------------------------------------

        right = tk.Frame(lower, bg=WHITE, width=220, padx=16, pady=14)

        right.pack(side="left", fill="y")

        right.pack_propagate(False)

        tk.Label(
            right, text="By Category", bg=WHITE, fg=NAVY, font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", pady=(0, 12))

        categories = {}

        for item in self.expenses:

            category = item.get("category", "Other")

            amount = float(item.get("amount", 0))

            categories[category] = categories.get(category, 0) + amount

        if not categories:

            tk.Label(
                right,
                text=("Your category totals\n" "will appear here."),
                bg=WHITE,
                fg=MUTED,
                justify="left",
            ).pack(anchor="w")

        else:

            for name, amount in sorted(
                categories.items(), key=lambda pair: pair[1], reverse=True
            )[:7]:

                tk.Label(
                    right,
                    text=f"{name}  •  {amount:.2f}",
                    bg=WHITE,
                    fg=TEXT,
                    font=("Segoe UI", 9),
                ).pack(anchor="w", pady=(5, 2))

                bar = ttk.Progressbar(right, maximum=max(total, 1), value=amount)

                bar.pack(fill="x", pady=(0, 4))

    # ========================================================
    # ADD / UPDATE EXPENSE FORM
    # ========================================================

    def show_add(self, record=None):

        self.clear_main()

        editing = record is not None

        if editing:

            self.selected_id = record["id"]

            title = "Update Expense"
            subtitle = "Modify the selected expense details."

        else:

            self.selected_id = None

            title = "Add an Expense"
            subtitle = "Enter the details of your new expense."

        self.heading(title, subtitle)

        # ----------------------------------------------------
        # FORM PANEL
        # ----------------------------------------------------

        panel = tk.Frame(
            self.main,
            bg=WHITE,
            padx=25,
            pady=22,
            highlightthickness=1,
            highlightbackground="#E5EAED",
        )

        panel.pack(fill="x", padx=30)

        panel.columnconfigure(1, weight=1)

        self.form_vars = {}

        # ----------------------------------------------------
        # REQUIRED FIELDS
        # ----------------------------------------------------

        fields = [
            ("title", "Expense Title *"),
            ("category", "Category *"),
            ("amount", "Amount *"),
            ("date", "Date *"),
        ]

        initial = record or {}

        for row, (key, label) in enumerate(fields):

            tk.Label(
                panel, text=label, bg=WHITE, fg=TEXT, font=("Segoe UI", 10, "bold")
            ).grid(row=row, column=0, sticky="w", padx=(0, 20), pady=9)

            if key == "date":
                default_value = date.today().isoformat()
            else:
                default_value = ""

            value = initial.get(key, default_value)

            var = tk.StringVar(value=str(value))

            if key == "category":

                widget = ttk.Combobox(
                    panel, textvariable=var, values=CATEGORIES, state="normal"
                )

            else:

                widget = ttk.Entry(panel, textvariable=var)

            widget.grid(row=row, column=1, sticky="ew", pady=9)

            self.form_vars[key] = var

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        tk.Label(
            panel, text="Description", bg=WHITE, fg=TEXT, font=("Segoe UI", 10, "bold")
        ).grid(row=4, column=0, sticky="nw", padx=(0, 20), pady=9)

        self.description = tk.Text(
            panel, height=4, wrap="word", font=("Segoe UI", 10), bd=1, relief="solid"
        )

        self.description.grid(row=4, column=1, sticky="ew", pady=9)

        self.description.insert("1.0", initial.get("description", ""))

        # ----------------------------------------------------
        # FORM BUTTONS
        # ----------------------------------------------------

        buttons = tk.Frame(panel, bg=WHITE)

        buttons.grid(row=5, column=1, sticky="e", pady=(15, 0))

        tk.Button(
            buttons,
            text="Clear",
            command=self.clear_form,
            bg=LIGHT,
            fg=NAVY,
            bd=0,
            padx=18,
            pady=9,
            cursor="hand2",
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Update Expense" if editing else "Save Expense",
            command=self.save_form,
            bg=TEAL,
            fg=WHITE,
            bd=0,
            padx=20,
            pady=9,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        ).pack(side="left", padx=5)

    # ========================================================
    # CLEAR FORM
    # ========================================================

    def clear_form(self):

        for key, variable in self.form_vars.items():

            if key == "date":

                variable.set(date.today().isoformat())

            else:

                variable.set("")

        self.description.delete("1.0", "end")

        self.selected_id = None

    # ========================================================
    # SAVE / UPDATE FORM
    # ========================================================

    def save_form(self):

        title = self.form_vars["title"].get().strip()
        category = self.form_vars["category"].get().strip()
        amount_text = self.form_vars["amount"].get().strip()
        date_text = self.form_vars["date"].get().strip()

        description = self.description.get("1.0", "end").strip()

        # ----------------------------------------------------
        # TITLE VALIDATION
        # ----------------------------------------------------

        if not title:

            messagebox.showwarning("Invalid Input", "Please enter an expense title.")

            return

        # ----------------------------------------------------
        # CATEGORY VALIDATION
        # ----------------------------------------------------

        if not category:

            messagebox.showwarning(
                "Invalid Input", "Please choose or enter a category."
            )

            return

        # ----------------------------------------------------
        # AMOUNT VALIDATION
        # ----------------------------------------------------

        try:

            amount = float(amount_text)

            if not math.isfinite(amount) or amount <= 0:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Amount", "Enter a valid amount greater than zero."
            )

            return

        # ----------------------------------------------------
        # DATE VALIDATION
        # ----------------------------------------------------

        try:

            manager.validate_date(date_text)

        except ValueError:

            messagebox.showwarning("Invalid Date", "Please use the format YYYY-MM-DD.")

            return

        # ----------------------------------------------------
        # ADD OR UPDATE
        # ----------------------------------------------------

        try:

            if self.selected_id:

                self.expenses = manager.update_expense(
                    self.expenses,
                    self.selected_id,
                    title,
                    category,
                    amount,
                    date_text,
                    description,
                )

                message = "Expense updated successfully."

            else:

                self.expenses = manager.add_expense(
                    self.expenses, title, category, amount, date_text, description
                )

                message = "Expense added successfully."

        except (RuntimeError, ValueError) as error:

            messagebox.showerror("Could Not Save", str(error))

            return

        messagebox.showinfo("Success", message)

        self.selected_id = None

        self.show_dashboard()

    # ========================================================
    # VIEW ALL EXPENSES
    # ========================================================

    def show_all(self):

        self.clear_main()

        self.heading(
            "All Expenses", "View, update, or delete your saved expense records."
        )

        # ----------------------------------------------------
        # TABLE PANEL
        # ----------------------------------------------------

        panel = tk.Frame(self.main, bg=WHITE, padx=16, pady=16)

        panel.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        # ----------------------------------------------------
        # ACTION BUTTONS
        # ----------------------------------------------------

        actions = tk.Frame(panel, bg=WHITE)

        actions.pack(fill="x", pady=(0, 14))

        tk.Button(
            actions,
            text="＋  Add Expense",
            command=self.show_add,
            bg=TEAL,
            fg=WHITE,
            activebackground="#0B8274",
            activeforeground=WHITE,
            bd=0,
            padx=18,
            pady=11,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            actions,
            text="✎  Edit Selected",
            command=self.edit_selected,
            bg=BLUE,
            fg=WHITE,
            activebackground="#2C628D",
            activeforeground=WHITE,
            bd=0,
            padx=18,
            pady=11,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            actions,
            text="Delete Selected",
            command=self.delete_selected,
            bg=RED,
            fg=WHITE,
            activebackground="#993B3B",
            activeforeground=WHITE,
            bd=0,
            padx=18,
            pady=11,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        ).pack(side="left")

        tk.Button(
            actions,
            text="Refresh",
            command=self.show_all,
            bg=LIGHT,
            fg=NAVY,
            bd=0,
            padx=16,
            pady=11,
            cursor="hand2",
        ).pack(side="right")

        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        self.all_tree = self.table(panel, self.expenses, height=14)

    # ========================================================
    # GET SELECTED RECORD
    # ========================================================

    def selected_record(self, tree):

        selection = tree.selection()

        if not selection:

            messagebox.showwarning("No Selection", "Please select an expense first.")

            return None

        record_id = selection[0]

        for expense in self.expenses:

            if expense["id"] == record_id:
                return expense

        return None

    # ========================================================
    # EDIT SELECTED EXPENSE
    # ========================================================

    def edit_selected(self):

        record = self.selected_record(self.all_tree)

        if record:

            self.show_add(record)

    # ========================================================
    # DELETE SELECTED EXPENSE
    # ========================================================

    def delete_selected(self):

        record = self.selected_record(self.all_tree)

        if not record:
            return

        confirmation = messagebox.askyesno(
            "Confirm Deletion", f'Delete "{record["title"]}" permanently?'
        )

        if not confirmation:
            return

        try:

            self.expenses = manager.delete_expense(self.expenses, record["id"])

        except (RuntimeError, ValueError) as error:

            messagebox.showerror("Could Not Delete", str(error))

            return

        messagebox.showinfo("Deleted", "Expense deleted successfully.")

        self.show_all()

    # ========================================================
    # SEARCH PAGE
    # ========================================================

    def show_search(self):

        self.clear_main()

        self.heading("Search Expenses", "Find expenses by title, category, or date.")

        # ----------------------------------------------------
        # SEARCH CONTROLS
        # ----------------------------------------------------

        controls = tk.Frame(self.main, bg=WHITE, padx=16, pady=16)

        controls.pack(fill="x", padx=30, pady=(0, 14))

        # Search text

        self.search_var = tk.StringVar()

        ttk.Entry(controls, textvariable=self.search_var).pack(
            side="left", fill="x", expand=True, padx=(0, 10)
        )

        # Search field

        self.search_by = tk.StringVar(value="Title")

        ttk.Combobox(
            controls,
            textvariable=self.search_by,
            values=["Title", "Category", "Date"],
            state="readonly",
            width=14,
        ).pack(side="left", padx=(0, 10))

        # Search button

        tk.Button(
            controls,
            text="Search",
            command=self.run_search,
            bg=TEAL,
            fg=WHITE,
            bd=0,
            padx=18,
            pady=9,
            cursor="hand2",
        ).pack(side="left", padx=(0, 8))

        # Clear button

        tk.Button(
            controls,
            text="Clear",
            command=self.clear_search,
            bg=LIGHT,
            fg=NAVY,
            bd=0,
            padx=18,
            pady=9,
            cursor="hand2",
        ).pack(side="left")

        # ----------------------------------------------------
        # SEARCH RESULTS
        # ----------------------------------------------------

        self.search_result_frame = tk.Frame(self.main, bg=WHITE, padx=16, pady=16)

        self.search_result_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        self.search_tree = self.table(
            self.search_result_frame, self.expenses, height=14
        )

    # ========================================================
    # RUN SEARCH
    # ========================================================

    def run_search(self):

        query = self.search_var.get().strip().casefold()

        field = {"Title": "title", "Category": "category", "Date": "date"}.get(
            self.search_by.get()
        )

        if not field:

            messagebox.showwarning("Search", "Please choose a search field.")

            return

        if not query:

            messagebox.showwarning("Search", "Please enter something to search for.")

            return

        matches = [
            item
            for item in self.expenses
            if query in str(item.get(field, "")).casefold()
        ]

        self.search_tree.destroy()

        self.search_tree = self.table(self.search_result_frame, matches, height=14)

        if not matches:

            messagebox.showinfo("No Results", "No matching expenses were found.")

    # ========================================================
    # CLEAR SEARCH
    # ========================================================

    def clear_search(self):

        self.search_var.set("")
        self.search_by.set("Title")

        self.search_tree.destroy()

        self.search_tree = self.table(
            self.search_result_frame, self.expenses, height=14
        )


# ============================================================
# PROGRAM START
# ============================================================


def main():

    root = tk.Tk()

    ExpenseTracker(root)

    root.mainloop()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    main()
